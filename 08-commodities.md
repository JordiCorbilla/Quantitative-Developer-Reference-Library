# Commodity Derivatives

Related chapters: [02-futures.md](02-futures.md), [09-cross-asset.md](09-cross-asset.md), [11-market-data.md](11-market-data.md), and [13-risk-and-pnl.md](13-risk-and-pnl.md).

## What This Domain Covers
Commodity products reference physical goods such as crude oil, natural gas, power, metals, crops, or freight. The economics often depend on delivery month, location, grade, storage, and transport rather than only on a generic spot price. Commodity analytics look familiar if you come from equities or FX, but physical constraints and storage economics change the modeling problem. Inventory, transport, seasonality, and quality differentials can matter as much as volatility.

## Product Taxonomy and Market Structure
- Energy, metals, agricultural, and freight-linked products
- Spot, forwards, and listed futures
- Swing options, storage options, spread options, and transportation optionality
- Physically settled vs cash-settled contracts

## Quoting and Market Conventions
- Contract units and delivery locations are part of the economics.
- Nearby and deferred contracts can embed strong seasonal effects.
- Quality, grade, and location basis matter.
- Storage and transport optionality can dominate simple financial carry relationships.

## Core Pricing Framework
Commodity forward curves are often described through cost of carry:

$$
F_0(T) = S_0 e^{(r + u - y)T}
$$

but convenience yield $y$ is not just a nuisance parameter. It reflects scarcity and inventory value, and can make backwardation economically reasonable. Many real commodity books are better thought of as optimization or inventory problems with embedded optionality.

## Worked Instrument Example: Crude Oil Future
Assume a trader buys 20 crude oil futures contracts at $78 per barrel. Each contract represents 1,000 barrels, so the position references:

$$
20 \times 1{,}000 = 20{,}000
$$

barrels. If the futures price rises to $82, the PnL is:

$$
(82 - 78) \times 20{,}000 = 80{,}000
$$

If the futures price falls to $74, the PnL is:

$$
(74 - 78) \times 20{,}000 = -80{,}000
$$

The same price move can have different meaning across delivery months. A front-month crude contract may react to immediate inventory scarcity, while a deferred contract may react more to long-term supply expectations. That is why commodity systems usually model a delivery curve, not a single spot-like number.

## Key Risk Measures and Sensitivities
- Delta to nearby and deferred curve points
- Calendar-spread and crack/spread risk
- Volatility and correlation exposure for spread options
- Inventory and location basis exposure
- Seasonal risk across delivery months

## Required Data, Curves, Surfaces, and Calibration Objects
- Contract specifications, delivery locations, and quality definitions
- Forward curves by location and grade
- Storage, transport, and inventory assumptions
- Volatility surfaces for options and spread products
- Correlation assumptions for cross-commodity exposures

## Numerical and Implementation Approaches
- Use explicit curve objects by delivery month rather than over-smoothing seasonal structure.
- Model storage and swing optionality with dynamic programming, trees, or Monte Carlo depending on complexity.
- Preserve contract metadata throughout the stack; location and grade are not attributes you can safely strip.

## Production Pitfalls and Sanity Checks
- Treating commodity forwards as if they were equity forwards with a cosmetic convenience-yield term.
- Ignoring location basis in aggregated risk.
- Building continuous futures series that erase seasonal structure.
- Missing operational constraints such as storage capacity or transport lag in valuation of physical optionality.

## Illustrative Code
```python
def simple_carry_forward(spot: float, expiry: float, rate: float, storage_cost: float, convenience_yield: float) -> float:
    import math
    return spot * math.exp((rate + storage_cost - convenience_yield) * expiry)
```

## References and Further Reading
- Eydeland and Wolyniec. *Energy and Power Risk Management*
- Geman. *Commodities and Commodity Derivatives*
- Clewlow and Strickland on energy derivatives modelling
