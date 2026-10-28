import {useEffect, useRef, useState} from 'react';

/** Abre, sobre o mapa, a ilustração em vídeo da área recuperada, gerada previamente e servida pela API. */
export default function VideoPosMineracao({minaId, pronto}: {minaId: string; pronto: boolean}) {
  const [aberto, setAberto] = useState(false);
  const [erro, setErro] = useState(false);
  const dialogo = useRef<HTMLDialogElement>(null);
  const gatilho = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (aberto) dialogo.current?.showModal();
    else dialogo.current?.close();
  }, [aberto]);

  return <>
    <button ref={gatilho} type="button" className="abrir-influencia video-pos-mineracao" disabled={!pronto} onClick={() => {setErro(false); setAberto(true);}}>
      Ver pós-mineração <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 6h12v12H4zM16 10l4-2v8l-4-2"/></svg>
    </button>
    <dialog ref={dialogo} className="dialogo-relatorio dialogo-video" aria-labelledby="titulo-video" onClose={() => {setAberto(false); gatilho.current?.focus();}}>
      <header className="cabecalho-relatorio">
        <h2 id="titulo-video">Pós-mineração</h2>
        <div className="acoes-relatorio">
          <button type="button" aria-label="Fechar vídeo" onClick={() => dialogo.current?.close()}>Fechar <span aria-hidden="true">×</span></button>
        </div>
      </header>
      {aberto ? <figure className="figura-video">
        {erro ? <p className="estado-relatorio" role="alert">Vídeo indisponível para esta mina.</p>
          : <video src={`/api/minas/${encodeURIComponent(minaId)}/video`} controls autoPlay playsInline onError={() => setErro(true)}/>}
        <figcaption>
          Ilustração gerada previamente por IA, não é projeto. Em cima, o sobrevoo atual; embaixo, o mesmo voo com a área minerada recuperada,
          a partir de uma imagem de referência editada no ChatGPT e do vídeo gerado pelo Luma Ray 3.2 (fal.ai). No produto, o vídeo seria gerado
          sob demanda a partir da sugestão de uso. Imagens © Google.
        </figcaption>
      </figure> : null}
    </dialog>
  </>;
}
