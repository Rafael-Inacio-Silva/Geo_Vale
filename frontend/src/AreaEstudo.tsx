import {useEffect, useRef, useState} from 'react';
import L from 'leaflet';
import 'leaflet-draw';
import 'leaflet-draw/dist/leaflet.draw.css';
import type {AreaConfirmada, AreaManual, AreaReferencia, ReferenciasTerritoriais} from './tipos.ts';
import {requisitar} from './api.ts';
import InfluenciasNoMapa from './InfluenciasNoMapa.tsx';

type Fase = 'vazia' | 'desenhando' | 'ajustando' | 'validando' | 'confirmada' | 'renomeando';
type Modo = 'manual' | 'referencia' | 'influencia';
const ESTILO = {color: '#ffc329', weight: 3, opacity: 1, fillColor: '#ffc329', fillOpacity: .15};

L.drawLocal.draw.handlers.polygon.tooltip = {
  start: 'Clique ou toque para marcar o primeiro ponto.',
  cont: 'Continue marcando o contorno.',
  end: 'Toque no primeiro ponto ou use Fechar contorno.',
};
L.drawLocal.draw.handlers.polyline.error = 'Os lados do contorno não podem se cruzar.';
L.drawLocal.edit.handlers.edit.tooltip = {text: 'Arraste os pontos para ajustar a área.', subtext: 'Confirme quando terminar.'};

