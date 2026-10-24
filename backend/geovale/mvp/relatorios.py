"""Relatórios simples e técnico autossuficientes, derivados da mesma revisão salva."""
from pathlib import Path
from io import BytesIO
from threading import Lock
import base64,json
from jinja2 import Environment,BaseLoader,select_autoescape
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.image import imread
from pyproj import Transformer
from shapely import transform
from shapely.geometry import shape
from geovale.decisao.territorio import carregar_caso
from geovale.decisao.metodos import ErroDecisao

TRAVA_MAPA=Lock()
ESTILO='''body{font:16px/1.6 system-ui,sans-serif;color:#183e34;background:#f4f5f0;margin:0}main{max-width:1040px;margin:auto;padding:42px 28px}header{border-bottom:2px solid #184e3d;padding-bottom:20px}h1{font-size:32px;margin:8px 0}h2{font-size:21px;margin-top:32px}h3{font-size:17px}small,.muted{color:#59685f}.marca{font-weight:800;letter-spacing:.04em}.aviso{background:#f5eedc;padding:16px;border-radius:10px;color:#5e4b22}.cartao{background:white;border:1px solid #dce3d7;border-radius:14px;padding:22px;margin-top:20px}img{max-width:100%;border-radius:10px}table{width:100%;border-collapse:collapse}th,td{padding:12px;text-align:left;border-bottom:1px solid #e1e5db}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:12px;color:#31453b}a{color:#215c43}footer{margin-top:32px;font-size:13px;color:#667066}@media print{body{background:white}main{padding:0}section{break-inside:avoid}pre{font-size:10px}a{color:inherit}}'''
MODELO='''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>GeoVale — {{ u.nome }} — {{ tipo }}</title><style>{{ estilo }}</style><main>
<header><div class="marca">GEOVALE</div><h1>{{ u.nome }}</h1><p>{{ u.localizacao }} · Relatório {{ tipo }} · Revisão {{ revisao }}</p><small>Resultado calculado em {{ r.resultado.calculado_em }}. Ambos os relatórios usam a mesma revisão salva.</small></header>
<p class="aviso"><strong>Comparação preliminar para orientar estudos.</strong> {{ u.aviso }} Perfil exploratório: regras ainda sem validação de especialistas.</p>
<section class="cartao"><h2>Área analisada</h2><img alt="Contorno da área sobre imagem aérea pública" src="data:image/png;base64,{{ mapa }}"><p class="muted">{{ r.analise.fontes.credito_imagem }} · Imagem de visualização, sem equivalência a levantamento de campo.</p><p><strong>{{ '%.2f'|format(u.area_ha) }} hectares</strong> · {{ u.numero_partes }} parte(s) do contorno.</p><table><tr><th>Declividade mediana</th><td>{{ '%.2f'|format(u.resumo.declividade_mediana_graus) }}°</td></tr><tr><th>Declividade P90</th><td>{{ '%.2f'|format(u.resumo.declividade_p90_graus) }}°</td></tr><tr><th>Cobertura predominante</th><td>{{ u.resumo.cobertura_predominante }} — {{ u.resumo.ano_cobertura }}</td></tr></table></section>
<section class="cartao"><h2>Prioridade relativa entre as opções</h2><p>{{ r.resultado.alcance }}</p><table><tr><th>Posição</th><th>Alternativa</th><th>Índice TOPSIS</th></tr>{% for a in u.resultado.ranking %}<tr><td>{{ a.posicao }}</td><td>{{ a.nome }}</td><td>{{ '%.4f'|format(a.indice) }}</td></tr>{% endfor %}</table><p>Índice entre 0 e 1, relativo às opções e aos critérios desta análise. Não é probabilidade, percentual de aptidão ou previsão de sucesso.</p>{% if u.resultado.sem_discriminacao %}<p>Os indicadores e pesos não distinguiram as alternativas.</p>{% endif %}<p>{% if u.resultado.sensivel_aos_pesos %}A liderança mudou em pelo menos um ajuste de dez pontos percentuais dos pesos; a conclusão é sensível às prioridades.{% else %}A liderança permaneceu nos ajustes de dez pontos percentuais testados. Isso não é garantia de validade técnica.{% endif %}</p></section>
<section class="cartao"><h2>Prioridades utilizadas</h2><table><tr><th>Critério</th><th>Peso</th></tr>{% for c in u.criterios %}<tr><td>{{ c.nome }}</td><td>{{ '%.2f'|format(u.pesos[loop.index0]) }}%</td></tr>{% endfor %}</table><p>Origem: {{ origem }}. Pesos refletem prioridades, não a existência de um parecer especializado.</p></section>
<section class="cartao"><h2>O que ainda precisa ser avaliado</h2><ul>{% for p in u.resumo.pendencias %}<li>{{ p }}</li>{% endfor %}</ul><p>O mapa é real e os indicadores foram calculados das fontes preparadas. As associações de classes e as curvas de relevo são hipóteses exploratórias documentadas; não são critérios aprovados pela mineradora.</p></section>
{% if tipo=='técnico' %}<section><h2>Fundamentos, critérios e regras</h2><p>AHP por autovetor principal; TOPSIS com normalização vetorial. Referências fundamentam a família do método, não os parâmetros locais.</p><ul>{% for f in referencias %}<li><a href="{{ f.url }}">{{ f.nome }}</a></li>{% endfor %}</ul><h3>Matriz de indicadores calculados, escala 0–100</h3><table><tr><th>Alternativa</th>{% for c in u.criterios %}<th>{{ c.nome }}</th>{% endfor %}</tr>{% for a in r.analise.alternativas %}<tr><td>{{ a.nome }}</td>{% for n in r.analise.matriz[loop.index0] %}<td>{{ '%.6f'|format(n) }}</td>{% endfor %}</tr>{% endfor %}</table><h3>Regras e hipóteses</h3><pre>{{ json(r.analise.regras) }}</pre><h3>Comparações AHP e consistência</h3><pre>{{ json(r.ahp) }}</pre><h3>Cálculo TOPSIS completo</h3><pre>{{ json(r.resultado.calculo) }}</pre><h3>Sensibilidade dos pesos</h3><pre>{{ json(r.resultado.sensibilidade) }}</pre><h3>Relevo, cobertura e qualidade</h3><pre>{{ json(r.analise.relevo) }}</pre><pre>{{ json(r.analise.cobertura) }}</pre><h3>Triagem e limitações</h3><pre>{{ json(r.analise.triagem) }}</pre><pre>{{ json(r.analise.limitacoes) }}</pre><h3>Fontes, coleta e integridade</h3><pre>{{ json(r.analise.fontes) }}</pre><h3>Entrada e versão</h3><pre>{{ json({'sha256_entrada':r.entrada.sha256_entrada,'arquivo':r.entrada.arquivo,'epsg_medida':r.entrada.epsg_medida,'versao':r.versao,'versao_perfil':r.versao_perfil,'geometria':r.entrada.geometria}) }}</pre></section>{% endif %}
<footer>GeoVale · Apoio à decisão com dados públicos e métodos rastreáveis · Gerador HTML 2.0 · Sem recalcular a análise durante a exportação.</footer></main></html>'''
REFERENCIAS=[{'nome':'Singh et al. (2024) — AHP/TOPSIS em usos pós-mineração','url':'https://doi.org/10.3389/feart.2024.1330217'},
 {'nome':'CRC TiME / enviroMETS (2026) — PMLU Options Assessment Tool','url':'https://crctime.com.au/crcwp/wp-content/uploads/2026/06/PMLU-Project-Report.pdf'},
 {'nome':'Worden et al. (2024) — avaliação regional de usos pós-mineração','url':'https://doi.org/10.1016/j.resourpol.2024.104680'},
 {'nome':'USGS — Annual NLCD, documentação dos dados','url':'https://www.usgs.gov/centers/eros/science/annual-nlcd-data-access'}]


