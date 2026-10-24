As oito buscas (as quatro não informadas do lab 04 e a gulosa e o A* com as duas heurísticas do lab 05) foram rodadas sobre a formulação do AMS, com 12 verificações de ordem de serviço (4096 combinações possíveis). O caminho ótimo tem custo 6,0 min e 4 ações: as quatro verificações essenciais.

| Busca | Custo | Ações | Nós expandidos | Nós gerados | Prof. máx. | Segundos |
|---|---:|---:|---:|---:|---:|
| largura | 6.0 | 4 | 806 | 2784 | 4 | 0.0066 |
| custo_uniforme | 6.0 | 4 | 624 | 2039 | 6 | 0.0122 |
| profundidade_limitada(limite=32) | 6.0 | 4 | 5 | 4 | 4 | 0.0 |
| aprofundamento_iterativo(limite=32) | 6.0 | 4 | 397 | 964 | 4 | 0.0041 |
| gulosa[admissivel] | 6.0 | 4 | 5 | 42 | 4 | 0.0001 |
| a_estrela[admissivel] | 6.0 | 4 | 30 | 152 | 4 | 0.0003 |
| gulosa[inadmissivel] | 25.0 | 8 | 9 | 68 | 8 | 0.0002 |
| a_estrela[inadmissivel] | 19.0 | 6 | 7 | 57 | 6 | 0.0001 |

Os tempos em segundos ficaram de fora porque variam a cada execução e, na escala de milissegundos, são ruído.

**Dominância das heurísticas.** A heurística admissível (soma dos tempos das essenciais que ainda faltam) domina a inadmissível. Ela nunca superestima o custo restante, então o A* com ela mantém a garantia de otimalidade: devolveu o custo ótimo de 6,0 min expandindo 30 nós, contra 624 do custo uniforme, que equivale a h = 0. Como a admissível vale zero no objetivo e é maior ou igual a zero em todo estado, ela é mais informada que h = 0, e a diferença de 624 para 30 nós é a economia que a heurística traz. A inadmissível parece mais informada e expande menos (7 nós), mas superestima o que falta e abate o que já foi feito duas vezes, e por isso o A* devolveu um caminho de custo 19,0, mais de três vezes o ótimo, e a gulosa chegou a 25,0. Além disso, ela não vale zero no objetivo (fica negativa, pois desconta o que já foi feito). A evidência da instância é clara: economizar nós só vale quando a heurística não superestima, porque errar para mais, uma vez que seja, derruba a otimalidade.

**Ressalvas.** A dominância no sentido estrito (h1 maior ou igual a h2 em todo estado) compara heurísticas admissíveis entre si, então o argumento aqui é admissível contra h = 0 (o custo uniforme) e admissível contra inadmissível pela garantia de otimalidade, não pela altura da estimativa. A gulosa com a admissível também acertou o custo (6,0, com 5 nós), mas sem garantia: ela só olha o que falta e não o que já foi gasto, e acertou porque as essenciais estão no começo da lista. A profundidade limitada continua não comparável (conta entradas na recursão, sem repetidos) e o bom resultado dela depende da ordem da lista de verificações.

**Busca mais adequada ao AMS: A\* com a heurística admissível.** Ela garante o custo mínimo, como o custo uniforme, e expande muito menos nós (30 contra 624), o que importa se o AMS ganhar mais verificações ou fontes. A inadmissível deve ser evitada: parece rápida, mas devolve parecer mais caro sem avisar.
