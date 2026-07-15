# Statistical Arbitrage and Pairs Trading

Related chapters: [03-equities.md](03-equities.md), [11-market-data.md](11-market-data.md), [13-risk-and-pnl.md](13-risk-and-pnl.md), [16-portfolio-construction-and-backtesting.md](16-portfolio-construction-and-backtesting.md), [20-execution-microstructure-and-tca.md](20-execution-microstructure-and-tca.md), and [23-probability-statistics-and-regression.md](23-probability-statistics-and-regression.md).

## What This Domain Covers
Statistical arbitrage turns a measured relationship into a tradeable portfolio.

The name can be misleading. It is not a risk-free arbitrage. It is a hypothesis that a relative relationship is stable enough to trade after costs, financing, borrow, and imperfect execution. A pairs trade is the clearest example: buy one asset, sell another, and expect their correctly hedged spread to revert after a temporary dislocation.

The useful mental model is a chain: define an investable universe, estimate a relationship using only information available at the time, turn its residual into a signal, trade it with realistic constraints, and monitor whether the relationship has stopped being economically meaningful.

## Product Taxonomy and Market Structure
Statistical-arbitrage strategies differ mainly by what creates the relative relationship and how quickly the portfolio must trade.

- Pairs trading in equities, ETFs, futures, or ADR/local listings.
- Cointegration and basket mean reversion across related securities.
- Factor-neutral residual portfolios.
- Index, ETF, and futures relative-value trades.
- Cross-sectional signals that rank many securities rather than trade one pair.
- Market-making and short-horizon relative value, where microstructure matters more than long-run equilibrium.

Pairs trading is often equity-oriented, but the workflow also applies to rates curve spreads, FX relative value, commodity calendar spreads, and credit basis trades. The instrument convention, liquidity, and funding mechanics change; the research discipline does not.

## Quoting and Market Conventions
- Use tradable bid/ask prices, not only mid prices, when turning a research signal into a trade.
- A long-short portfolio needs a defined gross exposure, net exposure, beta convention, and base currency.
- Short availability, borrow fee, recall risk, dividends, and corporate actions are economic inputs.
- Price, total-return, and excess-return series answer different questions. A spread must use a consistent choice.
- Entry and exit thresholds, rebalance time, delay, order type, and execution benchmark are strategy parameters, not implementation detail.

## Core Pricing Framework
The first question is not whether two prices move together. Correlation measures co-movement; it does not guarantee that a price spread is stable. A common pairs framework estimates a hedge ratio and studies the residual:

$$
s_t = y_t - \alpha - \beta x_t
$$

where $y_t$ and $x_t$ are aligned log-price series or economically comparable value series, and $s_t$ is the spread or residual. A strategy needs evidence that this residual is stationary, or at least sufficiently mean-reverting over the intended holding horizon.

The signal is often standardized with a rolling mean and volatility:

$$
z_t = \frac{s_t - \mu_t}{\sigma_t}
$$

![Statistical arbitrage research-to-trade workflow](assets/statistical-arbitrage-workflow.svg)

If $z_t$ is high, the residual is rich relative to its recent distribution; a simple rule might short $y$, buy $\beta$ units of $x$, and wait for the residual to normalize. If $z_t$ is low, the direction reverses. The rule is only a starting point: the hedge ratio, lookback window, thresholds, and exit logic must be chosen and validated out of sample.

### Correlation, Cointegration, and Mean Reversion

High correlation alone is not enough. Two trending assets can be highly correlated while their raw price difference keeps drifting. Cointegration asks whether a linear combination of non-stationary price series is stationary. It is often more relevant for a long-horizon pairs thesis, but it is still an estimated relationship that can fail.

Useful checks include:
- residual plots and rolling distribution checks;
- Augmented Dickey-Fuller or related stationarity tests, interpreted with their assumptions and limited power;
- rolling hedge-ratio stability;
- mean-reversion half-life estimates used as a holding-horizon diagnostic, not as a promise;
- factor, sector, currency, and market-beta exposures after hedge construction.

## Worked Instrument Example: A Hedged Spread
Assume a research model estimates:

$$
\log(P^A_t) = 0.10 + 1.20\log(P^B_t) + s_t
$$

and the latest residual is two rolling standard deviations above its mean. The strategy regards A as rich relative to B, so it sells USD 1.20 of A for every USD 1.00 of B bought, subject to its gross, net, beta, and borrow limits.

The trade thesis is not that A must fall or B must rise. It is that the residual should narrow. It can narrow through either leg, both legs, or a change in the estimated relationship. The hedge is therefore a portfolio construction choice, not a guarantee of market neutrality.

