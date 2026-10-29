# Catálogo de minas

Versão 4.8.0, 29/10/2026. O catálogo (`dados/minas.json`) tem a Mina Horizontes e a Mina Abóboras. Cada mina usa o mesmo processamento: 18 bases estaduais recortadas, relatório, sugestão multicritério e explicação por IA. Muda apenas o que é próprio da mina: contorno, recorte, processo ANM e cenário simulado.

## Como acrescentar uma mina

1. Achar a cava no OpenStreetMap (`landuse=quarry`) e o processo da ANM sob ela.
2. Recorte: se houver estudo ambiental público com mapa da área de influência, digitalizar como na Horizontes ([Influência](INFLUENCIA.md)). Sem estudo, `ferramentas/preparar_faixa.py <mina> <way OSM>` gera a faixa de 3 km.
3. Incluir a mina em `dados/minas.json` com fontes, processo ANM e código IBGE do município.
4. Coletar as 18 bases, criar `dados/cenarios/<mina>.json` com os pontos sobre a área minerada e os trechos do Igam.
5. Copiar o banco para `deploy/territorios.sqlite3` e rodar `ferramentas/gerar_prontos.py <mina>`.

## Mina Abóboras

| Item | Valor | Fonte |
|---|---|---|
| Identificação | Vale S.A., Complexo Vargem Grande, Nova Lima, junto à divisa com Rio Acima | [Parecer da Supram CM, PDE Abóboras (PA COPAM 8761/2012/007/2018)](https://sistemas.meioambiente.mg.gov.br/licenciamento/uploads/mev_ITRe4yRcj-BmX_GH79GCBrOd43S4.pdf), p. 3–4 |
| Contorno da cava | Cava da Mina Abóboras, way 315221702, 119,2 ha | [OpenStreetMap](https://www.openstreetmap.org/way/315221702), ODbL |
| Processo ANM | 004.811/1958, Vale S.A., concessão de lavra, ferro, 398,72 ha | SIGMINE: único processo que contém o centro da cava |
| Recorte | Faixa de 3 km em volta da cava: 4.266 ha | `ferramentas/preparar_faixa.py` |
| Bases | 18 de 18 prontas em 29/10/2026 | Coleta local |
| Área minerada no recorte | 1.001,9 ha (23,5%), em 3 setores | MapBiomas 2025, classe Mineração |

## Decisões e porquês

| Decisão | Por quê | Evidência |
|---|---|---|
| Faixa de 3 km em vez da AII da Horizontes | A Abóboras fica dentro da AII de águas e solos da Horizontes; usar o mesmo recorte daria a mesma área minerada, os mesmos setores e o mesmo relatório. Não foi achado estudo público com mapa da área de influência da Abóboras (os pareceres da PDE e da outorga descrevem a mina, mas não trazem esse mapa). | Teste de ponto no contorno da AII; buscas no portal da Semad em 29/10/2026. |
| 3 km | Distância que a Resolução CONAMA 428/2010 (art. 1º, § 2º, regra transitória) usou como entorno de influência de empreendimentos sobre UCs sem zona de amortecimento. É escala de referência, não área de influência legal da mina. | [Resolução CONAMA 428/2010](https://assiste.icmbio.gov.br/cepsul/images/stories/legislacao/Resolucao/2010/res_conama_428-2010_licenc_amb_uc.pdf). |
| Processo ANM pela posição da cava | Não há documento público que ligue a cava a um processo, como na Horizontes. O centro da cava cai em um único processo, de titularidade da Vale, em concessão de lavra de ferro. | Consulta espacial ao SIGMINE em 29/10/2026. |
| Município Nova Lima | A cava fica em Nova Lima, junto à divisa com Rio Acima, como dizem o parecer e o OSM. O contorno municipal exibido é o de Nova Lima. | Parecer da Supram CM; OSM. |
| Cenário simulado com os mesmos valores da Horizontes | Os valores são fictícios e servem para mostrar as entradas técnicas; inventar outros não daria mais informação. Só os pontos mudam, sobre dados reais da Abóboras. | `dados/cenarios/aboboras.json`. |
| Pontos de água pela codificação de bacias da ANA | Os trechos do Igam trazem o código Otto-Pfafstetter (`cobacia`): no mesmo curso, código menor fica a jusante. A1 fica na cabeceira do Córrego Seco, a mais de 1 km de mineração; A2 no Córrego da Volta Grande, logo abaixo da área minerada; A3 no Rio do Peixe, depois da foz do Volta Grande. | Atributos dos trechos enquadrados (Igam). |
| Vídeo depois | O vídeo pós-mineração depende do sobrevoo gravado pelo engenheiro. Até lá, o botão abre o aviso "Vídeo indisponível para esta mina". | [Vídeo pós-mineração](VIDEO_POS_MINERACAO.md). |

## Ajustes no código para a segunda mina

| Ajuste | Por quê |
|---|---|
| A influência aceita `faixa_declarada`, exigindo distância e norma de referência | Antes só havia o recorte digitalizado de estudo, com hash do PDF. |
| Textos do recorte (relatório, território e créditos do mapa) saem do pacote da mina | Eram fixos da Horizontes ("AII", "FEAM / Amplo"). Os da Horizontes ficam no código porque o pacote dela entra na assinatura dos dados coletados: mudá-lo faria o sistema recoletar a Horizontes. |
| Coleção WFS vazia com `crs` nulo é aceita | Sem registros no recorte, o servidor do Estado publica `"crs": null`; UCs federais e municipais não têm registros na faixa da Abóboras. Com registros, o CRS continua obrigatório. |
| Massas d'água com `reparar` declarado | Na faixa da Abóboras a fonte publica uma geometria inválida. Na Horizontes os 16 registros são idênticos com e sem reparo; por isso só a assinatura dessa base foi atualizada no banco, sem recoletar. |
