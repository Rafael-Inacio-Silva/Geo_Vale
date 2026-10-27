import {useCallback, useEffect, useRef, useState} from 'react';
import {requisitar} from './api.ts';
import {filtrarMinas} from './busca.mjs';
import type L from 'leaflet';
import Influencia from './Influencia.tsx';
import MapaTerritorio from './MapaTerritorio.tsx';
import CamadasTerritorio from './CamadasTerritorio.tsx';
import CartaoMina from './CartaoMina.tsx';
import {useProcessoANM} from './useProcessoANM.ts';
import type {CamadasAtivas, ConfiguracaoMapa, EstadoCamada, LegendaTrilha, LimiteMG, Mina} from './tipos.ts';

let configuracaoPendente: Promise<ConfiguracaoMapa> | null = null;
let limitePendente: Promise<LimiteMG> | null = null;

/** Compartilha as leituras durante a montagem dupla do StrictMode. */
function carregarConfiguracao() {
  configuracaoPendente ??= requisitar<ConfiguracaoMapa>('/api/mapa').catch(erro => {
    configuracaoPendente = null;
    throw erro;
  });
  return configuracaoPendente;
}

function carregarLimite() {
  limitePendente ??= requisitar<LimiteMG>('/api/mapa/limite-mg').catch(erro => {
    limitePendente = null;
    throw erro;
  });
  return limitePendente;
}

