# Cash Equities and Equity Analytics

Related chapters: [01-options.md](01-options.md), [02-futures.md](02-futures.md), [11-market-data.md](11-market-data.md), [13-risk-and-pnl.md](13-risk-and-pnl.md), and [16-portfolio-construction-and-backtesting.md](16-portfolio-construction-and-backtesting.md).

## What This Domain Covers
Cash equities look simple compared with derivatives, but equity analytics sit at the center of portfolio construction, execution, financing, and hedging workflows. This chapter focuses on what a quant developer needs to support cash books and equity-linked products correctly.

## Product Taxonomy and Market Structure
- Common and preferred shares
- ETFs and index trackers
- ADRs and cross-listed instruments
- Cash baskets, program trades, and index rebalances
- Margin-financed long and short positions

The market structure layer matters: auctions, fragmented venues, dark pools, market makers, and corporate actions all feed directly into analytics and PnL.

## Quoting and Market Conventions
- Prices are quoted per share; risk and PnL depend on lot size and position size.
- Total return includes dividends, splits, rights, spin-offs, and financing costs for shorts.
- Short inventory and borrow fees materially affect realized economics.
- Benchmark-relative language is common: beta, active weight, tracking error, sector neutrality.

## Core Pricing Framework
For many applications, the "pricing model" is simply marked market value plus corporate actions and financing:

$$
\text{EquityValue}_t = N_t \cdot S_t + \text{AccruedDividends} - \text{FinancingCost}
$$

What matters is not closed-form valuation but the consistency of:
- adjusted vs unadjusted prices,
- total-return vs price-return series,
- cash ledger treatment,
- stock borrow and rebate logic,
- benchmark and factor mapping.

Factor models and cost models turn cash equities into a risk and optimization problem rather than a derivative-pricing problem.

## Key Risk Measures and Sensitivities
- Price delta to each name
- Beta to benchmark or sector factors
- Factor exposures: size, value, momentum, quality, industry, country
- Liquidity and market-impact risk
- Short-borrow and financing exposure

## Required Data, Curves, Surfaces, and Calibration Objects
- Clean instrument identifiers and corporate-action history
- Real-time and end-of-day prices, volumes, and auction prints
- Shares outstanding, float, sector classifications, and benchmark memberships
- Borrow availability and financing curves for prime-style analytics
- Factor exposures, covariance matrices, and transaction-cost estimates for portfolio tools

## Numerical and Implementation Approaches
- Use adjusted and unadjusted price series deliberately; never mix them casually.
- Make corporate actions replayable so historical PnL can be reproduced.
- For factor risk, separate exposure estimation, covariance estimation, and portfolio aggregation.
- For execution models, prefer simple models with clear diagnostics over complex models that cannot be calibrated reliably.

## Production Pitfalls and Sanity Checks
- Split-adjusted prices used with raw position quantities.
- Dividends treated inconsistently between risk and ledger systems.
- Benchmark files and sector mappings drifting without versioning.
- Borrow cost omitted from short portfolio carry.
- Survivorship bias in historical analytics.

## Illustrative Code
```python
def cash_equity_pnl(quantity: float, start_price: float, end_price: float, dividends: float = 0.0, borrow_cost: float = 0.0) -> float:
    return quantity * (end_price - start_price + dividends) - borrow_cost
```

## References and Further Reading
- Grinold and Kahn. *Active Portfolio Management*
- Kissell. *The Science of Algorithmic Trading and Portfolio Management*
- Exchange and index-provider methodology documents
