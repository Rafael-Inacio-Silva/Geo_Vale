import {useEffect} from 'react';
import type {ExplicacaoSugestao, SetorSugerido, SugestaoUso} from './tipos.ts';

const numero = (valor: number, casas = 0) => valor.toLocaleString('pt-BR', {minimumFractionDigits: casas, maximumFractionDigits: casas});

/** Ranking, robustez, condicionantes e porquê do setor aberto, logo abaixo dele na lista. */
function DetalheSetor({setor, variacao, explicacao, explicando}: {
  setor: SetorSugerido; variacao: number; explicacao: ExplicacaoSugestao | null; explicando: boolean;
}) {
  const daIa = explicacao?.metodo === 'ia' && explicacao.textos[setor.id];
  return <article id={`detalhe-${setor.id}`} className="detalhe-setor" aria-label={`Detalhe de ${setor.id}`}>
    {setor.descricao ? <p className="estruturas-setor">{setor.descricao}</p> : null}
    <ol className="ranking-setor">
      {setor.ranking.map(uso => <li key={uso.uso}>
        <span><b>{uso.nome}</b><output>{numero(uso.nota)}</output></span>
        <i aria-hidden="true"><i style={{inlineSize: `${Math.max(uso.nota, 1)}%`, background: uso.cor}}/></i>
        {uso.permitido < 99.5 ? <small>Lei permite em {numero(uso.permitido)}% da área</small> : null}
      </li>)}
    </ol>
    <p className={setor.robustez.estavel ? 'robustez-setor' : 'robustez-setor sensivel'}>
      {setor.robustez.estavel ? `Estável com ±${numero(variacao * 100)}% nos pesos` : `Sensível: o 1º lugar muda com ±${numero(variacao * 100)}% nos pesos`}
    </p>
    {setor.cavidades >= 1 || setor.montante.length ? <ul className="condicionantes-setor">
      {setor.cavidades >= 1 ? <li>Potencial alto de cavidades em {numero(setor.cavidades)}% do setor</li> : null}
      {setor.montante.length ? <li>Barragem alteada a montante: depende da descaracterização</li> : null}
    </ul> : null}
    <h4 className="titulo-porque">{daIa ? 'Por que (IA)' : 'Por que'}{explicando ? <span role="status"> · gerando explicação…</span> : null}</h4>
    <p className="porque-setor">{daIa || setor.explicacao}</p>
  </article>;
}

/** Barra esquerda no modo sugestão, abaixo de Sugerir uso: legenda e setores; o setor aberto mostra o detalhe logo abaixo. */
export function ResultadoSugestao({sugestao, erro, carregando, recarregar, selecionado, selecionar, explicacao, explicando}: {
  sugestao: SugestaoUso | null; erro: string; carregando: boolean; recarregar: () => void;
  selecionado: string | null; selecionar: (id: string) => void;
  explicacao: ExplicacaoSugestao | null; explicando: boolean;
}) {
  // Setor aberto pelo mapa entra na área visível da lista.
  useEffect(() => {
    if (selecionado) document.getElementById(`setor-${selecionado}`)?.scrollIntoView({block: 'nearest'});
  }, [selecionado]);

  return <section className="painel-sugestao resultado-sugestao" aria-labelledby="titulo-sugestao">
    <div className="cabecalho-camadas"><h2 id="titulo-sugestao">Sugestão de uso</h2></div>
    {erro ? <p className="erro-territorio" role="alert">{erro} <button className="tentar-novamente" type="button" onClick={recarregar}>Tentar novamente</button></p> : null}
    {carregando && !sugestao ? <p className="nota-territorio" role="status">Calculando sugestão…</p> : null}
    {sugestao ? <>
      <ul className="legenda-usos" aria-label="Cor do 1º uso em cada setor">
        {sugestao.usos.map(u => <li key={u.id}><i style={{background: u.cor}} aria-hidden="true"/>{u.nome}</li>)}
      </ul>
      <p className="nota-territorio">Nota de 0 a 100: quanto o setor combina com o uso. Não é área nem probabilidade.</p>
      <ul className="setores-sugeridos" aria-label="Setores da área minerada">
        {sugestao.setores.map(s => <li key={s.id} id={`setor-${s.id}`}>
          <button type="button" aria-expanded={s.id === selecionado} aria-controls={`detalhe-${s.id}`} onClick={() => selecionar(s.id)}>
            <i style={{background: s.ranking[0].cor}} aria-hidden="true"/>
            <span><b>{s.id}</b> · {numero(s.ha)} ha<br/>{s.ranking[0].nome} · {numero(s.ranking[0].nota)}{s.robustez.estavel ? '' : ' · sensível'}</span>
          </button>
          {s.id === selecionado ? <DetalheSetor setor={s} variacao={sugestao.variacao} explicacao={explicacao} explicando={explicando}/> : null}
        </li>)}
      </ul>
      {selecionado ? null : <p className="nota-territorio">Clique em um setor no mapa ou na lista para ver o ranking e o porquê; clique de novo para fechar.</p>}
    </> : null}
  </section>;
}

/** Barra direita no modo sugestão: só os pesos, a emissão com pesos ajustados e a volta ao AHP. */
export function PesosSugestao({sugestao, pesos, alterarPesos, emitirRelatorio}: {
  sugestao: SugestaoUso | null; pesos: number[] | null; alterarPesos: (pesos: number[] | null) => void; emitirRelatorio: () => void;
}) {
  const valores = pesos ?? sugestao?.criterios.map(c => Math.round(c.peso_ahp * 100)) ?? [];
  const soma = valores.reduce((a, b) => a + b, 0) || 1;

  function mudarPeso(indice: number, valor: number) {
    const proximos = [...valores];
    proximos[indice] = valor;
    alterarPesos(proximos.some(v => v > 0) ? proximos : null);
  }

  return <section className="painel-sugestao" aria-labelledby="titulo-pesos">
    <div className="cabecalho-camadas"><h2 id="titulo-pesos">Pesos dos critérios</h2></div>
    {sugestao ? <fieldset className="pesos-criterios">
      <legend className="somente-leitor">Pesos dos critérios</legend>
      {sugestao.criterios.map((c, i) => <label key={c.id} className="peso-criterio">
        <span>{c.nome}<output>{Math.round(valores[i] / soma * 100)}%</output></span>
        <input type="range" min="0" max="100" step="1" value={valores[i]} aria-label={`Peso de ${c.nome}`} onChange={evento => mudarPeso(i, Number(evento.target.value))}/>
      </label>)}
      {pesos ? <button type="button" className="emitir-com-pesos" onClick={emitirRelatorio}>Emitir relatório com estes pesos</button> : null}
      <button type="button" className="tentar-novamente" disabled={!pesos} onClick={() => alterarPesos(null)}>Restaurar AHP</button>
    </fieldset> : <p className="nota-territorio" role="status">Calculando sugestão…</p>}
  </section>;
}
