# Ownership and first assignments

Each row is a coding assignment, not just a report section.

| Owner | Files and responsibility | First small PR |
| --- | --- | --- |
| M1 — you | `model.py`, `data.py`, `parameters.py`, `pipeline.py`, `experiments/baseline.py`; model/data/parameter and integration tests | Implement `equation` and `current_derivative`, with special-case and derivative checks |
| M2 | `root_solver.py`, `prediction.py`; root and curve tests | Implement `solve_root` for Newton on simple scalar equations |
| M3 | `optimization.py`; optimizer tests | Implement GN using a fake linear residual and a tested M4 linear solve |
| M4 | `residuals.py`, `jacobian.py`, `linear_solver.py`; corresponding tests | Implement pivoted Gaussian elimination with singular-system tests |
| M5 | `experiments.py`, `experiments/noise_analysis.py`; experiment tests | Implement `rmse` and seeded `add_current_noise` with tests |

M1 coordinates changes to `contracts.py` and CI. This does not transfer algorithm
ownership to M1. M1's substantial coding includes model physics, input validation,
parameter setup, callback wiring, failure propagation and integration tests.

## Independence

- M2 can test `solve_root` with `x*x - 4`, without PV code.
- M3 can use a residual callback for a tiny known linear least-squares problem.
- M4 can differentiate toy vector functions and solve hand-checkable matrices.
- M5 can use a fake fit callback returning controlled success/failure results.
- M1 can test integration wiring with fake predictors/fitters. No copied algorithms.

## Completion checklist — every owner

- Implement only the assigned functions behind the agreed signatures.
- Replace relevant skipped tests with meaningful assertions and remove their skips.
- Cover ordinary input, a boundary case and a failure case.
- Document numerical choices and explain one worked example in the PR.
- Run the relevant tests, the full suite and lint.
- Fix review feedback yourself; do not hand an incomplete implementation to M1.

## Returning incomplete work

Use the PR review or an issue:

> Owner: M__
> Failing input / reproduction: …
> Expected behavior from the interface: …
> Actual behavior: …
> Required acceptance test: …
> Integration is waiting on your fix; ownership stays with you.

Record any reassignment explicitly with the team. Do not silently make M1 the fallback.
Commit history shows authorship; PR descriptions show the actual numerical contribution.
