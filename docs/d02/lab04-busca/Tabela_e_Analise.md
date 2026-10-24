As quatro buscas foram rodadas sobre a formulação do AMS, com 12 verificações de ordem de serviço. Todas acharam o mesmo caminho, de custo 6,0 min e 4 ações: as quatro verificações essenciais.

| Busca | Custo | Ações | Nós expandidos | Nós gerados | Prof. máx. | Segundos |
|---|---:|---:|---:|---:|---:|---:|
| largura | 6.0 | 4 | 806 | 2784 | 4 | 0.0066 |
| custo_uniforme | 6.0 | 4 | 624 | 2039 | 6 | 0.0122 |
| profundidade_limitada(limite=32) | 6.0 | 4 | 5 | 4 | 4 | 0.0 |
| aprofundamento_iterativo(limite=32) | 6.0 | 4 | 397 | 964 | 4 | 0.0041 |

Nenhuma busca achou caminho mais barato que a largura. As essenciais são também as verificações mais baratas, então o caminho com menos ações coincide com o de menor custo, e as verificações extras (todas não essenciais) só somariam custo. A diferença está só no esforço: o custo uniforme expande menos nós que a largura (624 contra 806) porque adia as verificações caras.

A profundidade limitada é recursiva e não tem fronteira, então seus 5 nós expandidos não são comparáveis aos das outras. O acerto vem de as essenciais serem as primeiras da lista, e não de eficiência. O aprofundamento iterativo foi o que menos expandiu entre as comparáveis (397), porque as rodadas rasas são pequenas e a última acerta o primeiro ramo, mas ele repete trabalho a cada rodada. Os tempos são da ordem de milissegundos, então as diferenças em segundos são ruído.

Busca mais adequada ao AMS: custo uniforme. O que importa ao técnico é minimizar minutos, e ele garante custo mínimo em qualquer instância, ao contrário da largura, que só minimiza o número de ações, e da profundidade limitada e do aprofundamento, cujo bom resultado aqui depende da ordem da lista de verificações.