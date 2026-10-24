# Decisões de projeto

## Rota aprovada em 22/10/2026

Adotar geoprocessamento, critérios explícitos, AHP e TOPSIS. Retirar treinamento, inferência e apresentação de ML do escopo ativo. Os experimentos anteriores não demonstraram capacidade preditiva suficiente para sustentar a sugestão proposta; mudar o algoritmo não resolve a falta de rótulos de adequação e de variáveis essenciais. Usos registrados não equivalem a melhor uso ou viabilidade. Não reescrever experimentos antigos como se tivessem validado esta solução.

A estrutura aproveitada inclui validação GeoJSON, partes/buracos, fontes reais, interface React, Python e armazenamento versionado. Módulos, modelos, bases de treinamento, telas e documentos que descreviam a rota abandonada saem do projeto ativo; uma cópia anterior externa ao repositório permite recuperar o histórico local. Não houve alteração do histórico Git ou publicação remota nesta revisão.

## Escolhas implementadas

- AHP organiza prioridades e verifica consistência; TOPSIS ordena a matriz medida/transformada. Um não substitui o outro.
- Neutralidade inicial evita atribuir pesos fictícios a especialistas. Ajustes manuais têm origem explicitada.
- Perfil territorial exploratório com três indicadores permite demonstrar o fluxo sem fabricar custos ou notas sociais. Associações NLCD e expoentes são hipóteses próprias; não têm validação científica específica.
- Alternativas permanecem Agricultura, Uso florestal e Recreação em áreas abertas. O recorte não avalia lazer aquático.
- Dois recortes reais e offline tornam a demonstração reprodutível. Não prometer ingestão global automática ou funcionamento em mina da Vale sem preparar fontes e revisar parâmetros.
- Imagem aérea local em Leaflet 2D acrescenta contexto com baixo acoplamento. Não usar imagens Google sem integração/licenciamento; não construir 3D apenas para aparência.
- Remover formulário de login da jornada local. Sessão anônima isola dados por navegador; servidor em loopback. A autenticação corporativa é trabalho de implantação, não algo substituído por uma senha embutida no cliente.
- Dois HTMLs autossuficientes representam a mesma revisão salva.

## Validação real ainda necessária

Especialistas deverão revisar alternativas, critérios ausentes, associações de cobertura, escala de relevo, correlação entre indicadores, prioridades e restrições eliminatórias. Estudos ambientais e decisões de partes interessadas são insumos, não uma formalidade depois de uma conclusão automática. Literatura e benchmarking justificam a estratégia; não homologam a implementação ou a decisão de cada mina.

## Entrada manual aprovada em 23/10/2026

A entrada da aplicação ocorre exclusivamente pelo envio do arquivo do computador, pelo seletor ou por arraste. Os dois GeoJSONs da apresentação ficam na pasta local `~/Desktop/Mapas GeoVale/`, fora do código. Mantêm-se as fontes internas de relevo/cobertura/imagem necessárias ao processamento; a foto aérea passa a ser servida por área e sessão após o upload. Essa mudança de experiência não amplia a cobertura geográfica disponível nem valida as regras de decisão.

## Visual editorial — 23/10/2026

Adotar a referência visual enviada pelo responsável: verde-petróleo, amarelo e formas diagonais, com contraste entre a apresentação e a área de envio. Implementação em CSS e elementos vetoriais do próprio frontend, sem imagens remotas, dependências novas ou reprodução da peça publicitária. Aplicar a identidade à jornada completa do dashboard, preservando leitura, responsividade e controles acessíveis.
