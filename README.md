# fb94

Sample names for test fixtures, seed data, and mock rosters — drawn from, objectively, the best corpus in history: the venerable mid-90's classic *Fighting Baseball* for Super Famicom.

Its 700 player names were invented by someone working from an imperfect sense of what American baseball players are called, along with 1994 rosters from several American professional sports leagues.

```
npm install fb94
```

```js
import { generate } from 'fb94';

generate();   // ['Mike Truk']
generate(3);  // ['Bobson Dugnutt', 'Sleve McDichael', 'Rey McSriff']
```

## API

**`generate(count = 1)` → `string[]`**

Returns `count` names, always as an array. Every name is verbatim from the corpus — nothing is synthesized or recombined.

Names are dealt from a shuffled deck, so a call never repeats itself until it has used all 700. The deck persists between calls, so consecutive small calls also avoid repeats. Ask for more than 700 and it reshuffles and keeps going.

Throws `RangeError` unless `count` is a non-negative integer.

**`NAMES` → `readonly string[]`**

The full corpus in roster order, if you'd rather do your own picking.

## Without installing

Every published file is on jsDelivr, with CORS enabled, so the corpus doubles as a static endpoint:

```
https://cdn.jsdelivr.net/npm/fb94/names.json   {"count": 700, "names": [...]}
https://cdn.jsdelivr.net/npm/fb94/names.txt    newline-delimited
```

The module itself imports directly in browsers and Deno:

```js
import { generate } from 'https://cdn.jsdelivr.net/npm/fb94/index.js';
```

Pin a version in the path (`fb94@1.0.0`) if you need the bytes to never change.

## Corpus

`names.txt` is the source of truth; `names.js` and `names.json` are generated from it by `npm run build:data`, which runs automatically before publish. To correct a name, edit the text file.

ESM only. No dependencies, no build step.

## Acknowledgments

Special thanks to Sleve McDichael, Bobson Dugnutt, Dave Quitter, and Rey McSriff.
