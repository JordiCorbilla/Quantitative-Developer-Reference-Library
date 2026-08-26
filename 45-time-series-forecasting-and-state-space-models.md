# Time-Series Forecasting and State-Space Models

Related chapters: [11-market-data.md](11-market-data.md), [18-volatility-products.md](18-volatility-products.md), [23-probability-statistics-and-regression.md](23-probability-statistics-and-regression.md), [31-statistical-arbitrage-and-pairs-trading.md](31-statistical-arbitrage-and-pairs-trading.md), [40-point-in-time-data-and-event-systems.md](40-point-in-time-data-and-event-systems.md), [44-robust-portfolio-and-research-validation.md](44-robust-portfolio-and-research-validation.md), and [46-machine-learning-and-deep-learning-for-trading.md](46-machine-learning-and-deep-learning-for-trading.md).

## What This Domain Covers
Time-series forecasting models information in its observed order. In quantitative finance that usually means estimating a conditional mean, volatility, covariance, latent state, or economically meaningful equilibrium from data available at a stated forecast origin.

The central production question is not “which model fits best?” It is:

> Given a point-in-time information set, what quantity is forecast for which horizon, with what uncertainty, and how does the forecast behave after costs and decision latency?

This chapter covers classical univariate models, multivariate systems, and linear Gaussian state-space models. GARCH-family volatility forecasts are covered in [18-volatility-products.md](18-volatility-products.md); discrete-state hidden Markov models are introduced there as well. Machine-learning models can extend this toolkit, but do not remove the need for timestamp discipline, rolling validation, stable baselines, and calibrated uncertainty.

## Product Taxonomy and Market Structure
Forecasting work is best classified by target and horizon rather than algorithm name.

- **Univariate conditional-mean models:** AR, MA, ARMA, ARIMA, and seasonal ARIMA.
- **Models with external predictors:** ARIMAX or dynamic regression, with predictors restricted to values knowable at the forecast origin.
- **Multivariate systems:** VAR for jointly stationary series and VECM for cointegrated non-stationary series.
- **Latent-state models:** state-space models and Kalman filters for noisy observations, time-varying parameters, missing data, and nowcasting.
- **Volatility models:** EWMA, HAR-RV, ARCH/GARCH families, and regime-dependent volatility.
- **Discrete-state models:** Markov switching and HMMs, where the latent state is categorical rather than continuous.

Typical targets include returns, realized volatility, flows, spreads, yields, curve factors, volumes, and transaction costs. Price levels are frequently non-stationary; forecasting a return, difference, spread, or cointegrating error is often more defensible than extrapolating a raw level.

The forecast horizon changes the problem. A one-tick forecast is dominated by market microstructure and latency. A daily forecast must define close, timezone, and availability of end-of-day data. A monthly macro forecast must preserve publication vintages and revision history.

## Quoting and Market Conventions
- Define the forecast origin $t$, target timestamp $t+h$, horizon $h$, sampling interval, timezone, calendar, and close convention.
- State whether a target is a level, arithmetic return, log return, difference, percentage change, annualized rate, volatility, or variance.
- Keep decimal returns, percentages, basis points, volatility points, and annualization factors as distinct units.
- Align mixed calendars explicitly. Forward-filling a closed market into an open market can create artificial predictability.
- Record whether observations are event-time, exchange-time, receipt-time, or normalized bar-time.
- For revised data, train and backtest from the vintage available at each historical forecast origin, not the latest revised history.
- An exogenous regressor is admissible only if its value—or a separately generated forecast of it—would be available for the full required horizon.

A forecast record should minimally contain:

```text
model_version, training_window, information_as_of, forecast_created_at,
target_name, target_timestamp, horizon, point_forecast, interval_level,
lower_bound, upper_bound, units, data_vintage, feature_snapshot_id
```

## Core Pricing Framework
These are forecasting rather than no-arbitrage pricing models. Their output may feed valuation, risk, hedging, or execution, but the model objective and the economic decision loss must be specified separately.

### Stationarity, Differencing, and Cointegration
A weakly stationary series has time-invariant mean and variance, with autocovariance depending only on lag:

$$
\mathbb{E}[y_t]=\mu,\qquad
\operatorname{Cov}(y_t,y_{t-k})=\gamma_k.
$$

Stationarity is a modelling approximation, not a permanent property of markets. Visual inspection, rolling moments, structural-break checks, the Augmented Dickey-Fuller test, and KPSS-type tests provide complementary evidence; none proves that a relationship will persist.

The lag operator $B$ is defined by $B y_t=y_{t-1}$. First differencing gives:

$$
\Delta y_t=(1-B)y_t=y_t-y_{t-1}.
$$

