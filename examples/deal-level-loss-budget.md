# Deal-Level Loss Budget

Related chapter: [../38-deal-level-risk-and-strategy-pnl.md](../38-deal-level-risk-and-strategy-pnl.md).

Assume a multi-leg strategy has a USD 750k approved loss budget. Full revaluation, including financing and estimated exit costs, produces:

| Scenario | PnL |
| --- | ---: |
| Thesis succeeds | USD 510k |
| Thesis fails | USD -666k |
| Broad rally, no catalyst | USD -204k |
| Gap and illiquidity | USD -1,240k |

The reasonable-worst-case loss is the largest nonnegative scenario loss:

```math
L_{\text{RWC}}=\max(0, -\min_s\operatorname{PnL}_s)
=\text{USD }1{,}240\text{k}
```

Budget utilization is:

```math
u=\frac{1{,}240}{750}=165.3\%
```

The largest proportional size that would fit the budget is:

```math
k=\frac{750}{1{,}240}=60.48\%
```

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Scenario:
    name: str
    pnl: float


def budget_metrics(
    scenarios: list[Scenario],
    loss_budget: float,
) -> tuple[float, float, float]:
    if not scenarios or loss_budget <= 0.0:
        raise ValueError("scenarios and a positive budget are required")
    rwc = max(0.0, max(-scenario.pnl for scenario in scenarios))
    utilization = rwc / loss_budget
    scale = min(1.0, loss_budget / rwc) if rwc else 1.0
    return rwc, utilization, scale


results = [
    Scenario("thesis succeeds", 510_000),
    Scenario("thesis fails", -666_000),
    Scenario("broad rally, no catalyst", -204_000),
    Scenario("gap and illiquidity", -1_240_000),
]
rwc, utilization, scale = budget_metrics(results, 750_000)
assert rwc == 1_240_000
assert abs(utilization - 1.6533333333333333) < 1e-12
assert abs(scale - 0.6048387096774194) < 1e-12
```

Scaling is only a first sizing estimate. Full repricing must be rerun because option convexity, market impact, margin, fixed fees, and minimum trade sizes need not scale linearly. The scenario set should also be versioned and include hedge failure, liquidity, financing, and event-delay states rather than only ordinary market moves.
