# Historical VaR And Expected Shortfall

Related chapter: [../13-risk-and-pnl.md](../13-risk-and-pnl.md).

Assume these are sorted one-day portfolio PnL outcomes in USD thousands, from worst to best:

| Scenario | PnL |
| ---: | ---: |
| 1 | -420 |
| 2 | -310 |
| 3 | -250 |
| 4 | -180 |
| 5 | -120 |
| 6 | -40 |
| 7 | 20 |
| 8 | 60 |
| 9 | 110 |
| 10 | 150 |

Using the worst 20% tail for illustration:

```python
losses = [420, 310, 250, 180, 120, 40, -20, -60, -110, -150]
tail_count = 2
var_80 = losses[tail_count - 1]
es_80 = sum(losses[:tail_count]) / tail_count
```

Results:
- 80% VaR = USD 310k
- 80% ES = USD 365k

Interpretation:
- VaR gives the threshold loss at the chosen confidence level.
- ES averages the losses beyond that threshold.
- A production implementation must define sorting, interpolation, confidence level, horizon, PnL basis, and backtesting rules.
