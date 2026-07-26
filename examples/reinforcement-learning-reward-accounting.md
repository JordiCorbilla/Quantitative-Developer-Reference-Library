# Reinforcement-Learning Reward Accounting

Related chapters: [../47-reinforcement-learning-for-trading-and-execution.md](../47-reinforcement-learning-for-trading-and-execution.md), [../20-execution-microstructure-and-tca.md](../20-execution-microstructure-and-tca.md), and [../13-risk-and-pnl.md](../13-risk-and-pnl.md).

An RL reward should reconcile to an independently understandable economic ledger. This example constructs a dense execution reward that telescopes to terminal implementation shortfall.

## Signed Shortfall Convention

Let:

- $d=+1$ for a buy and $d=-1$ for a sell;
- $Q$ be parent quantity;
- $p_0$ be arrival price;
- $C_t=\sum_{i\leq t}q_i p_i$ be cumulative unsigned fill notional;
- $F_t$ be cumulative fees net of rebates;
- $q_t$ be remaining quantity;
- $m_t$ be the declared reference mark for the remainder.

Define:

$$
S_t
=
d\left(C_t+q_t m_t-Qp_0\right)+F_t
$$

For a completed buy, paying above arrival makes $S_T>0$. For a completed sell, receiving below arrival also makes $S_T>0$.

A dense reward with separately measured penalties is:

$$
r_t
=
-(S_t-S_{t-1})
-P_t^{\text{inventory}}
-P_t^{\text{tail}}
-P_t^{\text{constraint}}
$$

For the undiscounted economic audit sum, equivalently $\gamma=1$, when the episode completes:

$$
\sum_t r_t
=
-S_T-\sum_t P_t
$$

This invariant exposes sign errors and double counting. A discounted training return does not telescope, so it should be reported separately from this ledger.

## Numerical Buy Example

Buy 10,000 shares with arrival price $100.00:

| Step | Fill quantity | Fill price | End reference mid | Step fee | Remaining | $S_t$ | Inventory penalty | $r_t$ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 2,000 | $100.04 | $100.02 | $10 | 8,000 | $250 | $40 | -$290 |
| 2 | 5,000 | $100.07 | $100.05 | $25 | 3,000 | $615 | $15 | -$380 |
| 3 | 3,000 | $100.06 | $100.06 | $15 | 0 | $660 | $0 | -$45 |

The midpoint is a declared shaping mark for this transparent example, not an executable-price claim. It changes intermediate rewards while the remainder is nonzero. A production environment should retain the reference mark and a conservative side-aware completion quote, then force-liquidate or mark terminal inventory using the executable convention.

The completed fill notional is:

$$
C_T
=
(2{,}000)(100.04)
+(5{,}000)(100.07)
+(3{,}000)(100.06)
=
\$1{,}000{,}610
$$

Fees total $50, so:

$$
S_T
=
1{,}000{,}610+50-1{,}000{,}000
=
\$660
$$

Arrival notional is $1,000,000, making implementation shortfall:

$$
\frac{660}{1{,}000{,}000}\times10{,}000
=
6.60\text{ bp}
$$

The rewards sum to $-\$715$, exactly $-\$660$ of economic shortfall and $-\$55$ of inventory penalties.

## Dependency-Light Ledger

```python
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class FillStep:
    quantity: int
    price: float
    fee: float
    end_reference_mark: float
    inventory_penalty: float = 0.0
    tail_penalty: float = 0.0
    constraint_penalty: float = 0.0


@dataclass(frozen=True)
class RewardRow:
    remaining: int
    cumulative_notional: float
    cumulative_fees: float
    marked_shortfall: float
    economic_reward: float
    penalty: float
    training_reward: float


def execution_reward_ledger(
    side: int,
    parent_quantity: int,
    arrival_price: float,
    steps: list[FillStep],
) -> list[RewardRow]:
    if side not in (-1, 1):
        raise ValueError("side must be +1 for buy or -1 for sell")
    if (
        parent_quantity <= 0
        or not math.isfinite(arrival_price)
        or arrival_price <= 0.0
    ):
        raise ValueError("positive quantity and arrival price required")

    remaining = parent_quantity
    cumulative_notional = 0.0
    cumulative_fees = 0.0
    previous_shortfall = 0.0
    ledger: list[RewardRow] = []

    for step in steps:
        if not 0 <= step.quantity <= remaining:
            raise ValueError("fill exceeds remaining quantity")
        penalty_components = (
            step.inventory_penalty,
            step.tail_penalty,
            step.constraint_penalty,
        )
        numeric_values = (
            step.price,
            step.end_reference_mark,
            step.fee,
            *penalty_components,
        )
        if not all(math.isfinite(value) for value in numeric_values):
            raise ValueError("non-finite accounting input")
        if step.price <= 0.0 or step.end_reference_mark <= 0.0:
            raise ValueError("prices must be positive")
        if any(penalty < 0.0 for penalty in penalty_components):
            raise ValueError("penalties must be non-negative")
        penalties = sum(penalty_components)

        cumulative_notional += step.quantity * step.price
        cumulative_fees += step.fee
        remaining -= step.quantity
        completion_notional = (
            cumulative_notional + remaining * step.end_reference_mark
        )
        marked_shortfall = (
            side
            * (completion_notional - parent_quantity * arrival_price)
            + cumulative_fees
        )
        economic_reward = -(marked_shortfall - previous_shortfall)
        training_reward = economic_reward - penalties
        ledger.append(
            RewardRow(
                remaining=remaining,
                cumulative_notional=cumulative_notional,
                cumulative_fees=cumulative_fees,
                marked_shortfall=marked_shortfall,
                economic_reward=economic_reward,
                penalty=penalties,
                training_reward=training_reward,
            )
        )
        previous_shortfall = marked_shortfall

    if remaining != 0:
        raise ValueError("unfilled terminal quantity requires liquidation")
    return ledger


steps = [
    FillStep(2_000, 100.04, 10.0, 100.02, inventory_penalty=40.0),
    FillStep(5_000, 100.07, 25.0, 100.05, inventory_penalty=15.0),
    FillStep(3_000, 100.06, 15.0, 100.06),
]
ledger = execution_reward_ledger(+1, 10_000, 100.00, steps)

terminal_shortfall = ledger[-1].marked_shortfall
total_penalties = sum(row.penalty for row in ledger)
total_reward = sum(row.training_reward for row in ledger)
assert abs(terminal_shortfall - 660.0) < 1e-9
assert abs(total_penalties - 55.0) < 1e-9
assert abs(total_reward - (-terminal_shortfall - total_penalties)) < 1e-9
```

The code rejects an unfinished episode. A production environment can instead force-liquidate remaining quantity at an executable bid/ask plus a documented impact charge. That terminal charge must appear in both the economic ledger and reward.

## Reward-Hacking Tests

Before training, test policies that deliberately probe the accounting:

- do nothing until termination;
- submit an immediately marketable order;
- post an unrealistic limit size;
- cancel repeatedly to seek rebates or avoid risk;
- accumulate inventory just before the episode boundary;
- exploit stale midpoints or crossed markets;
- move costs into the next episode;
- choose an invalid action and rely on silent projection.

Track independent KPIs alongside training reward: raw shortfall, completion, inventory, spread, impact, fees, message count, constraint overrides, and tail loss. A reward increase without corresponding economic improvement is a model or environment defect, not alpha.
