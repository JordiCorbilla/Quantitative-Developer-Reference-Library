# Cross-Asset and XVA Framing

Related chapters: [04-fx.md](04-fx.md), [06-interest-rates.md](06-interest-rates.md), [07-credit.md](07-credit.md), [12-pricing-architecture.md](12-pricing-architecture.md), and [13-risk-and-pnl.md](13-risk-and-pnl.md).

## What This Domain Covers
Cross-asset work starts when a trade depends on more than one market stack or when pricing cannot ignore funding, collateral, counterparty, or correlation structure. The challenge is often architectural before it is mathematical.

## Product Taxonomy and Market Structure
- Quanto and hybrid options
- Cross-currency products
- Structured products with equity-rate, FX-rate, or credit-rate interaction
- xVA adjustments layered onto OTC derivatives portfolios
- Multi-asset portfolios requiring joint scenario and stress frameworks

## Quoting and Market Conventions
- Funding, collateral, and reporting currencies can differ.
- Correlation is rarely a single stable scalar across maturities and regimes.
- xVA desks often consume sensitivities and exposure profiles generated elsewhere rather than raw trade prices.
- Netting set, CSA terms, and counterparty hierarchy affect practical valuation adjustments.

## Core Pricing Framework
The cross-asset layer typically combines:
- a base trade valuation under the relevant product model,
- exposure modeling through time,
- discounting and collateral assumptions,
- counterparty and funding adjustments.

Representative adjustments:
- CVA: expected discounted loss from counterparty default.
- DVA: own-default adjustment.
- FVA / ColVA / MVA: funding, collateral, and initial-margin related adjustments.

Joint dynamics matter when payoff or exposure depends on multiple risk factors. Correlation and wrong-way risk cannot be bolted on casually after the fact.

## Key Risk Measures and Sensitivities
- Correlation delta or scenario-based dependence risk
- Funding and collateral sensitivities
- Counterparty spread or hazard risk
- Cross-gammas across asset classes
- Exposure profile shifts under market scenarios

## Required Data, Curves, Surfaces, and Calibration Objects
- Underlying curves, surfaces, and fixings from all participating asset classes
- Counterparty credit data and recovery assumptions
- CSA terms, netting-set mappings, thresholds, and margin rules
- Correlation inputs or joint-factor model parameters
- Exposure simulation configuration and scenario definitions

## Numerical and Implementation Approaches
- Decompose clean price engines from valuation-adjustment layers.
- Use simulation frameworks that can generate pathwise exposures across asset classes and counterparties.
- Keep trade-level dependencies explicit so missing market factors fail loudly.
- Prefer scenario frameworks over false precision when correlation or funding models are weakly identified.

## Production Pitfalls and Sanity Checks
- Treating xVA as a scalar add-on independent of netting and collateral.
- Mixing clean and all-in valuations in the same report.
- Ignoring wrong-way risk where exposure and counterparty health are clearly linked.
- Double-counting curve shocks across asset silos in enterprise scenarios.

## Illustrative Code
```python
def cva(exposures, default_probabilities, loss_given_default, discount_factors):
    return sum(e * dp * lgd * df for e, dp, lgd, df in zip(exposures, default_probabilities, loss_given_default, discount_factors))
```

## References and Further Reading
- Gregory. *The xVA Challenge*
- Green. *XVA*
- Brigo, Morini, and Pallavicini. *Counterparty Credit Risk*