Differencing can remove a stochastic trend, but unnecessary differencing discards low-frequency information and can induce moving-average behavior. Two or more $I(1)$ series are cointegrated if a non-zero linear combination is $I(0)$. Cointegration supports an error-correction representation; it does not by itself establish a profitable trade.

### AR, MA, and ARMA
An autoregressive model of order $p$ is:

$$
y_t=c+\sum_{i=1}^{p}\phi_i y_{t-i}+\epsilon_t.
$$

An MA($q$) model expresses the series using current and past innovations:

$$
y_t=\mu+\epsilon_t+\sum_{j=1}^{q}\theta_j\epsilon_{t-j}.
$$

ARMA($p,q$) combines both:

$$
\phi(B)(y_t-\mu)=\theta(B)\epsilon_t.
$$

The roots of the AR polynomial must lie outside the unit circle for covariance stationarity; the corresponding MA root condition gives invertibility. In practice, estimation libraries use a documented sign convention for $\theta$, so parameter interchange between implementations requires a test against identical data.

### ARIMA, SARIMA, and ARIMAX
ARIMA($p,d,q$) applies an ARMA model after $d$ differences:

$$
\phi(B)(1-B)^d y_t=c+\theta(B)\epsilon_t.
$$

Seasonal ARIMA extends this with seasonal period $s$:

$$
\Phi(B^s)\phi(B)(1-B)^d(1-B^s)^D y_t
=c+\Theta(B^s)\theta(B)\epsilon_t.
$$

Seasonality must follow the data-generating calendar. “Five trading days” is not an invariant weekly season when holidays intervene, and intraday seasonality should usually be modeled in exchange-local event time.

In the common regression-with-ARIMA-errors convention, ARIMAX adds known or forecast external inputs to a regression and models its residual $u_t$ with ARIMA dynamics:

$$
y_t=c+\boldsymbol{\beta}^{\mathsf T}x_t+u_t,
\qquad
\phi(B)(1-B)^d u_t=\theta(B)\epsilon_t.
$$

Some libraries instead implement ARMAX or transfer-function conventions in which lag polynomials operate on $y_t$, $x_t$, or both. These parameterizations are not algebraically interchangeable, so production code must record the library and exact equation rather than relying on the label `ARIMAX` alone.

Using contemporaneous $x_t$ is leakage if $x_t$ arrives after the trading decision. For multi-step forecasts, future $x_{t+1:t+h}$ must be known by construction—such as calendar indicators—or supplied by a separately validated forecast whose uncertainty is propagated.

### VAR and VECM
For a stationary vector $\mathbf y_t$, a VAR($p$) is:

$$
\mathbf y_t=\mathbf c+\sum_{i=1}^{p}A_i\mathbf y_{t-i}+\boldsymbol\epsilon_t.
$$

The parameter count grows approximately with the square of the number of series. Shrinkage, economically constrained variable selection, or factor compression is often needed when the sample is short.

A cointegrated VAR can be written as a VECM:

$$
\Delta\mathbf y_t
=\Pi\mathbf y_{t-1}
+\sum_{i=1}^{p-1}\Gamma_i\Delta\mathbf y_{t-i}
+\boldsymbol\epsilon_t,
\qquad
\Pi=\alpha\beta^{\mathsf T}.
$$

Columns of $\beta$ represent cointegrating relations; $\alpha$ describes how each series adjusts toward them. The Johansen procedure estimates cointegration rank in a multivariate system, but its results depend on lag order, deterministic terms, sample window, and structural stability.

### State-Space Models and the Kalman Filter
A linear Gaussian state-space model separates an unobserved state $\mathbf a_t$ from noisy observations $\mathbf y_t$:

$$
\mathbf a_t=T_t\mathbf a_{t-1}+R_t\boldsymbol\eta_t,
\qquad \boldsymbol\eta_t\sim\mathcal N(0,Q_t),
$$

$$
\mathbf y_t=Z_t\mathbf a_t+\mathbf d_t+\boldsymbol\epsilon_t,
\qquad \boldsymbol\epsilon_t\sim\mathcal N(0,H_t).
$$

The Kalman prediction and update are:

$$
\mathbf a_{t|t-1}=T_t\mathbf a_{t-1|t-1},
\qquad
P_{t|t-1}=T_tP_{t-1|t-1}T_t^{\mathsf T}+R_tQ_tR_t^{\mathsf T},
$$

$$
\mathbf v_t=\mathbf y_t-Z_t\mathbf a_{t|t-1}-\mathbf d_t,
\quad
F_t=Z_tP_{t|t-1}Z_t^{\mathsf T}+H_t,
\quad
K_t=P_{t|t-1}Z_t^{\mathsf T}F_t^{-1},
$$

