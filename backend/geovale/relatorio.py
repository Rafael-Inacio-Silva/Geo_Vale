"""Relatório GeoVale em PDF: território observado e cenário técnico fictício separados."""
import hashlib
import json
from datetime import datetime
from io import BytesIO
from pathlib import Path
from threading import Lock
from xml.sax.saxutils import escape
from zoneinfo import ZoneInfo

import reportlab
from rasterio.warp import transform_geom
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
    'titulo': ParagraphStyle('titulo', fontName='GeoNegrito', fontSize=25, leading=32, textColor=VERDE, spaceAfter=10),
    'subtitulo': ParagraphStyle('subtitulo', fontName='GeoNegrito', fontSize=17, leading=23, textColor=VERDE, spaceAfter=12),
    'secao': ParagraphStyle('secao', fontName='GeoNegrito', fontSize=15, leading=21, textColor=VERDE, spaceAfter=12, keepWithNext=True),
    'grupo': ParagraphStyle('grupo', fontName='GeoNegrito', fontSize=10, leading=15, textColor=TURQUESA, spaceBefore=10, spaceAfter=7, keepWithNext=True),
    'pequeno': ParagraphStyle('pequeno', fontName='GeoRegular', fontSize=7.7, leading=11, textColor=CINZA, spaceAfter=7),
    'celula': ParagraphStyle('celula', fontName='GeoRegular', fontSize=8, leading=12, textColor=VERDE),
    'cabecalho': ParagraphStyle('cabecalho', fontName='GeoNegrito', fontSize=8, leading=12, textColor=colors.white),
    'destaque': ParagraphStyle('destaque', fontName='GeoNegrito', fontSize=10, leading=15, textColor=VERDE, backColor=CLARO, borderPadding=10, spaceAfter=16),
}


def texto(valor):
    """Escapa conteúdo publicado antes de inseri-lo na marcação de parágrafos do PDF."""
    return escape(str(valor).replace('—', '-').replace('–', '-').replace('‑', '-'))


def paragrafo(valor, estilo='texto'):
    """Cria texto legível sem interpretar HTML vindo das fontes geográficas."""
    return Paragraph(texto(valor), ESTILOS[estilo])


def numero(valor, casas=0):
    """Formata contagens e proporções em português sem converter células em área."""
    return f'{valor:,.{casas}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


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


