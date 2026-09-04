# Agreed interfaces

This is the initial contract. Function bodies are intentionally unimplemented.
All arrays use floating-point NumPy arrays. Do not mutate caller inputs.

## Shared conventions

- `theta`: shape `(5,)`, in order `[Iph, I0, Rs, Rsh, n]`.
- Units: current A, voltage V, resistance ohm, temperature K; `n` is dimensionless.
- `IVData.voltage` and `.current`: finite one-dimensional arrays of equal nonzero length.
- `PVConditions`: positive `temperature_k`, positive integer `cells_in_series` (1 for a cell).
- Thermal voltage from `thermal_voltage(conditions)` is **per-cell** `k*T/q`.
  The model exponent denominator is `n * cells_in_series * Vt`.
- Physical domain: `Iph >= 0`, `I0 > 0`, `Rs >= 0`, `Rsh > 0`, `n > 0`.
  Parameter bounds must be finite and respect that domain. The parameter owner
  documents dataset-specific bounds; do not claim universal numerical bounds.
- Residual sign: **predicted current minus measured current**, shape `(N,)`.
- Jacobian shape: `(N, 5)` for PV; general callback tests may use `(N, P)`.
- Objective: mean squared error. GN/LM can minimize half the sum of squares;
  this has the same minimizers for fixed N. RMSE is in amperes.

## Call chain and owners

```text
M1 run_baseline(data, conditions, initial_theta, bounds, root_options, fit_options)
  └─ M3 fit_parameters(residual_fn, initial_theta, bounds, options)
       ├─ M4 residual_fn(theta) = residual_vector(theta, data, conditions, root_options)
       │    └─ M2 predict_curve(data.voltage, theta, conditions, root_options)
       │         └─ M2 solve_root(f, df, initial_guess=..., bracket=..., options=...)
       │              └─ M1 equation(I, V, theta, conditions), current_derivative(...)
       ├─ M4 finite_difference_jacobian(residual_fn, theta, bounds=..., options=...)
       └─ M4 solve_linear_system(A, b)
  └─ M5 rmse(fit.residuals), only if fit converged

M5 run_monte_carlo(data, fit_fn, options)
  ├─ add_current_noise(data, sigma, rng)
  └─ fit_fn(noisy_data): M1 baseline closure → FitResult
```

M1 implements the callback wiring, not another copy of members' algorithms.
Experiment entry-point templates show what needs to be wired; they do not run yet.

## Model and data — M1

`equation(I, V, theta, conditions)` returns
`Iph - I0 * expm1((V + I*Rs)/(n*Ns*Vt)) - (V + I*Rs)/Rsh - I`.
Zero means the guessed current satisfies the model. `current_derivative` is the
derivative with respect to **current**, not the five-parameter residual Jacobian.
Validate shapes, domains and finite values. Prefer `expm1` for small exponent
arguments; never silently clip an overflowing exponent and report a physical answer.

`load_iv_csv(path)` expects exactly the named numeric columns `voltage_v,current_a`.
Reject malformed/non-finite/empty input; `validate_data` does not silently drop points.
Data order is preserved. Temperature and series-cell count are explicit separate inputs.

`default_bounds` and `initial_guess` are documented heuristics, not known true parameters.
`validate_parameters(theta, bounds)` checks shape, finite values and physical/bound limits.

## Root solving and prediction — M2

`solve_root` receives scalar callbacks: a checker and its derivative. It is not PV-specific.
Newton needs an initial guess. Bisection/hybrid need a finite sign-changing bracket
(an endpoint root is valid). Hybrid may start at the bracket midpoint.
Bad options or missing required inputs raise `ValueError`. An attempted solve that
cannot succeed returns `RootResult(converged=False, root=None, reason=...)`.

Use both a scale-aware current-step/bracket-width test and a checker-residual test;
do not report success just because the step is tiny. An exact/acceptable initial root
may succeed immediately. Check finite function and derivative values.
Count checker calls in `function_evaluations`, derivative calls separately.

