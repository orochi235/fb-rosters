import { readFileSync, writeFileSync } from 'node:fs';

const names = readFileSync('names.txt', 'utf8')
  .split('\n')
  .map((s) => s.trim())
  .filter(Boolean);

writeFileSync('names.js', `export const NAMES = ${JSON.stringify(names, null, 2)};\n`);
writeFileSync('names.json', JSON.stringify({ count: names.length, names }, null, 2));

console.log(`${names.length} names -> names.js, names.json`);
