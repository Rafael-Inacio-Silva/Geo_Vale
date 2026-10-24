import {useRef,useState} from 'react';
import type {Estudo} from './tipos.ts';
import {enviarArquivo,operar} from './api.ts';
import {mesmosPesos,pesosValidos} from './pesos.ts';
import MapaArea from './MapaArea.tsx';
import Prioridades from './Prioridades.tsx';
const formato=new Intl.NumberFormat('pt-BR',{maximumFractionDigits:2});

/** Jornada pública local: enviar, analisar, definir prioridades e comparar sem painéis técnicos ou login. */
export default function App(){
  const [estudo,setEstudo]=useState<Estudo|null>(null);
  const [pesos,setPesos]=useState<number[]>([]);const [erro,setErro]=useState('');
  const [atividade,setAtividade]=useState('');const [modal,setModal]=useState(false);const [arrastando,setArrastando]=useState(false);
  const arquivo=useRef<HTMLInputElement>(null);
  const ocupado=atividade!=='';
  const alterado=estudo!==null&&!mesmosPesos(pesos,estudo.pesos);
  const resultado=estudo&&!alterado?estudo.resultado:null;
  const podeExportar=Boolean(resultado&&estudo?.salvo_revisao);
  /** Publica resposta aceita e sincroniza as prioridades com a mesma versão do servidor. */
  function aceitar(novo:Estudo){setEstudo(novo);setPesos(novo.pesos);}
  /** Serializa ações da tela e mantém o último mapa válido quando uma operação falha. */
  async function executar(nome:string,acao:()=>Promise<Estudo>){
    if(ocupado)return;setAtividade(nome);setErro('');
    try{aceitar(await acao());}catch(e){setErro(e instanceof Error?e.message:'Não foi possível concluir. Tente novamente.');}
    finally{setAtividade('');}
  }
  /** Usa o mesmo upload para arquivo escolhido e arquivo arrastado. */
  function receber(f:File|undefined){if(f)void executar('Preparando mapa',()=>enviarArquivo(f));}
  /** Edita apenas o peso exibido e torna a comparação antiga indisponível para exportação. */
  function mudarPeso(indice:number,valor:string){const n=valor===''?NaN:Number(valor);setPesos(p=>p.map((v,i)=>i===indice?n:v));}
  /** Reinicia a tela sem apagar revisões já salvas na sessão. */
  function novaArea(){setEstudo(null);setPesos([]);setErro('');setModal(false);}
  const trilha=<div className="trilha" aria-label="Etapas da análise"><span className={!estudo?'atual':'concluida'}><b>1</b> Escolher área</span><i/><span className={estudo&&!estudo.analisada?'atual':estudo?.analisada?'concluida':''}><b>2</b> Entender o território</span><i/><span className={estudo?.analisada?'atual':''}><b>3</b> Comparar possibilidades</span></div>;
  return <><header className="cabecalho"><div className="marca">
    <svg viewBox="0 0 40 40" aria-hidden="true"><rect x="1" y="1" width="38" height="38" rx="10" fill="none" stroke="currentColor" opacity=".4"/><path d="M9 28L17 12L23 22L28 15L33 28H9" fill="none" stroke="#ffc329" strokeWidth="2"/></svg><span>GeoVale</span></div>
    </header>
    <main className={`conteudo ${estudo?'conteudo-estudo':'conteudo-inicio'}`} aria-busy={ocupado}>
      {estudo?trilha:null}
      {!estudo?<section className="inicio"><div className="apresentacao-inicio"><p className="sobretitulo">ÁREAS PÓS-MINERAÇÃO</p><h1>Qual o melhor <span>futuro</span> para esta área?</h1>{trilha}</div>
        <div className={`envio ${arrastando?'arrastando':''}`} onDragOver={e=>{e.preventDefault();if(!ocupado)setArrastando(true);}} onDragLeave={()=>setArrastando(false)} onDrop={e=>{e.preventDefault();setArrastando(false);if(!ocupado){if(e.dataTransfer.files.length!==1)setErro('Envie um mapa por vez.');else receber(e.dataTransfer.files[0]);}}}>
          <svg width="42" height="42" viewBox="0 0 32 32" fill="none" aria-hidden="true"><path d="M5 25h22M16 22V5m-7 7 7-7 7 7" stroke="currentColor" strokeWidth="1.6"/></svg>
          <h2>Envie seu mapa</h2><p>Arraste um mapa ou escolha o arquivo.</p><button type="button" className="botao principal" disabled={ocupado} onClick={()=>arquivo.current?.click()}>Enviar GeoJSON <span aria-hidden="true">↗</span></button><small>Uma poligonal por arquivo · GeoJSON · até 1 MB</small>
        </div>
      </section>:<>
        <div className="titulo-area"><div><p className="sobretitulo">ÁREA DE ESTUDO</p><h1>{estudo.nome}</h1><p>{estudo.localizacao} <span className="separador">·</span> {formato.format(estudo.area_ha)} hectares</p></div><button type="button" className="botao secundario" disabled={ocupado} onClick={novaArea}>Trocar mapa</button></div>
        <div className="grade-area"><section className="cartao cartao-mapa"><MapaArea estudo={estudo}/><div className="rodape-mapa"><span><strong>{formato.format(estudo.area_ha)}</strong> hectares</span><span><strong>{estudo.numero_partes}</strong> parte(s)</span><span className="limite-imagem">Contorno público · imagem de referência</span></div></section>
        <aside className="cartao painel-jornada">
          {!estudo.analisada?<><span className="numero-etapa">02</span><h2>Análise da área</h2>{!estudo.cobertura_disponivel?<p className="aviso">Área fora da cobertura disponível. Escolha outro mapa.</p>:null}<button type="button" className="botao principal largura" disabled={ocupado||!estudo.cobertura_disponivel} onClick={()=>void executar('Analisando o território',()=>operar(estudo,'analisar'))}>Analisar área <span aria-hidden="true">→</span></button></>:<>
          <span className="numero-etapa">03</span><h2>Defina suas prioridades</h2>
          <div className="pesos">{estudo.criterios.map((c,i)=><div className="peso" key={c.id}><label htmlFor={`peso-${c.id}`}>{c.nome}</label><div className="peso-controles"><input aria-label={`Ajustar ${c.nome}`} type="range" min="0" max="100" step=".01" disabled={ocupado} value={Number.isFinite(pesos[i])?pesos[i]:0} onChange={e=>mudarPeso(i,e.target.value)}/><div className="valor-peso"><input id={`peso-${c.id}`} type="number" min="0" max="100" step=".01" disabled={ocupado} value={Number.isFinite(pesos[i])?pesos[i]:''} onChange={e=>mudarPeso(i,e.target.value)}/><span>%</span></div></div></div>)}</div>
          <div className={`soma-pesos ${pesosValidos(pesos)?'valida':''}`}><span>Total distribuído</span><strong>{pesos.every(Number.isFinite)?formato.format(pesos.reduce((a,b)=>a+b,0)):'—'}%</strong></div>
          <button type="button" className="link-botao" disabled={ocupado} onClick={()=>setModal(true)}>Comparar prioridades</button>
          <p className="origem-pesos">{alterado||estudo.origem_pesos==='manual_usuario'?'Pesos personalizados.':estudo.origem_pesos==='ahp_usuario'?'Pesos por comparação.':'Pesos iniciais iguais.'}</p>
          <button type="button" className="botao principal largura" disabled={ocupado||!pesosValidos(pesos)} onClick={()=>void executar('Comparando possibilidades',()=>operar(estudo,'comparar',{pesos,origem:alterado||estudo.origem_pesos==='manual_usuario'?'manual':'ahp'}))}>Comparar opções <span aria-hidden="true">→</span></button>
          {!pesosValidos(pesos)?<p className="texto-discreto">O total deve ser 100%.</p>:null}</>}
        </aside></div>
        {estudo.resumo?<section className="caracteristicas" aria-label="Características principais"><div><span>Declividade mediana</span><strong>{formato.format(estudo.resumo.declividade_mediana_graus)}°</strong></div><div><span>Declividade P90</span><strong>{formato.format(estudo.resumo.declividade_p90_graus)}°</strong></div><div><span>Cobertura predominante · {estudo.resumo.ano_cobertura}</span><strong>{estudo.resumo.cobertura_predominante}</strong></div></section>:null}
        {alterado&&estudo.resultado?<p className="aviso" role="status">Prioridades alteradas. Compare novamente.</p>:null}
        {resultado?<section className="resultados" aria-labelledby="titulo-resultado"><div className="titulo-resultado"><div><p className="sobretitulo">RESULTADO</p><h2 id="titulo-resultado">Prioridade relativa para estudo</h2></div><span className="selo exploratorio">Análise preliminar</span></div>
          <div className="opcoes">{resultado.ranking.map(a=><article className={`opcao ${a.posicao===1?'primeira':''}`} key={a.id}><span className="posicao">{a.posicao.toString().padStart(2,'0')}</span><h3>{a.nome}</h3><div className="indice"><span>Índice relativo</span><strong>{a.indice.toFixed(3).replace('.',',')}</strong></div><div className="barra-indice"><i style={{width:`${a.indice*100}%`}}/></div></article>)}</div>
          <div className="nota-resultado"><strong>{resultado.sem_discriminacao?'Opções empatadas.':resultado.sensivel_aos_pesos?'Resultado sensível aos pesos.':'Resultado estável nos ajustes testados.'}</strong></div>
          <div className="acoes-relatorio"><div><button type="button" className="botao secundario" disabled={ocupado||podeExportar} onClick={()=>void executar('Salvando resultado',()=>operar(estudo,'salvar'))}>{podeExportar?'Resultado salvo ✓':'Salvar resultado'}</button>{podeExportar?<><a className="botao principal" href={`/api/areas/${estudo.id}/revisoes/${estudo.salvo_revisao}/simples`}>Relatório simples ↓</a><a className="link-botao" href={`/api/areas/${estudo.id}/revisoes/${estudo.salvo_revisao}/tecnico`}>Relatório técnico ↓</a></>:null}</div></div>
        </section>:null}
        {estudo.analisada?<p className="limite-analise">Comparação preliminar; uso sujeito à avaliação técnica.</p>:null}
      </>}
      <input ref={arquivo} type="file" accept=".geojson,application/geo+json" hidden aria-label="Escolher mapa GeoJSON" onChange={e=>{receber(e.target.files?.[0]);e.currentTarget.value='';}}/>
      {ocupado?<div role="status" className="atividade"><span className="girando"/>{atividade}…</div>:null}
      {erro?<div role="alert" className="erro erro-principal">{erro}</div>:null}
    </main>
    <footer className="rodape"><span>Desenvolvido por Rafael Inácio Silva · MVP · 2026</span><span>Dados: fontes públicas</span></footer>
    {modal&&estudo?<Prioridades estudo={estudo} concluir={aceitar} fechar={()=>setModal(false)}/>:null}
  </>;
}
