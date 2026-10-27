import {lazy, Suspense, useEffect, useRef, useState} from 'react';

const PreviaPDF = lazy(() => import('./PreviaPDF.tsx'));

/** Abre o PDF da mina selecionada e permite baixar exatamente o documento visualizado. */
export default function RelatorioDaMina({minaId, pronto}: {minaId: string; pronto: boolean}) {
  const [aberto, setAberto] = useState(false);
  const [url, setUrl] = useState('');
  const [arquivo, setArquivo] = useState<Blob | null>(null);
  const [erro, setErro] = useState(false);
  const [tentativa, setTentativa] = useState(0);
  const dialogo = useRef<HTMLDialogElement>(null);
  const gatilho = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (aberto) dialogo.current?.showModal();
    else dialogo.current?.close();
  }, [aberto]);

  useEffect(() => {
    setUrl('');
    setArquivo(null);
    setErro(false);
    if (!aberto) return;
    const controle = new AbortController();
    let objeto = '';
    async function carregar() {
      try {
        const resposta = await fetch(`/api/minas/${encodeURIComponent(minaId)}/relatorio`, {signal: AbortSignal.any([controle.signal, AbortSignal.timeout(60000)])});
        if (!resposta.ok || !resposta.headers.get('content-type')?.startsWith('application/pdf')) throw new Error();
        const arquivo = await resposta.blob();
        if (controle.signal.aborted) return;
        objeto = URL.createObjectURL(arquivo);
        setUrl(objeto);
        setArquivo(arquivo);
      } catch {
        if (!controle.signal.aborted) setErro(true);
      }
    }
    void carregar();
    return () => {controle.abort(); if (objeto) URL.revokeObjectURL(objeto);};
  }, [aberto, minaId, tentativa]);

  return <>
    <button ref={gatilho} type="button" className="relatorio-territorio" disabled={!pronto} onClick={() => setAberto(true)}><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 3h8l4 4v14H6zM14 3v5h4M9 12h6M9 16h6"/></svg>{pronto ? 'Ver relatório' : 'Preparando relatório…'}</button>
    <dialog ref={dialogo} className="dialogo-relatorio" aria-labelledby="titulo-relatorio" onClose={() => {setAberto(false); gatilho.current?.focus();}}>
      <header className="cabecalho-relatorio">
        <h2 id="titulo-relatorio">Relatório da mina</h2>
        <div className="acoes-relatorio">
          {url ? <a href={url} download={`geovale-${minaId}.pdf`}>Baixar PDF</a> : null}
          <button type="button" aria-label="Fechar relatório" onClick={() => dialogo.current?.close()}>Fechar <span aria-hidden="true">×</span></button>
        </div>
      </header>
      {arquivo ? <Suspense fallback={<div className="estado-relatorio" role="status">Abrindo PDF…</div>}><PreviaPDF arquivo={arquivo}/></Suspense>
        : <div className="estado-relatorio">{erro ? <div role="alert"><p>Não foi possível abrir o relatório.</p><button className="tentar-novamente" type="button" onClick={() => setTentativa(v => v + 1)}>Tentar novamente</button></div> : <p role="status">Gerando relatório…</p>}</div>}
    </dialog>
  </>;
}
