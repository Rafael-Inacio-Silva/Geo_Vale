import {useEffect,useRef,useState} from 'react';
import L from 'leaflet';
import type {Estudo} from './tipos.ts';
import 'leaflet/dist/leaflet.css';

/** Apresenta contorno e imagem aérea local; não solicita imagens Google nem transmite o mapa a terceiros. */
export default function MapaArea({estudo}:{estudo:Estudo}) {
  const elemento=useRef<HTMLDivElement>(null);
  const mapa=useRef<L.Map|null>(null);
  const [fundo,setFundo]=useState(true);
  const [falha,setFalha]=useState(false);
  useEffect(()=>{
    if(!elemento.current) return;
    setFalha(false);
    const m=L.map(elemento.current,{zoomControl:false,attributionControl:true,scrollWheelZoom:false});
    mapa.current=m;
    L.control.zoom({position:'bottomright'}).addTo(m);
    const geo=L.geoJSON(estudo.geometria,{style:{color:'#ffd14a',weight:3,fillColor:'#ffc329',fillOpacity:.08}});
    if(estudo.imagem && fundo) {
      L.imageOverlay(estudo.imagem.url,estudo.imagem.bounds,{attribution:estudo.imagem.credito,interactive:false}).on('error',()=>setFalha(true)).addTo(m);
    }
    // Duas linhas mantêm o contorno legível sobre áreas claras e escuras da imagem.
    L.geoJSON(estudo.geometria,{style:{color:'#00473f',weight:6,opacity:.8,fillOpacity:0},interactive:false}).addTo(m);
    geo.addTo(m);
    /** Mantém a poligonal inteira visível quando o contêiner muda de largura ou altura. */
    function ajustarJanela(){
      if(!elemento.current)return;
      const margem=Math.max(12,Math.min(32,elemento.current.clientWidth*.04));
      m.invalidateSize({animate:false});
      m.fitBounds(geo.getBounds(),{padding:[margem,margem],maxZoom:15,animate:false});
    }
    ajustarJanela();
    L.control.scale({imperial:false,position:'bottomleft'}).addTo(m);
    let quadro=0;
    const observador=new ResizeObserver(()=>{
      cancelAnimationFrame(quadro);
      quadro=requestAnimationFrame(ajustarJanela);
    });
    observador.observe(elemento.current);
    return ()=>{observador.disconnect();cancelAnimationFrame(quadro);m.remove();mapa.current=null;};
  },[estudo.id,fundo]);
  /** Retorna ao enquadramento da poligonal sem alterar análise ou prioridades. */
  function enquadrar(){mapa.current?.fitBounds(L.geoJSON(estudo.geometria).getBounds(),{padding:[32,32],maxZoom:15});}
  return <div className="mapa-conjunto">
    <div ref={elemento} className="mapa" aria-label={`Mapa da área ${estudo.nome}`} role="region"/>
    <div className="mapa-ferramentas">
      {estudo.imagem?<button type="button" className="mapa-botao" aria-pressed={fundo} onClick={()=>setFundo(!fundo)}>{fundo?'Imagem aérea':'Contorno'}</button>:null}
      <button type="button" className="mapa-botao" onClick={enquadrar}>Enquadrar área</button>
    </div>
    <span className="mapa-legenda"><i/> Área enviada</span>
    {falha?<p className="mapa-falha" role="status">Imagem indisponível. O contorno e a análise continuam disponíveis.</p>:null}
  </div>;
}
