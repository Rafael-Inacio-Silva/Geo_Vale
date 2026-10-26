import {useEffect, useRef, useState} from 'react';
import L from 'leaflet';
import {requisitar} from './api.ts';
import type {LimiteMunicipal, Mina} from './tipos.ts';

/** Exibe só o município da seleção corrente; consultas antigas nunca recolocam o contorno. */
export default function MunicipioNoMapa({mapa, mina, podeEnquadrar}: {mapa: L.Map | null; mina: Mina | null; podeEnquadrar: () => boolean}) {
  const [recarga, setRecarga] = useState(0);
  const [estado, setEstado] = useState<{id: string; fase: 'carregando' | 'pronto' | 'erro'} | null>(null);
  const permissaoAtual = useRef(podeEnquadrar);
  permissaoAtual.current = podeEnquadrar;
  const id = mina?.id;
  const latitude = mina?.latitude;
  const longitude = mina?.longitude;
  useEffect(() => {
    if (!mapa || !id || latitude === undefined || longitude === undefined) return;
    const controle = new AbortController();
    let camada: L.GeoJSON | null = null;
    if (!mapa.getPane('municipio')) {
      const pane = mapa.createPane('municipio');
      pane.style.zIndex = '420';
      pane.style.pointerEvents = 'none';
    }
    setEstado({id, fase: 'carregando'});
    void requisitar<LimiteMunicipal>(`/api/minas/${encodeURIComponent(id)}/limite-municipal`, controle.signal).then(dados => {
      if (controle.signal.aborted) return;
      camada = L.geoJSON(dados, {
        pane: 'municipio', interactive: false,
        attribution: 'Município: <a href="https://servicodados.ibge.gov.br/api/docs/malhas?versao=3">IBGE</a>',
        style: {color: '#276c99', weight: 3, dashArray: '8 5', fillOpacity: 0},
      }).addTo(mapa);
      // A chegada do município não desfaz desenho, consulta de referência ou navegação do engenheiro.
      const centro = mapa.getCenter();
      if (permissaoAtual.current() && mapa.getZoom() === 14 && Math.abs(centro.lat - latitude) < .0001 && Math.abs(centro.lng - longitude) < .0001) {
        mapa.fitBounds(camada.getBounds().extend([latitude, longitude]), {paddingTopLeft: [32, 70], paddingBottomRight: [32, 70], animate: false});
      }
      setEstado({id, fase: 'pronto'});
    }).catch(() => {if (!controle.signal.aborted) setEstado({id, fase: 'erro'});});
    return () => {controle.abort(); camada?.remove();};
  }, [mapa, id, latitude, longitude, recarga]);
  if (!mina || estado?.id !== mina.id || estado.fase === 'pronto') return null;
  return <div className="estado-municipio" role="status">
    <span>{estado.fase === 'carregando' ? `Carregando contorno de ${mina.municipio}…` : `Contorno de ${mina.municipio} indisponível.`}</span>
    {estado.fase === 'erro' ? <button type="button" onClick={() => setRecarga(valor => valor + 1)}>Recarregar contorno</button> : null}
  </div>;
}
