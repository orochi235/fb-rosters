import { readFileSync, writeFileSync } from 'node:fs';

const CORPORA = [
  { txt: 'names.txt', js: 'names.js', json: 'names.json', symbol: 'NAMES' },
  { txt: 'names-celebrities.txt', js: 'names-celebrities.js', json: 'names-celebrities.json',
    symbol: 'CELEBRITIES' },
];

for (const { txt, js, json, symbol } of CORPORA) {
  const names = readFileSync(txt, 'utf8')
    .split('\n')
    .map((s) => s.trim())
    .filter(Boolean);

  writeFileSync(js, `export const ${symbol} = ${JSON.stringify(names, null, 2)};\n`);
  writeFileSync(json, JSON.stringify({ count: names.length, names }, null, 2));

  console.log(`${names.length} names -> ${js}, ${json}`);
}
