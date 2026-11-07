# O mapa do meu domínio — conferência (Laboratório 04)

Conjunto: manutencao · 384 dimensões antes da redução
Escolha registrada (slide 55): normalizado · semente da vizinhança: 20260901
Mapas: mapa-do-espaco.png (componentes principais à esquerda, vizinhança à direita) · pontos: mapa-pontos.csv

## Passo 4 — os três pares que você escolheu no mapa (slide 52)

| par | cosseno original | a vizinhança visual |
|---|---|---|
| (35, 36) | +0.9780 | confirma |
| (0, 1) | +0.8866 | confirma |
| (60, 93) | +0.2564 | NÃO confirma |

## As quatro perguntas do slide 53

1. Os dois métodos produzem os mesmos agrupamentos?
R: Não. O PCA forma uma nuvem única, densa à esquerda, e preserva a estrutura global. O t-SNE separa grupos locais e preserva melhor a vizinhança

2. Há grupo que só aparece em um deles?
R: Os pares quase idênticos, como (35, 36) e (30, 31), ficam colados no t-SNE. No PCA aparecem no meio da nuvem, sem destaque.

3. Os vizinhos visuais confirmam no cosseno original?
R: Nem sempre. No t-SNE, 45 de 200 pontos têm como vizinho mais próximo um par com cosseno abaixo de 0,5. Dos meus três pares, dois confirmam e um não, o (60, 93) com 0,2564.

4. O que aconteceria com um vetor novo, fora do conjunto?
R: No PCA a projeção é fixa: subtrai o centro e multiplica pelas componentes. No t-SNE não existe, e o mapa teria que ser refeito.

## O caso em que o mapa enganou (critério do slide 52)

Par e o que a figura sugeria, e o que o cosseno original disse:

R: o par (60, 93). No t-SNE o par aparece colado, mas as frases são "O contato do contator K3 apresentou soldagem dos contatos principais" e "O molde da peça BK-12 está com canal de resfriamento obstruído", e o cosseno original é 0,2564, perto do cosseno médio de duas frases quaisquer (0,205). O mapa aproximou assuntos diferentes.
