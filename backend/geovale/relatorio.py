"""Relatório GeoVale em PDF: território observado e cenário técnico fictício separados."""
import hashlib
import json
from datetime import datetime
from io import BytesIO
from pathlib import Path
from threading import Lock
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor
import math
import pypdfium2 as pdfium
from geovale.mapa_relatorio import MapaTerritorial
from geovale.fichas import PARAMETROS_AGUA, formato, ha, montar_fichas, preparar, projetar
from geovale.comentarios import Comentarista
from geovale.multicriterio import SugestoesUso, USOS, entrada_ia, nome_setor, resumo_pesos, texto_setor
from xml.sax.saxutils import escape
from zoneinfo import ZoneInfo

import reportlab
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Flowable, LongTable, PageBreak, Paragraph,
                               SimpleDocTemplate, Spacer, TableStyle)

VERDE = colors.HexColor('#00594f')
TURQUESA = colors.HexColor('#008477')
AMARELO = colors.HexColor('#ffc329')
CINZA = colors.HexColor('#536d64')
CLARO = colors.HexColor('#edf4ef')
LARGURA = A4[0] - 84
FONTE = Path(reportlab.__file__).parent / 'fonts'
for nome, arquivo in [('GeoRegular', 'Vera.ttf'), ('GeoNegrito', 'VeraBd.ttf'), ('GeoItalico', 'VeraIt.ttf')]:
    pdfmetrics.registerFont(TTFont(nome, str(FONTE / arquivo)))
pdfmetrics.registerFontFamily('GeoRegular', normal='GeoRegular', bold='GeoNegrito', italic='GeoItalico', boldItalic='GeoNegrito')
ESTILOS = {
    'texto': ParagraphStyle('texto', fontName='GeoRegular', fontSize=9, leading=14, textColor=VERDE, spaceAfter=9),
    'secao': ParagraphStyle('secao', fontName='GeoNegrito', fontSize=15, leading=21, textColor=VERDE, spaceAfter=12, keepWithNext=True),
    'pequeno': ParagraphStyle('pequeno', fontName='GeoRegular', fontSize=7.7, leading=11, textColor=CINZA, spaceAfter=7),
    'celula': ParagraphStyle('celula', fontName='GeoRegular', fontSize=7.5, leading=11, textColor=VERDE),
    'cabecalho': ParagraphStyle('cabecalho', fontName='GeoNegrito', fontSize=8, leading=12, textColor=colors.white),
}


def texto(valor):
    """Escapa conteúdo publicado antes de inseri-lo na marcação de parágrafos do PDF."""
    return escape(str(valor).replace('—', '-').replace('–', '-').replace('‑', '-'))


def paragrafo(valor, estilo='texto'):
    """Cria texto legível sem interpretar HTML vindo das fontes geográficas."""
    return Paragraph(texto(valor), ESTILOS[estilo])


def data_local(valor):
    """Apresenta a consulta e emissão no fuso de São Paulo, separadas das datas de levantamento."""
    return datetime.fromisoformat(valor).astimezone(ZoneInfo('America/Sao_Paulo')).strftime('%d/%m/%Y %H:%M')


def tabela(cabecalho, linhas, larguras=None):
    """Repete cabeçalho e quebra tabelas longas entre páginas sem cortar texto das células."""
    dados = [[paragrafo(v, 'cabecalho') for v in cabecalho]]
    dados += [[v if isinstance(v, Flowable) else paragrafo(v, 'celula') for v in linha] for linha in linhas]
    t = LongTable(dados, colWidths=larguras or [LARGURA / len(cabecalho)] * len(cabecalho), repeatRows=1, hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), VERDE), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, CLARO]),
        ('LINEBELOW', (0, 0), (-1, 0), 2, AMARELO),
        ('LINEBELOW', (0, 1), (-1, -1), .35, colors.HexColor('#d9e4dc')),
        ('LEFTPADDING', (0, 0), (-1, -1), 8), ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8), ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    return t


