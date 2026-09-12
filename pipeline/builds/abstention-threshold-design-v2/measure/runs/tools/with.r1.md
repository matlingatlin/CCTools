# tool calls from with.r1

```
ls -la . ./skill 2>&1 | head -100
```

```
python3 - <<'EOF'
import csv

def load(fn, scorecol):
    rows=[]
    with open(fn) as f:
        r=csv.DictReader(f)
        for row in r:
            rows.append((row['id'], float(row[scorecol]), int(row['correct'])))
    return rows

def auroc(rows):
    pos=[s for _,s,c in rows if c==1]
    neg=[s for _,s,c in rows if c==0]
    if not pos or not neg: return None
    count=0
    total=len(pos)*len(neg)
    for p in pos:
        for n in neg:
            if p>n: count+=1
            elif p==n: count+=0.5
    return count/total

for fn,col in [('scored_predictions.csv','score'), ('selfreported_confidence.csv','stated_confidence')]:
    rows=load(fn,col)
    n=len(rows)
    acc=sum(c for _,_,c in rows)/n
    print(fn, 'n=',n,'baseline_acc=%.3f'%acc, 'auroc=%.3f'%auroc(rows))
EOF

```

```
python3 - <<'EOF'
import csv

def load(fn, scorecol):
    rows=[]
    with open(fn) as f:
        r=csv.DictReader(f)
        for row in r:
            rows.append((row['id'], float(row[scorecol]), int(row['correct'])))
    return rows

rows = load('scored_predictions.csv','score')
rows_sorted = sorted(rows, key=lambda x: x[1])

# decile buckets
n=len(rows_sorted)
print("Decile buckets (score range -> n, accuracy):")
for i in range(10):
    lo = int(i*n/10); hi = int((i+1)*n/10)
    chunk = rows_sorted[lo:hi]
    scores=[s for _,s,c in chunk]
    accs=[c for _,s,c in chunk]
    print(f"  decile {i+1}: score [{min(scores):.3f},{max(scores):.3f}] n={len(chunk)} acc={sum(accs)/len(accs):.3f}")

# sweep: for each candidate cut = each distinct score value, coverage = fraction with score>=cut, precision on that segment
distinct_scores = sorted(set(s for _,s,c in rows), reverse=False)
print("\nSweep (cut, coverage%, answered_n, precision%):")
best=None
for cut in sorted(set(s for _,s,c in rows)):
    answered = [c for _,s,c in rows if s>=cut]
    if not answered: continue
    cov = len(answered)/n
    prec = sum(answered)/len(answered)
    if prec>=0.95:
        if best is None or cov>best[1]:
            best=(cut,cov,len(answered),prec)

print("Best (highest coverage cut meeting >=95% precision):", best)

# print a coarse table too, every ~10th distinct cut plus near the crossing
cuts = sorted(set(s for _,s,c in rows))
print("\ncut, coverage, n_answered, precision")
for cut in cuts:
    answered=[c for _,s,c in rows if s>=cut]
    cov=len(answered)/n
    prec=sum(answered)/len(answered)
    print(f"{cut:.3f}, {cov*100:.1f}%, {len(answered)}, {prec*100:.1f}%")
EOF

```

```
python3 - <<'EOF'
import math
def wilson(k,n,z=1.96):
    p=k/n
    denom=1+z**2/n
    center=p+z**2/(2*n)
    adj=z*math.sqrt(p*(1-p)/n+z**2/(4*n**2))
    lo=(center-adj)/denom
    hi=(center+adj)/denom
    return lo,hi

# cut 0.506 -> n=111, precision .9549 -> k=106
print("cut 0.506, n=111:", wilson(106,111))

# compare stricter cut e.g. 0.6 coverage 40% n=80 precision 98.8% k=79
print("cut 0.602, n=80, k=79:", wilson(79,80))

# and price of a stricter cut vs 0.506, e.g go to next round-ish cut 0.53 coverage 50% n=100 prec97
EOF

```

```
python3 - <<'EOF'
import csv

def load(fn, scorecol):
    rows=[]
    with open(fn) as f:
        r=csv.DictReader(f)
        for row in r:
            rows.append((row['id'], float(row[scorecol]), int(row['correct'])))
    return rows

rows = load('selfreported_confidence.csv','stated_confidence')
rows_sorted = sorted(rows, key=lambda x: x[1])
n=len(rows_sorted)
print("Decile buckets (stated_confidence -> n, accuracy):")
for i in range(10):
    lo=int(i*n/10); hi=int((i+1)*n/10)
    chunk=rows_sorted[lo:hi]
    scores=[s for _,s,c in chunk]
    accs=[c for _,s,c in chunk]
    print(f"  decile {i+1}: conf [{min(scores):.3f},{max(scores):.3f}] n={len(chunk)} acc={sum(accs)/len(accs):.3f}")

overall_acc = sum(c for _,_,c in rows)/n
print("overall accuracy:", overall_acc)

# best cut meeting 95% precision, if any
best=None
for cut in sorted(set(s for _,s,c in rows)):
    answered=[c for _,s,c in rows if s>=cut]
    if not answered: continue
    cov=len(answered)/n
    prec=sum(answered)/len(answered)
    if prec>=0.95 and (best is None or cov>best[1]):
        best=(cut,cov,len(answered),prec)
print("best cut meeting 95%:", best)

# distribution of stated_confidence values
vals=[s for _,s,c in rows]
print("min/max stated_confidence:", min(vals), max(vals))
import collections
print("value counts (rounded):", collections.Counter(round(v,1) for v in vals))
EOF

```
