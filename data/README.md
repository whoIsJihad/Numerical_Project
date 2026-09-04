# Input datasets

CSV format (SI units):

```csv
voltage_v,current_a
0.0,5.0
0.3,4.5
0.5,2.0
```

These numbers illustrate the format only; they are **not** a benchmark or a verified
SDM-generated dataset. No benchmark measurements are bundled in this scaffold.

M1 obtains one legitimate single-cell dataset first and records beside it:
source URL/citation, reuse terms, temperature in kelvin, series-cell count,
original units, preprocessing and dataset name. Verify these before fitting.
Do not assume module measurements use `cells_in_series=1`.

Small, shareable source CSVs may be committed. Restricted data goes in ignored
`data/private/` and must not appear in PRs. Generated plots/results go in `outputs/`.
