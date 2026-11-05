"""Testes do agente de linha de base: as regras e a medição sobre os 30 casos."""

from __future__ import annotations

from ams.baseline import CAMINHO_DOS_CASOS, carregar_casos, decidir, medir

LEITURA_NORMAL = {
    "tipo": "M", "temperatura_ar": 298.1, "temperatura_processo": 308.6,
    "rotacao": 1551, "torque": 42.8, "desgaste": 0,
}


def leitura(**mudancas) -> dict:
    return {**LEITURA_NORMAL, **mudancas}


def test_leitura_normal_e_risco_baixo() -> None:
    assert decidir(leitura()) == "baixo"


def test_desgaste_no_limite_e_risco_alto() -> None:
    assert decidir(leitura(desgaste=200)) == "alto"
    assert decidir(leitura(desgaste=199)) == "baixo"


def test_delta_t_baixo_so_conta_com_rotacao_baixa() -> None:
    baixo_dt = {"temperatura_processo": 306.0}  # delta de 7,9 K
    assert decidir(leitura(rotacao=1300, **baixo_dt)) == "alto"
    assert decidir(leitura(rotacao=1500, **baixo_dt)) == "baixo"


def test_potencia_fora_da_faixa_e_risco_alto() -> None:
    assert decidir(leitura(torque=10.0, rotacao=2678)) == "alto"   # ~2.800 W
    assert decidir(leitura(torque=66.0, rotacao=1400)) == "alto"   # ~9.700 W


def test_sobrecarga_depende_do_tipo_de_produto() -> None:
    sobrecarga = {"desgaste": 190, "torque": 60.0, "rotacao": 1400}
    assert decidir(leitura(tipo="L", **sobrecarga)) == "alto"   # 11.400 > 11.000
    assert decidir(leitura(tipo="M", **sobrecarga)) == "baixo"  # 11.400 < 12.000


def test_conjunto_tem_30_casos_com_atipicos() -> None:
    casos = carregar_casos(CAMINHO_DOS_CASOS)
    categorias = {c["categoria"] for c in casos}
    assert len(casos) == 30
    assert {"falha", "facil", "dificil", "atipico"} <= categorias
    assert sum(c["categoria"] == "atipico" for c in casos) >= 2


def test_medicao_devolve_a_metrica_primaria() -> None:
    resultado = medir()
    assert resultado["total"] == 30
    assert resultado["com_falha"] + resultado["sem_falha"] == 30
    assert 0.0 <= resultado["taxa_antecipadas"] <= 1.0
    assert resultado["falhas_antecipadas"] <= resultado["com_falha"]
    assert resultado["com_falha"] == 11