/** Mantém várias áreas independentes; confirma, edita e restaura cada recorte sem persistência. */
export default function AreaEstudo({mapa, minaId, aoInteragir}: {aoInteragir: () => void; mapa: L.DrawMap | null; minaId?: string}) {
  const [modo, setModo] = useState<Modo>('manual');
  const modoAtual = useRef<Modo>('manual');
  const [contexto, setContexto] = useState<'referencia' | 'influencia' | null>(null);
  const verticesDesenho = useRef<L.LatLng[]>([]);
  const interrompendoDesenho = useRef(false);
  const cameraManual = useRef<{centro: L.LatLng; zoom: number} | null>(null);
  const [fase, setFase] = useState<Fase>('vazia');
  const faseAtual = useRef<Fase>('vazia');
  const [pontos, setPontos] = useState(0);
  const [erro, setErro] = useState('');
  const [nomes, setNomes] = useState<Record<number, string>>({});
  const nomesAtuais = useRef(nomes);
  nomesAtuais.current = nomes;
  const [nomeEditado, setNomeEditado] = useState('');
  const [erroNome, setErroNome] = useState('');
  const botaoRenomear = useRef<HTMLButtonElement>(null);
  const devolverFocoNome = useRef(false);
  const [lista, setLista] = useState<{id: number; dados: AreaConfirmada}[]>([]);
  const areas = useRef(new Map<number, AreaConfirmada>());
  const ativa = useRef<number | null>(null);
  const anterior = useRef<number | null>(null);
  const sequencia = useRef(0);
  const outras = useRef<L.FeatureGroup | null>(null);
  const [area, setArea] = useState<AreaConfirmada | null>(null);
  const confirmada = useRef<AreaConfirmada | null>(null);
  const [referencias, setReferencias] = useState<ReferenciasTerritoriais | null>(null);
  const [erroReferencias, setErroReferencias] = useState('');
  const [carregandoReferencias, setCarregandoReferencias] = useState(false);
  const [tentativaReferencias, setTentativaReferencias] = useState(0);
  const [filtros, setFiltros] = useState<string[]>([]);
  const pedido = useRef<AbortController | null>(null);
  const recursos = useRef<{grupo: L.FeatureGroup; desenho: L.Draw.Polygon | null; editor: L.EditToolbar.Edit | null} | null>(null);

  function mudarFase(valor: Fase) {faseAtual.current = valor; setFase(valor);}

  function nomeArea(id: number | null) {
    return id === null ? '' : nomesAtuais.current[id] ?? `Área ${id}`;
  }

  function iniciarRenomeacao() {
    setNomeEditado(nomeArea(ativa.current));
    setErroNome('');
    mudarFase('renomeando');
  }

  function cancelarRenomeacao() {
    devolverFocoNome.current = true;
    setErroNome('');
    mudarFase('confirmada');
  }

  function renomear() {
    const id = ativa.current;
    if (id === null || !areas.current.has(id)) return;
    const nome = nomeEditado.trim().replace(/\s+/gu, ' ');
    if (!nome || nome.length > 80) {setErroNome('Informe um nome de até 80 caracteres.'); return;}
    const proximos = {...nomesAtuais.current, [id]: nome};
    nomesAtuais.current = proximos;
    setNomes(proximos);
    devolverFocoNome.current = true;
    setErroNome('');
    if (confirmada.current) exibirArea(confirmada.current, true);
    atualizarOutras();
    mudarFase('confirmada');
  }

  useEffect(() => {
    if (fase === 'confirmada' && devolverFocoNome.current) {
      devolverFocoNome.current = false;
      botaoRenomear.current?.focus();
    }
  }, [fase]);

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
      if (dados.properties.origem === 'referencia_osm') camada.options.attribution = 'Referência: &copy; <a href="https://www.openstreetmap.org/way/315221699">OpenStreetMap</a> contributors (ODbL)';
      if (confirmacao && ativa.current !== null) {
        const nome = document.createElement('span');
        nome.textContent = nomeArea(ativa.current);
        camada.bindTooltip(nome);
      }
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
        if (dados.properties.origem === 'referencia_osm') camada.options.attribution = 'Referência: &copy; <a href="https://www.openstreetmap.org/way/315221699">OpenStreetMap</a> contributors (ODbL)';
        const nome = document.createElement('span');
        nome.textContent = nomeArea(id);
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
    modoAtual.current = 'manual';
    setModo('manual');
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
    verticesDesenho.current = [];
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
      const poligono = criado.layer as L.Polygon;
      poligono.options.pane = 'area-estudo';
      grupo.addLayer(poligono);
      mudarFase('ajustando');
      const anel = poligono.toGeoJSON().geometry.coordinates[0];
      setPontos(anel.length - 1);
      estado.editor = new L.EditToolbar.Edit(mapa, {featureGroup: grupo, poly: {allowIntersection: false}, selectedPathOptions: {...ESTILO, dashArray: '7 5'}});
      estado.editor.enable();
    };
    const aoMarcarPonto = (evento: L.LeafletEvent) => {
      const marcadores = (evento as L.LeafletEvent & {layers: L.LayerGroup}).layers.getLayers() as L.Marker[];
      verticesDesenho.current = marcadores.map(marcador => marcador.getLatLng());
      setPontos(marcadores.length);
    };
    const aoEditarPonto = () => {
      const poligono = grupo.getLayers()[0] as L.Polygon | undefined;
      if (poligono) setPontos(poligono.toGeoJSON().geometry.coordinates[0].length - 1);
      setErro('');
    };
    const aoPararDesenho = () => {
      if (!encerrado && !interrompendoDesenho.current && modoAtual.current === 'manual' && faseAtual.current === 'desenhando') {
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

  useEffect(() => {
    setReferencias(null);
    setContexto(null);
    setFiltros([]);
    setErroReferencias('');
    if (!minaId) {setCarregandoReferencias(false); if (modoAtual.current !== 'manual') ativarModo('manual', false, false); return;}
    const controle = new AbortController();
    setCarregandoReferencias(true);
    void requisitar<ReferenciasTerritoriais>(`/api/minas/${encodeURIComponent(minaId)}/referencias`, controle.signal).then(dados => {
      if (controle.signal.aborted) return;
      setReferencias(dados);
      setFiltros(dados.features.filter(f => f.properties.tipo === 'influencia').map(f => f.properties.id));
    }).catch(falha => {
      if (!controle.signal.aborted) setErroReferencias(falha instanceof Error ? falha.message : 'Referências indisponíveis.');
    }).finally(() => {if (!controle.signal.aborted) setCarregandoReferencias(false);});
    return () => {controle.abort();};
  }, [minaId, tentativaReferencias]);

  /** Alterna a consulta sem descartar o desenho e retoma a câmera de trabalho. */
  function ativarModo(destino: Modo, iniciarSeVazio = true, restaurarCamera = true) {
    if (!mapa || (destino !== 'manual' && (!minaId || !referencias))) return;
    mapa.stop();
    const anteriorModo = modoAtual.current;
    modoAtual.current = destino;
    setModo(destino);
    aoInteragir();
    const estado = recursos.current;
    if (destino !== 'manual') {
      if (anteriorModo === 'manual' && estado) {
        if (faseAtual.current !== 'vazia') cameraManual.current = {centro: mapa.getCenter(), zoom: mapa.getZoom()};
        estado.editor?.disable();
        if (faseAtual.current === 'desenhando') {
          const salvos = [...verticesDesenho.current];
          estado.desenho?.disable();
          estado.desenho = null;
          estado.grupo.clearLayers();
          if (salvos.length > 1) L.polyline(salvos, {...ESTILO, pane: 'area-estudo', dashArray: '6 5', interactive: false}).addTo(estado.grupo);
          else if (salvos.length) L.circleMarker(salvos[0], {pane: 'area-estudo', color: ESTILO.color, radius: 4, interactive: false}).addTo(estado.grupo);
        }
      }
      setContexto(destino);
      const exibidas = destino === 'referencia' ? referencias!.features.filter(f => f.properties.tipo === 'referencia') : referencias!.features;
      mapa.fitBounds(L.geoJSON(exibidas).getBounds(), {padding: [36, 64], maxZoom: 18, animate: false});
      return;
    }
    if (anteriorModo !== 'manual') {
      if (restaurarCamera && cameraManual.current && faseAtual.current !== 'vazia') mapa.setView(cameraManual.current.centro, cameraManual.current.zoom, {animate: false});
      if (faseAtual.current === 'desenhando') {
        const salvos = [...verticesDesenho.current];
        desenhar();
        for (const ponto of salvos) recursos.current?.desenho?.addVertex(ponto);
      } else if (faseAtual.current === 'ajustando') prepararEdicao();
    }
    if (faseAtual.current === 'vazia' && iniciarSeVazio) desenhar();
  }

  function desenhar() {
    const estado = recursos.current;
    if (!mapa || !estado) return;
    aoInteragir();
    pedido.current?.abort();
    interrompendoDesenho.current = true;
    estado.desenho?.disable();
    interrompendoDesenho.current = false;
    estado.editor?.disable();
    estado.grupo.clearLayers();
    setErro('');
    setPontos(0);
    verticesDesenho.current = [];
    mudarFase('desenhando');
    estado.desenho = new L.Draw.Polygon(mapa, {
      allowIntersection: false, showArea: false, showLength: false, maxPoints: 500,
      shapeOptions: {...ESTILO, pane: 'area-estudo'},
      drawError: {color: '#a73720', message: 'Os lados do contorno não podem se cruzar.'},
    });
    estado.desenho.enable();
  }

  /** Adiciona a referência explicitamente ou reutiliza a entrada intacta existente. */
  function usarReferencia() {
    if (!mapa || !minaId || !referencias || (fase !== 'vazia' && fase !== 'confirmada')) return;
    const dados = referencias.features.find(f => f.properties.id === 'mina_horizontes') as AreaReferencia | undefined;
    if (!dados) return;
    const existente = [...areas.current].find(([, valor]) => valor.properties.origem === 'referencia_osm');
    if (existente) {selecionarArea(existente[0]); return;}
    ativarModo('manual', false);
    iniciarAdicao();
    guardarArea(dados);
    const poligono = poligonoAtual();
    if (poligono) mapa.fitBounds(poligono.getBounds(), {padding: [36, 64], maxZoom: 18});
  }

  async function confirmar() {
    const poligono = poligonoAtual();
    if (!poligono) return;
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
      if (modoAtual.current === 'manual') prepararEdicao();
      mudarFase('ajustando');
    }
  }

  function remover() {
    if (ativa.current !== null) {
      areas.current.delete(ativa.current);
      const proximos = {...nomesAtuais.current};
      delete proximos[ativa.current];
      nomesAtuais.current = proximos;
      setNomes(proximos);
    }
    const restante = [...areas.current.keys()].at(-1);
    setLista([...areas.current].map(([id, dados]) => ({id, dados})));
    if (restante !== undefined) {selecionarArea(restante); return;}
    ativa.current = null;
    anterior.current = null;
    confirmada.current = null;
    setArea(null);
    restaurarConfirmada();
  }

  return <section className={`area-estudo fase-${fase}`} aria-label="Área de estudo" onKeyDown={evento => {if (evento.key === 'Escape' && modoAtual.current === 'manual' && faseAtual.current === 'desenhando') {evento.stopPropagation(); restaurarConfirmada();}}}>
    <InfluenciasNoMapa mapa={mapa} dados={referencias} filtros={filtros} visivel={!!contexto && !!minaId} somenteReferencia={contexto === 'referencia'}/>
    <div className="modos-area" role="group" aria-label="Modo de trabalho">
      <button type="button" className="acao-area" disabled={!mapa} aria-pressed={modo === 'manual'} onClick={() => ativarModo('manual')}>Manual</button>
      <button type="button" className="acao-area" disabled={!mapa || !minaId || !referencias} title={!minaId ? 'Selecione uma mina.' : 'Ver o contorno de mineração do OpenStreetMap'} aria-pressed={modo === 'referencia'} onClick={() => ativarModo('referencia')}>Referência</button>
      <button type="button" className="acao-area" disabled={!mapa || !minaId || !referencias} title={!minaId ? 'Selecione uma mina.' : 'Ver os recortes de influência do estudo'} aria-pressed={modo === 'influencia'} onClick={() => ativarModo('influencia')}>Influência</button>
    </div>
    {carregandoReferencias ? <p className="nota-area" role="status">Carregando referências…</p> : null}
    {erroReferencias ? <p className="erro-area" role="alert">{erroReferencias} <button type="button" className="tentar-novamente" onClick={() => setTentativaReferencias(v => v + 1)}>Recarregar referências</button></p> : null}
    {modo === 'referencia' ? <div className="painel-referencia">
      <p className="estado-area">Referência da mina</p>
      <p className="nota-area">Contorno de mineração do OpenStreetMap. <a href="https://www.openstreetmap.org/way/315221699" target="_blank" rel="noopener noreferrer">Ver fonte</a></p>
      <button type="button" className="acao-area primaria" disabled={fase !== 'vazia' && fase !== 'confirmada'} onClick={usarReferencia}>{lista.some(item => item.dados.properties.origem === 'referencia_osm') ? 'Selecionar esta área' : 'Usar como área'}</button>
    </div> : null}
    {modo === 'influencia' && referencias && minaId ? <fieldset className="filtros-influencia">
      <legend>Recortes do estudo</legend>
      {referencias.features.filter(f => f.properties.tipo === 'influencia').map(f => <label className="seletor-tema" key={f.properties.id}>
        <input type="checkbox" checked={filtros.includes(f.properties.id)} onChange={evento => setFiltros(atuais => evento.target.checked ? [...atuais, f.properties.id] : atuais.filter(id => id !== f.properties.id))}/>
        <span className="nome-tema">{f.properties.nome}</span><i className="linha-influencia" style={{borderColor: f.properties.cor}} aria-hidden="true"/>
      </label>)}
      <p className="mina-sombreada"><i aria-hidden="true"/> Mina sombreada · OpenStreetMap</p>
      <details className="fonte-referencias"><summary>Fonte e significado</summary><p>ADA: área diretamente afetada. AID: influência direta. AII: influência indireta.</p><p>Meio físico do projeto Tamanduá e Horizontes. Contornos aproximados, sem limite de fechamento.</p><a href={referencias.fonte.url} target="_blank" rel="noopener noreferrer">Parecer FEAM · Fig. 2.3 · p. 18</a></details>
    </fieldset> : null}
    {modo !== 'manual' && fase !== 'vazia' && fase !== 'confirmada' ? <p className="nota-area pausa-area" role="status">{fase === 'validando' ? 'Confirmando sua área…' : 'Seu trabalho está guardado. Volte a Manual para continuar.'}</p> : null}
    <div hidden={modo !== 'manual'}>
    {contexto ? <p className="contexto-area">Contexto: {contexto === 'referencia' ? 'referência' : 'influência'} <button type="button" className="tentar-novamente" onClick={() => setContexto(null)}>Ocultar</button></p> : null}
    {lista.length > 0 && (fase === 'confirmada' || fase === 'renomeando') ? <div className="lista-areas" role="group" aria-label="Áreas demarcadas"><span>Áreas ({lista.length})</span>{lista.map(item => <button type="button" className="acao-area" key={item.id} aria-label={`Selecionar ${nomeArea(item.id)} (área ${item.id})`} disabled={fase === 'renomeando'} aria-pressed={ativa.current === item.id} onClick={() => selecionarArea(item.id)}>{nomeArea(item.id)}</button>)}</div> : null}
    {fase === 'vazia' || fase === 'confirmada' ? <button type="button" className="acao-area primaria iniciar-area" disabled={!mapa} onClick={() => {if (fase === 'confirmada') iniciarAdicao(); desenhar();}}>{lista.length ? 'Adicionar área' : 'Desenhar área'}</button> : null}
    {fase === 'desenhando' ? <>
      <p className="estado-area" role="status">Marque os pontos no mapa · {pontos} pontos</p>
      <div className="acoes-area"><button type="button" className="acao-area primaria" disabled={pontos < 3} onClick={() => recursos.current?.desenho?.completeShape()}>Fechar contorno</button><button type="button" className="acao-area" disabled={!pontos} onClick={() => {if (pontos === 1) desenhar(); else recursos.current?.desenho?.deleteLastVertex();}}>Desfazer ponto</button><button type="button" className="acao-area" onClick={restaurarConfirmada}>Cancelar</button></div>
    </> : null}
    {fase === 'ajustando' || fase === 'validando' ? <>
      <p className="estado-area" role="status">{fase === 'validando' ? 'Confirmando área…' : 'Ajuste os pontos e confirme a área.'}</p>
      <div className="acoes-area"><button type="button" className="acao-area primaria" disabled={fase === 'validando'} onClick={() => {void confirmar();}}>Confirmar área</button><button type="button" className="acao-area" onClick={restaurarConfirmada}>Cancelar</button></div>
    </> : null}
    {fase === 'confirmada' || fase === 'renomeando' ? <>
      <p className="estado-area" role="status">{area?.properties.origem === 'referencia_osm' ? `${nomeArea(ativa.current)} · referência da mina` : `${nomeArea(ativa.current)} · ${area?.properties.vertices} pontos`}</p>
      {fase === 'renomeando' ? <form className="renomear-area" onSubmit={evento => {evento.preventDefault(); renomear();}} onKeyDown={evento => {if (evento.key === 'Escape') {evento.stopPropagation(); cancelarRenomeacao();}}}>
        <label htmlFor="nome-area">Nome da área</label>
        <input id="nome-area" value={nomeEditado} onChange={evento => {setNomeEditado(evento.target.value); setErroNome('');}} maxLength={80} required autoFocus onFocus={evento => evento.currentTarget.select()} autoComplete="off" aria-invalid={!!erroNome} aria-describedby={erroNome ? 'erro-nome-area' : undefined}/>
        {erroNome ? <p id="erro-nome-area" className="erro-area" role="alert">{erroNome}</p> : null}
        <div className="acoes-area"><button type="submit" className="acao-area primaria">Salvar nome</button><button type="button" className="acao-area" onClick={cancelarRenomeacao}>Cancelar</button></div>
      </form> : <div className="acoes-area"><button type="button" className="acao-area" onClick={() => {aoInteragir(); const p = poligonoAtual(); if (p) mapa?.fitBounds(p.getBounds(), {padding: [36, 36], maxZoom: 18});}}>Ver área</button><button type="button" className="acao-area" onClick={() => {aoInteragir(); prepararEdicao(); mudarFase('ajustando'); setErro('');}}>Ajustar</button><button type="button" className="acao-area" onClick={desenhar}>Redesenhar</button><button type="button" className="acao-area" ref={botaoRenomear} onClick={iniciarRenomeacao}>Renomear</button><button type="button" className="acao-area" onClick={remover}>Remover</button></div>}
    </> : null}
    {erro ? <p className="erro-area" role="alert">{erro}</p> : null}
    </div>
  </section>;
}
