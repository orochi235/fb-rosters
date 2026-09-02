"""Stage 4b: merge the hand-assembled era-verified list with Wikidata sitelink rankings.

Wikidata gives depth and international reach; it is a poor 1994 fame proxy because
sitelinks measure durable fame. The divergence is worst for politicians and Nobel
laureates, whose fame arrives decades late, so those categories are dropped and the
hand list supplies them. Women athletes fall below the sitelink threshold entirely,
so sport comes from the hand list too.
"""
import json, glob, os, re, unicodedata
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from sources import load, MONONYMS

# fame arrives too late in these categories for sitelinks to indicate 1994 prominence
DROP_CATEGORIES = {'politician', 'scientist', 'journalist'}

# prominent only well after 1994; sitelinks cannot distinguish them
ANACHRONISTIC = {
 "Kamala Harris","Theresa May","Michelle Obama","Dilma Rousseff","Ursula von der Leyen",
 "Marine Le Pen","Michelle Bachelet","Ellen Johnson Sirleaf","Herta Müller",
 "Elfriede Jelinek","Svetlana Alexievich","Wangari Muta Maathai","Anna Wintour",
 "Carrie Lam","Sushma Swaraj","Annegret Kramp-Karrenbauer","Iveta Radičová",
 "Jadranka Kosor","Sandra Mason","Marie-Louise Coleiro Preca","Melissa McBride",
 "Halle Berry","Tzipi Livni","Angela Merkel","Christine Lagarde","Sonia Gandhi",
}

def deacc(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def usable(name):
    """Two clean Latin name parts, no parentheticals, initials or honorifics."""
    n = deacc(name).strip()
    if not re.fullmatch(r"[A-Za-z' -]+", n): return None
    parts = [p for p in n.split() if len(p) > 1]
    if len(parts) < 2: return None
    first, last = parts[0], parts[-1]
    if len(last) < 3 or len(first) < 2: return None
    # Sources style themselves (bell hooks, k.d. lang); the roster does not inherit it.
    # Only the leading character is touched, so McEntire and O'Connor survive intact.
    cap = lambda w: w[0].upper() + w[1:]
    return cap(first), cap(last)

rows, kept = {}, 0
for f in sorted(glob.glob('artifacts/wd_*.json')):
    cat = os.path.basename(f)[3:-5]
    if cat in DROP_CATEGORIES: continue
    try: data = json.load(open(f))['results']['bindings']
    except Exception: continue
    for r in data:
        name, s = r['name']['value'], int(r['sitelinks']['value'])
        if name in ANACHRONISTIC: continue
        u = usable(name)
        if not u: continue
        if name not in rows or s > rows[name][0]: rows[name] = (s, cat, u); kept += 1

hand = load()
merged, seen = [], set()
for first, last, domain in hand:                       # hand list first: era-verified
    if (first, last) not in seen:
        seen.add((first, last)); merged.append((first, last, domain, 9999))
# Wikidata is capped hard. Its depth is *internationally* famous women, which is not
# the same as recognizable to an American in 1994 -- and recognition, not depth, is the
# binding constraint. Uncapped, the long tail swamps the hand list and the effect dies.
WIKIDATA_CAP = 140
added = 0
for name, (s, cat, (first, last)) in sorted(rows.items(), key=lambda kv: -kv[1][0]):
    if added >= WIKIDATA_CAP: break
    if (first, last) not in seen:
        seen.add((first, last)); merged.append((first, last, cat, s)); added += 1

os.makedirs('artifacts', exist_ok=True)
with open('artifacts/sources.txt', 'w') as fh:         # flat, per the spec
    for first, last, _, _ in merged: fh.write(f"{first} {last}\n")
json.dump([{"first": f, "last": l, "domain": d, "sitelinks": s} for f, l, d, s in merged],
          open('artifacts/sources-detail.json', 'w'), indent=1)

from collections import Counter
print(f"hand list:  {len(hand)}")
print(f"wikidata:   {len(rows)} usable after dropping {sorted(DROP_CATEGORIES)}")
print(f"MERGED:     {len(merged)} distinct women")
for d, n in Counter(d for _,_,d,_ in merged).most_common(12): print(f"  {d:<22} {n}")