An example signal policy might be:
- enter when $|z_t| \geq 2.0$;
- reduce or close when $|z_t| \leq 0.5$;
- stop, de-risk, or disable the pair when the model, liquidity, borrow, or factor-risk checks fail.

The thresholds are illustrative. A production strategy selects them by an out-of-sample process that includes all trading costs and a realistic delay between observation and fill.

## Key Risk Measures and Sensitivities
- Spread z-score, residual volatility, and residual drawdown.
- Hedge-ratio, beta, sector, factor, currency, and market-neutrality exposure.
- Gross and net exposure, leverage, concentration, and pair overlap.
- Borrow availability, borrow fee, recall, dividend, and corporate-action exposure.
- Liquidity, ADV participation, bid-ask spread, and execution shortfall.
- Model-break, parameter-instability, and regime sensitivity.
- Capacity and crowding risk, especially when many portfolios trade similar residuals.

## Required Data, Curves, Surfaces, and Calibration Objects
- Point-in-time universe membership, identifiers, delisting history, and corporate actions.
- Adjusted and unadjusted price series with a documented adjustment policy.
- Bid/ask, volume, ADV, spread, volatility, and trading-calendar data.
- Short availability, borrow fee, rebate, financing, dividends, and recall data.
- Market, sector, style-factor, currency, and benchmark exposures.
- Rolling hedge estimates, stationarity diagnostics, signal history, and model version.
- Order, fill, position, and cash ledgers sufficient to replay the strategy exactly.

## Numerical and Implementation Approaches
- Separate pair selection, hedge estimation, signal calculation, portfolio construction, execution, and accounting into explicit stages.
- Use walk-forward or rolling estimation. Never estimate a hedge ratio with observations that were not available at the decision time.
- Re-estimate parameters on a documented schedule and retain the historical parameter snapshot used for each trade.
- Use robust regression or factor-neutral residual construction when one outlier or a common factor dominates the relationship.
- Model transaction costs, borrow, financing, and fill uncertainty before selecting thresholds.
- Size positions from residual volatility and liquidity while respecting portfolio-level gross, net, factor, and concentration limits.
- Add a trading halt or review state for material data changes, corporate actions, delistings, borrow recalls, and model-break alerts.

## Production Pitfalls and Sanity Checks
- Selecting pairs from the full sample and presenting the result as an out-of-sample discovery.
- Using correlation as proof of cointegration or assuming a stationary residual will remain stationary.
- Building a spread from split-adjusted price history but replaying an unadjusted position ledger.
- Ignoring borrow cost, borrow recall, dividends paid on a short, financing, and hard-to-borrow constraints.
- Treating a z-score as a timing signal without checking stale prices, asynchronous closes, or a corporate-action event.
- Re-estimating a hedge ratio after the fact and applying it to a historical trade ledger.
- Aggregating pairs that are individually neutral into a portfolio with a large hidden sector, factor, or liquidity bet.
- Optimizing entry and exit thresholds until noise looks like alpha.

Minimum checks:
- each signal can be reproduced from a point-in-time market-data and parameter snapshot;
- long and short legs reconcile to executed quantities, prices, financing, and corporate-action cashflows;
- the reported spread PnL reconciles to leg-level PnL and costs;
- exposure limits hold after fills and price drift, not only at target weights;
- performance remains credible under delayed fills, wider spreads, higher borrow cost, and pair retirement.

## Illustrative Code
```python
def z_score(value: float, mean: float, std_dev: float) -> float:
    if std_dev <= 0:
        raise ValueError("standard deviation must be positive")
    return (value - mean) / std_dev


def pair_signal(z: float, entry: float = 2.0, exit: float = 0.5) -> str:
    if entry <= exit:
        raise ValueError("entry threshold must exceed exit threshold")
    if z >= entry:
        return "short_residual"
    if z <= -entry:
        return "long_residual"
    if abs(z) <= exit:
        return "close_or_flat"
    return "hold"


def residual(y_log_price: float, x_log_price: float, alpha: float, beta: float) -> float:
    return y_log_price - alpha - beta * x_log_price
```

## References and Further Reading
- Gatev, Goetzmann, and Rouwenhorst. *Pairs Trading: Performance of a Relative-Value Arbitrage Rule*.
- Vidyamurthy. *Pairs Trading: Quantitative Methods and Analysis*.
- Avellaneda and Lee. *Statistical Arbitrage in the U.S. Equities Market*.
- Links: [16-portfolio-construction-and-backtesting.md](16-portfolio-construction-and-backtesting.md), [20-execution-microstructure-and-tca.md](20-execution-microstructure-and-tca.md), and [23-probability-statistics-and-regression.md](23-probability-statistics-and-regression.md).
