# fb-rosters

Sample names for test fixtures, seed data, and mock rosters — drawn from, objectively, the best corpus in history: the venerable mid-90's classic *Fighting Baseball* for Super Famicom.

Its 700 player names were invented by someone working from an imperfect sense of what American baseball players are called, along with 1994 rosters from several American professional sports leagues.

```
npm install fb-rosters
```

```js
import { generate } from 'fb-rosters';

generate();   // ['Mike Truk']
generate(3);  // ['Bobson Dugnutt', 'Sleve McDichael', 'Rey McSriff']
```

There is a second roster of 700, built from the same process applied to women who
were famous in the early 1990s. It is opt-in and nothing reaches it by accident.

```js
generate(3, { roster: 'celebrities' });  // ['Aretha Flomers', 'Phitney Kawyer', 'Mora Gher']
generate(3, { roster: 'all' });          // drawn from both
```

## API

**`generate(count = 1, options = {})` → `string[]`**

Returns `count` names, always as an array. Every name is verbatim from a corpus — nothing is synthesized or recombined.

`options.roster` selects between `'athletes'` (the default, the Fighting Baseball corpus), `'celebrities'`, and `'all'`. Passing anything else throws `RangeError`, as does a `count` that is not a non-negative integer.

Names are dealt from a shuffled deck, so a call never repeats itself until that deck is used up. The deck persists between calls, so consecutive small calls also avoid repeats. Ask for more than the corpus holds and it reshuffles and keeps going. Each roster keeps its own deck, so drawing from one never disturbs another's guarantee.

**`NAMES` / `CELEBRITIES` → `readonly string[]`**

Either corpus in roster order, if you'd rather do your own picking. `ROSTERS` holds both, keyed by name.

`'all'` is a way of dealing, not a third corpus — there is no combined array to import. If you want one, `[...ROSTERS.athletes, ...ROSTERS.celebrities]`.

## Without installing

Every published file is on jsDelivr, with CORS enabled, so the corpus doubles as a static endpoint:

```
https://cdn.jsdelivr.net/npm/fb-rosters/names.json   {"count": 700, "names": [...]}
https://cdn.jsdelivr.net/npm/fb-rosters/names.txt    newline-delimited

https://cdn.jsdelivr.net/npm/fb-rosters/names-celebrities.json
https://cdn.jsdelivr.net/npm/fb-rosters/names-celebrities.txt
```

The module itself imports directly in browsers and Deno:

```js
import { generate } from 'https://cdn.jsdelivr.net/npm/fb-rosters/index.js';
```

Pin a version in the path (`fb-rosters@1.0.0`) if you need the bytes to never change.

## Corpus

`names.txt` and `names-celebrities.txt` are the sources of truth; the `.js` and `.json` files are generated from them by `npm run build:data`, which runs automatically before publish. To correct a name, edit the text file.

The celebrities roster was not written by hand. The transform behind the original corpus was recovered by aligning its 700 names against the real 1994 MLB and NHL rosters — 82% sit exactly one edit from a real player, against 17% for a control — and then applied to a list of women prominent in the early 90s. `research/` holds the pipeline and the numbers.

ESM only. No dependencies, no build step.

## Acknowledgments

Special thanks to Sleve McDichael, Bobson Dugnutt, Dave Quitter, and Rey McSriff.

And to Aretha Flomers, Gonnie McEntare, Mora Gher, and Bjonk Nadonna.
