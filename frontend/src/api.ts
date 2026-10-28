/** Consulta os contratos territoriais, com mensagem pública e tempo limitado. */
export async function requisitar<T>(url: string, sinal?: AbortSignal, limite = 25000): Promise<T> {
  let resposta: Response;
  try {
    resposta = await fetch(url, {signal: sinal ? AbortSignal.any([sinal, AbortSignal.timeout(limite)]) : AbortSignal.timeout(limite)});
  } catch {
    throw new Error('Não foi possível conectar. Confira sua conexão e tente novamente.');
  }
  if (!resposta.ok) {
    const dados = await resposta.json().catch(() => null);
    throw new Error(typeof dados?.mensagem === 'string' ? dados.mensagem : 'Não foi possível carregar o mapa. Tente novamente.');
  }
  return resposta.json() as Promise<T>;
}