class MapaTerritorial(Flowable):
    """Desenha geometrias persistidas em UTM, sem baixar tiles ou alterar dados de análise."""

    def __init__(self, dados, tema='agua', altura=285):
        super().__init__()
        self.width, self.height = LARGURA, altura
        self.feicoes = [(f['properties']['id'], transform_geom('EPSG:4326', 'EPSG:31983', f['geometry'])) for f in dados['influencia']['features']]
        self.bases = [(b['base']['camada'], [transform_geom('EPSG:4326', 'EPSG:31983', f['geometry']) for f in b['dados']['features']])
                      for b in dados['bases'] if b['tipo'] == 'vetor' and b['base']['tema_id'] == tema]

    def draw(self):
        tela = self.canv
        tela.saveState()
        tela.setFillColor(colors.HexColor('#f3f6f2'))
        tela.roundRect(0, 0, self.width, self.height, 8, fill=1, stroke=0)
        contorno = next(g for k, g in self.feicoes if k == 'influencia')
        def pontos(geom):
            if geom['type'] == 'Polygon': return [p for anel in geom['coordinates'] for p in anel]
            return [p for poligono in geom['coordinates'] for anel in poligono for p in anel]
        ps = pontos(contorno)
        x0, x1 = min(p[0] for p in ps), max(p[0] for p in ps)
        y0, y1 = min(p[1] for p in ps), max(p[1] for p in ps)
        escala = min((self.width - 65) / (x1 - x0), (self.height - 60) / (y1 - y0))
        dx, dy = (self.width - (x1 - x0) * escala) / 2, 36 + (self.height - 60 - (y1 - y0) * escala) / 2
        def caminho(geom):
            p = tela.beginPath()
            tipo, coords = geom['type'], geom['coordinates']
            partes = coords if tipo == 'MultiLineString' else [coords] if tipo == 'LineString' else [a for pol in coords for a in pol] if tipo == 'MultiPolygon' else coords
            for linha in partes:
                for i, ponto in enumerate(linha):
                    x, y = dx + (ponto[0] - x0) * escala, dy + (ponto[1] - y0) * escala
                    if i == 0: p.moveTo(x, y)
                    else: p.lineTo(x, y)
                if 'Polygon' in tipo: p.close()
            return p
        tela.setFillColor(colors.HexColor('#fff0b8'))
        tela.setStrokeColor(AMARELO)
        tela.setLineWidth(1.3)
        tela.drawPath(caminho(contorno), fill=1, stroke=1, fillMode=0)
        for camada, geometrias in self.bases:
            agua = 'hidrografia' in camada or 'massa_dagua' in camada
            tela.setStrokeColor(colors.HexColor('#237bba' if agua else '#a14c81'))
            tela.setFillColor(colors.HexColor('#98c9e0' if agua else '#d6bad0'))
            tela.setLineWidth(.55 if agua else .8)
            for geom in geometrias: tela.drawPath(caminho(geom), fill=int('Polygon' in geom['type']), stroke=1, fillMode=0)
        mina = next(g for k, g in self.feicoes if k == 'mina')
        tela.setFillColor(colors.HexColor('#8bb8a8'))
        tela.setStrokeColor(VERDE)
        tela.setLineWidth(1.5)
        tela.drawPath(caminho(mina), fill=1, stroke=1, fillMode=0)
        tela.setFont('GeoNegrito', 8)
        tela.setFillColor(VERDE)
        tela.drawString(self.width - 27, self.height - 18, 'N')
        tela.line(self.width - 24, self.height - 39, self.width - 24, self.height - 23)
        tela.line(self.width - 24, self.height - 23, self.width - 28, self.height - 29)
        tela.line(self.width - 24, self.height - 23, self.width - 20, self.height - 29)
        tela.setFont('GeoRegular', 7)
        tela.drawString(12, 12, 'Influência: amarelo  |  Mina: verde  |  Dados do tema: linhas e superfícies')
        comprimento = 1000 * escala
        tela.setLineWidth(1)
        tela.line(14, 28, 14 + comprimento, 28)
        tela.drawString(18 + comprimento, 25, '1 km - UTM 23S')
        tela.restoreState()


def ler_cenario(raiz, mina_id):
    """Exige cenário explicitamente fictício vinculado à mina e com referência metodológica."""
    caminho = Path(raiz) / 'dados/cenarios' / f'{mina_id}.json'
    c = json.loads(caminho.read_text())
    if c['mina_id'] != mina_id or c['natureza'] != 'simulado' or not c['premissas'] or not c['referencia']['secoes']:
        raise ValueError('Cenário técnico inválido')
    if len({p['id'] for p in c['premissas']}) != len(c['premissas']): raise ValueError('Premissas duplicadas')
    for p in c['premissas']:
        if not all(isinstance(p[k], str) and p[k] for k in ('id', 'tema', 'situacao', 'condicao', 'base')):
            raise ValueError('Premissa incompleta')
    return c


def nome_registro(feicao):
    """Prefere nomes efetivamente publicados e mantém ausência de nome explícita."""
    p = feicao['properties']
    for campo in ('nome_uc', 'nmoriginal', 'nmalternat', 'noriocomp', 'legenda', 'Name', 'codigo_rod'):
        valor = p.get(campo)
        if isinstance(valor, str) and valor.strip(): return valor
    return 'Sem nome publicado'


def detalhe_registro(feicao):
    """Organiza descritores cadastrais presentes, sem interpretá-los como medidas do recorte."""
    p = feicao['properties']
    campos = [('categoria', 'Categoria'), ('grupo', 'Grupo'), ('sigla', 'Sigla'), ('administracao', 'Administração'),
              ('tipomassa', 'Tipo'), ('tipotrecho', 'Tipo'), ('nmterreno', 'Terreno'), ('jurisdicao', 'Jurisdição'),
              ('tipo', 'Tipo'), ('situacao', 'Situação'), ('cdclasse', 'Classe')]
    saida = [f'{rotulo}: {p[c]}' for c, rotulo in campos if p.get(c) is not None and str(p[c]).strip()]
    return '; '.join(saida[:3]) or '-'


