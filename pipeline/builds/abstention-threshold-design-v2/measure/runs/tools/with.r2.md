# tool calls from with.r2

```
echo "--- cwd ---"; pwd; echo "--- ls ---"; ls -la; echo "--- skill dir ---"; find ./skill -maxdepth 3 -type f 2>/dev/null
```

```
echo "=== scored_predictions.csv head ==="; head -5 scored_predictions.csv; wc -l scored_predictions.csv
echo "=== selfreported_confidence.csv head ==="; head -5 selfreported_confidence.csv; wc -l selfreported_confidence.csv
```

```
python3 << 'EOF'
import csv

def load(fname, scorecol):
    rows=[]
    with open(fname) as f:
        r=csv.DictReader(f)
        for row in r:
            rows.append((float(row[scorecol]), int(row['correct'])))
    return rows

def auroc(rows):
    pos = [s for s,c in rows if c==1]
    neg = [s for s,c in rows if c==0]
    if not pos or not neg:
        return None
    count=0
    total=len(pos)*len(neg)
    for p in pos:
        for n in neg:
            if p>n: count+=1
            elif p==n: count+=0.5
    return count/total

def deciles(rows):
    rows_sorted = sorted(rows, key=lambda x: x[0])
    n=len(rows_sorted)
    buckets=[]
    for i in range(10):
        lo = i*n//10
        hi=(i+1)*n//10
        chunk = rows_sorted[lo:hi]
        if chunk:
            acc = sum(c for s,c in chunk)/len(chunk)
            buckets.append((chunk[0][0], chunk[-1][0], len(chunk), acc))
    return buckets

def sweep(rows, step=0.01):
    # for each cut, coverage = fraction with score>=cut, precision = accuracy among those
    cuts = sorted(set(s for s,c in rows))
    results=[]
    for cut in cuts:
        answered = [c for s,c in rows if s>=cut]
        n=len(answered)
        if n==0: continue
        prec = sum(answered)/n
        cov = n/len(rows)
        results.append((cut, cov, n, prec))
    return results

for fname, col in [('scored_predictions.csv','score'), ('selfreported_confidence.csv','stated_confidence')]:
    rows = load(fname, col)
    n=len(rows)
    base_acc = sum(c for s,c in rows)/n
    a = auroc(rows)
    print(f"=== {fname} ===")
    print(f"n={n}, base accuracy={base_acc:.3f}, AUROC={a:.3f}")
    print("deciles (lo,hi,n,acc):")
    for b in deciles(rows):
        print(f"  {b[0]:.3f}-{b[1]:.3f}  n={b[2]:3d}  acc={b[3]:.3f}")
    print()
EOF
```

```
python3 << 'EOF'
import csv

def load(fname, scorecol):
    rows=[]
    with open(fname) as f:
        r=csv.DictReader(f)
        for row in r:
            rows.append((float(row[scorecol]), int(row['correct'])))
    return rows

rows = load('scored_predictions.csv','score')
rows_sorted = sorted(rows, key=lambda x: -x[0])  # descending by score
n_total=len(rows)

# cumulative precision as we lower the cut (include more)
cum_correct=0
cum_n=0
table=[]
prev_score=None
for s,c in rows_sorted:
    cum_n+=1
    cum_correct+=c
    prec = cum_correct/cum_n
    cov = cum_n/n_total
    table.append((s,cov,cum_n,prec))

# print every row where precision crosses around 0.95, plus overview at 10 coverage points
print("Full table near precision=0.95 boundary:")
last_meeting=None
for s,cov,cnt,prec in table:
    if prec>=0.95:
        last_meeting=(s,cov,cnt,prec)
print("Highest-coverage cut with precision>=0.95 (cumulative from top):", last_meeting)

# print table rows around that n
target_n = last_meeting[2]
for i in range(max(0,target_n-8), min(len(table), target_n+8)):
    print(i, table[i])

print()
print("Coarse sweep (every ~10%ile of cut values):")
cuts = sorted(set(s for s,c in rows))
for i in range(0,len(cuts), max(1,len(cuts)//10)):
    cut = cuts[i]
    answered=[c for s,c in rows if s>=cut]
    n=len(answered)
    prec=sum(answered)/n
    cov=n/n_total
    print(f"cut={cut:.3f} cov={cov:.3f} n={n} precision={prec:.3f}")
EOF
```

```
grep -n -i "verbaliz\|stated confidence\|self-report" -A 4 ./skill/references/uncertainty-signal-evidence.md | head -80
```

```
python3 << 'EOF'
import csv

def load(fname, scorecol):
    rows=[]
    with open(fname) as f:
        r=csv.DictReader(f)
        for row in r:
            rows.append((float(row[scorecol]), int(row['correct'])))
    return rows

rows = load('selfreported_confidence.csv','stated_confidence')
n_total=len(rows)
cuts = sorted(set(s for s,c in rows))
print("cut, coverage, n, precision  (base rate = %.3f)" % (sum(c for s,c in rows)/n_total))
for i in range(0,len(cuts), max(1,len(cuts)//12)):
    cut = cuts[i]
    answered=[c for s,c in rows if s>=cut]
    n=len(answered)
    prec=sum(answered)/n
    cov=n/n_total
    print(f"cut={cut:.3f} cov={cov:.3f} n={n:3d} precision={prec:.3f}")
# max cut
cut=max(cuts)
answered=[c for s,c in rows if s>=cut]
print(f"max cut={cut:.3f} cov={len(answered)/n_total:.3f} n={len(answered)} precision={sum(answered)/len(answered):.3f}")
EOF
```
