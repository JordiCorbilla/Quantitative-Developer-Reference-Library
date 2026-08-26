# Large Order Participation Limit

Related chapter: [20-execution-microstructure-and-tca.md](../20-execution-microstructure-and-tca.md).

Assume a 400,000-share parent buy order. The first two hours are forecast to account for 1,000,000 shares of market volume, and the mandate sets a 10% maximum participation rate.

$$
\text{maximum child quantity} = 1{,}000{,}000 \times 10\% = 100{,}000\text{ shares}
$$

```python
def participation_limit(forecast_volume: float, max_participation: float, parent_remaining: float) -> float:
    if not 0 < max_participation <= 1:
        raise ValueError("max_participation must be in (0, 1]")
    return min(forecast_volume * max_participation, parent_remaining)


assert participation_limit(1_000_000, 0.10, 400_000) == 100_000
assert participation_limit(1_000_000, 0.10, 80_000) == 80_000
```

The limit must be recalculated from observed volume and current conditions. It does not guarantee a neutral market impact: spread, volatility, order-book depth, news, and other participants may all change the cost of the trade.