def desenhar_mapa(retrato:dict,dados:Path) -> str:
    """Desenha o mesmo contorno sobre a imagem local em Web Mercator, com recortes internos preservados."""
    e=retrato['entrada'];fontes=retrato['analise']['fontes']
    manifesto=carregar_caso(e['caso'],dados)
    if manifesto['sha256']!=fontes['sha256']:
        raise ErroDecisao('As fontes atuais diferem da revisão salva. Restaure o pacote original para gerar o relatório.')
    with TRAVA_MAPA:
        figura=Figure(figsize=(10,6),dpi=120);eixo=figura.subplots()
        img=imread(dados/e['caso']/'imagem.jpg')
        x0,y0,x1,y1=fontes['imagem_extent_3857']
        eixo.imshow(img,extent=[x0,x1,y0,y1],origin='upper')
        t=Transformer.from_crs(4326,3857,always_xy=True)
        g=transform(shape(e['geometria']),t.transform,interleaved=False)
        partes=list(g.geoms) if g.geom_type=='MultiPolygon' else [g]
        for parte in partes:
            for anel in [parte.exterior,*parte.interiors]:
                x,y=anel.xy;eixo.plot(x,y,color='white',linewidth=3.5);eixo.plot(x,y,color='#b6ec68',linewidth=1.8)
        eixo.set_xlim(x0,x1);eixo.set_ylim(y0,y1);eixo.set_aspect('equal');eixo.set_axis_off();figura.tight_layout(pad=0)
        arquivo=BytesIO();FigureCanvasAgg(figura).print_png(arquivo)
        return base64.b64encode(arquivo.getvalue()).decode()


def gerar_relatorio(retrato:dict,tipo:str,revisao:int,dados:Path) -> bytes:
    """Renderiza somente a revisão persistida; escapa todo texto de entrada e não consulta serviços externos."""
    if tipo not in ('simples','tecnico'):raise ValueError('Relatório inválido')
    if not retrato.get('resultado') or not retrato.get('analise'):raise ValueError('Revisão incompleta')
    ambiente=Environment(loader=BaseLoader(),autoescape=select_autoescape(default=True))
    origem={'manual_usuario':'Ajuste manual do usuário','ahp_usuario':'Comparações AHP informadas pelo usuário','ahp_neutro':'AHP neutro de demonstração, sem julgamento de especialista'}[retrato['origem_pesos']]
    return ambiente.from_string(MODELO).render(r=retrato,u=retrato['resumo_publico'],tipo='técnico' if tipo=='tecnico' else 'simples',
        revisao=revisao,estilo=ESTILO,mapa=desenhar_mapa(retrato,dados),origem=origem,referencias=REFERENCIAS,
        json=lambda v:json.dumps(v,ensure_ascii=False,indent=2,allow_nan=False)).encode()
