# agent-spec.md — modelo do meu agente

<!--
Este arquivo é para preencher, não para ler e devolver. As perguntas de cada
seção estão em comentário como este: elas não aparecem na pré-visualização,
aparecem no editor. Responda ABAIXO de cada seção, apagando nada delas.

As seções que ainda não foram vistas em aula ficam de pé, com a linha
"quando se preenche" dizendo o encontro em que isso acontece. O documento
cresce a cada laboratório — o de hoje é o primeiro.

Preencha com exemplos concretos do SEU domínio. Uma linha que funcionaria
para qualquer empresa é uma linha genérica — o exemplo do seu segmento
(agente-spec-exemplo.pdf, no mesmo pacote) mostra o contraste.
-->

**Domínio:** Assistente de Manutenção Segura
**Autor(a):** Guilherme Espaniol Schlickmann · **Última revisão:** 14/10/2026

---

## 1. PEAS

<!-- Perguntas que guiam o preenchimento:
  - Performance: o que conta como sucesso, em uma fórmula? Sobre o quê se
    conta, sobre qual conjunto, quanto é sucesso? Qual termo impede a
    trapaça mais óbvia (fechar rápido sem resolver)?
  - Environment: onde o agente opera? O que existe lá — sistemas, pessoas,
    documentos, ruído? Cite elementos concretos.
  - Actuators: o que o agente pode FAZER? Inclua comunicar e escalar:
    informar a decisão é uma ação, e passar adiante também é.
  - Sensors: o que o agente consegue PERCEBER? Só o que ele enxerga existe
    para ele.
  Um PEAS que menciona tecnologia de solução (banco vetorial, nome de modelo)
  está descrevendo a solução — o PEAS descreve o problema.
-->
**Quando se preenche:** no Laboratório 01, hoje. Refinado na Atividade Orientada.

**Performance:** a fatia de falhas reais antecipadas — ordens de serviço de máquinas que falharam e que o agente classificou como risco alto, divididas pelo total de ordens de máquinas que falharam. Conjunto: os 9.991 registros do AI4I 2020 (10.000 menos os 9 com falha marcada sem nenhum modo), com 330 falhas. Sucesso: acima de 80% — hoje, a melhor regra de um limiar (desgaste > 245 min) antecipa 1,2% (4 de 330). Dois termos contra a trapaça: alarmes falsos (risco alto em máquina que não falhou) abaixo de 15% das ordens sem falha, para que "marcar tudo como alto" não pontue; e zero ordens com intervenção elétrica ou em partes móveis liberadas sem recomendação de bloqueio e etiquetagem (LOTO).

**Environment:** o chão de fábrica com as máquinas-ferramenta de produto L, M e H; o sistema de ordens de serviço, com a descrição da intervenção escrita pelo planejador; os sensores de temperatura do ar e do processo, rotação, torque e desgaste da ferramenta; o histórico de falhas por modo (TWF, HDF, PWF, OSF, RNF); as normas NR-10, NR-12 e NR-35; o técnico de manutenção, com pouco tempo entre uma ordem e outra; o supervisor de segurança, que audita depois. Ruído: registros com falha marcada e sem modo, descrições curtas ou ambíguas, leituras trocadas.

**Actuators:** classificar o risco de falha da máquina (baixo, médio, alto); indicar as normas aplicáveis à intervenção; recomendar ou dispensar o bloqueio e etiquetagem (LOTO) antes de começar; comunicar ao técnico um parecer curto com a justificativa; escalar a ordem ao supervisor de segurança quando os dados forem inconsistentes ou a confiança for baixa; registrar a recomendação para auditoria.

**Sensors:** os campos da ordem de serviço (número, máquina, tipo de produto); a leitura atual dos cinco sensores; o texto livre da descrição da intervenção; o histórico de falhas da máquina; o texto das normas. O que não está nesses canais não existe para o agente: ele não vê a condição da equipe, o estado físico real da máquina, nem se o bloqueio foi de fato aplicado — só o que foi recomendado.

