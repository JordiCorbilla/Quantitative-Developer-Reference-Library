# Rates Options: Caps, Floors, and Swaptions

Related chapters: [01-options.md](01-options.md), [05-fixed-income.md](05-fixed-income.md), [06-interest-rates.md](06-interest-rates.md), [10-numerical-methods.md](10-numerical-methods.md), and [18-volatility-products.md](18-volatility-products.md).

## What This Domain Covers
Rates options are options on future interest rates or swaps.

A cap protects against rates rising above a strike. A floor protects against rates falling below a strike. A swaption gives the right to enter an interest-rate swap. These instruments sit at the center of rates volatility, mortgage hedging, callable bonds, structured notes, and balance-sheet risk.

The quant challenge is that the underlying is not a stock price. It is a forward rate, swap rate, annuity, curve, or model state. Quoting conventions, normal vs lognormal volatility, tenor grids, and calibration instruments are central.

## Product Taxonomy and Market Structure
Start with the underlying rate exposure.

- Caps: portfolios of caplets on forward rates.
- Floors: portfolios of floorlets on forward rates.
- Collars: long cap and short floor, or the reverse.
- European swaptions: option to enter a swap on one exercise date.
- Bermudan swaptions: option to enter or cancel on multiple dates.
- Callable bond and structured-note embedded options.

## Quoting and Market Conventions
- Caps/floors quote strike, maturity, index tenor, and Black or normal vol.
- Swaptions quote option expiry, underlying swap tenor, strike, and vol convention.
- Normal vols are common when rates can be near or below zero.
- Vol cubes depend on expiry, tenor, and strike or moneyness.
- Premium settlement, annuity, calendars, and exercise cut-off matter.

## Core Pricing Framework
A cap is a strip of caplets. For a simple term-rate coupon fixing at $T_i$ and paying at $T_{i+1}$, a caplet pays $N\alpha_i\max(L_{T_i}-K,0)$ at payment. Its price uses the payment-date discount factor and the corresponding forward measure. A compounded overnight coupon can have different observation, exercise, and payment timing; resolve the actual payoff before selecting the model.

For a European physically settled payer swaption, the underlying is a par swap rate and the natural scale is the swap annuity. Under a consistent collateral and projection setup, the time-zero price can be expressed as:

$$
V_0=A_0\,\mathbb{E}^{Q^A}[(S_T-K)^+],
\qquad A_0=N\sum_j\alpha_jP(0,T_j).
$$

Here $S_T$ is the underlying forward-starting swap rate at exercise, $K$ is the strike, $A_0$ is today's fixed-leg annuity including notional, and $Q^A$ is the annuity measure. The random exercise-time annuity is absorbed by the measure change; replacing it with an arbitrary fixed annuity inside a risk-neutral expectation is not the same calculation. Rates are decimals, so the annuity is currency per 1.00 rate unit. A reported PVBP equals $10^{-4}A_0$.

Black-style models assume lognormal rates or shifted rates. Bachelier-style models assume normal rate moves. Desk convention determines which model is used for quote interpretation and risk.

For an ATM European payer under a constant normal-volatility quote, the Bachelier price simplifies to $A_0\sigma_N\sqrt{T}/\sqrt{2\pi}$. With $A_0=\text{USD }4.5m$, $T=1$ year, and $\sigma_N=100$ basis points per square-root year ($0.01$ in decimal units), premium is about USD 17,952. This is a price before exercise; the next example is an exercise-time value. Cash-settled swaptions can use a contractual cash annuity and a different settlement convention. QuantLib's [swaption engine](https://github.com/lballabio/QuantLib/blob/master/ql/pricingengines/swaption/blackswaptionengine.hpp) explicitly distinguishes physical and cash settlement annuities.

## Worked Instrument Example: Payer Swaption Payoff
Assume:
- exercise-time underlying swap annuity: USD 4.5m per 1.00 rate unit,
- expiry swap rate: 4.20%,
- strike: 4.00%.

The intrinsic payoff is:

$$
4{,}500{,}000 \times (4.20\% - 4.00\%) = 9{,}000
$$

A payer swaption benefits when the underlying swap rate rises above the strike, because it gives the holder the right to pay fixed below market. For physical settlement, USD 9,000 is the value of the swap entered at exercise, rather than necessarily a cash payment received then. Premium paid, subsequent swap cashflows, and any cash-settlement annuity are separate economics.

## Key Risk Measures and Sensitivities
- Delta/PV01 to curve moves.
- Vega by option expiry and swap tenor.
- Smile/skew sensitivity.
- Gamma and convexity under rate shocks.
- Correlation and model risk for Bermudan/callable products.
- Normal-vs-Black volatility basis.

## Required Data, Curves, Surfaces, and Calibration Objects
- OIS discount curve and projection curves.
- Cap/floor volatility surfaces.
- Swaption volatility cube.
- Exercise schedules and underlying swap schedules.
- Model parameters for Hull-White, GSR, LMM, SABR, or desk model.
- Fixings, calendars, day counts, and settlement rules.

## Numerical and Implementation Approaches
- Use caplet/floorlet decomposition for vanilla caps and floors.
- Use annuity-measure intuition for European swaptions.
- Calibrate rates option models to the correct cap/floor or swaption instruments.
- Use trees, PDEs, or regression methods for Bermudan exercise.
- Keep Black, shifted-Black, and Bachelier quote conversions explicit.

## Production Pitfalls and Sanity Checks
- Mixing normal and lognormal vol quotes.
- Applying one volatility across expiry/tenor/strike without checking cube convention.
- Using the wrong annuity or underlying swap schedule.
- Ignoring exercise cut-off and settlement rules.
- Calibrating to caps but pricing swaptions without understanding model fit.
- Reporting scalar rho instead of curve-bucket sensitivities.

## Illustrative Code
```python
import math


def payer_swaption_intrinsic(annuity: float, swap_rate: float, strike: float) -> float:
    return annuity * max(swap_rate - strike, 0.0)


# ATM normal-model price with time-zero annuity including notional.
annuity_today = 4_500_000.0
normal_vol = 100.0 * 1e-4
expiry_years = 1.0
atm_premium = annuity_today * normal_vol * math.sqrt(expiry_years) / math.sqrt(2 * math.pi)
assert round(atm_premium, 2) == 17_952.40
assert math.isclose(payer_swaption_intrinsic(4_500_000.0, 0.042, 0.04), 9_000.0)
```

## References and Further Reading
- QuantLib. [Black and Bachelier swaption engine](https://github.com/lballabio/QuantLib/blob/master/ql/pricingengines/swaption/blackswaptionengine.hpp), including settlement-specific annuity calculation.
- Brigo and Mercurio. *Interest Rate Models*
- Andersen and Piterbarg. *Interest Rate Modeling*
- Hagan et al. on SABR volatility modelling
