# Quantitative Developer Reference Library Overview

This repo is a practitioner-oriented reference for building, validating, and operating quantitative analytics. It is written for quant developers first: people who need to understand the math well enough to implement it correctly, connect it to market data, and defend the result in production.

## Purpose
- Provide a durable map of core products, pricing ideas, risk measures, and implementation patterns.
- Capture desk conventions and sanity checks that are easy to miss in pure theory notes.
- Keep the structure stable enough that the library can grow chapter by chapter without becoming inconsistent.

## Audience
- Quant developers building pricing, risk, market data, and PnL systems
- Engineering-minded front-office quants
- Practitioners preparing for interviews, design discussions, or production debugging

## How To Read The Library
- Start here once for notation, discounting language, and glossary.
- Use individual chapters as independent references after that.
- Read [01-options.md](01-options.md), [05-fixed-income.md](05-fixed-income.md), [06-interest-rates.md](06-interest-rates.md), and [10-numerical-methods.md](10-numerical-methods.md) together if you want the deepest first pass through implementation-heavy material.
- Read [11-market-data.md](11-market-data.md), [12-pricing-architecture.md](12-pricing-architecture.md), [13-risk-and-pnl.md](13-risk-and-pnl.md), and [14-testing-and-validation.md](14-testing-and-validation.md) as the engineering layer around the analytics.

## Library Map

| File | Focus | Why It Matters |
| --- | --- | --- |
| [01-options.md](01-options.md) | Vanilla and exotic options, Greeks, volatility surfaces | The most common entry point for pricing and hedging logic |
| [02-futures.md](02-futures.md) | Futures, forwards, basis, carry, and rolling | Core mechanics for listed and OTC linear products |
| [03-equities.md](03-equities.md) | Cash equities, financing, factor intuition, execution | Links pricing theory to real trading and portfolio systems |
| [04-fx.md](04-fx.md) | Spot, forwards, swaps, and FX option conventions | Essential for multi-currency systems and collateral logic |
| [05-fixed-income.md](05-fixed-income.md) | Bonds, cashflows, yields, duration, spread measures | The foundation for rates and credit analytics |
| [06-interest-rates.md](06-interest-rates.md) | Swaps, FRAs, caps/floors, swaptions, curve building | Multi-curve pricing is a quant dev core skill |
| [07-credit.md](07-credit.md) | CDS, credit curves, indices, tranche framing | Connects hazard-rate modelling to tradable products |
| [08-commodities.md](08-commodities.md) | Storage, convenience yield, seasonality, optionality | Highlights where spot-carry intuition breaks |
| [09-cross-asset.md](09-cross-asset.md) | Correlation, collateral, funding, xVA, hybrids | Shows what changes once desks and curves interact |
| [10-numerical-methods.md](10-numerical-methods.md) | Trees, PDE, Monte Carlo, interpolation, calibration | The implementation toolkit behind every product chapter |
| [11-market-data.md](11-market-data.md) | Symbology, cleaning, timeseries, curves, surfaces | Analytics fail when market state is wrong |
| [12-pricing-architecture.md](12-pricing-architecture.md) | Trade models, engines, dependencies, APIs | Turns formulas into maintainable systems |
| [13-risk-and-pnl.md](13-risk-and-pnl.md) | Greeks, scenarios, explain, controls | Bridges pricing output to daily desk workflows |
| [14-testing-and-validation.md](14-testing-and-validation.md) | Unit tests, numerical controls, model validation | Prevents silent regressions and false confidence |
| [15-performance-and-production.md](15-performance-and-production.md) | Latency, scaling, observability, resilience | Production quality is part of quantitative correctness |

## Shared Quantitative Conventions

### Risk-Neutral Pricing
Unless a chapter says otherwise, present values are written under a pricing measure with discounting separated from payoff generation:

$$
V(t) = \mathbb{E}^{\mathbb{Q}}\left[D(t, T) \cdot X_T \mid \mathcal{F}_t\right]
$$

where:
- $X_T$ is the terminal payoff or cashflow stream
- $D(t, T)$ is the discount factor implied by the collateral / discounting convention in force
- the chosen measure depends on the numeraire and is often implementation-specific

This matters because production systems should not hard-code "risk-free rate" into every formula. The correct discount curve depends on collateral, CSA terms, currency, and sometimes product type.

### Time
- Time to maturity is written as $\tau = T - t$ when the model uses continuous time.
- In code, never assume time is measured in calendar years by simple day count division unless the product convention actually does that.
- Day count convention, holiday calendar, business-day adjustment, and schedule generation are first-class data inputs, not formatting details.

