# Cross-Currency Swaps

Related chapters: [04-fx.md](04-fx.md), [06-interest-rates.md](06-interest-rates.md), [09-cross-asset.md](09-cross-asset.md), [11-market-data.md](11-market-data.md), and [19-financing-repo-and-securities-lending.md](19-financing-repo-and-securities-lending.md).

## What This Domain Covers
A cross-currency swap exchanges funding exposure across currencies.

The simple story is two parties exchange notionals in different currencies, pay interest in those currencies, and often exchange notionals back at maturity. The practical story is richer: collateral currency, basis spreads, resettable notionals, FX fixings, curve construction, and funding stress all matter.

Cross-currency swaps are core instruments for funding, asset-liability management, and multi-currency derivatives pricing. They connect FX, rates, collateral, and basis curves.

## Product Taxonomy and Market Structure
Start by identifying notional exchange and coupon style.

- Fixed-fixed cross-currency swaps.
- Fixed-floating cross-currency swaps.
- Floating-floating cross-currency basis swaps.
- Mark-to-market or resettable notional swaps.
- Non-deliverable cross-currency swaps in restricted currencies.

## Quoting and Market Conventions
- Quotes often appear as basis spreads added to one floating leg.
- Initial and final notional exchanges may be included or excluded.
- Resettable swaps update one notional using FX fixings.
- Collateral currency affects discounting.
- Payment calendars, fixing lags, day counts, and spot lags differ by currency.

## Core Pricing Framework
A cross-currency swap is valued as two currency cashflow legs converted through FX and discounted under the collateral convention.

At a high level:

$$
PV = PV_{\text{domestic leg}} - FX_0 \times PV_{\text{foreign leg}}
$$

The basis spread is the spread that makes the two legs balance under market quotes.

In practice, pricing requires a curve stack: domestic discount curve, foreign projection curve, collateral discounting assumptions, FX spot, FX forwards or basis curve, and fixing data.

## Worked Instrument Example: Notional Exchange
Assume:
- EUR notional: EUR 10m,
- EUR/USD spot: 1.1000,
- USD notional exchanged: USD 11m.

At inception one party pays EUR 10m and receives USD 11m. Over time, each side pays coupons in its own currency. At maturity, the notionals are exchanged back unless the structure omits final exchange or uses resettable notionals.

If the swap is resettable, the USD notional may be updated using FX fixings so FX exposure is reduced but not eliminated from operations and settlement.

## Key Risk Measures and Sensitivities
- FX delta and FX fixing risk.
- Domestic and foreign curve PV01.
- Cross-currency basis sensitivity.
- Collateral currency and funding sensitivity.
- Reset and settlement risk.
- Counterparty and wrong-way risk.

## Required Data, Curves, Surfaces, and Calibration Objects
- FX spot, FX forwards, and cross-currency basis quotes.
- Domestic and foreign discount/projection curves.
- Coupon schedules, calendars, day counts, and fixing rules.
- Initial/final exchange flags and resettable notional rules.
- CSA and collateral currency terms.

## Numerical and Implementation Approaches
- Represent each currency leg explicitly.
- Keep notional exchanges as cashflows, not annotations.
- Build basis curves with clear collateral assumptions.
- Reconcile FX forwards implied by curves against market FX swap and basis quotes.
- Treat resettable notionals as lifecycle events.

## Production Pitfalls and Sanity Checks
- Discounting both legs with the wrong collateral curve.
- Missing final exchange of notionals.
- Treating resettable notional as eliminating all FX risk.
- Mixing FX spot date and trade date.
- Applying one calendar to both currency legs.
- Reporting PV without currency decomposition.

## Illustrative Code
```python
def convert_foreign_pv_to_domestic(foreign_pv: float, fx_spot_domestic_per_foreign: float) -> float:
    return foreign_pv * fx_spot_domestic_per_foreign
```

## References and Further Reading
- Andersen and Piterbarg. *Interest Rate Modeling*
- Henrard. *Interest Rate Modelling in the Multi-Curve Framework*
- Dealer cross-currency basis swap convention guides
