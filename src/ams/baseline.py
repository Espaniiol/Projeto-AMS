"""Agente de linha de base do AMS: regras explícitas, sem modelo de linguagem.

Percepção (a leitura dos sensores de uma ordem), decisão (regras sobre os
limiares dos modos de falha do AI4I 2020) e ação (o nível de risco). É o
agente reativo simples mais barato que resolve a fatia "classificar o risco
da máquina"; o número que ele mede é a linha de base contra a qual o agente
de D10 será comparado.

Sem estado interno: o AI4I traz uma leitura por máquina, sem histórico, e o
PEAS avalia cada ordem de forma episódica — não há o que lembrar entre casos.

Uso (da raiz do repositório):
    PYTHONPATH=src python3 -m ams.baseline
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

CAMINHO_DOS_CASOS = (
    Path(__file__).resolve().parent.parent.parent / "data" / "casos" / "casos-baseline.csv"
)

# --------------------------------------------------------------------------
# Os limiares — um por modo de falha do dataset (TWF, HDF, PWF, OSF)
# --------------------------------------------------------------------------
LIMITE_DESGASTE = 200            # min — TWF ocorre na faixa de 200 a 240 min
LIMITE_DELTA_T = 8.6             # K — HDF: processo menos o ar abaixo disso...
LIMITE_ROTACAO_HDF = 1380        # rpm — ...e rotação abaixo disso
POTENCIA_MINIMA = 3500.0         # W — PWF: potência fora da faixa [3500, 9000]
POTENCIA_MAXIMA = 9000.0         # W
LIMITE_SOBRECARGA = {"L": 11000, "M": 12000, "H": 13000}  # min·Nm — OSF

RISCO_ALTO = "alto"
RISCO_BAIXO = "baixo"


def potencia_w(registro: dict) -> float:
    """Potência mecânica em watts: torque (Nm) x velocidade angular (rad/s)."""
    return registro["torque"] * registro["rotacao"] * 2 * math.pi / 60


def decidir(registro: dict) -> str:
    """Uma rodada: a leitura entra, o nível de risco sai.

    A primeira regra que casar decide — qualquer modo de falha provável
    basta para risco alto. A ordem das regras não muda o resultado, só
    qual delas é citada.
    """
    if registro["desgaste"] >= LIMITE_DESGASTE:
        return RISCO_ALTO
    delta_t = registro["temperatura_processo"] - registro["temperatura_ar"]
    if delta_t < LIMITE_DELTA_T and registro["rotacao"] < LIMITE_ROTACAO_HDF:
        return RISCO_ALTO
    if not POTENCIA_MINIMA <= potencia_w(registro) <= POTENCIA_MAXIMA:
        return RISCO_ALTO
    if registro["desgaste"] * registro["torque"] > LIMITE_SOBRECARGA[registro["tipo"]]:
        return RISCO_ALTO
    return RISCO_BAIXO


# Colunas do CSV (as originais do AI4I 2020) -> chaves usadas pelas regras
COLUNAS = {
    "UDI": "udi",
    "Type": "tipo",
    "Air temperature [K]": "temperatura_ar",
    "Process temperature [K]": "temperatura_processo",
    "Rotational speed [rpm]": "rotacao",
    "Torque [Nm]": "torque",
    "Tool wear [min]": "desgaste",
    "Machine failure": "falha",
}


def carregar_casos(caminho: str | Path = CAMINHO_DOS_CASOS) -> list[dict]:
    """Lê o CSV de casos rotulados (colunas originais do AI4I) e converte os campos."""
    with Path(caminho).open(encoding="utf-8-sig", newline="") as arquivo:
        linhas = list(csv.DictReader(arquivo))
    casos = []
    for linha in linhas:
        caso = {chave: linha[coluna] for coluna, chave in COLUNAS.items()}
        caso.update(id_caso=linha["id_caso"], risco_correto=linha["risco_correto"],
                    categoria=linha["categoria"])
        caso["udi"] = int(caso["udi"])
        caso["temperatura_ar"] = float(caso["temperatura_ar"])
        caso["temperatura_processo"] = float(caso["temperatura_processo"])
        caso["rotacao"] = int(caso["rotacao"])
        caso["torque"] = float(caso["torque"])
        caso["desgaste"] = int(caso["desgaste"])
        caso["falha"] = int(caso["falha"])
        casos.append(caso)
    return casos


def medir(caminho: str | Path = CAMINHO_DOS_CASOS, decisor=decidir) -> dict:
    """Roda o agente sobre os casos e devolve a métrica primária e as secundárias.

    Primária: falhas antecipadas — dos casos que falharam, a fração que o
    agente classificou como risco alto. Secundária: alarmes falsos — dos
    casos sem falha, a fração classificada como risco alto (o termo que
    impede "marcar tudo como alto").
    """
    casos = carregar_casos(caminho)
    com_falha = [c for c in casos if c["falha"]]
    sem_falha = [c for c in casos if not c["falha"]]
    antecipadas = sum(decisor(c) == RISCO_ALTO for c in com_falha)
    alarmes = [c for c in sem_falha if decisor(c) == RISCO_ALTO]
    perdidas = [c for c in com_falha if decisor(c) != RISCO_ALTO]
    acertos = sum(decisor(c) == c["risco_correto"] for c in casos)
    return {
        "caminho": str(caminho),
        "total": len(casos),
        "com_falha": len(com_falha),
        "sem_falha": len(sem_falha),
        "falhas_antecipadas": antecipadas,
        "taxa_antecipadas": antecipadas / len(com_falha) if com_falha else 0.0,
        "alarmes_falsos": len(alarmes),
        "taxa_alarmes_falsos": len(alarmes) / len(sem_falha) if sem_falha else 0.0,
        "acertos": acertos,
        "falhas_perdidas": perdidas,
        "alarmes": alarmes,
    }


def imprimir(resultado: dict) -> None:
    """A métrica, o valor e o conjunto — e onde o agente erra."""
    r = resultado
    print("Métrica primária: falhas antecipadas (falhas classificadas como risco alto "
          "sobre o total de falhas)")
    print(f"Valor: {r['falhas_antecipadas']}/{r['com_falha']} = "
          f"{round(r['taxa_antecipadas'], 4)}")
    print(f"Secundária — alarmes falsos: {r['alarmes_falsos']}/{r['sem_falha']} = "
          f"{round(r['taxa_alarmes_falsos'], 4)}")
    print(f"Acerto geral (apenas para referência): {r['acertos']}/{r['total']}")
    print(f"Conjunto: {r['caminho']} — {r['total']} casos ({r['com_falha']} com falha, "
          f"{r['sem_falha']} sem falha)")
    if r["falhas_perdidas"]:
        print("Falhas que o agente não antecipou:")
        for c in r["falhas_perdidas"]:
            print(f"  {c['id_caso']} (UDI {c['udi']}, {c['categoria']})")
    else:
        print("Falhas que o agente não antecipou: nenhuma")
    if r["alarmes"]:
        print("Alarmes falsos (risco alto sem falha):")
        for c in r["alarmes"]:
            print(f"  {c['id_caso']} (UDI {c['udi']}, {c['categoria']}, "
                  f"desgaste {c['desgaste']} min)")


if __name__ == "__main__":
    imprimir(medir())
