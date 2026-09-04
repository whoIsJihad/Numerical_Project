"""Member 3: fit parameters by calling Member 4's Jacobian and linear solver."""


def fit_parameters(
    residual_fn, theta0, bounds, scales, method="lm", tol=1e-8, max_iter=100
):
    """Return theta/residuals/converged/reason/iterations/evaluations/history dict.

    GN: solve (J.T@J)*step=-J.T@r; use bounded backtracking.
    LM: add damping*identity, adjust damping using objective improvement.
    Keep candidates inside bounds; reject failed trial evaluations, with bounded
    retries. Initial evaluation failure returns a failed result.
    Count every residual call, including FD and rejected trials. History stores
    accepted MSE values. Return best valid theta/residuals; residuals may be None.
    Use scaled step, objective and gradient checks; report iteration-limit failure.
    Document tolerance policy. Catch known RuntimeError numerical failures only;
    NotImplementedError is a programming/incomplete-code signal and must propagate.
    """
    raise NotImplementedError("Member 3: Gauss-Newton and LM")
