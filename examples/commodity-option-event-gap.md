# Commodity Option Event Gap and Tail-First Sizing

Related chapters: [../08-commodities.md](../08-commodities.md), [../01-options.md](../01-options.md), and [../37-volatility-relative-value-and-event-volatility.md](../37-volatility-relative-value-and-event-volatility.md).

This example sizes a hypothetical short commodity futures-option straddle for a scheduled report. It uses the exact expiry payoff to avoid treating a local gamma approximation as a tail valuation.

Assume:

| Input | Value |
| --- | ---: |
| Entry future and strike | USD 75 per barrel |
| Short call plus short put premium | USD 4 per barrel |
| Contract multiplier | 1,000 barrels |
| Pre-add-on scenario loss budget | USD 110,000 |
| Option expiry | Immediately after the event |

The short straddle's expiry PnL per contract is:

```math
\operatorname{PnL}_{1}(F_T)
=1{,}000\left[4-|F_T-75|\right].
```

For a first scenario set:

| Scenario | $F_T$ | Hedge state | PnL per contract |
| --- | ---: | --- | ---: |
| Down USD 15 | USD 60 | Tradable after gap | USD -11,000 |
| Down USD 8 | USD 67 | Locked at displayed limit | USD -4,000 before reopening/add-ons |
| Unchanged | USD 75 | Tradable | USD 4,000 |
| Up USD 8 | USD 83 | Locked at displayed limit | USD -4,000 before reopening/add-ons |
| Up USD 15 | USD 90 | Tradable after gap | USD -11,000 |

The mechanical contract cap is:

```math
N_{\max}
=
\left\lfloor
\frac{110{,}000}{11{,}000}
\right\rfloor
=10.
```

The locked rows do **not** make $\pm8$ a maximum move. Their displayed prices may not be executable, a short-gamma rebalance may be impossible, and the reopening price can lie outside the initial limit. A production scenario attaches a delayed-fill or no-fill path and an expanded-limit/reopening shock before approving the cap.

Now add a signed-price diagnostic at $F_T=-37.63$. That is the settlement recorded for the NYMEX May 2020 WTI contract on April 20, 2020, one day before expiry; it is used here as a state-space test, not as a forecast for this hypothetical contract or event. It was a specific near-expiry futures settlement, not a statement that every crude spot price or curve point was negative. See the [CFTC summary](https://www.cftc.gov/PressRoom/PressReleases/8315-20).

The hypothetical straddle PnL at that signed futures level is:

```math
1{,}000\left[4-|-37.63-75|\right]
=-\$108{,}630.
```

If that scenario is relevant to the contract and holding horizon, the same loss budget permits only one contract before liquidity, model-risk, margin, and concentration add-ons:

```math
\left\lfloor\frac{110{,}000}{108{,}630}\right\rfloor=1.
```

The purpose is not to mandate this historical price as every oil option's stress. It is to expose a dangerous dependency: clamping the future at zero, rejecting a signed vendor value, or using a lognormal pricer outside its domain can turn a six-figure per-contract scenario into a missing row.

```python
from dataclasses import dataclass
from math import floor


@dataclass(frozen=True)
class GapScenario:
    name: str
    futures_at_expiry: float
    hedge_available_at_mark: bool


def short_straddle_expiry_pnl(
    scenario: GapScenario,
    strike: float,
    premium_per_barrel: float,
    multiplier_barrels: float,
) -> float:
    if multiplier_barrels <= 0.0 or premium_per_barrel < 0.0:
        raise ValueError("invalid contract economics")
    intrinsic = abs(scenario.futures_at_expiry - strike)
    return multiplier_barrels * (premium_per_barrel - intrinsic)


def tail_first_contract_cap(
    loss_budget: float,
    scenarios: list[GapScenario],
    strike: float,
    premium_per_barrel: float,
    multiplier_barrels: float,
) -> int:
    if loss_budget <= 0.0 or not scenarios:
        raise ValueError("positive loss budget and scenarios are required")

    pnls = [
        short_straddle_expiry_pnl(
            scenario,
            strike,
            premium_per_barrel,
            multiplier_barrels,
        )
        for scenario in scenarios
    ]
    worst_loss = max(-pnl for pnl in pnls)
    if worst_loss <= 0.0:
        raise ValueError("no losing scenario: expand the stress set")
    return floor(loss_budget / worst_loss)


core_scenarios = [
    GapScenario("down_15", 60.0, True),
    GapScenario("down_8_locked", 67.0, False),
    GapScenario("unchanged", 75.0, True),
    GapScenario("up_8_locked", 83.0, False),
    GapScenario("up_15", 90.0, True),
]
signed_price_scenario = GapScenario("signed_price_diagnostic", -37.63, False)

common = dict(
    strike=75.0,
    premium_per_barrel=4.0,
    multiplier_barrels=1_000.0,
)

core_pnls = [
    short_straddle_expiry_pnl(scenario, **common)
    for scenario in core_scenarios
]
signed_price_pnl = short_straddle_expiry_pnl(
    signed_price_scenario,
    **common,
)

assert core_pnls == [-11_000.0, -4_000.0, 4_000.0, -4_000.0, -11_000.0]
assert abs(signed_price_pnl - (-108_630.0)) < 1e-9
assert tail_first_contract_cap(
    110_000.0,
    core_scenarios,
    **common,
) == 10
assert tail_first_contract_cap(
    110_000.0,
    core_scenarios + [signed_price_scenario],
    **common,
) == 1
assert any(not scenario.hedge_available_at_mark for scenario in core_scenarios)
```

Sanity checks before approving the risk:

- Source scheduled releases from versioned official calendars. WASDE, EIA petroleum data, and OPEC/OPEC+ communications have different clocks, holiday behavior, and rescheduling risk.
- Confirm the event occurs before the option's last-trade and expiry cut-offs in the exchange time zone.
- Use the correct futures delivery month, option expiry, multiplier, premium unit, currency, settlement style, and exercise rules.
- Preserve signed futures values end to end and reject a lognormal model when its positive-price domain is violated.
- Full-reprice before expiry; the absolute-value formula above is exact only at expiry.
- Add volatility, skew, curve, basis, and proxy-hedge shocks. A level-only scenario is not sufficient for a commodity option book.
- Model locked markets as unavailable or size-limited hedges, not guaranteed fills at the displayed limit.
- Haircut physical coverage for volume, grade, location, and timing mismatch before calling a producer overwrite covered.
- Reserve for fees, margin, liquidity, concentration, reopening gaps, and model error after computing the mechanical cap.
