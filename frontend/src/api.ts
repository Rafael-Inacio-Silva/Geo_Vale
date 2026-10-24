import type {Estudo} from './tipos.ts';

/** Normaliza erro público sem apresentar mensagens internas ou HTML do servidor. */
export async function requisitar<T>(url:string,opcoes:RequestInit={}):Promise<T> {
  const resposta=await fetch(url,{...opcoes,credentials:'same-origin',signal:opcoes.signal??AbortSignal.timeout(120000),headers:{'X-GeoVale':'1',...opcoes.headers}});
  let dados:unknown;
  try { dados=await resposta.json(); } catch { throw new Error('Não foi possível conectar ao serviço. Confira se a API está em execução.'); }
  if (!resposta.ok) {
    const mensagem=typeof dados==='object' && dados!==null && 'mensagem' in dados && typeof dados.mensagem==='string'?dados.mensagem:'Não foi possível concluir esta operação.';
    throw new Error(mensagem);
  }
  return dados as T;
}

/** Envia JSON com o número da versão que o usuário efetivamente consultou. */
export function operar(estudo:Estudo,acao:string,campos:Record<string,unknown>={}):Promise<Estudo> {
  return requisitar(`/api/areas/${estudo.id}/${acao}`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({versao:estudo.versao,...campos})});
}

/** Envia um único arquivo, preservando o nome sem usá-lo como identificação da mina. */
export function enviarArquivo(arquivo:File):Promise<Estudo> {
  const formulario=new FormData();formulario.append('arquivo',arquivo);
  return requisitar('/api/areas',{method:'POST',body:formulario});
}
