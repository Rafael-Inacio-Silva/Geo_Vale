import {useState} from 'react';
import type {CamadaTerritorial, CamadasAtivas, EstadoCamada, LegendaTrilha} from './tipos.ts';

interface Propriedades {
  camadas: CamadaTerritorial[];
  ativas: CamadasAtivas;
  estados: Record<string, EstadoCamada>;
  legendaTrilhas: LegendaTrilha[];
  alterar: (id: string, opacidade: number | null) => void;
  recarregar: (id: string) => void;
}

/** Mostra a legenda oficial e permite recuperar uma imagem que não carregou. */
function Legenda({nome, url}: {nome: string; url: string}) {
  const [falhou, setFalhou] = useState(false);
  const [tentativa, setTentativa] = useState(0);
  return <figure className="legenda-tema">
    <figcaption>{nome}</figcaption>
    {falhou ? <button type="button" className="tentar-novamente" onClick={() => {setFalhou(false); setTentativa(atual => atual + 1);}}>Recarregar legenda</button>
      : <img key={tentativa} src={url} alt={`Cores e classes de ${nome}`} onError={() => setFalhou(true)}/>}
  </figure>;
}

/** Usa os nomes e cores oficiais apenas das categorias retornadas neste enquadramento. */
function LegendaTrilhas({trilhas, estado}: {trilhas: LegendaTrilha[]; estado?: EstadoCamada}) {
  if (!trilhas.length) return <p className="estado-tema">{estado === 'erro' ? 'Legenda indisponível.' : estado === 'carregando' || !estado ? 'Carregando legenda…' : 'Nenhuma trilha neste enquadramento.'}</p>;
  return <ul className="legenda-trilhas" aria-label="Trilhas no enquadramento" tabIndex={0}>
    {trilhas.map(trilha => <li key={trilha.id}><i style={{borderColor: trilha.cor, borderTopWidth: trilha.largura, opacity: trilha.opacidade}} aria-hidden="true"/><span>{trilha.nome}</span></li>)}
  </ul>;
}

/** Solicita imagens WMS somente ao abrir; nas trilhas, usa a legenda da consulta vetorial. */
function LegendasTema({bases, trilhas, estado}: {bases: CamadaTerritorial['bases']; trilhas?: LegendaTrilha[]; estado?: EstadoCamada}) {
  const [aberta, setAberta] = useState(false);
  return <details className="legendas-tema" onToggle={evento => setAberta(evento.currentTarget.open)}><summary>Legenda</summary>
    {aberta ? trilhas !== undefined ? <LegendaTrilhas trilhas={trilhas} estado={estado}/> : bases.filter(base => base.mapa !== false).map(base => <Legenda key={base.camada} nome={base.nome} url={base.legenda}/>) : null}
  </details>;
}

/** Liga temas independentes e ajusta a transparência sem esconder o mapa de fundo. */
export default function CamadasTerritorio({camadas, ativas, estados, legendaTrilhas, alterar, recarregar}: Propriedades) {
  const [expandidas, setExpandidas] = useState<Record<string, boolean>>({});
  return <section className="camadas" aria-labelledby="titulo-camadas">
    <div className="cabecalho-camadas"><h2 id="titulo-camadas">Camadas</h2><span>Expandir no mapa</span></div>
    <div className="lista-camadas">
      {camadas.map(camada => {
        const ativa = ativas[camada.id] !== undefined;
        const estado = estados[camada.id];
        const expandida = expandidas[camada.id] ?? false;
        return <div key={camada.id} className={`tema ${ativa ? 'tema-ativo' : ''}`}>
          <div className="cabecalho-tema">
            <label className="seletor-tema">
              <input type="checkbox" checked={ativa} onChange={evento => alterar(camada.id, evento.target.checked ? camada.opacidade : null)}/>
              <span className="nome-tema">{camada.nome}</span><i className="cor-tema" style={{background: camada.cor}} aria-hidden="true"/>
            </label>
            {ativa ? <button type="button" className="expandir-tema" aria-label={`Opções de ${camada.nome}`} aria-expanded={expandida} aria-controls={`opcoes-${camada.id}`} onClick={() => setExpandidas(atuais => ({...atuais, [camada.id]: !expandida}))}><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m7 10 5 5 5-5"/></svg></button> : null}
          </div>
          {ativa ? <>
          <div id={`opcoes-${camada.id}`} className="opcoes-tema" hidden={!expandida}>
            <label className="transparencia" htmlFor={`opacidade-${camada.id}`}>Intensidade <output>{Math.round(ativas[camada.id] * 100)}%</output></label>
            <input id={`opacidade-${camada.id}`} aria-label={`Intensidade de ${camada.nome}`} type="range" min="10" max="100" step="5" value={Math.round(ativas[camada.id] * 100)} onChange={evento => alterar(camada.id, Number(evento.target.value) / 100)}/>
            <LegendasTema bases={camada.bases} trilhas={camada.tipo === 'geojson' ? legendaTrilhas : undefined} estado={estado}/>
          </div>
          <div className="estado-camada">
            {estado === 'erro' ? <p className="erro-tema" role="status">Camada indisponível. <button type="button" className="tentar-novamente" onClick={() => recarregar(camada.id)}>Recarregar</button></p> : null}
            {estado === 'carregando' ? <p className="estado-tema" role="status">Carregando…</p> : null}
            {estado === 'fora' ? <p className="estado-tema">Disponível em {camada.alcance}.</p> : null}
            {estado === 'vazia' ? <p className="estado-tema">Sem trilhas cadastradas neste enquadramento.</p> : null}
          </div>
          </> : null}
        </div>;
      })}
    </div>
  </section>;
}
