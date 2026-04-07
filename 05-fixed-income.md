# Fixed Income

Related chapters: [06-interest-rates.md](06-interest-rates.md), [07-credit.md](07-credit.md), [10-numerical-methods.md](10-numerical-methods.md), and [11-market-data.md](11-market-data.md).

## What This Domain Covers
Fixed-income analytics begin with cashflows, calendars, and discounting. They scale into curve construction, spread analysis, callable structures, and credit decomposition. Quant developers need to understand both the instrument math and the mechanics that make bond systems hard to reproduce exactly.

## Product Taxonomy and Market Structure
- Treasury and sovereign bonds
- Corporate bonds and credit-sensitive cash instruments
- Bills, notes, and zero-coupon instruments
- Floating-rate notes
- Inflation-linked bonds
- Callable, puttable, sinkable, and amortizing structures
- Repos and securities financing, which often determine practical funding assumptions

## Quoting and Market Conventions
- Clean price excludes accrued interest; dirty price includes it.
- Settlement date may differ from trade date and is calendar-dependent.
- Day count conventions vary across issuers and coupon types.
- Yield-to-maturity is a convenience summary, not a state variable suitable for all risk or relative-value analysis.
- Government, swap, z-spread, OAS, and asset-swap spread each answer different questions.

Core identities:

$$
\text{Dirty Price} = \text{Clean Price} + \text{Accrued Interest}
$$

$$
\text{PV} = \sum_i CF_i \cdot P(0, t_i)
$$

Yields compress the entire curve into one scalar and should be treated with caution. When a system uses both yield-based and discount-factor-based analytics, the mapping rules must be explicit.

## Core Pricing Framework

### Cashflow Discounting
The most robust fixed-income implementation values a bond by generated cashflows and discount factors:

$$
\text{PV} = \sum_{i=1}^{n} CF_i \cdot P(0, t_i)
$$

For a plain fixed coupon bond, the $CF_i$ are deterministic given the schedule. For floaters, coupon projection depends on forward rates and fixing logic. For callable bonds, valuation becomes an embedded-option problem linked to [06-interest-rates.md](06-interest-rates.md) and [10-numerical-methods.md](10-numerical-methods.md).

### Yield, Duration, And Convexity
Yield-to-maturity solves:

$$
\text{Dirty Price} = \sum_{i=1}^{n} \frac{CF_i}{(1 + y / m)^{m t_i}}
$$

under a chosen compounding frequency $m$. This is useful for quoting and rough comparison, but:
- two bonds with the same yield can have different cashflow risk,
- yield changes do not cleanly aggregate across instruments,
- spread products require separation of rate and credit effects.

Duration and convexity are better first-order and second-order summaries:

$$
\Delta P \approx -D_{\text{mod}} P \Delta y + \frac{1}{2} C P (\Delta y)^2
$$

### Spread Measures
- Z-spread: constant spread added to the discount curve to fit price.
- OAS: option-adjusted spread after accounting for embedded optionality.
- Asset-swap spread: ties bond pricing to swap-market funding conventions.
- I-spread / G-spread: spread over swap or government benchmark curves.

A good implementation stores which spread measure is being reported. "Spread" without qualifier is not a stable interface.

## Key Risk Measures and Sensitivities
- DV01 / PVBP: price sensitivity to a one-basis-point shift.
- Key-rate duration: sensitivity to localized curve moves.
- Convexity: second-order rate sensitivity.
- Carry and roll-down under a chosen horizon convention.
- Spread DV01 for credit-sensitive bonds.
- Optionality risk for callable and puttable structures.

## Required Data, Curves, Surfaces, and Calibration Objects
- Bond static data: coupon, schedule rules, maturity, call schedule, day count, holiday calendar, settlement lag.
- Discount curve and benchmark curves.
- Fixings or forward curves for floaters.
- Credit spread inputs where bonds are not treated as pure rates products.
- Inflation curves or index lags for linkers.
- Deliverable and financing metadata when bonds interact with futures or repo analytics.

## Numerical and Implementation Approaches
- Generate schedules explicitly and deterministically; schedule generation bugs create most reconciliation failures.
- Use discount-factor valuation as the canonical engine, with yield analytics layered on top.
- Solve yields, z-spreads, or OAS with robust root-finding and bracket checks.
- For callable structures, use trees, lattice methods, or Monte Carlo regression consistent with the embedded option.
- Cache schedule and accrual metadata aggressively; it is expensive and repeatedly reused.

## Production Pitfalls and Sanity Checks
- Accrued interest off by one day because settlement and accrual conventions were conflated.
- Clean and dirty price mixed in risk reports.
- Yield compounding basis not matched to the market quote.
- Broken stub periods or holiday adjustments changing coupon counts unexpectedly.
- Reporting DV01 from yield shifts for instruments whose true risk is curve-shaped or option-sensitive.
- Failing to replay historical prices because static data changed after issuance.

Minimum checks:
- accrued interest is zero on coupon dates and increases monotonically between them when expected,
- dirty price equals clean price plus accrued,
- zero-coupon bond price falls with maturity under a positive-rate curve,
- par bond prices near issuance align with coupon vs market-rate intuition,
- bumped-curve PV changes agree with DV01 sign and order of magnitude.

## Illustrative Code
```python
def bond_dirty_price(cashflows, discount_factors):
    return sum(cf * df for cf, df in zip(cashflows, discount_factors))


def macaulay_duration(cashflows, discount_factors, times, dirty_price):
    weighted_pv = sum(t * cf * df for t, cf, df in zip(times, cashflows, discount_factors))
    return weighted_pv / dirty_price


def modified_duration(macaulay: float, yield_rate: float, compounding_frequency: int) -> float:
    return macaulay / (1.0 + yield_rate / compounding_frequency)
```

## References and Further Reading
- Tuckman and Serrat. *Fixed Income Securities*
- Fabozzi. *Bond Markets, Analysis, and Strategies*
- Hagan and West on curve construction and interpolation
