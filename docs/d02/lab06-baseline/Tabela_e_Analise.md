# Laboratório 06 — agente de linha de base: relatório de desempenho

## O agente

Agente reativo simples, sem modelo de linguagem e sem estado interno, em `src/ams/baseline.py`. Ele recebe a leitura dos sensores de uma ordem de serviço e devolve o nível de risco (`alto` ou `baixo`). Qualquer uma das quatro regras abaixo, uma por modo de falha do AI4I 2020, basta para risco alto:

| Regra | Modo | Limiar |
|---|---|---|
| Desgaste da ferramenta | TWF | 200 min ou mais |
| Dissipação de calor | HDF | ΔT abaixo de 8,6 K e rotação abaixo de 1380 rpm |
| Potência | PWF | fora da faixa de 3.500 a 9.000 W |
| Sobrecarga | OSF | desgaste × torque acima de 11.000 (L), 12.000 (M) ou 13.000 (H) min·Nm |

Sem estado interno porque o AI4I traz uma leitura por máquina, sem histórico, e o PEAS avalia cada ordem de forma episódica (seção 2 do `agent-spec.md`): não há o que lembrar entre um caso e outro.

## O conjunto

`data/casos/casos-baseline.csv`: **30 casos sintéticos (inventados)**, criados para este laboratório. Não são linhas do AI4I nem o conjunto de reserva do pacote. Usam as mesmas colunas do AI4I 2020; o `UDI` começa em 90001, o `Product ID` tem prefixo `S` e a coluna `origem` vale `sintetico` em todas as linhas, para não se confundirem com dados reais. As colunas `id_caso`, `risco_correto` e `categoria` são do projeto.

O rótulo `Machine failure` segue as regras de geração do AI4I: há falha por HDF, PWF ou OSF quando a condição física do modo é satisfeita; TWF, RNF e falha sem modo foram definidos caso a caso.

| Categoria | Casos | O que são |
|---|---:|---|
| fácil | 10 | máquinas claramente normais, sem falha |
| falha | 8 | falhas por HDF, PWF, OSF (2 de cada) e TWF (2) |
| difícil | 8 | 4 com desgaste de 202 a 238 min sem falha e 4 perto dos limiares sem falha |
| atípico | 4 | falha aleatória (RNF) com sensores normais, falha sem modo, ΔT baixo com rotação alta sem falha, e ferramenta nova com falha por calor |

O conjunto tem 11 falhas em 30 casos (37%), contra 3,4% da base completa do AI4I: ele é enriquecido de propósito, para haver o que medir.

## Resultado

| Métrica | Valor | Meta do PEAS |
|---|---|---|
| **Falhas antecipadas (primária)**: falhas classificadas como risco alto sobre o total de falhas | **9/11 = 81,8%** | acima de 80% |
| Alarmes falsos (secundária): casos sem falha classificados como risco alto | 4/19 = 21,1% | abaixo de 15% |
| Acerto geral (referência) | 24/30 | |

Onde erra:
- **Falhas não antecipadas (2):** C27, uma falha aleatória (RNF) com todos os sensores normais, e C28, uma falha sem modo registrado e também com sensores normais.
- **Alarmes falsos (4):** C19, C20, C21 e C22, todos com desgaste entre 202 e 238 min e sem falha.

Para contexto, a mesma regra sobre a base real completa do AI4I (`data/raw`, recorte do PEAS de 9.991 registros): 329/330 falhas antecipadas (99,7%) e 678/9.661 alarmes falsos (7,0%). Nessa base, as metas do PEAS são cumpridas.

## Análise

O agente erra de duas formas sistemáticas. Perde as falhas que não deixam rastro nos sensores (RNF e falha sem modo, C27 e C28) e dispara alarme falso em toda máquina com desgaste entre 200 e 240 min, porque o TWF só ocorre de forma aleatória nessa faixa. É o limite de um agente reativo de limiares fixos: ele só enxerga o que os sensores mostram e não distingue a máquina desgastada que vai falhar da que não vai.

Os números do conjunto não devem ser lidos como o desempenho esperado em produção. Os casos são sintéticos e enriquecidos com falhas e casos difíceis, e os rótulos de HDF, PWF e OSF seguem as mesmas regras que o agente usa, então o acerto nesses modos é esperado por construção; a dificuldade real está nos casos de TWF e nos dois atípicos. Por isso a linha de base é lida junto com o conjunto sobre o qual foi medida e com o resultado na base real.

## Limites desta medição

- **Dados sintéticos:** o conjunto foi inventado para o laboratório, não vem de medições reais; o resultado na base real do AI4I está citado só como contexto.
- **Rótulos circulares:** HDF, PWF e OSF são rotulados pelas mesmas condições que o agente usa, então o recall nesses modos é alto por construção.
- **Conjunto pequeno:** com 11 falhas, cada falha vale cerca de 9 pontos percentuais de recall; um intervalo de confiança só viria na D3.
- **LOTO não medido:** o AI4I não tem descrição da intervenção nem registro de bloqueio, então o critério do PEAS "zero ordens com intervenção elétrica ou em partes móveis liberadas sem LOTO" não pode ser avaliado aqui.
- **Duas classes:** o agente só devolve risco alto ou baixo; o nível médio do PEAS não é usado.
