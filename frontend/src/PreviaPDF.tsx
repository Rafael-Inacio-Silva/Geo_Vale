import {useEffect, useRef, useState} from 'react';

type Manifesto = {versao: string; paginas: {numero: number; texto: string}[]};

/** Exibe páginas do mesmo PDF, renderizadas no servidor para compatibilidade entre navegadores. */
export default function PreviaPDF({minaId, versao, aoRecarregar}: {minaId: string; versao: string; aoRecarregar: () => void}) {
  const [manifesto, setManifesto] = useState<Manifesto | null>(null);
  const [pagina, setPagina] = useState(1);
  const [erroManifesto, setErroManifesto] = useState(false);
  const [estado, setEstado] = useState<'carregando' | 'pronto' | 'erro'>('carregando');
  const area = useRef<HTMLDivElement>(null);
  const base = `/api/minas/${encodeURIComponent(minaId)}/relatorio`;

  useEffect(() => {
    const controle = new AbortController();
    setErroManifesto(false);
    void fetch(`${base}/previa?versao=${encodeURIComponent(versao)}`, {signal: AbortSignal.any([controle.signal, AbortSignal.timeout(30000)])})
      .then(async resposta => {
        if (!resposta.ok) throw new Error();
        const m: Manifesto = await resposta.json();
        if (m.versao !== versao || !m.paginas.length) throw new Error();
        if (!controle.signal.aborted) setManifesto(m);
      }).catch(() => {if (!controle.signal.aborted) setErroManifesto(true);});
    return () => controle.abort();
  }, [base, versao]);

  function mudarPagina(destino: number) {
    setEstado('carregando');
    setPagina(destino);
    area.current?.scrollTo({top: 0});
  }
  function repetir() {aoRecarregar();}
  const endereco = `${base}/paginas/${pagina}?versao=${encodeURIComponent(versao)}`;
  const falhou = erroManifesto || estado === 'erro';

  return <div className="previa-pdf">
    <nav className="paginas-relatorio" aria-label="Páginas do relatório">
      <button type="button" disabled={!manifesto || pagina === 1} onClick={() => mudarPagina(pagina - 1)}>Anterior</button>
      <span role="status">{manifesto ? `Página ${pagina} de ${manifesto.paginas.length}` : 'Abrindo relatório…'}</span>
      <button type="button" disabled={!manifesto || pagina === manifesto.paginas.length} onClick={() => mudarPagina(pagina + 1)}>Próxima</button>
    </nav>
    <div className="folha-relatorio" ref={area}>
      {falhou ? <div role="alert"><p>Não foi possível visualizar esta página.</p><button className="tentar-novamente" type="button" onClick={repetir}>Tentar novamente</button></div> : null}
      {!falhou && (!manifesto || estado === 'carregando') ? <p className="carregando-folha" role="status">Carregando página…</p> : null}
      {manifesto ? <img key={endereco} src={endereco} alt={`Página ${pagina} do relatório GeoVale`} hidden={estado !== 'pronto' || erroManifesto}
        onLoad={() => setEstado('pronto')} onError={() => setEstado('erro')}/> : null}
      <p className="somente-leitor">{manifesto?.paginas[pagina - 1]?.texto ?? ''}</p>
    </div>
  </div>;
}
