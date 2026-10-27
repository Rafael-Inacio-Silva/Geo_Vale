import {useEffect, useRef, useState} from 'react';
import L from 'leaflet';
import {requisitar} from './api.ts';
import type {AguaExtraida} from './tipos.ts';

/** Consulta sob demanda o recorte fixo e conserva o resultado ao alternar modos/barras. */
export default function ExtracaoAgua({mapa, minaId, visivel}: {mapa: L.Map | null; minaId?: string; visivel: boolean}) {
  const [dados, setDados] = useState<AguaExtraida | null>(null);
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState('');
  const [mostrar, setMostrar] = useState(true);
  const pedido = useRef<AbortController | null>(null);

  useEffect(() => {
    pedido.current?.abort();
    setDados(null);
    setErro('');
    setCarregando(false);
    setMostrar(true);
    return () => {pedido.current?.abort();};
  }, [minaId]);

  useEffect(() => {
    if (!mapa || !dados || !visivel || !mostrar || !minaId) return;
    if (!mapa.getPane('agua-extraida')) mapa.createPane('agua-extraida').style.zIndex = '440';
    const camada = L.geoJSON(dados, {
      pane: 'agua-extraida',
      attribution: 'Água recortada: <a href="https://geoportal.meioambiente.mg.gov.br" target="_blank" rel="noopener noreferrer">IDE-Sisema / ANA / Igam</a>',
      style: feicao => ({color: feicao?.properties.base === 'massas' ? '#076894' : '#006bb0', weight: 3, fillColor: '#169fda', fillOpacity: .4}),
      onEachFeature: (feicao, camadaFeicao) => {
        const texto = document.createElement('span');
        texto.textContent = `${feicao.properties.nome ?? 'Sem nome publicado'} · ${feicao.properties.base === 'trechos' ? 'Trecho hidrográfico' : 'Massa d’água'} · ${feicao.properties.id_fonte}`;
        camadaFeicao.bindTooltip(texto);
      },
    }).addTo(mapa);
    return () => {camada.remove();};
  }, [mapa, dados, visivel, mostrar, minaId]);

  async function extrair() {
    if (!minaId || carregando) return;
    pedido.current?.abort();
    const controle = new AbortController();
    pedido.current = controle;
    setCarregando(true);
    setErro('');
    // Um resultado anterior não é apresentado como se fosse uma consulta nova bem-sucedida.
    setDados(null);
    try {
      const resultado = await requisitar<AguaExtraida>(`/api/minas/${encodeURIComponent(minaId)}/agua-influencia`, controle.signal);
      if (!controle.signal.aborted) setDados(resultado);
    } catch (falha) {
      if (!controle.signal.aborted) setErro(falha instanceof Error ? falha.message : 'Não foi possível extrair os dados de água.');
    } finally {
      if (!controle.signal.aborted) setCarregando(false);
    }
  }

  return <div className="extracao-agua" hidden={!visivel}>
    <h3>Conhecer a água</h3>
    <p className="nota-area">Recorte: Águas e solos · AID. Os filtros acima alteram apenas a visualização.</p>
    <button type="button" className="acao-area primaria" disabled={!minaId || carregando} onClick={() => {void extrair();}}>{carregando ? 'Extraindo…' : dados ? 'Consultar novamente' : erro ? 'Tentar extração novamente' : 'Extrair dados de água'}</button>
    {carregando ? <p className="nota-area" role="status">Consultando e recortando as duas bases…</p> : null}
    {erro ? <p className="erro-area" role="alert">{erro}</p> : null}
    {dados ? <>
      <div className="resumo-agua" role="status">
        <p><strong>{dados.resumo.trechos}</strong> trechos hidrográficos</p>
        <p><strong>{dados.resumo.massas}</strong> massas d’água</p>
      </div>
      <p className="nota-area">Registros que intersectam o recorte. Trechos do mesmo rio contam separadamente.</p>
      {dados.features.length ? <label className="seletor-tema"><input type="checkbox" checked={mostrar} onChange={evento => setMostrar(evento.target.checked)}/><span>Mostrar água recortada no mapa</span></label> : <p className="nota-area">Nenhum registro encontrado nessas bases para este recorte.</p>}
      <p className="nota-area">Consulta: <time dateTime={dados.consultado_em}>{new Date(dados.consultado_em).toLocaleString('pt-BR')}</time></p>
      <details className="fonte-referencias"><summary>Registros e fontes</summary>
        <p>AID aproximada do projeto Tamanduá/Horizontes. <a href={dados.recorte.fonte} target="_blank" rel="noopener noreferrer">Parecer FEAM · Fig. 2.3 · p. 18</a>, mapa de 02/11/2023.</p>
        {dados.fontes.map(fonte => <p key={fonte.id}><a href={fonte.metadado} target="_blank" rel="noopener noreferrer">{fonte.nome} · IDE-Sisema</a><br/>Versões publicadas: {[...fonte.versoes_publicadas, ...fonte.revisoes_publicadas].join('; ') || 'Não informadas nos registros encontrados'}.</p>)}
        <p>Data da consulta não é data de levantamento. Sem análise da qualidade da água, impacto ou segurança.</p>
        <ul className="registros-agua">{dados.features.map(feicao => <li key={feicao.properties.id_fonte}>
          <strong>{feicao.properties.nome ?? 'Sem nome publicado'}</strong><br/>
          {feicao.properties.base === 'trechos' ? 'Trecho hidrográfico' : 'Massa d’água'}{feicao.properties.tipo_publicado ? ` · ${feicao.properties.tipo_publicado}` : ''}<br/>
          <span>{feicao.properties.id_fonte}</span>
        </li>)}</ul>
      </details>
    </> : null}
    <p className="nota-area">Caracterização preliminar em contorno aproximado. Não define intervenção ou limite de fechamento.</p>
  </div>;
}