---

## 2. O ambiente em sete dimensões

<!--
Perguntas que guiam o preenchimento (uma por dimensão):
  - Observabilidade: existe algo que muda a decisão e o agente não mede?
  - Número de agentes: existe alguém cujas ações mudam o seu resultado?
    Um humano que reage ao agente conta.
  - Determinismo: a mesma ação no mesmo estado dá sempre o mesmo efeito?
  - Episódico ou sequencial: a decisão de agora afeta as decisões seguintes?
  - Estático ou dinâmico: o ambiente muda enquanto o agente delibera?
  - Discreto ou contínuo: estados e ações são contáveis?
  - Conhecido ou desconhecido: o agente sabe de antemão as regras? (Trata do
    que ele SABE, não do que ele VÊ.)
  Cada classificação vem com uma frase de justificativa — a etiqueta sozinha
  não vale nada.
-->
**Quando se preenche:** no Laboratório 02, no sábado (encontro 2).


| Dimensão | Classificação | Justificativa | O que obriga no projeto |
|---|---|---|---|
| Observabilidade | Parcialmente observável | A condição real da máquina, o histórico de intervenções e o procedimento da equipe não chegam nos sensores | Estado interno; memória e contexto |
| Número de agentes | Multiagente | O técnico decide a última palavra e reage ao parecer, e o supervisor audita depois | Protocolo de comunicação e previsão do outro |
| Determinismo | Estocástico | Falha é rara e multicausal, e o parecer gerado por modelo de linguagem varia | Valor esperado, nova tentativa, tempo máximo |
| Episódico ou sequencial | Episódico | Cada ordem de serviço é avaliada independente das outras | Avaliação por conjunto de casos independentes |
| Estático ou dinâmico | Semidinâmico | A ordem não muda sozinha, mas a espera atrasa a intervenção | Prazo de resposta e resposta parcial aceitável |
| Discreto ou contínuo | Discreto | Risco, normas e LOTO são conjuntos contáveis | Enumeração direta |
| Conhecido ou desconhecido | Conhecido | As NRs e os modos de falha são documentados | Sem fase de exploração |

---

## 3. Tipo de agente pretendido

<!--
Perguntas que guiam o preenchimento:
  - O tipo mais simples que resolve: reativo simples, baseado em modelo,
    baseado em objetivos, baseado em utilidade, ou um deles com aprendizagem?
  - A caracterização do ambiente (seção 2) é que decide — parcialmente
    observável elimina o reativo simples.
  - Justifique com a dimensão do ambiente que obriga a escolha.
-->
**Quando se preenche:** no sábado (encontro 2, manhã).

[o tipo mais simples que resolve, justificado pela dimensão
do ambiente que o obriga]

---

## 4. Medida de desempenho

<!--
Perguntas que guiam o preenchimento:
  - A fórmula do campo Performance, agora em definição operacional: como se
    calcula, passo a passo, sem ambiguidade?
  - Métrica primária e duas secundárias. As secundárias pegam o que a
    primária deixa passar (custo, latência, reabertura).
  - O conjunto de casos: de onde vêm, quantos são, de que período.
  - O limiar de sucesso e o valor de hoje.
-->
**Quando se preenche:** a fórmula começa no Laboratório 01; a definição
operacional completa — primária, secundárias, conjunto e limiar — é item da
Atividade Orientada.

[métrica primária e duas secundárias, cada uma com: como se
calcula, sobre qual conjunto, qual o limiar de sucesso e o
valor de hoje]

---

## 5. Restrições

<!--
Perguntas que guiam o preenchimento:
  - Latência aceitável: a partir de quantos segundos a resposta perde valor?
  - Custo aceitável: quanto pode custar cada resolução?
  - O que o agente jamais pode fazer: a ação irreversível que ele não executa
    sozinho. Esta linha vira política em D12.
  - A troca que você aceita: quanto de qualidade por quanto de custo?
    Um exemplo numérico vale mais que a fórmula.
