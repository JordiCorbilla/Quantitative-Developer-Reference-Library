# Gerber Co-Movement

Related chapter: [../44-robust-portfolio-and-research-validation.md](../44-robust-portfolio-and-research-validation.md).

Classify standardized returns as `1` above a positive threshold, `-1` below a negative threshold, and `0` inside the neutral region. Suppose two assets have these joint-extreme counts:

| State pair | Count |
| --- | ---: |
| Up/up | 5 |
| Down/down | 3 |
| Up/down | 1 |
| Down/up | 1 |

Using the convention that ignores observations where either asset is neutral:

```math
g_{12}
=\frac{n^{UU}+n^{DD}-n^{UD}-n^{DU}}
{n^{UU}+n^{DD}+n^{UD}+n^{DU}}
=\frac{5+3-1-1}{10}
=0.60
```

```python
def gerber_pair(states_a: list[int], states_b: list[int]) -> float:
    if len(states_a) != len(states_b) or not states_a:
        raise ValueError("aligned non-empty state series are required")
    if any(state not in {-1, 0, 1} for state in states_a + states_b):
        raise ValueError("states must be -1, 0, or 1")

    concordant = sum(
        1 for a, b in zip(states_a, states_b) if a != 0 and b != 0 and a == b
    )
    discordant = sum(
        1 for a, b in zip(states_a, states_b) if a != 0 and b != 0 and a == -b
    )
    if concordant + discordant == 0:
        raise ValueError("no jointly extreme observations")
    return (concordant - discordant) / (concordant + discordant)


a = [1, 1, 1, 1, 1, -1, -1, -1, 1, -1, 0, 1]
b = [1, 1, 1, 1, 1, -1, -1, -1, -1, 1, 1, 0]
g = gerber_pair(a, b)
assert abs(g - 0.60) < 1e-12
```

If annualized robust volatility scales are 20% and 30%, covariance is:

```math
\widehat\Sigma_{12}=0.60(0.20)(0.30)=0.036
```

A 50/50 portfolio has annualized volatility:

```math
\sqrt{0.5^2(0.20^2)+0.5^2(0.30^2)+2(0.5)(0.5)(0.036)}
=22.47\%
```

The example has very few jointly extreme observations. Production controls should require adequate counts, persist the threshold and statistic variant, test sensitivity to window and scale estimator, and verify that the complete covariance matrix is symmetric and positive semidefinite.
