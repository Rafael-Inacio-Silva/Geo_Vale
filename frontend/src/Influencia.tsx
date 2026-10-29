import {useEffect, useState} from 'react';
import L from 'leaflet';
import {requisitar} from './api.ts';
import CamadasNaInfluencia from './CamadasNaInfluencia.tsx';
import RelatorioDaMina from './RelatorioDaMina.tsx';
import VideoPosMineracao from './VideoPosMineracao.tsx';
import type {CamadaTerritorial, CamadasAtivas, InfluenciaTerritorial, LegendaTrilha, TerritorioPreparado} from './tipos.ts';

/** Alterna o território no mapa, entra no modo sugestão e oferece o relatório PDF da mina selecionada. */
export default function Influencia({mapa, minaId, temas, expandidas, aoConsultar, informarLegenda, modoSugestao, alternarSugestao, pedidoRelatorio}: {
  mapa: L.Map | null; minaId?: string; temas: CamadaTerritorial[]; expandidas: CamadasAtivas;
  aoConsultar: () => void; informarLegenda: (legenda: LegendaTrilha[]) => void;
  modoSugestao: boolean; alternarSugestao: () => void; pedidoRelatorio: {pesos: number[]; vez: number} | null;
}) {
  const [aberta, setAberta] = useState(false);
  const [contorno, setContorno] = useState<InfluenciaTerritorial | null>(null);
  const [territorio, setTerritorio] = useState<TerritorioPreparado | null>(null);
  const [erro, setErro] = useState('');
  const [tentativa, setTentativa] = useState(0);

  useEffect(() => {
    setAberta(false);
    setContorno(null);
    setTerritorio(null);
    setErro('');
    if (!minaId) return;
    const controle = new AbortController();
    let agendamento: ReturnType<typeof setTimeout> | undefined;
    const url = `/api/minas/${encodeURIComponent(minaId)}`;
    void requisitar<InfluenciaTerritorial>(`${url}/influencia`, controle.signal).then(dados => {
      if (!controle.signal.aborted) setContorno(dados);
    }).catch(falha => {if (!controle.signal.aborted) setErro(falha.message);});
    async function lerTerritorio() {
      try {
        const dados = await requisitar<TerritorioPreparado>(`${url}/territorio`, controle.signal);
        if (controle.signal.aborted) return;
        setTerritorio(dados);
        agendamento = setTimeout(() => {void lerTerritorio();}, dados.completo ? 60000 : 3000);
      } catch {
        if (!controle.signal.aborted) agendamento = setTimeout(() => {void lerTerritorio();}, 15000);
      }
    }
    void lerTerritorio();
    return () => {controle.abort(); clearTimeout(agendamento);};
  }, [minaId, tentativa]);

  useEffect(() => {
    if (!mapa || !contorno || !minaId) return;
    if (!mapa.getPane('influencia')) mapa.createPane('influencia').style.zIndex = '430';
    const grupo = L.featureGroup().addTo(mapa);
    // No modo sugestão o recorte continua como referência, sem as camadas temáticas.
    for (const f of contorno.features.filter(f => aberta || modoSugestao || f.properties.id === 'mina').sort((a, b) => a.properties.id === 'mina' ? 1 : b.properties.id === 'mina' ? -1 : 0)) {
      const mina = f.properties.id === 'mina';
      L.geoJSON(f, {
        pane: 'influencia', interactive: false,
        // Créditos do pacote de cada mina: way OSM da cava e estudo ou faixa declarada do recorte.
        attribution: mina ? `Mina: &copy; <a href="${f.properties.fonte?.url}">OpenStreetMap</a> contributors (ODbL)` : `Influência: <a href="${contorno.fonte.url}" target="_blank" rel="noopener noreferrer">${contorno.fonte.credito}</a>`,
        style: {color: mina ? '#00594f' : '#efa900', weight: 3, fillColor: mina ? '#00594f' : '#ffc329', fillOpacity: mina ? .3 : .025},
      }).addTo(grupo);
    }
    return () => {grupo.remove();};
  }, [mapa, contorno, aberta, modoSugestao, minaId]);

  function alternarInfluencia() {
    if (!mapa || !contorno || !minaId) return;
    aoConsultar();
    setAberta(valor => !valor);
    if (!aberta) {
      mapa.stop();
      mapa.fitBounds(L.geoJSON(contorno).getBounds(), {padding: [30, 60], maxZoom: 16, animate: false});
    }
  }

  return <section className="influencia-territorio" aria-label="Influência da mina">
    <button type="button" className="abrir-influencia" aria-pressed={aberta} disabled={!minaId || !mapa || !contorno || modoSugestao} title={modoSugestao ? 'Volte ao território para usar' : undefined} onClick={alternarInfluencia}>Influência <svg viewBox="0 0 24 24" aria-hidden="true"><path d="m4 7 7-3 9 4-3 11-10 1-3-13Z"/></svg></button>
    {erro ? <p className="erro-territorio" role="alert">{erro} <button className="tentar-novamente" type="button" onClick={() => setTentativa(v => v + 1)}>Recarregar</button></p> : null}
    {aberta && !modoSugestao && mapa && contorno && minaId ? <>
      <CamadasNaInfluencia mapa={mapa} minaId={minaId} contorno={contorno} temas={temas} expandidas={expandidas} informarLegenda={informarLegenda}/>
    </> : null}
    {minaId ? <RelatorioDaMina key={`relatorio-${minaId}`} minaId={minaId} pronto={territorio?.completo ?? false} pedido={pedidoRelatorio}/> : null}
    {minaId ? <button type="button" className="abrir-influencia sugerir-uso" aria-pressed={modoSugestao} disabled={!territorio?.completo || !mapa} onClick={alternarSugestao}>
      Sugerir uso <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/></svg>
    </button> : null}
    {minaId ? <VideoPosMineracao key={`video-${minaId}`} minaId={minaId} pronto={(territorio?.completo ?? false) && !!mapa}/> : null}
  </section>;
}
