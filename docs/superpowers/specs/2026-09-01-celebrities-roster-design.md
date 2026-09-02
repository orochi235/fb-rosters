# Second roster: mangled early-90s celebrities

For whoever implements this. Assumes familiarity with the `fb-rosters` package but
not with the conversation that produced this document.

The existing corpus is 700 names from *Fighting Baseball* (SFC, 1994) — real 1994
MLB and NHL players, altered just enough to avoid a lawsuit. It is entirely male.
This adds a second corpus built by the same process from a different source: women
who were famous in the early 1990s.

The question this answers: how do you produce a second corpus that reads as
genuinely of a piece with the first, rather than as a list of invented funny names?

## The premise

The original is not a list, it is a *function applied to a roster*. Recover the
function, then apply it to a different roster.

Working model, to be confirmed by the research pipeline below: each surname takes
**exactly one Latin-character substitution**, and first names are lifted intact and
reshuffled across the roster. The substitution is deliberate — minimum edit distance
that clears legal risk while preserving recognizability — not transcription error.

The choice of replacement character shows L1 phonological bias (L↔R, V→B, F→P),
but the process operates on Latin script throughout. **A katakana round-trip is ruled
out**: the corpus contains 71 names with clusters kana cannot represent (`Czerpaws`,
`Balgneault`, `Thidault`), preserves French orthography (`-eau`, `-ault`, `-que`),
and shows zero epenthetic vowels across 700 names. Do not reintroduce a kana step.

Target register — these are the standard, not decoration:

```
Bjonk Nadonna      Mae Jenison       Anna Nicole Smoth
Toni Norrison      Shannon Lucib     Linda Evangelisda
Whitney Loberts    Ellen Ochoo       Gabriela Sadatini
```

Two effects carry it. **Recognition**: the reader has to almost-place the name, so
sources must be famous, not merely real. **Crunch**: colliding national naming
conventions in one list, which the original got by welding MLB onto NHL.

## Compatibility constraint

Load-bearing, and easy to breach by accident. `names.json` is a documented public
endpoint — the README promises jsDelivr returns `{"count": 700, "names": [...]}`
with pinned versions guaranteeing stable bytes.

`names.txt`, `names.js`, and `names.json` must stay byte-identical. The new corpus
gets its own files.

## Shipped surface

The new corpus is off by default and unreachable without naming it.

```js
generate(3)                              // original corpus, unchanged
NAMES                                    // original corpus, unchanged
generate(3, { roster: 'celebrities' })   // opt-in
ROSTERS.athletes / ROSTERS.celebrities   // both, by name
```

- `generate(count?: number, options?: { roster?: 'athletes' | 'celebrities' | 'all' })`
- `'athletes'` names the existing corpus, so neither roster is the marked category.
- Each mode gets its own shuffle deck — three in total, fully independent. `'all'`
  cannot perturb what `generate(3)` returns.
- New files: `names-celebrities.txt` (source of truth), plus generated `.js`/`.json`.
  `build-data.js` handles both; both are added to `files` in `package.json`.

`'all'` is a deck strategy, never a corpus. **No `names-all.*` file and no
`ROSTERS.all` constant**, both of which would be a third copy to keep in sync. The
combined deck draws from the two existing arrays and never materializes a persistent
merged one. A caller who genuinely wants the concatenation writes
`[...ROSTERS.athletes, ...ROSTERS.celebrities]` and owns the copy.

Union semantics: all names shuffled together, so each roster's share is proportional
to its size. If the celebrity corpus lands short of 700 the mix tilts slightly toward
athletes, which is honest rather than something to correct with weighting.

Cost of shipping in the same tarball: ~35KB per corpus (txt 9K + js 12.5K + json 14K)
for every installer, including those who never opt in. Accepted deliberately.

This cannot be tree-shaken: one `generate` that switches on `roster` closes over both
arrays, so no bundler can prove either is unused. Subpath exports
(`fb-rosters/celebrities`) would fix it and were rejected. Anyone who wants only the
names already has a zero-install path — the per-file jsDelivr endpoints the README
documents — so the package exists for people who want the API, and they can afford
35KB. Do not re-propose subpath exports.

