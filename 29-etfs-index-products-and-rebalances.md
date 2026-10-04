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
Begin with the constituent quantities, then turn the basket value into an index level. For a simple float-adjusted capitalization-weighted price index in one currency:

```math
I_t=\frac{\sum_i Q_{i,t}f_{i,t}S_{i,t}}{D_t},
\qquad
w_{i,t}=\frac{Q_{i,t}f_{i,t}S_{i,t}}
{\sum_j Q_{j,t}f_{j,t}S_{j,t}}.
```

Here $Q_i$ is the index share count, $f_i$ is the float adjustment, and $D_t$ is the index divisor. Prices need FX conversion for a basket spanning currencies. Weights are fractions of market value, rather than share quantities: summing $w_iS_i$ does not generally reconstruct the index. With unchanged holdings and no intervening distributions or corporate actions, the basket's one-period return is $\sum_i w_{i,t-1}r_{i,t}$. Price-weighted, equal-weighted, capped, total-return, and currency-hedged indices each require their own methodology.

The divisor preserves continuity for specified non-market events. Suppose two constituents have adjusted share counts of 10 and 20, prices of 50 and 25, and a divisor of 10. Basket value is 1,000 and the index is 100. A two-for-one split of the first stock changes its shares to 20 and price to 25, preserving the value. A constituent replacement can instead change basket value; the divisor must then be reset to preserve the index level under the provider's rules. Reproduce both cases in [examples/index-divisor-and-weights.md](examples/index-divisor-and-weights.md). The [S&P DJI methodology](https://www.spglobal.com/spdji/en/methodology/article/index-mathematics-methodology/) explains the role of share counts, index families, and divisor adjustments.

For an ETF, premium/discount to NAV is:

```math
\frac{\text{ETF Price} - \text{NAV}}{\text{NAV}}
```

Creation/redemption mechanisms usually keep liquid ETFs close to NAV, but premiums and discounts can widen when markets are stressed, underlying assets are illiquid, or baskets are hard to trade.

NAV here means value **per fund share**, matched to the ETF price's currency and timestamp. An official end-of-day NAV or an indicative intraday estimate can use stale underlying marks, particularly across time zones. A measured premium can reflect that timing difference as well as trading frictions; it is not automatically an executable arbitrage.

## Worked Instrument Example: ETF Premium To NAV
Assume:
- ETF market price: USD 50.20,
- NAV: USD 50.00.

Premium to NAV is:

```math
\frac{50.20 - 50.00}{50.00} = 0.40\%
```

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
- S&P Dow Jones Indices. [Index Mathematics Methodology](https://www.spglobal.com/spdji/en/methodology/article/index-mathematics-methodology/).
- ETF prospectuses and creation/redemption basket files
- Grinold and Kahn. *Active Portfolio Management*
