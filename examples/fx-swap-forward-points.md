# FX Swap Forward Points Example

Related chapter: [../04-fx.md](../04-fx.md).

Assume a EUR/USD spot rate of 1.1000 and a 3-month forward rate of 1.0960.

The forward points are:

$$
1.0960 - 1.1000 = -0.0040
$$

In pip-style points:

$$
-0.0040 \times 10{,}000 = -40
$$

An FX swap can be viewed as:
- near leg: exchange EUR and USD on the spot date,
- far leg: reverse the exchange on the maturity date at the forward rate.

If a treasurer needs USD today but expects to reverse the funding later, the swap locks the near exchange and far exchange. The risk is not that the two legs are undefined; the risk is that future rollover points, liquidity, margin, or counterparty limits may change if the position has to be rolled again.

```python
def forward_points(spot: float, forward: float, points_scale: float = 10_000.0) -> float:
    return (forward - spot) * points_scale


spot = 1.1000
forward = 1.0960
points = forward_points(spot, forward)
```

Implementation notes:
- Preserve pair orientation. EUR/USD points are not USD/EUR points.
- Store spot date, far date, near-leg cashflows, and far-leg cashflows explicitly.
- Treat collateral, margin, netting set, and counterparty limits as part of the economics for production risk.
