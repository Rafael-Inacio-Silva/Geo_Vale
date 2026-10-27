# Validação das fichas e prévia

Versão 4.3.0, 27/10/2026, macOS/Python 3.12/Node 24.

## Automatização

96 testes Python aprovados no conjunto completo. Testes Node aprovados, sem falhas. O código da interface não mudou nesta versão, além do número de versão; TypeScript/build não foram reexecutados. Avisos de depreciação Starlette/HTTPX e Rasterio/NumPy permanecem sem falhas.

Os testes novos verificam: campo extra e cota zero aceitos somente quando declarados no catálogo; área das células em UTM 23S igual à extensão projetada da grade; área minerada vinda da classe Mineração, com divisão de linhas, polígonos e pontos entre área minerada e entorno; UCs agrupadas pelo grupo publicado, com ou sem acento; pontos de água conferidos com a classe do trecho mais próximo, classe 2 por padrão e classe especial sem padrão numérico; cenário com ponto, parâmetro, rótulo, referência ou ID inválido recusado. Os testes anteriores derivam do catálogo o número de bases e marcadores.

## Dados e documento reais

As cinco bases novas e a declividade (assinatura alterada pelo novo nome do tema) foram coletadas em 27/10/2026 numa cópia isolada do banco local, com o código 4.3.0. O servidor que estava em execução com o código 4.2.0 não foi reiniciado; o banco do projeto recebe as bases novas quando o servidor for reiniciado.

Resultados da Horizontes: 602 trechos com vazão regionalizada, 603 trechos enquadrados, 6 polígonos de potencial de cavidades, 362 APPs hídricas e 10 barragens, além das bases anteriores. A soma das células medidas em UTM 23S deu 15.309,2 ha na declividade e 15.308,9 ha na cobertura, para um recorte de 15.308,5 ha. Área minerada: 3.173,3 ha; mina OSM: 512,2 ha, dos quais 508,1 ha dentro da área minerada.

A emissão conferida tem 11 páginas, 9 marcadores e 2.168.139 bytes. O texto de todas as páginas foi extraído. Foram renderizadas e inspecionadas a visão geral, relevo, água, entorno, barragens e dados simulados: mapas com área minerada, barragens numeradas pelo código publicado e pontos simulados rotulados; tabelas e fontes legíveis.

## Navegador

Numa instância isolada (porta 8031, cópia do banco), a mina foi selecionada e Influência mostrou as camadas recortadas, com o tema Barragens no painel. Ver relatório abriu a prévia com 11 páginas. Não houve erro no console nem no servidor. O download byte a byte e a falha provocada de imagem foram conferidos na 4.2.0; esse mecanismo não mudou e não foi repetido.

## IA e alcance

A integração OpenAI Responses / GPT-5 nano está preparada, com chave exclusivamente no arquivo local ignorado pelo Git. O arquivo permanece vazio, sem chamada real à OpenAI. O contrato foi testado com respostas controladas; o documento atual identifica comentários por regras. Não houve ML treinado, chamada paga, validação de especialista, ensaio real de água/estabilidade ou decisão de pós-mineração. A camada de ZAS não foi integrada porque a resposta pública excede 32 MiB. [Método](RELATORIO.md), [dados](DADOS_TERRITORIAIS.md), [recorte](INFLUENCIA.md).
