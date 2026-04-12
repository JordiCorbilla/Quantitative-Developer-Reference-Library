# Portfolio Construction and Backtesting

Related chapters: [03-equities.md](03-equities.md), [11-market-data.md](11-market-data.md), [12-pricing-architecture.md](12-pricing-architecture.md), [13-risk-and-pnl.md](13-risk-and-pnl.md), and [14-testing-and-validation.md](14-testing-and-validation.md).

## What This Domain Covers
Portfolio construction and backtesting sit between analytics and trading workflow. This is where expected returns, factor models, benchmark definitions, transaction costs, and rebalancing rules become an executable process rather than a research note.

For a quant developer, the hard part is rarely writing one optimizer call. The hard part is making the whole workflow consistent: adjusted data, benchmark-relative risk, constraint handling, turnover accounting, and reproducible backtests.

## Product Taxonomy and Market Structure
- Long-only and long-short portfolios
- Benchmark-relative and absolute-return mandates
- Mean-variance and risk-budgeting style optimizers
- Factor-aware and sector-neutral portfolios
- Signal-driven rebalancing strategies
- Event-driven and schedule-driven backtests

This chapter is mostly equity-oriented because that is where portfolio engineering language is most explicit, but the same patterns reappear in multi-asset allocation, overlay portfolios, and desk-level risk allocation tools.

## Quoting and Market Conventions
- Portfolio weights may be gross, net, or fully invested; do not treat them as interchangeable.
- Benchmark-relative analytics require an explicit benchmark definition, rebalance schedule, and constituent history.
- Total-return and price-return series answer different questions; backtests must declare which one they use.
- Turnover, slippage, commissions, borrow cost, and financing cost are part of the strategy definition, not after-the-fact adjustments.
- Rebalance timing matters: close-to-close, next-open, and end-of-day official marks produce different results.

Useful benchmark-relative definitions:

$$
w^{\text{active}} = w - w^{\text{bench}}
$$

$$
\text{Tracking Error} = \sqrt{(w - w^{\text{bench}})^\top \Sigma (w - w^{\text{bench}})}
$$

If a report says "active risk" without specifying benchmark, covariance horizon, and annualization convention, the number is not a stable interface.

## Core Pricing Framework
The canonical portfolio-construction problem is an optimization under risk and implementation constraints:

$$
\min_w \frac{1}{2} w^\top \Sigma w - \lambda \mu^\top w + C(w, w_{\text{prev}})
$$

subject to funding, leverage, concentration, factor, and turnover limits.

In practice:
- $\mu$ is expected return, score, alpha forecast, or sometimes an implied equilibrium return.
- $\Sigma$ is the portfolio covariance estimate, often factor-based rather than pure sample covariance.
- $C(\cdot)$ captures transaction costs, slippage, turnover penalties, or market-impact approximations.

Factor models are often the right engineering abstraction:

$$
\Sigma = B \Omega B^\top + D
$$

where:
- $B$ is the asset-by-factor exposure matrix,
- $\Omega$ is the factor covariance matrix,
- $D$ is diagonal specific risk.

This matters because portfolio tools are usually built around exposures, active bets, and risk budgets rather than pairwise asset covariances alone.

## Key Risk Measures and Sensitivities
- Portfolio volatility and marginal risk contribution
- Tracking error and active share
- Factor exposures and factor contribution to risk
- Beta to benchmark or market factor
- VaR / expected shortfall for portfolio loss views
- Drawdown, downside deviation, and tail metrics
- Concentration, liquidity, and capacity indicators
- Turnover and implementation shortfall

The important distinction is between pre-trade and post-trade risk:
- pre-trade risk answers what the target portfolio would look like,
- post-trade risk answers what was actually held after fills, drift, and costs.

## Required Data, Curves, Surfaces, and Calibration Objects
- Adjusted and unadjusted historical prices with explicit adjustment policy
- Benchmark histories, constituent mappings, and classification data
- Factor return series and exposure inputs
- Covariance estimates, shrinkage policies, and annualization conventions
- Volume, ADV, spread, and liquidity proxies for cost estimation
- Corporate actions, borrow costs, and financing assumptions
- Rebalance calendars, holiday calendars, and market-close definitions
- Portfolio and trade ledgers sufficient to replay positions through time

## Numerical and Implementation Approaches
- Separate signal generation, risk estimation, optimization, execution-cost modelling, and portfolio accounting into explicit stages.
- Keep benchmark definition and rebalance rules versioned alongside the strategy configuration.
- Prefer factor covariance models when the asset universe is large relative to the available history.
- Store both target weights and realized holdings; drift between them is analytically meaningful.
- Make turnover and cost calculations deterministic and visible in the output schema.
- Use rolling-window estimation carefully; estimation horizon, lagging, and overlapping windows can change results materially.

Useful workflow split:
- research inputs,
- cleaned market data,
- portfolio objective and constraints,
- rebalance engine,
- cost model,
- performance and attribution report.

## Production Pitfalls and Sanity Checks
- Look-ahead bias from using data that would not have been available on the rebalance date.
- Survivorship bias from backtesting only today's investable universe.
- Mixing adjusted prices for signal generation with unadjusted quantities for holdings replay.
- Benchmark files changing historically without versioning.
- Silent weight renormalization masking missing assets or failed constraints.
- Ignoring turnover and slippage until after optimization, then discovering the strategy is untradeable.
- Reporting realized performance from target weights rather than executed positions.

Minimum checks:
- weights satisfy funding and exposure constraints within tolerance,
- backtest holdings can be replayed exactly from trades and prices,
- reported turnover matches actual holdings changes,
- benchmark-relative metrics reconcile to the benchmark series used in the run,
- cost assumptions are parameterized and visible in the output,
- small changes in estimation window or rebalance date do not create implausibly discontinuous results.

## Illustrative Code
```python
import pandas as pd


def active_weights(weights: pd.Series, benchmark: pd.Series) -> pd.Series:
    aligned_weights = weights.reindex(weights.index.union(benchmark.index), fill_value=0.0)
    aligned_benchmark = benchmark.reindex(aligned_weights.index, fill_value=0.0)
    return aligned_weights - aligned_benchmark


def factor_covariance(exposures: pd.DataFrame, factor_cov: pd.DataFrame, specific_var: pd.Series) -> pd.DataFrame:
    common = exposures.values @ factor_cov.values @ exposures.values.T
    specific = pd.Series(specific_var, index=exposures.index).fillna(0.0)
    total = common + pd.DataFrame(
        [[specific[i] if i == j else 0.0 for j in exposures.index] for i in exposures.index],
        index=exposures.index,
        columns=exposures.index,
    ).values
    return pd.DataFrame(total, index=exposures.index, columns=exposures.index)


def turnover(prev_weights: pd.Series, new_weights: pd.Series) -> float:
    aligned_prev = prev_weights.reindex(new_weights.index.union(prev_weights.index), fill_value=0.0)
    aligned_new = new_weights.reindex(aligned_prev.index, fill_value=0.0)
    return float((aligned_new - aligned_prev).abs().sum())
```

This is deliberately small. A production implementation would also version data snapshots, account for trading calendars and execution timing, and distinguish target weights from executed holdings.

## References and Further Reading
- Grinold and Kahn. *Active Portfolio Management*
- Meucci. *Risk and Asset Allocation*
- Kissell. *The Science of Algorithmic Trading and Portfolio Management*
- Practitioner material on factor models, benchmark-relative risk, and transaction-cost modelling
