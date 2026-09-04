# PV parameter estimation

A five-person Python Numerical Methods project. **This is a scaffold: numerical
functions are intentionally unimplemented.** Start with one single-cell dataset.

## Files and ownership

| File | Owner | Responsibility |
| --- | --- | --- |
| `model.py` | Member 1 | PV equation/derivative, CSV loading, validation, initial parameters |
| `current.py` | Member 2 | Newton, bisection, hybrid solver and current prediction |
| `fit.py` | Member 3 | Gauss–Newton and Levenberg–Marquardt parameter fitting |
| `numerics.py` | Member 4 | Residuals, finite-difference Jacobian, pivoted linear solve |
| `experiments.py` | Member 5 | RMSE, seeded noise studies, summaries and plots |
| `run.py` | Member 1 | Connect the components and provide the entry point |
| `test_project.py` | Everyone | Implement the tests labelled with your member number |

Measurements → predict currents → residuals → update parameters → repeat.
The **inner solver changes current** with parameters fixed.
The **outer optimizer changes parameters** and repeats the current predictions.

## Setup

Use Python 3.11 or newer, from the project folder:

```bash
python -m venv .venv
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -ra
```

If the folder moved, recreate the virtual environment before activation.
`python run.py` will deliberately raise `NotImplementedError` until implemented.
Scaffold checks only test imports; skipped tests are unfinished, not passing algorithms.
GitHub runs the same test suite for pull requests.

## Shared interfaces

All functions are documented in their files. Use NumPy arrays and ordinary dictionaries;
there is no separate configuration framework.

- Parameters always follow `[Iph, I0, Rs, Rsh, n]`, shape `(5,)`.
- Voltage/current arrays have matching shape `(N,)`, in volts/amperes.
  Preserve measurement order; reject empty, malformed or nonfinite data.
- `vt` is per-cell thermal voltage `k*T/q`; `ns` is series-cell count.
  The model denominator is `n*ns*vt`. Temperature is in kelvin.
- Physical domain: `Iph >= 0, I0 > 0, Rs >= 0, Rsh > 0, n > 0`.
  `bounds` is `(lower_array, upper_array)`; use finite, physically valid limits.
  Initial guesses and bounds are documented dataset-specific heuristics.
- Residuals are **predicted minus measured**, shape `(N,)`; Jacobian shape is `(N,5)`.
  Minimize mean squared residuals. RMSE is in amperes.
- Root results: `root, converged, reason, iterations, function_evaluations`.
  Failed solves return `root=None`, never the last unverified guess.
- Curve results: `current, roots`. Failed points are NaN with aligned root diagnostics.
  The residual function raises `RuntimeError` on any failed point; never drop rows.
- Fit results: `theta, residuals, converged, reason, iterations, evaluations, history`.
  Keep the best valid iterate; residuals may be None. History contains accepted MSEs.
  `evaluations` counts residual calls, including finite differences and rejected trials.
- Invalid input raises `ValueError`; numerical evaluation/linear-solve failures raise
  `RuntimeError`. Never catch `NotImplementedError` as a numerical failure.
- Do not mutate caller arrays. Return failures explicitly; low RMSE alone does not prove
  that all five fitted parameters are physically identifiable.

M2 calls M1's equation. M4 calls M2's predictions. M3 accepts a residual callback
and calls M4's Jacobian/linear solver. M1's runner connects them; M5 repeats whole fits.
Implement course algorithms explicitly; NumPy arrays are fine, SciPy optimizers are not
the implementation. Teammates can test their components with simple fake callbacks.

## Build in this order

1. Model checker, scalar Newton solver and pivoted linear solver, each with tests.
2. Current curve, residuals and numerical Jacobian.
3. One end-to-end Gauss–Newton fit.
4. Hybrid safeguards, warm starts and LM.
5. Reproducible noisy fits and reporting.

M1 starts with `model.equation` and its test. Each member implements and tests their
own functions. A completed test replaces its placeholder and removes its skip marker.

## Data and results

Put a small, shareable CSV in `data/` with columns `voltage_v,current_a`.
No benchmark data is bundled. Record source, reuse terms, temperature and series-cell
count beside any dataset. Module data needs the correct cell count.
Generated results belong in ignored `outputs/`; create it when needed.

## Contribute: fork → branch → pull request

Fork [the team repository](https://github.com/whoIsJihad/Numerical_Project), then:

```bash
git clone https://github.com/YOUR-USERNAME/Numerical_Project.git
cd Numerical_Project
git remote add upstream https://github.com/whoIsJihad/Numerical_Project.git
git fetch upstream
git switch -c member2/newton upstream/main
# Implement one small task and its tests.
python -m pytest -ra
git add current.py test_project.py
git commit -m "Implement Newton solver with tests"
git push -u origin member2/newton
```

Open a PR to the team's `main`. Include the method, tests, failure cases and remaining
work. Keep your edits in the test section labelled with your member number.
The component author addresses review feedback. Interface changes require agreement.
Review before merging; merge commits preserve individual authorship. Member 1's work
also receives teammate review. Fetch upstream before starting each new task.
