# tool calls from without.r2

```
ls -la && echo "---" && wc -l scored_predictions.csv selfreported_confidence.csv 2>&1
```

```
python3 - <<'EOF'
import csv

def load(path, conf_col):
    rows = []
    with open(path) as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append((float(row[conf_col]), int(row['correct'])))
    return rows

def analyze(rows, label):
    rows_sorted = sorted(rows, key=lambda x: -x[0])
    n = len(rows_sorted)
    print(f"--- {label} --- n={n}")
    overall_acc = sum(c for _,c in rows_sorted)/n
    print(f"overall accuracy: {overall_acc:.3f}")
    # try thresholds
    thresholds = sorted(set(x[0] for x in rows_sorted))
    best = None
    results = []
    for t in thresholds:
        sub = [c for s,c in rows_sorted if s>=t]
        if not sub: continue
        prec = sum(sub)/len(sub)
        coverage = len(sub)/n
        results.append((t, prec, coverage, len(sub)))
    return results

sp = load('scored_predictions.csv','score')
res = analyze(sp, 'scored_predictions (score)')
for t,prec,cov,n in res:
    flag = " <== " if prec>=0.95 else ""
    print(f"t={t:.3f} precision={prec:.4f} coverage={cov:.3f} n_auto={n}{flag}")
EOF
```

```
python3 - <<'EOF'
import csv, math

def load(path, conf_col):
    rows = []
    with open(path) as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append((float(row[conf_col]), int(row['correct'])))
    return rows

def wilson_lb(k, n, z=1.96):
    if n==0: return None
    phat = k/n
    denom = 1+z*z/n
    center = phat + z*z/(2*n)
    margin = z*math.sqrt(phat*(1-phat)/n + z*z/(4*n*n))
    return (center-margin)/denom

sp = load('scored_predictions.csv','score')
n=len(sp)
for t in [0.45,0.50,0.53,0.55,0.60,0.65,0.70]:
    sub=[c for s,c in sp if s>=t]
    k=sum(sub); m=len(sub)
    prec=k/m if m else float('nan')
    lb = wilson_lb(k,m)
    print(f"t={t:.2f} n_auto={m:3d} coverage={m/n:.3f} precision={prec:.4f} wilson_lb95={lb:.4f} errors={m-k}")
EOF
```

```
python3 - <<'EOF'
import csv, math

def load(path, conf_col):
    rows = []
    with open(path) as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append((float(row[conf_col]), int(row['correct'])))
    return rows

def wilson_lb(k, n, z=1.96):
    if n==0: return None
    phat = k/n
    denom = 1+z*z/n
    center = phat + z*z/(2*n)
    margin = z*math.sqrt(phat*(1-phat)/n + z*z/(4*n*n))
    return (center-margin)/denom

sc = load('selfreported_confidence.csv','stated_confidence')
n = len(sc)
print("n=",n, "overall accuracy=", sum(c for _,c in sc)/n)

# distribution of stated confidence
from collections import Counter
vals = sorted(set(s for s,_ in sc))
print("distinct stated_confidence values:", vals[:20], "..." if len(vals)>20 else "")
print("min/max:", min(vals), max(vals))

# calibration bins
import numpy as np
bins = [0,0.5,0.6,0.7,0.8,0.9,0.95,0.99,1.01]
for i in range(len(bins)-1):
    lo,hi = bins[i], bins[i+1]
    sub = [c for s,c in sc if lo<=s<hi]
    if sub:
        print(f"[{lo:.2f},{hi:.2f}) n={len(sub):3d} accuracy={sum(sub)/len(sub):.3f}")

print()
for t in [0.5,0.6,0.7,0.8,0.85,0.9,0.95,0.99]:
    sub=[c for s,c in sc if s>=t]
    if not sub: 
        print(f"t={t}: no rows >= t")
        continue
    k=sum(sub); m=len(sub)
    prec=k/m
    lb=wilson_lb(k,m)
    print(f"t={t:.2f} n_auto={m:3d} coverage={m/n:.3f} accuracy={prec:.4f} wilson_lb95={lb:.4f}")
EOF
```

```
python3 - <<'EOF'
import csv, math

def load(path, conf_col):
    rows = []
    with open(path) as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append((float(row[conf_col]), int(row['correct'])))
    return rows

def wilson_lb(k, n, z=1.96):
    if n==0: return None
    phat = k/n
    denom = 1+z*z/n
    center = phat + z*z/(2*n)
    margin = z*math.sqrt(phat*(1-phat)/n + z*z/(4*n*n))
    return (center-margin)/denom

sc = load('selfreported_confidence.csv','stated_confidence')
n = len(sc)
print("n=",n, "overall accuracy=", round(sum(c for _,c in sc)/n,3))

bins = [0.79,0.85,0.90,0.95,0.99,1.01]
for i in range(len(bins)-1):
    lo,hi = bins[i], bins[i+1]
    sub = [c for s,c in sc if lo<=s<hi]
    if sub:
        print(f"[{lo:.2f},{hi:.2f}) n={len(sub):3d} accuracy={sum(sub)/len(sub):.3f}")

print()
for t in [0.79,0.85,0.90,0.95,0.99]:
    sub=[c for s,c in sc if s>=t]
    if not sub:
        continue
    k=sum(sub); m=len(sub)
    prec=k/m
    lb=wilson_lb(k,m)
    print(f"t={t:.2f} n_auto={m:3d} coverage={m/n:.3f} accuracy={prec:.4f} wilson_lb95={lb:.4f}")

# correlation check
import statistics
scores=[s for s,_ in sc]
corr = statistics.correlation(scores,[c for _,c in sc]) if hasattr(statistics,'correlation') else None
print("corr stated_conf vs correct:", corr)
EOF
```
