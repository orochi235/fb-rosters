import json, sqlite3, sys, unicodedata
from collections import Counter

def deacc(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def lev(a, b, cap=3):
    if abs(len(a)-len(b)) > cap: return cap+1
    prev = list(range(len(b)+1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j]+1, cur[j-1]+1, prev[j-1] + (ca != cb)))
        if min(cur) > cap: return cap+1
        prev = cur
    return prev[-1]

universe = json.load(open('rosters-1994.json'))
real_last = sorted({p['last'] for p in universe})
real_first = Counter(p['first'] for p in universe)

def align(surnames, label):
    hist, results = Counter(), []
    for k, s in enumerate(surnames, 1):
        best, bd = [], 99
        for r in real_last:
            d = lev(s.lower(), r.lower())
            if d < bd: bd, best = d, [r]
            elif d == bd and d <= 2: best.append(r)
        hist[bd if bd <= 2 else '3+'] += 1
        results.append({"fake": s, "dist": bd, "cands": best[:6], "n": len(best)})
        if k % 100 == 0: print(f"  {label} {k}/{len(surnames)}", file=sys.stderr)
    return hist, results

fake = [l.strip().split(None, 1) for l in open('/Users/mike/src/fb-rosters/names.txt') if l.strip()]
fake_first = [p[0] for p in fake]
fake_last  = [p[1] for p in fake]

print("aligning corpus...", file=sys.stderr)
hist, results = align(fake_last, "corpus")

# NULL MODEL: real surnames from 1974 MLB (same naming culture, cannot be the source)
c = sqlite3.connect('lahman.sqlite')
q = """select distinct p.namelast from appearances a join people p on p.playerid=a.playerid
       where a.yearid=1974 and p.namelast is not null"""
ctrl_all = {deacc(r[0].strip()) for r in c.execute(q)} - set(real_last)
ctrl = sorted(ctrl_all)[:700]
print(f"null model: {len(ctrl)} surnames from MLB 1974 not present in 1994", file=sys.stderr)
chist, _ = align(ctrl, "null")

print("\n=== SURNAME EDIT DISTANCE TO NEAREST REAL 1994 PLAYER ===")
print(f"{'dist':<6} {'corpus':>14} {'null (1974)':>14}")
for k in [0,1,2,'3+']:
    cn, nn = hist.get(k,0), chist.get(k,0)
    print(f"{str(k):<6} {cn:>6} ({cn/700*100:>4.1f}%) {nn:>6} ({nn/len(ctrl)*100:>4.1f}%)")

uniq1 = [r for r in results if r['dist']==1 and r['n']==1]
amb1  = [r for r in results if r['dist']==1 and r['n']>1]
print(f"\ndistance-1 unambiguous: {len(uniq1)}   ambiguous: {len(amb1)}")

fn_hit = sum(1 for f in fake_first if f in real_first)
print(f"first names present verbatim in the real universe: {fn_hit}/700 ({fn_hit/700*100:.0f}%)")

json.dump(results, open('alignments.json','w'), indent=1)
print("\nsample unambiguous distance-1 alignments:")
for r in uniq1[:20]: print(f"  {r['fake']:<16} <- {r['cands'][0]}")
