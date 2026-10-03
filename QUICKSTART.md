# Run The Reference From A Clean Checkout

Start with a question in the [reading paths](READING-PATHS.md), then reproduce a calculation before changing its assumptions. This repository is a documentation reference with executable teaching examples. The capstones are implementation exercises; the checkout does not contain six completed trading systems or a packaged production pricing API.

## Set Up Python

Use Python 3.12, the version configured in CI. From the checkout root on Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-validation.txt
.venv\Scripts\python.exe scripts/check_repository.py
```

On Linux or macOS:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements-validation.txt
.venv/bin/python scripts/check_repository.py
```

No shell activation is required. The dependencies are NumPy and pandas; the other examples use the Python standard library. Markdown and SVG files can be read directly without building a website. Dependency constraints state supported minimums rather than promising bitwise identical results across every future package release.

## Follow One Calculation

The [earnings repricing story](examples/option-greeks-and-earnings-repricing.md) explains a call losing money despite a stock rise. The [tree convergence benchmark](examples/option-tree-convergence.md) checks the analytic prices through a separate numerical method. The [curve bootstrap](examples/curve-bootstrap-and-quote-risk.md) connects input quotes, calibration residuals, off-node bond value, and a rebuilt quote shock.

Copy an example's Python fence into a local Python session to experiment. Examples that load chapter code expect the repository root as their working directory. The check command handles that automatically and can itself be invoked by absolute path from another directory.

## Understand A Passing Check

`scripts/check_repository.py` fails on the first failed stage. It checks local navigation, heading anchors, Markdown structure, SVG metadata, validator regressions, and every numbered-chapter and standalone-example Python fence, including the independent tree benchmark and quote repricing assertions. It reports the execution count rather than relying on a hard-coded inventory.

Assertions are part of validation: do not run with Python's `-O` option or set `PYTHONOPTIMIZE`. The [source and convention guide](SOURCES-AND-CONVENTIONS.md) identifies the authority for consequential claims. Passing checks do not certify every external link, bibliography item, production convention, or trading claim. The [review record](DOCUMENTATION-REVIEW.md) states the completed scope.
