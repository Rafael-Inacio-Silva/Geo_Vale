import {useEffect, useRef, useState} from 'react';
import L from 'leaflet';
import type {FeatureCollection, MultiPolygon, Polygon} from 'geojson';
import {requisitar} from './api.ts';
import type {SetorSugerido, SugestaoUso as Sugestao} from './tipos.ts';

/** Monta o conteúdo do popup com texto seguro, sem interpretar HTML. */
function detalheSetor(setor: SetorSugerido) {
  const raiz = document.createElement('div');
  raiz.className = 'popup-setor';
  const titulo = document.createElement('strong');
  titulo.textContent = `${setor.id} · ${setor.ha.toLocaleString('pt-BR', {maximumFractionDigits: 1})} ha`;
  const lista = document.createElement('ol');
  for (const uso of setor.ranking) {
    const item = document.createElement('li');
    item.textContent = `${uso.nome}: ${Math.round(uso.nota)}` + (uso.permitido < 99.5 ? ` (permitido em ${Math.round(uso.permitido)}%)` : '');
    lista.append(item);
  }
  const explicacao = document.createElement('p');
  explicacao.textContent = setor.explicacao;
  raiz.append(titulo, lista, explicacao);
  return raiz;
}

/** Ordena usos por setor da área minerada; os pesos escolhidos aqui também seguem para o relatório. */
export default function SugestaoUso({mapa, minaId, pronto, pesos, alterarPesos}: {
  mapa: L.Map | null; minaId: string; pronto: boolean; pesos: number[] | null; alterarPesos: (pesos: number[] | null) => void;
}) {
  const [aberta, setAberta] = useState(false);
  const [sugestao, setSugestao] = useState<Sugestao | null>(null);
  const [erro, setErro] = useState('');
  const [carregando, setCarregando] = useState(false);
  const [tentativa, setTentativa] = useState(0);
  const enquadrada = useRef(false);

  useEffect(() => {
    if (!aberta) return;
    const controle = new AbortController();
    setCarregando(true);
    setErro('');
    // Espera o engenheiro parar de arrastar antes de recalcular.
    const prazo = setTimeout(() => {
      const consulta = pesos ? `?pesos=${pesos.join(',')}` : '';
      void requisitar<Sugestao>(`/api/minas/${encodeURIComponent(minaId)}/sugestao${consulta}`, controle.signal).then(dados => {
        if (controle.signal.aborted) return;
        setSugestao(dados);
        setCarregando(false);
      }).catch(falha => {
        if (controle.signal.aborted) return;
        setErro(falha.message);
        setCarregando(false);
      });
    }, 350);
    return () => {clearTimeout(prazo); controle.abort();};
  }, [aberta, minaId, pesos, tentativa]);

  useEffect(() => {
    if (!aberta || !mapa || !sugestao) return;
    if (!mapa.getPane('sugestao')) mapa.createPane('sugestao').style.zIndex = '440';
    const setores = sugestao.setores;
    const colecao: FeatureCollection<Polygon | MultiPolygon, {id: string}> = {type: 'FeatureCollection', features: setores.map(s => ({type: 'Feature', properties: {id: s.id}, geometry: s.geometria}))};
    const camada = L.geoJSON(colecao, {
      pane: 'sugestao',
      style: f => ({color: '#ffffff', weight: 1.5, fillColor: setores.find(s => s.id === f?.properties.id)?.ranking[0].cor ?? '#536d64', fillOpacity: .72}),
      onEachFeature: (f, camadaSetor) => {
        const setor = setores.find(s => s.id === f.properties.id);
        if (!setor) return;
        camadaSetor.bindTooltip(`${setor.id} · ${setor.ranking[0].nome}`, {sticky: true});
        camadaSetor.bindPopup(() => detalheSetor(setor), {maxWidth: 300});
      },
    }).addTo(mapa);
    if (!enquadrada.current && setores.length) {
      enquadrada.current = true;
      mapa.stop();
      mapa.fitBounds(camada.getBounds(), {padding: [30, 60], maxZoom: 15, animate: false});
    }
    return () => {camada.remove();};
  }, [aberta, mapa, sugestao]);

  const valores = pesos ?? sugestao?.criterios.map(c => Math.round(c.peso_ahp * 100)) ?? [];
  const soma = valores.reduce((a, b) => a + b, 0) || 1;

  function mudarPeso(indice: number, valor: number) {
    const proximos = [...valores];
    proximos[indice] = valor;
    alterarPesos(proximos.some(v => v > 0) ? proximos : null);
  }

  return <div className="sugestao-uso">
    <button type="button" className="abrir-influencia" aria-pressed={aberta} disabled={!pronto || !mapa} onClick={() => {setAberta(v => !v); enquadrada.current = false;}}>
      Sugerir uso <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/></svg>
    </button>
    {aberta ? <div className="painel-sugestao">
      {erro ? <p className="erro-territorio" role="alert">{erro} <button className="tentar-novamente" type="button" onClick={() => setTentativa(v => v + 1)}>Tentar novamente</button></p> : null}
      {carregando ? <p className="nota-territorio" role="status">{sugestao ? 'Recalculando…' : 'Calculando sugestão…'}</p> : null}
      {sugestao ? <>
        <ul className="legenda-usos" aria-label="Cor do 1º uso em cada setor">
          {sugestao.usos.map(u => <li key={u.id}><i style={{background: u.cor}} aria-hidden="true"/>{u.nome}</li>)}
        </ul>
        <fieldset className="pesos-criterios">
          <legend>Pesos dos critérios</legend>
          {sugestao.criterios.map((c, i) => <label key={c.id} className="peso-criterio">
            <span>{c.nome}<output>{Math.round(valores[i] / soma * 100)}%</output></span>
            <input type="range" min="0" max="100" step="1" value={valores[i]} aria-label={`Peso de ${c.nome}`} onChange={evento => mudarPeso(i, Number(evento.target.value))}/>
          </label>)}
          <p className="nota-territorio">{pesos ? 'Pesos ajustados; o relatório usa estes pesos.' : `Pesos calculados por AHP (consistência ${sugestao.razao_consistencia.toLocaleString('pt-BR', {maximumFractionDigits: 3})}).`}</p>
          <button type="button" className="tentar-novamente" disabled={!pesos} onClick={() => alterarPesos(null)}>Restaurar AHP</button>
        </fieldset>
        <ol className="setores-sugeridos" aria-label="1º uso por setor">
          {sugestao.setores.map(s => <li key={s.id}><b>{s.id}</b> {s.ranking[0].nome} · {Math.round(s.ranking[0].nota)}{s.robustez.estavel ? '' : ' · sensível aos pesos'}</li>)}
        </ol>
        <p className="nota-territorio">Sugestão para discussão. Clique em um setor para ver o ranking e o porquê.</p>
      </> : null}
    </div> : null}
  </div>;
}
