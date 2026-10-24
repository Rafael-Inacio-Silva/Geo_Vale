"""Orquestra estados e versões sem devolver bastidores na resposta normal da interface."""
from copy import deepcopy
from datetime import datetime,timezone
from geovale.decisao.metodos import ErroDecisao, calcular_ahp, calcular_topsis, analisar_sensibilidade
from geovale.decisao.territorio import CRITERIOS,ALTERNATIVAS,AVISO


def agora() -> str:
    """Registra instante UTC sem confundir coleta da fonte com execução da análise."""
    return datetime.now(timezone.utc).isoformat()


def pesos_exibicao(pesos:list[float]) -> list[float]:
    """Arredonda somente os pesos aceitos para edição em duas casas e preserva soma de 100%."""
    p=[round(float(w)*100,2) for w in pesos]
    p[int(max(range(len(p)),key=p.__getitem__))]=round(p[int(max(range(len(p)),key=p.__getitem__))]+100-sum(p),2)
    return p


def iniciar(entrada:dict,identificador:str,dono:str) -> dict:
    """Cria rascunho de upload; a caracterização só ocorre ao clicar em Analisar área."""
    ahp=calcular_ahp([[1,1,1],[1,1,1],[1,1,1]])
    return {'id':identificador,'dono':dono,'versao':1,'criado_em':agora(),'entrada':entrada,
            'analise':None,'ahp':ahp,'pesos':pesos_exibicao(ahp['pesos']),
            'origem_pesos':'ahp_neutro','resultado':None,'salvo_revisao':None,
            'versao_perfil':'territorial-exploratorio-1.0'}


def conferir_versao(estudo:dict,corpo:dict):
    """Rejeita edição de uma versão anterior sem substituir a análise atual."""
    if type(corpo.get('versao')) is not int or corpo['versao']!=estudo['versao']:
        raise ErroDecisao('A análise mudou. Consulte o resultado atual antes de tentar novamente.')


def registrar_ahp(estudo:dict,corpo:dict):
    """Aceita três comparações recíprocas, confere consistência e invalida resultado dependente."""
    conferir_versao(estudo,corpo)
    if not estudo['analise']:raise ErroDecisao('Analise a área antes de definir prioridades.')
    p=corpo.get('comparacoes')
    if not isinstance(p,list) or len(p)!=3 or any(type(v) not in (int,float) or v<=0 for v in p):
        raise ErroDecisao('Informe as três comparações de prioridade.')
    a,b,c=p
    r=calcular_ahp([[1,a,b],[1/a,1,c],[1/b,1/c,1]])
    if not r['consistente']:raise ErroDecisao('As prioridades estão conflitantes (consistência acima de 10%). Reveja as comparações.')
    estudo.update(ahp=r,pesos=pesos_exibicao(r['pesos']),origem_pesos='ahp_usuario',resultado=None,salvo_revisao=None,versao=estudo['versao']+1)


def comparar(estudo:dict,corpo:dict):
    """Classifica somente indicadores territoriais disponíveis; não libera uso nem produz custo ou parecer."""
    conferir_versao(estudo,corpo)
    a=estudo['analise']
    if not a:raise ErroDecisao('Analise a área antes de comparar as opções.')
    pesos=corpo.get('pesos');origem=corpo.get('origem')
    if origem not in ('ahp','manual'):raise ErroDecisao('Origem dos pesos inválida.')
    if origem=='ahp' and pesos!=estudo['pesos']:raise ErroDecisao('Os pesos diferem das prioridades calculadas. Use ajuste manual ou recalcule as prioridades.')
    r=calcular_topsis(a['matriz'],pesos,['beneficio']*len(CRITERIOS))
    sensibilidade=analisar_sensibilidade(a['matriz'],pesos,['beneficio']*len(CRITERIOS))
    ranking=[]
    for i in r['ordem']:
        alt=ALTERNATIVAS[i]
        maior=max(range(len(CRITERIOS)),key=lambda j:r['ponderada'][i][j])
        ranking.append({'id':alt['id'],'nome':alt['nome'],'posicao':r['posicoes'][i],'indice':r['escores'][i],
                        'explicacao':f'O maior valor na linha normalizada e ponderada desta opção é {CRITERIOS[maior]["nome"].lower()}. A posição depende do conjunto de critérios e pesos.',
                        'descricao':alt['descricao']})
    estudo.update(pesos=list(pesos),origem_pesos=estudo['origem_pesos'] if origem=='ahp' else 'manual_usuario',
                  resultado={'calculado_em':agora(),'ranking':ranking,'calculo':r,'sensibilidade':sensibilidade,
                             'alcance':'Prioridade relativa para estudo territorial, sem avaliação de viabilidade ou segurança.',
                             'aviso':AVISO},salvo_revisao=None,versao=estudo['versao']+1)


def publicar(estudo:dict) -> dict:
    """Expõe apenas mapa, poucas características, prioridades e resultado resumido; mantém matriz e fonte no servidor."""
    e=estudo['entrada'];a=estudo['analise'];r=estudo['resultado']
    resumo=None
    if a:
        resumo={'declividade_mediana_graus':a['relevo']['declividade_mediana_graus'],
                'declividade_p90_graus':a['relevo']['declividade_p90_graus'],
                'cobertura_predominante':a['cobertura_predominante'],
                'ano_cobertura':a['cobertura']['ano'],
                'pendencias':a['triagem']['nao_avaliados']}
    resultado=None if not r else {'ranking':r['ranking'],'alcance':r['alcance'],
                                  'sem_discriminacao':r['calculo']['sem_discriminacao'],
                                  'sensivel_aos_pesos':bool(r['sensibilidade']['mudou_em']),
                                  'calculado_em':r['calculado_em']}
    return {'id':estudo['id'],'versao':estudo['versao'],'nome':e['nome'],'localizacao':e['localizacao'],
            'arquivo':e['arquivo'],'area_ha':e['area_ha'],'numero_partes':e['numero_partes'],
            'geometria':e['geometria'],'bbox':e['bbox'],
            'imagem':{**e['imagem'],'url':f'/api/areas/{estudo["id"]}/imagem'} if e['imagem'] else None,
            'cobertura_disponivel':bool(e['caso']),'analisada':a is not None,'resumo':resumo,
            'criterios':[{k:c[k] for k in ('id','nome','descricao')} for c in CRITERIOS],
            'pesos':estudo['pesos'],'origem_pesos':estudo['origem_pesos'],
            'resultado':resultado,'salvo_revisao':estudo['salvo_revisao'],
            'aviso':AVISO,'perfil':'Exploratório — parâmetros ainda sem validação de especialistas.'}


def retrato(estudo:dict) -> dict:
    """Congela versão exata sem identificador secreto de sessão para gerar ambos os relatórios."""
    copia=deepcopy(estudo)
    copia.pop('dono',None)
    copia['resumo_publico']=publicar(estudo)
    return copia
