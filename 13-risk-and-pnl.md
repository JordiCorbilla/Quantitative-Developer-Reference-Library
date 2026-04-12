# Risk and PnL

Related chapters: [01-options.md](01-options.md), [06-interest-rates.md](06-interest-rates.md), [09-cross-asset.md](09-cross-asset.md), [12-pricing-architecture.md](12-pricing-architecture.md), [14-testing-and-validation.md](14-testing-and-validation.md), and [16-portfolio-construction-and-backtesting.md](16-portfolio-construction-and-backtesting.md).

## What This Domain Covers
Pricing tells you what a position is worth. Risk and PnL tell you what can change, why it changed, and whether the explanation is trustworthy. This is where quantitative analytics meet daily trading workflow and control infrastructure.

## Product Taxonomy and Market Structure
- Sensitivity-based risk
- Scenario and stress risk
- VaR and expected shortfall style portfolio views
- Daily PnL explain
- Intraday explain and what-if analysis
- Control reports and sign-off workflows

## Quoting and Market Conventions
- Risk only makes sense relative to a shock convention.
- PnL explain must align with the official marks and market-data cut used for reporting.
- Bucket definitions, scenario definitions, and aggregation currencies are part of the product contract for risk systems.

## Core Pricing Framework
Common decomposition:

$$
\text{PnL} \approx \sum_i \frac{\partial V}{\partial x_i}\Delta x_i + \frac{1}{2}\sum_{i,j}\frac{\partial^2 V}{\partial x_i \partial x_j}\Delta x_i \Delta x_j + \text{carry} + \text{new trades} + \text{residual}
$$

The practical challenge is not writing the formula. It is:
- defining the risk factors $x_i$,
- matching them to market-data moves,
- deciding how recalibration is handled,
- explaining residuals.

## Key Risk Measures and Sensitivities
- Delta, gamma, vega, theta, rho
- PV01, CS01, and key-rate buckets
- Cross-gammas and correlation risk
- Scenario loss under historical or hypothetical shocks
- Carry and roll-down
- Residual or unexplained PnL

## Required Data, Curves, Surfaces, and Calibration Objects
- Official trade population and positions
- End-of-day or intraday market snapshots
- Risk-factor mappings and bucket definitions
- Scenario libraries and shock rules
- Historical fixings and prior-day marks for explain
- Calibration policies that determine which parameters move with the market

## Numerical and Implementation Approaches
- Keep risk-factor definitions stable and versioned.
- Distinguish between market moves, time roll, trade activity, and model changes in explain.
- Run both local sensitivities and scenario tools; each catches different failure modes.
- Align explain calculations with the same pricing engines used for official marks, or document the approximation explicitly.

## Production Pitfalls and Sanity Checks
- Reporting Greeks that cannot reproduce observed PnL because the shock convention is different.
- Recalibrated parameters changing silently between start-of-day and end-of-day explains.
- Aggregation currency conversions applied inconsistently.
- Residual PnL accepted as normal when it actually signals missing risk factors or stale data.
- New trades and lifecycle events mixed into market-move explain.

## Illustrative Code
```python
def first_order_explain(sensitivities: dict[str, float], market_moves: dict[str, float]) -> float:
    return sum(sensitivities.get(name, 0.0) * move for name, move in market_moves.items())
```

## References and Further Reading
- PnL explain and market-risk methodology documents used by trading and risk teams
- Glasserman on risk estimation and simulation methods
- Links: [12-pricing-architecture.md](12-pricing-architecture.md), [14-testing-and-validation.md](14-testing-and-validation.md)
