import type {SetorSugerido, SugestaoUso} from './tipos.ts';

const numero = (valor: number, casas = 0) => valor.toLocaleString('pt-BR', {minimumFractionDigits: casas, maximumFractionDigits: casas});

/** Ranking, robustez, condicionantes e porquê do setor escolhido, separados das notas. */
function DetalheSetor({setor, variacao}: {setor: SetorSugerido; variacao: number}) {
  return <article className="detalhe-setor" aria-labelledby={`titulo-${setor.id}`}>
    <h3 id={`titulo-${setor.id}`}>{setor.id} · {numero(setor.ha, 1)} ha</h3>
    {setor.descricao ? <p className="estruturas-setor">{setor.descricao}</p> : null}
    <ol className="ranking-setor">
      {setor.ranking.map(uso => <li key={uso.uso}>
        <span><b>{uso.nome}</b><output>{numero(uso.nota)}</output></span>
        <i aria-hidden="true"><i style={{inlineSize: `${Math.max(uso.nota, 1)}%`, background: uso.cor}}/></i>
        {uso.permitido < 99.5 ? <small>Permitido em {numero(uso.permitido)}% do setor</small> : null}
      </li>)}
    </ol>
    <p className={setor.robustez.estavel ? 'robustez-setor' : 'robustez-setor sensivel'}>
      {setor.robustez.estavel ? `Estável com ±${numero(variacao * 100)}% nos pesos` : `Sensível: o 1º lugar muda com ±${numero(variacao * 100)}% nos pesos`}
    </p>
    {setor.cavidades >= 1 || setor.montante.length ? <ul className="condicionantes-setor">
      {setor.cavidades >= 1 ? <li>Potencial alto de cavidades em {numero(setor.cavidades)}% do setor</li> : null}
      {setor.montante.length ? <li>Barragem alteada a montante: depende da descaracterização</li> : null}
    </ul> : null}
    <p className="porque-setor">{setor.explicacao}</p>
  </article>;
}

/** Substitui a lista de camadas no modo sugestão: legenda, setores, detalhe do escolhido e pesos. */
export default function PainelSugestao({sugestao, erro, carregando, recarregar, selecionado, selecionar, pesos, alterarPesos}: {
  sugestao: SugestaoUso | null; erro: string; carregando: boolean; recarregar: () => void;
  selecionado: string | null; selecionar: (id: string) => void;
  pesos: number[] | null; alterarPesos: (pesos: number[] | null) => void;
}) {
  const valores = pesos ?? sugestao?.criterios.map(c => Math.round(c.peso_ahp * 100)) ?? [];
  const soma = valores.reduce((a, b) => a + b, 0) || 1;
  const setor = sugestao?.setores.find(s => s.id === selecionado);

  function mudarPeso(indice: number, valor: number) {
    const proximos = [...valores];
    proximos[indice] = valor;
    alterarPesos(proximos.some(v => v > 0) ? proximos : null);
  }

  return <section className="painel-sugestao" aria-labelledby="titulo-sugestao">
    <div className="cabecalho-camadas"><h2 id="titulo-sugestao">Sugestão de uso</h2><span>Para discussão</span></div>
    {erro ? <p className="erro-territorio" role="alert">{erro} <button className="tentar-novamente" type="button" onClick={recarregar}>Tentar novamente</button></p> : null}
    {carregando ? <p className="nota-territorio" role="status">{sugestao ? 'Recalculando…' : 'Calculando sugestão…'}</p> : null}
    {sugestao ? <>
      <ul className="legenda-usos" aria-label="Cor do 1º uso em cada setor">
        {sugestao.usos.map(u => <li key={u.id}><i style={{background: u.cor}} aria-hidden="true"/>{u.nome}</li>)}
      </ul>
      <ul className="setores-sugeridos" aria-label="Setores da área minerada">
        {sugestao.setores.map(s => <li key={s.id}>
          <button type="button" aria-pressed={s.id === selecionado} onClick={() => selecionar(s.id)}>
            <i style={{background: s.ranking[0].cor}} aria-hidden="true"/>
            <span><b>{s.id}</b> · {numero(s.ha)} ha<br/>{s.ranking[0].nome} · {numero(s.ranking[0].nota)}{s.robustez.estavel ? '' : ' · sensível'}</span>
          </button>
        </li>)}
      </ul>
      {setor ? <DetalheSetor setor={setor} variacao={sugestao.variacao}/> : <p className="nota-territorio">Clique em um setor no mapa ou na lista para ver o ranking e o porquê.</p>}
      <fieldset className="pesos-criterios">
        <legend>Pesos dos critérios</legend>
        {sugestao.criterios.map((c, i) => <label key={c.id} className="peso-criterio">
          <span>{c.nome}<output>{Math.round(valores[i] / soma * 100)}%</output></span>
          <input type="range" min="0" max="100" step="1" value={valores[i]} aria-label={`Peso de ${c.nome}`} onChange={evento => mudarPeso(i, Number(evento.target.value))}/>
        </label>)}
        <p className="nota-territorio">{pesos ? 'Pesos ajustados; Ver relatório usa estes pesos.' : `Pesos calculados por AHP (consistência ${numero(sugestao.razao_consistencia, 3)}).`}</p>
        <button type="button" className="tentar-novamente" disabled={!pesos} onClick={() => alterarPesos(null)}>Restaurar AHP</button>
      </fieldset>
    </> : null}
  </section>;
}
