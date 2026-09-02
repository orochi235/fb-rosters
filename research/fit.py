import json
from collections import Counter
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

res = [r for r in json.load(open('artifacts/alignments.json')) if r['dist']==1 and r['n']==1]

def edit_of(a, b):
    """classify the single edit taking real b -> fake a"""
    a_, b_ = a.lower(), b.lower()
    if len(a_) == len(b_):
        i = next(k for k in range(len(a_)) if a_[k] != b_[k])
        return ('sub', b_[i], a_[i], i, len(b_))
    if len(a_) > len(b_):
        for i in range(len(b_)+1):
            if a_[:i]+a_[i+1:] == b_: return ('ins', '', a_[i], i, len(b_))
    else:
        for i in range(len(a_)+1):
            if b_[:i]+b_[i+1:] == a_: return ('del', b_[i], '', i, len(b_))
    return ('?', '', '', -1, len(b_))

kinds, subs, pos = Counter(), Counter(), Counter()
for r in res:
    k, frm, to, i, n = edit_of(r['fake'], r['cands'][0])
    kinds[k] += 1
    if k == 'sub':
        subs[(frm, to)] += 1
        pos['initial' if i == 0 else ('final' if i == n-1 else 'internal')] += 1

tot = sum(kinds.values())
print(f"=== EDIT TYPE (n={tot} unambiguous distance-1 pairs) ===")
for k, v in kinds.most_common(): print(f"  {k:<6} {v:>4} ({v/tot*100:4.1f}%)")

ps = sum(pos.values())
print(f"\n=== POSITION OF SUBSTITUTION (n={ps}) ===")
for k, v in pos.most_common(): print(f"  {k:<9} {v:>4} ({v/ps*100:4.1f}%)")

print(f"\n=== TOP 30 SUBSTITUTIONS (real -> fake) ===")
for (f, t), v in subs.most_common(30):
    print(f"  {f} -> {t}   {v}")

vowels = set('aeiou')
vv = sum(v for (f,t),v in subs.items() if f in vowels and t in vowels)
cc = sum(v for (f,t),v in subs.items() if f not in vowels and t not in vowels)
mix = sum(subs.values()) - vv - cc
print(f"\nvowel->vowel {vv}  consonant->consonant {cc}  crossing {mix}")
json.dump({"subs": {f"{f}>{t}": v for (f,t),v in subs.items()},
           "kinds": dict(kinds), "positions": dict(pos)}, open('artifacts/model.json','w'), indent=1)
