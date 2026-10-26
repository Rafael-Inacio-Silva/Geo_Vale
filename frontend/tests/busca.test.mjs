import assert from 'node:assert/strict';
import test from 'node:test';
import {readFileSync} from 'node:fs';
import {filtrarMinas} from '../src/busca.mjs';

const minas = JSON.parse(readFileSync(new URL('../../dados/minas.json', import.meta.url), 'utf8'));

test('catálogo expõe apenas Horizontes, sem duplicar seu nome anterior', () => {
  assert.deepEqual(filtrarMinas(minas, '').map(mina => mina.id), ['horizontes']);
  assert.equal(filtrarMinas(minas, 'HORIZONTES').length, 1);
  assert.equal(filtrarMinas(minas, 'capitao do mato').length, 1);
  assert.equal(filtrarMinas(minas, '  Nova   Lima  ').length, 1);
});

test('consulta sem correspondência não inventa outra mina', () => {
  assert.deepEqual(filtrarMinas(minas, 'Itabira'), []);
  assert.equal(filtrarMinas(minas, 'Vale Nova Lima').length, 1);
});
