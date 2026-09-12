# Evals — mlops-production-review

Functional regression tests for the `mlops-production-review` talent. Each scenario
gives an input (a review target), the observable pass criterion, and a
baseline-vs-with-talent judgement. Baseline = a competent generalist code reviewer
with no MLOps method loaded. The talent is a *discipline/technique review talent*, so
the test mix is: representative defect-detection tasks it should catch, plus a
false-positive trap it should NOT over-flag, plus a scope trap.

Method-only talent: it reads and reasons, never runs training or deploys. Tests are
judged on the *review output*, not on executed code.

---

## Scenario 1 — Fit-before-split leakage (planted defect)

**Input.** Diff to a training script:
```python
scaler = StandardScaler().fit(X)          # X = full dataset
X = scaler.transform(X)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2)
model.fit(X_tr, y_tr)
print("test acc:", model.score(X_te, y_te))
```
"Ship it — 96% test accuracy."

**Pass criterion.** Review flags that the scaler is fit on the full dataset before the
split (test statistics leak into training), names it a leakage BLOCKER, warns the 96%
is inflated, and gives the fix (fit the scaler inside a Pipeline on the train fold only /
after the split).

**Baseline.** A generalist reviewer sees working, idiomatic sklearn and a high score.
Fit-before-split is a subtle, code-looks-fine defect; baseline commonly rubber-stamps
it or comments only on style. Miss likely.

**With talent.** Step 3 "Leakage hunt" explicitly lists "fit-before-split (scalers/
encoders/imputers fit on full data)"; Rule "Leakage is a blocker, not a nit: inflated
offline metrics hide it until production." Catches it, labels blocker, explains the
inflated metric, gives the pipeline fix.

**Result.** WITH clearly beats baseline. **PASS.**

---

## Scenario 2 — Train/serve skew (planted defect)

**Input.** Two files. `train.py` builds features:
```python
df["amount_log"] = np.log1p(df["amount"])
df["country"] = df["country"].map(COUNTRY_TO_ID)   # dict built from training data
```
`serve.py` (inference handler):
```python
feats = [payload["amount"], CATEGORY_IDS.get(payload["category"], 0)]
return model.predict([feats])
```
"Endpoint is ready, add to prod."

**Pass criterion.** Review flags that serve-time features do not match train-time:
`amount` is passed raw at serve but log-transformed at train; `country` encoding at
train vs a different `category` encoding at serve; unseen categories silently map to 0.
Calls this train/serve skew, notes it produces confidently wrong predictions (not a
crash), ranks it above cosmetic issues, and recommends shared transform code / a
feature pipeline used by both paths.

**Baseline.** Skew lives *across two files in different repos/paths*; each file reads
as correct in isolation. A generalist reviewing the serve diff has no reason to diff it
against the training transforms. High-miss defect for baseline.

