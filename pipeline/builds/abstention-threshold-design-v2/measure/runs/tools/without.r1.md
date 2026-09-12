# tool calls from without.r1

```
ls -la && echo "---" && wc -l *.csv
```

```
python3 << 'EOF'
import csv

def load(fn, conf_col):
    rows = []
    with open(fn) as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append((float(row[conf_col]), int(row['correct'])))
    return rows

def analyze(rows, label):
    rows_sorted = sorted(rows, key=lambda x: -x[0])
    n = len(rows_sorted)
    total_correct = sum(c for _,c in rows_sorted)
    print(f"--- {label} ---")
    print(f"n={n}, overall accuracy={total_correct/n:.3f}")
    # try thresholds
    thresholds = sorted(set(s for s,_ in rows_sorted))
    best = None
    results = []
    for t in thresholds:
        sub = [c for s,c in rows_sorted if s >= t]
        if not sub: continue
        prec = sum(sub)/len(sub)
        cov = len(sub)/n
        results.append((t, prec, cov, len(sub)))
    return results

sp = load('scored_predictions.csv', 'score')
res = analyze(sp, 'scored_predictions')
for t,prec,cov,n in sorted(res, key=lambda x: x[0]):
    marker = " <-- meets 95%" if prec>=0.95 else ""
    print(f"t={t:.3f} precision={prec:.4f} coverage={cov:.3f} n_kept={n}{marker}")
EOF
```

```
python3 << 'EOF'
import csv, math

def load(fn, conf_col):
    rows = []
    with open(fn) as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append((float(row[conf_col]), int(row['correct'])))
    return rows

def wilson_lower(k, n, z=1.96):
    if n==0: return None
    phat = k/n
    denom = 1+z**2/n
    center = phat + z*z/(2*n)
    margin = z*math.sqrt(phat*(1-phat)/n + z*z/(4*n*n))
    return (center-margin)/denom

sp = load('scored_predictions.csv','score')
for t in [0.5,0.506,0.51,0.53,0.55,0.60,0.65]:
    sub=[c for s,c in sp if s>=t]
    k=sum(sub); n=len(sub)
    prec=k/n
    lb = wilson_lower(k,n)
    print(f"t={t}: n_kept={n} coverage={n/len(sp):.3f} precision={prec:.4f} wilson_lb95={lb:.4f}")
EOF
```

```
python3 << 'EOF'
import csv, math

def load(fn, conf_col):
    rows = []
    with open(fn) as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append((float(row[conf_col]), int(row['correct'])))
    return rows

def wilson_lower(k, n, z=1.96):
    if n==0: return None
    phat = k/n
    denom = 1+z**2/n
    center = phat + z*z/(2*n)
    margin = z*math.sqrt(phat*(1-phat)/n + z*z/(4*n*n))
    return (center-margin)/denom

sc = load('selfreported_confidence.csv','stated_confidence')
n=len(sc)
overall = sum(c for _,c in sc)/n
print(f"n={n} overall accuracy={overall:.3f}")

# distribution of stated confidence
import statistics
vals = sorted(s for s,_ in sc)
print("min/max stated_confidence:", vals[0], vals[-1])
print("count above 0.9:", sum(1 for s,_ in sc if s>=0.9))
print("count above 0.95:", sum(1 for s,_ in sc if s>=0.95))

thresholds = sorted(set(s for s,_ in sc))
for t in thresholds:
    sub=[c for s,c in sc if s>=t]
    if not sub: continue
    k=sum(sub); nn=len(sub)
    prec=k/nn
    if nn>=5:
        pass
print()
for t,_ in sorted(sc, key=lambda x:-x[0]):
    pass

# print table for thresholds >=0.5 step
for t in [round(x*0.05,2) for x in range(0,21)]:
    sub=[c for s,c in sc if s>=t]
    if not sub: continue
    k=sum(sub); nn=len(sub)
    prec=k/nn
    lb=wilson_lower(k,nn)
    print(f"t={t:.2f} n_kept={nn} coverage={nn/n:.3f} precision={prec:.4f} wilson_lb={lb:.4f}")

# correlation
mean_s = sum(s for s,_ in sc)/n
mean_c = overall
cov = sum((s-mean_s)*(c-mean_c) for s,c in sc)/n
var_s = sum((s-mean_s)**2 for s,_ in sc)/n
var_c = sum((c-mean_c)**2 for _,c in sc)/n
corr = cov/math.sqrt(var_s*var_c)
print("correlation stated_confidence vs correct:", corr)
EOF
```

```
python3 << 'EOF'
import csv
def load(fn, conf_col):
    rows = []
    with open(fn) as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append((float(row[conf_col]), int(row['correct'])))
    return rows

sp = load('scored_predictions.csv','score')
sub = [c for s,c in sp if s>=0.90]
print("scored_predictions.csv, score>=0.90: n=",len(sub),"precision=",sum(sub)/len(sub))

sc = load('selfreported_confidence.csv','stated_confidence')
sub2 = [c for s,c in sc if s>=0.90]
print("selfreported_confidence.csv, stated_confidence>=0.90: n=",len(sub2),"precision=",sum(sub2)/len(sub2))
EOF
```
