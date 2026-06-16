# Volatility Products

Related chapters: [01-options.md](01-options.md), [09-cross-asset.md](09-cross-asset.md), [10-numerical-methods.md](10-numerical-methods.md), [11-market-data.md](11-market-data.md), and [13-risk-and-pnl.md](13-risk-and-pnl.md).

## What This Domain Covers
Volatility products trade realized variance, implied variance, volatility indices, forward volatility, skew, and correlation. They sit between option-surface analytics and portfolio risk because their value depends on the whole distribution, not only spot direction.

## Product Taxonomy and Market Structure
- Variance swaps and volatility swaps.
- VIX futures, VIX options, and volatility-index linked notes.
- Forward-starting variance and options.
- Dispersion trades between index volatility and constituent volatility.
- Corridor variance, gamma swaps, and other realized-volatility payoffs.

## Quoting and Market Conventions
- Variance is volatility squared; quoting in volatility points while settling variance creates unit risk.
- Variance swaps are usually quoted by variance strike or volatility strike, but the payoff is on realized variance.
- VIX products reference a specific index methodology, not generic implied volatility.
- Dispersion trades embed index-constituent correlation exposure.
- Realized variance definitions depend on sampling frequency, close source, holidays, and corporate-action handling.

## Core Pricing Framework
A simplified variance swap payoff is:

$$
N_{\text{var}}(\sigma_{\text{realized}}^2 - K_{\text{var}})
$$

The fair variance strike can be related to a strip of options across strikes under idealized assumptions. In production, the practical problem is building an arbitrage-aware surface and applying the correct index methodology.

### Visual Volatility Reference

![Volatility products map](assets/volatility-products-map.svg)

Volatility products depend on the option surface, but each product extracts a different exposure: realized variance, forward variance, index methodology, or correlation.

## Worked Instrument Example: Variance Swap
Assume:
- variance notional: USD 50,000 per variance point,
- realized volatility: 24%,
- strike volatility: 20%.

The payoff uses squared volatility:

$$
50{,}000 \times (24^2 - 20^2) = 8{,}800{,}000
$$

This example uses volatility points, a common market shorthand. A production implementation must be explicit about whether volatility is represented as percent points or decimals.

## Key Risk Measures and Sensitivities
- Vega and variance vega.
- Gamma and realized-volatility exposure.
- Skew and smile sensitivity.
- Vol-of-vol and convexity.
- Correlation exposure for dispersion.
- Forward variance and roll-down exposure.

## Required Data, Curves, Surfaces, and Calibration Objects
- Option chains across strikes and maturities.
- Interest-rate, dividend, borrow, and forward inputs.
- Volatility index methodology inputs.
- Realized return series with sampling and corporate-action policies.
- Constituent weights and correlation data for dispersion.
- Surface calibration and no-arbitrage controls.

## Numerical and Implementation Approaches
- Keep variance, volatility, and volatility points as distinct units in code.
- Use robust interpolation and extrapolation controls for option surfaces.
- Validate option-strip replication against listed variance or volatility quotes where available.
- For VIX-style products, implement the official index methodology as a separate tested component.

## Production Pitfalls and Sanity Checks
- Squaring decimal volatility in one module and percent volatility in another.
- Treating VIX futures as spot VIX.
- Ignoring jump and close-to-close sampling effects in realized variance.
- Reporting dispersion risk without exposing correlation sensitivity.
- Calibrating a smooth surface that violates static no-arbitrage constraints.

## Illustrative Code
```python
def variance_swap_payoff(var_notional: float, realized_vol_points: float, strike_vol_points: float) -> float:
    return var_notional * (realized_vol_points ** 2 - strike_vol_points ** 2)
```

## References and Further Reading
- Gatheral. *The Volatility Surface*
- Demeterfi, Derman, Kamal, and Zou on variance swaps.
- Exchange methodology documents for volatility indices.
