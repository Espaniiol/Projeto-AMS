# Anotações — Laboratório 02, a descida à mão

> O critério do slide 11: as quatro perguntas respondidas por escrito, com o
> número que sustenta cada resposta. Preencha a tabela rodando o esqueleto
> com as três taxas do slide 12 e copiando a última linha de cada execução.

## A última linha de cada taxa

| Taxa | Última linha da saída (perda, w, b) |
|---|---|
| 0,001 | passo 200 perda 22462.1 w 215.016 b -17.7381 |
| 0,1 | passo 200 perda 0.752176 w 300.008 b 4.91185 |
| 1,5 | passo 200 perda inf w -3.12216e+190 b 4.826e+189 |

## As quatro perguntas do slide 11

**1. A perda está caindo a cada passo, ou oscilando?**

R: Com a taxa 0,1 ela cai a cada passo, sem oscilar: vai de 284.802 no passo 1 para 36.735, 5.450 e 1.259 nos passos 2 a 4, e chega a 0,752 no passo 53. 
   Com a taxa 0,001 também cai a cada passo, mas devagar (284.802 → 281.149 → 277.543). 
   Com a 1,5 ela não cai: sobe a cada passo.

**2. Ela estabiliza, ou continua descendo até o fim?**

R: Com a taxa 0,1 ela estabiliza em 0,752176 a partir do passo 53 e fica igual até o passo 200; esse valor é o piso, próximo da variância do ruído dos dados. 
   Com a 0,001 ela continua descendo até o fim (22.462 no passo 200, ainda em queda de cerca de 300 por passo), então 200 passos não bastam. 
   Com a 1,5 não estabiliza, explode.

**3. Os pesos encontrados batem com os que geraram os dados?**

R: Com a taxa 0,1, sim: w = 300,008 e b = 4,912, contra os verdadeiros 300 e 5. 
   Com a 0,001, não: w = 215,0 e b = −17,7, ainda longe, porque a descida não terminou. 
   Com a 1,5, não: w = −3,1e190, sem sentido.

**4. Se algo divergiu, qual foi o primeiro passo estranho?**

R: Com a taxa 1,5, o passo 2: a perda subiu de 284.802 para 2,14e7 (cerca de 75 vezes maior), quando deveria cair. A partir daí ela multiplica por cerca de 76 a cada passo (1,6e9 no passo 3, 1,2e11 no passo 4) até estourar o limite do número decimal e virar inf no passo 161.
