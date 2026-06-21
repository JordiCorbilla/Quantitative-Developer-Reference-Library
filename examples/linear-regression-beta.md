# Linear Regression Beta Example

Related chapter: [../23-probability-statistics-and-regression.md](../23-probability-statistics-and-regression.md).

Assume monthly market returns and stock returns:

| Month | Market return | Stock return |
| ---: | ---: | ---: |
| 1 | -2.0% | -2.8% |
| 2 | 1.0% | 1.4% |
| 3 | 3.0% | 4.1% |
| 4 | -1.0% | -1.1% |
| 5 | 2.0% | 2.7% |

Estimate beta as the OLS slope:

$$
\hat{\beta} = \frac{\sum_i (x_i - \bar{x})(y_i - \bar{y})}{\sum_i (x_i - \bar{x})^2}
$$

```python
market = [-0.02, 0.01, 0.03, -0.01, 0.02]
stock = [-0.028, 0.014, 0.041, -0.011, 0.027]

x_bar = sum(market) / len(market)
y_bar = sum(stock) / len(stock)
beta = sum((x - x_bar) * (y - y_bar) for x, y in zip(market, stock)) / sum((x - x_bar) ** 2 for x in market)
```

Result:
- beta is approximately `1.31`

Interpretation:
- For a 1% benchmark move, the fitted stock move is about 1.31%, before residual risk.
- The estimate is only meaningful with a declared benchmark, return frequency, lookback window, and residual diagnostics.
