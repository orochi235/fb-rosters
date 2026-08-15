import { test } from 'node:test';
import assert from 'node:assert/strict';
import { generate, NAMES } from './index.js';

test('corpus is intact', () => {
  assert.equal(NAMES.length, 700);
  assert.ok(NAMES.includes('Mike Truk'));
});

test('every name is verbatim from the corpus', () => {
  const corpus = new Set(NAMES);
  for (const name of generate(200)) assert.ok(corpus.has(name), name);
});

test('a batch has no repeats', () => {
  const batch = generate(700);
  assert.equal(new Set(batch).size, 700);
});

test('past exhaustion it reshuffles rather than running dry', () => {
  assert.equal(generate(1500).length, 1500);
});

test('defaults to one name', () => {
  assert.equal(generate().length, 1);
});

test('zero is allowed, negative and fractional are not', () => {
  assert.deepEqual(generate(0), []);
  assert.throws(() => generate(-1), RangeError);
  assert.throws(() => generate(1.5), RangeError);
});
