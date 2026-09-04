"""Member 1: wire the pipeline; do not duplicate the numerical algorithms."""


def run_baseline(
    voltage,
    current,
    vt,
    theta0,
    bounds,
    scales,
    ns=1,
    root_method="hybrid",
    fit_method="lm",
):
    """Return {"fit": fit result, "rmse": value or None}.

    Validate inputs. Bind numerics.residuals into a callback accepting only theta.
    Pass that callback to fit.fit_parameters. Call experiments.rmse only if
    the fit converged. A failed fit has rmse=None.
    """
    raise NotImplementedError("Member 1: connect the pipeline")


def main():
    """Read CSV/temperature/settings, get starting parameters, run and report.

    Begin with one baseline fit. Later offer a noise-study option using Member 5's
    monte_carlo and a fixed-start fit callback. Report failures honestly and
    exit nonzero for failed baseline runs. No argument parser is implemented yet.
    """
    raise NotImplementedError("Member 1: entry point")


if __name__ == "__main__":
    main()
