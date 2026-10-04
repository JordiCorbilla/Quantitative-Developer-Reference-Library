# Regulatory Margin and Capital Analytics

Related chapters: [09-cross-asset.md](09-cross-asset.md), [13-risk-and-pnl.md](13-risk-and-pnl.md), [14-testing-and-validation.md](14-testing-and-validation.md), [19-financing-repo-and-securities-lending.md](19-financing-repo-and-securities-lending.md), and [22-model-governance-and-ipv.md](22-model-governance-and-ipv.md).

## What This Domain Covers
Margin and capital are the institutional cost of risk.

A trade does not only consume market risk limits. It can require collateral, initial margin, regulatory capital, liquidity add-ons, and explain reports. Those requirements depend on legal terms, netting sets, eligible collateral, product class, sensitivities, model rules, and reporting date.

This chapter treats margin and capital as controlled calculations. The problem is not just computing a number; it is proving why the number changed.

## Product Taxonomy and Market Structure
The first split is between collateral exchanged today, margin held against future exposure, and capital held against regulatory risk.

- Variation margin and initial margin.
- ISDA SIMM and schedule-based margin.
- CCP margin models.
- FRTB market-risk capital and standardized approaches.
- Stress capital, liquidity add-ons, concentration add-ons, and margin explain.
- XVA-adjacent capital and funding analytics.

## Quoting and Market Conventions
- Margin is not quoted like a price, but the calculation has a strict convention contract.
- Netting set, CSA, product class, risk bucket, and legal entity determine aggregation.
- Sensitivities must use the prescribed risk-factor definitions and units.
- Liquidity horizons and risk weights are rule-driven, not desk preferences.
- Model approvals and regulatory versions are part of the calculation input.

## Core Pricing Framework
Most margin and capital models are rule engines wrapped around risk analytics.

Many margin and capital models reduce to:

```math
\text{requirement} = f(\text{trades}, \text{sensitivities}, \text{risk weights}, \text{correlations}, \text{netting rules}, \text{add-ons})
```

The hard part is reproducibility. Two runs should differ only because an input, rule version, or market state changed.

### Visual Margin Reference

![Regulatory margin and capital stack](assets/regulatory-margin-stack.svg)

Margin analytics sit on top of legal data, market risk, collateral terms, model rules, stress assumptions, and governance controls.

## Worked Instrument Example: Simple Initial Margin Add-On
Assume:
- SIMM-style dollar sensitivity input, $s_k$: USD 2m,
- prescribed risk weight, $RW_k$: 15%,
- concentration factor, $CR_k$: 1.0.

A simplified weighted sensitivity is:

```math
WS_k=RW_k\,s_k\,CR_k=15\%\times\text{USD }2m\times1.0=\text{USD }300k.
```

Here USD 2m is already the dollar-equivalent sensitivity defined by the applicable methodology; it is not "USD 2m per 1% move" multiplied by a 15-percentage-point scenario. Real models first build prescribed sensitivities and then aggregate weighted sensitivities across buckets, correlations, product classes, tenors, netting sets, and add-ons. This example is only the unit intuition, and the current methodology version remains authoritative.

## Key Risk Measures and Sensitivities
- Initial margin and variation margin.
- Margin VaR, stress loss, and liquidity horizon contribution.
- Sensitivity by regulatory bucket.
- Netting benefit and concentration add-on.
- Margin explain from trade changes, market moves, and model/rule changes.
- Capital consumption and return on capital.

## Required Data, Curves, Surfaces, and Calibration Objects
- Trade population and legal entity mappings.
- CSA, netting set, collateral eligibility, and margin terms.
- Sensitivities by prescribed risk factor.
- Regulatory rule version, bucket definitions, risk weights, and correlations.
- Market data snapshots and stress scenarios.
- Prior run results for explain.

## Numerical and Implementation Approaches
- Treat rule version as an immutable input.
- Build deterministic aggregation with transparent intermediate outputs.
- Store trade-to-netting-set mappings and sensitivity lineage.
- Separate market moves, new trades, lifecycle events, and rule changes in margin explain.
- Reconcile margin inputs to official risk and finance systems.

## Production Pitfalls and Sanity Checks
- Aggregating trades under the wrong netting set or legal entity.
- Unit mismatches in sensitivities submitted to a prescribed model.
- Reporting total margin without explaining drivers.
- Allowing rule updates to restate old reports without versioning.
- Ignoring collateral eligibility and concentration limits.

## Illustrative Code
```python
def weighted_sensitivity(sensitivity: float, risk_weight: float) -> float:
    return sensitivity * risk_weight
```

## References and Further Reading
- [ISDA SIMM methodology and governance](https://www.isda.org/category/margin/isda-simm/).
- Basel Committee FRTB documentation.
- CCP margin methodology documents.
