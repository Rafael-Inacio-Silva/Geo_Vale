/** Confere os pesos editados sem transformá-los silenciosamente em outra prioridade. */
export function pesosValidos(pesos:number[]):boolean {
  return pesos.length===3 && pesos.every(p=>Number.isFinite(p)&&p>=0&&p<=100) && Math.abs(pesos.reduce((a,b)=>a+b,0)-100)<1e-8;
}
/** Detecta qualquer alteração para impedir exportar o resultado anterior como se fosse atual. */
export function mesmosPesos(a:number[],b:number[]):boolean {
  return a.length===b.length && a.every((p,i)=>Math.abs(p-b[i])<1e-9);
}
