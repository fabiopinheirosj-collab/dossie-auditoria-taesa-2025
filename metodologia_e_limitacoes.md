# Metodologia e limitações

## Conta selecionada
O ativo de contrato de concessão foi escolhido por ser a maior conta do ativo consolidado na demonstração de 31/12/2025: circulante R$ 1,701.687 milhões e não circulante R$ 15,184.815 milhões. A NE 7 e o relatório do auditor identificam julgamentos significativos na mensuração.

## Premissas da base
O CSV possui 500.000 linhas, com IDs sintéticos, 14 rótulos de concessionária/SPE, datas de vencimento de 2025 a 2035, valores nominais, taxas anuais, valores presentes sintéticos, status e flag de inconsistência inserida. Não foi gerado a partir de razão real. A origem exata dos valores não pode ser validada com base no arquivo isolado; portanto, não se atribui a eles representatividade estatística de saldos da companhia.

## Conciliação
Valor presente sintético total: R$ 12,582,984,987.38. Saldo público do ativo de contrato de concessão consolidado: R$ 16,886,502,000.00. Diferença: R$ 4,303,517,012.62. Diferença não explicada; requer detalhamento da população e unidade de medida. Não ajustar a base para igualar o saldo público.

## Testes
- Integridade: linhas, colunas, nulos, IDs duplicados.
- Consistência interna: comparar flag booleana e status textual.
- Amostragem: amostra aleatória simples de 600 registros, seed 20261025.
- Exceções: armazenadas em CSV para rastreabilidade.
- Limitação: não há recálculo substantivo do valor presente por falta de data-base/modelo contratual real validado; testes estruturais não comprovam mensuração correta.

## Materialidade didática
5% do saldo público da conta foco para materialidade global; 75% da global para materialidade de execução. Percentuais sujeitos a avaliação profissional em auditoria real.
