# EWMA and HAR-RV Forecast

Related chapters: [../18-volatility-products.md](../18-volatility-products.md) and [../45-time-series-forecasting-and-state-space-models.md](../45-time-series-forecasting-and-state-space-models.md).

This example compares two transparent next-day variance calculations. Both inputs and outputs are daily decimal variance.

## EWMA Update
Assume:

- previous variance $h_{t-1}=0.000100$;
- previous daily return $r_{t-1}=-0.020$;
- decay $\lambda=0.94$.

Then:

$$
h_t
=0.94(0.000100)+0.06(-0.020)^2
=0.000118.
$$

The daily volatility is $\sqrt{0.000118}=1.0863\%$. The sign of the return does not affect this symmetric EWMA update.

## HAR-RV Forecast
Suppose realized-variance inputs computed through the forecast origin are:

- daily $RV_t=0.000120$;
- trailing five-day mean $\overline{RV}_{t,5}=0.000100$;
- trailing 22-day mean $\overline{RV}_{t,22}=0.000080$.

With $\beta_0=0.000005$, $\beta_d=0.40$, $\beta_w=0.35$, and $\beta_m=0.20$:

$$
\widehat{RV}_{t+1}
=0.000005
+0.40(0.000120)
+0.35(0.000100)
+0.20(0.000080)
=0.000104.
$$

That is a daily volatility forecast of about $1.0198\%$, or about $16.19\%$ under a simple $\sqrt{252}$ annualization.

```python
from math import sqrt


def ewma_variance(previous_variance: float, previous_return: float, decay: float) -> float:
    if previous_variance < 0:
        raise ValueError("variance cannot be negative")
    if not 0.0 < decay < 1.0:
        raise ValueError("decay must be between zero and one")
    return decay * previous_variance + (1.0 - decay) * previous_return**2


def har_rv(
    intercept: float,
    daily_beta: float,
    weekly_beta: float,
    monthly_beta: float,
    daily_rv: float,
    weekly_rv: float,
    monthly_rv: float,
) -> float:
    forecast = (
        intercept
        + daily_beta * daily_rv
        + weekly_beta * weekly_rv
        + monthly_beta * monthly_rv
    )
    if forecast < 0:
        raise ValueError("negative variance forecast")
    return forecast


ewma = ewma_variance(0.000100, -0.020, 0.94)
har = har_rv(
    intercept=0.000005,
    daily_beta=0.40,
    weekly_beta=0.35,
    monthly_beta=0.20,
    daily_rv=0.000120,
    weekly_rv=0.000100,
    monthly_rv=0.000080,
)

assert abs(ewma - 0.000118) < 1e-15
assert abs(har - 0.000104) < 1e-15
assert abs(sqrt(har) * sqrt(252) - 0.1619) < 0.0001
```

The two forecasts are not directly comparable unless they use the same return coverage. For example, an EWMA based on close-to-close returns and HAR-RV based only on intraday returns have different targets. Production validation also fixes the sampling grid, overnight treatment, holiday policy, bad-tick controls, coefficient fit window, and forecast timestamp.
