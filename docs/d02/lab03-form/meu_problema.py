"""Laboratório 03 — o meu subproblema formulado como espaço de estados.

Subproblema 1 do catálogo (diagnóstico): em que ordem fazer as verificações
de uma ordem de serviço do AMS. É a classe `Diagnostico` do catálogo, com os
dados do AMS e validações na construção — o mesmo código da seção 7 do
`agent-spec.md`. Teste de sanidade (seis verificações verdes):

    python meu_problema.py
"""

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


if __name__ == "__main__":
    import importlib.util
    import sys
    from pathlib import Path

    teste = importlib.util.spec_from_file_location(
        "verificar-formulacao",
        Path(__file__).resolve().parent / "verificar-formulacao.py")
    modulo = importlib.util.module_from_spec(teste)
    sys.modules["verificar-formulacao"] = modulo
    teste.loader.exec_module(modulo)
    raise SystemExit(modulo.main([str(Path(__file__)) + ":MEU_PROBLEMA"]))
