# Private-Credit Covenant Headroom

Related chapter: [../39-private-credit-distressed-and-real-estate-credit.md](../39-private-credit-distressed-and-real-estate-credit.md).

This example calculates a maximum net-leverage covenant under base and stressed financials. The arithmetic is simple; the difficult production task is reproducing the agreement's definitions, permitted adjustments, test dates, and cure mechanics.

Assume:

- total debt: USD 225m,
- eligible cash: USD 15m,
- agreement-defined EBITDA: USD 50m,
- maximum net-leverage covenant: 5.25x.

Net debt and actual leverage are:

$$
\text{net debt}=225m-15m=USD\ 210m,
$$

$$
\text{actual leverage}=\frac{210m}{50m}=4.20x.
$$

Headroom can be reported in turns and in debt-capacity dollars:

$$
\text{headroom}_{x}=5.25x-4.20x=1.05x,
$$

$$
\text{headroom}_{\$}
=5.25\times50m-210m
=USD\ 52.5m.
$$

The dollar measure holds EBITDA and eligible cash constant. It is not incremental borrowing capacity if another covenant, basket, liquidity condition, or lender-consent requirement is tighter.

## EBITDA Stress

Suppose EBITDA falls 25% to USD 37.5m, with debt and cash unchanged:

$$
\text{stressed leverage}=\frac{210m}{37.5m}=5.60x.
$$

The test is 0.35x above the maximum, equivalent to negative USD 13.125m of debt-capacity headroom:

$$
5.25\times37.5m-210m=-USD\ 13.125m.
$$

EBITDA required to sit exactly at the covenant is:

$$
\frac{210m}{5.25}=USD\ 40m.
$$

The borrower therefore needs USD 2.5m more agreement-defined EBITDA than in the stressed case, or an equivalent reduction in net debt, before considering cures or waivers.

| Case | EBITDA | Net debt | Leverage | Turn headroom | Dollar headroom | Status |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Base | USD 50m | USD 210m | 4.20x | 1.05x | USD 52.5m | Pass |
| 25% EBITDA decline | USD 37.5m | USD 210m | 5.60x | -0.35x | USD -13.125m | Breach |

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class LeverageTest:
    actual_leverage: float
    turn_headroom: float
    dollar_headroom: float
    passes: bool


def maximum_leverage_test(
    debt: float,
    eligible_cash: float,
    covenant_ebitda: float,
    maximum_leverage: float,
) -> LeverageTest:
    if covenant_ebitda <= 0.0:
        raise ValueError("covenant EBITDA must be positive")
    net_debt = debt - eligible_cash
    actual = net_debt / covenant_ebitda
    turn_headroom = maximum_leverage - actual
    dollar_headroom = maximum_leverage * covenant_ebitda - net_debt
    return LeverageTest(
        actual_leverage=actual,
        turn_headroom=turn_headroom,
        dollar_headroom=dollar_headroom,
        passes=turn_headroom >= 0.0,
    )


base = maximum_leverage_test(
    debt=225_000_000,
    eligible_cash=15_000_000,
    covenant_ebitda=50_000_000,
    maximum_leverage=5.25,
)
stress = maximum_leverage_test(
    debt=225_000_000,
    eligible_cash=15_000_000,
    covenant_ebitda=37_500_000,
    maximum_leverage=5.25,
)

assert base.actual_leverage == 4.2
assert base.dollar_headroom == 52_500_000
assert round(stress.actual_leverage, 2) == 5.60
assert stress.dollar_headroom == -13_125_000
assert base.passes and not stress.passes
```

Before calling the stressed result an event of default, check whether the covenant is active and springing, how EBITDA and debt are defined, whether cash netting is capped, which entities are included, whether add-backs or annualization apply, and whether an equity cure, grace period, amendment, or waiver changes the result. Store those rules and their source clauses alongside the calculation.
