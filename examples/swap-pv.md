# Simple Interest-Rate Swap PV

Related chapter: [../06-interest-rates.md](../06-interest-rates.md).

For a fixed-vs-floating swap:

```math
PV = PV_{\text{float}} - PV_{\text{fixed}}
```

Assume:
- notional: USD 100m
- fixed rate: 4.00%
- annual fixed accruals for two years
- discount factors: 0.96 and 0.92
- projected floating leg PV: USD 7.8m

Fixed leg PV:

```math
100m \times 4\% \times (0.96 + 0.92) = 7.52m
```

Swap PV to receive floating and pay fixed:

```math
7.80m - 7.52m = 0.28m
```

```python
notional = 100_000_000.0
fixed_rate = 0.04
discount_factors = [0.96, 0.92]
floating_leg_pv = 7_800_000.0

fixed_leg_pv = notional * fixed_rate * sum(discount_factors)
receive_float_pv = floating_leg_pv - fixed_leg_pv

assert abs(fixed_leg_pv - 7_520_000.0) < 1e-9
assert abs(receive_float_pv - 280_000.0) < 1e-9
```

Implementation notes:
- Real swaps need schedules, calendars, day-count conventions, reset dates, fixing logic, and projection curves.
- Modern pricing usually separates projection curves from discount curves.
- PV01 should be checked by bumping the relevant curve nodes.
