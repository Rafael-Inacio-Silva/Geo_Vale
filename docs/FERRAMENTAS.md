# Ferramentas utilizadas e justificativas

Registro de 26/10/2026, correspondente à versão 3.5.0. Escopo demonstrado: abrir o mapa em Minas Gerais, localizar a Mina Horizontes e explorar cinco temas estaduais, consultar trilhas municipais e delimitar várias áreas de estudo, consultar o cadastro ANM e mostrar o município selecionado pelo IBGE, além de extrair dados de água na AID fixa. As escolhas abaixo se referem ao que está implementado no projeto.

## Aplicação

| Necessidade | Ferramenta | Justificativa no GeoVale | Resultado demonstrável |
|---|---|---|---|
| Organizar a interface e suas interações | React | Divide pesquisa, mapa e controles de camadas em componentes, com estado compartilhado para seleção e intensidade. | Marcar uma camada atualiza o mapa; selecionar a mina atualiza o painel e o enquadramento. |
| Conferir os contratos da interface durante o desenvolvimento | TypeScript | Define os tipos de mina, configuração e camadas e verifica seu uso na compilação. A validação de dados externos continua no backend. | Verificação de tipos antes da geração da interface compilada. |
| Apresentar uma interface limpa e responsiva | HTML e CSS | Permitem controlar identidade visual, margens, foco, tamanhos e organização conforme a janela. | Painel amplo, controles legíveis e adaptação entre desktop e celular. |
| Navegar no mapa e combinar imagens geográficas | Leaflet | Reúne fundos, zoom, marcador, contorno e suporte WMS na biblioteca já utilizada pelo projeto. | Alternância Mapa/Satélite, seis controles independentes, intensidade e legendas. |
| Desenhar e ajustar a área de estudo | Leaflet.draw 1.0.4 | Reaproveita o mapa Leaflet com desenho e edição de vértices; controles React mantêm a identidade visual. | Fechar, ajustar, confirmar, cancelar e redesenhar o polígono. |
| Organizar a lógica do servidor | Python | Implementa o cadastro territorial, a consulta externa e a preparação da geometria no mesmo ambiente do backend. | Disponibilização da configuração e do contorno para a interface. |
| Disponibilizar dados por HTTP | FastAPI | Expõe configuração, contorno, trilhas, saúde e validação geométrica local, servindo a interface na mesma origem. | O navegador consulta `/api/mapa` e `/api/mapa/limite-mg`. |
| Executar o serviço local | Uvicorn | É o servidor usado por `executar.py` para iniciar a aplicação FastAPI. | Aplicação acessível em `http://127.0.0.1:8000`. |
| Preparar a geometria oficial para exibição | Shapely | Prepara o contorno estadual para exibição, confere linhas municipais, valida o desenho manual e intersecta água com a AID fixa. Para o desenho, rejeita erros sem reparo automático. | Contorno estadual válido e mais leve para a navegação. O tratamento não certifica limites nem precisão cadastral. |

Evidências no código: [App](../frontend/src/App.tsx), [controles de camadas](../frontend/src/CamadasTerritorio.tsx), [mapa Leaflet](../frontend/src/MapaTerritorio.tsx), [API](../backend/geovale/api/main.py), [preparação do contorno](../backend/geovale/mapa.py) e [execução](../executar.py).

## Fontes geográficas

| Fonte | Uso efetivo | Justificativa e limite |
|---|---|---|
| OpenStreetMap | Fundo Mapa, com ruas e localidades. | Contexto cartográfico para navegação, com atribuição e respeito à política de uso do serviço público. |
| Esri World Imagery | Fundo Satélite. | Contexto visual aproveitando a integração existente. Data e resolução variam por lugar e zoom; a imagem não comprova a condição atual da mina. |
| Prefeitura de Nova Lima / ArcGIS REST | Trilhas cadastradas por consulta GeoJSON da região visível e cores/nomes pelo renderer do item oficial. | Testa uma segunda infraestrutura oficial. Cobertura municipal, cadastro sem garantia de acesso ou segurança. |
| ANM / SIGMINE — ArcGIS REST | Processo associado à Horizontes, titular, fase e área cadastrada, sem geometria. | Fonte primária cadastral, sem copiar o portal nem presumir perímetro físico ou situação operacional. |
| IBGE — API de malhas | Contorno de Nova Lima na seleção da mina. | Fonte oficial para contexto municipal, simplificada para web, sem carregar todas as cidades ou certificar limites locais. |
| IDE-Sisema | Serviço de acesso ao contorno estadual e às dez bases dos cinco temas. | Integração com uma infraestrutura pública oficial de Minas Gerais, com identificadores e legendas documentados. Os produtores dos dados são identificados separadamente. |

