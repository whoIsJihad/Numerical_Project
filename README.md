# Robust PV Parameter Estimation

Python Numerical Methods course project, built by five members.

**Status: interface scaffold only. All project functions deliberately raise
`NotImplementedError`. No estimator or numerical method is implemented yet.**

## The pipeline

Measured voltage/current data → trial parameters → solve current at each voltage
→ predicted-minus-measured residuals → Jacobian → GN/LM parameter update
→ fitted parameters and RMSE → repeat fits with measurement noise.

There are two loops: the inner loop changes current with parameters fixed;
the outer loop changes the five parameters. See [interfaces](docs/INTERFACES.md).

## Who implements what?

| Member | Owned work |
| --- | --- |
| **1 — project owner** | PV equation and derivative, dataset loading/validation, thermal voltage, bounds/initial guesses, baseline runner and integration tests |
| 2 | Newton, bisection, safeguarded Newton, curve prediction and warm starts |
| 3 | Gauss–Newton, LM, stopping rules, damping and failed-trial handling |
| 4 | Residuals, finite-difference Jacobian and pivoted linear-system solver |
| 5 | Seeded noise experiments, statistics, metrics, plots and result export |

Every member owns their tests, documentation
and review fixes. Member 1 coordinates and integrates; they do not inherit unfinished modules.
Detailed assignments and first PRs: [ownership](docs/OWNERSHIP.md).

## Set up locally

Use Python 3.11 or newer. From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e '.[dev]'
python -m pytest
python -m ruff check .
```

Initially, only scaffold checks pass; numerical tests are explicitly skipped.
**A green scaffold build does not mean the numerical project works.**
See [testing and milestones](docs/TESTING.md) before implementing a component.

## How to contribute: fork → branch → PR

Team repository: [whoIsJihad/Numerical_Project](https://github.com/whoIsJihad/Numerical_Project).
Replace `<YOUR-USERNAME>` with your own GitHub username below.

1. Open the team repository on GitHub and click **Fork**.
2. Clone your fork and connect the original repository:

   ```bash
   git clone https://github.com/<YOUR-USERNAME>/Numerical_Project.git
   cd Numerical_Project
   git remote add upstream https://github.com/whoIsJihad/Numerical_Project.git
   git fetch upstream
   git switch -c member2/newton upstream/main
   ```

3. Implement one small owner-assigned task. Replace its skipped test templates
   with real assertions, remove their skip decorators, and run tests and lint.
4. Commit using your own Git identity and push your branch:

   ```bash
   git add src/pv_estimation/root_solver.py tests/test_member2_roots.py
   git commit -m "feat(roots): implement scalar Newton solver with tests"
   git push -u origin member2/newton
   ```

5. Open a pull request from your fork's branch to the team repository's `main`.
   Complete the PR checklist, link the assigned task, and request review.
6. If review finds a bug, **the component owner fixes it on that same branch**.
   Keep PRs small; do not bundle other members' unfinished work.

Before a new task, fetch upstream and create a fresh branch from `upstream/main`.
For work needing another member's component, use a small test double until it lands.
Agree on shared-interface changes in the PR before changing callers.

### Merge rules for the project owner

- Require passing CI plus review of numerical evidence; skipped tests are not evidence.
- Use **Create a merge commit** to preserve members' individual commits.
- Return defects with: failing input, expected result, actual result, acceptance test.
- Do not implement a teammate's missing component to make integration pass.
- Repository admin: protect `main` against force pushes/direct pushes, require CI
  and a review, and enable merge commits. This scaffold does not configure GitHub settings.
- Member 1's own PRs should be reviewed by another member.

## Project map

```text
src/pv_estimation/
  contracts.py       shared data containers and options
  model.py           M1: equation checker and current derivative
  data.py            M1: measured data loading and validation
  parameters.py      M1: bounds, validation and starting guess
  pipeline.py        M1: baseline orchestration
  root_solver.py     M2: scalar root methods
  prediction.py      M2: currents across a voltage dataset
  optimization.py    M3: GN and LM
  residuals.py       M4: prediction errors
  jacobian.py        M4: parameter sensitivity by finite differences
  linear_solver.py   M4: Gaussian elimination with partial pivoting
  experiments.py     M5: Monte Carlo, metrics, plotting and export
experiments/         baseline/noise entry-point templates
tests/               owner-specific and end-to-end test templates
docs/                contracts, assignments and acceptance criteria
data/                dataset format and provenance guidance
outputs/             generated results (ignored)
```

## Incremental milestones

1. Equation and data validated; root solver and linear solver tested independently.
2. One current curve, residual vector and finite-difference Jacobian work.
3. One deterministic Gauss–Newton fit works end to end.
4. Safeguards, warm starts and LM work, including failure tests.
5. Seeded Monte Carlo study with honest failure counts and parameter variation.

Start with **one single-cell SDM dataset**. A module dataset needs its series-cell count.
DDM, additional root algorithms and condition-number analysis are optional later work.
Do not use SciPy optimizers to implement the course algorithms; NumPy arrays are allowed.
