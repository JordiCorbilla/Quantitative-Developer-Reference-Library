# Factor Models and Systematic Signal Research

Related chapters: [03-equities.md](03-equities.md), [13-risk-and-pnl.md](13-risk-and-pnl.md), [16-portfolio-construction-and-backtesting.md](16-portfolio-construction-and-backtesting.md), [23-probability-statistics-and-regression.md](23-probability-statistics-and-regression.md), [31-statistical-arbitrage-and-pairs-trading.md](31-statistical-arbitrage-and-pairs-trading.md), [40-point-in-time-data-and-event-systems.md](40-point-in-time-data-and-event-systems.md), [44-robust-portfolio-and-research-validation.md](44-robust-portfolio-and-research-validation.md), and [45-time-series-forecasting-and-state-space-models.md](45-time-series-forecasting-and-state-space-models.md).

## What This Domain Covers
Factor models explain common return drivers; systematic signals rank or time positions using reproducible rules. The two are related but not interchangeable. A value exposure can be an intentional alpha, an unwanted risk, or both. A momentum score is not a portfolio until it has been lagged, neutralized, sized, costed, executed, and recorded in a position ledger.

This chapter connects named asset-pricing models such as CAPM, Fama-French, and Carhart to practical multi-factor risk systems and to common signal families: momentum, mean reversion, breakout, trend following, seasonality, and cross-sectional ranking.

## Product Taxonomy and Market Structure
Useful distinctions include:

- **Return factor versus characteristic:** a traded factor return is a portfolio time series; a characteristic is an asset attribute such as book-to-market or trailing momentum.
- **Explanatory versus predictive model:** a model that attributes realized return need not forecast future return.
- **Time-series versus cross-sectional signal:** a time-series rule compares an asset with its own history; a cross-sectional rule compares assets at the same decision time.
- **Statistical versus fundamental factor:** PCA and residual factors are data-derived; value, quality, carry, or industry factors have an economic definition.
- **Risk model versus alpha model:** a risk model estimates common covariance and specific risk; an alpha model estimates expected return. Using the same noisy signal for both can create circular confidence.

Common systematic signal families:

- medium-horizon momentum and trend following;
- short-horizon reversal and residual mean reversion;
- price, range, or volatility breakouts;
- calendar, roll, carry, or seasonal effects;
- cross-sectional value, quality, momentum, defensive, and carry rankings;
- event-conditioned signals whose features and labels are point-in-time correct.

## Quoting and Market Conventions
- State whether returns are simple or logarithmic, price or total returns, local or base-currency returns, and raw or excess of cash.
- Define the market close, lookback endpoints, skip periods, rebalance timestamp, execution delay, and holding horizon.
- Fundamental characteristics need an availability timestamp, reporting lag, restatement policy, currency, fiscal calendar, and denominator convention.
- A factor named `value`, `quality`, or `momentum` is not self-defining. Persist its formula, universe, winsorization, standardization, neutralization, weighting, and rebalance rule.
- Cross-sectional ranks must define treatment of ties, missing values, microcaps, suspended securities, delistings, and assets without borrow.
- Factor returns may be long-short, benchmark-relative, beta-neutral, sector-neutral, or fully invested. Record gross and net exposure.

## Core Pricing Framework
### CAPM And Multi-Factor Return Models

The Capital Asset Pricing Model writes asset excess return as market exposure plus residual:

$$
r_{i,t}-r_{f,t}
=
\alpha_i+\beta_{i,M}(r_{M,t}-r_{f,t})+\epsilon_{i,t}.
$$

CAPM is a useful baseline for beta and abnormal-return attribution, not a complete description of expected returns. Beta depends on benchmark, currency, frequency, window, weighting, and regime.

The Fama-French three-factor model adds size and value:

$$
r_i-r_f
=
\alpha_i+\beta_M MKT+\beta_S SMB+\beta_H HML+\epsilon_i.
$$

