import assert from 'node:assert/strict';
import test from 'node:test';
import {readFileSync} from 'node:fs';
import {filtrarMinas} from '../src/busca.mjs';

const minas = JSON.parse(readFileSync(new URL('../../dados/minas.json', import.meta.url), 'utf8'));
const ids = lista => lista.map(mina => mina.id);

test('catálogo expõe Horizontes e Abóboras, sem duplicar o nome anterior da Horizontes', () => {
  assert.deepEqual(ids(filtrarMinas(minas, '')), ['horizontes', 'aboboras']);
  assert.deepEqual(ids(filtrarMinas(minas, 'HORIZONTES')), ['horizontes']);
  assert.deepEqual(ids(filtrarMinas(minas, 'capitao do mato')), ['horizontes']);
  assert.deepEqual(ids(filtrarMinas(minas, 'aboboras')), ['aboboras']);
  assert.equal(filtrarMinas(minas, '  Nova   Lima  ').length, 2);
});

test('consulta sem correspondência não inventa outra mina', () => {
  assert.deepEqual(filtrarMinas(minas, 'Itabira'), []);
  assert.equal(filtrarMinas(minas, 'Vale Nova Lima').length, 2);
});