Document `names-celebrities.txt` / `.json` in the README's CDN section alongside the
existing endpoints.

Add `"sideEffects": false` to `package.json` regardless; the package currently lacks
it and it helps consumers who drop the package entirely.

## Research pipeline

Lives under `research/`, not shipped. Each stage writes its artifact, so every claim
is reproducible and the corpus is auditable rather than asserted.

1. Acquire 1994 MLB and 1993–94 NHL rosters → `rosters-1994.json`
2. Fuzzy-align the 700 against them → `alignments.json`
3. Fit → `model.json`: coverage %, edit-distance histogram, substitution matrix
4. Assemble the source list → `sources.txt`
5. Apply: substitution + first-name shuffle + mononym pairing
6. Filter (below)

**There is no human review pass, deliberately.** Curating the output for laughs would
produce a comedy list rather than a Fighting Baseball one. The source corpus was not
curated -- `Kevin Faite` and `Brad Klark` are not jokes -- and that unevenness is why
`Bobson Dugnutt` lands when you reach it. A hand-picked reel reads as written, which
is the one thing this cannot be. The safety and plausibility filters in stage 6 are
automated and test-guarded; they are not what is being skipped here.

**Stage 3 is a falsification test, not a formality.** If the edit-distance histogram
spikes at 1, the deliberate-minimal-edit model holds. A broad distribution means the
model is wrong and the pipeline needs rethinking before stage 5.

**Known risk — report before fitting.** Stage 2 may align only a fraction of the 700.
The alignable ones are by construction the lightly-damaged ones, so fitting on a low
yield produces a model of the easy tier presented as a model of the corpus. Publish
the coverage number first and decide explicitly whether to proceed.

## Stage 4: source domains

Every entry is a real, individually famous woman prominent in roughly 1990–95.
Estimated depth ~745, so 700 is reachable without loosening the era — which keeps
the pre-internet framing intact.

| Domain | Depth | Crunch |
|---|---|---|
| Music (Grammy + Billboard) | ~150 | med |
| Film/TV (Oscar/Emmy + unnominated TV) | ~150 | med |
| Sport (tennis, skating, gymnastics, track) | ~120 | high |
| Politics + news anchors | ~60 | high |
| Novelists | ~60 | high |
| Models | ~50 | high |
| Country music | ~40 | low |
| Tabloid | ~30 | low |
| Comedy | ~30 | low |
| Astronauts | ~20 | high |
| Business/media | ~20 | low |
| Royalty/socialites | ~15 | med |

Tennis, models, novelists, politics and astronauts supply most of the crunch; music
and film supply most of the depth.

Two selection rules:

- **Fame is the only criterion.** It admits tabloid figures and Playmates who were
  household names, and excludes the ones who were not — no carve-outs in either
  direction. `sources.txt` stays a flat undifferentiated list; per-domain section
  headers turn provenance into a claim about categories of women.
- **Exclude involuntary fame**, particularly anyone who was a minor at the time.
  Being mangled into a joke corpus is different for someone who chose publicity.

**Mononyms** (Madonna, Björk, Cher, Sade, Aaliyah) get mangled and paired with a
random surname, first name, or another mononym. Deliberately over-represent them:
in an ordinary name the surname carries recognition and the first name is filler, so
one spike per entry — a mononym pair fires twice.

## Stage 6: filters

1. **Still looks like a name.** Random single-character substitution mostly yields
   garbage (`Grace`→`Gracq`). The original 700 passed a human eye; so must these.
2. **Not some other real person.** Legal distance from the source is worthless if
   the output lands on a different real name. `Selena`→`Serena` and `Enya`→`Anya`
   are the shape of the reject.

No LLM-generated names anywhere. Every output traces to a source name plus a logged
edit — that traceability is the difference between this and writing jokes.

## Out of scope

Changing the existing corpus, its files, or its API.
