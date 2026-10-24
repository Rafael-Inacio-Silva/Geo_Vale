import test from 'node:test';
import assert from 'node:assert/strict';
import {pesosValidos,mesmosPesos} from '../src/pesos.ts';
test('pesos somam cem, com zero permitido e sem ajuste silencioso',()=>{
 assert.equal(pesosValidos([33.34,33.33,33.33]),true);assert.equal(pesosValidos([0,0,100]),true);
 for(const p of [[30,30,30],[-1,1,100],[NaN,0,100],[Infinity,0,0],[]])assert.equal(pesosValidos(p),false);
});
test('edição invalida resultado e exportação anterior',()=>{
 assert.equal(mesmosPesos([30,30,40],[30,30,40]),true);
 assert.equal(mesmosPesos([31,30,39],[30,30,40]),false);
 assert.equal(mesmosPesos([NaN,30,40],[30,30,40]),false);
});
