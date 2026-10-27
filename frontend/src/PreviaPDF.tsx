import {useEffect, useRef, useState} from 'react';
import {getDocument, GlobalWorkerOptions} from 'pdfjs-dist/legacy/build/pdf.mjs';
import type {PDFDocumentLoadingTask, PDFDocumentProxy, RenderTask} from 'pdfjs-dist/legacy/build/pdf.mjs';
import trabalhador from 'pdfjs-dist/legacy/build/pdf.worker.min.mjs?url';

GlobalWorkerOptions.workerSrc = trabalhador;

/** Renderiza o mesmo PDF baixável, com paginação, adaptação à largura e texto acessível. */
export default function PreviaPDF({arquivo}: {arquivo: Blob}) {
  const [documento, setDocumento] = useState<PDFDocumentProxy | null>(null);
  const [pagina, setPagina] = useState(1);
  const [largura, setLargura] = useState(600);
  const [texto, setTexto] = useState('');
  const [erro, setErro] = useState(false);
  const [tentativa, setTentativa] = useState(0);
  const [renderizando, setRenderizando] = useState(true);
  const area = useRef<HTMLDivElement>(null);
  const tela = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    setDocumento(null);
    setErro(false);
    setRenderizando(true);
    let encerrado = false;
    let tarefa: PDFDocumentLoadingTask | undefined;
    void arquivo.arrayBuffer().then(bruto => {
      if (encerrado) return;
      tarefa = getDocument({data: new Uint8Array(bruto)});
      return tarefa.promise.then(pdf => {if (!encerrado) setDocumento(pdf);});
    }).catch(falha => {if (!encerrado) {console.error('Falha ao abrir PDF:', falha); setErro(true); setRenderizando(false);}});
    return () => {encerrado = true; if (tarefa) void tarefa.destroy().catch(() => {});};
  }, [arquivo, tentativa]);

  useEffect(() => {
    const elemento = area.current;
    if (!elemento) return;
    const ajustar = () => setLargura(Math.max(180, Math.min(960, elemento.clientWidth - 32)));
    const observador = new ResizeObserver(ajustar);
    observador.observe(elemento);
    ajustar();
    return () => observador.disconnect();
  }, []);

  useEffect(() => {
    if (!documento || !tela.current) return;
    const canvas = tela.current;
    let encerrado = false;
    let tarefa: RenderTask | undefined;
    setRenderizando(true);
    setErro(false);
    setTexto('');
    async function desenhar() {
      const folha = await documento!.getPage(pagina);
      if (encerrado) return;
      const proporcao = Math.min(window.devicePixelRatio || 1, 2);
      const escala = largura / folha.getViewport({scale: 1}).width;
      const visao = folha.getViewport({scale: escala * proporcao});
      canvas.width = Math.ceil(visao.width);
      canvas.height = Math.ceil(visao.height);
      canvas.style.width = `${largura}px`;
      canvas.style.height = `${visao.height / proporcao}px`;
      tarefa = folha.render({canvas, viewport: visao});
      await tarefa.promise;
      const conteudo = await folha.getTextContent();
      if (!encerrado) {
        setTexto(conteudo.items.map(item => 'str' in item ? item.str : '').join(' '));
        setRenderizando(false);
      }
    }
    void desenhar().catch(falha => {if (!encerrado) {console.error('Falha ao renderizar página do PDF:', falha); setErro(true); setRenderizando(false);}});
    return () => {encerrado = true; tarefa?.cancel();};
  }, [documento, pagina, largura]);

  function mudarPagina(destino: number) {
    setPagina(destino);
    area.current?.scrollTo({top: 0});
  }

  return <div className="previa-pdf">
    <nav className="paginas-relatorio" aria-label="Páginas do relatório">
      <button type="button" disabled={!documento || pagina === 1} onClick={() => mudarPagina(pagina - 1)}>Anterior</button>
      <span role="status">{documento ? `Página ${pagina} de ${documento.numPages}` : 'Abrindo PDF…'}</span>
      <button type="button" disabled={!documento || pagina === documento.numPages} onClick={() => mudarPagina(pagina + 1)}>Próxima</button>
    </nav>
    <div className="folha-relatorio" ref={area}>
      {erro ? <div role="alert"><p>Não foi possível visualizar esta página.</p><button className="tentar-novamente" type="button" onClick={() => setTentativa(v => v + 1)}>Tentar novamente</button></div> : null}
      {!erro && renderizando ? <p className="carregando-folha" role="status">Carregando página…</p> : null}
      <canvas key={pagina} ref={tela} aria-hidden="true" hidden={erro || !documento}/>
      <p className="somente-leitor">{erro ? '' : texto}</p>
    </div>
  </div>;
}
