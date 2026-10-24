import {useEffect,useRef,useState} from 'react';
import type {Estudo} from './tipos.ts';
import {operar} from './api.ts';
const PARES=[[0,1],[0,2],[1,2]] as const;

/** Coleta três julgamentos AHP numa ação opcional, fora da tela principal. */
export default function Prioridades({estudo,concluir,fechar}:{estudo:Estudo; concluir:(e:Estudo)=>void; fechar:()=>void}) {
  const dialogo=useRef<HTMLDialogElement>(null);
  const [pares,setPares]=useState([1,1,1]);const [erro,setErro]=useState('');const [ocupado,setOcupado]=useState(false);
  useEffect(()=>{const d=dialogo.current;d?.showModal();return ()=>d?.close();},[]);
  /** Deixa a consistência matemática e a gravação dos pesos sob responsabilidade da API. */
  async function confirmar(){
    setOcupado(true);setErro('');
    try{const novo=await operar(estudo,'prioridades',{comparacoes:pares});concluir(novo);fechar();}
    catch(e){setErro(e instanceof Error?e.message:'Não foi possível calcular as prioridades.');}
    finally{setOcupado(false);}
  }
  return <dialog ref={dialogo} className="dialogo" aria-labelledby="titulo-prioridades" onCancel={e=>{if(ocupado)e.preventDefault();else fechar();}} onClose={fechar}>
    <button type="button" className="fechar-dialogo" onClick={fechar} disabled={ocupado} aria-label="Fechar comparações">×</button>
    <p className="sobretitulo">SUAS PRIORIDADES</p><h2 id="titulo-prioridades">O que importa mais?</h2>
    {PARES.map(([i,j],k)=><label className="par-prioridade" key={`${i}-${j}`}>
      <span>{estudo.criterios[i].nome} <small>em relação a</small> {estudo.criterios[j].nome}</span>
      <select value={pares[k]} disabled={ocupado} onChange={e=>setPares(p=>p.map((v,n)=>n===k?Number(e.target.value):v))}>
        <option value={1}>Mesma importância</option>
        {[3,5,7,9].map(v=><option key={v} value={v}>{estudo.criterios[i].nome}: {v} vezes</option>)}
        {[3,5,7,9].map(v=><option key={`r${v}`} value={1/v}>{estudo.criterios[j].nome}: {v} vezes</option>)}
      </select>
    </label>)}
    {erro?<p role="alert" className="erro">{erro}</p>:null}
    <button type="button" className="botao principal" disabled={ocupado} onClick={confirmar}>{ocupado?'Calculando…':'Aplicar prioridades'}</button>
  </dialog>;
}
