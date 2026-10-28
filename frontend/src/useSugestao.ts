import {useCallback, useEffect, useState} from 'react';
import {requisitar} from './api.ts';
import type {ExplicacaoSugestao, SugestaoUso} from './tipos.ts';

/** Lê a sugestão da mina no modo sugestão, recalcula quando os pesos param de mudar e depois busca a explicação por IA dos mesmos pesos. */
export function useSugestao(minaId: string | undefined, ativo: boolean, pesos: number[] | null) {
  const [sugestao, setSugestao] = useState<SugestaoUso | null>(null);
  const [erro, setErro] = useState('');
  const [carregando, setCarregando] = useState(false);
  const [explicacao, setExplicacao] = useState<ExplicacaoSugestao | null>(null);
  const [explicando, setExplicando] = useState(false);
  const [tentativa, setTentativa] = useState(0);

  useEffect(() => {setSugestao(null); setExplicacao(null);}, [minaId]);

  useEffect(() => {
    if (!ativo || !minaId) return;
    const controle = new AbortController();
    setCarregando(true);
    setErro('');
    setExplicacao(null);
    setExplicando(false);
    // Espera o engenheiro parar de arrastar antes de recalcular.
    const prazo = setTimeout(() => {
      const consulta = pesos ? `?pesos=${pesos.join(',')}` : '';
      void requisitar<SugestaoUso>(`/api/minas/${encodeURIComponent(minaId)}/sugestao${consulta}`, controle.signal).then(dados => {
        if (controle.signal.aborted) return;
        setSugestao(dados);
        setCarregando(false);
        // A explicação por IA leva segundos: a tela já mostra a das regras e troca quando esta chegar.
        setExplicando(true);
        return requisitar<ExplicacaoSugestao>(`/api/minas/${encodeURIComponent(minaId)}/sugestao/explicacao${consulta}`, controle.signal, 90000).then(texto => {
          if (controle.signal.aborted) return;
          setExplicacao(texto);
          setExplicando(false);
        }, () => {if (!controle.signal.aborted) setExplicando(false);});
      }).catch(falha => {
        if (controle.signal.aborted) return;
        setErro(falha.message);
        setCarregando(false);
      });
    }, 350);
    return () => {clearTimeout(prazo); controle.abort();};
  }, [ativo, minaId, pesos, tentativa]);

  const recarregar = useCallback(() => setTentativa(v => v + 1), []);
  return {sugestao, erro, carregando, recarregar, explicacao, explicando};
}
