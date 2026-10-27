import {useCallback, useEffect, useState} from 'react';
import L from 'leaflet';
import TrilhasNoMapa from './TrilhasNoMapa.tsx';
import type {CamadaTerritorial, CamadasAtivas, EstadoCamada, InfluenciaTerritorial, LegendaTrilha} from './tipos.ts';

/** Mantém o estilo oficial, mascarando a imagem fora do polígono irregular no próprio mapa. */
function TemaRecortado({mapa, tema, contorno, ativo, recarga, informar}: {
  mapa: L.Map; tema: CamadaTerritorial; contorno: InfluenciaTerritorial; ativo: boolean;
  recarga: number; informar: (id: string, estado: EstadoCamada) => void;
}) {
  useEffect(() => {
    if (!ativo) return;
    const area = contorno.features.find(f => f.properties.id === 'influencia');
    const opcoes: L.WMSOptions = {
      layers: tema.bases.filter(b => b.mapa !== false).map(b => b.camada).join(','),
      format: 'image/png', transparent: true, version: '1.1.1',
      attribution: tema.credito, opacity: tema.opacidade, zIndex: 200 + tema.ordem,
      bounds: L.geoJSON(area).getBounds(), noWrap: true, tileSize: 512, maxZoom: 19,
      updateWhenIdle: true, updateWhenZooming: false, keepBuffer: 0,
    };
    const camada = L.tileLayer.wms(tema.url, opcoes);
    let falhou = false;
    let prazo: ReturnType<typeof setTimeout> | undefined;
    camada.on('loading', () => {
      falhou = false;
      informar(tema.id, 'carregando');
      clearTimeout(prazo);
      prazo = setTimeout(() => {falhou = true; informar(tema.id, 'erro');}, 25000);
    });
    camada.on('tileerror', () => {falhou = true; informar(tema.id, 'erro');});
    camada.on('load', () => {clearTimeout(prazo); informar(tema.id, falhou ? 'erro' : 'pronta');});
    camada.addTo(mapa);
    const recipiente = camada.getContainer();
    recipiente?.classList.add('leaflet-zoom-hide');
    const atualizarMascara = () => {
      if (!recipiente || !area) return;
      const poligonos = area.geometry.type === 'Polygon' ? [area.geometry.coordinates] : area.geometry.coordinates;
      const caminho = poligonos.flatMap(poligono => poligono.map(anel => anel.map(([lon, lat], i) => {
        const ponto = mapa.latLngToLayerPoint([lat, lon]);
        return `${i ? 'L' : 'M'}${ponto.x} ${ponto.y}`;
      }).join(' ') + ' Z')).join(' ');
      recipiente.style.clipPath = `path(evenodd, "${caminho}")`;
    };
    atualizarMascara();
    mapa.on('zoomend viewreset moveend resize', atualizarMascara);
    return () => {clearTimeout(prazo); mapa.off('zoomend viewreset moveend resize', atualizarMascara); camada.remove(); camada.off();};
  }, [mapa, tema, contorno, ativo, recarga, informar]);
  return null;
}

/** Camadas desmarcadas permanecem dentro da influência; marcar amplia o tema no mapa. */
export default function CamadasNaInfluencia({mapa, minaId, contorno, temas, expandidas, informarLegenda}: {
  mapa: L.Map; minaId: string; contorno: InfluenciaTerritorial; temas: CamadaTerritorial[];
  expandidas: CamadasAtivas; informarLegenda: (legenda: LegendaTrilha[]) => void;
}) {
  const [estados, setEstados] = useState<Record<string, EstadoCamada>>({});
  const [recarga, setRecarga] = useState(0);
  const informar = useCallback((id: string, estado: EstadoCamada) => {
    setEstados(atuais => atuais[id] === estado ? atuais : {...atuais, [id]: estado});
  }, []);
  const recortados = temas.filter(t => expandidas[t.id] === undefined);
  const falhas = recortados.filter(t => estados[t.id] === 'erro').map(t => t.nome);
  const falhou = falhas.length > 0;
  const carregando = recortados.some(t => !estados[t.id] || estados[t.id] === 'carregando');
  return <>
    {temas.map(tema => tema.tipo === 'wms'
      ? <TemaRecortado key={tema.id} mapa={mapa} tema={tema} contorno={contorno} ativo={expandidas[tema.id] === undefined} recarga={recarga} informar={informar}/>
      : <TrilhasNoMapa key={tema.id} mapa={mapa} tema={tema} urlRecorte={`/api/minas/${encodeURIComponent(minaId)}/trilhas-influencia`} opacidade={expandidas[tema.id] === undefined ? tema.opacidade : undefined} recarga={recarga} informarEstado={informar} informarLegenda={informarLegenda}/>)}
    {falhou ? <p className="erro-territorio" role="alert">Não carregou: {falhas.join(', ')}. <button type="button" className="tentar-novamente" onClick={() => setRecarga(v => v + 1)}>Recarregar</button></p>
      : carregando ? <p className="nota-territorio" role="status">Carregando camadas…</p> : null}
  </>;
}
