#!/usr/bin/env python3
"""
Análises reprodutíveis da base sintética de auditoria TAESA 2025.
Todos os registros da base são sintéticos; não são registros internos da TAESA.
Uso: python analisar_base.py --input ../dados/base_audit_taesa_2025_500k.csv.gz --out ../resultados
"""
import argparse, os, json
import pandas as pd
import numpy as np

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--sample-size", type=int, default=600)
    ap.add_argument("--seed", type=int, default=20261025)
    a=ap.parse_args()
    os.makedirs(a.out,exist_ok=True)
    df=pd.read_csv(a.input)
    required=["id_registro","concessionaria_spe","conta_contabil","data_vencimento",
              "valor_nominal_brl","taxa_juros_a_a","valor_presente_contabil_brl",
              "status_auditoria","flag_inconsistencia_inserida"]
    missing=[c for c in required if c not in df.columns]
    if missing: raise ValueError(f"Colunas ausentes: {missing}")
    sample=df.sample(n=min(a.sample_size,len(df)),random_state=a.seed)
    checks={
      "natureza":"SINTÉTICA - não corresponde ao razão auxiliar real da TAESA",
      "linhas":int(len(df)),
      "ids_duplicados":int(df.id_registro.duplicated().sum()),
      "celulas_nulas":int(df.isna().sum().sum()),
      "valor_nominal_total_brl":round(float(df.valor_nominal_brl.sum()),2),
      "valor_presente_total_brl":round(float(df.valor_presente_contabil_brl.sum()),2),
      "registros_com_flag_inserida":int(df.flag_inconsistencia_inserida.astype(bool).sum()),
      "registros_status_divergente":int(df.status_auditoria.str.contains("Divergência",case=False,na=False).sum()),
      "taxas_fora_intervalo_0_1":int((~df.taxa_juros_a_a.between(0,1)).sum()),
      "valores_presentes_negativos":int((df.valor_presente_contabil_brl<0).sum()),
      "amostra_n":int(len(sample)),
      "amostra_seed":a.seed,
      "amostra_flagged":int(sample.flag_inconsistencia_inserida.astype(bool).sum()),
      "amostra_flagged_pct":round(float(sample.flag_inconsistencia_inserida.astype(bool).mean()*100),4)
    }
    # Compare embedded flag and text status; this tests internal consistency, not accounting validity.
    status_flag_mismatch = (
      df.flag_inconsistencia_inserida.astype(bool) !=
      df.status_auditoria.str.contains("Divergência",case=False,na=False)
    )
    checks["divergencia_flag_status"] = int(status_flag_mismatch.sum())
    df.loc[status_flag_mismatch].to_csv(os.path.join(a.out,"excecoes_flag_status.csv"),index=False)
    sample.to_csv(os.path.join(a.out,"amostra_aleatoria.csv"),index=False)
    pd.DataFrame([checks]).to_csv(os.path.join(a.out,"resumo_testes.csv"),index=False)
    with open(os.path.join(a.out,"resumo_testes.json"),"w",encoding="utf-8") as f:
      json.dump(checks,f,ensure_ascii=False,indent=2)
    print(json.dumps(checks,ensure_ascii=False,indent=2))
if __name__=="__main__": main()