def logo(tela, x, y, escala=1):
    """Reproduz em vetor o símbolo e a marca GeoVale usados no frontend."""
    tela.saveState()
    tela.translate(x, y)
    tela.scale(escala, escala)
    tela.setStrokeColor(colors.HexColor('#70b3a5'))
    tela.setLineWidth(1)
    tela.roundRect(1, 1, 38, 38, 10, fill=0, stroke=1)
    caminho = tela.beginPath()
    caminho.moveTo(9, 12)
    for a, b in [(17, 28), (23, 18), (28, 25), (33, 12), (9, 12)]: caminho.lineTo(a, b)
    tela.setStrokeColor(AMARELO)
    tela.setLineWidth(2)
    tela.drawPath(caminho, stroke=1)
    tela.setFillColor(colors.white)
    tela.setFont('GeoNegrito', 24)
    tela.drawString(49, 10, 'GeoVale')
    tela.restoreState()


TRAVA_PDFIUM = Lock()


def ler_cenario(raiz, mina_id):
    """Valida os dados fictícios, seus pontos e referências, e a ligação explícita com a mina e fonte metodológica."""
    c=json.loads((Path(raiz)/'dados/cenarios'/f'{mina_id}.json').read_text())
    agua=c.get('agua',[])
    if c['mina_id']!=mina_id or c['natureza']!='simulado' or not c['referencia']['secoes'] or not 1<=len(c['dados'])+len(agua)<=20:
        raise ValueError('Cenário técnico inválido')
    ids=[d['id'] for d in c['dados']+agua]
    if len(set(ids))!=len(ids):raise ValueError('Dados duplicados')
    def numero(v):return not isinstance(v,bool) and isinstance(v,(int,float)) and math.isfinite(v)
    def ponto(d):
        p=d.get('ponto')
        return p is None or (isinstance(p,list) and len(p)==2 and all(numero(v) for v in p) and -180<=p[0]<=180 and -90<=p[1]<=90
                             and isinstance(d.get('rotulo'),str) and 1<=len(d['rotulo'])<=3)
    for d in c['dados']:
        if not all(isinstance(d.get(k),str) and d[k] for k in ('id','nome','unidade','metodo','comentario')) or not ponto(d):
            raise ValueError('Dado incompleto')
        if not numero(d['valor']):
            raise ValueError('Valor fictício inválido')
        ref=d.get('referencia_tecnica')
        if ref is not None and not (isinstance(ref.get('texto'),str) and len({'minimo','maximo'}&set(ref))==1 and numero(ref.get('minimo',ref.get('maximo')))):
            raise ValueError('Referência técnica inválida')
    for a in agua:
        if (not all(isinstance(a.get(k),str) and a[k] for k in ('id','nome','metodo','rotulo')) or a.get('ponto') is None or not ponto(a)
                or not a.get('parametros') or not set(a['parametros'])<=set(PARAMETROS_AGUA) or not all(numero(v) for v in a['parametros'].values())):
            raise ValueError('Ponto de água inválido')
    return c


class DocumentoPDF(SimpleDocTemplate):
    """Acrescenta marcadores de navegação às fichas do relatório."""
    def afterFlowable(self, elemento):
        if isinstance(elemento, Paragraph) and elemento.style.name=='secao':
            chave='secao-'+hashlib.sha256(elemento.getPlainText().encode()).hexdigest()[:12]
            self.canv.bookmarkPage(chave);self.canv.addOutlineEntry(elemento.getPlainText(),chave,level=0)


