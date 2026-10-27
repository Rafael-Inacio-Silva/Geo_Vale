"""Relatório GeoVale em PDF: território observado e cenário técnico fictício separados."""
import hashlib
import json
from datetime import datetime
from io import BytesIO
from pathlib import Path
from threading import Lock
from collections import OrderedDict
import math
import pypdfium2 as pdfium
from geovale.mapa_relatorio import MapaTerritorial
from geovale.fichas import montar_fichas
from geovale.comentarios import Comentarista
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
    """Valida os dados fictícios e sua ligação explícita com a mina e fonte metodológica."""
    c=json.loads((Path(raiz)/'dados/cenarios'/f'{mina_id}.json').read_text())
    if c['mina_id']!=mina_id or c['natureza']!='simulado' or not c['referencia']['secoes'] or not 1<=len(c['dados'])<=20:
        raise ValueError('Cenário técnico inválido')
    if len({d['id'] for d in c['dados']})!=len(c['dados']):raise ValueError('Dados duplicados')
    for d in c['dados']:
        if not all(isinstance(d[k],str) and d[k] for k in ('id','nome','unidade','metodo','comentario')):
            raise ValueError('Dado incompleto')
        if isinstance(d['valor'],bool) or not isinstance(d['valor'],(int,float)) or not math.isfinite(d['valor']):
            raise ValueError('Valor fictício inválido')
    return c


class DocumentoPDF(SimpleDocTemplate):
    """Acrescenta marcadores de navegação às fichas do relatório."""
    def afterFlowable(self, elemento):
        if isinstance(elemento, Paragraph) and elemento.style.name=='secao':
            chave='secao-'+hashlib.sha256(elemento.getPlainText().encode()).hexdigest()[:12]
            self.canv.bookmarkPage(chave);self.canv.addOutlineEntry(elemento.getPlainText(),chave,level=0)


def gerar_pdf(dados,cenario,fichas,comentarios):
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
        tab=tabela(['Dado / valor / origem','Leitura contextual (separada do dado)'],linhas,[LARGURA*.48,LARGURA*.52])
        tab.setStyle(TableStyle([('TOPPADDING',(0,1),(-1,-1),6),('BOTTOMPADDING',(0,1),(-1,-1),6)]))
        adicionar(tab)
    adicionar(paragrafo('Visão geral | '+mina['nome'],'secao'),
              paragrafo(f'{mina["municipio"]}/{mina["uf"]} | '+data_local(dados['gerado_em']),'pequeno'),
              MapaTerritorial(dados,altura=225),Spacer(1,10))
    resumos=[]
    for ficha in fichas[:-1]:
        itens=ficha['dados'];valor=' | '.join(d['nome']+': '+d['valor'].replace('\n','; ') for d in itens if not d['id'].endswith(('.classes','.nodata')) and d['origem']!='Não medido')
        resumos.append([ficha['nome'],valor])
    resumos.append(['Dados sem camada *','; '.join(d['nome']+': '+d['valor'] for d in fichas[-1]['dados'])])
    resumo=tabela(['Tema','Dados objetivos do território'],resumos,[LARGURA*.24,LARGURA*.76])
    resumo.setStyle(TableStyle([('TOPPADDING',(0,1),(-1,-1),5),('BOTTOMPADDING',(0,1),(-1,-1),5)]))
    adicionar(resumo,Spacer(1,6),
              paragrafo(cenario['descricao'],'pequeno'),
              paragrafo('Recorte comum aproximado da AII águas/solos (FEAM, Figura 2.3). Não define área de intervenção ou fechamento. Os comentários não alteram os valores e não classificam usos futuros.','pequeno'))
    for i,ficha in enumerate(fichas,1):
        adicionar(PageBreak(),paragrafo(f'{i:02d} | '+ficha['nome'],'secao'))
        if ficha['id']!='tecnicos':
            adicionar(MapaTerritorial(dados,tema=ficha['id'],altura=190 if ficha['id']=='vegetacao' else 280 if ficha['id']=='agua' else 250),Spacer(1,9))
        else:adicionar(paragrafo(cenario['descricao'],'pequeno'))
        fatos(ficha)
        adicionar(Spacer(1,8),paragrafo(comentarios['rotulo']+'. Comentários não constituem laudo ou decisão de uso.','pequeno'))
        if ficha['bases']:
            fontes=[]
            for b in ficha['bases']:
                fontes.append('<link href="'+texto(b['base']['metadado'])+'" color="#008477">'+texto(b['base']['nome'])+'</link> ('+texto(data_local(b['consultado_em']))+')')
            adicionar(Paragraph('Fontes: '+'; '.join(fontes)+'.',ESTILOS['pequeno']))
            adicionar(paragrafo('Mapa: cores oficiais dos rasters; geometrias recortadas. Mina: © OpenStreetMap contributors, ODbL; influência: FEAM / Amplo.','pequeno'))
        else:
            ref=cenario['referencia']
            adicionar(Paragraph('Referência de estrutura: <link href="'+texto(ref['url'])+'" color="#008477">'+texto(ref['instituicao']+' - '+ref['titulo'])+'</link>, '+texto(ref['revisao'])+'. Seções '+texto(ref['secoes'])+'. Os valores com * foram criados no GeoVale.',ESTILOS['pequeno']))
    def pagina(tela,d):
        tela.saveState();tela.setFillColor(VERDE);tela.rect(0,A4[1]-70,A4[0],70,fill=1,stroke=0);logo(tela,40,A4[1]-57,.9)
        tela.setFillColor(AMARELO);tela.rect(0,A4[1]-73,A4[0],3,fill=1,stroke=0)
        tela.setFont('GeoRegular',7);tela.setFillColor(CINZA);tela.drawString(42,25,'GeoVale | Dados, contexto e cenário simulado');tela.drawRightString(A4[0]-42,25,str(d.page));tela.restoreState()
    doc.build(elementos,onFirstPage=pagina,onLaterPages=pagina)
    return destino.getvalue()


class RelatoriosPDF:
    """PDF e prévia por versão: o navegador exibe páginas prontas do mesmo documento baixável."""
    def __init__(self,fonte,raiz,comentarista=None):
        self.fonte,self.raiz=fonte,raiz;self.cache={};self.documentos=OrderedDict();self.imagens=OrderedDict();self.manifestos={}
        self.trava=Lock();self.comentarista=comentarista or Comentarista(raiz=raiz)

    def obter(self,mina_id):
        """Atualiza fatos por coleta/cenário e comentários por modelo, sem reextrair fontes."""
        dados=self.fonte.relatorio(mina_id);cenario=ler_cenario(self.raiz,mina_id)
        chave=hashlib.sha256(json.dumps({'dados':{k:v for k,v in dados.items() if k!='gerado_em'},'cenario':cenario,'modelo':'4.2.0','comentarios':self.comentarista.assinatura},sort_keys=True,ensure_ascii=False).encode()).hexdigest()
        with self.trava:
            anterior=self.cache.get(mina_id)
            if anterior and anterior[0]==chave:return anterior[1]
            fichas=montar_fichas(dados,cenario);comentarios=self.comentarista.gerar(fichas)
            dados['rasters']={b['base']['id']:self.fonte.arquivo(mina_id,b['base']['id']) for b in dados['bases'] if b['tipo']=='raster'}
            pdf=gerar_pdf(dados,cenario,fichas,comentarios);versao=hashlib.sha256(pdf).hexdigest()
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