/** Organiza mapa central, consulta à direita e influência e dados do território na barra esquerda. */
export default function App() {
  const [barraTerritorio, setBarraTerritorio] = useState(true);
  const [barraConsulta, setBarraConsulta] = useState(true);
  const [mapa, setMapa] = useState<L.Map | null>(null);
  const prioridadeTerritorio = useRef(false);
  const priorizarTerritorio = useCallback(() => {prioridadeTerritorio.current = true;}, []);
  const [configuracao, setConfiguracao] = useState<ConfiguracaoMapa | null>(null);
  const [limite, setLimite] = useState<LimiteMG | null>(null);
  const [enquadrarMunicipio, setEnquadrarMunicipio] = useState(true);
  const [selecionada, setSelecionada] = useState<Mina | null>(null);
  const anm = useProcessoANM(selecionada?.id);
  const [ativas, setAtivas] = useState<CamadasAtivas>({});
  const [estadosCamadas, setEstadosCamadas] = useState<Record<string, EstadoCamada>>({});
  const [recargasCamadas, setRecargasCamadas] = useState<Record<string, number>>({});
  const [legendaTrilhas, setLegendaTrilhas] = useState<LegendaTrilha[]>([]);
  const [consulta, setConsulta] = useState('');
  const [erroConfiguracao, setErroConfiguracao] = useState('');
  const [erroLimite, setErroLimite] = useState('');
  const [tentativa, setTentativa] = useState(0);

  useEffect(() => {
    let ativo = true;
    setErroConfiguracao('');
    setErroLimite('');
    void carregarConfiguracao().then(dados => {
      if (ativo) setConfiguracao(dados);
    }).catch(erro => {if (ativo) setErroConfiguracao(erro.message);});
    void carregarLimite().then(dados => {
      if (ativo) setLimite(dados);
    }).catch(erro => {if (ativo) setErroLimite(erro.message);});
    return () => {ativo = false;};
  }, [tentativa]);

  const minas = configuracao ? filtrarMinas(configuracao.minas, consulta) : [];
  const erro = erroConfiguracao || erroLimite;

  /** O cartão alterna seleção; o marcador sempre aproxima a mina. */
  function selecionarMina(mina: Mina, origem: 'cartao' | 'marcador' = 'cartao') {
    if (origem === 'cartao' && selecionada?.id === mina.id) {
      setSelecionada(null);
      return;
    }
    setEnquadrarMunicipio(origem === 'cartao');
    setSelecionada({...mina});
  }

  function alterarCamada(id: string, opacidade: number | null) {
    setAtivas(atuais => {
      const proximas = {...atuais};
      if (opacidade === null) delete proximas[id]; else proximas[id] = opacidade;
      return proximas;
    });
  }

  function informarEstado(id: string, estado: EstadoCamada) {
    setEstadosCamadas(atuais => atuais[id] === estado ? atuais : {...atuais, [id]: estado});
  }

  return <>
    <a href="#territorio" className="pular-conteudo">Ir para o mapa</a>
    <header className="cabecalho">
      <div className="marca">
        <svg viewBox="0 0 40 40" aria-hidden="true"><rect x="1" y="1" width="38" height="38" rx="10" fill="none" stroke="currentColor" opacity=".4"/><path d="M9 28L17 12L23 22L28 15L33 28H9" fill="none" stroke="#ffc329" strokeWidth="2"/></svg>
        <span>GeoVale</span>
      </div>
    </header>
    <main className="conteudo">
      <h1 className="somente-leitor">GeoVale — mapa territorial</h1>
      <div className={`territorio${barraTerritorio ? '' : ' territorio-oculto'}${barraConsulta ? '' : ' consulta-oculta'}`}>
        <aside id="barra-territorio" className="painel-territorio" aria-label="Território da mina" hidden={!barraTerritorio}>
          <h2>Território da mina</h2>
          <Influencia mapa={mapa} minaId={selecionada?.id} temas={configuracao?.camadas ?? []} expandidas={ativas} aoConsultar={priorizarTerritorio} informarLegenda={setLegendaTrilhas}/>
        </aside>
        <button type="button" className="alternar-painel alternar-territorio" aria-controls="barra-territorio" aria-expanded={barraTerritorio} aria-label={barraTerritorio ? 'Ocultar território' : 'Mostrar território'} title={barraTerritorio ? 'Ocultar território' : 'Mostrar território'} onClick={() => setBarraTerritorio(valor => !valor)}><svg viewBox="0 0 24 24" aria-hidden="true"><path d={barraTerritorio ? 'm14 7-5 5 5 5' : 'm10 7 5 5-5 5'}/></svg><span>Território</span></button>
        <button type="button" className="alternar-painel alternar-consulta" aria-controls="barra-consulta" aria-expanded={barraConsulta} aria-label={barraConsulta ? 'Ocultar mina e camadas' : 'Mostrar mina e camadas'} title={barraConsulta ? 'Ocultar mina e camadas' : 'Mostrar mina e camadas'} onClick={() => setBarraConsulta(valor => !valor)}><svg viewBox="0 0 24 24" aria-hidden="true"><path d={barraConsulta ? 'm10 7 5 5-5 5' : 'm14 7-5 5 5 5'}/></svg><span>Mina e camadas</span></button>
        <aside id="barra-consulta" className="pesquisa" aria-label="Pesquisa de minas" hidden={!barraConsulta}>
          <label htmlFor="pesquisa-mina">Pesquisar mina</label>
          <div className="campo-pesquisa">
            <svg width="19" height="19" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5" stroke="currentColor" strokeWidth="1.7"/><path d="m16 16 4 4" stroke="currentColor" strokeWidth="1.7"/></svg>
            <input id="pesquisa-mina" type="search" placeholder="Nome da mina" value={consulta} onChange={evento => setConsulta(evento.target.value)} autoComplete="off"/>
          </div>
          <div className="lista-minas" aria-live="polite">
            {configuracao ? (minas.length ? minas.map(mina => <CartaoMina key={mina.id} mina={mina} selecionada={selecionada?.id === mina.id} selecionar={selecionarMina} anm={anm.estado} recarregar={anm.recarregar}/>) : <p className="vazio">Nenhuma mina encontrada.</p>) : <p role="status" className="vazio">{erroConfiguracao ? 'Pesquisa indisponível.' : 'Carregando minas…'}</p>}
          </div>
          {configuracao ? <CamadasTerritorio camadas={configuracao.camadas} ativas={ativas} estados={estadosCamadas} legendaTrilhas={legendaTrilhas} alterar={alterarCamada} recarregar={id => setRecargasCamadas(atuais => ({...atuais, [id]: (atuais[id] ?? 0) + 1}))}/> : null}
          {erro ? <div className="erro" role="alert"><p>{erro}</p><button type="button" className="tentar-novamente" onClick={() => setTentativa(atual => atual + 1)}>Tentar novamente</button></div> : null}
        </aside>
        <section id="territorio" className="painel-mapa" aria-label="Mapa territorial" tabIndex={-1}>
          {configuracao ? <MapaTerritorio enquadrarMunicipio={enquadrarMunicipio} configuracao={configuracao} limite={limite} selecionada={selecionada} selecionar={selecionarMina} ativas={ativas} recargas={recargasCamadas} informarEstado={informarEstado} informarLegendaTrilhas={setLegendaTrilhas} informarMapa={setMapa} prioridadeTerritorio={prioridadeTerritorio} voltar={() => setSelecionada(null)}/> : <div className="mapa-carregando" role="status">{erroConfiguracao ? 'Mapa indisponível.' : 'Abrindo mapa…'}</div>}
          {limite?.aviso ? <p className="aviso-fonte" role="status">{limite.aviso}</p> : null}
        </section>
      </div>
    </main>
    <footer className="rodape"><span>Desenvolvido por Rafael Inácio Silva · MVP · 2026</span><span>Dados: fontes públicas</span></footer>
  </>;
}
