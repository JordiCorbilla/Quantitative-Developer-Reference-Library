# Vasicek Short-Rate Step

Related chapter: [../06-interest-rates.md](../06-interest-rates.md).

The Vasicek model is:

$$
dr_t = a(b-r_t)dt + \sigma dW_t
$$

Assume:
- current short rate: 3.00%
- mean reversion: 0.50
- long-run mean: 4.00%
- time step: 0.25 years
- volatility: 1.00%
- shock: -0.20

```python
rate = 0.03
mean_reversion = 0.50
long_run_mean = 0.04
dt = 0.25
volatility = 0.01
shock = -0.20

next_rate = rate + mean_reversion * (long_run_mean - rate) * dt + volatility * shock
```

Result:

$$
0.03 + 0.50(0.04 - 0.03)0.25 + 0.01(-0.20) = 0.02925
$$

So the next simulated short rate is 2.925%.

Implementation notes:
- Vasicek is useful for intuition but can produce negative rates.
- Hull-White extends this idea with a time-dependent drift to fit today's curve.
- Model choice should match the product and calibration instruments.