def gerar_pdf(dados,cenario,fichas,comentarios,sugestao=None,explicacoes=None):
    """Relatório simples: mapa, fatos e leitura contextual em campos separados."""
    destino=BytesIO();mina=dados['mina']
    doc=DocumentoPDF(destino,pagesize=A4,leftMargin=42,rightMargin=42,topMargin=91,bottomMargin=43,
                     title=f'GeoVale - Fichas territoriais - {mina["nome"]}',author='GeoVale')
    elementos=[]
    def adicionar(*itens):elementos.extend(itens)
    def fatos(ficha):
        linhas=[]
        for d in ficha['dados']:
            bruto=Paragraph('<b>'+texto(d['nome'])+'</b><br/>'+texto(d['valor']).replace('\n','<br/>')+'<br/><font size="6.7" color="#536d64">'+texto(d['origem'])+'</font>',ESTILOS['celula'])
            linhas.append([bruto,paragrafo(comentarios['comentarios'][d['id']],'celula')])
        leitura='Leitura contextual (IA)' if ficha['id'] in comentarios['ia'] else 'Leitura contextual'
        tab=tabela(['Dado / valor / origem',leitura],linhas,[LARGURA*.48,LARGURA*.52])
        tab.setStyle(TableStyle([('TOPPADDING',(0,1),(-1,-1),6),('BOTTOMPADDING',(0,1),(-1,-1),6)]))
        adicionar(tab)
    minerada=dados.get('area_minerada')
    cava=projetar(next(f['geometry'] for f in dados['influencia']['features'] if f['properties']['id']=='mina')).area/1e4
    if minerada:
        alvo=(f"<b>Área minerada no recorte: {texto(ha(minerada['ha']))} ({texto(formato(minerada['ha']*100/dados['recorte_ha'],1))}%)</b>, "
              f"delimitada pela classe Mineração de {texto(minerada['fonte'])}. A mina OSM ({texto(ha(cava))}) representa só a cava. "
              'As fichas separam área minerada e entorno; o recorte AII é contexto.')
    else:
        alvo='Área minerada não identificada na cobertura; as fichas descrevem o recorte inteiro.'
    adicionar(paragrafo('Visão geral | '+mina['nome'],'secao'),
              paragrafo(f'{mina["municipio"]}/{mina["uf"]} | '+data_local(dados['gerado_em']),'pequeno'),
              MapaTerritorial(dados,altura=170),Spacer(1,6),Paragraph(alvo,ESTILOS['texto']))
    resumos=[[ficha['nome'],' | '.join(d['resumo'] for d in ficha['dados'] if d.get('resumo'))] for ficha in fichas[:-1]]
    resumos.append(['Dados simulados *','; '.join(d['resumo'] for d in fichas[-1]['dados'] if d.get('resumo'))])
    if sugestao:
        resumos.append(['Sugestão multicritério','; '.join(f"{s['id']} ({ha(s['ha'])}): {s['ranking'][0]['nome']} {formato(s['ranking'][0]['nota'])}" for s in sugestao['setores'])])
    resumo=tabela(['Tema','Dados objetivos do território'],resumos,[LARGURA*.24,LARGURA*.76])
    resumo.setStyle(TableStyle([('TOPPADDING',(0,1),(-1,-1),5),('BOTTOMPADDING',(0,1),(-1,-1),5)]))
    adicionar(resumo,Spacer(1,6),
              paragrafo(cenario['descricao'],'pequeno'),
              paragrafo('Recorte comum aproximado da AII águas/solos (FEAM, Figura 2.3), usado como contexto; não define área de intervenção ou fechamento. A leitura contextual indica implicações para o planejamento sem alterar valores; a sugestão multicritério ordena usos para discussão, sem decidir.','pequeno'))
    alturas={'vegetacao':190,'agua':180,'barragens':180}
    for i,ficha in enumerate(fichas,1):
        adicionar(PageBreak(),paragrafo(f'{i:02d} | '+ficha['nome'],'secao'))
        if ficha['id']!='tecnicos':
            adicionar(MapaTerritorial(dados,tema=ficha['id'],altura=alturas.get(ficha['id'],250)),Spacer(1,9))
        else:
            adicionar(MapaTerritorial(dados,tema='tecnicos',altura=230,pontos=[(d['rotulo'],*d['ponto']) for d in ficha['dados'] if d.get('ponto')]),
                      Spacer(1,8),paragrafo(cenario['descricao'],'pequeno'))
        fatos(ficha)
        adicionar(Spacer(1,8))
        if ficha['bases']:
            fontes=[]
            for b in ficha['bases']:
                fontes.append('<link href="'+texto(b['base']['metadado'])+'" color="#008477">'+texto(b['base']['nome'])+'</link> ('+texto(data_local(b['consultado_em']))+')')
            adicionar(Paragraph('Fontes: '+'; '.join(fontes)+'.',ESTILOS['pequeno']))
            adicionar(paragrafo('Mapa: cores oficiais dos rasters; geometrias recortadas. Área minerada: classe Mineração do MapBiomas. Mina: © OpenStreetMap contributors, ODbL; influência: FEAM / Amplo.','pequeno'))
        else:
            ref=cenario['referencia']
            adicionar(Paragraph('Referência de estrutura: <link href="'+texto(ref['url'])+'" color="#008477">'+texto(ref['instituicao']+' - '+ref['titulo'])+'</link>, '+texto(ref['revisao'])+'. Seções '+texto(ref['secoes'])+'. Os valores com * foram criados no GeoVale. Limites de água: Resolução CONAMA 357/2005; classe do trecho: enquadramento publicado pelo Igam (dado real).',ESTILOS['pequeno']))
    if sugestao:
        cores={u['id']:u['cor'] for u in USOS}
        adicionar(PageBreak(),paragrafo(f'{len(fichas)+1:02d} | Sugestão multicritério','secao'),
                  MapaTerritorial(dados,tema='sugestao',altura=220,setores=[(s['id'],s['geometria'],cores[s['ranking'][0]['uso']]) for s in sugestao['setores']]),Spacer(1,8),
                  paragrafo(f"Sugestão para discussão, não decisão. Setores são partes contínuas da área minerada com pelo menos {sugestao['minimo_ha']} ha "
                            f"({ha(sugestao['fora_ha'])} em fragmentos menores ficaram fora). Restrições legais excluem usos; cada critério vira nota de 0 a 1 e "
                            f"entra na soma com o peso abaixo. Pesos {'calculados por AHP' if sugestao['origem_pesos']=='AHP' else 'ajustados pelo engenheiro'} "
                            f"(razão de consistência da matriz padrão: {formato(sugestao['razao_consistencia'],3)}): {resumo_pesos(sugestao)}.",'pequeno'))
        linhas=[]
        for s in sugestao['setores']:
            condicoes=[f"Robustez: {'estável' if s['robustez']['estavel'] else 'sensível'} com ±{round(sugestao['variacao']*100)}% nos pesos"]
            if s['cavidades']>=1:condicoes.append(f"cavidades com potencial alto: {formato(s['cavidades'])}%")
            if s['montante']:condicoes.append('barragem a montante')
            bruto=Paragraph('<b>'+texto(nome_setor(s))+'</b><br/>'+texto(texto_setor(s)).replace('\n','<br/>')+'<br/><font size="6.7" color="#536d64">'+texto('; '.join(condicoes))+'</font>',ESTILOS['celula'])
            linhas.append([bruto,paragrafo(explicacoes['textos'][s['id']],'celula')])
        tab=tabela(['Setor e notas (0 a 100)','Por que (IA)' if explicacoes['metodo']=='ia' else 'Por que'],linhas,[LARGURA*.46,LARGURA*.54])
        tab.setStyle(TableStyle([('TOPPADDING',(0,1),(-1,-1),6),('BOTTOMPADDING',(0,1),(-1,-1),6)]))
        adicionar(tab,Spacer(1,8),
                  paragrafo('Restrições: '+'; '.join(f"{r['nome']} admite {', '.join(n['nome'].lower() for n in USOS if n['id'] in r['permite'])} ({r['base']})" for r in sugestao['restricoes'])+'.','pequeno'),
                  paragrafo('Relevo da Topodata (SRTM, 2000): dentro da área minerada não representa a cava atual; substituir por levantamento topográfico atual. Métodos e evidências em docs/MULTICRITERIO.md.','pequeno'))
    def pagina(tela,d):
        tela.saveState();tela.setFillColor(VERDE);tela.rect(0,A4[1]-70,A4[0],70,fill=1,stroke=0);logo(tela,40,A4[1]-57,.9)
        tela.setFillColor(AMARELO);tela.rect(0,A4[1]-73,A4[0],3,fill=1,stroke=0)
        tela.setFont('GeoRegular',7);tela.setFillColor(CINZA);tela.drawString(42,25,'GeoVale | Dados, contexto e cenário simulado');tela.drawRightString(A4[0]-42,25,str(d.page));tela.restoreState()
    doc.build(elementos,onFirstPage=pagina,onLaterPages=pagina)
    return destino.getvalue()


