import { NAMES } from './names.js';
import { CELEBRITIES } from './names-celebrities.js';

export const ROSTERS = Object.freeze({ athletes: NAMES, celebrities: CELEBRITIES });

// 'all' deals from both arrays; it is a deck strategy, not a third corpus.
const SOURCES = { athletes: [NAMES], celebrities: [CELEBRITIES], all: [NAMES, CELEBRITIES] };

const decks = { athletes: [], celebrities: [], all: [] };

function sizeOf(roster) {
  return SOURCES[roster].reduce((n, corpus) => n + corpus.length, 0);
}

function refill(roster, exclude) {
  let deck = [];
  for (const corpus of SOURCES[roster]) deck = deck.concat(corpus);
  for (let i = deck.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [deck[i], deck[j]] = [deck[j], deck[i]];
  }
  if (exclude.size) {
    const fresh = deck.filter((n) => !exclude.has(n));
    deck = deck.filter((n) => exclude.has(n)).concat(fresh);
  }
  decks[roster] = deck;
}

export function generate(count = 1, options = {}) {
  if (!Number.isInteger(count) || count < 0) {
    throw new RangeError(`count must be a non-negative integer, got ${count}`);
  }
  const { roster = 'athletes' } = options;
  if (!Object.hasOwn(SOURCES, roster)) {
    throw new RangeError(
      `roster must be one of ${Object.keys(SOURCES).join(', ')}, got ${roster}`,
    );
  }
  const total = sizeOf(roster);
  const out = [];
  const seen = new Set();
  while (out.length < count) {
    if (decks[roster].length === 0) refill(roster, seen.size < total ? seen : new Set());
    const name = decks[roster].pop();
    out.push(name);
    seen.add(name);
  }
  return out;
}

export { NAMES, CELEBRITIES };
