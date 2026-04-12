# Quantitative Developer Reference Library

Practical reference material for quant developers, engineering-minded quants, and anyone building pricing, risk, and market data systems. The goal is not to be a textbook. The goal is to compress the parts that matter in production: market conventions, pricing intuition, implementation shape, validation checks, and failure modes.

Start with [00-overview.md](00-overview.md). It defines the shared notation, discounting language, curve and surface glossary, and the overall map of the library.

## Library Map

### Core Instruments
- [00-overview.md](00-overview.md) - entrypoint, conventions, glossary, and reading guide
- [01-options.md](01-options.md) - options pricing, volatility, Greeks, and hedging
- [02-futures.md](02-futures.md) - futures, forwards, basis, carry, and contract mechanics
- [03-equities.md](03-equities.md) - cash equities, financing, execution, and factor intuition
- [04-fx.md](04-fx.md) - spot, forwards, swaps, and FX options conventions
- [05-fixed-income.md](05-fixed-income.md) - bonds, yields, duration, spreads, and curve inputs
- [06-interest-rates.md](06-interest-rates.md) - swaps, FRAs, futures, caps/floors, and multi-curve pricing
- [07-credit.md](07-credit.md) - CDS, bond-credit linkage, indices, and tranche concepts
- [08-commodities.md](08-commodities.md) - forwards, storage, convenience yield, and seasonal structure
- [09-cross-asset.md](09-cross-asset.md) - correlation, funding, collateral, and xVA framing
- [10-numerical-methods.md](10-numerical-methods.md) - Monte Carlo, PDE, trees, interpolation, and calibration

### Quant Engineering
- [11-market-data.md](11-market-data.md) - identifiers, symbology, time series, curves, surfaces, and data quality
- [12-pricing-architecture.md](12-pricing-architecture.md) - trade models, market state, pricing engines, and library design
- [13-risk-and-pnl.md](13-risk-and-pnl.md) - sensitivities, explain, scenario risk, and control frameworks
- [14-testing-and-validation.md](14-testing-and-validation.md) - numerical tests, model validation, and release discipline
- [15-performance-and-production.md](15-performance-and-production.md) - latency, throughput, observability, and operational resilience
- [16-portfolio-construction-and-backtesting.md](16-portfolio-construction-and-backtesting.md) - factor models, optimizers, turnover, costs, and benchmark-relative workflows

## How To Use This Repo
- Read the overview once, then use chapters as standalone references.
- Treat each chapter as a practitioner checklist: what gets quoted, what gets built, what breaks.
- Follow the cross-links. Options, fixed income, rates, numerical methods, and pricing architecture are intentionally tightly connected.
- Use the code snippets as sanity-check scaffolding, not as production-ready libraries.

## Design Principles
- Markdown-first, no docs toolchain required.
- Broad coverage first, then depth in the most implementation-dense areas.
- Theory only where it helps build or validate systems.
- Conventions and edge cases matter as much as formulas.
- The repo should keep growing without changing its basic structure.

## Contribution Direction
- Preserve the chapter template so readers always know where to find pricing, risk, data, and implementation guidance.
- Prefer short, precise examples over long tutorials.
- Add links between related chapters whenever a concept depends on another domain.
- Keep notation consistent with [00-overview.md](00-overview.md).
