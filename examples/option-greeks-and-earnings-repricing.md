# Option Greeks And Earnings Repricing

Related chapters: [../01-options.md](../01-options.md) and [../37-volatility-relative-value-and-event-volatility.md](../37-volatility-relative-value-and-event-volatility.md).

Start with the practical question: can a call lose money when the stock rises? Yes, if the benefit from direction is outweighed by changes in volatility, time, or other inputs. This synthetic example follows one European call through an earnings-style shock, then checks the model Greeks against prices rather than accepting the reported numbers on faith.

We use the chapter's Black-Scholes implementation, a constant rate and continuous dividend yield, and a calendar year of 365 days. Prices and Greeks are per underlying unit. Vega and rho returned by the model use absolute decimal shocks; theta is per year of elapsed time. No realized earnings data, transaction costs, or American exercise are modeled.

## Follow The Position

The stock starts at 100, strike is 100, expiry is 30/365 years, and volatility is 60%. Rates and dividends are zero. After one day the stock rises to 102 and volatility falls to 30%. The initial call costs 6.853941 and the final call is worth 4.499161, giving a loss of 235.48 for one contract with a 100-unit multiplier.

The sequential explain changes spot first, time second, and volatility third. Its increments are approximately +1.114246, -0.115288, and -3.353738 per underlying unit. They sum to the exact model price change. Changing the order changes the allocation of interactions, even though the total stays the same.

## Reproduce And Challenge The Numbers

Run this fence from the repository root. It compiles only the named chapter's Python fence in memory and writes no files. This shares the documented implementation; finite differences, parity, and the PDE provide separate checks of its mathematical relationships, rather than an independent pricing engine.

```python
import math
import re
from pathlib import Path


chapter = Path("01-options.md")
if not chapter.is_file():
    raise FileNotFoundError("Run this example from the repository root")
fence = chr(96) * 3
blocks = re.findall(fence + r"python\s*\n(.*?)" + fence, chapter.read_text(encoding="utf-8"), re.DOTALL)
assert len(blocks) == 1
namespace = {"__name__": "__documentation_snippet__"}
exec(compile(blocks[0], str(chapter), "exec"), namespace)
price_and_greeks = namespace["black_scholes_vanilla"]


def value(inputs, kind):
    return price_and_greeks(**inputs, option_type=kind).price


def bump(inputs, key, amount):
    return {**inputs, key: inputs[key] + amount}


# Check both option types across short, ordinary, and longer tenors,
# negative and positive rates, nonzero carry, and several moneyness states.
for spot, strike, expiry, rate, dividend, vol in [
    (100.0, 100.0, 30 / 365, 0.0, 0.0, 0.60),
    (80.0, 100.0, 0.5, -0.01, 0.02, 0.35),
    (120.0, 100.0, 2.0, 0.04, 0.01, 0.25),
]:
    inputs = dict(spot=spot, strike=strike, expiry=expiry,
                  rate=rate, dividend=dividend, vol=vol)
    call = price_and_greeks(**inputs, option_type="call")
    put = price_and_greeks(**inputs, option_type="put")
    expected_parity = spot * math.exp(-dividend * expiry) - strike * math.exp(-rate * expiry)
    assert math.isclose(call.price - put.price, expected_parity, abs_tol=1e-10)
    assert math.isclose(call.delta - put.delta, math.exp(-dividend * expiry), abs_tol=1e-12)
    assert math.isclose(call.gamma, put.gamma, abs_tol=1e-12)
    assert math.isclose(call.vega, put.vega, abs_tol=1e-12)

    for kind, result in [("call", call), ("put", put)]:
        for key, greek, step in [
            ("spot", result.delta, 1e-3),
            ("vol", result.vega, 1e-5),
            ("rate", result.rho, 1e-5),
            # Elapsed time advances while remaining expiry decreases.
            ("expiry", -result.theta, 1e-5),
        ]:
            finite_difference = (value(bump(inputs, key, step), kind)
                                 - value(bump(inputs, key, -step), kind)) / (2 * step)
            assert math.isclose(finite_difference, greek, rel_tol=1e-6, abs_tol=1e-7)
        step = 0.01
        numerical_gamma = (value(bump(inputs, "spot", step), kind)
                           - 2 * result.price
                           + value(bump(inputs, "spot", -step), kind)) / step**2
        assert math.isclose(numerical_gamma, result.gamma, rel_tol=1e-5, abs_tol=1e-7)
        pde_gap = (result.theta + (rate - dividend) * spot * result.delta
                   + 0.5 * vol**2 * spot**2 * result.gamma - rate * result.price)
        assert abs(pde_gap) < 1e-10
        assert result.gamma > 0 and result.vega > 0
    assert call.delta > 0 > put.delta
    assert call.rho > 0 > put.rho

initial = dict(spot=100.0, strike=100.0, expiry=30 / 365,
               rate=0.0, dividend=0.0, vol=0.60)
spot_only = {**initial, "spot": 102.0}
time_then_spot = {**spot_only, "expiry": 29 / 365}
final = {**time_then_spot, "vol": 0.30}
states = [initial, spot_only, time_then_spot, final]
premiums = [value(state, "call") for state in states]
changes = [after - before for before, after in zip(premiums, premiums[1:])]
assert math.isclose(premiums[0], 6.853940718253547, abs_tol=1e-10)
assert math.isclose(premiums[-1], 4.499160651451923, abs_tol=1e-10)
assert changes[0] > 0 and changes[1] < 0 and changes[2] < 0
assert math.isclose(sum(changes), premiums[-1] - premiums[0], abs_tol=1e-12)
assert round((premiums[-1] - premiums[0]) * 100, 2) == -235.48

# Unit conversions: the desk's one-vol-point vega is 0.01 times
# model vega; one-basis-point rho is 0.0001 times model rho.
greeks = price_and_greeks(**initial, option_type="call")
assert math.isclose(greeks.vega * (0.61 - 0.60), greeks.vega * 0.01, abs_tol=1e-12)

# A counterexample to the unqualified rule "long option theta is negative".
deep_put = price_and_greeks(50.0, 100.0, 1.0, 0.05, 0.0, 0.10, "put")
later_put = price_and_greeks(50.0, 100.0, 1.0 - 1 / 365, 0.05, 0.0, 0.10, "put")
assert deep_put.theta > 0 and later_put.price > deep_put.price

# An ATM-forward call does not have exactly half-delta.
atm_forward_call = price_and_greeks(100.0, 100.0, 1.0, 0.0, 0.0, 0.40, "call")
assert atm_forward_call.delta > 0.5
```

The large volatility shock needs full repricing. Small-shock Greek checks validate local derivatives; they do not make a linear explain reliable for jumps or establish the accuracy of the model for traded earnings options. A production event book also needs bid/ask marks, an exercise model, surface shocks, hedge execution, and a cash ledger.
