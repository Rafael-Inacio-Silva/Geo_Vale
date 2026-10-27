import {useEffect, useState} from 'react';
import L from 'leaflet';
import {requisitar} from './api.ts';
import CamadasNaInfluencia from './CamadasNaInfluencia.tsx';
import type {CamadaTerritorial, CamadasAtivas, InfluenciaTerritorial, LegendaTrilha, TerritorioPreparado} from './tipos.ts';

/** Alterna o território no mapa e exporta o relatório completo já preparado por mina. */
export default function Influencia({mapa, minaId, temas, expandidas, aoConsultar, informarLegenda}: {
  mapa: L.Map | null; minaId?: string; temas: CamadaTerritorial[]; expandidas: CamadasAtivas;
  aoConsultar: () => void; informarLegenda: (legenda: LegendaTrilha[]) => void;
}) {
  const [aberta, setAberta] = useState(false);
  const [contorno, setContorno] = useState<InfluenciaTerritorial | null>(null);
  const [territorio, setTerritorio] = useState<TerritorioPreparado | null>(null);
  const [erro, setErro] = useState('');
  const [tentativa, setTentativa] = useState(0);
  const [exportando, setExportando] = useState(false);
  const [erroExportacao, setErroExportacao] = useState('');

  useEffect(() => {
    setAberta(false);
    setContorno(null);
    setTerritorio(null);
    setErro('');
    setErroExportacao('');
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
    for (const f of contorno.features.filter(f => aberta || f.properties.id === 'mina').sort((a, b) => a.properties.id === 'mina' ? 1 : b.properties.id === 'mina' ? -1 : 0)) {
      const mina = f.properties.id === 'mina';
      L.geoJSON(f, {
        pane: 'influencia', interactive: false,
        attribution: mina ? 'Mina: &copy; <a href="https://www.openstreetmap.org/way/315221699">OpenStreetMap</a> contributors (ODbL)' : 'Influência: <a href="https://sistemas.meioambiente.mg.gov.br/consulta-intervencao/uploads/122024/24642_gvwxhTH__066nrKD6s2u.pdf" target="_blank" rel="noopener noreferrer">FEAM / Vale / Amplo</a>',
        style: {color: mina ? '#00594f' : '#efa900', weight: 3, fillColor: mina ? '#00594f' : '#ffc329', fillOpacity: mina ? .3 : .025},
      }).addTo(grupo);
    }
    return () => {grupo.remove();};
  }, [mapa, contorno, aberta, minaId]);

  function alternarInfluencia() {
    if (!mapa || !contorno || !minaId) return;
    aoConsultar();
    setAberta(valor => !valor);
    if (!aberta) {
      mapa.stop();
      mapa.fitBounds(L.geoJSON(contorno).getBounds(), {padding: [30, 60], maxZoom: 16, animate: false});
    }
  }

  async function exportar() {
    if (!minaId || exportando) return;
    setExportando(true);
    setErroExportacao('');
    try {
      const resposta = await fetch(`/api/minas/${encodeURIComponent(minaId)}/relatorio`, {signal: AbortSignal.timeout(60000)});
      if (!resposta.ok) throw new Error();
      const arquivo = await resposta.blob();
      const url = URL.createObjectURL(arquivo);
      const link = document.createElement('a');
      link.href = url;
      link.download = `geovale-${minaId}.json`;
      link.click();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
    } catch {
      setErroExportacao('Não foi possível exportar. Tente novamente.');
    } finally {
      setExportando(false);
    }
  }

  return <section className="influencia-territorio" aria-label="Influência da mina">
    <button type="button" className="abrir-influencia" aria-pressed={aberta} disabled={!minaId || !mapa || !contorno} onClick={alternarInfluencia}>Influência <svg viewBox="0 0 24 24" aria-hidden="true"><path d="m4 7 7-3 9 4-3 11-10 1-3-13Z"/></svg></button>
    {erro ? <p className="erro-territorio" role="alert">{erro} <button className="tentar-novamente" type="button" onClick={() => setTentativa(v => v + 1)}>Recarregar</button></p> : null}
    {aberta && mapa && contorno && minaId ? <>
      <CamadasNaInfluencia mapa={mapa} minaId={minaId} contorno={contorno} temas={temas} expandidas={expandidas} informarLegenda={informarLegenda}/>
      <button type="button" className="exportar-territorio" disabled={!territorio?.completo || exportando} onClick={() => {void exportar();}}><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v12m-5-5 5 5 5-5M4 16v5h16v-5"/></svg>{exportando ? 'Exportando…' : territorio?.completo ? 'Exportar JSON' : 'Preparando relatório…'}</button>
      {erroExportacao ? <p className="erro-territorio" role="alert">{erroExportacao}</p> : null}
    </> : null}
  </section>;
}
