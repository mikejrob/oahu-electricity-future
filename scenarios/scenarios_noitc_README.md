# No-credit (FEOC) sensitivity

The base case carries the current-law 48E credit (storage + geothermal,
x0.70 capital for 2027-2035 vintages). The no-credit world — relevant if
FEOC material-assistance rules disqualify the battery supply chain or the
credit is repealed — is fully solved: the complete pre-credit scenario set
(184 cells, 0.25% and 0.1% tolerances) is preserved in
`results/RESULTS_SUMMARY_noitc.csv`. `gen_build_costs_noitc.csv` (generated
by the build) reproduces the pre-credit cost basis for re-running any cell:
alias it in place of `gen_build_costs.csv` on any scenario line.
