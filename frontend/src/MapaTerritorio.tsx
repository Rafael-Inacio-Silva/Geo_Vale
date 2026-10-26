import {useCallback, useEffect, useRef, useState} from 'react';
import L from 'leaflet';
import type {CamadasAtivas, ConfiguracaoMapa, EstadoCamada, LegendaTrilha, LimiteMG, Mina} from './tipos.ts';
import 'leaflet/dist/leaflet.css';
import MunicipioNoMapa from './MunicipioNoMapa.tsx';
import TrilhasNoMapa from './TrilhasNoMapa.tsx';

interface Propriedades {
  configuracao: ConfiguracaoMapa;
  limite: LimiteMG | null;
  selecionada: Mina | null;
  selecionar: (mina: Mina, origem: 'marcador') => void;
  enquadrarMunicipio: boolean;
  voltar: () => void;
  informarMapa: (mapa: L.DrawMap | null) => void;
  prioridadeArea: {current: boolean};
  ativas: CamadasAtivas;
  recargas: Record<string, number>;
  informarEstado: (id: string, estado: EstadoCamada) => void;
  informarLegendaTrilhas: (entradas: LegendaTrilha[]) => void;
}

/** Exibe fundo mundial, temas de fontes distintas, contorno estadual e referência da mina. */
export default function MapaTerritorio({configuracao, limite, selecionada, selecionar, voltar, ativas, recargas, informarEstado, informarLegendaTrilhas, informarMapa, prioridadeArea, enquadrarMunicipio}: Propriedades) {
  const podeEnquadrarMunicipio = useCallback(() => enquadrarMunicipio && !prioridadeArea.current, [prioridadeArea, enquadrarMunicipio]);
  const elemento = useRef<HTMLDivElement>(null);
  const mapa = useRef<L.Map | null>(null);
  const [instanciaAtual, setInstanciaAtual] = useState<L.DrawMap | null>(null);
  const camadaFundo = useRef<L.TileLayer | null>(null);
  const sobreposicoes = useRef(new Map<string, {camada: L.TileLayer.WMS; recarga: number; limpar: () => void}>());
  const informarEstadoAtual = useRef(informarEstado);
  informarEstadoAtual.current = informarEstado;
  const contorno = useRef<L.GeoJSON | null>(null);
  const enquadrouEstado = useRef(false);
  const marcadores = useRef(new Map<string, L.CircleMarker>());
  const selecionarAtual = useRef(selecionar);
  const selecionadaAtual = useRef(selecionada);
  const [fundo, setFundo] = useState(configuracao.fundos[0].id);
  const [falhaFundo, setFalhaFundo] = useState(false);
  selecionarAtual.current = selecionar;
  selecionadaAtual.current = selecionada;

  useEffect(() => {
    if (!elemento.current) return;
    const instancia = L.map(elemento.current, {zoomControl: false, minZoom: 2, maxZoom: 19, worldCopyJump: true}).setView(configuracao.estado.centro, configuracao.estado.zoom);
    mapa.current = instancia;
    setInstanciaAtual(instancia);
    informarMapa(instancia);
    L.control.zoom({position: 'bottomright', zoomInTitle: 'Aproximar', zoomOutTitle: 'Afastar'}).addTo(instancia);
    L.control.scale({imperial: false, position: 'bottomleft'}).addTo(instancia);
    for (const mina of configuracao.minas) {
      const ponto = L.circleMarker([mina.latitude, mina.longitude], {radius: 9, color: '#fff', weight: 3, fillColor: '#007f73', fillOpacity: 1, bubblingMouseEvents: false}).addTo(instancia);
      const rotulo = document.createElement('span');
      rotulo.textContent = mina.nome;
      ponto.bindTooltip(rotulo, {direction: 'top', offset: [0, -9]});
      const aproximar = () => selecionarAtual.current(mina, 'marcador');
      ponto.on('click', aproximar);
      const simbolo = ponto.getElement();
      if (simbolo) {
        simbolo.setAttribute('role', 'button');
        simbolo.setAttribute('aria-label', `Aproximar ${mina.nome}`);
        simbolo.setAttribute('tabindex', '0');
        simbolo.addEventListener('keydown', evento => {
          if (!(evento instanceof KeyboardEvent)) return;
          if (evento.key === 'Enter' || evento.key === ' ') {evento.preventDefault(); aproximar();}
        });
      }
      marcadores.current.set(mina.id, ponto);
    }
    const observador = new ResizeObserver(() => instancia.invalidateSize({animate: false}));
    observador.observe(elemento.current);
    return () => {
      observador.disconnect();
      for (const item of sobreposicoes.current.values()) item.limpar();
      sobreposicoes.current.clear();
      informarMapa(null);
      instancia.remove();
      marcadores.current.clear();
      mapa.current = null;
      contorno.current = null;
      enquadrouEstado.current = false;
    };
  }, [configuracao, informarMapa]);

  useEffect(() => {
    const instancia = mapa.current;
    if (!instancia) return;
    const provedor = configuracao.fundos.find(item => item.id === fundo);
    if (!provedor) return;
    setFalhaFundo(false);
    const camada = L.tileLayer(provedor.url, {attribution: provedor.credito, maxZoom: provedor.zoom_maximo, keepBuffer: 1});
    camada.on('tileerror', () => setFalhaFundo(true));
    camada.addTo(instancia);
    camadaFundo.current = camada;
    return () => {camada.off('tileerror'); camada.remove(); camadaFundo.current = null;};
  }, [configuracao, fundo]);

  useEffect(() => {
    const instancia = mapa.current;
    if (!instancia) return;

    for (const [id, item] of sobreposicoes.current) {
      if (ativas[id] === undefined) {
        item.limpar();
        sobreposicoes.current.delete(id);
      }
    }
    for (const tema of configuracao.camadas) {
      if (tema.tipo !== 'wms') continue;
      const cobertura = L.latLngBounds(tema.cobertura);
      const opacidade = ativas[tema.id];
      if (opacidade === undefined) continue;
      const existente = sobreposicoes.current.get(tema.id);
      if (existente) {
        existente.camada.setOpacity(opacidade);
        if (existente.recarga !== (recargas[tema.id] ?? 0)) {
          existente.recarga = recargas[tema.id] ?? 0;
          existente.camada.redraw();
        }
        continue;
      }
      const camada = L.tileLayer.wms(tema.url, {
        layers: tema.bases.map(base => base.camada).join(','),
        format: 'image/png', transparent: true, version: '1.1.1',
        attribution: tema.credito, opacity: opacidade, zIndex: 200 + tema.ordem,
        tileSize: 512, maxZoom: 19, bounds: cobertura, noWrap: true,
        updateWhenIdle: true, updateWhenZooming: false, keepBuffer: 0,
      });
      let falhou = false;
      let carregando = false;
      let prazo: ReturnType<typeof setTimeout> | undefined;
      const informar = (estado: EstadoCamada) => informarEstadoAtual.current(tema.id, estado);
      const atualizarExtensao = () => {
        if (!cobertura.intersects(instancia.getBounds())) informar('fora');
        else informar(falhou ? 'erro' : carregando ? 'carregando' : 'pronta');
      };
      camada.on('loading', () => {
        falhou = false;
        carregando = true;
        informar('carregando');
        clearTimeout(prazo);
        prazo = setTimeout(() => {falhou = true; informar('erro');}, 25000);
      });
      camada.on('tileerror', () => {falhou = true; informar('erro');});
      camada.on('load', () => {
        clearTimeout(prazo);
        carregando = false;
        atualizarExtensao();
      });
      instancia.on('moveend', atualizarExtensao);
      sobreposicoes.current.set(tema.id, {camada, recarga: recargas[tema.id] ?? 0, limpar: () => {
        clearTimeout(prazo);
        instancia.off('moveend', atualizarExtensao);
        camada.off('loading tileerror load');
        camada.remove();
        camada.off();
      }});
      camada.addTo(instancia);
      atualizarExtensao();
    }
  }, [ativas, recargas, configuracao]);

  useEffect(() => {
    const instancia = mapa.current;
    if (!instancia || !limite) return;
    const camada = L.geoJSON(limite, {
      interactive: false,
      attribution: 'Limite: FJP / <a href="https://geoportal.meioambiente.mg.gov.br/home">IDE-Sisema</a>',
      style: {color: '#007f73', weight: 3, fillColor: '#007f73', fillOpacity: 0.035},
    }).addTo(instancia);
    contorno.current = camada;
    if (!enquadrouEstado.current && !selecionadaAtual.current) {
      instancia.fitBounds(camada.getBounds(), {padding: [16, 16], animate: false});
      enquadrouEstado.current = true;
    }
    return () => {camada.remove(); contorno.current = null;};
  }, [limite, configuracao]);

  useEffect(() => {
    const instancia = mapa.current;
    if (!instancia) return;
    for (const [id, ponto] of marcadores.current) {
      const ativo = selecionada?.id === id;
      ponto.setStyle({fillColor: ativo ? '#ffc329' : '#007f73', color: ativo ? '#00473f' : '#fff'});
      ponto.setRadius(ativo ? 12 : 9);
      if (ativo) ponto.openTooltip(); else ponto.closeTooltip();
    }
    prioridadeArea.current = false;
    if (selecionada) instancia.setView([selecionada.latitude, selecionada.longitude], 14, {animate: false});
    else if (contorno.current) instancia.fitBounds(contorno.current.getBounds(), {padding: [16, 16], animate: false});
    else instancia.setView(configuracao.estado.centro, configuracao.estado.zoom, {animate: false});
  }, [selecionada, configuracao, prioridadeArea]);

  /** Retorna ao enquadramento estadual sem restringir a navegação mundial. */
  function verEstado() {
    voltar();
    const instancia = mapa.current;
    if (!instancia) return;
    if (contorno.current) instancia.fitBounds(contorno.current.getBounds(), {padding: [16, 16], animate: false});
    else instancia.setView(configuracao.estado.centro, configuracao.estado.zoom, {animate: false});
  }

  return <>
    <div ref={elemento} className="mapa" role="region" aria-label="Mapa de Minas Gerais com navegação mundial"/>
    <div className="ferramentas-mapa">
      <div className="fundos" role="group" aria-label="Mapa de fundo">{configuracao.fundos.map(item => <button type="button" key={item.id} aria-pressed={fundo === item.id} onClick={() => setFundo(item.id)}>{item.nome}</button>)}</div>
      <button type="button" className="ver-estado" onClick={verEstado}>Ver Minas Gerais</button>
    </div>
    <TrilhasNoMapa mapa={instanciaAtual} tema={configuracao.camadas.find(tema => tema.id === 'trilhas')!} opacidade={ativas.trilhas} recarga={recargas.trilhas ?? 0} informarEstado={informarEstado} informarLegenda={informarLegendaTrilhas}/>
    <MunicipioNoMapa mapa={instanciaAtual} mina={selecionada} podeEnquadrar={podeEnquadrarMunicipio}/>
    {falhaFundo ? <div className="falha-fundo" role="status"><span>Não foi possível carregar parte do mapa de fundo.</span><button type="button" onClick={() => {setFalhaFundo(false); camadaFundo.current?.redraw();}}>Recarregar</button></div> : null}
    <div className="legenda-mapa"><span><i className="linha-legenda"/> Minas Gerais</span>{selecionada ? <span><i className="municipio-legenda"/> {selecionada.municipio}</span> : null}<span><i className="ponto-legenda"/> Mina</span></div>
  </>;
}
