# tool calls from incumbent.r2

```
ls -la && echo "---scored---" && cat scored_predictions.csv | head -5 && wc -l scored_predictions.csv && echo "---selfreported---" && cat selfreported_confidence.csv | head -5 && wc -l selfreported_confidence.csv
```

```
cat err.txt
```

```
python3 << 'EOF'
import csv

def load(fn, scorecol):
    rows=[]
    with open(fn) as f:
        r=csv.DictReader(f)
        for row in r:
            rows.append((float(row[scorecol]), int(row['correct'])))
    return rows

def auroc(rows):
    pos=[s for s,c in rows if c==1]
    neg=[s for s,c in rows if c==0]
    if not pos or not neg: return None
    count=0
    for p in pos:
        for n in neg:
            if p>n: count+=1
            elif p==n: count+=0.5
    return count/(len(pos)*len(neg))

def deciles(rows):
    rows_sorted = sorted(rows, key=lambda x: x[0])
    n=len(rows_sorted)
    print("n=",n, "base rate correct=", sum(c for _,c in rows)/n)
    bucket_size = n//10
    for i in range(10):
        start=i*bucket_size
        end = (i+1)*bucket_size if i<9 else n
        chunk = rows_sorted[start:end]
        if not chunk: continue
        avg_score = sum(s for s,_ in chunk)/len(chunk)
        acc = sum(c for _,c in chunk)/len(chunk)
        print(f"decile {i}: n={len(chunk)} scorerange=[{chunk[0][0]:.3f},{chunk[-1][0]:.3f}] avgscore={avg_score:.3f} acc={acc:.3f}")

def sweep(rows, label):
    rows_sorted = sorted(rows, key=lambda x: -x[0])  # descending score
    n=len(rows_sorted)
    print(f"--- sweep {label} ---")
    thresholds = sorted(set(s for s,_ in rows), reverse=True)
    # pick representative thresholds across range
    import numpy as np
    for t in [0.99,0.95,0.9,0.85,0.8,0.75,0.7,0.65,0.6,0.55,0.5,0.4,0.3]:
        answered = [c for s,c in rows if s>=t]
        if not answered: continue
        cov = len(answered)/n
        prec = sum(answered)/len(answered)
        print(f"t>={t:.2f}: coverage={cov:.3f} ({len(answered)}/{n}) precision={prec:.3f}")

print("=== scored_predictions.csv (model confidence) ===")
rows1 = load('scored_predictions.csv','score')
print("AUROC:", auroc(rows1))
deciles(rows1)
sweep(rows1, "scored_predictions")

print()
print("=== selfreported_confidence.csv (LLM stated confidence) ===")
rows2 = load('selfreported_confidence.csv','stated_confidence')
print("AUROC:", auroc(rows2))
deciles(rows2)
sweep(rows2, "selfreported_confidence")
EOF

```

```
python3 << 'EOF'
import csv

def load(fn, scorecol):
    rows=[]
    with open(fn) as f:
        r=csv.DictReader(f)
        for row in r:
            rows.append((float(row[scorecol]), int(row['correct'])))
    return rows

def auroc(rows):
    pos=[s for s,c in rows if c==1]
    neg=[s for s,c in rows if c==0]
    if not pos or not neg: return None
    count=0
    for p in pos:
        for n in neg:
            if p>n: count+=1
            elif p==n: count+=0.5
    return count/(len(pos)*len(neg))

def deciles(rows):
    rows_sorted = sorted(rows, key=lambda x: x[0])
    n=len(rows_sorted)
    print("n=",n, "base rate correct=", sum(c for _,c in rows)/n)
    bucket_size = n//10
    for i in range(10):
        start=i*bucket_size
        end = (i+1)*bucket_size if i<9 else n
        chunk = rows_sorted[start:end]
        if not chunk: continue
        avg_score = sum(s for s,_ in chunk)/len(chunk)
        acc = sum(c for _,c in chunk)/len(chunk)
        print(f"decile {i}: n={len(chunk)} scorerange=[{chunk[0][0]:.3f},{chunk[-1][0]:.3f}] avgscore={avg_score:.3f} acc={acc:.3f}")

def sweep(rows, label, thresholds):
    n=len(rows)
    print(f"--- sweep {label} ---")
    for t in thresholds:
        answered = [c for s,c in rows if s>=t]
        if not answered:
            print(f"t>={t:.2f}: coverage=0.000 (0/{n}) precision=n/a")
            continue
        cov = len(answered)/n
        prec = sum(answered)/len(answered)
        print(f"t>={t:.2f}: coverage={cov:.3f} ({len(answered)}/{n}) precision={prec:.3f}")

print("=== scored_predictions.csv (model confidence) ===")
rows1 = load('scored_predictions.csv','score')
print("AUROC:", auroc(rows1))
deciles(rows1)
sweep(rows1, "scored_predictions", [0.99,0.97,0.95,0.93,0.9,0.87,0.85,0.82,0.8,0.77,0.75,0.72,0.7,0.65,0.6,0.55,0.5])

print()
print("=== selfreported_confidence.csv (LLM stated confidence) ===")
rows2 = load('selfreported_confidence.csv','stated_confidence')
print("AUROC:", auroc(rows2))
deciles(rows2)
sweep(rows2, "selfreported_confidence", [0.99,0.98,0.97,0.96,0.95,0.94,0.93,0.92,0.91,0.9,0.85,0.8,0.7])
EOF

```

```
python3 << 'EOF'
import csv

def load(fn, scorecol):
    rows=[]
    with open(fn) as f:
        r=csv.DictReader(f)
        for row in r:
            rows.append((float(row[scorecol]), int(row['correct'])))
    return rows

rows1 = load('scored_predictions.csv','score')
n=len(rows1)
# fine sweep between 0.50 and 0.60
thresholds = sorted(set(s for s,_ in rows1))
thresholds = [t for t in thresholds if 0.45<=t<=0.60]
for t in thresholds:
    answered = [c for s,c in rows1 if s>=t]
    cov=len(answered)/n
    prec=sum(answered)/len(answered)
    print(f"t>={t:.3f}: coverage={cov:.3f} ({len(answered)}/{n}) precision={prec:.3f}")
EOF

```