### Curves
- Discount curve: maps dates to discount factors used for present valuing collateralized cashflows.
- Forward curve: maps dates or accrual periods to implied forward rates or forward prices.
- Credit curve: maps dates to hazard rates, survival probabilities, or quoted spreads.
- Dividend or borrow curve: maps dates to financing or carry assumptions for equities.
- Inflation curve, repo curve, commodity convenience-yield curve, and basis curves are all domain-specific variations of the same dependency pattern.

### Surfaces And Cubes
- Volatility surface: usually strike-maturity, delta-tenor, or moneyness-tenor.
- Vol cube: surface plus another axis such as swap tenor for swaptions.
- Correlation surface / skew / term structure: used when a single scalar correlation is too weak to explain observed prices.

### Measures, Numeraires, And Model State
- Choose state variables that match the product: spot, forward, short rate, Libor rate, hazard rate, variance process, inventory level, or factor vector.
- Choose a measure that simplifies simulation or valuation: money-market, terminal, forward, annuity, or stock numeraire are common examples.
- In architecture, separate immutable market observations from derived state such as interpolated nodes, calibrated parameters, and cached Jacobians.

## Notation

| Symbol | Meaning |
| --- | --- |
| $S_t$ | Spot price at time $t$ |
| $F(t, T)$ | Forward price or forward rate for settlement at $T$ |
| $K$ | Strike, fixed rate, or quoted contract level |
| $r$ | Continuously compounded rate when a single-rate simplification is used |
| $q$ | Dividend yield or carry yield in equity-style models |
| $\sigma$ | Volatility parameter or implied volatility quote |
| $P(t, T)$ | Discount factor from $t$ to $T$ |
| $L(T_i, T_{i+1})$ | Forward Libor / Ibor style rate over an accrual period |
| $N(x)$ | Standard normal CDF |
| $n(x)$ | Standard normal PDF |
| $\Delta, \Gamma, \nu, \Theta, \rho$ | First-line option Greeks: delta, gamma, vega, theta, rho |
| PV01 / DV01 | Present-value change for a one basis point rate move |

## Unit And Quote Discipline
- Rates can be quoted in percent while engines expect decimals. Make conversion explicit.
- Volatility is commonly quoted in percent, variance is dimensionless per unit time, and time scaling matters.
- A basis point is $10^{-4}$ in absolute rate units.
- Clean price and dirty price are different objects.
- Premium currency, reporting currency, and collateral currency may differ.
- Delta conventions are not universal across asset classes. Equity delta and FX delta are not interchangeable concepts.

## Cross-Chapter Glossary

| Term | Working Definition |
| --- | --- |
| Carry | Expected PnL from holding a position assuming unchanged market levels under a chosen roll convention |
| Roll-down | PnL from moving along a curve or surface as time passes |
| Basis | Difference between related quoted instruments that should not be forced into a single scalar spread |
| Calibration | Choosing model parameters to fit observable market prices or vol quotes |
| Explain | Decomposing realized or hypothetical PnL into risk-factor contributions |
| No-arbitrage | A set of constraints that prevent obviously inconsistent prices, such as negative densities or broken parity relationships |
| Sticky strike / sticky delta | Rules for how implied vol is assumed to move when spot moves, used for risk calculations and surface shocks |

## Common Sanity Checks
- Prices should satisfy trivial bounds before they hit a pricing engine.
- Parity identities should hold within tolerance when products are related by replication.
- Discount factors should be monotone non-increasing in maturity under standard assumptions.
- Survival probabilities should stay in $[0, 1]$ and decrease with time.
- Calendar, day count, and schedule changes should be explainable from conventions, not from hidden defaults.
- Bump sizes must be stable enough to avoid noise but small enough to approximate the intended derivative.

## Chapter Contract
Every chapter in this repo follows the same top-level structure:
1. What This Domain Covers
2. Product Taxonomy and Market Structure
3. Quoting and Market Conventions
4. Core Pricing Framework
5. Key Risk Measures and Sensitivities
6. Required Data, Curves, Surfaces, and Calibration Objects
7. Numerical and Implementation Approaches
8. Production Pitfalls and Sanity Checks
9. Illustrative Code
10. References and Further Reading

## Recommended Reading Paths
- Build the core stack: [01-options.md](01-options.md) -> [10-numerical-methods.md](10-numerical-methods.md) -> [12-pricing-architecture.md](12-pricing-architecture.md)
- Build rates competency: [05-fixed-income.md](05-fixed-income.md) -> [06-interest-rates.md](06-interest-rates.md) -> [11-market-data.md](11-market-data.md)
- Build production judgment: [13-risk-and-pnl.md](13-risk-and-pnl.md) -> [14-testing-and-validation.md](14-testing-and-validation.md) -> [15-performance-and-production.md](15-performance-and-production.md)