`predict_curve` owns PV brackets, cold starts and continuation. It sorts voltage indices
internally if warm starting, then restores original order (including duplicate voltages).
Only successful roots can warm-start the next voltage. A failed point is `NaN` in
`CurveResult.current`, with a failed `RootResult`; never an unverified last iterate.
For physically valid theta the PV checker is decreasing in I; bracket expansion must
still have a finite limit and report overflow/no bracket. Do not assume `[0, Iph]`
works for every voltage. `root_results` stays aligned with original data order.

## Residuals, Jacobian and linear solves — M4

`residual_vector` returns all N residuals only if every current solve succeeds.
Otherwise raise `EvaluationError` naming the failed voltage index/reason. Never
drop failed points, silently use NaN, or substitute zero residuals.

`finite_difference_jacobian` uses parameter-scaled perturbations, not one absolute h
for parameters whose magnitudes differ enormously. Perturbation magnitude starts at
`relative_step * max(abs(theta[j]), parameter_scales[j])`; all scales are positive.
Use a feasible forward or backward step near bounds. Ensure the represented step
is nonzero; use the actual step in the denominator. Failed evaluations raise
`EvaluationError`; do not fabricate a zero column. `base_residual` may avoid one repeat.

`solve_linear_system(A,b)` supports square finite A and matching 1-D b, using Gaussian
elimination with **partial pivoting**, including back substitution. Invalid shapes raise
`ValueError`; numerical singularity raises `LinearSolveError`. Use a matrix-scale-aware
pivot threshold. Do not use `inv`, `solve`, `lstsq` or SciPy in this implementation.

## Optimizer — M3

GN solves `(J.T @ J) step = -J.T @ r`; LM adds `lambda * I` to the left side.
Use M4's Jacobian and linear solve. Normal equations may be ill-conditioned; report
failure instead of pretending that a singular solve succeeded.

`FitOptions` supplies per-parameter scales for finite differences and scaled step tests.
Full parameter rescaling and improved LM damping matrices are later refinements.
GN uses bounded backtracking; LM adjusts damping based on actual objective improvement.
Never evaluate physically invalid candidates or silently clip an accepted step.
A failed trial evaluation is rejected, with bounded retry/backtracking/damping attempts.
Failure at the starting point produces a failed fit. Catch known numerical exceptions,
not every exception; programming errors and `NotImplementedError` must remain visible.

`FitResult.theta` is the best valid parameter iterate (initial theta if none evaluated).
`residuals` is the best valid residual vector or `None`; only `converged=True` is success.
`reason` explains stopping/failure. Check scaled gradient, step, objective change,
finite values and the iteration limit; document the precise convergence policy.
`history` records accepted iterates and objective values, not fabricated improvements.
`residual_evaluations` counts every callback call, including FD and rejected/failed trials.
It is **not** the number of inner checker calls. `runtime_seconds` covers the entire fit.

## Baseline and experiments — M1 / M5

M1 `run_baseline` validates input, constructs the residual callback, calls M3 and returns
`BaselineResult`. RMSE is `None` for a failed fit even if a partial iterate exists.

M5 uses `np.random.default_rng(seed)` with a single stream per experiment, never a
global RNG or the same reset seed each trial. Noise is independent Gaussian current
noise with standard deviation `sigma_current_a`; voltage and original data are unchanged.
Start every fit from the same declared initial theta for a controlled comparison.
Predeclare noise levels, repeats, seed and fit options. Persist the configuration.

Keep **all** trials, including failures. Summary failure rate uses all trials;
RMSE/parameter statistics use successful trials only and report their count.
Zero successes gives `None` summary metrics, not zero. Sample parameter standard
deviation requires at least two successes; otherwise return `None`.
Export strict JSON (convert arrays; use null rather than NaN) and record dataset
provenance, temperature, series-cell count, options, seed and revision when available.
Runtime comparisons should not assert exact timing. Sensitivity comes from the Jacobian;
condition numbers/identifiability are optional after the baseline.
