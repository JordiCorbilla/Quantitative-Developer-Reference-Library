# Cointegrated Pair Trade Lifecycle

Related chapter: [../31-statistical-arbitrage-and-pairs-trading.md](../31-statistical-arbitrage-and-pairs-trading.md).

This example uses The Coca-Cola Company (`KO`) and PepsiCo (`PEP`) as familiar, economically related securities. The companies do not run the pairs strategy; a statistical-arbitrage manager might research their securities as a candidate pair. The prices, fitted model, residual history, costs, and trade below are deliberately synthetic. They are not current market data, evidence of live cointegration, or a recommendation.

![Illustrative KO and PEP pairs-trade lifecycle](../assets/ko-pep-pairs-trade-lifecycle.svg)

## Frozen Research Snapshot

Assume a prior point-in-time training window produced the price-level relationship:

$$
P_t^{KO}=3.00+0.40P_t^{PEP}+s_t,
$$

with spread mean $mu_s=0$ and spread standard deviation $sigma_s=1$. Therefore:

$$
z_t=\frac{s_t-\mu_s}{\sigma_s}=s_t.
$$

This convenient scaling is only for teaching. A real study would use a much longer adjusted-price or log-price history, confirm compatible integration orders, apply the correct Engle-Granger residual test, and freeze the fitted coefficients before the trading window.

| Observation | KO | PEP | Fitted spread $s_t$ | z-score | State change |
| --- | ---: | ---: | ---: | ---: | --- |
| T-2 | 67.00 | 160.00 | 0.00 | 0.00 | Flat |
| T-1 | 68.00 | 160.50 | 0.80 | 0.80 | Flat |
| T0 | 69.00 | 160.00 | 2.00 | 2.00 | Enter short spread |
| T+1 | 69.20 | 160.50 | 2.00 | 2.00 | Hold |
| T+2 | 68.40 | 161.00 | 1.00 | 1.00 | Hold |
| T+3 | 67.60 | 161.50 | 0.00 | 0.00 | Convergence exit |

At T0, KO is rich relative to the frozen PEP relationship:

$$
s_{T0}=69-3-0.40(160)=2,
\qquad z_{T0}=2.
$$

For every KO share sold short, the fitted price-level hedge buys $0.40$ PEP shares. With 1,000 KO shares, the target is:

| Leg | Quantity | Entry price | Entry notional |
| --- | ---: | ---: | ---: |
| Short KO | -1,000 | USD 69.00 | USD -69,000 |
| Long PEP | +400 | USD 160.00 | USD +64,000 |
| Portfolio |  |  | USD 133,000 gross; USD -5,000 net |

The cointegration hedge is not automatically dollar-, beta-, volatility-, or factor-neutral. A portfolio layer may adjust or overlay the pair, but it must then track the difference between the statistical hedge and the final executable hedge.

## Exit and PnL

At T+3:

$$
s_{T+3}=67.60-3-0.40(161.50)=0,
$$

so the spread has returned to its fitted mean and the position closes.

| Component | Calculation | PnL |
| --- | --- | ---: |
| Short KO | $1{,}000(69.00-67.60)$ | USD 1,400 |
| Long PEP | $400(161.50-160.00)$ | USD 600 |
| Gross convergence PnL |  | USD 2,000 |
| Illustrative all-in execution, borrow, and financing |  | USD -150 |
| Net PnL |  | USD 1,850 |

Net PnL is $1.39\%$ of initial gross notional. This winning path is not the expected result of every signal. The same policy must also test adverse widening, gaps, time stops, borrow recall, earnings, corporate actions, and model invalidation.

## Stateful Trading Policy

A production rule needs state. A flat book may enter, an open book may hold or exit, and a disabled pair may not trade merely because its z-score is extreme.

