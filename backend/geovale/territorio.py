"""Prepara e guarda dados por mina em SQLite, independentemente da navegação do mapa."""
import hashlib
import json
import logging
import os
import sqlite3
import threading
import time
import zlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

from shapely.geometry import shape
from geovale.camadas import CAMADAS
from geovale.fontes_territorio import coletar_base
from geovale.influencia import ler_influencia, textos_recorte

VERSAO_METODO = '4.0.0'
PRAZO_ATUALIZACAO = 24 * 3600
PRAZO_REPETICAO = 300
REGISTRO = logging.getLogger('geovale.territorio')


def catalogar_bases(catalogo):
    """Deriva todos os conjuntos do mesmo catálogo usado pelos seletores visuais."""
    bases = []
    for tema in catalogo:
        for base in tema['bases']:
            identidade = hashlib.sha256(base['camada'].encode()).hexdigest()[:16]
            bases.append({**base, 'id': identidade, 'tema_id': tema['id'], 'tema': tema['nome']})
    if len({b['camada'] for b in bases}) != len(bases):
        raise ValueError('Camada duplicada no catálogo de dados')
    return bases


def assinatura_base(base, influencia):
    """Vincula cada base ao seu recorte/evidência; adicionar outra base não invalida as existentes."""
    dados = {'base': base, 'influencia': influencia, 'metodo': VERSAO_METODO}
    return hashlib.sha256(json.dumps(dados, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def agora_iso():
    """Distingue a data de processamento das datas de referência publicadas nas fontes."""
    return datetime.now(timezone.utc).isoformat()


class DadosTerritoriais:
    """Processa o catálogo automaticamente e persiste resultados completos por base e por mina."""

    def __init__(self, raiz, catalogo=CAMADAS, coletar=coletar_base, relogio=time.time, fixos=None):
        self.raiz = Path(raiz)
        # Publicação de demonstração: usa o banco coletado como retrato datado, sem coletar nem vencer.
        self.fixos = os.environ.get('GEOVALE_DADOS_FIXOS') == '1' if fixos is None else fixos
        self.catalogo = catalogo
        self.coletar = coletar
        self.relogio = relogio
        self.banco = self.raiz / '.local/territorios.sqlite3'
        self._parar = threading.Event()
        self._ciclo = threading.Lock()
        self._thread = None
        self._preparo = threading.Lock()

    @contextmanager
    def conectar(self):
        """Abre armazenamento local sem publicar dados coletados ou credenciais no Git."""
        with self._preparo:
            self.banco.parent.mkdir(parents=True, exist_ok=True)
            conexao = sqlite3.connect(self.banco, timeout=10)
            conexao.row_factory = sqlite3.Row
            conexao.execute('PRAGMA journal_mode=WAL')
            conexao.execute("""CREATE TABLE IF NOT EXISTS bases (
                mina TEXT NOT NULL, camada TEXT NOT NULL, assinatura TEXT NOT NULL,
                estado TEXT NOT NULL, tentado REAL NOT NULL, consultado TEXT,
                documento BLOB, artefato BLOB, erro TEXT,
                PRIMARY KEY (mina, camada))""")
            conexao.commit()
        try:
            with conexao:
                yield conexao
        finally:
            conexao.close()

    def influencia(self, mina_id):
        """Lê o recorte local configurado para cada mina do catálogo."""
        return ler_influencia(self.raiz / 'dados/influencias' / f'{mina_id}.geojson', mina_id)

    def iniciar(self):
        """Prepara as minas na abertura do servidor e reavalia pendências a cada minuto."""
        if self.fixos or (self._thread is not None and self._thread.is_alive()):
            return
        self._parar.clear()
        self._thread = threading.Thread(target=self._executar, daemon=True, name='geovale-territorios')
        self._thread.start()

    def encerrar(self):
        """Interrompe o agendamento automático; os dados válidos continuam em disco."""
        self._parar.set()
        if self._thread is not None:
            self._thread.join(timeout=1)

    def _executar(self):
        """Mantém o processamento independente de cliques, checkboxes ou viewport."""
        while not self._parar.is_set():
            try:
                self.atualizar()
            except Exception:
                REGISTRO.exception('Não foi possível preparar os dados territoriais.')
            self._parar.wait(60)

    def atualizar(self):
        """Atualiza somente bases novas, alteradas, vencidas ou com falha recuperável."""
        with self._ciclo:
            minas = json.loads((self.raiz / 'dados/minas.json').read_text())
            bases = catalogar_bases(self.catalogo)
            for mina in minas:
                if self._parar.is_set():
                    break
                influencia = self.influencia(mina['id'])
                recorte = shape(next(f['geometry'] for f in influencia['features'] if f['properties']['id'] == 'influencia'))
                agora = self.relogio()
                pendentes = []
                with self.conectar() as db:
                    for base in bases:
                        chave = assinatura_base(base, influencia)
                        anterior = db.execute('SELECT * FROM bases WHERE mina=? AND camada=?', (mina['id'], base['camada'])).fetchone()
                        prazo = PRAZO_ATUALIZACAO if anterior and anterior['estado'] == 'pronto' else PRAZO_REPETICAO
                        if anterior and anterior['assinatura'] == chave and agora - anterior['tentado'] < prazo:
                            continue
                        manter = anterior is not None and anterior['assinatura'] == chave
                        db.execute('INSERT OR REPLACE INTO bases VALUES (?,?,?,?,?,?,?,?,?)',
                                   (mina['id'], base['camada'], chave, 'processando', agora,
                                    anterior['consultado'] if manter else None,
                                    anterior['documento'] if manter else None,
                                    anterior['artefato'] if manter else None, None))
                        pendentes.append((base, chave))
                if not pendentes:
                    continue
                with ThreadPoolExecutor(max_workers=3) as executor:
                    pedidos = {executor.submit(self.coletar, base, recorte): (base, chave) for base, chave in pendentes}
                    for pedido in as_completed(pedidos):
                        base, chave = pedidos[pedido]
                        try:
                            documento, artefato = pedido.result()
                            documento['consultado_em'] = agora_iso()
                            documento['recorte'] = {'id': 'influencia', 'fonte': influencia['fonte'], 'assinatura': chave}
                            bruto = zlib.compress(json.dumps(documento, ensure_ascii=False, allow_nan=False).encode())
                            with self.conectar() as db:
                                db.execute('UPDATE bases SET estado=?, consultado=?, documento=?, artefato=?, erro=NULL WHERE mina=? AND camada=? AND assinatura=?',
                                           ('pronto', documento['consultado_em'], bruto, artefato, mina['id'], base['camada'], chave))
                            REGISTRO.info('%s: %s pronta (%s).', mina['id'], base['nome'], documento['quantidade'])
                        except Exception as erro:
                            REGISTRO.warning('%s: falha em %s (%s).', mina['id'], base['nome'], erro)
                            with self.conectar() as db:
                                db.execute('UPDATE bases SET estado=?, erro=? WHERE mina=? AND camada=? AND assinatura=?',
                                           ('erro', 'A fonte não forneceu um recorte completo e válido. Nova tentativa automática em até cinco minutos.', mina['id'], base['camada'], chave))

    def vencido(self, linha):
        """Dado com mais de 24 h pede nova coleta; com dados fixos, a data de consulta continua no relatório e nada vence."""
        return not self.fixos and self.relogio() - linha['tentado'] >= PRAZO_ATUALIZACAO

    def _ler(self, mina_id, base, influencia):
        """Rejeita dados guardados para outro recorte ou configuração da base."""
        with self.conectar() as db:
            linha = db.execute('SELECT * FROM bases WHERE mina=? AND camada=?', (mina_id, base['camada'])).fetchone()
        if linha is None or linha['assinatura'] != assinatura_base(base, influencia):
            return None, None
        dados = json.loads(zlib.decompress(linha['documento'])) if linha['documento'] else None
        return dict(linha), dados

    def obter(self, mina_id):
        """Entrega resumo do catálogo inteiro; seletores visuais não são parâmetros desta leitura."""
        influencia = self.influencia(mina_id)
        saida = []
        for base in catalogar_bases(self.catalogo):
            linha, dados = self._ler(mina_id, base, influencia)
            resumo = {k: v for k, v in base.items() if k != 'legenda'}
            resumo.update(estado=linha['estado'] if linha else 'pendente', erro=linha['erro'] if linha else None,
                          consultado_em=linha['consultado'] if linha else None,
                          desatualizado=bool(linha and self.vencido(linha)))
            if dados:
                resumo.update({k: v for k, v in dados.items() if k not in ('dados', 'recorte', 'descricao_cobertura_xml', 'estilo_padrao_xml')})
                resumo['total_campos'] = len(dados.get('campos', []))
                resumo['dados_url'] = f"/api/minas/{mina_id}/territorio/{base['id']}"
                if dados['tipo'] == 'raster':
                    resumo['arquivo_url'] = resumo['dados_url'] + '/arquivo'
            saida.append(resumo)
        prontas = sum(b['estado'] == 'pronto' and not b['desatualizado'] for b in saida)
        return {'mina_id': mina_id, 'recorte': {'nome': 'Área de influência · recorte comum do MVP',
                'origem': textos_recorte(influencia)['origem_texto'],
                'fonte': influencia['fonte'], 'aproximado': True},
                'bases': saida, 'total_bases': len(saida), 'bases_prontas': prontas,
                'completo': prontas == len(saida), 'prazo_atualizacao_horas': 24,
                'aviso': 'Caracterização preliminar em recorte comum aproximado. Não define áreas de intervenção, beneficiários ou aptidão.'}

    def registros(self, mina_id, base_id):
        """Disponibiliza todos os atributos/porções vetoriais ou metadados matriciais guardados."""
        base = next((b for b in catalogar_bases(self.catalogo) if b['id'] == base_id), None)
        if base is None:
            raise KeyError(base_id)
        influencia = self.influencia(mina_id)
        linha, dados = self._ler(mina_id, base, influencia)
        if dados is None:
            return None
        return {'base': base, 'estado': linha['estado'], 'desatualizado': self.vencido(linha), **dados}

    def arquivo(self, mina_id, base_id):
        """Entrega somente o GeoTIFF já guardado para uma base matricial do catálogo atual."""
        base = next((b for b in catalogar_bases(self.catalogo) if b['id'] == base_id), None)
        if base is None:
            raise KeyError(base_id)
        linha, dados = self._ler(mina_id, base, self.influencia(mina_id))
        return linha['artefato'] if linha and dados and dados['tipo'] == 'raster' else None


    def relatorio(self, mina_id):
        """Reúne o catálogo persistido para o PDF, sem rede ou expansão de matrizes em texto."""
        influencia = self.influencia(mina_id)
        mina = next(m for m in json.loads((self.raiz / 'dados/minas.json').read_text()) if m['id'] == mina_id)
        with self.conectar() as db:
            linhas = {l['camada']: dict(l) for l in db.execute('SELECT * FROM bases WHERE mina=?', (mina_id,))}
        bases = []
        for base in catalogar_bases(self.catalogo):
            linha = linhas.get(base['camada'])
            if (not linha or linha['assinatura'] != assinatura_base(base, influencia)
                    or linha['estado'] != 'pronto' or self.vencido(linha)):
                raise ValueError('Relatório completo ainda indisponível')
            dados = json.loads(zlib.decompress(linha['documento']))
            bases.append({'base': base, 'estado': linha['estado'], **dados})
        return {'formato': 'geovale-territorio', 'versao': VERSAO_METODO, 'gerado_em': agora_iso(),
                'mina': mina, 'influencia': influencia, 'completo': True, 'bases': bases,
                'aviso': 'Caracterização preliminar em recorte comum aproximado. Não é plano de fechamento nem avaliação de aptidão. Datas de consulta não são datas de levantamento. Atributos cadastrais não são medidas recalculadas do recorte.'}
