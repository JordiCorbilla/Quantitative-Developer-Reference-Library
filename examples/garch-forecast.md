# GARCH(1,1) Forecast Example

Related chapter: [../18-volatility-products.md](../18-volatility-products.md).

The GARCH(1,1) variance update is:

$$
\sigma_t^2 = \omega + \alpha \epsilon_{t-1}^2 + \beta \sigma_{t-1}^2
$$

Assume:
- $\omega = 0.000002$
- $\alpha = 0.08$
- $\beta = 0.90$
- previous shock $\epsilon_{t-1} = -0.015$
- previous variance $\sigma_{t-1}^2 = 0.0001$

```python
omega = 0.000002
alpha = 0.08
beta = 0.90
prev_shock = -0.015
prev_variance = 0.0001

next_variance = omega + alpha * prev_shock ** 2 + beta * prev_variance
next_vol = next_variance ** 0.5
```

Result:
- next variance = `0.000110`
- next volatility = about `1.05%` for the return period

Checks:
- $\alpha + \beta = 0.98$, so volatility is highly persistent.
- If residuals are heavy-tailed, a normal innovation assumption may understate VaR.
- Parameter stability should be tested across rolling windows.