$$
\mathbf a_{t|t}=\mathbf a_{t|t-1}+K_t\mathbf v_t,
\qquad
P_{t|t}=P_{t|t-1}-K_tF_tK_t^{\mathsf T}.
$$

Filtering uses observations through $t$ and is live-usable. Smoothing conditions on later observations and is appropriate for retrospective estimation, not a historical trading signal unless the delay is represented. A numerically stable implementation uses matrix factorizations or square-root filters rather than explicit matrix inverses.

A Kalman model usually has a continuous latent state with Gaussian innovations. An HMM has a discrete latent state and an emission distribution. Switching state-space models combine both ideas, at significantly higher estimation and model-risk cost.

## Worked Instrument Example
Suppose a demeaned daily spread follows an estimated AR(1):

$$
y_t=0.80y_{t-1}+\epsilon_t,\qquad
\operatorname{Var}(\epsilon_t)=0.0004.
$$

At the forecast origin, $y_t=0.050$. The one- and three-day conditional forecasts are:

$$
\hat y_{t+1|t}=0.80(0.050)=0.040,
$$

$$
\hat y_{t+3|t}=0.80^3(0.050)=0.0256.
$$

The three-day innovation variance is:

$$
0.0004(1+0.80^2+0.80^4)=0.00081984,
$$

so the forecast standard deviation is about $0.0286$. A Gaussian 95% interval is approximately $0.0256\pm1.96(0.0286)$, or $[-0.0305,0.0817]$.

The point forecast mean-reverts, but the interval still spans both signs. A trading policy must compare the expected convergence with costs, uncertainty, position risk, and the probability that the fitted relationship has changed.

## Key Risk Measures and Sensitivities
- Forecast error by horizon: bias, MAE, RMSE, quantile loss, or a decision-specific loss.
- Empirical interval coverage and conditional coverage across calm and stressed periods.
- Parameter uncertainty, coefficient stability, root proximity to the unit circle, and cointegration-rank stability.
- Innovation covariance, residual autocorrelation, residual heteroskedasticity, and tail behavior.
- Sensitivity to training window, lag order, differencing, deterministic terms, and outlier policy.
- Forecast decay, turnover induced by revisions, and performance after latency and costs.
- State uncertainty, Kalman innovation size, normalized innovation squared, and covariance conditioning.
- Benchmark-relative value: a complex model should beat an appropriate naive forecast out of sample.

## Required Data, Curves, Surfaces, and Calibration Objects
- Point-in-time observations with event, publication, receipt, and effective timestamps where relevant.
- Trading calendars, timezones, bar definitions, missing-observation policy, and corporate-action treatment.
- Data vintages for revised macroeconomic or fundamental series.
- Target transformation and inverse-transformation metadata.
- Feature definitions, lags, release schedules, and future-availability rules.
- Training window, forecast origins, purge or embargo rules, refit schedule, and hyperparameter history.
- Estimated coefficients, innovation covariance, state vector, state covariance, and model version.
- Benchmark forecasts and an immutable record of predictions made before outcomes were known.

## Numerical and Implementation Approaches
### Model-Development Sequence
1. Define the target, horizon, decision time, units, and loss before selecting a model.
2. Establish naive baselines: last value, historical mean, seasonal naive, random walk, or EWMA as appropriate.
3. Apply transformations using training-window parameters only.
4. Select lags and deterministic terms inside each training fold, not once on the complete history.
5. Produce rolling-origin or expanding-window forecasts and store every forecast before observing its target.
6. Evaluate accuracy, interval calibration, economic value, turnover, and stability by regime and horizon.
7. Shadow the live pipeline and reconcile feature snapshots before allowing forecasts into decisions.

### Forecast Horizons
- **Recursive:** fit one-step dynamics and feed forecasts back into the model. It is parsimonious but compounds misspecification.
- **Direct:** fit a separate model for each horizon. It reduces recursion error but uses more parameters and may produce incoherent paths.
- **Joint/multiple-output:** estimate horizons together and preserve cross-horizon dependence, at greater complexity.

Report the method and horizon explicitly. Never compare a one-step recursive validation score with a five-step live decision as though they were the same target.

### Rolling Validation and Leakage Controls
Random train/test splits are generally invalid for dependent time series. Use ordered splits with the full operational delay:

```text
train through t -> compute features knowable at t -> predict t+h
-> wait through label horizon and publication lag -> score prediction
```

Purge overlapping labels when they share future returns, and embargo adjacent samples when the feature or label construction leaks across fold boundaries. Fit scalers, PCA loadings, imputation rules, lag order, cointegration vectors, and feature selection within the training window. Preserve delisted instruments and point-in-time universe membership.

