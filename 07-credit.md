# Credit Instruments

Related chapters: [05-fixed-income.md](05-fixed-income.md), [09-cross-asset.md](09-cross-asset.md), [11-market-data.md](11-market-data.md), and [13-risk-and-pnl.md](13-risk-and-pnl.md).

## What This Domain Covers
Credit products combine fixed-income cashflow mechanics with default timing and recovery assumptions. The asset class is implementation-heavy because the same issuer can trade through bonds, CDS, indices, and structured credit products with different conventions.

## Product Taxonomy and Market Structure
- Single-name CDS
- CDS indices and tranches
- Corporate and sovereign credit bonds
- Loan and leveraged-credit exposures
- First-to-default and basket-style structures

## Quoting and Market Conventions
- CDS can quote as running spread, upfront plus running coupon, or index points.
- Recovery assumptions are explicit model inputs.
- Standard coupons and IMM-like roll dates matter operationally.
- Bond spread measures are not interchangeable with CDS spread.

## Core Pricing Framework
Reduced-form credit models use hazard rates or survival probabilities:

$$
Q(0, T) = \exp\left(-\int_0^T \lambda(u) du\right)
$$

CDS pricing balances premium leg and protection leg under a recovery assumption. Bond pricing adds default-adjusted expected cashflows and, often, liquidity premia not captured by a simple hazard-rate model.

## Key Risk Measures and Sensitivities
- CS01 by name and bucket
- Jump-to-default exposure
- Recovery sensitivity
- Index tranche correlation and base-correlation exposures
- Basis risk between bond and CDS positions

## Required Data, Curves, Surfaces, and Calibration Objects
- CDS quotes, standard coupons, accrual conventions, and roll dates
- Bond prices and spread measures
- Recovery assumptions and possibly stochastic-recovery model parameters
- Credit curves by issuer and seniority
- Correlation surfaces for tranche analytics where relevant

## Numerical and Implementation Approaches
- Bootstrap hazard curves from liquid CDS points.
- Align bond analytics with fixed-income schedule generation and accrued-interest logic.
- Keep default event handling explicit in trade representation and scenario engines.
- Use scenario tools for wrong-way risk and spread gap moves even when the pricing model is simple.

## Production Pitfalls and Sanity Checks
- Survival probabilities outside $[0, 1]$ due to bad interpolation.
- Mixing spread measures across bonds and CDS without a documented mapping.
- Missing accrued premium logic in CDS settlement.
- Recoveries hard-coded globally when books actually use name- or sector-specific assumptions.

## Illustrative Code
```python
import math


def survival_probability(hazard_rate: float, expiry: float) -> float:
    return math.exp(-hazard_rate * expiry)


def expected_loss(notional: float, default_probability: float, recovery: float) -> float:
    return notional * default_probability * (1.0 - recovery)
```

## References and Further Reading
- O'Kane. *Modelling Single-name and Multi-name Credit Derivatives*
- Duffie and Singleton. *Credit Risk*
- ISDA CDS standard model documentation
