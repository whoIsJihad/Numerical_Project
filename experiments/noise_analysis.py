"""M5 entry-point template, not an implemented experiment yet."""


def main() -> None:
    """Parse dataset, conditions, sigma, repeats, seed and fit settings.

    Construct a fit_fn calling M1 run_baseline(...).fit with fixed starting
    parameters. Run Monte Carlo, summarize, export metadata and plot variation.
    Reuse public components; do not write an alternative estimator here.
    """
    raise NotImplementedError("M5: implement noise-analysis entry point after baseline works")


if __name__ == "__main__":
    main()
