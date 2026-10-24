# Estado real — GeoVale 2.0

Atualizado em 24/10/2026. A rota ativa é **GIS + AHP + TOPSIS**, sem ML. Consulte [Metodologia](METODOLOGIA.md) e [Decisões](DECISOES.md).

A entrada ocorre exclusivamente pelo envio de um GeoJSON do computador. Implementados: validação, mapa com fotografia aérea e hectares, análise de relevo/cobertura, prioridades manuais/AHP, consistência, TOPSIS/empates, sensibilidade, invalidação de resultados antigos, revisão SQLite imutável e dois relatórios HTML da mesma revisão. **Trocar mapa** retorna à escolha do arquivo.

A jornada completa cobre Rapatee (162,29 ha) e Burning Star 3 (530,55 ha). Os dois arquivos da apresentação estão em `~/Desktop/Mapas GeoVale/`. Outras poligonais válidas podem ser exibidas, mas exigem preparação de fontes para receber análise. Não há diagnóstico homologado de aptidão, autorização de uso, avaliação financeira, geotécnica ou social.

Interface sem login ou painéis técnicos. Logo estática, etapas abaixo do título, caixa centralizada à direita, textos essenciais e fundo contínuo de pedra na cor original. Explicações detalhadas no [Manual de uso](MANUAL_USO.md). Os pacotes geográficos, os cálculos e o conteúdo dos relatórios foram preservados.

Verificações desta revisão: **119 testes Python e 2 testes frontend passaram**; TypeScript e build Vite aprovados. O envio manual de Rapatee pelo navegador carregou 162,29 ha, analisou e comparou com os índices 0,974 / 0,719 / 0,013; Trocar mapa retornou à entrada. As verificações anteriores incluíram integridade de 20 arquivos, leitura de duas geometrias do GeoPackage e abertura em dez tamanhos por viewport do navegador. Não foi teste físico em todos os dispositivos.

Execute pela raiz com ambiente Python compatível e build frontend: `python executar.py`. Porta padrão 8000, apenas loopback; `GEOVALE_PORT` permite outra porta. Rascunhos em memória; revisões em `.local/geovale.sqlite3`. Os downloads exigem o cookie da sessão; os HTMLs já baixados funcionam independentemente dele. Veja o [README](../README.md).

Pendências operacionais: validar critérios e regras com especialistas, ampliar fontes e restrições, preparar dados brasileiros, revisar termos de uso das fontes e projetar autenticação/infraestrutura para eventual exposição remota. Linux, interface QGIS, estudos técnicos de campo e implantação pública não foram executados nesta entrega.

Entrega de código e documentação versionada para o repositório GitHub, conforme autorização de 24/10/2026. A aplicação continua local, sem implantação pública. Instruções locais, conversas, banco, dependências e build permanecem fora do Git.

Revisão geral de 24/10/2026: corrigida a abertura de geometrias com posições 2D/3D misturadas, preservando o documento original; coordenadas e pesos fora da representação numérica são recusados sem erro interno. A exportação confere tanto o pacote atual quanto os hashes congelados na revisão salva, impedindo troca silenciosa da fotografia. Foram acrescentados 11 casos de regressão. O verificador dos pacotes confirmou novamente 20 arquivos, as duas geometrias do GeoPackage e os mesmos índices de referência. Links locais, sintaxe Python, lock frontend e exclusões de publicação foram conferidos.