-->
**Quando se preenche:** na Atividade Orientada.

[latência aceitável, custo aceitável, o que o agente jamais
pode fazer sozinho, e a troca qualidade × custo que você
aceita — com um exemplo numérico]

---

## 6. Catálogo de ações

<!--
Perguntas que guiam o preenchimento:
  - Para cada ação: nome, entrada, saída, é reversível?, qual o risco se
    errar? As quatro colunas são obrigatórias — "baixo" não é descrição de
    risco.
  - Ações de leitura E de escrita: as que alteram o mundo são as que exigem
    cuidado, e são justamente as que mais ficam de fora.
  - Este catálogo é, literalmente, a lista de ferramentas que você vai
    implementar em D10.
-->
**Quando se preenche:** na Atividade Orientada — o pacote `D2-07` traz o
modelo da tabela e dois exemplos preenchidos.

[tabela: nome · entrada · saída · é reversível? · risco se
errar — ações de leitura e de escrita]

---

## 7. Formulação por busca

<!--
Perguntas que guiam o preenchimento:
  - Qual fatia do problema é um espaço de estados? (Nem toda fatia é — e
    reconhecer a que não é vale tanto quanto formular a que é.)
  - Os cinco componentes: estado inicial, ações, modelo de transição, teste
    de objetivo, custo de caminho. Comece pelo teste de objetivo.
  - O estado descreve a SITUAÇÃO, não a história de como se chegou nela.
-->
**Quando se preenche:** no Laboratório 03, sábado à tarde (encontro 2).

A fatia do problema que é busca: **em que ordem fazer as verificações de uma ordem de serviço** antes de classificar o risco da máquina — o subproblema 1 do catálogo, com os dados do AMS. 
Os cinco componentes:

| Componente | No AMS |
|---|---|
| Estado inicial | Nenhuma verificação feita |
| Ações | Fazer a próxima verificação ainda não feita (desgaste, temperatura, potência, desgaste x torque, histórico, descrição, tipo de produto) |
| Transição | Soma a verificação às feitas; se positiva, soma também às positivas |
| Teste de objetivo | As quatro verificações essenciais, que distinguem os modos TWF, HDF, PWF e OSF, todas feitas |
| Custo | O tempo de cada verificação, em minutos |

O estado é o par (feitas, positivas), cada um como tupla ordenada — a situação, nunca a ordem em que as verificações foram feitas. O que **não** é busca no AMS: a decisão de exigir LOTO é regra, e comunicar o parecer ao técnico é política. A formulação é a classe `Diagnostico` do catálogo (subproblema 1), com os dados do AMS e validações na construção (lista vazia, nomes repetidos, tempo não positivo, nenhuma essencial). Passa nas seis verificações do teste de sanidade (`verificar-formulacao.py`). O código:

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Verificacao:
    """Uma verificação que o diagnóstico pode fazer."""

    nome: str
    tempo: float      # custo de executá-la (minutos)
    positivo: bool    # o resultado NESTE caso (o caso é fixo)
    essencial: bool   # precisa entrar no laudo para a confiança suficiente


VERIFICACOES_AMS: tuple[Verificacao, ...] = (
    Verificacao("conferir desgaste da ferramenta acima de 200 min", 1.0, True, True),
    Verificacao("conferir diferença de temperatura abaixo de 8,6 K", 1.0, False, True),
    Verificacao("conferir potência fora da faixa de 3.500 a 9.000 W", 2.0, False, True),
    Verificacao("conferir desgaste x torque acima do limite do produto", 2.0, False, True),
    Verificacao("consultar o histórico de falhas da máquina", 5.0, True, False),
    Verificacao("ler a descrição da intervenção na ordem", 3.0, False, False),
    Verificacao("confirmar o tipo de produto (L, M ou H)", 0.5, False, False),
    Verificacao("conferir a rotação atual contra a faixa nominal da máquina", 1.0, False, False),
    Verificacao("conferir a temperatura do ar com a do ambiente da planta", 1.5, False, False),
    Verificacao("conferir a data da última manutenção preventiva", 2.0, False, False),
    Verificacao("verificar se o bloqueio (LOTO) já está aplicado", 3.0, False, False),
    Verificacao("consultar o supervisor sobre o procedimento da equipe", 8.0, False, False),    
)


