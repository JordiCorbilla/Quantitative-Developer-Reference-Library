# Trade Lifecycle And Operations

Related chapters: [04-fx.md](04-fx.md), [11-market-data.md](11-market-data.md), [12-pricing-architecture.md](12-pricing-architecture.md), [13-risk-and-pnl.md](13-risk-and-pnl.md), [15-performance-and-production.md](15-performance-and-production.md), [20-execution-microstructure-and-tca.md](20-execution-microstructure-and-tca.md), and [21-regulatory-margin-capital.md](21-regulatory-margin-capital.md).

## What This Domain Covers
A trade does not become real only because a model can price it. It becomes real when somebody agrees the economics, the trade is booked, the counterparty confirms it, the cash or security moves, and the desk can explain what happened afterwards.

That lifecycle is part of quantitative development because every pricing and risk system is downstream of it. If the side is wrong, the value date is wrong, the confirmation is mismatched, or a settlement event is missing, the model can be mathematically correct and the reported risk can still be wrong.

This chapter follows the path from trade intent to post-trade control. FX is the worked example because the lifecycle is easy to see: two currencies, a quote, a value date, and real cash settlement. The same mental model applies to listed options, swaps, credit, financing, ETFs, and structured products.

## Product Taxonomy and Market Structure
The lifecycle shape depends on how the instrument trades and settles.

- **Cash products**: equities, bonds, FX spot, ETFs. The key events are execution, allocation, settlement, corporate actions or coupons, and reconciliation.
- **Linear derivatives**: forwards, futures, swaps, FX swaps, total return swaps. The key events include resets, margin, rolls, fixings, and dated cashflows.
- **Options and structured products**: listed options, OTC options, swaptions, convertibles, structured notes. Exercise, barrier monitoring, early termination, and lifecycle notices become central.
- **Credit and securitized products**: CDS, indices, tranches, ABS, CLOs. Credit events, determinations, waterfall dates, and recovery mechanics matter.
- **Cleared products**: listed futures, cleared swaps, some FX and rates products. Clearing replaces bilateral settlement paths with margin and central counterparty workflows.

The practical market structure is not just "buyer and seller". A trade may pass through a venue, broker, dealer, prime broker, clearing house, custodian, settlement system, risk engine, general ledger, and regulatory reporting process.

## Quoting and Market Conventions
Lifecycle errors often start at the quote.

- A bid is usually the price at which the market maker buys from the taker.
- An ask is usually the price at which the market maker sells to the taker.
- The spread is both an execution cost and a liquidity signal.
- The trade side must be stored from the perspective of the book or legal entity, not inferred from a human label.
- Value date, settlement calendar, currency, notional, multiplier, and day count are economic terms, not back-office decoration.

For FX, quote orientation is especially important. Buying EUR/USD means buying EUR and selling USD. The same economic intent written in inverted orientation must still produce the same cashflows.

## Core Pricing Framework
The pricing framework for lifecycle work is not a closed-form formula. It is the rule that valuation must be run against the correct economic state of the trade. A clean model price is only meaningful if the trade is genuinely live, confirmed, and represented with the right cashflows.

The basic state machine is:

1. **Pre-trade**: request, quote, suitability, limit check, market-data snapshot.
2. **Execution**: quote accepted or order filled.
3. **Capture and booking**: trade representation enters the front-office system.
4. **Validation**: economic terms, limits, static data, calendars, and settlement instructions are checked.
5. **Confirmation**: counterparties agree the trade terms.
6. **Clearing or settlement preparation**: margin, funding, nostro, custodian, clearing broker, or CLS instructions are prepared.
7. **Settlement and cash movement**: cash, securities, or variation margin move.
8. **Post-trade control**: reconciliation, PnL explain, risk explain, accounting, reporting, and exception handling.

![FX trade lifecycle from quote to settlement](assets/fx-trade-lifecycle.svg)

The key point is that pricing and lifecycle state are connected. A trade that is pending confirmation, disputed, partially settled, novated, compressed, assigned, terminated, or exercised is not the same operational object as a clean live trade.

## Worked Instrument Example: FX Spot Trade
Suppose an asset manager buys EUR 250 million against USD at EUR/USD 1.0923 for spot settlement.

The economics are simple:

$$
\text{EUR }250{,}000{,}000
$$

is received, and:

$$
\text{USD }250{,}000{,}000 \times 1.0923 = \text{USD }273{,}075{,}000
$$

is paid on the value date.

The lifecycle is where the operational detail appears:

- **Execution**: the asset manager accepts an ask quote from a bank or venue.
- **Capture**: the system records pair, side, notional, price, trade date, value date, counterparty, and settlement instructions.
- **Confirmation**: both parties match the economic terms.
- **Funding**: treasury ensures USD is available and expected EUR receipt is recognized.
- **Settlement**: payment-versus-payment, often through CLS for eligible currencies and participants, reduces principal settlement risk.
- **Post-trade**: cash balances, PnL, realized FX, fees, and any settlement breaks are reconciled.

The model is not complicated. The operational risk is that one small field can turn the economic story upside down.

