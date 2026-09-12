# tool calls from incumbent.r1

```
ls -la ./scored_predictions.csv ./selfreported_confidence.csv 2>&1; echo "---"; wc -l ./scored_predictions.csv ./selfreported_confidence.csv 2>&1
```

```
head -5 ./scored_predictions.csv; echo "---"; head -5 ./selfreported_confidence.csv
```

```
cd /tmp && python3 << 'EOF'
import csv

def load(path, scorecol):
    rows = []
    with open(path) as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append((float(row[scorecol]), int(row['correct'])))
    return rows

def auroc(rows):
    pos = [s for s,c in rows if c==1]
    neg = [s for s,c in rows if c==0]
    if not pos or not neg:
        return None
    count = 0
    total = len(pos)*len(neg)
    for p in pos:
        for n in neg:
            if p > n: count += 1
            elif p == n: count += 0.5
    return count/total

def deciles(rows):
    rows_sorted = sorted(rows, key=lambda x: x[0])
    n = len(rows_sorted)
    bucket_size = n // 10
    print("decile buckets (score range: n, accuracy)")
    for i in range(10):
        start = i*bucket_size
        end = (i+1)*bucket_size if i < 9 else n
        chunk = rows_sorted[start:end]
        if not chunk: continue
        acc = sum(c for s,c in chunk)/len(chunk)
        lo = chunk[0][0]; hi = chunk[-1][0]
        print(f"  decile {i+1}: n={len(chunk)} range=[{lo:.3f},{hi:.3f}] acc={acc:.3f}")

def sweep(rows, label):
    print(f"\n=== Sweep for {label} ===")
    thresholds = sorted(set(s for s,c in rows))
    n = len(rows)
    results = []
    for t in [round(x*0.02,2) for x in range(0,51)]:
        above = [(s,c) for s,c in rows if s >= t]
        if len(above) == 0: continue
        coverage = len(above)/n
        precision = sum(c for s,c in above)/len(above)
        results.append((t, coverage, precision, len(above)))
    # print a reasonable subset
    prev_cov = None
    for t, cov, prec, cnt in results:
        print(f"  t={t:.2f}  coverage={cov:.3f} ({cnt}/{n})  precision={prec:.3f}")

print("### scored_predictions.csv (model confidence) ###")
rows1 = load('./scored_predictions.csv', 'score')
print("AUROC:", auroc(rows1))
deciles(rows1)

print()
print("### selfreported_confidence.csv (LLM stated confidence) ###")
rows2 = load('./selfreported_confidence.csv', 'stated_confidence')
print("AUROC:", auroc(rows2))
deciles(rows2)
EOF
```

```
pwd
```

```
python3 << 'EOF'
import csv

def load(path, scorecol):
    rows = []
    with open(path) as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append((float(row[scorecol]), int(row['correct'])))
    return rows

def auroc(rows):
    pos = [s for s,c in rows if c==1]
    neg = [s for s,c in rows if c==0]
    if not pos or not neg:
        return None
    count = 0
    total = len(pos)*len(neg)
    for p in pos:
        for n in neg:
            if p > n: count += 1
            elif p == n: count += 0.5
    return count/total

def deciles(rows):
    rows_sorted = sorted(rows, key=lambda x: x[0])
    n = len(rows_sorted)
    bucket_size = n // 10
    print("decile buckets (score range: n, accuracy)")
    for i in range(10):
        start = i*bucket_size
        end = (i+1)*bucket_size if i < 9 else n
        chunk = rows_sorted[start:end]
        if not chunk: continue
        acc = sum(c for s,c in chunk)/len(chunk)
        lo = chunk[0][0]; hi = chunk[-1][0]
        print(f"  decile {i+1}: n={len(chunk)} range=[{lo:.3f},{hi:.3f}] acc={acc:.3f}")

def sweep(rows, label, step=0.02):
    print(f"\n=== Sweep for {label} ===")
    n = len(rows)
    results = []
    for i in range(0,51):
        t = round(i*step,2)
        above = [(s,c) for s,c in rows if s >= t]
        if len(above) == 0: continue
        coverage = len(above)/n
        precision = sum(c for s,c in above)/len(above)
        results.append((t, coverage, precision, len(above)))
    for t, cov, prec, cnt in results:
        print(f"  t={t:.2f}  coverage={cov:.3f} ({cnt}/{n})  precision={prec:.3f}")

print("### scored_predictions.csv (model confidence) ###")
rows1 = load('./scored_predictions.csv', 'score')
print("n =", len(rows1), "overall accuracy =", sum(c for s,c in rows1)/len(rows1))
print("AUROC:", auroc(rows1))
deciles(rows1)
sweep(rows1, "scored_predictions", step=0.02)

print()
print("### selfreported_confidence.csv (LLM stated confidence) ###")
rows2 = load('./selfreported_confidence.csv', 'stated_confidence')
print("n =", len(rows2), "overall accuracy =", sum(c for s,c in rows2)/len(rows2))
print("AUROC:", auroc(rows2))
deciles(rows2)
sweep(rows2, "selfreported_confidence", step=0.02)
EOF
```

```
python3 << 'EOF'
import csv

def load(path, scorecol):
    rows = []
    with open(path) as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append((float(row[scorecol]), int(row['correct'])))
    return rows

rows1 = load('./scored_predictions.csv', 'score')
n = len(rows1)
# fine sweep between 0.50 and 0.65
for i in range(500,651):
    t = i/1000
    above = [(s,c) for s,c in rows1 if s >= t]
    if not above: continue
    cov = len(above)/n
    prec = sum(c for s,c in above)/len(above)
    print(f"t={t:.3f} coverage={cov:.3f} ({len(above)}/{n}) precision={prec:.4f}")
EOF
```
