# Parametric And Monte Carlo VaR

Related chapters: [../13-risk-and-pnl.md](../13-risk-and-pnl.md) and [../10-numerical-methods.md](../10-numerical-methods.md).

Assume zero expected one-day PnL and standard deviation USD $1.5$ million. Under a normal parametric model at $99\%$ confidence:

```math
\operatorname{VaR}_{0.99}
=
\Phi^{-1}(0.99)\times1.5
\approx
USD\ 3.49\text{ million},
```

```math
\operatorname{ES}_{0.99}
=
1.5\frac{\phi(\Phi^{-1}(0.99))}{0.01}
\approx
USD\ 4.00\text{ million}.
```

The following dependency-free code reproduces the parametric result and illustrates a seeded normal Monte Carlo estimate:

```python
from math import ceil, exp, pi, sqrt
from random import Random
from statistics import NormalDist

standard_deviation = 1_500_000.0
confidence = 0.99
z_score = NormalDist().inv_cdf(confidence)
density = exp(-0.5 * z_score**2) / sqrt(2.0 * pi)

parametric_var = z_score * standard_deviation
parametric_es = standard_deviation * density / (1.0 - confidence)

rng = Random(20260726)
losses = sorted(
    -rng.gauss(0.0, standard_deviation)
    for _ in range(200_000)
)
path_count = len(losses)
quantile_index = ceil(confidence * path_count) - 1
monte_carlo_var = losses[quantile_index]

strict_tail = losses[quantile_index + 1:]
strict_tail_mass = len(strict_tail) / path_count
boundary_mass = max(0.0, (1.0 - confidence) - strict_tail_mass)
monte_carlo_es = (
    sum(strict_tail) / path_count
    + boundary_mass * monte_carlo_var
) / (1.0 - confidence)

assert round(parametric_var / 1_000_000, 2) == 3.49
assert round(parametric_es / 1_000_000, 2) == 4.00
assert abs(monte_carlo_var / parametric_var - 1.0) < 0.03
assert abs(monte_carlo_es / parametric_es - 1.0) < 0.03
```

The lower empirical quantile and ES calculation deliberately separate the VaR order statistic from the strictly worse observations and add only the boundary mass needed to make a tail of probability $1-\alpha$. The simulation is intentionally the same normal linear model, so the estimates should converge toward the parametric values. It does not demonstrate the main reason to use Monte Carlo. Production Monte Carlo should generate coherent multi-factor states, reprice nonlinear positions, test discretization and model choices, and report sampling uncertainty across path batches.

Historical simulation uses observed shocks instead of normal draws; filtered historical simulation rescales those shocks; named stress scenarios impose coherent hypothetical moves. Their results can legitimately differ. Reconcile position population, horizon, confidence, loss sign, quantile convention, and valuation mapping before attributing differences to model choice.
