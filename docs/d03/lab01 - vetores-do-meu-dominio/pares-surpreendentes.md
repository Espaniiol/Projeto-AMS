# Pares que surpreenderam — Laboratório 01

> O slide 19 do D3-E1 pede DOIS casos anotados: um par PRÓXIMO sem razão
> aparente e um par DISTANTE que deveria estar junto. Eles voltam na D7,
> quando a turma montar o próprio índice de recuperação — escreva aqui e
> guarde este arquivo no seu repositório.

Conjunto: `dados/manutencao` (200 frases, 384 dimensões). Cossenos medidos sem normalizar (o cosseno é o mesmo com `NORMALIZAR = True`).

## Um par PRÓXIMO sem razão aparente

- Índices do par: (35, 36)
- As duas frases:
  - primeira: Afrouxe os parafusos do mancal em ordem cruzada antes de remover a tampa.
  - segunda: Aperte os parafusos do mancal em ordem cruzada antes de remover a tampa.
- Cosseno medido: 0,9780 (o par mais parecido dos 19.900 pares)
- Por que essa proximidade surpreendeu:

R: As duas frases mandam fazer ações opostas (afrouxar e apertar) e, ainda assim, são o par mais parecido de todo o conjunto. O que as aproxima é tudo o que elas têm em comum — parafusos, mancal, ordem cruzada, tampa — e a única palavra que as distingue pesa quase nada na comparação. Os pares (30, 31), abra e feche a válvula de alívio (cos 0,9426), e (32, 33), suba e baixe a pressão (cos 0,9348), seguem o mesmo padrão. Para um índice de recuperação do AMS isso é um risco, uma pergunta sobre como afrouxar poderia devolver ao técnico a instrução de apertar, e em manutenção segura uma instrução oposta é um erro, não uma variação.

## Um par DISTANTE que deveria estar junto

- Índices do par: (15, 154)
- As duas frases:
  - primeira: A pista externa do rolamento do ventilador apresenta pitting avançado.
  - segunda: O rolamento do lado oposto ao acoplamento não foi substituído na última intervenção.
- Cosseno medido: 0,1265 (posição 14.224 de 19.900, no terço mais distante)
- Por que essa distância surpreendeu:

R: As duas frases tratam do mesmo componente e da mesma decisão de manutenção: um rolamento com dano avançado (pitting) e um rolamento que deveria ter sido trocado e não foi. Um técnico que consulta sobre o primeiro quer encontrar o segundo, porque um é a causa do outro. Mas o modelo as separa, porque elas usam vocabulário diferente (pista externa e pitting, de um lado; lado oposto ao acoplamento e substituído, do outro) e falam de aspectos diferentes do rolamento (o defeito, e o histórico de troca). A comparação mede semelhança de assunto e de palavras, e não a relação de causa entre as duas situações.

## O que a comparação com NORMALIZAR = True mudou

- Alguma ordem mudou? De qual par: não. A ordem dos pares por cosseno é a mesma, e os dez mais parecidos e os dez mais distantes são os mesmos, com os mesmos valores.

R: O cosseno já ignora o comprimento do vetor, então normalizar não o altera. O que mudou foi a distância euclidiana, sem normalizar, ela mistura direção e comprimento (o par 8, cos 0,8024, tem euclidiana 2,30, menor que a dos pares 6 e 7, que têm cosseno maior), ja normalizada, ela passa a ser uma função decrescente do cosseno (‖a−b‖² = 2 − 2·cos), e as duas medidas dão a mesma ordem.
