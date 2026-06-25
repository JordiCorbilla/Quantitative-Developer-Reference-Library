# Heston Variance Step

Related chapter: [../18-volatility-products.md](../18-volatility-products.md).

The Heston variance process is:

$$
dv_t = \kappa(\theta - v_t)dt + \sigma\sqrt{v_t}dW_t
$$

Assume:
- current variance: 0.04
- long-run variance: 0.0225
- mean reversion speed: 1.5
- vol-of-vol: 0.30
- time step: 0.01
- shock: -0.25

```python
variance = 0.04
kappa = 1.5
theta = 0.0225
vol_of_vol = 0.30
dt = 0.01
shock = -0.25

next_variance = variance + kappa * (theta - variance) * dt + vol_of_vol * (variance ** 0.5) * shock * (dt ** 0.5)
```

Result:

$$
0.04 + 1.5(0.0225 - 0.04)0.01 + 0.30\sqrt{0.04}(-0.25)\sqrt{0.01} = 0.0382375
$$

Implementation notes:
- Discrete simulation can produce negative variance unless the scheme handles the boundary.
- Calibration should define parameter bounds and whether the Feller condition is enforced.
- Heston prices are sensitive to numerical integration and surface quality.
