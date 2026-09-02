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
