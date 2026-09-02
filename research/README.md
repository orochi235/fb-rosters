# Research pipeline

Recovers the transform that produced the `athletes` corpus, so the `celebrities`
corpus can be built by the same process rather than by writing jokes. See
`../docs/superpowers/specs/2026-09-01-celebrities-roster-design.md`.

Run in order:

    ./fetch-rosters.sh     # stage 1 -> artifacts/rosters-1994.json (1858 players)
    python3 align.py       # stage 2 -> artifacts/alignments.json
    python3 fit.py         # stage 3 -> artifacts/model.json

`align.py` also runs a null model — 577 real MLB surnames from 1974, the same
naming culture but two decades too early to be the source. Without it the
alignment rate means nothing, since ~1550 surnames make coincidental matches
common. Keep it in any rerun.

## Result

| surname edit distance | corpus (700) | null (577) |
|---|---|---|
| 0 | 1.7% | 0.0% |
| 1 | 82.4% | 17.5% |
| 2 | 11.9% | 39.2% |
| 3+ | 4.0% | 43.3% |

Of 503 unambiguous distance-1 pairs: 97.4% substitutions, and 86.9% of those fall
on the **first letter of the surname**. Consonants swap for consonants (448) and
vowels for vowels (34); the classes almost never cross.

c↔k accounts for 37 substitutions and does not change pronunciation at all
(`Klark`←Clark, `Cozlov`←Kozlov). That rules out transcription error as the
mechanism — it is a respelling, done in Latin script, to clear legal distance while
keeping the name recognizable. A phonological bias is still visible in *which*
letter gets chosen (r↔l 54, b↔v 21, f↔p 14), but it rides on top of a deliberate
minimal edit.

First names are not mangled so much as reshuffled: 625/700 appear verbatim among
real 1994 players.

## Stages 4-6: building the celebrities corpus

    python3 merge-sources.py            # stage 4 -> artifacts/sources.txt
    python3 generate-celebrities.py 0.35   # stages 5-6 -> artifacts/names-celebrities.txt

The argument is the first-name mangle rate. The source corpus sits at 8%, but its
first-name pool is generic and heavily repeated (Mike x22 across 700), which
anonymizes without any edit. The celebrity pool is flat and distinctive, so an
untouched "Whitney" is a full recognition spike where an untouched "Mike" is not.
0.35 compensates; past ~0.5 both halves of the name are wrong and it reads as random
rather than uncanny.

### Wikidata is capped on purpose

Sitelink count across language Wikipedias is a real fame ranking, and a sweep of 24
occupations yielded 2434 women born 1935-68. Using it uncapped made the output
*worse*: its depth is women famous *internationally and durably*, which is a
different set from women an American recognized in 1994. Recognition, not depth, is
the binding constraint. Hence `WIKIDATA_CAP = 140`.

Two systematic biases, both worth knowing before raising that cap:

- **Fame arrives late in politics.** Sitelinks rank Kamala Harris first and surface
  Theresa May, von der Leyen and three post-2000 Nobel laureates. Those categories
  are dropped and the hand list supplies the era's political figures.
- **The sweep barely returns women athletes, but mostly through its own faults.**
  An earlier version of this file blamed thin coverage of women's sport across
  language Wikipedias. Checking that: widening the birth window to 1930-1977 takes
  tennis from 45 to 87, so the 1935-1968 cutoff was excluding the athletes who
  peaked in 1994; and the figure-skater and gymnast QIDs are wrong, returning
  badminton players, a politician and a boxer. Fix the queries before drawing any
  conclusion about coverage from them.

  What does survive as a coverage signal, both in-window and correctly categorized:
  bell hooks has 61 sitelinks (rank 286) while Marcia Clark, a US household name in
  1995, does not clear 22. Sitelinks track durable academic and canonical standing
  better than they track what was mass-popular in a given year.

  Sport comes from the hand list either way, which is where most of the corpus's
  international crunch comes from.

### Filters

1. **Still looks like a name** — the mangled surname must open with an onset real
   surnames use and contain only trigrams attested in real surnames. Derived from
   the 1994 universe, not written by hand. This is what kills `Tlark`, `Rpelling`,
   `Bvereva`.
2. **Not another real person** — no output may equal a real name.
3. **Not a male first name** — the 1994 athlete universe is entirely male, so it
   doubles as the reject list when a mangle turns Doris into Boris.
4. **Not an unfortunate word** — a small denylist; the human pass is the backstop.
