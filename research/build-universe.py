"""Stage 1b: fold Lahman 1994 + fetched NHL rosters into artifacts/rosters-1994.json."""
import json, glob, sqlite3, unicodedata, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs('artifacts', exist_ok=True)

def deacc(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

c = sqlite3.connect('lahman.sqlite')
mlb = [{"first": deacc(f.strip()), "last": deacc(l.strip()), "league": "MLB"}
       for f, l in c.execute("""select distinct p.namefirst, p.namelast
                                from appearances a join people p on p.playerid = a.playerid
                                where a.yearid = 1994
                                  and p.namefirst is not null and p.namelast is not null""")]

nhl, seen = [], set()
for path in sorted(glob.glob('nhl_raw/*.json')):
    d = json.load(open(path))
    for g in ('forwards', 'defensemen', 'goalies'):
        for p in d.get(g, []):
            f = deacc(p['firstName']['default'].strip())
            l = deacc(p['lastName']['default'].strip())
            if (f, l) not in seen:
                seen.add((f, l)); nhl.append({"first": f, "last": l, "league": "NHL"})

json.dump(mlb + nhl, open('artifacts/rosters-1994.json', 'w'), indent=1)
print(f"MLB {len(mlb)} + NHL {len(nhl)} = {len(mlb)+len(nhl)} players "
      f"({len({p['last'] for p in mlb+nhl})} distinct surnames)")
