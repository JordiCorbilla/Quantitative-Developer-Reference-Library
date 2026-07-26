# Kalman Filter Dynamic Hedge-Ratio Update

Related chapters: [../31-statistical-arbitrage-and-pairs-trading.md](../31-statistical-arbitrage-and-pairs-trading.md) and [../45-time-series-forecasting-and-state-space-models.md](../45-time-series-forecasting-and-state-space-models.md).

This example performs one scalar Kalman-filter update for:

$$
y_t=\beta_t x_t+\epsilon_t,\qquad
\beta_t=\beta_{t-1}+\eta_t.
$$

It omits an intercept to keep the arithmetic visible. Assume the prior filtered state and the new aligned observation are:

- prior hedge ratio $\beta_{t-1|t-1}=1.10$;
- prior state variance $P_{t-1|t-1}=0.040$;
- process variance $Q=0.001$;
- observation variance $R=0.010$;
- $x_t=1.20$ and $y_t=1.40$.

The prediction covariance is:

$$
P_{t|t-1}=0.040+0.001=0.041.
$$

The predicted observation is $1.10(1.20)=1.32$, so the innovation is $v_t=0.08$. The innovation variance and Kalman gain are:

$$
F_t=x_t^2P_{t|t-1}+R
=1.20^2(0.041)+0.010=0.06904,
$$

$$
K_t=\frac{P_{t|t-1}x_t}{F_t}
=0.712630.
$$

The filtered hedge and its variance are:

$$
\beta_{t|t}=1.10+0.712630(0.08)=1.157010,
$$

$$
P_{t|t}=(1-K_tx_t)P_{t|t-1}=0.005939.
$$

```python
def dynamic_beta_update(
    prior_beta: float,
    prior_variance: float,
    x: float,
    y: float,
    process_variance: float,
    observation_variance: float,
) -> tuple[float, float, float]:
    if prior_variance < 0 or process_variance < 0:
        raise ValueError("state variances cannot be negative")
    if observation_variance <= 0:
        raise ValueError("observation variance must be positive")

    predicted_variance = prior_variance + process_variance
    innovation = y - prior_beta * x
    innovation_variance = x * x * predicted_variance + observation_variance
    gain = predicted_variance * x / innovation_variance

    filtered_beta = prior_beta + gain * innovation
    filtered_variance = (1.0 - gain * x) * predicted_variance
    return filtered_beta, filtered_variance, innovation


beta, variance, innovation = dynamic_beta_update(
    prior_beta=1.10,
    prior_variance=0.040,
    x=1.20,
    y=1.40,
    process_variance=0.001,
    observation_variance=0.010,
)

assert abs(beta - 1.1570104287) < 1e-10
assert abs(variance - 0.0059385863) < 1e-10
assert abs(innovation - 0.08) < 1e-12
```

Interpretation:

- the observation moves the point estimate from `1.10` to about `1.157`;
- the covariance shrinks because the observation contains information about the state;
- increasing $Q$ makes the hedge adapt faster and usually increases rebalance turnover;
- increasing $R$ places less weight on the new observation.

This update is not a trading rule. A production model estimates or validates $Q$ and $R$ in ordered training windows, supports an intercept or other state components where justified, uses numerically stable covariance updates, and timestamps whether the stored hedge is predicted or filtered. A retrospective smoothed hedge is not available to a live historical decision.
