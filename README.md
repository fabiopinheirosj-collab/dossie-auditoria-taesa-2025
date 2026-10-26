# Dossiê acadêmico de auditoria — TAESA — Exercício 2025

**Universidade:** Universidade de Brasília (UnB)  
**Disciplina:** Auditoria  
**Preparador/matrícula:** 241038826  
**Data de preparação:** 25/10/2026  
**Natureza:** exercício acadêmico baseado em informações públicas e dados sintéticos; não é auditoria independente e não emite asseguração.

## Estrutura
- `dossie/DOSSIE_AUDITORIA_TAESA_2025.pdf` — dossiê compilado.
- `PT/` — 27 papéis de trabalho individuais: Estrutura Conceitual e NBC TA 200 a 600, conforme roteiro.
- `dados/base_audit_taesa_2025_500k.csv.gz` — base sintética comprimida com 500.000 linhas.
- `documentacao/dicionario_variaveis.csv` — dicionário de dados.
- `documentacao/matriz_cobertura_normas.csv` — cobertura das normas.
- `documentacao/resultado_diagnostico_base.json` — resultado do perfilamento.
- `codigo/gerar_base.py` — código reproduzível de geração da base sintética (semente fixa 42).
- `codigo/analisar_base.py` — código reproduzível de perfilamento, testes e amostragem.
- `planilhas/analises_e_conciliacao_taesa_2025.xlsx` — resumo, amostra de 600 linhas, exceções e dicionário.
- `planilhas/amostra_aleatoria_600.csv` — amostra reproduzível.
- `fontes/fontes_publicas.csv` — links, datas de acesso e localizadores.

## Como reproduzir
Requer Python 3.10+ e as bibliotecas listadas em `requirements.txt`. Execute a partir da raiz do repositório.
```bash
pip install -r requirements.txt
# 1. Gerar/regerar a base sintética de 500.000 registros
python codigo/gerar_base.py
# 2. Reproduzir testes e seleção de amostra
python codigo/analisar_base.py --input dados/base_audit_taesa_2025_500k.csv.gz --out resultados --sample-size 600 --seed 20261025
```
O gerador usa semente fixa (`42`) e grava a base comprimida em `dados/base_audit_taesa_2025_500k.csv.gz`. Para gravar em outro caminho, use `--output caminho/arquivo.csv` (ou `.csv.gz` para compressão). A análise gera resumo CSV/JSON, amostra e exceções entre `flag_inconsistencia_inserida` e `status_auditoria`.

## Base sintética: limitações importantes
A base contém 500.000 registros sintéticos associados à conta modelada “Ativo Financeiro de Contrato de Concessão”. Os dados não são extraídos de sistemas internos da TAESA. Os rótulos de SPE, taxas, vencimentos, valores e status não devem ser tratados como fatos da companhia.

A soma de `valor_presente_contabil_brl` é **R$ 12,582,984,987.38**, enquanto o saldo consolidado público do ativo de contrato de concessão em 31/12/2025 é **R$ 16,886,502,000.00** (circulante + não circulante, conforme DF). A diferença é **R$ 4,303,517,012.62**. Não se deve forçar uma conciliação artificial: a diferença precisa ser explicada por escopo, composição, classificação e/ou premissas antes de qualquer uso em auditoria. A conta no balanço é denominada **ativo de contrato de concessão**; a nomenclatura “ativo financeiro” da base precisa ser alinhada ao modelo contábil e às notas explicativas.

## Classificação dos procedimentos
1. **Realizado com evidência pública:** leitura de demonstrações, relatório do auditor e informações públicas; cálculos aritméticos reproduzíveis.
2. **Planejado por falta de acesso:** testes dependentes de contratos, razão, orçamento, sistemas, atas, advogados, confirmações e controles internos.
3. **Simulado para fins didáticos:** análise sobre base sintética e erros inseridos.

## Fontes centrais
- DF TAESA 2025/2024, com relatório do auditor e notas: https://ri.taesa.com.br/wp-content/uploads/2026/03/TAESA-DFs-31.12.2025.pdf
- Release 4T25/2025: https://ri.taesa.com.br/wp-content/uploads/2026/03/Release-4T25.pdf
- Portal de RI: https://ri.taesa.com.br/

## Nota sobre materialidade
A materialidade usada no dossiê é uma premissa acadêmica provisória: 5% do saldo consolidado de ativo de contrato de concessão para materialidade global e 75% desse valor para materialidade de execução. Ela não substitui julgamento profissional, nem uma análise das necessidades dos usuários e de outras bases possíveis.

## Antes de entregar
- Confira se a matrícula `241038826` está correta antes da publicação.
- Confirme com o professor se aceita a conciliação não alcançada, que está exposta sem ajustes artificiais.
- Revise o alinhamento entre a conta da base e a nomenclatura contábil oficial.
- Não declare como executadas confirmações, entrevistas, inspeções físicas ou testes em sistemas internos.