A IDE-Sisema distribui dados de diferentes instituições. O contorno tem origem nos limites da FJP. Os cinco temas reúnem INPE/Topodata, ANA/Igam, UFV/Cetec/UFLA/Sisema, MapBiomas, IEF/ICMBio/municípios e IBGE/DNIT. **Leaflet mostra os dados; esses fornecedores produzem ou disponibilizam os dados.**

Vale, FEAM, OpenStreetMap e o cadastro minerário da ANM sustentam a identificação e a proveniência dos dados da Horizontes descritas em [Dados geográficos](DADOS_GEOGRAFICOS.md). O cadastro da única mina fica em `dados/minas.json`; a identificação lê esse cadastro local; dados cadastrais atuais vêm da ANM e o limite municipal vem do IBGE.

Mantivemos os fundos atuais para concentrar o MVP na integração e exploração das informações. Os serviços públicos têm condições de uso e disponibilidade; não foram classificados como ilimitados. A decisão sobre Google, 3D e atualidade das imagens está registrada em [Escolhas territoriais](ESCOLHAS_TERRITORIAIS.md).

## Padrões de integração e formatos

WMS e WFS são padrões de serviço geográfico, não programas que substituem o Leaflet ou a IDE-Sisema.

| Padrão ou formato | Como é usado | Por que foi escolhido nesta etapa |
|---|---|---|
| WFS 2.0.0 | O backend consulta o limite de MG e, sob demanda, duas bases vetoriais de água na extensão da AID. | Permite obter a geometria e conferir sua identificação, referência espacial e extensão antes de exibi-la. |
| ArcGIS REST Query | Consulta trilhas pelo backend com bbox e `outSR=4326`, e o processo associado na ANM; a configuração do item municipal fornece o renderer por nome. | Integra dados de outra infraestrutura sem Selenium ou cópia integral do portal. |
| GeoJSON | Formato do contorno, linhas municipais e polígono manual entre a API e o mapa. | Mantém geometrias consumidas pelo Leaflet e validadas no servidor. Nesta etapa o engenheiro escolhe a mina no catálogo, sem envio de arquivo. |
| WMS 1.1.1 | O navegador solicita imagens transparentes dos temas e suas legendas oficiais. | Permite combinar as bases na região visível, carregando cada tema somente quando marcado. |
| Tiles de fundo | Blocos de imagem de OpenStreetMap ou Esri solicitados conforme região e zoom. | Permitem navegação mundial sem baixar previamente um mapa mundial completo. |
| HTTPS e JSON | Comunicação com fontes e entrega da configuração territorial. | Contratos explícitos para configuração, identificação das bases e tratamento de falhas. |

O WMS entrega a representação visual, enquanto o WFS fornece a geometria do contorno e os registros vetoriais para extração de água. As sobreposições atuais apoiam exploração regional; as fontes, suas datas e suas escalas precisam ser consideradas na interpretação.

## Preparação, verificação e versionamento

| Ferramenta | Papel atual | Justificativa |
|---|---|---|
| Node.js e npm | Ambiente e gerenciamento dos pacotes da interface; execução dos comandos de desenvolvimento e teste. | Dependências e comandos reproduzíveis por meio de `package.json` e do lock. Node não precisa permanecer em execução para servir o build pelo backend. |
| Vite | Servidor de desenvolvimento e compilação da interface. | Gera os recursos estáticos servidos pela aplicação local. |
| Ambiente virtual Python e pip | Isolamento e instalação das dependências do backend. | Preservam o ambiente pessoal e permitem instalar os pacotes fixados com hashes. |
| pytest + TestClient/HTTPX | Testes da API, fonte externa simulada, cache, falhas e integridade do catálogo. | Conferem os contratos e situações de indisponibilidade sem depender da disponibilidade do fornecedor em cada teste. |
| Test runner do Node | Testes da pesquisa da única mina. | Verifica nome atual/anterior, normalização da busca e ausência de correspondência. |
| TypeScript e build | Verificação de tipos e geração da interface. | Conferem a integração do código antes de executar a versão compilada. |
| Navegador | Verificação funcional e visual com as fontes reais. | Confirma carregamento, sobreposição, retirada, legendas, recuperação e responsividade que os testes isolados não demonstram sozinhos. |
| Git | Controle de versões e revisão das alterações locais. | Permite acompanhar mudanças e conferir diferenças. |
| GitHub | Repositório remoto do projeto. | Organiza o compartilhamento do código versionado. Esta entrega é versionada e enviada ao remoto por solicitação do usuário, mantendo a execução local. |

