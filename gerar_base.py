#!/usr/bin/env python3
"""Gera a base sintética de 500.000 registros para o exercício de auditoria TAESA 2025.

IMPORTANTE: os dados são artificiais e não representam registros internos ou valores reais
por contrato/SPE da TAESA. A semente fixa permite reproduzir os resultados.

Uso a partir da raiz do repositório:
    python codigo/gerar_base.py
    python codigo/gerar_base.py --output dados/minha_base.csv
"""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd


def gerar_base(n_linhas: int = 500_000) -> pd.DataFrame:
    # Configuração para garantir reprodutibilidade
    np.random.seed(42)
    print(f"Iniciando a geração da base simulada com {n_linhas:,} registros para a TAESA...")

    # 1. Geração de IDs e concessões/SPEs ficticiamente atribuídas
    concessoes = [
        "TAESA - Matriz", "Novatrans", "Brasnorte", "Afluente T",
        "ETSE", "SST", "TSN", "ATE I", "ATE II", "ATE III",
        "Mutum", "Lagoa Nova", "San Rondon", "Pico do Itabira"
    ]
    arr_concessoes = np.random.choice(concessoes, size=n_linhas)

    # 2. Identificadores e datas sintéticas
    ids_contrato = [f"CTR-2025-{i:06d}" for i in range(1, n_linhas + 1)]
    datas_vencimento = pd.date_range(
        start="2025-01-01", end="2035-12-31", periods=n_linhas
    )

    # 3. Valores nominais e presentes sintéticos
    valor_nominal = np.random.gamma(shape=2.0, scale=15000.0, size=n_linhas) + 1000.0
    taxa_juros_anual = np.random.uniform(0.06, 0.12, size=n_linhas)
    fator_desconto = 1 / (
        (1 + taxa_juros_anual) ** np.random.uniform(0.1, 5.0, size=n_linhas)
    )
    valor_presente = valor_nominal * fator_desconto

    # 4. Inserção controlada de inconsistências para testes didáticos
    taxa_erro = 0.005
    mascara_erro = np.random.rand(n_linhas) < taxa_erro
    valor_presente[mascara_erro] = (
        valor_presente[mascara_erro]
        * np.random.uniform(1.2, 1.8, size=mascara_erro.sum())
    )

    status = np.array(["Adimplente"] * n_linhas, dtype=object)
    status[mascara_erro] = "Divergência de Cálculo / Requer Ajuste"

    # 5. Montagem do DataFrame (mantém a lógica do código fornecido pelo aluno)
    df_taesa = pd.DataFrame({
        "id_registro": ids_contrato,
        "concessionaria_spe": arr_concessoes,
        "conta_contabil": "Ativo Financeiro de Contrato de Concessão",
        "data_vencimento": datas_vencimento.strftime("%Y-%m-%d"),
        "valor_nominal_brl": np.round(valor_nominal, 2),
        "taxa_juros_a_a": np.round(taxa_juros_anual, 4),
        "valor_presente_contabil_brl": np.round(valor_presente, 2),
        "status_auditoria": status,
        "flag_inconsistencia_inserida": mascara_erro,
    })
    return df_taesa


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", default="dados/base_audit_taesa_2025_500k.csv.gz",
        help="Caminho do CSV de saída; use .gz para gerar CSV comprimido (padrão: %(default)s)."
    )
    parser.add_argument(
        "--rows", type=int, default=500_000,
        help="Quantidade de registros sintéticos (padrão: %(default)s)."
    )
    args = parser.parse_args()
    if args.rows < 1:
        parser.error("--rows precisa ser maior que zero")

    df_taesa = gerar_base(args.rows)
    destino = Path(args.output)
    destino.parent.mkdir(parents=True, exist_ok=True)
    compressao = "gzip" if destino.suffix.lower() == ".gz" else None
    df_taesa.to_csv(destino, index=False, encoding="utf-8", compression=compressao)

    saldo_contabil_total = df_taesa["valor_presente_contabil_brl"].sum()
    inconsistencias = int(df_taesa["flag_inconsistencia_inserida"].sum())
    print("\n--- CONCILIAÇÃO DA BASE SIMULADA ---")
    print(f"Quantidade total de registros: {len(df_taesa):,}")
    print(f"Saldo Contábil Consolidado Simulado: R$ {saldo_contabil_total:,.2f}")
    print(f"Total de registros com inconsistências inseridas (para amostragem): {inconsistencias:,}")
    print(f"\nArquivo gerado com sucesso: '{destino}'")
    print("LEMBRETE: valores e inconsistências são sintéticos, não evidências reais da TAESA.")


if __name__ == "__main__":
    main()
