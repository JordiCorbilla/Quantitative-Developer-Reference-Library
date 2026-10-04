# Pairs Trading Spread Signal

Related chapter: [31-statistical-arbitrage-and-pairs-trading.md](../31-statistical-arbitrage-and-pairs-trading.md).

This is a small signal calculation, not evidence that a pair is tradeable.

Assume a fixed, previously estimated residual has a current value of `0.090`, a rolling mean of `0.010`, and a rolling standard deviation of `0.040`.

```math
z = \frac{0.090 - 0.010}{0.040} = 2.0
```

With an illustrative entry threshold of 2.0, this is a `short_residual` signal: sell the asset represented by the positive residual and buy its hedge. An implementation still needs to check borrow availability, bid/ask prices, factor exposures, portfolio limits, and whether the residual was produced from point-in-time data.

```python
def z_score(residual: float, mean: float, std_dev: float) -> float:
    if std_dev <= 0:
        raise ValueError("standard deviation must be positive")
    return (residual - mean) / std_dev


signal = z_score(residual=0.090, mean=0.010, std_dev=0.040)
assert signal == 2.0
```

The pair should close, reduce, or be re-evaluated according to its documented exit, stop, and model-break rules. A z-score is a research output, not an instruction to trade without constraints.
