# Pricing Architecture

Related chapters: [10-numerical-methods.md](10-numerical-methods.md), [11-market-data.md](11-market-data.md), [13-risk-and-pnl.md](13-risk-and-pnl.md), and [15-performance-and-production.md](15-performance-and-production.md).

## What This Domain Covers
Pricing architecture is the translation layer between financial models and maintainable systems. Most analytics platforms fail not because the formulas are unknown, but because product representation, market-state access, model dependency management, and risk workflows are tangled together.

## Product Taxonomy and Market Structure
- Trade capture and trade normalization
- Static data and schedule generation
- Market-state representation
- Pricing engines and model adapters
- Risk engines, scenario engines, and batch workflows
- Result stores, audit trails, and explain tooling

## Quoting and Market Conventions
- Trades should preserve quote conventions required to reconstruct valuation.
- Premium currency, settlement rules, calendars, exercise style, and fixing conventions belong in the trade model.
- Market-state objects should expose normalized views, but lineage back to raw quote context must remain available.

## Core Pricing Framework
A clean pricing stack usually separates:
- instrument definition,
- resolved trade with schedules and conventions,
- market state,
- model parameters,
- pricing engine,
- result object with risk and diagnostics.

Useful design rules:
- pure valuation functions where possible,
- explicit dependency injection for market data and numerical policies,
- immutable market snapshots,
- diagnostics returned with price, not hidden in logs.

The architecture should support multiple engines per product: for example, Black closed form for benchmarking, PDE for American features, and Monte Carlo for exotic or exposure calculations.

## Key Risk Measures and Sensitivities
- Trade-level and portfolio-level price/risk outputs
- Sensitivity lineage: what was bumped, shocked, or re-calibrated
- Runtime, convergence, and fallback diagnostics
- Dependency visibility: which curves, surfaces, fixings, and models were used

## Required Data, Curves, Surfaces, and Calibration Objects
- Canonical trade schemas
- Product-specific resolvers for schedules and conventions
- Immutable market snapshot or context object
- Model configuration and calibration objects
- Result schema that can carry price, risk, diagnostics, and provenance together

## Numerical and Implementation Approaches
- Use interface boundaries that reflect domain objects, not utility convenience.
- Keep pricing engines stateless with respect to the trade and market snapshot they receive.
- Pre-resolve expensive schedule logic where that improves throughput without hiding conventions.
- Provide a benchmark engine for every major product family.
- Treat calibration as a dependency-producing stage, not as something every pricing call silently performs.

## Production Pitfalls and Sanity Checks
- Trade models that lose essential market conventions during normalization.
- Market snapshots passed around as mutable dictionaries.
- Pricing engines that fetch data globally, making replay and testing impossible.
- Risk results reported without enough provenance to explain discrepancies.
- Recalibration hidden inside risk bumps, producing non-local and irreproducible sensitivities.

## Illustrative Code
```python
from dataclasses import dataclass


@dataclass(frozen=True)
class PricingRequest:
    trade: object
    market: object
    model: object


@dataclass(frozen=True)
class PricingResult:
    price: float
    diagnostics: dict


class PricingEngine:
    def price(self, request: PricingRequest) -> PricingResult:
        raise NotImplementedError
```

## References and Further Reading
- Joshi. *C++ Design Patterns and Derivatives Pricing*
- Large-scale risk-system architecture talks and engineering writeups
- Internal model-governance and audit requirements for your environment
