# ETFs, Index Products, and Rebalances

Related chapters: [03-equities.md](03-equities.md), [11-market-data.md](11-market-data.md), [16-portfolio-construction-and-backtesting.md](16-portfolio-construction-and-backtesting.md), [20-execution-microstructure-and-tca.md](20-execution-microstructure-and-tca.md), and [22-model-governance-and-ipv.md](22-model-governance-and-ipv.md).

## What This Domain Covers
Index products turn a rules-based basket into something tradable.

An ETF, index future, index option, or swap references a portfolio that changes through time. The visible product may look like one ticker, but the analytics depend on constituents, weights, corporate actions, creation/redemption baskets, benchmark methodology, and rebalance timing.

For a quant developer, the important story is that index exposure is not static. The product is a wrapper around rules, data, and operational events.

## Product Taxonomy and Market Structure
Start with the wrapper around the index exposure.

- ETFs and exchange-traded products.
- Index futures and options.
- Index total return swaps.
- Custom baskets and program trades.
- Leveraged and inverse ETFs.
- Thematic, factor, sector, and country index products.

## Quoting and Market Conventions
- ETF price, NAV, iNAV, and creation/redemption basket are different objects.
- Index levels may be price return, total return, or net total return.
- Rebalance and reconstitution schedules define future holdings changes.
- Corporate actions and free-float adjustments affect weights.
- Tracking error depends on fees, sampling, replication, lending, withholding tax, and execution.

## Core Pricing Framework
The core identity is basket value:

$$
\text{Index Level} \propto \sum_i w_i S_i
$$

For an ETF, premium/discount to NAV is:

$$
\frac{\text{ETF Price} - \text{NAV}}{\text{NAV}}
$$

Creation/redemption mechanisms usually keep liquid ETFs close to NAV, but premiums and discounts can widen when markets are stressed, underlying assets are illiquid, or baskets are hard to trade.

## Worked Instrument Example: ETF Premium To NAV
Assume:
- ETF market price: USD 50.20,
- NAV: USD 50.00.

Premium to NAV is:

$$
\frac{50.20 - 50.00}{50.00} = 0.40\%
$$

The ETF trades 40 bps above NAV. That may be normal for a hard-to-access market or a warning sign if the underlying basket is liquid.

## Key Risk Measures and Sensitivities
- Tracking error versus benchmark.
- Premium/discount to NAV.
- Constituent, sector, country, and factor exposure.
- Rebalance turnover and trading cost.
- Creation/redemption liquidity.
- Corporate-action and index-methodology risk.

## Required Data, Curves, Surfaces, and Calibration Objects
- Index constituent history and weights.
- ETF holdings, creation/redemption baskets, and cash components.
- Corporate actions, float adjustments, and index methodology files.
- Prices, volumes, spreads, and auctions for constituents and ETF.
- Fees, securities lending revenue, withholding tax, and dividend treatment.

## Numerical and Implementation Approaches
- Store index membership as point-in-time data.
- Separate official index levels from reconstructed basket values.
- Rebalance using only information available at the rebalance decision time.
- Model transaction costs and market impact for index changes.
- Reconcile ETF NAV, holdings, and market price.

## Production Pitfalls and Sanity Checks
- Survivorship bias from using current constituents historically.
- Confusing price-return and total-return index series.
- Ignoring cash components in ETF baskets.
- Mis-handling splits, special dividends, or index float changes.
- Backtesting rebalance trades at prices unavailable at decision time.
- Treating ETF liquidity as independent of underlying basket liquidity.

## Illustrative Code
```python
def premium_to_nav(etf_price: float, nav: float) -> float:
    if nav <= 0.0:
        raise ValueError("nav must be positive")
    return (etf_price - nav) / nav
```

## References and Further Reading
- Index provider methodology documents
- ETF prospectuses and creation/redemption basket files
- Grinold and Kahn. *Active Portfolio Management*
