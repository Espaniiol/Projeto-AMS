As quatro buscas (largura, custo uniforme, profundidade limitada e aprofundamento iterativo) foram rodadas sobre a formulação do AMS, com 7 verificações de ordem de serviço. Todas acharam o mesmo caminho, de custo 6,0 min e 4 ações: as quatro verificações essenciais.

| Busca | Custo | Ações | Nós expandidos | Nós gerados | Prof. máx. | Segundos |
|---|---:|---:|---:|---:|---:|---:|
| largura | 6.0 | 4 | 156 | 294 | 4 | 0.0004 |
| custo_uniforme | 6.0 | 4 | 116 | 230 | 5 | 0.0002 |
| profundidade_limitada(limite=32) | 6.0 | 4 | 5 | 4 | 4 | 0.0 |
| aprofundamento_iterativo(limite=32) | 6.0 | 4 | 107 | 214 | 4 | 0.0003 |

Nenhuma busca achou caminho mais barato que a largura. As essenciais são também as verificações mais baratas, então o caminho com menos ações coincide com o de menor custo. A diferença está só no esforço onde o custo uniforme expande menos nós que a largura porque adia as verificações caras.

A profundidade limitada é recursiva e não tem fronteira, então seus 5 nós expandidos não são comparáveis aos das outras. O acerto vem de as essenciais serem as primeiras da lista, e não de eficiência. O espaço é pequeno (128 combinações) e os tempos são ruído.

Busca mais adequada ao AMS: custo uniforme. O que importa ao técnico é minimizar minutos, e ele garante custo mínimo em qualquer instância, ao contrário da largura, que só minimiza o número de ações.