# Curve Bootstrap, Quote Residuals, And Rebuilt Risk

Related chapters: [../06-interest-rates.md](../06-interest-rates.md), [../05-fixed-income.md](../05-fixed-income.md), and [../13-risk-and-pnl.md](../13-risk-and-pnl.md).

A curve that looks smooth can still price the instruments used to build it incorrectly. Start with a one-year deposit and two-, three-, and five-year par swaps. Build discount factors, ask the curve to reproduce those quotes, then value a bond whose payments fall between the calibration nodes. Finally bump the five-year quote and rebuild: this is quote risk, not a direct bump to an unrelated zero rate.

The numbers are synthetic. We use one curve for both discounting and projection, annual swaps starting today, unit year fractions, no settlement lag or calendar adjustments, and a deposit quoted with simple interest. This simplified teaching market is deliberately different from a collateralized multi-curve desk setup. The [QuantLib maintainer's curve guide](https://www.quantlibguide.com/Curve%20bootstrapping.html) explains calibration helpers and the separation of discount and forecasting curves in a fuller implementation.

## Solve With Interpolation Active

The deposit fixes $D(1)=1/(1+r_{dep})$. For an annual par swap maturing at integer $n$, $K\sum_{i=1}^{n}D(i)=1-D(n)$. The five-year swap includes a four-year payment, so the interpolator must participate in the solve rather than being added afterwards. Between nodes we interpolate $\log D(t)$ linearly; outside the supplied interval we fail instead of silently extrapolating.

```python
import math
from bisect import bisect_left


def discount(nodes, time):
    times = sorted(nodes)
    if not times[0] <= time <= times[-1]:
        raise ValueError("Discount time is outside the calibrated interval")
    if time in nodes:
        return nodes[time]
    right = bisect_left(times, time)
    left, right = times[right - 1], times[right]
    weight = (time - left) / (right - left)
    return math.exp((1 - weight) * math.log(nodes[left]) + weight * math.log(nodes[right]))


def swap_rate(nodes, maturity):
    annuity = sum(discount(nodes, year) for year in range(1, maturity + 1))
    return (1 - discount(nodes, maturity)) / annuity


def bootstrap(deposit, swaps):
    if 1 + deposit <= 0:
        raise ValueError("Deposit implies a nonpositive discount factor")
    nodes = {0: 1.0, 1: 1 / (1 + deposit)}
    for maturity, quote in sorted(swaps.items()):
        if not isinstance(maturity, int) or maturity <= max(nodes):
            raise ValueError("Swap maturities must be increasing integer years above one")
        def residual(terminal):
            trial = {**nodes, maturity: terminal}
            return quote * sum(discount(trial, year) for year in range(1, maturity + 1)) - (1 - terminal)
        low, high = 1e-8, 2.0
        if residual(low) * residual(high) >= 0:
            raise ValueError("Quote has no root inside the benchmark bracket")
        for _ in range(100):
            middle = (low + high) / 2
            if residual(low) * residual(middle) <= 0:
                high = middle
            else:
                low = middle
        nodes[maturity] = (low + high) / 2
    return nodes


deposit = .04
quotes = {2: .042, 3: .043, 5: .045}
curve = bootstrap(deposit, quotes)
residuals = {1: (1 / curve[1] - 1) - deposit}
residuals.update({year: swap_rate(curve, year) - quote for year, quote in quotes.items()})
assert max(abs(error) for error in residuals.values()) < 1e-12
assert all(value > 0 for value in curve.values())
assert abs(discount(curve, 4) ** 2 - curve[3] * curve[5]) < 1e-14

# A 4.5-year bond: semiannual coupons, 4% annual coupon, unit principal.
cashflows = [(i / 2, .02) for i in range(1, 10)]
cashflows[-1] = (4.5, 1.02)
def bond_pv(nodes):
    return sum(amount * discount(nodes, time) for time, amount in cashflows)

base = bond_pv(curve)
bump = 1e-4
up = bootstrap(deposit, {**quotes, 5: quotes[5] + bump})
down = bootstrap(deposit, {**quotes, 5: quotes[5] - bump})
for rebuilt, sign in ((up, 1), (down, -1)):
    for year, quote in quotes.items():
        assert abs(swap_rate(rebuilt, year) - quote - (sign * bump if year == 5 else 0)) < 1e-12
quote_derivative = (bond_pv(up) - bond_pv(down)) / (2 * bump)
signed_pv01 = quote_derivative * 1e-4 * 1_000_000
actual_up_pnl = (bond_pv(up) - base) * 1_000_000
assert signed_pv01 < 0
assert abs(actual_up_pnl - signed_pv01) < .10

# Positive discount factors need not be below one when rates are negative.
negative = bootstrap(-.01, {2: -.009, 3: -.008, 5: -.007})
assert negative[1] > 1
assert abs(swap_rate(negative, 5) + .007) < 1e-12
try:
    discount(curve, 6)
except ValueError:
    pass
else:
    raise AssertionError("Extrapolation must be explicit")

print("Calibration residuals (decimal rates):", residuals)
print(f"Bond PV per principal unit: {base:.8f}")
print(f"Five-year quote signed PV01 on 1m principal: {signed_pv01:.4f}")
print(f"Actual +1bp rebuilt-curve PnL on 1m principal: {actual_up_pnl:.4f}")
```

## Read The Risk Correctly

The residual checks verify that interpolation and calibration agree. The five-year quote bump changes the final node and the interpolated payments, while earlier quote instruments still reprice. Signed PV01 is the approximate value change for an upward one-basis-point quote move; some desks instead report a positive loss measure called DV01, so store the definition with the result.

The bond calculation excludes accrued interest because valuation is at the start of its synthetic schedule. Real trades require actual accrual fractions, calendars, fixings, stubs, clean/dirty conventions, and the appropriate projection curves. For how a different interpolation space changes off-node values even with unchanged nodes, continue with [the interpolation comparison](yield-curve-interpolation-comparison.md).
