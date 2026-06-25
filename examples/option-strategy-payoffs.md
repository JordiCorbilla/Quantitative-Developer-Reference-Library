# Option Strategy Payoff Examples

Related chapter: [../01-options.md](../01-options.md).

Assume:
- lower strike: 100
- higher strike: 110
- call premium at 100: 6
- call premium at 110: 2

For a bull call spread:

```python
def call_payoff(spot: float, strike: float) -> float:
    return max(spot - strike, 0.0)


def bull_call_spread_payoff(spot: float) -> float:
    return call_payoff(spot, 100.0) - call_payoff(spot, 110.0) - (6.0 - 2.0)
```

At expiry:

| Spot | Net payoff |
| ---: | ---: |
| 95 | -4 |
| 100 | -4 |
| 105 | 1 |
| 110 | 6 |
| 120 | 6 |

Interpretation:
- Maximum loss is the net premium paid: 4.
- Maximum profit is strike width less net premium: 10 - 4 = 6.
- The strategy is moderately bullish because upside is capped.