The five-factor model adds profitability `RMW` and investment `CMA`. The Carhart four-factor specification adds a momentum factor, often labelled `MOM` or `UMD`, to the three-factor model. These names identify published construction families, not universal data columns: source, breakpoints, region, weighting, and formation lag still matter.

### Barra-Style Cross-Sectional Risk Models

A practical multi-factor risk model represents asset returns as:

$$
r_t = B_t f_t + \epsilon_t,
\qquad
\Sigma_t = B_t\Omega_tB_t^\top + D_t,
$$

where \(B_t\) contains industry and style exposures, \(f_t\) contains factor returns, \(\Omega_t\) is factor covariance, and \(D_t\) contains specific variances. Commercial Barra models have documented proprietary specifications; “Barra-style” should mean this engineering structure, not a claim that an internal approximation reproduces a vendor model.

Exposure estimation can be:

- observed, such as country or industry membership;
- characteristic-based, such as standardized size or leverage;
- regression-estimated, such as market beta;
- statistical, such as principal-component loadings.

### Signal Families

A volatility-scaled time-series momentum score can be written:

$$
s_{i,t}^{TS}
=
\frac{\sum_{u=t-h}^{t-k} r_{i,u}}
{\widehat{\sigma}_{i,t}},
$$

where \(k\) is an explicit skip period and every input is available before the decision. A moving-average crossover or channel breakout is another trend rule, but window choice and trade timing must be part of the strategy definition.

A mean-reversion score often standardizes a residual:

$$
z_{i,t}=\frac{x_{i,t}-\widehat{\mu}_{i,t}}{\widehat{\sigma}_{i,t}}.
$$

The residual may be relative to a pair, sector, factor model, curve, or state-space estimate. It is not evidence that the relationship will continue to revert.

For a cross-sectional characteristic \(x_{i,t}\), a simple neutralized score is:

$$
\widetilde{x}_{i,t}
=
x_{i,t}
-
\operatorname{groupmean}(x_{i,t}),
$$

followed by winsorization, scaling, and portfolio constraints. Regression residualization can neutralize several exposures at once, but the design matrix and weights must be point-in-time.

Seasonal signals compare like-for-like calendar states across enough independent history. Month-of-year averages, day-of-week effects, commodity delivery seasons, and index-rebalance patterns are especially vulnerable to multiple testing and structural change. A seasonal chart is not a tradable signal until spread, capacity, release timing, and publication bias are included.

## Worked Instrument Example
Suppose four assets have raw momentum scores:

| Asset | Industry | Raw score |
| --- | --- | ---: |
| A | Technology | 1.4 |
| B | Technology | 0.6 |
| C | Banks | 0.3 |
| D | Banks | -0.5 |

Each industry mean is \(1.0\) for Technology and \(-0.1\) for Banks. Subtracting the contemporaneous industry mean gives:

| Asset | Industry-neutral score |
| --- | ---: |
| A | 0.4 |
| B | -0.4 |
| C | 0.4 |
| D | -0.4 |

Scaling absolute weights to gross exposure \(1.0\) produces weights \(+0.25,-0.25,+0.25,-0.25\). The portfolio is industry-dollar neutral by construction, but it is not automatically neutral to beta, size, country, liquidity, or nonlinear exposures. Those require a risk model and explicit constraints.

The calculation is reproduced in [examples/factor-signal-neutralization.md](examples/factor-signal-neutralization.md).

## Key Risk Measures and Sensitivities
- Gross, net, beta, country, industry, style, currency, and duration exposure.
- Factor contribution to variance and factor-versus-specific PnL attribution.
- Information coefficient, rank IC, hit rate, turnover, decay by horizon, and breadth.
- Long-short spread return before and after spread, impact, borrow, financing, and taxes.
- Weight and PnL concentration by name, factor, sector, date, event, and data source.
- Sensitivity to universe, winsorization, lag, skip period, neutralization, and rebalance timing.
- Drawdown, tail loss, crowding, capacity, short squeeze, and factor crash scenarios.
- Parameter and definition drift between research, risk, and production implementations.

