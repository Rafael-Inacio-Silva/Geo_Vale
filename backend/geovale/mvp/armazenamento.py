"""Revisões imutáveis SQLite, isoladas por sessão anônima e sem sobrescrever análises antigas."""
from pathlib import Path
from datetime import datetime, timezone
from hashlib import sha256
import json
import sqlite3
from contextlib import contextmanager


class Revisoes:
    """Mantém a versão aceita e os bytes JSON usados pelos dois relatórios."""

    def __init__(self,caminho:Path):
        """Cria apenas a nova tabela, preservando qualquer banco legado no mesmo arquivo."""
        self.caminho=caminho
        caminho.parent.mkdir(parents=True,exist_ok=True)
        with self.conectar() as con:
            con.execute('''CREATE TABLE IF NOT EXISTS estudos_mcda_v2 (
                area_id TEXT NOT NULL, revisao INTEGER NOT NULL, sessao_hash TEXT NOT NULL,
                criado_em TEXT NOT NULL, sha256 TEXT NOT NULL, retrato TEXT NOT NULL,
                PRIMARY KEY(area_id,revisao))''')
            con.execute('CREATE INDEX IF NOT EXISTS idx_estudos_sessao ON estudos_mcda_v2(sessao_hash,area_id)')
            con.execute("CREATE TRIGGER IF NOT EXISTS estudos_sem_update BEFORE UPDATE ON estudos_mcda_v2 BEGIN SELECT RAISE(ABORT,'Revisão imutável'); END")
            con.execute("CREATE TRIGGER IF NOT EXISTS estudos_sem_delete BEFORE DELETE ON estudos_mcda_v2 BEGIN SELECT RAISE(ABORT,'Revisão imutável'); END")

    @contextmanager
    def conectar(self):
        """Abre conexão curta e serializa gravações com timeout, sem compartilhar conexão entre threads."""
        con=sqlite3.connect(self.caminho,timeout=10)
        con.execute('PRAGMA busy_timeout=10000')
        try:
            with con:
                yield con
        finally:
            con.close()

    def salvar(self,identificador:str,sessao:str,retrato:dict) -> int:
        """Acrescenta revisão atomicamente; o usuário não escolhe número ou sobrescreve a anterior."""
        raw=json.dumps(retrato,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)
        with self.conectar() as con:
            con.execute('BEGIN IMMEDIATE')
            r=con.execute('SELECT COALESCE(MAX(revisao),0) FROM estudos_mcda_v2 WHERE area_id=?',(identificador,)).fetchone()[0]+1
            con.execute('INSERT INTO estudos_mcda_v2 VALUES(?,?,?,?,?,?)',(identificador,r,sessao,datetime.now(timezone.utc).isoformat(),sha256(raw.encode()).hexdigest(),raw))
        return r

    def ler(self,identificador:str,revisao:int,sessao:str) -> dict|None:
        """Recupera somente a sessão proprietária e confere a assinatura antes de exportar."""
        with self.conectar() as con:
            r=con.execute('SELECT retrato,sha256 FROM estudos_mcda_v2 WHERE area_id=? AND revisao=? AND sessao_hash=?',(identificador,revisao,sessao)).fetchone()
        if r is None:return None
        if sha256(r[0].encode()).hexdigest()!=r[1]:raise ValueError('A revisão salva falhou na conferência de integridade.')
        return json.loads(r[0])