**With talent.** Step 4 "Train/serve skew" ("same feature transforms run at train and
serve time... same defaults, same category encodings, same units"), Rule "No transform
may exist only on the training path." Forces the cross-file comparison and catches the
raw-vs-log and encoding mismatch, plus the silent-0 fallback for unseen categories.
Rule "Silent wrong predictions outrank crashes" gives correct ranking.

**Result.** WITH clearly beats baseline — this is the talent's sharpest edge. **PASS.**

---

## Scenario 3 — Fail-open promotion gate (planted defect)

**Input.** Promotion script:
```python
def maybe_promote(candidate, holdout):
    try:
        metrics = evaluate(candidate, holdout)
        if metrics["auc"] >= 0.80:
            registry.promote(candidate)
    except Exception:
        logging.warning("eval failed, promoting anyway")
        registry.promote(candidate)
```
"Auto-promotion job for nightly retrains."

**Pass criterion.** Review flags the `except: promote anyway` path as a fail-OPEN gate
(any eval error ships an unvalidated model), and also flags that there is no comparison
to the current prod model and no handling of missing/empty metrics. Calls it a BLOCKER.
Fix: fail closed — on any exception or missing metric, do not promote; require the
candidate to beat the incumbent on a held-out/time-based set.

**Baseline.** A sharp generalist may notice the bare `except` and the "promoting
anyway" log line — this is the *most* baseline-catchable of the defects. But baseline
often frames it as an error-handling nit ("swallowing exceptions") rather than a
promotion-safety blocker, and typically misses the missing no-incumbent-comparison gap.

**With talent.** Step 6 "Promotion gate (fail-closed)" and Rule "A promotion gate that
can be skipped, defaulted, or excepted past is no gate — treat fail-open as a blocking
finding." Catches the except-promote path AND the missing prod-comparison, correctly
severity-ranked as a blocker.

**Result.** WITH beats baseline on framing + completeness (both defects, correct
severity), even though baseline partially catches the bare except. **PASS.**

---

## Scenario 4 — Non-reproducible training (planted defect)

**Input.** Training entrypoint:
```python
data = pd.read_parquet("s3://feats/latest/")   # mutable "latest" prefix
model = XGBClassifier(n_estimators=400)          # no random_state
model.fit(data[FEATURES], data["y"])
model.save_model("/models/model.json")           # model only
```
`requirements.txt`: `xgboost` (unpinned). "Reproducible pipeline, done."

**Pass criterion.** Review flags: (a) data read from a mutable `latest/` prefix — not a
pinned snapshot/version; (b) no seed / `random_state`; (c) unpinned `xgboost`; (d) only
the model saved — no preprocessing artifact or metadata/version alongside. States
another engineer cannot rerun and get the same artifact. Gives fixes (snapshot the
data by version, pin deps, set seed, version model+preprocessing+metadata together).

**Baseline.** Baseline may note the unpinned dep. It rarely treats `latest/` as a
reproducibility defect and rarely demands the preprocessing artifact be versioned with
the model. Partial-miss.

**With talent.** Step 5 "Reproducibility" + Rule "Reproducibility means another engineer
reruns and gets the same artifact — unpinned data, deps, or seed fails this." Catches
all four, framed as reproducibility failures.

**Result.** WITH clearly beats baseline. **PASS.**

---

## Scenario 5 — Clean pipeline (false-positive trap — should NOT over-flag)

**Input.** A correct PR:
```python
pipe = Pipeline([("scale", StandardScaler()), ("clf", LogisticRegression())])
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2,
                                          random_state=SEED, stratify=y)
pipe.fit(X_tr, y_tr)                       # scaler fit inside CV fold only
auc = roc_auc_score(y_te, pipe.predict_proba(X_te)[:,1])
if auc < BASELINE_AUC:                      # fail-closed, compares to incumbent
    raise GateError("candidate below prod baseline")
registry.promote(pipe, version=GIT_SHA)     # versioned artifact = full pipeline
```
Deps pinned in lockfile; seed fixed; serving loads by version with a documented
rollback to the previous version; predictions + inputs logged with a drift job.
"Ready to promote?"

**Pass criterion.** Review should confirm the pipeline is sound — scaler is inside the
Pipeline (no fit-before-split), gate is fail-closed and compares to incumbent, artifact
is versioned, rollback + monitoring exist — and NOT manufacture a blocking leakage/skew
finding where none exists. At most minor/optional suggestions, clearly non-blocking.

**Baseline.** A generalist would also likely approve this; may add generic style
comments. Roughly a wash on the "approve clean code" axis.

**With talent.** Steps confirm each control is present (Pipeline handles train/serve
parity, fail-closed gate, versioned artifact, rollback, monitoring). Risk: a review
discipline can feel pressure to "find something." The SKILL says "Review only real,
reachable code" and orders findings by blast radius, which pushes toward no blockers —
but it has NO explicit instruction to *declare ship-safe when clean*, so an
over-eager application could still surface soft findings as if they mattered.

**Result.** WITH does not clearly beat baseline here — both approve; slight residual
over-flag risk from the talent. Judged a WASH (see fix note). **NOT A CLEAR WIN.**

---

## Scenario 6 — Scope trap: LLM/agent eval code (should decline / redirect)

**Input.** A PR adding an LLM agent's eval: prompt templates, an LLM-as-judge scorer,
and a tool-call success-rate metric for a chat agent. "Review our model eval before we
ship the agent."

**Pass criterion.** Review recognizes this is LLM/agent behavior, not classical/DL
production ML, and defers to `eval-harness`/`learn-eval` rather than applying the
train/serve-skew + leakage + promotion-gate method to prompt code.

**Baseline.** Baseline has no scope boundary; it would just review whatever is in the
diff, possibly applying ML-training vocabulary that doesn't fit prompt/agent eval.

**With talent.** Description + "When NOT" both explicitly exclude "LLM/agent/prompt eval
design (eval-harness, learn-eval)" and say "not chat/agent behavior." Correctly
redirects.

**Result.** WITH beats baseline (correct scope discipline). **PASS.**

---

## Summary

| # | Scenario | Type | Pass? |
|---|----------|------|-------|
| 1 | Fit-before-split leakage | defect | PASS |
| 2 | Train/serve skew across files | defect | PASS |
| 3 | Fail-open promotion gate | defect | PASS |
| 4 | Non-reproducible training | defect | PASS |
| 5 | Clean pipeline (false-positive trap) | trap | WASH (not a clear win) |
| 6 | LLM/agent eval (scope trap) | trap | PASS |

**5 clear wins / 6.** The talent's decisive edges are the *quiet* defects a generalist
reviewer misses because the code reads as correct in isolation — fit-before-split
leakage (1), cross-file train/serve skew (2), and the fail-open-vs-error-handling
framing of the gate (3). It also holds scope discipline (6). The only non-win is the
clean-pipeline trap (5): the method confirms the controls but lacks an explicit
"declare ship-safe when nothing blocks" instruction, leaving mild over-flag risk.

**Verdict: PASSED.** Clearly beats baseline on its core function (catching production ML
defects that look like working code). Recommended non-blocking improvement: add a step-9
clause to state "if no blocking finding exists, say so and approve" to close the
false-positive gap surfaced by Scenario 5.