Versões e instalação em [Dependências](DEPENDENCIAS.md). Resultados executados e limites da conferência em [Validação](VALIDACAO.md); esta lista de ferramentas não equivale a uma nova execução dos testes.

## Explicação curta para apresentação

> “Construí a interface com React e TypeScript e usei Leaflet para navegar no mapa e sobrepor informações. O backend Python com FastAPI organiza o acesso aos dados, e o Shapely prepara o contorno estadual para visualização. Integrei bases públicas da IDE-Sisema por serviços geográficos padronizados, mantendo a origem dos dados identificada. Assim, o protótipo permite explorar o território da Mina Horizontes e combinar cinco temas relevantes ao contexto pós-mineração, incorporar trilhas de outra fonte oficial e delimitar várias áreas de estudo. O IBGE fornece o município selecionado e a ANM fornece os atributos cadastrais. A referência vetorial da mina vem do OpenStreetMap e a influência aproximada vem do parecer FEAM; ambas são servidas localmente, com fonte identificada. A confirmação valida a geometria; uma extração independente consulta e recorta dados de água na AID, apresentando contagens e fontes sem produzir diagnóstico.”

A justificativa temática vem dos estudos e referências corporativas reunidos em [Escolhas territoriais](ESCOLHAS_TERRITORIAIS.md). As cinco escolhas são um recorte documental de MVP, ainda sem validação de especialista da Vale. A apresentação deve distinguir a exploração visual implementada da avaliação técnica de usos futuros.

Para organizar posteriormente o roteiro, este registro segue a sequência: **necessidade → ferramenta → justificativa → resultado demonstrável**. A integração municipal está em [Trilhas](TRILHAS_NOVA_LIMA.md), e o desenho em [Área de estudo](AREA_ESTUDO.md). A arquitetura detalhada permanece em [Arquitetura](ARQUITETURA.md).

As ferramentas de áreas ficam na barra esquerda; pesquisa, detalhes e camadas na direita. Ambas podem ser ocultadas por setas sem perder dados da página. A integração [ANM](ANM.md) e o [IBGE](LIMITE_MUNICIPAL.md) usam biblioteca HTTP padrão Python e Shapely existente, sem novos pacotes ou Selenium. A coleção de áreas é memória do navegador, não banco geográfico.

## Referências locais de duas fontes

GeoJSON versionado guarda a área de mineração OpenStreetMap e quatro recortes aproximados do meio físico do parecer. A receita registra pixels e grade UTM; Python/Shapely reproduz o preparo sem nova dependência. A API local entrega os arquivos, sem download externo ao clicar. Essa escolha permite demonstrar integração de evidência documental com bases públicas, mantendo a diferença entre digitalização aproximada, cadastro e desenho pessoal. [Método e limites](REFERENCIAS_TERRITORIAIS.md).

Os modos Manual/Referência/Influência preservam rascunhos e filtros ao alternar. Usar como área adiciona a referência explicitamente ou seleciona a já existente; o último contexto pode permanecer sob o desenho, com opção Ocultar. [Fluxo](AREA_ESTUDO.md).

## Ferramentas da caracterização de água

WFS entrega registros e geometrias; `urllib` e `ThreadPoolExecutor` consultam as duas bases fixas em paralelo; Shapely faz a interseção com a AID documental. React apresenta a contagem por fonte e Leaflet mostra os trechos recortados. Reutilizam-se bibliotecas instaladas, sem Selenium, QGIS obrigatório, banco ou nova contratação. A escolha demonstra integração/automação da vaga. [Evidência e fala da apresentação](EXTRACAO_AGUA.md).