## Lifecycle Patterns Across Other Instruments
The same lifecycle lens improves every product chapter.

| Product | Lifecycle Events That Matter | Typical Failure Mode |
| --- | --- | --- |
| Listed option | Exercise, assignment, expiry, corporate-action adjustment | Option expires or is assigned but risk still assumes it is live |
| Futures | Daily margin, expiry, delivery notice, roll | Position is priced on the wrong contract or stale roll assumption |
| Bond | Coupon, ex-dividend date, settlement, call notice, maturity | Accrued interest or settlement date is wrong |
| Interest-rate swap | Fixing, reset, payment, compression, collateral | Floating coupon is projected after the real fixing is known |
| FX swap | Near leg, far leg, roll, funding, settlement | Near leg settles but far-leg exposure or roll risk is missed |
| CDS | Premium accrual, credit event, auction settlement | Default event workflow is not reflected in valuation |
| ETF | Creation/redemption, basket change, rebalance | NAV, holdings, and traded price are reconciled at different timestamps |
| Repo or securities lending | Collateral substitution, haircut, margin call, return | Financing exposure is treated as static when collateral changes |

## Key Risk Measures and Sensitivities
Lifecycle state changes the risk report.

- **Market risk**: delta, PV01, vega, spread, and basis risk should reflect only economically live exposure.
- **Settlement risk**: principal or cashflow exposure exists until payment finality.
- **Counterparty risk**: exposure changes when confirmations, collateral, netting, and settlement status change.
- **Liquidity risk**: rolls, exits, and settlement fails can force funding at bad times.
- **Operational risk**: breaks, late confirms, wrong static data, and failed payments become real economic events.
- **PnL explain**: lifecycle events should be separated from market moves, carry, and residual.

## Required Data, Curves, Surfaces, and Calibration Objects
Lifecycle-aware analytics need more than market prices.

- Trade economics: side, quantity, notional, price, dates, currency, product type.
- Party and account data: counterparty, legal entity, book, clearing member, custodian, settlement account.
- Static data: calendars, business-day rules, identifiers, multipliers, contract specs, settlement instructions.
- Market data: price, curve, surface, spread, volatility, fixing, and snapshot timestamp.
- Lifecycle state: booked, amended, confirmed, cleared, settled, matured, exercised, terminated, cancelled.
- Cashflow state: projected, fixed, paid, failed, disputed, reconciled.
- Control state: limit status, confirmation status, exception owner, and break reason.

## Numerical and Implementation Approaches
The clean implementation pattern is to treat lifecycle as structured state, not free-text status.

- Store immutable economic terms separately from lifecycle events and amendments.
- Use event sourcing or an auditable event log for amendments, fixings, exercises, settlements, and terminations.
- Reprice from a consistent market-data snapshot and a consistent trade-state snapshot.
- Make cashflow state explicit: forecast, fixed, due, paid, failed, cancelled.
- Keep product valuation independent from operational workflow, but make the workflow able to tell valuation which events have occurred.
- Reconcile front-office, middle-office, settlement, accounting, and regulatory views by trade identifier and event date.

## Production Pitfalls and Sanity Checks
- A cancelled or matured trade still appears in live risk.
- A trade amendment changes economics but not downstream confirmation or risk state.
- Settlement date is inferred from trade date without the right currency or exchange calendar.
- A known fixing is overwritten by projected curve data.
- Cashflows are netted for PnL but grossed for settlement without explicit logic.
- Clearing or collateral status changes but discounting or margin treatment does not.
- Backtests use final lifecycle state instead of point-in-time lifecycle state.
- PnL explain has a residual because lifecycle events are not tagged separately.

## Illustrative Code
```python
from dataclasses import dataclass, replace
from enum import Enum


class TradeState(Enum):
    QUOTED = "quoted"
    EXECUTED = "executed"
    BOOKED = "booked"
    CONFIRMED = "confirmed"
    SETTLED = "settled"
    CLOSED = "closed"


ALLOWED_TRANSITIONS = {
    TradeState.QUOTED: {TradeState.EXECUTED},
    TradeState.EXECUTED: {TradeState.BOOKED},
    TradeState.BOOKED: {TradeState.CONFIRMED},
    TradeState.CONFIRMED: {TradeState.SETTLED},
    TradeState.SETTLED: {TradeState.CLOSED},
}


@dataclass(frozen=True)
class TradeLifecycle:
    trade_id: str
    state: TradeState

    def transition(self, new_state: TradeState) -> "TradeLifecycle":
        allowed = ALLOWED_TRANSITIONS.get(self.state, set())
        if new_state not in allowed:
            raise ValueError(f"cannot move {self.trade_id} from {self.state.value} to {new_state.value}")
        return replace(self, state=new_state)


trade = TradeLifecycle("FX-1001", TradeState.QUOTED)
trade = trade.transition(TradeState.EXECUTED)
trade = trade.transition(TradeState.BOOKED)
```

## References and Further Reading
- CLS settlement and payment-versus-payment educational material
- ISDA confirmation, collateral, and lifecycle-event documentation
- Exchange and clearing-house product specifications
- Internal operations, settlement, and trade-control standards
