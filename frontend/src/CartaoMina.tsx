import {useState} from 'react';
import type {EstadoANM, Mina} from './tipos.ts';

interface Propriedades {
  mina: Mina;
  selecionada: boolean;
  selecionar: (mina: Mina) => void;
  anm: EstadoANM;
  recarregar: () => void;
}

/** Mantém identificação e detalhes opcionais dentro do mesmo cartão da mina. */
export default function CartaoMina({mina, selecionada, selecionar, anm, recarregar}: Propriedades) {
  const [aberto, setAberto] = useState(false);
  const expandido = aberto && selecionada;
  const idDetalhes = `detalhes-${mina.id}`;
  const processo = anm.dados?.properties;
  return <article className={`cartao-mina ${selecionada ? 'selecionada' : ''}`}>
    <div className="cabecalho-mina">
      <button type="button" className="mina" aria-pressed={selecionada} onClick={() => selecionar(mina)}>
        <span className="ponto-mina" aria-hidden="true"/><span><strong>{mina.nome}</strong><span>{mina.empresa} · {mina.municipio}/{mina.uf}</span></span>
      </button>
      <button type="button" className="expandir-mina" aria-label={`Detalhes de ${mina.nome}`} aria-expanded={expandido} aria-controls={idDetalhes} onClick={() => {setAberto(!expandido); if (!expandido && !selecionada) selecionar(mina);}}>
        <svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path d="m6 9 6 6 6-6" fill="none" stroke="currentColor" strokeWidth="2"/></svg>
      </button>
    </div>
    <div id={idDetalhes} className="detalhe-mina" hidden={!expandido}>
      <dl><div><dt>Empresa</dt><dd>{mina.empresa}</dd></div><div><dt>Município</dt><dd>{mina.municipio}/{mina.uf}</dd></div><div><dt>Complexo</dt><dd>{mina.complexo}</dd></div></dl>
      {anm.carregando ? <p className="estado-cadastro" role="status">Consultando ANM…</p> : processo ? <>
        <dl className="cadastro-anm"><div><dt>Processo ANM</dt><dd>{processo.processo}</dd></div><div><dt>Titular</dt><dd>{processo.titular}</dd></div><div><dt>Fase cadastral</dt><dd>{processo.fase}</dd></div><div><dt>Área cadastrada</dt><dd>{processo.area_ha.toLocaleString('pt-BR', {maximumFractionDigits: 2})} ha</dd></div></dl>
        <p className="fonte-cadastro">ANM · {new Date(anm.dados!.fonte.consultado_em).toLocaleDateString('pt-BR')}</p>
      </> : anm.erro ? <p className="erro-cadastro" role="status">{anm.erro} <button type="button" className="tentar-novamente" onClick={recarregar}>Recarregar ANM</button></p> : null}
      <p className="referencia">Localização de referência</p>
    </div>
  </article>;
}