class Diagnostico:
    """O problema de busca: em que ordem fazer as verificações de uma OS.

    O estado é o par (verificações feitas, verificações positivas), cada um
    como tupla ordenada: a situação, nunca a ordem em que se chegou nela.
    """

    def __init__(self, verificacoes: tuple[Verificacao, ...]):
        if not verificacoes:
            raise ValueError("lista de verificações vazia: o problema não tem ações")
        nomes = [v.nome for v in verificacoes]
        repetidos = sorted({n for n in nomes if nomes.count(n) > 1})
        if repetidos:
            raise ValueError(f"nomes de verificação repetidos: {repetidos}")
        for v in verificacoes:
            if v.tempo <= 0:
                raise ValueError(f"tempo deve ser positivo em {v.nome!r}: {v.tempo}")
        if not any(v.essencial for v in verificacoes):
            raise ValueError("nenhuma verificação essencial: o objetivo já vale no início")
        self.verificacoes = verificacoes
        self._por_nome = {v.nome: v for v in verificacoes}
        self.estado_inicial: tuple[tuple[str, ...], tuple[str, ...]] = ((), ())

    def _verificacao(self, acao: str) -> Verificacao:
        if acao not in self._por_nome:
            raise ValueError(f"ação desconhecida: {acao!r}")
        return self._por_nome[acao]

    def acoes(self, estado: tuple[tuple[str, ...], tuple[str, ...]]) -> list[str]:
        feitas, _ = estado
        return [v.nome for v in self.verificacoes if v.nome not in feitas]

    def transicao(
        self, estado: tuple[tuple[str, ...], tuple[str, ...]], acao: str,
    ) -> tuple[tuple[str, ...], tuple[str, ...]]:
        feitas, positivas = estado
        verificacao = self._verificacao(acao)
        novas_feitas = tuple(sorted((*feitas, acao)))
        if verificacao.positivo:
            return novas_feitas, tuple(sorted((*positivas, acao)))
        return novas_feitas, positivas

    def objetivo(self, estado: tuple[tuple[str, ...], tuple[str, ...]]) -> bool:
        feitas, _ = estado
        essenciais = {v.nome for v in self.verificacoes if v.essencial}
        return essenciais.issubset(feitas)

    def custo(
        self,
        estado: tuple[tuple[str, ...], tuple[str, ...]],
        acao: str,
        estado_seguinte: tuple[tuple[str, ...], tuple[str, ...]],
    ) -> float:
        return self._verificacao(acao).tempo

    def heuristica_admissivel(
        self, estado: tuple[tuple[str, ...], tuple[str, ...]],
    ) -> float:
        """Soma dos tempos das essenciais que ainda faltam (nunca superestima)."""
        feitas, _ = estado
        return sum(v.tempo for v in self.verificacoes
                   if v.essencial and v.nome not in feitas)

    def heuristica_inadmissivel(
        self, estado: tuple[tuple[str, ...], tuple[str, ...]],
    ) -> float:
        """O que falta vale 3x e o que foi feito abate 2x: superestima, não é admissível."""
        feitas, _ = estado
        faltam = sum(v.tempo for v in self.verificacoes
                     if v.essencial and v.nome not in feitas)
        ja_feito = sum(self._por_nome[nome].tempo for nome in feitas)
        return 3.0 * faltam - 2.0 * ja_feito


MEU_PROBLEMA = Diagnostico(VERIFICACOES_AMS)
```

