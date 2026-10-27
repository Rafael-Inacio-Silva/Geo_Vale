import {useEffect, useRef} from 'react';
import L from 'leaflet';
import type {CamadaTerritorial, EstadoCamada, LegendaTrilha, TrilhasGeoJSON} from './tipos.ts';

interface Propriedades {
  mapa: L.Map | null;
  urlRecorte?: string;
  tema: CamadaTerritorial;
  opacidade: number | undefined;
  recarga: number;
  informarEstado: (id: string, estado: EstadoCamada) => void;
  informarLegenda: (entradas: LegendaTrilha[]) => void;
}

/** Integra traçados municipais por GeoJSON, mantendo os demais temas independentes. */
export default function TrilhasNoMapa({mapa, tema, opacidade, recarga, informarEstado, informarLegenda, urlRecorte}: Propriedades) {
  const camada = useRef<L.GeoJSON | null>(null);
  const legendaAtual = useRef(informarLegenda);
  legendaAtual.current = informarLegenda;
  const informarAtual = useRef(informarEstado);
  informarAtual.current = informarEstado;
  const intensidade = useRef(opacidade ?? 1);
  intensidade.current = opacidade ?? 1;
  const ativa = opacidade !== undefined;

  useEffect(() => {
    if (!mapa || !ativa) return;
    if (!mapa.getPane('trilhas')) mapa.createPane('trilhas').style.zIndex = '390';
    const linhas = L.geoJSON(undefined, {
      pane: 'trilhas', attribution: tema.credito,
      style: feicao => ({color: feicao?.properties.cor, weight: feicao?.properties.largura, opacity: intensidade.current * (feicao?.properties.opacidade ?? 1)}),
      onEachFeature: (feicao, linha) => {
        const rotulo = document.createElement('span');
        rotulo.textContent = feicao.properties?.nome || 'Trilha cadastrada';
        linha.bindTooltip(rotulo, {sticky: true});
      },
    }).addTo(mapa);
    camada.current = linhas;
    let abortar: AbortController | null = null;
    let agendado: ReturnType<typeof setTimeout> | undefined;
    let encerrado = false;
    const informar = (estado: EstadoCamada) => informarAtual.current(tema.id, estado);
    const carregar = async () => {
      abortar?.abort();
      const controle = new AbortController();
      abortar = controle;
      linhas.clearLayers();
      legendaAtual.current([]);
      const visivel = mapa.getBounds();
      if (!urlRecorte && !L.latLngBounds(tema.cobertura).intersects(visivel)) {informar('fora'); return;}
      informar('carregando');
      const bbox = [Math.max(-180, visivel.getWest()), Math.max(-85, visivel.getSouth()), Math.min(180, visivel.getEast()), Math.min(85, visivel.getNorth())].map(v => v.toFixed(6)).join(',');
      try {
        const resposta = await fetch(urlRecorte ?? `${tema.url}?${new URLSearchParams({bbox})}`, {signal: AbortSignal.any([controle.signal, AbortSignal.timeout(20000)])});
        if (!resposta.ok) throw new Error();
        const dados = await resposta.json() as TrilhasGeoJSON;
        if (controle.signal.aborted || encerrado) return;
        linhas.addData(dados);
        legendaAtual.current(dados.legenda);
        informar(dados.fora_cobertura ? 'fora' : dados.features.length ? 'pronta' : 'vazia');
      } catch {
        if (!controle.signal.aborted && !encerrado) informar('erro');
      }
    };
    const aoMover = () => {
      abortar?.abort();
      clearTimeout(agendado);
      agendado = setTimeout(() => {void carregar();}, 250);
    };
    if (!urlRecorte) mapa.on('moveend', aoMover);
    void carregar();
    return () => {
      encerrado = true;
      abortar?.abort();
      clearTimeout(agendado);
      mapa.off('moveend', aoMover);
      linhas.remove();
      camada.current = null;
    };
  }, [mapa, tema, ativa, recarga, urlRecorte]);

  useEffect(() => {
    camada.current?.setStyle(feicao => ({opacity: (opacidade ?? 1) * (feicao?.properties.opacidade ?? 1)}));
  }, [opacidade]);
  return null;
}