## Required Data, Curves, Surfaces, and Calibration Objects
- Point-in-time prices, returns, corporate actions, delistings, and investable-universe membership.
- Fundamental statement and estimate vintages with publication and knowledge timestamps.
- Classification histories, benchmark histories, country/currency mappings, and security-master lineage.
- Factor definitions, factor-return series, exposure snapshots, covariance, and specific risk.
- Volume, spread, borrow, financing, locate, limit, and venue data for implementation.
- Signal specifications containing formula, inputs, lags, windows, transformations, and missing-value policy.
- Trial registry, fold definitions, code/configuration version, target and executed weights, fills, and PnL.

## Numerical and Implementation Approaches
- Build features first, freeze their availability timestamps, and only then create forward labels.
- Fit transformations on training data. Cross-sectional winsorization and standardization still leak if calculated using unavailable constituents or later corrections.
- Keep raw characteristics, transformed scores, neutralized scores, alpha forecasts, target weights, and executed holdings as separate versioned objects.
- Use weighted least squares or constrained regression when estimating factor returns if the weighting and robustness policy are economically justified.
- Test signals by chronological walk-forward evaluation with purging and embargo where labels overlap.
- Combine signals only after checking correlation, common data lineage, turnover interaction, and whether apparent diversification survives costs and stress.
- Reconcile factor-model PnL to position-level PnL and preserve an explicit unexplained residual.

## Production Pitfalls and Sanity Checks
- Treating an asset-pricing factor as a guaranteed alpha.
- Calling a characteristic “Fama-French” or “Barra” without reproducing the relevant construction.
- Using revised fundamentals, current classifications, or surviving securities in historical ranks.
- Standardizing across the full sample or using the same close for both feature and fill.
- Choosing momentum windows, breakout levels, seasonal cells, or neutralization rules on the final test period.
- Ignoring short borrow, market impact, limit states, and crowding in long-short backtests.
- Neutralizing sector dollars while leaving a large beta, duration, volatility, or liquidity exposure.
- Reporting a high in-sample t-statistic without the number of tried variants and out-of-sample decay.

Minimum checks include zero-sum constraints where intended, exact reconstruction of each score from its vintage inputs, stable exposure units, no feature timestamp after the decision cutoff, reproducible constituent counts, factor-plus-specific PnL reconciliation, and performance under delayed fills and higher costs.

## Illustrative Code
```python
from collections import defaultdict


def group_neutralize(
    values: dict[str, float],
    groups: dict[str, str],
) -> dict[str, float]:
    grouped: dict[str, list[float]] = defaultdict(list)
    for asset, value in values.items():
        grouped[groups[asset]].append(value)

    means = {
        group: sum(group_values) / len(group_values)
        for group, group_values in grouped.items()
    }
    return {
        asset: value - means[groups[asset]]
        for asset, value in values.items()
    }


def gross_normalize(scores: dict[str, float]) -> dict[str, float]:
    gross = sum(abs(score) for score in scores.values())
    if gross <= 0:
        raise ValueError("gross normalization requires a non-zero score")
    return {asset: score / gross for asset, score in scores.items()}
```

This code demonstrates the arithmetic only. A production implementation needs point-in-time universes, missing-data controls, robust transformations, exposure constraints, lot sizing, costs, and immutable model versions.

## References and Further Reading
- Sharpe. *Capital Asset Prices: A Theory of Market Equilibrium under Conditions of Risk*.
- Fama and French on common risk factors and the five-factor asset-pricing model.
- Carhart. *On Persistence in Mutual Fund Performance*.
- Grinold and Kahn. *Active Portfolio Management*.
- MSCI documentation for the architecture and conventions of Barra equity risk models.
- Jegadeesh and Titman on cross-sectional return momentum.
- Moskowitz, Ooi, and Pedersen on time-series momentum.
- Gatev, Goetzmann, and Rouwenhorst on pairs trading.
