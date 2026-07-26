# Historical VaR And Expected Shortfall

Related chapter: [../13-risk-and-pnl.md](../13-risk-and-pnl.md).

Assume these are sorted one-day portfolio PnL outcomes in USD thousands, from worst to best:

| Scenario | PnL |
| ---: | ---: |
| 1 | -420 |
| 2 | -310 |
| 3 | -250 |
| 4 | -180 |
| 5 | -120 |
| 6 | -40 |
| 7 | 20 |
| 8 | 60 |
| 9 | 110 |
| 10 | 150 |

Using the lower empirical quantile and the worst 20% tail for illustration:

```python
from math import ceil

losses = sorted([420, 310, 250, 180, 120, 40, -20, -60, -110, -150])
confidence = 0.80
quantile_index = ceil(confidence * len(losses)) - 1
var_80 = losses[quantile_index]

strict_tail = losses[quantile_index + 1:]
strict_tail_mass = len(strict_tail) / len(losses)
boundary_mass = max(0.0, (1.0 - confidence) - strict_tail_mass)
es_80 = (
    sum(strict_tail) / len(losses)
    + boundary_mass * var_80
) / (1.0 - confidence)
```

Results:
- 80% VaR = USD 250k
- 80% ES = USD 365k

Interpretation:
- VaR gives the threshold loss at the chosen confidence level.
- Here the two worst observations, USD 310k and USD 420k, lie strictly above VaR and exactly fill the 20% tail.
- When $(1-\alpha)n$ is not an integer, a production implementation must declare its quantile convention and include the required fraction of the boundary observation so the ES tail has total mass $1-\alpha$.
- A production implementation must also define sorting, interpolation, confidence level, horizon, PnL basis, weighting, and backtesting rules.
