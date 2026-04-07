# Futures and Forwards

Related chapters: [04-fx.md](04-fx.md), [05-fixed-income.md](05-fixed-income.md), [08-commodities.md](08-commodities.md), and [11-market-data.md](11-market-data.md).

## What This Domain Covers
Futures and forwards are linear contracts, but the implementation details are not trivial. Contract specification, settlement mechanics, carry inputs, and rolling behavior all affect pricing, hedging, and PnL explain.

## Product Taxonomy and Market Structure
- OTC forwards: customized notional, maturity, settlement, and collateral terms.
- Exchange-traded futures: standardized contract size, expiry cycle, margining, and daily variation settlement.
- Equity index futures, commodity futures, bond futures, short-rate futures, and FX futures all share linear payoffs but differ materially in carry and delivery logic.
- Physically delivered contracts require deliverable-grade logic, while cash-settled contracts rely on an index or fixing methodology.

## Quoting and Market Conventions
- Forwards are quoted as outright forward price or forward points over spot.
- Futures are quoted in contract units defined by the exchange; understanding the point value is mandatory for risk and PnL.
- Bond futures require conversion factors, cheapest-to-deliver logic, and delivery-option awareness.
- Short-rate futures may quote as price = 100 - rate, which flips intuition for price vs rate moves.
- Rolling a futures position changes contract, liquidity point, and often the relevant carry assumptions.

## Core Pricing Framework
In a simple carry model:

$$
F_0(T) = S_0 e^{(r + u - y)T}
$$

where $u$ is storage or financing cost and $y$ is income or convenience yield. Variants:
- equity index forward: carry comes from funding minus dividends,
- FX forward: carry comes from domestic minus foreign rates,
- commodity forward: storage and convenience yield dominate,
- futures on margined exchanges may differ from forwards due to daily settlement and convexity effects.

For fixed-income futures, the core pricing object is often the implied repo or cheapest-to-deliver package rather than a clean carry formula.

## Key Risk Measures and Sensitivities
- Delta to spot or relevant cash instrument.
- Carry and roll-down exposure over the holding horizon.
- Basis risk between futures and the hedged physical or OTC position.
- Curve risk for rate and bond futures.
- Calendar-spread risk between nearby and deferred contracts.

## Required Data, Curves, Surfaces, and Calibration Objects
- Contract specifications: multiplier, tick size, expiry, first notice date, last trade date, settlement method.
- Spot price or reference cash market.
- Financing, dividend, repo, storage, or convenience-yield assumptions depending on asset class.
- Deliverable basket metadata and conversion factors for bond futures.
- Roll calendars and liquidity rules for analytics that use continuous futures series.

## Numerical and Implementation Approaches
- Use direct pricing formulas for simple forwards.
- Treat listed futures as explicit instruments in market data, not just derived forwards.
- Build continuous-series analytics carefully; back-adjusted, ratio-adjusted, and panama-style stitching solve different problems.
- For bond futures, compute invoice price, net basis, and cheapest-to-deliver explicitly.

## Production Pitfalls and Sanity Checks
- Mixing futures and forwards as if daily margining never matters.
- Ignoring contract multipliers in PnL and risk aggregation.
- Incorrect handling of roll dates, especially when a strategy trades front-month liquidity but risk is reported on a continuous series.
- Using spot carry formulas for commodity contracts where storage constraints are binding.
- Failing to distinguish trade date, first notice date, and last trade date.

## Illustrative Code
```python
import math


def fair_forward_price(spot: float, expiry: float, funding_rate: float, income_yield: float = 0.0, storage_cost: float = 0.0) -> float:
    carry = funding_rate + storage_cost - income_yield
    return spot * math.exp(carry * expiry)


def futures_pnl(entry_price: float, current_price: float, multiplier: float, contracts: int) -> float:
    return (current_price - entry_price) * multiplier * contracts
```

## References and Further Reading
- Hull, J. *Options, Futures, and Other Derivatives*
- Chance and Brooks. *Introduction to Derivatives and Risk Management*
- Exchange rulebooks for product-specific contract definitions
