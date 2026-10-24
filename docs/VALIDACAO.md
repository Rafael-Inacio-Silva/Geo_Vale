# Verificação da versão 2.0

## Revisão de 24/10/2026

Entrada exclusivamente por arquivo GeoJSON do computador. **119 testes Python e 2 testes frontend passaram**, assim como TypeScript e build Vite. A verificação de URLs antigas confirmou que elas não criam áreas. No navegador, Rapatee foi enviado pelo seletor do computador: mapa de 162,29 ha, análise e comparação 0,974 / 0,719 / 0,013; Trocar mapa retornou à entrada. O servidor local da porta 8024 foi atualizado.

## Cobertura automatizada

Validação GeoJSON, AHP/TOPSIS com valores analíticos, pesos inválidos, empates, sensibilidade, relevo conhecido, NoData, jornadas dos dois recortes reais, isolamento de sessão, integridade de fontes, revisões e relatórios. Testes frontend cobrem total dos pesos e invalidação do resultado/exportação ao editar prioridades. TypeScript e build Vite verificam o código distribuído.

## Evidências anteriores preservadas

- Verificador offline confirmou os hashes de 20 arquivos e a leitura de duas geometrias válidas do GeoPackage.
- Plano de relevo com gradiente 1 produziu 45°; vizinhança com NoData não foi preenchida.
- AHP conferido com vetor conhecido, inconsistência e reciprocidade; TOPSIS com caso analítico de benefício/custo, invariância de escala, colunas nulas e empates.
- Envio manual dos dois arquivos reais pelo navegador: Rapatee, 162,29 ha; Burning Star 3, 530,55 ha. Fotos e análises responderam. Os índices neutros de referência foram 0,974 / 0,719 / 0,013 e 0,981 / 0,306 / 0,010, respectivamente.
- Total inválido desabilitou comparação e ocultou resultado/links desatualizados. AHP conflitante foi recusado; mesma importância foi aceita.
- Os HTMLs simples e técnico da mesma revisão contêm mapa PNG embutido e não contêm scripts. Estrutura e conteúdo foram conferidos em arquivos e testes HTTP. A abertura visual das URLs locais desses HTMLs foi bloqueada pelo navegador automatizado; não se declara inspeção visual desses documentos abertos.
- Abertura medida em 320×640, 390×844, 816×890, 844×390, 1024×768, 1280×720, 1366×768, 1536×824, 1920×1031 e 1920×1080, sem overflow horizontal nem cortes nos rótulos das etapas. Caixa centralizada na vertical nas telas com duas colunas. Verificação por viewport, sem aparelho físico.
- O mapa conservou a poligonal inteira após os redimensionamentos verificados. A foto é histórica; não afirmar imagem atual.

## Limites

Os testes verificam software e coerência do fluxo. Não demonstram validade científica das notas, concordância de especialistas, viabilidade de uso ou homologação de uma mina pela Vale. Não houve estudo geotécnico, análise financeira/social, auditoria externa, teste de carga, execução Linux ou interface QGIS. Há um aviso de depreciação Starlette/TestClient relacionado a HTTPX, sem falha nas verificações anteriores. Não há implantação remota.

Reprodução e ambiente: [README](../README.md) e [Dependências](DEPENDENCIAS.md).

## Revisão geral antes do versionamento — 24/10/2026

A suíte completa passou com 119 testes Python em macOS e 2 testes frontend; TypeScript e build Vite aprovados. Os 11 novos casos cobrem posições 2D/3D em Polygon/MultiPolygon, inteiros extremos em altitude/pesos/AHP e os dois relatórios diante de fotografia alterada, incluindo um manifesto atualizado que diverge da revisão salva. As falhas numéricas não alteram a análise aceita, e uma fonte diferente impede exportação sem reescrever a revisão.

O verificador offline confirmou novamente dez arquivos por pacote, as duas geometrias do GeoPackage e os índices neutros de referência. Vinte arquivos Python foram analisados sintaticamente; links locais e versões diretas do lock frontend foram conferidos. A seleção de arquivos publicáveis passou pela checagem de instruções locais, bancos, dependências, builds e padrões de credenciais. Mantido apenas o aviso já conhecido de depreciação Starlette/TestClient. Não se declara execução Linux, abertura da interface QGIS ou implantação remota.