### Diagnostics and Uncertainty
- Inspect residual ACF/PACF and apply Ljung-Box-type portmanteau tests at economically relevant lags.
- Check residual scale, asymmetry, tails, structural breaks, and conditional heteroskedasticity.
- For VAR/VECM, inspect stability roots and residual cross-correlation.
- For a Kalman filter, monitor standardized innovations, missing-observation behavior, and whether $Q$ or $H$ is collapsing to a boundary.
- Evaluate forecast intervals out of sample. Gaussian analytic intervals omit parameter, model, and regime uncertainty.
- Use residual, block, parametric, or Bayesian simulation only when its dependence and refitting assumptions match the use case.

An implementation contract should reject forecasts whose feature snapshot is incomplete, whose `information_as_of` exceeds the decision timestamp, or whose horizon and unit do not match the consuming strategy.

## Production Pitfalls and Sanity Checks
- Testing stationarity once on the full sample and treating the result as timeless.
- Differencing a series until a test passes without checking economic meaning or invertibility.
- Choosing ARIMA order, cointegration rank, or state noise from the full evaluation period.
- Using revised macro history or finalized bars that were unavailable at the forecast origin.
- Feeding realized future exogenous values into an ARIMAX backtest.
- Forward-filling prices across market closures and interpreting the resulting lead-lag as alpha.
- Treating in-sample Kalman-smoothed states as if they were live filtered states.
- Ignoring parameter uncertainty and publishing an overly narrow analytic interval.
- Selecting a model by one aggregate error metric while performance is concentrated in one regime.
- Comparing models on different forecast origins, missing-value subsets, or transaction-cost assumptions.

Minimum sanity checks:

- all forecasts join one-to-one to an immutable forecast origin and target timestamp;
- a naive benchmark is evaluated on exactly the same observations;
- model inputs can be recreated from the recorded vintage and feature snapshot;
- residual diagnostics and interval coverage are reported by horizon;
- estimates are invariant to adding data strictly after the forecast origin;
- inverse transformations preserve units and do not introduce retransformation bias silently;
- live filtering never consumes a smoothed state or a late-arriving observation.

## Illustrative Code
```python
from math import sqrt


def ar1_forecast(
    current: float,
    intercept: float,
    phi: float,
    innovation_variance: float,
    horizon: int,
) -> tuple[float, float]:
    """Return the AR(1) conditional mean and innovation variance at a horizon."""
    if horizon < 1:
        raise ValueError("horizon must be positive")
    if innovation_variance < 0:
        raise ValueError("innovation variance cannot be negative")

    mean = current
    variance = 0.0
    for _ in range(horizon):
        mean = intercept + phi * mean
        variance = phi * phi * variance + innovation_variance
    return mean, variance


def scalar_kalman_update(
    predicted_state: float,
    predicted_variance: float,
    observation: float,
    observation_variance: float,
) -> tuple[float, float, float]:
    """One scalar filtering update; returns state, variance, and innovation."""
    if predicted_variance < 0 or observation_variance <= 0:
        raise ValueError("invalid covariance")
    innovation = observation - predicted_state
    innovation_variance = predicted_variance + observation_variance
    gain = predicted_variance / innovation_variance
    filtered_state = predicted_state + gain * innovation
    filtered_variance = (1.0 - gain) * predicted_variance
    return filtered_state, filtered_variance, innovation


mean, variance = ar1_forecast(
    current=0.050,
    intercept=0.0,
    phi=0.80,
    innovation_variance=0.0004,
    horizon=3,
)
assert abs(mean - 0.0256) < 1e-12
assert abs(sqrt(variance) - 0.028632848) < 1e-8
```

The functions demonstrate mechanics, not estimation. Production code also validates timestamps and units, stores fitted-state provenance, uses stable linear algebra, and evaluates forecasts on an ordered out-of-sample schedule.

## References and Further Reading
- Box, Jenkins, Reinsel, and Ljung. *Time Series Analysis: Forecasting and Control*.
- Hamilton. *Time Series Analysis*.
- Durbin and Koopman. *Time Series Analysis by State Space Methods*.
- Hyndman and Athanasopoulos. *Forecasting: Principles and Practice*.
- Lütkepohl. *New Introduction to Multiple Time Series Analysis*.
- Engle and Granger on cointegration and error correction.
- Johansen on cointegration rank in Gaussian vector autoregressive systems.
- Links: [18-volatility-products.md](18-volatility-products.md), [31-statistical-arbitrage-and-pairs-trading.md](31-statistical-arbitrage-and-pairs-trading.md), and [44-robust-portfolio-and-research-validation.md](44-robust-portfolio-and-research-validation.md).
