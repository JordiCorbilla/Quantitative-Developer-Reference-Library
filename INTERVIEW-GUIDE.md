# Quant Developer Interview Guide

This guide maps common interview topics to the library chapters and highlights what a strong answer should include.

## How To Answer Well
- Start with the concept in one sentence.
- State the convention or modelling assumption.
- Give the core formula only if it clarifies the answer.
- Explain implementation inputs and failure modes.
- Mention one validation or sanity check.

## Probability, Statistics, And Regression
Read: [23-probability-statistics-and-regression.md](23-probability-statistics-and-regression.md)

Common questions:
- What is covariance versus correlation?
- What assumptions sit behind OLS regression?
- What does R-squared measure?
- What is multicollinearity?
- How do you estimate beta with regression?
- Why is statistical significance not enough for a trading signal?

Good answers mention:
- return definition and sampling frequency,
- expectation, variance, covariance, and correlation,
- OLS residuals and squared-error minimization,
- linearity, independence, heteroskedasticity, normality, and multicollinearity,
- train/test splits by time and avoiding leakage,
- economic significance, costs, capacity, and robustness.

## Options And Greeks
Read: [01-options.md](01-options.md), [10-numerical-methods.md](10-numerical-methods.md)

Common questions:
- Explain put-call parity.
- What are delta, gamma, vega, theta, and rho?
- Why does implied volatility have a surface?
- How would you validate an option pricer?

Good answers mention:
- payoff and exercise style,
- discounting and dividend assumptions,
- volatility surface conventions,
- finite-difference or bump validation,
- parity and arbitrage bounds.

## Rates And Fixed Income
Read: [05-fixed-income.md](05-fixed-income.md), [06-interest-rates.md](06-interest-rates.md)

Common questions:
- Clean price vs dirty price.
- Duration vs convexity.
- How does a vanilla interest-rate swap price?
- Why do modern systems use multiple curves?

Good answers mention:
- schedules, day count, calendars,
- projection vs discount curves,
- PV01/key-rate risk,
- fixing and reset mechanics.

## Risk, VaR, ES, And Beta
Read: [13-risk-and-pnl.md](13-risk-and-pnl.md)

Common questions:
- Difference between VaR and Expected Shortfall.
- How does beta enter equity VaR?
- Why can PnL explain leave a residual?
- What is wrong with relying only on VaR?

Good answers mention:
- horizon and confidence level,
- full revaluation vs sensitivity approximation,
- backtesting exceptions,
- tail severity and stress scenarios,
- residual/idiosyncratic risk.

## Volatility And GARCH
Read: [18-volatility-products.md](18-volatility-products.md)

Common questions:
- What does GARCH(1,1) model?
- What is the stationarity condition?
- Difference between realized and implied volatility.
- What do EGARCH or GJR-GARCH add?
- What is a Markov switching model or HMM?
- How would a regime-switching GARCH model differ from a single-regime GARCH model?

Good answers mention:
- conditional variance,
- shock and volatility persistence,
- leverage/asymmetry effects,
- heavy-tailed residuals and regime stability,
- use in VaR and volatility forecasting.
- hidden states, transition probabilities, filtered probabilities, and avoiding look-ahead from smoothed states.

## Execution: VWAP, TWAP, POV, TCA
Read: [20-execution-microstructure-and-tca.md](20-execution-microstructure-and-tca.md)

Common questions:
- Difference between VWAP and TWAP.
- When would you use implementation shortfall?
- What is market impact?
- How do you evaluate an execution algo?

Good answers mention:
- benchmark choice,
- volume curve,
- participation rate,
- spread, fees, impact, and opportunity cost,
- partial fills and side-aware slippage.

## Architecture And Production
Read: [11-market-data.md](11-market-data.md), [12-pricing-architecture.md](12-pricing-architecture.md), [15-performance-and-production.md](15-performance-and-production.md)

Common questions:
- How would you design a pricing service?
- How do you version market data?
- How do you make risk results reproducible?
- How do you debug a slow or unstable analytics run?

Good answers mention:
- trade model, market state, and engine separation,
- immutable market snapshots,
- dependency lineage,
- deterministic tests,
- observability and profiling.

## Backtesting And Portfolio Construction
Read: [16-portfolio-construction-and-backtesting.md](16-portfolio-construction-and-backtesting.md)

Common questions:
- What is look-ahead bias?
- How do factor models help portfolio risk?
- What is turnover and why does it matter?
- How do you include transaction costs?

Good answers mention:
- universe membership timing,
- adjusted vs unadjusted data,
- factor covariance decomposition,
- target vs executed holdings,
- slippage and capacity.
