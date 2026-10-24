# Persistência

Banco padrão `.local/geovale.sqlite3`; variável opcional `GEOVALE_BANCO` altera o caminho. O diretório não entra no Git. O schema é criado pelo módulo `mvp/armazenamento.py`; SQL legado foi removido para não duplicar uma estrutura abandonada.

Tabela `estudos_mcda_v2`: `area_id`, `revisao`, `sessao_hash`, `criado_em`, `sha256`, `retrato`. Chave composta área/revisão, índice por sessão/área. Gravação em transação `BEGIN IMMEDIATE`; próxima revisão calculada atomicamente. Triggers rejeitam UPDATE e DELETE. Uma nova comparação gera nova revisão; salvar novamente o mesmo estado é idempotente.

`retrato` contém entrada, geometria, análise, fontes, hipóteses, AHP, pesos e sua origem, TOPSIS e sensibilidade, além do resumo público. Não contém o segredo do cookie. SHA256 dos bytes JSON é verificado na leitura. Isolamento por hash da sessão em cada consulta: outra sessão não recupera a revisão por conhecer a URL.

Os dois relatórios são vistas da mesma revisão. O ranking não é recalculado ao baixar. A figura é renderizada com geometria salva e a imagem do pacote cuja integridade é conferida. Alterar arquivos de fonte pode impedir a exportação; preserve os pacotes juntamente com o banco para reprodução futura.

Rascunhos não são persistidos e não há navegação visual de revisões antigas. Mantenha as URLs dos relatórios durante a sessão ou baixe os HTMLs. Copie o SQLite com o servidor parado para backup consistente; não apague bancos anteriores. A criação desta tabela não remove tabelas de versões antigas que eventualmente existam no mesmo arquivo.