```python
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class PairPolicy:
    entry_z: float = 2.0
    exit_z: float = 0.5
    stop_z: float = 3.5
    maximum_age: int = 20


def spread(y_price: float, x_price: float, alpha: float, beta: float) -> float:
    values = (y_price, x_price, alpha, beta)
    if not all(math.isfinite(value) for value in values):
        raise ValueError("spread inputs must be finite")
    if y_price <= 0.0 or x_price <= 0.0:
        raise ValueError("prices must be positive")
    return y_price - alpha - beta * x_price


def z_score(value: float, mean: float, standard_deviation: float) -> float:
    if not all(math.isfinite(item) for item in (value, mean, standard_deviation)):
        raise ValueError("z-score inputs must be finite")
    if standard_deviation <= 0.0:
        raise ValueError("standard deviation must be positive")
    return (value - mean) / standard_deviation


def pair_action(
    z: float,
    state: str,
    age: int,
    policy: PairPolicy,
    model_valid: bool = True,
) -> str:
    if not math.isfinite(z) or age < 0:
        raise ValueError("invalid signal state")
    if state not in {"flat", "long_spread", "short_spread", "disabled"}:
        raise ValueError("unknown position state")
    if not 0.0 <= policy.exit_z < policy.entry_z < policy.stop_z:
        raise ValueError("thresholds must satisfy exit < entry < stop")
    if policy.maximum_age <= 0:
        raise ValueError("maximum age must be positive")
    if state == "disabled":
        return "remain_disabled"
    if not model_valid:
        return "disable_and_close" if state != "flat" else "disable"
    if state == "flat":
        if z >= policy.entry_z:
            return "enter_short_spread"
        if z <= -policy.entry_z:
            return "enter_long_spread"
        return "remain_flat"
    if age >= policy.maximum_age:
        return "time_exit"
    if state == "short_spread":
        if z >= policy.stop_z:
            return "stop_exit"
        if z <= policy.exit_z:
            return "convergence_exit"
        return "hold"
    if z <= -policy.stop_z:
        return "stop_exit"
    if z >= -policy.exit_z:
        return "convergence_exit"
    return "hold"


def pair_pnl(
    y_shares: float,
    beta: float,
    y_entry: float,
    y_exit: float,
    x_entry: float,
    x_exit: float,
    short_spread: bool,
    all_in_cost: float,
) -> tuple[float, float, float]:
    values = (
        y_shares, beta, y_entry, y_exit,
        x_entry, x_exit, all_in_cost,
    )
    if not all(math.isfinite(value) for value in values):
        raise ValueError("PnL inputs must be finite")
    if y_shares <= 0.0 or beta <= 0.0 or all_in_cost < 0.0:
        raise ValueError("shares and beta must be positive; cost cannot be negative")
    x_shares = beta * y_shares
    direction = -1.0 if short_spread else 1.0
    y_pnl = direction * y_shares * (y_exit - y_entry)
    x_pnl = -direction * x_shares * (x_exit - x_entry)
    return y_pnl, x_pnl, y_pnl + x_pnl - all_in_cost


policy = PairPolicy()
entry_spread = spread(69.00, 160.00, alpha=3.00, beta=0.40)
entry_z = z_score(entry_spread, mean=0.0, standard_deviation=1.0)
assert pair_action(entry_z, "flat", age=0, policy=policy) == "enter_short_spread"

exit_spread = spread(67.60, 161.50, alpha=3.00, beta=0.40)
exit_z = z_score(exit_spread, mean=0.0, standard_deviation=1.0)
assert pair_action(exit_z, "short_spread", age=3, policy=policy) == "convergence_exit"
assert pair_action(3.60, "short_spread", age=2, policy=policy) == "stop_exit"
assert pair_action(-2.20, "flat", age=0, policy=policy) == "enter_long_spread"
assert pair_action(-0.30, "long_spread", age=4, policy=policy) == "convergence_exit"
assert pair_action(0.0, "short_spread", age=1, policy=policy, model_valid=False) == "disable_and_close"

ko_pnl, pep_pnl, net_pnl = pair_pnl(
    y_shares=1_000,
    beta=0.40,
    y_entry=69.00,
    y_exit=67.60,
    x_entry=160.00,
    x_exit=161.50,
    short_spread=True,
    all_in_cost=150.00,
)
assert abs(ko_pnl - 1_400.00) < 1e-9
assert abs(pep_pnl - 600.00) < 1e-9
assert abs(net_pnl - 1_850.00) < 1e-9
```

## Checks Before Trusting the Pair

- Refit and test only on data available before T0; never use the illustrated trading path to select the pair or coefficients.
- Confirm whether the residual is stationary across subperiods and whether results survive false-discovery control across all pairs tested.
- Reconcile the cointegration hedge with dollar, beta, sector, volatility, and factor exposures.
- Use executable bid/ask prices, simultaneous-leg or basket execution, partial-fill controls, and an explicit legging-loss limit.
- Accrue borrow, financing, dividends, fees, and corporate actions at leg level.
- Suspend or retire the pair when the relationship, hedge ratio, residual volatility, liquidity, borrow, or economic thesis changes.

