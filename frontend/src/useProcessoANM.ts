import {useCallback, useEffect, useRef, useState} from 'react';
import {requisitar} from './api.ts';
import type {EstadoANM, ProcessoANM} from './tipos.ts';

const VAZIO: EstadoANM = {dados: null, carregando: false, erro: ''};

/** Consulta apenas os atributos do cartão, cancelando respostas de outra seleção. */
export function useProcessoANM(minaId: string | undefined) {
  const [estado, setEstado] = useState<EstadoANM & {id?: string}>(VAZIO);
  const atual = useRef(estado);
  const pendente = useRef<{id: string; controle: AbortController; promessa: Promise<ProcessoANM>} | null>(null);
  function atualizar(valor: EstadoANM & {id?: string}) {atual.current = valor; setEstado(valor);}

  const carregar = useCallback((renovar = false): Promise<ProcessoANM> => {
    if (!minaId) return Promise.reject(new Error('Selecione uma mina.'));
    if (pendente.current?.id === minaId) return pendente.current.promessa;
    if (!renovar && atual.current.id === minaId && atual.current.dados) return Promise.resolve(atual.current.dados);
    pendente.current?.controle.abort();
    const controle = new AbortController();
    atualizar({id: minaId, dados: null, carregando: true, erro: ''});
    const promessa = requisitar<ProcessoANM>(`/api/minas/${encodeURIComponent(minaId)}/processo-anm`, controle.signal).then(dados => {
      if (controle.signal.aborted) throw new Error('Consulta cancelada.');
      atualizar({id: minaId, dados, carregando: false, erro: ''});
      return dados;
    }).catch(falha => {
      if (!controle.signal.aborted) atualizar({id: minaId, dados: null, carregando: false, erro: falha instanceof Error ? falha.message : 'ANM indisponível.'});
      throw falha;
    }).finally(() => {if (pendente.current?.controle === controle) pendente.current = null;});
    pendente.current = {id: minaId, controle, promessa};
    return promessa;
  }, [minaId]);

  useEffect(() => {
    if (!minaId) {atual.current = VAZIO; setEstado(VAZIO); return;}
    void carregar().catch(() => {});
    return () => {
      if (pendente.current?.id === minaId) {pendente.current.controle.abort(); pendente.current = null;}
    };
  }, [minaId, carregar]);

  return {estado: estado.id === minaId ? estado : VAZIO, recarregar: () => {void carregar(true).catch(() => {});}};
}