class RelatoriosPDF:
    """PDF e prévia por versão: o navegador exibe páginas prontas do mesmo documento baixável."""
    def __init__(self,fonte,raiz,comentarista=None,sugestoes=None):
        self.fonte,self.raiz=fonte,raiz;self.cache={};self.documentos=OrderedDict();self.imagens=OrderedDict();self.manifestos={}
        self.trava=Lock();self.comentarista=comentarista or Comentarista(raiz=raiz);self.sugestoes=sugestoes or SugestoesUso(fonte)

    def obter(self,mina_id,pesos=None):
        """Atualiza fatos por coleta/cenário/pesos e explicações por modelo, sem reextrair fontes."""
        dados=self.fonte.relatorio(mina_id);cenario=ler_cenario(self.raiz,mina_id)
        chave=hashlib.sha256(json.dumps({'dados':{k:v for k,v in dados.items() if k!='gerado_em'},'cenario':cenario,'modelo':'4.5.0',
                                         'pesos':None if pesos is None else [round(float(p),6) for p in pesos],'comentarios':self.comentarista.assinatura},sort_keys=True,ensure_ascii=False).encode()).hexdigest()
        with self.trava:
            anterior=self.cache.get(mina_id)
            if anterior and anterior[0]==chave:return anterior[1]
            dados['rasters']={b['base']['id']:self.fonte.arquivo(mina_id,b['base']['id']) for b in dados['bases'] if b['tipo']=='raster'}
            fichas=montar_fichas(preparar(dados),cenario)
            sugestao=self.sugestoes.obter(mina_id,pesos,dados) if dados.get('area_minerada') else None
            # Fichas e sugestão vão ao modelo ao mesmo tempo: a espera é a da chamada mais lenta.
            with ThreadPoolExecutor(max_workers=2) as execucao:
                lendo=execucao.submit(self.comentarista.gerar,fichas)
                explicando=execucao.submit(self.comentarista.explicar,entrada_ia(sugestao),{s['id']:s['explicacao'] for s in sugestao['setores']}) if sugestao else None
                comentarios=lendo.result();explicacoes=explicando.result() if explicando else None
            pdf=gerar_pdf(dados,cenario,fichas,comentarios,sugestao,explicacoes);versao=hashlib.sha256(pdf).hexdigest()
            self.cache[mina_id]=(chave,pdf);self.documentos[(mina_id,versao)]=pdf
            while len(self.documentos)>4:
                removido,_=self.documentos.popitem(last=False);self.manifestos.pop(removido,None)
            return pdf

    def descrever(self,mina_id,versao):
        """Obtém texto acessível de cada página com uso serializado e fechamento explícito do PDFium."""
        with self.trava:
            chave=(mina_id,versao)
            if chave not in self.documentos:raise ValueError('Versão do relatório expirada')
            if chave in self.manifestos:return self.manifestos[chave]
            with TRAVA_PDFIUM:
                with pdfium.PdfDocument(self.documentos[chave]) as doc:
                    paginas=[]
                    for n in range(len(doc)):
                        pg=doc[n];texto_pg=pg.get_textpage()
                        try:paginas.append({'numero':n+1,'texto':texto_pg.get_text_bounded()})
                        finally:texto_pg.close();pg.close()
            saida={'versao':versao,'paginas':paginas};self.manifestos[chave]=saida;return saida

    def pagina(self,mina_id,versao,numero):
        """Renderiza PNG somente da página pedida; cache limitado a doze imagens e escala fixa."""
        with self.trava:
            chave=(mina_id,versao);imagem=(*chave,numero)
            if chave not in self.documentos:raise ValueError('Versão do relatório expirada')
            if imagem in self.imagens:
                self.imagens.move_to_end(imagem);return self.imagens[imagem]
            with TRAVA_PDFIUM:
                with pdfium.PdfDocument(self.documentos[chave]) as doc:
                    if not 1<=numero<=len(doc):raise IndexError('Página inexistente')
                    pg=doc[numero-1]
                    try:
                        bitmap=pg.render(scale=1.7)
                        try:
                            im=bitmap.to_pil();saida=BytesIO();im.save(saida,format='PNG');im.close();bruto=saida.getvalue()
                        finally:bitmap.close()
                    finally:pg.close()
            self.imagens[imagem]=bruto
            while len(self.imagens)>12:self.imagens.popitem(last=False)
            return bruto
