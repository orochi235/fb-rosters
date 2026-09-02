"""Stage 5+6: apply the fitted transform to the stage-4 sources.
Every output = one real source name + one logged edit. Nothing is invented."""
import json, os, random, re, unicodedata
from collections import Counter, defaultdict
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from sources import MONONYMS

def load():
    """Merged stage-4 sources (hand list + Wikidata), built by merge-sources.py."""
    detail = json.load(open('artifacts/sources-detail.json'))
    return [(d['first'], d['last'], d['domain']) for d in detail]

random.seed(1994)
# The source corpus mangles first names at 8%, but its first-name pool is generic and
# heavily repeated (Mike x22) which anonymizes on its own. This pool is flat and
# distinctive, so matching the rate would undershoot the effect. Dial, not a constant.
import sys
FIRST_RATE = float(sys.argv[1]) if len(sys.argv) > 1 else 0.35
VOWELS = set('aeiou')
model = json.load(open('artifacts/model.json'))

# fitted substitution table: real letter -> [(replacement, weight)]
table = defaultdict(list)
for k, w in model['subs'].items():
    f, t = k.split('>')
    table[f].append((t, w))

# fitted position distribution
POS = model['positions']
pos_choices, pos_weights = zip(*POS.items())

sources = load()
real_people = {f"{f} {l}" for f, l, _ in sources} | {m for m in MONONYMS}
athletes = json.load(open('artifacts/rosters-1994.json'))
real_people |= {f"{p['first']} {p['last']}" for p in athletes}
real_last = {p['last'].lower() for p in athletes} | {l.lower() for _, l, _ in sources}

# filter 1: "still looks like a name", derived from the real name universe rather than
# by hand. A mangled surname must open with an onset real surnames actually use, and
# every trigram it contains must be attested somewhere in a real surname.
ONSETS, TRIGRAMS = set(), set()
for w in real_last:
    ONSETS.add(w[:2])
    for i in range(len(w)-2): TRIGRAMS.add(w[i:i+3])

def plausible(w):
    w = w.lower()
    if len(w) < 3: return True
    if w[:2] not in ONSETS: return False
    return all(w[i:i+3] in TRIGRAMS for i in range(len(w)-2))
real_first_pool = [f for f, _, _ in sources]
MALE_NAMES = {p['first'].lower() for p in athletes}

def mangle_first(f):
    m, _ = substitute(f, set())
    if not m or m.lower() in MALE_NAMES: return f    # Doris -> Boris and friends
    return m

# A mangle can land on a word the source name never contained. Cheap guard; the
# stage-7 human pass is the real backstop.
UNFORTUNATE = ("boner","cock","dick","tit","cunt","fuck","shit","piss","slut","whore",
               "wank","turd","fart","anus","semen","penis","vagin","nazi","rape","spic",
               "kike","chink","wog","coon","fag","homo","retard")

def clean(word):
    w = word.lower()
    return not any(bad in w for bad in UNFORTUNATE)

def substitute(word, used):
    """One substitution, position and replacement both sampled from the fitted model."""
    for _ in range(60):
        pos_kind = random.choices(pos_choices, weights=pos_weights)[0]
        i = 0 if pos_kind == 'initial' else (len(word)-1 if pos_kind == 'final'
                                             else random.randrange(1, max(2, len(word)-1)))
        if i >= len(word): continue
        if i == 0 and len(word) > 1 and word[1].isupper(): continue   # O'Connor, McClain
        ch = word[i].lower()
        cands = table.get(ch)
        if not cands:                      # fall back to same-class letters seen in the data
            pool = [(t, w) for k, v in table.items() if (k in VOWELS) == (ch in VOWELS)
                    for t, w in v]
            if not pool: continue
            cands = pool
        cands = [(t, w) for t, w in cands if (t in VOWELS) == (ch in VOWELS) and t != ch]
        if not cands: continue
        rep = random.choices([t for t, _ in cands], weights=[w for _, w in cands])[0]
        out = word[:i] + (rep.upper() if word[i].isupper() else rep) + word[i+1:]
        if not plausible(out): continue               # filter 1: still looks like a name
        if not clean(out): continue
        if out.lower() in real_last: continue        # filter 2: not another real person
        if out in used: continue                      # distinct mangle per reuse
        return out, f"{word}[{i}]{ch}>{rep}"
    return None, None

roster, log, used_surnames, seen = [], [], set(), set()

def emit(first, surname, domain, note=""):
    m, edit = substitute(surname, used_surnames)
    if not m: return False
    name = f"{first} {m}"
    if name in real_people or name in seen: return False
    used_surnames.add(m); seen.add(name)
    roster.append(name)
    log.append({"out": name, "from_surname": surname, "edit": edit,
                "first_from": first, "domain": domain, "note": note})
    return True

# mononyms first, deliberately over-represented: mangled and paired
for m in MONONYMS:
    for _ in range(3):
        partner = random.choice(MONONYMS + real_first_pool)
        mm, edit = substitute(m, used_surnames)
        if not mm: continue
        pm = mangle_first(partner) if random.random() < .5 else partner
        name = f"{pm} {mm}"
        if name in real_people or name in seen: continue
        used_surnames.add(mm); seen.add(name); roster.append(name)
        log.append({"out": name, "from_surname": m, "edit": edit,
                    "first_from": partner, "domain": "mononym", "note": "mononym pair"})

order = sources[:]
random.shuffle(order)
while len(roster) < 700:
    before = len(roster)
    for _, last, domain in order:
        if len(roster) >= 700: break
        first = random.choice(real_first_pool)
        if random.random() < FIRST_RATE:
            first = mangle_first(first)
        emit(first, last, domain)
    if len(roster) == before: break

def restore_apostrophes(n):
    return re.sub(r"\bO([A-Z])", r"O'\1", n)

roster = [restore_apostrophes(n) for n in roster]
random.shuffle(roster)
open('artifacts/names-celebrities.txt', 'w').write('\n'.join(roster) + '\n')
json.dump(log, open('artifacts/celebrity-provenance.json', 'w'), indent=1)
print(f"{len(roster)} names -> artifacts/names-celebrities.txt")
print(f"distinct source surnames used: {len({l['from_surname'] for l in log})}")
print(f"mononym-derived entries: {sum(1 for l in log if l['domain']=='mononym')}")
