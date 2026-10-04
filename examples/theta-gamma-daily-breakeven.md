# Theta-Gamma Daily Breakeven

Related chapters: [../01-options.md](../01-options.md) and [../37-volatility-relative-value-and-event-volatility.md](../37-volatility-relative-value-and-event-volatility.md).

This example calculates the local one-step move required for a delta-hedged long option's gamma PnL to offset its theta. It is a model diagnostic, not an expiry payoff break-even or a trading guarantee.

Assume:

| Input | Value | Unit and convention |
| --- | ---: | --- |
| Spot, $S$ | 100 | currency per underlying unit |
| Implied volatility, $\sigma_{\text{imp}}$ | 25% | annualized on a 252-step variance clock |
| Long gamma, $\Gamma$ | 0.035 | option-value units per $1^2$ spot move |
| Step length, $\Delta\tau$ | $1/252$ | one trading-variance day |
| Rates and carry | 0 | simplifying assumption |

With rates and carry suppressed, the Black-Scholes PDE relates theta and gamma:

```math
\Theta_{\Delta\tau}
\approx
-\frac{1}{2}\Gamma S^2\sigma_{\text{imp}}^2\Delta\tau.
```

The interval theta is therefore:

```math
\Theta_{\Delta\tau}
=-\frac{1}{2}(0.035)(100)^2(0.25)^2\frac{1}{252}
=-0.0434028.
```

The delta-hedged local PnL for a spot move $\Delta S$ is:

```math
\Delta\Pi
\approx
\frac{1}{2}\Gamma(\Delta S)^2+\Theta_{\Delta\tau}.
```

Setting that approximation to zero gives:

```math
|\Delta S|_{\text{BE}}
=\sqrt{\frac{-2\Theta_{\Delta\tau}}{\Gamma}}
=S\sigma_{\text{imp}}\sqrt{\Delta\tau}
=1.57485.
```

| Absolute one-step move | Gamma PnL | Theta PnL | Approximate net PnL |
| ---: | ---: | ---: | ---: |
| 0.00 | 0.00000 | -0.04340 | -0.04340 |
| 1.00 | 0.01750 | -0.04340 | -0.02590 |
| 1.57485 | 0.04340 | -0.04340 | 0.00000 |
| 2.00 | 0.07000 | -0.04340 | 0.02660 |

The sign of the move does not change the local gamma term. The path still matters operationally. After an up move, the long-gamma option has more delta and the hedge sells underlying; after a down move, it has less delta and the hedge buys underlying. A short-gamma hedge does the opposite.

```python
from dataclasses import dataclass
from math import sqrt


@dataclass(frozen=True)
class GammaThetaStep:
    theta_pnl: float
    gamma_pnl: float
    net_pnl: float
    breakeven_abs_move: float


def gamma_theta_step(
    spot: float,
    implied_vol: float,
    gamma: float,
    variance_year_fraction: float,
    spot_move: float,
) -> GammaThetaStep:
    if spot <= 0.0:
        raise ValueError("spot must be positive for this lognormal example")
    if implied_vol < 0.0 or variance_year_fraction <= 0.0:
        raise ValueError("volatility and variance time must be valid")
    if gamma <= 0.0:
        raise ValueError("this function is written for a long-gamma position")

    theta_pnl = (
        -0.5
        * gamma
        * spot**2
        * implied_vol**2
        * variance_year_fraction
    )
    gamma_pnl = 0.5 * gamma * spot_move**2
    breakeven = sqrt(-2.0 * theta_pnl / gamma)
    return GammaThetaStep(
        theta_pnl=theta_pnl,
        gamma_pnl=gamma_pnl,
        net_pnl=theta_pnl + gamma_pnl,
        breakeven_abs_move=breakeven,
    )


inputs = dict(
    spot=100.0,
    implied_vol=0.25,
    gamma=0.035,
    variance_year_fraction=1.0 / 252.0,
)

at_one = gamma_theta_step(**inputs, spot_move=1.0)
at_two = gamma_theta_step(**inputs, spot_move=2.0)
at_breakeven = gamma_theta_step(
    **inputs,
    spot_move=100.0 * 0.25 * sqrt(1.0 / 252.0),
)

assert abs(at_one.theta_pnl - (-0.043402777777777776)) < 1e-12
assert abs(at_one.net_pnl - (-0.025902777777777775)) < 1e-12
assert abs(at_two.net_pnl - 0.02659722222222223) < 1e-12
assert abs(at_breakeven.breakeven_abs_move - 1.5748519708715748) < 1e-12
assert abs(at_breakeven.net_pnl) < 1e-12
assert gamma_theta_step(**inputs, spot_move=-2.0).net_pnl == at_two.net_pnl
```

Sanity checks before using the result:

- Use the same variance clock and annualization basis for implied volatility, theta, and the move horizon.
- Confirm whether gamma and theta are per share, per contract, per point, or already position-scaled; apply quantity and multiplier exactly once.
- Restore the PDE's rate, carry, funding, and dividend terms when they are material.
- Treat $\widehat\sigma_{\text{step}}=|\Delta S|/(S\sqrt{\Delta\tau})$ as a one-step diagnostic, not a statistically robust realized-volatility estimate.
- Reprice the actual position for jumps, strike crossings, surface shifts, early exercise, and large moves.
- Deduct spread, hedge slippage, fees, and market impact. A move at the model break-even can still produce a trading loss.
- Keep model theta separate from the desk's Friday-to-Monday or holiday roll PnL; those rolls may age market data and event variance differently.