def bloco_classes(base):
    """Resume a distribuição de todas as classes nativas em proporção de células válidas."""
    t = tabela(['Classe publicada', 'Células válidas', '% das células válidas'],
                  [(c['nome'], numero(c['celulas']), numero(c['percentual_celulas_validas'], 2) + '%') for c in base['classes']],
                  [LARGURA * .56, LARGURA * .22, LARGURA * .22])
    t.setStyle(TableStyle([('TOPPADDING', (0, 1), (-1, -1), 5), ('BOTTOMPADDING', (0, 1), (-1, -1), 5)]))
    return t


class DocumentoPDF(SimpleDocTemplate):
    """Acrescenta marcadores de navegação às seções do relatório."""

    def afterFlowable(self, elemento):
        if isinstance(elemento, Paragraph) and elemento.style.name == 'secao':
            chave = 'secao-' + hashlib.sha256(elemento.getPlainText().encode()).hexdigest()[:12]
            self.canv.bookmarkPage(chave)
            self.canv.addOutlineEntry(elemento.getPlainText(), chave, level=0)


def gerar_pdf(dados, cenario):
    """Gera documento padronizado sem dados fictícios nos blocos de observações geográficas."""
    destino = BytesIO()
    mina = dados['mina']
    documento = DocumentoPDF(destino, pagesize=A4, leftMargin=42, rightMargin=42, topMargin=91, bottomMargin=49,
                                  title=f'GeoVale - Relatório territorial - {mina["nome"]}', author='GeoVale', subject='Dados territoriais e cenário técnico simulado')
    elementos = []
    def adicionar(*itens): elementos.extend(itens)
    def secao(nome): adicionar(PageBreak(), paragrafo(nome, 'secao'))
    def bases_tema(tema): return [b for b in dados['bases'] if b['base']['tema_id'] == tema]
    def quantidade(tema): return sum(b['quantidade'] for b in bases_tema(tema))
    def resumo_base(b):
        unidade = 'células válidas' if b['tipo'] == 'raster' else 'registros'
        metadado = paragrafo(f'{numero(b["quantidade"])} {unidade} | Consulta: {data_local(b["consultado_em"])}', 'pequeno')
        metadado.keepWithNext = True
        adicionar(paragrafo(b['base']['nome'], 'grupo'), metadado)
    def inventario(b):
        fs = b['dados']['features']
        if not fs: adicionar(paragrafo('Nenhum registro publicado encontrado no recorte.')); return
        linhas = [(str(f['id']).rsplit('.', 1)[-1], nome_registro(f), detalhe_registro(f)) for f in fs]
        adicionar(tabela(['ID na base', 'Identificação publicada', 'Descritores disponíveis'], linhas, [LARGURA * .17, LARGURA * .4, LARGURA * .43]))

    adicionar(paragrafo('DADOS TERRITORIAIS + CENÁRIO TÉCNICO SIMULADO', 'pequeno'),
              paragrafo('Relatório territorial', 'titulo'), paragrafo(mina['nome'], 'subtitulo'),
              paragrafo(f'{mina["municipio"]}/{mina["uf"]} | Emissão: {data_local(dados["gerado_em"])}'),
              MapaTerritorial(dados), Spacer(1, 10),
              paragrafo('Representação vetorial do recorte e da mina, com hidrografia cadastrada. Influência aproximada: FEAM, Figura 2.3. Mina: OpenStreetMap contributors, ODbL. Hidrografia: ANA/Igam, IDE-Sisema. Sem imagem de satélite.', 'pequeno'),
              tabela(['Bases integradas', 'Temas territoriais', 'Cenário'], [[len(dados['bases']), len({b['base']['tema_id'] for b in dados['bases']}), cenario['horizonte']]]),
              Spacer(1, 12), paragrafo('Dados geográficos reais e premissas técnicas fictícias apresentados em seções distintas.', 'destaque'))

    secao('01 | Território e bases consultadas')
    adicionar(paragrafo('O recorte comum organiza a leitura territorial da mina e de seu entorno. A representação da mina está contida no mapa de contexto; o contorno maior é a extensão usada para reunir todas as bases.'),
              paragrafo('Delimitação de referência', 'grupo'),
              paragrafo('Contorno externo da AII de águas e solos, meio físico, do projeto de ampliação Tamanduá/Horizontes. Digitalizado aproximadamente da Figura 2.3 do Parecer 64/FEAM/GST/2024. Seu uso para todos os temas é uma simplificação do MVP, sem definição de áreas de intervenção ou fechamento.'),
              tabela(['Tema / base', 'Quantidade', 'Unidade'], [(b['base']['tema'] + ' / ' + b['base']['nome'], numero(b['quantidade']), 'células válidas' if b['tipo'] == 'raster' else 'registros') for b in dados['bases']], [LARGURA * .63, LARGURA * .18, LARGURA * .19]),
              Spacer(1, 12), paragrafo('Todos os temas entram neste documento. Checkboxes, intensidade, fundo e enquadramento da tela não filtram o conteúdo do relatório.', 'pequeno'))

    secao('02 | Relevo, declividade e solos')
    for b in bases_tema('relevo'):
        resumo_base(b)
        if b['tipo'] == 'raster':
            adicionar(bloco_classes(b), Spacer(1, 9), paragrafo(f'Grade nativa: {b["crs"]}. Dimensões: {b["dimensoes"][0]} linhas x {b["dimensoes"][1]} colunas. Células sem dados dentro do recorte: {numero(b["celulas_sem_dados"])}.', 'pequeno'))
    adicionar(paragrafo('A declividade Topodata deriva do SRTM de 2000. É contexto regional e não uma avaliação atual dos taludes da mina. Percentuais descrevem células válidas, sem cálculo de área.', 'pequeno'))
    for b in bases_tema('solos'): resumo_base(b); inventario(b)
    adicionar(Spacer(1, 10), paragrafo('O mapa pedológico regional descreve tipos de solo. Compactação, fertilidade, contaminação e condições para plantio exigem outras avaliações.', 'pequeno'))

    secao('03 | Água e drenagem')
    adicionar(paragrafo('Rios e corpos d’água cadastrados na influência', 'grupo'), MapaTerritorial(dados, altura=300), Spacer(1, 10))
    for b in bases_tema('agua'): resumo_base(b)
    adicionar(paragrafo('As quantidades representam registros cadastrados: trechos de um mesmo rio podem aparecer separadamente. As geometrias são recortadas pela influência irregular. Não foram medidas qualidade da água, vazão atual, nível ou segurança das estruturas.', 'pequeno'),
              paragrafo('O inventário de todos os registros de água está no Anexo A. A drenagem técnica do cenário simulado aparece em seção própria.'))

    secao('04 | Vegetação e conservação')
    for b in bases_tema('vegetacao'):
        if b['tipo'] == 'raster': resumo_base(b); adicionar(bloco_classes(b), Spacer(1, 10))
    conservacao = []
    for b in bases_tema('vegetacao'):
        if b['tipo'] != 'vetor': continue
        esfera = 'Estadual' if 'estaduais' in b['base']['camada'] else 'Federal' if 'federais' in b['base']['camada'] else 'Municipal'
        conservacao.extend((esfera, nome_registro(f), detalhe_registro(f)) for f in b['dados']['features'])
    adicionar(paragrafo('Unidades de conservação cadastradas', 'grupo'),
              tabela(['Esfera', 'Identificação publicada', 'Descritores'], conservacao or [('-', 'Nenhum registro no recorte', '-')], [LARGURA * .15, LARGURA * .5, LARGURA * .35]))
    adicionar(Spacer(1, 10), paragrafo('Cobertura da terra: referência 2025, MapBiomas. As classes incluem usos diversos; a tabela não representa somente vegetação. A classe conjunta Rio, Lago e Oceano é o rótulo publicado e não discrimina o tipo local nem a salinidade da água. Unidades de conservação são cadastros de esferas distintas, sem união de áreas ou interpretação automática de restrições.', 'pequeno'))

    secao('05 | Entorno, infraestrutura e trilhas')
    adicionar(MapaTerritorial(dados, tema='trilhas', altura=290), Spacer(1, 10))
    for b in bases_tema('entorno') + bases_tema('trilhas'): resumo_base(b)
    adicionar(paragrafo('Áreas urbanizadas, rodovias e trilhas dão contexto à circulação e ocupação do território. Presença cadastral não demonstra acesso autorizado, condição operacional, demanda social ou segurança de visitantes.', 'pequeno'),
              paragrafo('O Anexo A reúne todos os registros de infraestrutura e trilhas encontrados no recorte. Os nomes são os publicados pelas fontes.'))

    secao('06 | Cenário técnico simulado')
    adicionar(paragrafo(cenario['horizonte'], 'subtitulo'), paragrafo(cenario['descricao'], 'destaque'),
              paragrafo('Premissas adotadas para a demonstração', 'grupo'),
              tabela(['Componente', 'Situação simulada', 'Premissa técnica'], [(p['tema'], p['situacao'], p['condicao']) for p in cenario['premissas']], [LARGURA * .19, LARGURA * .24, LARGURA * .57]), Spacer(1, 10),
              paragrafo('A estrutura do cenário se inspira nos procedimentos de planejamento, vistoria e reabilitação do plano Minas-Rio. Os estados acima foram criados para este protótipo; não são resultados extraídos de laudos da mina nem conclusões executadas pela empresa do documento de referência.', 'pequeno'))

    secao('07 | Síntese e condições a verificar')
    adicionar(paragrafo('Leitura integrada dos dados e premissas', 'grupo'),
              paragrafo(f'O recorte reúne {numero(quantidade("agua"))} registros de água, {numero(quantidade("solos"))} registros pedológicos, {numero(quantidade("entorno"))} registros de entorno/infraestrutura e {numero(quantidade("trilhas"))} registros de trilhas. Essas contagens são descritivas e não medidas de risco ou benefício.'),
              tabela(['Possibilidade a estudar', 'Elementos disponíveis', 'Condições pendentes'], [
                  ['Recuperação ecológica', 'Dados reais de cobertura da terra, solos e água; estabilização e drenagem assumidas no cenário simulado.', 'Preparo do solo, projeto específico, implantação e acompanhamento da revegetação.'],
                  ['Lazer e educação ambiental', f'{numero(quantidade("trilhas"))} registros reais de trilhas na influência; contexto de ocupação e acessos.', 'Localização da atividade, segurança de visitantes, acesso autorizado e participação da comunidade.'],
                  ['Reaproveitamento de estruturas', 'Uma edificação candidata, exclusivamente como premissa fictícia do cenário.', 'Confirmação da estrutura, avaliação específica, finalidade e viabilidade de implantação.'],
              ], [LARGURA * .24, LARGURA * .4, LARGURA * .36]), Spacer(1, 14),
              paragrafo('Este documento organiza evidências e pendências. Não calcula pontuação de aptidão, não classifica alternativas e não certifica segurança. A matriz multicritério e seus pesos ainda não foram definidos.', 'destaque'))

    secao('08 | Fontes e rastreabilidade')
    adicionar(paragrafo('Dados territoriais reais', 'grupo'))
    linhas = []
    for i, b in enumerate(dados['bases'], 1):
        link = Paragraph(f'<link href="{texto(b["base"]["metadado"])}" color="#008477">Ficha oficial da base</link>', ESTILOS['celula'])
        linhas.append([f'{i:02d}. {b["base"]["nome"]}', data_local(b['consultado_em']), link])
    adicionar(tabela(['Base', 'Consulta (São Paulo)', 'Referência'], linhas, [LARGURA * .5, LARGURA * .25, LARGURA * .25]), Spacer(1, 12),
              paragrafo('Delimitação e mapa', 'grupo'),
              paragrafo('FEAM - Parecer 64/FEAM/GST/2024, Figura 2.3, PDF p. 18 / impressa 15. Mapa de 02/11/2023. Contorno aproximado da AII de águas e solos do projeto conjunto Tamanduá/Horizontes.'),
              paragrafo('OpenStreetMap contributors - way 315221699, licença ODbL. Referência cartográfica colaborativa da mina, sem certificação de perímetro atual.'),
              paragrafo('Referência metodológica do cenário', 'grupo'),
              paragrafo(f'{cenario["referencia"]["instituicao"]}. {cenario["referencia"]["titulo"]}. Revisão: {cenario["referencia"]["revisao"]}. Seções: {cenario["referencia"]["secoes"]}. Páginas impressas: {cenario["referencia"]["paginas_impressas"]}.'),
              Paragraph(f'<link href="{texto(cenario["referencia"]["url"])}" color="#008477">Consultar documento de referência</link>', ESTILOS['texto']),
              paragrafo('As prescrições do plano foram usadas como inspiração de estrutura. As condições simuladas foram definidas no GeoVale. Não foram transferidos parâmetros de projeto, custos ou resultados técnicos do Minas-Rio para esta mina.', 'pequeno'),
              paragrafo('Data de consulta é a data de obtenção do dado, não de levantamento. A representação na tela pode consultar imagens atuais enquanto este relatório retrata a coleta persistida. Campos e matrizes completos permanecem no armazenamento interno; o PDF apresenta sínteses e inventário legível, sem coordenadas ou matrizes extensas.', 'pequeno'))

    secao('Anexo A | Inventário dos registros')
    adicionar(paragrafo('Todos os registros vetoriais encontrados no recorte são listados a seguir, com identificador curto na base, identificação e descritores disponíveis. O ID curto é a parte final do identificador publicado, cujo prefixo é o da base. Ausência de nome permanece explícita. Atributos cadastrais não são reinterpretados como medidas da porção recortada.', 'pequeno'))
    for b in dados['bases']:
        if b['tipo'] == 'vetor': resumo_base(b); inventario(b); adicionar(Spacer(1, 9))

    def pagina(tela, doc):
        tela.saveState()
        tela.setFillColor(VERDE)
        tela.rect(0, A4[1] - 70, A4[0], 70, fill=1, stroke=0)
        logo(tela, 40, A4[1] - 57, .9)
        tela.setFillColor(AMARELO)
        tela.rect(0, A4[1] - 73, A4[0], 3, fill=1, stroke=0)
        tela.setFont('GeoRegular', 7)
        tela.setFillColor(CINZA)
        tela.drawString(42, 29, 'GeoVale | Relatório territorial e cenário técnico simulado')
        tela.drawRightString(A4[0] - 42, 29, f'{doc.page}')
        tela.restoreState()
    documento.build(elementos, onFirstPage=pagina, onLaterPages=pagina)
    return destino.getvalue()


class RelatoriosPDF:
    """Mantém um PDF por mina, invalidado por mudança de dados, cenário ou modelo."""

    def __init__(self, fonte, raiz):
        self.fonte, self.raiz = fonte, raiz
        self.cache = {}
        self.trava = Lock()

    def obter(self, mina_id):
        """Usa somente dados persistidos atuais e o cenário local, sem consultas externas."""
        dados = self.fonte.relatorio(mina_id)
        cenario = ler_cenario(self.raiz, mina_id)
        chave = hashlib.sha256(json.dumps({'dados': {k: v for k, v in dados.items() if k != 'gerado_em'}, 'cenario': cenario, 'modelo': '4.1.0'}, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        with self.trava:
            anterior = self.cache.get(mina_id)
            if anterior and anterior[0] == chave: return anterior[1]
            pdf = gerar_pdf(dados, cenario)
            self.cache[mina_id] = (chave, pdf)
            return pdf
