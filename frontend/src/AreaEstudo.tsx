import {useEffect, useRef, useState} from 'react';
import L from 'leaflet';
import 'leaflet-draw';
import 'leaflet-draw/dist/leaflet.draw.css';
import type {AreaConfirmada, AreaManual, ProcessoANM} from './tipos.ts';

type Fase = 'vazia' | 'carregando_anm' | 'previa_anm' | 'desenhando' | 'ajustando' | 'validando' | 'confirmada';
const ESTILO = {color: '#ffc329', weight: 3, opacity: 1, fillColor: '#ffc329', fillOpacity: .15};

L.drawLocal.draw.handlers.polygon.tooltip = {
  start: 'Clique ou toque para marcar o primeiro ponto.',
  cont: 'Continue marcando o contorno.',
  end: 'Toque no primeiro ponto ou use Fechar contorno.',
};
L.drawLocal.draw.handlers.polyline.error = 'Os lados do contorno não podem se cruzar.';
L.drawLocal.edit.handlers.edit.tooltip = {text: 'Arraste os pontos para ajustar a área.', subtext: 'Confirme quando terminar.'};

/** Mantém várias áreas independentes; confirma, edita e restaura cada recorte sem persistência. */
export default function AreaEstudo({mapa, minaId, obterProcessoANM, aoInteragir}: {aoInteragir: () => void; mapa: L.DrawMap | null; minaId?: string; obterProcessoANM: () => Promise<ProcessoANM>}) {
  const [fase, setFase] = useState<Fase>('vazia');
  const faseAtual = useRef<Fase>('vazia');
  const [pontos, setPontos] = useState(0);
  const [erro, setErro] = useState('');
  const [lista, setLista] = useState<{id: number; dados: AreaConfirmada}[]>([]);
  const areas = useRef(new Map<number, AreaConfirmada>());
  const ativa = useRef<number | null>(null);
  const anterior = useRef<number | null>(null);
  const sequencia = useRef(0);
  const outras = useRef<L.FeatureGroup | null>(null);
  const [area, setArea] = useState<AreaConfirmada | null>(null);
  const confirmada = useRef<AreaConfirmada | null>(null);
  const rascunhoANM = useRef<ProcessoANM | null>(null);
  const minaAtual = useRef(minaId);
  minaAtual.current = minaId;
  const pedido = useRef<AbortController | null>(null);
  const recursos = useRef<{grupo: L.FeatureGroup; desenho: L.Draw.Polygon | null; editor: L.EditToolbar.Edit | null} | null>(null);

  function mudarFase(valor: Fase) {faseAtual.current = valor; setFase(valor);}

  function poligonoAtual() {
    return recursos.current?.grupo.getLayers().find(item => item instanceof L.Polygon) as L.Polygon | undefined;
  }

  function prepararEdicao() {
    const estado = recursos.current;
    if (!mapa || !estado) return;
    estado.editor?.disable();
    estado.editor = new L.EditToolbar.Edit(mapa, {featureGroup: estado.grupo, poly: {allowIntersection: false}, selectedPathOptions: {...ESTILO, dashArray: '7 5'}});
    estado.editor.enable();
  }

  function exibirArea(dados: AreaConfirmada, confirmacao = false) {
    const grupo = recursos.current?.grupo;
    if (!grupo) return;
    grupo.clearLayers();
    L.geoJSON(dados, {pane: 'area-estudo', style: {...ESTILO, fillColor: confirmacao ? '#007f73' : ESTILO.fillColor}}).eachLayer(camada => {
      if (dados.properties.origem === 'processo_anm') camada.options.attribution = 'Área cadastral: <a href="https://geo.anm.gov.br/portal/">ANM</a>';
      grupo.addLayer(camada);
    });
  }

  function atualizarOutras() {
    const grupo = outras.current;
    if (!grupo) return;
    grupo.clearLayers();
    for (const [id, dados] of areas.current) {
      if (id === ativa.current) continue;
      L.geoJSON(dados, {pane: 'area-estudo', style: {color: '#007f73', weight: 3, fillColor: '#007f73', fillOpacity: .12}}).eachLayer(camada => {
        if (dados.properties.origem === 'processo_anm') camada.options.attribution = 'Área cadastral: <a href="https://geo.anm.gov.br/portal/">ANM</a>';
        const nome = document.createElement('span');
        nome.textContent = `Área ${id}`;
        camada.bindTooltip(nome);
        camada.on('click', () => {if (faseAtual.current === 'confirmada' || faseAtual.current === 'vazia') selecionarArea(id);});
        grupo.addLayer(camada);
      });
    }
  }

  function selecionarArea(id: number) {
    const dados = areas.current.get(id);
    if (!dados) return;
    aoInteragir();
    ativa.current = id;
    anterior.current = null;
    confirmada.current = dados;
    setArea(dados);
    exibirArea(dados, true);
    atualizarOutras();
    setErro('');
    mudarFase('confirmada');
    const poligono = poligonoAtual();
    if (poligono) mapa?.fitBounds(poligono.getBounds(), {paddingTopLeft: [32, 64], paddingBottomRight: [32, 64], maxZoom: 18});
  }

  function iniciarAdicao() {
    anterior.current = ativa.current;
    ativa.current = null;
    confirmada.current = null;
    setArea(null);
    atualizarOutras();
  }

  function guardarArea(dados: AreaConfirmada) {
    const id = ativa.current ?? ++sequencia.current;
    areas.current.set(id, dados);
    ativa.current = id;
    anterior.current = null;
    confirmada.current = dados;
    setArea(dados);
    setLista([...areas.current].map(([chave, valor]) => ({id: chave, dados: valor})));
    atualizarOutras();
    exibirArea(dados, true);
    mudarFase('confirmada');
  }

  function restaurarConfirmada() {
    pedido.current?.abort();
    rascunhoANM.current = null;
    if (anterior.current !== null) {
      ativa.current = anterior.current;
      confirmada.current = areas.current.get(anterior.current) ?? null;
      setArea(confirmada.current);
      anterior.current = null;
    }
    atualizarOutras();
    mudarFase(confirmada.current ? 'confirmada' : 'vazia');
    const estado = recursos.current;
    if (!estado) return;
    estado.desenho?.disable();
    estado.editor?.disable();
    estado.grupo.clearLayers();
    if (confirmada.current) exibirArea(confirmada.current, true);
    setPontos(0);
    setErro('');
  }

  useEffect(() => {
    if (!mapa) return;
    if (!mapa.getPane('area-estudo')) mapa.createPane('area-estudo').style.zIndex = '450';
    const grupo = L.featureGroup().addTo(mapa);
    const demais = L.featureGroup().addTo(mapa);
    outras.current = demais;
    const estado = {grupo, desenho: null as L.Draw.Polygon | null, editor: null as L.EditToolbar.Edit | null};
    recursos.current = estado;
    let encerrado = false;
    const aoCriar = (evento: L.LeafletEvent) => {
      if (encerrado) return;
      const criado = evento as L.DrawEvents.Created;
      if (criado.layerType !== 'polygon') return;
      grupo.clearLayers();
      rascunhoANM.current = null;
      const poligono = criado.layer as L.Polygon;
      poligono.options.pane = 'area-estudo';
      grupo.addLayer(poligono);
      mudarFase('ajustando');
      const anel = poligono.toGeoJSON().geometry.coordinates[0];
      setPontos(anel.length - 1);
      estado.editor = new L.EditToolbar.Edit(mapa, {featureGroup: grupo, poly: {allowIntersection: false}, selectedPathOptions: {...ESTILO, dashArray: '7 5'}});
      estado.editor.enable();
    };
    const aoMarcarPonto = (evento: L.LeafletEvent) => setPontos((evento as L.LeafletEvent & {layers: L.LayerGroup}).layers.getLayers().length);
    const aoEditarPonto = () => {
      const poligono = grupo.getLayers()[0] as L.Polygon | undefined;
      if (poligono) setPontos(poligono.toGeoJSON().geometry.coordinates[0].length - 1);
      setErro('');
    };
    const aoPararDesenho = () => {
      if (!encerrado && faseAtual.current === 'desenhando') {
        restaurarConfirmada();
      }
    };
    const limpar = () => {
      if (encerrado) return;
      encerrado = true;
      pedido.current?.abort();
      estado.desenho?.disable();
      estado.editor?.disable();
      mapa.off(L.Draw.Event.CREATED, aoCriar);
      mapa.off(L.Draw.Event.DRAWVERTEX, aoMarcarPonto);
      mapa.off(L.Draw.Event.EDITVERTEX, aoEditarPonto);
      mapa.off(L.Draw.Event.DRAWSTOP, aoPararDesenho);
      mapa.off('unload', limpar);
      grupo.remove();
      demais.remove();
      if (outras.current === demais) outras.current = null;
      if (recursos.current === estado) recursos.current = null;
    };
    mapa.on(L.Draw.Event.CREATED, aoCriar);
    mapa.on(L.Draw.Event.DRAWVERTEX, aoMarcarPonto);
    mapa.on(L.Draw.Event.EDITVERTEX, aoEditarPonto);
    mapa.on(L.Draw.Event.DRAWSTOP, aoPararDesenho);
    mapa.on('unload', limpar);
    return limpar;
  }, [mapa]);

  function desenhar() {
    const estado = recursos.current;
    if (!mapa || !estado) return;
    aoInteragir();
    pedido.current?.abort();
    estado.desenho?.disable();
    estado.editor?.disable();
    estado.grupo.clearLayers();
    setErro('');
    setPontos(0);
    rascunhoANM.current = null;
    mudarFase('desenhando');
    estado.desenho = new L.Draw.Polygon(mapa, {
      allowIntersection: false, showArea: false, showLength: false, maxPoints: 500,
      shapeOptions: {...ESTILO, pane: 'area-estudo'},
      drawError: {color: '#a73720', message: 'Os lados do contorno não podem se cruzar.'},
    });
    estado.desenho.enable();
  }

  async function carregarAreaANM() {
    if (!mapa || !minaId) return;
    aoInteragir();
    const solicitada = minaId;
    const controle = new AbortController();
    pedido.current?.abort();
    pedido.current = controle;
    recursos.current?.editor?.disable();
    mudarFase('carregando_anm');
    setErro('');
    try {
      const dados = await obterProcessoANM();
      if (controle.signal.aborted) return;
      if (minaAtual.current !== solicitada) {restaurarConfirmada(); return;}
      rascunhoANM.current = dados;
      exibirArea(dados);
      setPontos(dados.properties.vertices);
      mudarFase('previa_anm');
      const poligono = poligonoAtual();
      if (poligono) mapa.fitBounds(poligono.getBounds(), {paddingTopLeft: [32, 64], paddingBottomRight: [32, 64], maxZoom: 18});
    } catch (falha) {
      if (controle.signal.aborted) return;
      restaurarConfirmada();
      if (minaAtual.current === solicitada) setErro(falha instanceof Error ? falha.message : 'Não foi possível carregar o polígono da ANM.');
    }
  }

  async function confirmar() {
    const poligono = poligonoAtual();
    if (!poligono) return;
    if (rascunhoANM.current) {
      const dados = rascunhoANM.current;
      rascunhoANM.current = null;
      guardarArea(dados);
      return;
    }
    recursos.current?.editor?.disable();
    const controle = new AbortController();
    pedido.current?.abort();
    pedido.current = controle;
    mudarFase('validando');
    setErro('');
    try {
      const resposta = await fetch('/api/area/validar', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(poligono.toGeoJSON()), signal: AbortSignal.any([controle.signal, AbortSignal.timeout(15000)])});
      const dados = await resposta.json();
      if (controle.signal.aborted) return;
      if (!resposta.ok) throw new Error(typeof dados.mensagem === 'string' ? dados.mensagem : 'Não foi possível confirmar a área.');
      guardarArea(dados as AreaManual);
    } catch (falha) {
      if (controle.signal.aborted) return;
      setErro(falha instanceof Error && falha.name === 'Error' ? falha.message : 'Não foi possível confirmar a área. Tente novamente.');
      prepararEdicao();
      mudarFase('ajustando');
    }
  }

  function remover() {
    if (ativa.current !== null) areas.current.delete(ativa.current);
    const restante = [...areas.current.keys()].at(-1);
    setLista([...areas.current].map(([id, dados]) => ({id, dados})));
    if (restante !== undefined) {selecionarArea(restante); return;}
    ativa.current = null;
    anterior.current = null;
    confirmada.current = null;
    setArea(null);
    restaurarConfirmada();
  }

  return <section className={`area-estudo fase-${fase}`} aria-label="Área de estudo" onKeyDown={evento => {if (evento.key === 'Escape' && (faseAtual.current === 'desenhando' || faseAtual.current === 'carregando_anm' || faseAtual.current === 'previa_anm')) {evento.stopPropagation(); restaurarConfirmada();}}}>
    {lista.length > 0 && fase === 'confirmada' ? <div className="lista-areas" role="group" aria-label="Áreas demarcadas"><span>Áreas ({lista.length})</span>{lista.map(item => <button type="button" className="acao-area" key={item.id} aria-label={`Selecionar área ${item.id}`} aria-pressed={ativa.current === item.id} onClick={() => selecionarArea(item.id)}>Área {item.id}</button>)}</div> : null}
    {fase === 'vazia' ? <div className="acoes-area"><button type="button" className="acao-area primaria" disabled={!mapa} onClick={desenhar}>Desenhar área</button><button type="button" className="acao-area" disabled={!mapa || !minaId} title={!minaId ? 'Selecione uma mina para carregar o processo.' : 'Carregar a poligonal do processo minerário'} onClick={() => {void carregarAreaANM();}}>Polígono ANM</button></div> : null}
    {fase === 'carregando_anm' ? <><p className="estado-area" role="status">Carregando polígono da ANM…</p><button type="button" className="acao-area" onClick={restaurarConfirmada}>Cancelar</button></> : null}
    {fase === 'previa_anm' ? <><p className="estado-area" role="status">Processo ANM {rascunhoANM.current?.properties.processo}</p><p className="nota-area">Poligonal cadastral para a área de estudo.</p><div className="acoes-area"><button type="button" className="acao-area primaria" onClick={() => {void confirmar();}}>Confirmar área</button><button type="button" className="acao-area" onClick={restaurarConfirmada}>Cancelar</button></div></> : null}
    {fase === 'desenhando' ? <>
      <p className="estado-area" role="status">Marque os pontos no mapa · {pontos} pontos</p>
      <div className="acoes-area"><button type="button" className="acao-area primaria" disabled={pontos < 3} onClick={() => recursos.current?.desenho?.completeShape()}>Fechar contorno</button><button type="button" className="acao-area" disabled={!pontos} onClick={() => {if (pontos === 1) desenhar(); else recursos.current?.desenho?.deleteLastVertex();}}>Desfazer ponto</button><button type="button" className="acao-area" onClick={restaurarConfirmada}>Cancelar</button></div>
    </> : null}
    {fase === 'ajustando' || fase === 'validando' ? <>
      <p className="estado-area" role="status">{fase === 'validando' ? 'Confirmando área…' : 'Ajuste os pontos e confirme a área.'}</p>
      <div className="acoes-area"><button type="button" className="acao-area primaria" disabled={fase === 'validando'} onClick={() => {void confirmar();}}>Confirmar área</button><button type="button" className="acao-area" onClick={restaurarConfirmada}>Cancelar</button></div>
    </> : null}
    {fase === 'confirmada' ? <>
      <p className="estado-area" role="status">{area?.properties.origem === 'processo_anm' ? `Área ${ativa.current} · Processo ANM ${(area as ProcessoANM).properties.processo}` : `Área ${ativa.current} confirmada · ${area?.properties.vertices} pontos`}</p>
      <div className="acoes-area"><button type="button" className="acao-area primaria" onClick={() => {iniciarAdicao(); desenhar();}}>Adicionar área</button><button type="button" className="acao-area" onClick={() => {aoInteragir(); const p = poligonoAtual(); if (p) mapa?.fitBounds(p.getBounds(), {padding: [36, 36], maxZoom: 18});}}>Ver área</button><button type="button" className="acao-area" onClick={() => {aoInteragir(); rascunhoANM.current = null; prepararEdicao(); mudarFase('ajustando'); setErro('');}}>Ajustar</button><button type="button" className="acao-area" onClick={desenhar}>Redesenhar</button><button type="button" className="acao-area" disabled={!minaId} onClick={() => {iniciarAdicao(); void carregarAreaANM();}}>Polígono ANM</button><button type="button" className="acao-area" onClick={remover}>Remover</button></div>
    </> : null}
    {erro ? <p className="erro-area" role="alert">{erro}</p> : null}
  </section>;
}
