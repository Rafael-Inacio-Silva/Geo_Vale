import {useEffect, useRef} from 'react';
import L from 'leaflet';
import type {FeatureCollection, MultiPolygon, Polygon} from 'geojson';
import type {SugestaoUso} from './tipos.ts';

/** Pinta os setores pelo 1º uso, destaca o selecionado e mostra que o mapa está no modo sugestão. */
export default function SugestaoNoMapa({mapa, sugestao, selecionado, selecionar, sair}: {
  mapa: L.Map | null; sugestao: SugestaoUso | null; selecionado: string | null;
  selecionar: (id: string) => void; sair: () => void;
}) {
  const enquadrada = useRef(false);
  const selecionarAtual = useRef(selecionar);
  selecionarAtual.current = selecionar;

  useEffect(() => {
    if (!mapa || !sugestao) return;
    if (!mapa.getPane('sugestao')) mapa.createPane('sugestao').style.zIndex = '440';
    const setores = sugestao.setores;
    const colecao: FeatureCollection<Polygon | MultiPolygon, {id: string}> = {type: 'FeatureCollection', features: setores.map(s => ({type: 'Feature', properties: {id: s.id}, geometry: s.geometria}))};
    const camada = L.geoJSON(colecao, {
      pane: 'sugestao',
      style: f => {
        const ativo = f?.properties.id === selecionado;
        return {color: ativo ? '#00473f' : '#ffffff', weight: ativo ? 3.5 : 1.5,
                fillColor: setores.find(s => s.id === f?.properties.id)?.ranking[0].cor ?? '#536d64', fillOpacity: ativo ? .85 : .7};
      },
      onEachFeature: (f, camadaSetor) => {
        const setor = setores.find(s => s.id === f.properties.id);
        if (!setor) return;
        camadaSetor.bindTooltip(`${setor.id} · ${setor.ranking[0].nome}`, {sticky: true});
        camadaSetor.on('click', () => selecionarAtual.current(setor.id));
      },
    }).addTo(mapa);
    if (!enquadrada.current && setores.length) {
      enquadrada.current = true;
      mapa.stop();
      mapa.fitBounds(camada.getBounds(), {padding: [40, 40], maxZoom: 15, animate: false});
    }
    return () => {camada.remove();};
  }, [mapa, sugestao, selecionado]);

  return <div className="modo-sugestao" role="status">
    <span>Modo sugestão</span>
    <button type="button" onClick={sair}>Voltar ao território</button>
  </div>;
}
