# Factor Signal Neutralization

Related chapter: [../48-factor-models-and-systematic-signals.md](../48-factor-models-and-systematic-signals.md).

Suppose four assets have point-in-time momentum scores:

| Asset | Industry | Raw score |
| --- | --- | ---: |
| A | Technology | 1.4 |
| B | Technology | 0.6 |
| C | Banks | 0.3 |
| D | Banks | -0.5 |

The Technology mean is $1.0$, and the Banks mean is $-0.1$. Subtracting the relevant industry mean gives:

| Asset | Calculation | Neutralized score |
| --- | ---: | ---: |
| A | $1.4-1.0$ | 0.4 |
| B | $0.6-1.0$ | -0.4 |
| C | $0.3-(-0.1)$ | 0.4 |
| D | $-0.5-(-0.1)$ | -0.4 |

The sum of scores is zero within each industry. Total absolute score is $1.6$, so gross-normalized weights are:

| Asset | Weight |
| --- | ---: |
| A | 0.25 |
| B | -0.25 |
| C | 0.25 |
| D | -0.25 |

Gross exposure is $1.0$, net exposure is zero, and each industry has zero net dollar exposure.

```python
scores = {"A": 1.4, "B": 0.6, "C": 0.3, "D": -0.5}
groups = {"A": "Technology", "B": "Technology", "C": "Banks", "D": "Banks"}

group_means = {
    group: sum(scores[a] for a in scores if groups[a] == group)
    / sum(1 for a in scores if groups[a] == group)
    for group in set(groups.values())
}
neutral = {a: scores[a] - group_means[groups[a]] for a in scores}
gross = sum(abs(value) for value in neutral.values())
weights = {a: value / gross for a, value in neutral.items()}

assert abs(sum(weights.values())) < 1e-12
assert abs(sum(weights[a] for a in ("A", "B"))) < 1e-12
assert abs(sum(weights[a] for a in ("C", "D"))) < 1e-12
```

This is only one neutralization layer. Before trading, test market beta, country, currency, size, volatility, liquidity, and short-borrow exposures. Calculate the scores from the historical universe and data vintage available at the decision time, then apply explicit costs and execution delay.
