# Test pipeline

## Commands

```bash
python -m pytest                         # all tests, with pending skips shown
python -m pytest -m scaffold             # only interface/import checks
python -m pytest tests/test_member2_roots.py
python -m pytest -m numerical
python -m pytest -m integration
python -m ruff check .
```

CI runs lint, compile checks and the full suite on Python 3.11 and 3.12. It uploads
JUnit reports so skipped tests are visible. Numerical and integration templates
are intentionally marked skipped, not passing or xfailed.

## How to turn a template into a test

1. Find your owner-specific test case.
2. Replace `raise NotImplementedError` with setup and real assertions.
3. Remove its `@pytest.mark.skip(...)` decorator (keep the numerical/integration marker).
4. Implement your function until the test passes; add cases you discover.
5. State remaining skips and missing dependencies in your PR.

Do not remove a skip and leave an empty test. Do not catch all exceptions to make
tests pass. Use tolerances with units/scales and explain expected values.

## Acceptance tests by owner

| Owner | Minimum evidence |
| --- | --- |
| M1 | Equation at `Rs=0` agrees with direct current; derivative agrees with an independent central difference; invalid parameters/data rejected; CSV preserves order; series-cell factor tested; initial guess is feasible |
| M2 | Known scalar root for each method; endpoint root; bad bracket; zero derivative; iteration limit; non-finite evaluation; output ordering; failed point and warm-start behavior |
| M3 | Known linear least-squares solution; nonlinear improvement; active bounds; failed initial/trial evaluations; singular system; evaluation counts; iteration limit and honest convergence status |
| M4 | Residual sign and shape; failed prediction rejected; analytic toy Jacobian match; tiny-scale parameter and bound-aware steps; pivot-required solve; singular solve; no input mutation |
| M5 | RMSE known result; deterministic seeds; sigma=0 identity; no input mutation; all failures retained; zero/one-success summaries; export metadata; plots use correct units |

## Integration milestones — M1 owns wiring tests

1. Validate/load a tiny synthetic dataset (do not invent benchmark provenance).
2. Fixed theta → predicted current curve → residuals against known synthetic values.
3. Synthetic curve → nearby initial guess → improved deterministic fit.
4. Failed current solve propagates to residual failure and optimizer handling.
5. Seeded noise study repeats identically, excluding wall-clock measurements.

Do not require exact recovery of all five parameters just because RMSE is low.
Parameter identifiability is a separate numerical question.

## Release gate

Before calling a milestone complete, its required tests must be implemented and unskipped.
Before final submission, all numerical/integration templates must be completed; the
manual CI option `require_complete` fails if any test remains skipped. The command is:

```bash
python -m pytest --junitxml=junit.xml
python tools/check_no_skips.py junit.xml
```

This small tooling check is implemented; it contains no numerical project algorithm.
