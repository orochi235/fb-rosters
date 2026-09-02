import { test } from 'node:test';
import assert from 'node:assert/strict';
import { generate, NAMES, CELEBRITIES, ROSTERS } from './index.js';

test('corpora are intact', () => {
  assert.equal(NAMES.length, 700);
  assert.ok(NAMES.includes('Mike Truk'));
  assert.equal(CELEBRITIES.length, 700);
  assert.equal(ROSTERS.athletes, NAMES);
  assert.equal(ROSTERS.celebrities, CELEBRITIES);
});

test('every name is verbatim from the corpus', () => {
  const corpus = new Set(NAMES);
  for (const name of generate(200)) assert.ok(corpus.has(name), name);
  const celebs = new Set(CELEBRITIES);
  for (const name of generate(200, { roster: 'celebrities' })) assert.ok(celebs.has(name), name);
});

test('a batch has no repeats', () => {
  assert.equal(new Set(generate(700)).size, 700);
  assert.equal(new Set(generate(700, { roster: 'celebrities' })).size, 700);
  assert.equal(new Set(generate(1400, { roster: 'all' })).size, 1400);
});

test('past exhaustion it reshuffles rather than running dry', () => {
  assert.equal(generate(1500).length, 1500);
  assert.equal(generate(1500, { roster: 'celebrities' }).length, 1500);
});

test('defaults to one name from the athletes roster', () => {
  const [name] = generate();
  assert.ok(NAMES.includes(name));
});

test('zero is allowed, negative and fractional are not', () => {
  assert.deepEqual(generate(0), []);
  assert.throws(() => generate(-1), RangeError);
  assert.throws(() => generate(1.5), RangeError);
});

test('an unknown roster throws', () => {
  assert.throws(() => generate(1, { roster: 'nope' }), RangeError);
  assert.throws(() => generate(1, { roster: 'toString' }), RangeError);
});

test('all draws from both corpora', () => {
  const batch = generate(1400, { roster: 'all' });
  const fromAthletes = new Set(NAMES);
  const fromCelebs = new Set(CELEBRITIES);
  assert.ok(batch.some((n) => fromAthletes.has(n)));
  assert.ok(batch.some((n) => fromCelebs.has(n)));
});

test("one roster's deck does not disturb another's no-repeat guarantee", () => {
  generate(400, { roster: 'celebrities' });
  generate(50, { roster: 'all' });
  assert.equal(new Set(generate(700)).size, 700);
});

test('the corpora are disjoint', () => {
  const overlap = NAMES.filter((n) => new Set(CELEBRITIES).has(n));
  assert.deepEqual(overlap, []);
});
