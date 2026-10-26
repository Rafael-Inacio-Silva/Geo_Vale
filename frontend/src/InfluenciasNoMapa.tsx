import {useEffect} from 'react';
import L from 'leaflet';
import type {ReferenciasTerritoriais} from './tipos.ts';

/** Sobrepõe os recortes documentais sem interceptar o desenho ou a seleção de áreas. */
export default function InfluenciasNoMapa({mapa, dados, filtros, visivel, somenteReferencia}: {mapa: L.Map | null; dados: ReferenciasTerritoriais | null; filtros: string[]; visivel: boolean; somenteReferencia: boolean}) {
  useEffect(() => {
    if (!mapa || !dados || !visivel) return;
    if (!mapa.getPane('influencias')) mapa.createPane('influencias').style.zIndex = '430';
    const grupo = L.featureGroup().addTo(mapa);
    // A referência OSM fica sombreada mesmo quando todos os filtros de influência estão desmarcados.
    const ordenadas = [...dados.features].sort((a, b) => {
      const ordem = ['aii_agua_solos', 'aid_hidrogeologia', 'aid_agua_solos', 'ada_unificada', 'mina_horizontes'];
      return ordem.indexOf(a.properties.id) - ordem.indexOf(b.properties.id);
    });
    for (const feicao of ordenadas) {
      const p = feicao.properties;
      const referencia = p.tipo === 'referencia';
      if (!referencia && (somenteReferencia || !filtros.includes(p.id))) continue;
      L.geoJSON(feicao, {
        pane: 'influencias', interactive: false,
        attribution: referencia ? 'Referência: &copy; <a href="https://www.openstreetmap.org/way/315221699">OpenStreetMap</a> contributors (ODbL)' : 'Influências aproximadas: <a href="https://sistemas.meioambiente.mg.gov.br/consulta-intervencao/uploads/122024/24642_gvwxhTH__066nrKD6s2u.pdf" target="_blank" rel="noopener noreferrer">FEAM / Vale / Amplo</a>',
        style: {color: p.cor, weight: referencia ? 2 : 3, fillColor: p.cor, fillOpacity: referencia ? .32 : p.id === 'ada_unificada' ? .12 : .035, dashArray: p.id === 'ada_unificada' ? '5 4' : undefined},
      }).addTo(grupo);
    }
    return () => {grupo.remove();};
  }, [mapa, dados, filtros, visivel, somenteReferencia]);
  return null;
}
