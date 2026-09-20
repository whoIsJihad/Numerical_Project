"""Residuals, numerical derivatives, and Gaussian elimination."""

import numpy as np

from current import solve_currents
from model import validate_data, validate_parameters


def residuals(
    theta: np.ndarray,
    voltage: np.ndarray,
    measured_current: np.ndarray,
    vt: float,
    ns: int = 1,
    root_method: str = "hybrid",
) -> np.ndarray:
    """Return calculated current minus measured current at every voltage."""
    validate_data(voltage, measured_current)
    validate_parameters(theta)
    result = solve_currents(voltage, theta, vt, ns, root_method)
    for index, root in enumerate(result["roots"]):
        if not root["converged"]:
            raise RuntimeError(f"current solve failed at row {index}: {root['reason']}")
    errors = result["current"] - measured_current
    if not np.all(np.isfinite(errors)):
        raise RuntimeError("residual calculation produced NaN or infinity")
    return errors


def jacobian(
    theta: np.ndarray,
    voltage: np.ndarray,
    measured_current: np.ndarray,
    vt: float,
    bounds: tuple[np.ndarray, np.ndarray],
    scales: np.ndarray,
    ns: int = 1,
    root_method: str = "hybrid",
    relative_step: float = 1e-6,
) -> np.ndarray:
    """Show how every residual changes when each PV parameter changes slightly.

    Rows represent measured points. Columns represent [Iph, I0, Rs, Rsh, n].
    """
    validate_data(voltage, measured_current)
    validate_parameters(theta, bounds)
    lower, upper = bounds
    if not isinstance(scales, np.ndarray) or scales.shape != theta.shape:
        raise ValueError("scales must have the same shape as theta")
    if not np.all(np.isfinite(scales)) or np.any(scales <= 0):
        raise ValueError("scales must contain positive finite values")
    if not np.isfinite(relative_step) or relative_step <= 0:
        raise ValueError("relative_step must be positive")

    base_errors = residuals(theta, voltage, measured_current, vt, ns, root_method)
    table = np.empty((voltage.size, theta.size), dtype=np.float64)

    for column in range(theta.size):
        step = relative_step * max(abs(theta[column]), scales[column])
        forward_theta = theta.copy()
        backward_theta = theta.copy()
        forward_theta[column] = min(theta[column] + step, upper[column])
        backward_theta[column] = max(theta[column] - step, lower[column])

        can_move_forward = forward_theta[column] != theta[column]
        can_move_backward = backward_theta[column] != theta[column]

        if can_move_forward and can_move_backward:
            forward_errors = residuals(
                forward_theta, voltage, measured_current, vt, ns, root_method
            )
            backward_errors = residuals(
                backward_theta, voltage, measured_current, vt, ns, root_method
            )
            distance = forward_theta[column] - backward_theta[column]
            table[:, column] = (forward_errors - backward_errors) / distance
        elif can_move_forward:
            forward_errors = residuals(
                forward_theta, voltage, measured_current, vt, ns, root_method
            )
            distance = forward_theta[column] - theta[column]
            table[:, column] = (forward_errors - base_errors) / distance
        elif can_move_backward:
            backward_errors = residuals(
                backward_theta, voltage, measured_current, vt, ns, root_method
            )
            distance = theta[column] - backward_theta[column]
            table[:, column] = (base_errors - backward_errors) / distance
        else:
            raise RuntimeError(f"cannot change parameter {column} inside its bounds")

    return table


def solve_linear(
    matrix: np.ndarray, rhs: np.ndarray, pivot_rtol: float = 1e-12
) -> np.ndarray:
    """Solve matrix @ solution = rhs with Gaussian elimination and row swapping."""
    if not isinstance(matrix, np.ndarray) or not isinstance(rhs, np.ndarray):
        raise TypeError("matrix and rhs must be NumPy arrays")
    if matrix.ndim != 2 or matrix.shape[0] == 0 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("matrix must be square and nonempty")
    if rhs.shape != (matrix.shape[0],):
        raise ValueError("rhs length must match the matrix size")
    if not np.all(np.isfinite(matrix)) or not np.all(np.isfinite(rhs)):
        raise ValueError("matrix and rhs cannot contain NaN or infinity")

    work = matrix.astype(np.float64, copy=True)
    answers = rhs.astype(np.float64, copy=True)
    size = work.shape[0]
    minimum_pivot = pivot_rtol * np.max(np.abs(work))

    # Turn the matrix into an upper triangular matrix.
    for column in range(size):
        pivot_row = column + int(np.argmax(np.abs(work[column:, column])))
        if abs(work[pivot_row, column]) <= minimum_pivot:
            raise RuntimeError("matrix is singular")
        if pivot_row != column:
            work[[column, pivot_row]] = work[[pivot_row, column]]
            answers[[column, pivot_row]] = answers[[pivot_row, column]]
        for row in range(column + 1, size):
            multiplier = work[row, column] / work[column, column]
            work[row, column:] -= multiplier * work[column, column:]
            answers[row] -= multiplier * answers[column]

    # Work upward from the last row to find every unknown.
    solution = np.empty(size)
    for row in range(size - 1, -1, -1):
        known = work[row, row + 1 :] @ solution[row + 1 :]
        solution[row] = (answers[row] - known) / work[row, row]
    return solution
