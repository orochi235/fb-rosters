import { NAMES } from './names.js';

let deck = [];

function refill(exclude) {
  deck = NAMES.slice();
  for (let i = deck.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [deck[i], deck[j]] = [deck[j], deck[i]];
  }
  if (exclude.size) {
    const fresh = deck.filter((n) => !exclude.has(n));
    deck = deck.filter((n) => exclude.has(n)).concat(fresh);
  }
}

export function generate(count = 1) {
  if (!Number.isInteger(count) || count < 0) {
    throw new RangeError(`count must be a non-negative integer, got ${count}`);
  }
  const out = [];
  const seen = new Set();
  while (out.length < count) {
    if (deck.length === 0) refill(seen.size < NAMES.length ? seen : new Set());
    const name = deck.pop();
    out.push(name);
    seen.add(name);
  }
  return out;
}

export { NAMES };
