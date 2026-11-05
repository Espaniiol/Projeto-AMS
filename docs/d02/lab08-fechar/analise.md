# Análise — o que torna o problema difícil e que agente ele exige

## O que torna o problema difícil

Três propriedades do ambiente (seção 2 do `agent-spec.md`), cada uma amarrada a algo que apareceu nas medições.

**A observabilidade parcial não é rótulo aqui.** A linha de base perdeu C27 (falha aleatória) e C28 (falha sem modo registrado): os dois têm todos os sensores normais, então a informação que decide a falha não está na leitura do instante. Das 11 falhas do conjunto, as duas únicas que escaparam foram essas.

**O ambiente é estocástico.** Os quatro alarmes falsos (C19 a C22) têm desgaste entre 202 e 238 min, a faixa em que o TWF só ocorre de forma aleatória: a mesma leitura leva a falha numa máquina e não leva noutra. Nos 30 casos, os alarmes falsos chegaram a 4 de 19 (21,1%), acima do limite de 15% do PEAS; na base real foram 678 de 9.661 (7,0%).

**O erro custa de forma assimétrica, e o técnico reage ao parecer.** Uma falha perdida pode ferir quem trabalha na máquina; um alarme falso custa uma parada. Como o técnico decide por último (multiagente), um parecer sem justificativa ou confiante demais é seguido sem questionamento. A dificuldade também aparece na busca: a ordem das 12 verificações tem 4.096 combinações, e o custo uniforme expandiu 624 nós para achar um caminho de 6,0 min que a heurística admissível achou com 30.

## Que tipo de agente o problema realmente exige

O reativo simples **basta para classificar o risco no AI4I**: a linha de base de quatro regras antecipou 329 de 330 falhas (99,7%). Mas esse número é alto por construção, porque os rótulos de HDF, PWF e OSF seguem as mesmas condições que as regras usam, e os erros acima mostram onde ele deixa de bastar. A linha de base não tem estado por uma razão de dado, não de ambiente: o AI4I traz uma leitura por máquina, sem histórico, e cada ordem é avaliada de forma episódica. Isso não contradiz a observabilidade parcial da seção 2; é o limite do que o dado permite.

O ambiente real pede um **agente baseado em modelo**, com estado interno por máquina (histórico de falhas e de intervenções), e **baseado em objetivos** só na fatia da ordem das verificações, onde o A* com heurística admissível dá o custo ótimo. A escolha **obriga** o projeto a ter memória por máquina, valor esperado e nova tentativa (ambiente estocástico) e um protocolo de comunicação com o técnico e o supervisor (multiagente). Ela **dispensa** avaliar trajetórias inteiras (ambiente episódico, basta um conjunto de casos independentes) e uma fase de exploração (ambiente conhecido: as NRs e os limiares são documentados).

## O que isto muda no projeto

A D10 precisa trazer o que as regras não enxergam: o **histórico por máquina** (novo dado) e a **descrição da intervenção** (texto, que decide a norma e o LOTO). Esse é o ganho possível sobre a linha de base, e não os limiares, que as regras já cobrem. A linha de base é competitiva onde os rótulos são gerados por regra (99,7% de falhas antecipadas, 7,0% de alarmes falsos na base real), e isso é informação valiosa, não fracasso: qualquer agente mais caro precisa superar esse número para se justificar.
