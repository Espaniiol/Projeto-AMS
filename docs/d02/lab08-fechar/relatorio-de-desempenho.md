# Relatório de desempenho da linha de base

**Projeto:** AMS — Assistente de Manutenção Segura · **Data:** 29/10/2026

## 1. A métrica primária

**Falhas antecipadas**: entre as ordens de máquinas que falharam, a fração que o agente classificou como risco alto, sobre o total de ordens com falha.

Cálculo: `falhas antecipadas = (ordens com falha classificadas como risco alto) ÷ (ordens com falha)`. Meta do PEAS: acima de 80%. É a medida do efeito no ambiente, não do comportamento do agente. Duas secundárias a acompanham: alarmes falsos (ordens sem falha classificadas como risco alto, sobre as ordens sem falha, meta abaixo de 15%) e acerto geral, só como referência.

## 2. O valor

Saída de `python -m ams.baseline`:

```
Métrica primária: falhas antecipadas (falhas classificadas como risco alto sobre o total de falhas)
Valor: 9/11 = 0.8182
Secundária — alarmes falsos: 4/19 = 0.2105
Acerto geral (apenas para referência): 24/30
```

A primária ficou em **9/11 = 81,8%**, acima da meta de 80%. Os alarmes falsos ficaram em **4/19 = 21,1%**, acima do limite de 15%. Este é o primeiro resultado e é a linha de base contra a qual o agente da D10 será comparado.

## 3. O conjunto

`data/casos/casos-baseline.csv`: **30 casos sintéticos (inventados)**, criados para este laboratório; não é o conjunto de reserva do pacote D2-06. Têm as colunas do AI4I 2020, `UDI` a partir de 90001, e a coluna `origem` vale `sintetico` em todas as linhas. Distribuição: 11 com falha e 19 sem falha, em quatro categorias.

| Categoria | Casos | O que são |
|---|---:|---|
| fácil | 10 | máquinas normais, sem falha |
| falha | 8 | falhas por HDF, PWF, OSF e TWF |
| difícil | 8 | 4 com desgaste de 202 a 238 min sem falha e 4 perto dos limiares sem falha |
| atípico | 4 | falha aleatória (RNF), falha sem modo, ΔT baixo com rotação alta sem falha, e ferramenta nova com falha por calor |

O conjunto é enriquecido de propósito: 37% de falhas, contra 3,4% na base completa do AI4I. Para contexto, a mesma regra sobre a base real (`data/raw`, recorte de 9.991 registros do PEAS) antecipa 329 de 330 falhas (99,7%) e dispara 678 alarmes falsos em 9.661 ordens sem falha (7,0%).

## 4. Onde o agente erra

```
Falhas que o agente não antecipou:
  C27 (UDI 90027, atipico)
  C28 (UDI 90028, atipico)
Alarmes falsos (risco alto sem falha):
  C19 (UDI 90019, dificil, desgaste 202 min)
  C20 (UDI 90020, dificil, desgaste 215 min)
  C21 (UDI 90021, dificil, desgaste 228 min)
  C22 (UDI 90022, dificil, desgaste 238 min)
```

**O padrão.** Os seis erros são de dois tipos e todos concentrados em casos difíceis ou atípicos; nenhum caso fácil nem falha por HDF, PWF ou OSF errou. As duas falhas perdidas (C27, falha aleatória, e C28, falha sem modo registrado) têm todos os sensores normais. Os quatro alarmes falsos (C19 a C22) têm desgaste entre 202 e 238 min, a faixa em que a regra do TWF dispara.

**A hipótese.** O agente só enxerga a leitura do instante e decide por limiares fixos. Na falha aleatória e na falha sem modo, a informação que decide não está nos sensores, então nenhuma regra de limiar a alcança. Na faixa de 200 a 240 min, o TWF ocorre de forma aleatória: a mesma leitura leva a falha numa máquina e não leva noutra, e a regra não tem como distingui-las sem outra informação, como o histórico da máquina. Os rótulos de HDF, PWF e OSF seguem as mesmas condições que as regras usam, então o acerto nesses modos é esperado por construção; a dificuldade real está nos atípicos e no TWF.

## 5. A tabela comparativa de busca

Oito buscas sobre a formulação do AMS (a ordem das verificações de uma ordem de serviço), com 12 verificações, o que dá 4.096 combinações possíveis. O caminho ótimo custa 6,0 min e tem 4 ações: as quatro verificações essenciais.

| Busca | Custo | Ações | Nós expandidos | Nós gerados | Prof. máx. | Segundos |
|---|---:|---:|---:|---:|---:|---:|
| largura | 6.0 | 4 | 806 | 2784 | 4 | 0.0066 |
| custo_uniforme | 6.0 | 4 | 624 | 2039 | 6 | 0.0122 |
| profundidade_limitada(limite=32) | 6.0 | 4 | 5 | 4 | 4 | 0.0 |
| aprofundamento_iterativo(limite=32) | 6.0 | 4 | 397 | 964 | 4 | 0.0041 |
| gulosa[admissivel] | 6.0 | 4 | 5 | 42 | 4 | 0.0001 |
| a_estrela[admissivel] | 6.0 | 4 | 30 | 152 | 4 | 0.0003 |
| gulosa[inadmissivel] | 25.0 | 8 | 9 | 68 | 8 | 0.0002 |
| a_estrela[inadmissivel] | 19.0 | 6 | 7 | 57 | 6 | 0.0001 |

Os tempos em segundos variam a cada execução e, na escala de milissegundos, são ruído; a comparação vale pelos nós.

**A pergunta do item 4.** Sim: o A* com a heurística admissível manteve o custo ótimo (6,0 min) e expandiu muito menos que o custo uniforme, **30 nós contra 624**, uma economia de 594 nós (95%). A heurística (soma dos tempos das essenciais que ainda faltam) nunca superestima o que resta e vale zero no objetivo, então o A* mantém a garantia de otimalidade e ainda descarta quase todo o espaço: das 4.096 combinações, ele só entra nas que continuam a caminho das quatro essenciais. A heurística inadmissível mostra o outro lado: o A* com ela expandiu só 7 nós, mas devolveu custo 19,0 (mais de três vezes o ótimo), e a gulosa chegou a 25,0. Economizar nós só vale quando a heurística não superestima.

**Ressalvas da medição.** A profundidade limitada não é comparável às demais: ela conta as entradas na recursão, sem repetidos, e o resultado bom (5 nós) depende de as essenciais estarem no começo da lista de verificações. A gulosa com a heurística admissível também acertou o custo ótimo, mas sem garantia: ela só olha o que falta e não o que já foi gasto, e acertou por causa da ordem da lista.