"""Adjust the five PV parameters until the calculated curve matches the data."""

import numpy as np

from model import validate_data, validate_parameters
from numerics import jacobian, residuals, solve_linear


def fit_parameters(
    voltage: np.ndarray,
    measured_current: np.ndarray,
    vt: float,
    theta0: np.ndarray,
    bounds: tuple[np.ndarray, np.ndarray],
    scales: np.ndarray,
    ns: int = 1,
    root_method: str = "hybrid",
    method: str = "lm",
    tol: float = 1e-8,
    max_iter: int = 100,
) -> dict:
    """Improve theta with Gauss-Newton or Levenberg-Marquardt.

    The function returns the best parameters found, their errors, and a short
    record of whether the fitting process succeeded.
    """
    validate_data(voltage, measured_current)
    validate_parameters(theta0, bounds)
    if not isinstance(scales, np.ndarray) or scales.shape != theta0.shape:
        raise ValueError("scales must have the same shape as theta0")
    if not np.all(np.isfinite(scales)) or np.any(scales <= 0):
        raise ValueError("scales must contain positive finite values")
    if method not in ("gauss_newton", "lm"):
        raise ValueError("method must be gauss_newton or lm")
    if (
        not np.isfinite(tol)
        or tol <= 0
        or not isinstance(max_iter, int)
        or max_iter < 1
    ):
        raise ValueError("tol and max_iter must be positive")

    lower, upper = bounds
    theta = theta0.astype(np.float64, copy=True)
    history = []
    evaluations = 0
    damping = 1e-3

    try:
        current_errors = residuals(
            theta, voltage, measured_current, vt, ns, root_method
        )
        evaluations += 1
    except NotImplementedError:
        raise
    except RuntimeError as error:
        return {
            "theta": theta,
            "residuals": None,
            "converged": False,
            "reason": str(error),
            "iterations": 0,
            "evaluations": evaluations,
            "history": history,
        }

    current_mse = float(np.mean(current_errors**2))
    history.append(current_mse)

    for iteration in range(1, max_iter + 1):
        try:
            slopes = jacobian(
                theta, voltage, measured_current, vt, bounds, scales, ns, root_method
            )
        except NotImplementedError:
            raise
        except RuntimeError as error:
            return {
                "theta": theta,
                "residuals": current_errors,
                "converged": False,
                "reason": str(error),
                "iterations": iteration - 1,
                "evaluations": evaluations,
                "history": history,
            }

        gradient = slopes.T @ current_errors
        if np.max(np.abs(gradient) * scales) <= tol:
            return {
                "theta": theta,
                "residuals": current_errors,
                "converged": True,
                "reason": "gradient became small",
                "iterations": iteration - 1,
                "evaluations": evaluations,
                "history": history,
            }

        normal_matrix = slopes.T @ slopes
        accepted = False
        trial_step = np.zeros(5)

        # Gauss-Newton tries its full step, then shorter versions if needed.
        if method == "gauss_newton":
            try:
                full_step = solve_linear(normal_matrix, -gradient)
            except RuntimeError as error:
                return {
                    "theta": theta,
                    "residuals": current_errors,
                    "converged": False,
                    "reason": str(error),
                    "iterations": iteration - 1,
                    "evaluations": evaluations,
                    "history": history,
                }
            fraction = 1.0
            for _ in range(20):
                candidate = np.clip(theta + fraction * full_step, lower, upper)
                try:
                    candidate_errors = residuals(
                        candidate, voltage, measured_current, vt, ns, root_method
                    )
                    evaluations += 1
                except RuntimeError:
                    fraction /= 2
                    continue
                candidate_mse = float(np.mean(candidate_errors**2))
                if candidate_mse < current_mse:
                    trial_step = candidate - theta
                    accepted = True
                    break
                fraction /= 2

        # LM adds damping. More damping means a smaller, safer step.
        else:
            for _ in range(20):
                damped_matrix = normal_matrix + damping * np.eye(5)
                try:
                    proposed_step = solve_linear(damped_matrix, -gradient)
                except RuntimeError:
                    damping *= 10
                    continue
                candidate = np.clip(theta + proposed_step, lower, upper)
                try:
                    candidate_errors = residuals(
                        candidate, voltage, measured_current, vt, ns, root_method
                    )
                    evaluations += 1
                except RuntimeError:
                    damping *= 10
                    continue
                candidate_mse = float(np.mean(candidate_errors**2))
                if candidate_mse < current_mse:
                    trial_step = candidate - theta
                    damping = max(damping / 3, 1e-15)
                    accepted = True
                    break
                damping *= 10

        if not accepted:
            return {
                "theta": theta,
                "residuals": current_errors,
                "converged": False,
                "reason": "no improving step found",
                "iterations": iteration,
                "evaluations": evaluations,
                "history": history,
            }

        previous_mse = current_mse
        theta = candidate
        current_errors = candidate_errors
        current_mse = candidate_mse
        history.append(current_mse)

        small_step = np.max(np.abs(trial_step) / scales) <= tol
        small_improvement = previous_mse - current_mse <= tol * max(previous_mse, 1.0)
        if small_step or small_improvement:
            reason = (
                "parameter change became small"
                if small_step
                else "error stopped improving"
            )
            return {
                "theta": theta,
                "residuals": current_errors,
                "converged": True,
                "reason": reason,
                "iterations": iteration,
                "evaluations": evaluations,
                "history": history,
            }

    return {
        "theta": theta,
        "residuals": current_errors,
        "converged": False,
        "reason": "maximum iterations reached",
        "iterations": max_iter,
        "evaluations": evaluations,
        "history": history,
    }
