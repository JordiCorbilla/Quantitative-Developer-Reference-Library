# Prime Brokerage, Counterparty, and Funding

Related chapters: [03-equities.md](03-equities.md), [09-cross-asset.md](09-cross-asset.md), [13-risk-and-pnl.md](13-risk-and-pnl.md), [19-financing-repo-and-securities-lending.md](19-financing-repo-and-securities-lending.md), [21-regulatory-margin-capital.md](21-regulatory-margin-capital.md), [26-equity-swaps-and-total-return-swaps.md](26-equity-swaps-and-total-return-swaps.md), and [30-trade-lifecycle-and-operations.md](30-trade-lifecycle-and-operations.md).

## What This Domain Covers
Prime brokerage and counterparty infrastructure determine whether a theoretically attractive trade can be financed, shorted, margined, settled, and maintained through stress.

A quant developer needs to connect three views:

1. **Trade economics**: financing spread, borrow fee, collateral return, commissions, and balance-sheet charges.
2. **Liquidity mechanics**: margin calls, settlement cash, collateral eligibility, recalls, buy-ins, and withdrawal capacity.
3. **Counterparty exposure**: current mark-to-market, netting, collateral, potential future exposure, and close-out risk.

These are not purely operational concerns. A convertible-arbitrage trade can fail when stock borrow is recalled. A merger position can become much more expensive if borrow goes special. An OTC hedge can reduce market risk while concentrating counterparty and liquidity risk. A multi-prime book can diversify default exposure but create fragmented collateral and inconsistent position records.

The objective is to measure the fully financed, executable, and close-out-aware return of the position—not only its clean model value.

## Product Taxonomy and Market Structure
The main relationships are:

- **Cash prime brokerage**: custody-style position records, margin lending, short-sale support, clearing, and financing.
- **Securities lending**: locate, borrow, loan maintenance, recalls, returns, and buy-ins.
- **Synthetic prime brokerage**: swaps or contracts for difference that provide economic exposure without cash ownership.
- **Repo and reverse repo**: cash borrowing or lending secured by securities.
- **OTC derivatives**: bilateral trades governed by master agreements and collateral terms.
- **Cleared derivatives**: exchange or clearing-house variation and initial margin.
- **Custody and unencumbered assets**: assets held outside financing chains or available for transfer.
- **Treasury and cash management**: currency balances, settlements, margin forecasts, and liquidity buffers.

The legal counterparty, executing broker, clearer, custodian, and financing provider may be different entities. Systems must represent those roles separately.

Stock-loan states should be explicit:

- indicative availability,
- locate obtained,
- borrow confirmed,
- settled loan,
- rate change,
- recall,
- return requested,
- buy-in pending,
- closed.

An indicative locate is not guaranteed term borrow. A settled borrow can still be repriced or recalled depending on the agreement.

## Quoting and Market Conventions
Financing terms are easy to misstate because desks use different sign conventions.

- A **debit rate** is charged on financed long cash balances.
- A **credit rate** or short rebate may be paid on short-sale proceeds.
- A **borrow fee** reduces the rebate and can exceed it for hard-to-borrow securities.
- Repo rates apply to the cash leg; haircuts determine how much cash is advanced.
- Margin requirements can be expressed as a percentage, stress loss, risk-based requirement, or house add-on.
- Collateral may receive an agreed interest rate subject to a spread.
- OTC thresholds, minimum transfer amounts, independent amounts, and eligible collateral are agreement-specific.

Rates require:

- currency,
- reference index,
- spread,
- day-count basis,
- effective time,
- term or open status,
- compounding and accrual convention.

Borrow fees can change intraday. Store rate histories with effective timestamps rather than replacing the prior rate. Accruals should use settled quantities, not requested or located quantities.

Counterparty exposure is agreement-dependent. Netting applies within enforceable netting sets, not automatically across all trades with the same banking group.

## Core Pricing Framework
For a financed long/short equity book over a short interval, a simplified financing PnL is:

$$
\text{Financing PnL}
=
-L r_L \Delta t
+ S r_R \Delta t
- \sum_i S_i f_i \Delta t
+ C r_C \Delta t
- \text{fees},
$$

where:

- \(L\) is the financed long debit balance;
- \(S\) is general short-sale proceeds;
- \(r_L\) is the long debit rate;
- \(r_R\) is the short rebate;
- \(S_i\) and \(f_i\) are short market value and borrow fee for name \(i\);
- \(C\) is remunerated collateral;
- \(r_C\) is its collateral rate.

The exact ledger depends on whether proceeds can offset long debits, whether collateral is segregated, and whether exposure is cash or synthetic.

Current bilateral exposure for a netting set can be simplified as:

$$
E_t = \max(V_t - C_t, 0),
$$

where \(V_t\) is net mark-to-market owed to the portfolio and \(C_t\) is recognized collateral after agreement rules and haircuts. Potential future exposure adds a distribution of future changes:

$$
\text{PFE}_{q}(T)
=
\operatorname{Quantile}_{q}
\left[
\max(V_T - C_T, 0)
\right].
$$

Liquidity risk is not captured by exposure alone. A negative mark-to-market may require a real variation-margin payment even when the final trade payoff is expected to recover.

## Worked Instrument Example
Consider a market-neutral cash equity trade:

- long market value: USD 20m;
- short market value: USD 20m;
- holding horizon: 30/360 years;
- long debit rate: 5.75%;
- short rebate before special borrow: 4.25%;
- special borrow fee on USD 5m of the short book: 9.00%;
- the remaining USD 15m is general collateral with no additional borrow fee.

Assume short proceeds offset the long debit for financing purposes. The long debit cost is:

$$
20{,}000{,}000 \times 5.75\% \times \frac{30}{360}
= \text{USD }95{,}833.
$$

The short rebate is:

$$
20{,}000{,}000 \times 4.25\% \times \frac{30}{360}
= \text{USD }70{,}833.
$$

The special borrow fee is:

$$
5{,}000{,}000 \times 9.00\% \times \frac{30}{360}
= \text{USD }37{,}500.
$$

Net financing PnL before commissions is:

$$
-95{,}833 + 70{,}833 - 37{,}500
= -\text{USD }62{,}500.
$$

If the special borrow fee rises from 9% to 30%, the thirty-day special-borrow cost becomes USD 125,000. That single financing change worsens strategy PnL by USD 87,500. If the stock is recalled, the relevant stress is not merely another fee increase: the short may have to be covered while the long leg remains exposed.

## Key Risk Measures and Sensitivities
- Financing carry by currency, prime broker, strategy, and position.
- Borrow fee, availability, utilization, concentration, and rate volatility.
- Recall and buy-in stress by security.
- Margin requirement and incremental margin by trade.
- Variation-margin cash forecast by date and currency.
- Unencumbered cash and high-quality liquid assets.
- Days of liquidity under normal and stressed outflows.
- Counterparty current exposure and PFE by enforceable netting set.
- Collateral concentration, eligibility, haircut, and wrong-way risk.
- Settlement fails, aged fails, and disputed margin.
- Counterparty concentration and replacement-cost stress.
- Gross, net, leverage, and rehypothecation exposure.

Stress funding, borrow, liquidity, and market prices together. A price fall can increase volatility-based margin; a crowded short can become expensive or unavailable; collateral haircuts can widen at the same time.

## Required Data, Curves, Surfaces, and Calibration Objects
- Prime-broker and legal-entity identifiers, roles, and account structure.
- Agreement terms: margin methodology, netting sets, thresholds, eligible collateral, and close-out rules.
- Cash balances, settled positions, pending trades, and settlement obligations.
- Debit, rebate, repo, collateral, and internal transfer-pricing curves.
- Stock-loan inventory, locate status, settled borrow, rate, term, lender, and recall events.
- Margin requirements, house add-ons, disputes, calls, and settlements.
- Collateral inventory, eligibility, haircuts, encumbrance, and substitution rights.
- OTC trade values, sensitivities, netting-set mappings, and exposure simulations.
- Counterparty credit curves, ratings, limits, and recovery assumptions.
- Currency calendars, payment cutoffs, and intraday liquidity schedules.

Snapshots should reconcile to broker statements but retain internal economic classifications. A broker account code is not a durable strategy or trade-idea identifier.

## Numerical and Implementation Approaches
Build a daily financing ledger at settled lot or position level:

1. determine settled quantity and market value;
2. select the effective financing or borrow rate;
3. apply agreement-specific day count and accrual;
4. record cash accrual separately from market PnL;
5. process rate changes, recalls, returns, and substitutions as events;
6. reconcile broker charges and cash statements.

For allocation across prime brokers, compare total incremental cost:

$$
\text{Incremental Cost}
=
\text{financing}
+ \text{borrow}
+ \text{execution}
+ \text{margin liquidity}
+ \text{counterparty concentration penalty}.
$$

The lowest quoted spread is not necessarily the best allocation if it consumes scarce margin capacity or increases single-counterparty concentration.

Maintain separate views for:

- clean price and Greeks,
- financed economic PnL,
- cash and collateral movements,
- counterparty exposure,
- broker statement and general-ledger reconciliation.

For PFE, simulate netting-set values under consistent market scenarios and apply collateral rules through time, including margin frequency and settlement lag. Do not add stand-alone trade exposures when legally enforceable netting exists, and do not net across agreements merely because names appear related.

## Production Pitfalls and Sanity Checks
- Accruing borrow on trade-date rather than settled quantity.
- Treating an indicative locate as guaranteed availability.
- Ignoring rate changes, recalls, or partial returns.
- Double-counting short rebate and borrow fee.
- Applying one day count or holiday calendar to every financing currency.
- Assuming all short proceeds can offset long debits.
- Netting trades across non-nettable agreements.
- Ignoring collateral settlement lag in exposure and liquidity.
- Allocating to the cheapest broker without margin or concentration cost.
- Reconciling only market value while financing cash remains unexplained.
- Using end-of-day positions for an intraday margin call.
- Stressing counterparty default without replacement cost or asset-access delay.

Minimum checks:

- financing accrual reconciles to balance, rate, day count, and effective dates;
- settled stock borrow equals the short quantity requiring coverage, subject to documented exceptions;
- every position maps to a legal account, counterparty, and agreement;
- collateral does not exceed available inventory and cannot be pledged twice;
- margin cashflows reconcile to calls, disputes, and settlements;
- netting-set exposure aggregates back to trade values;
- stressed liquidity includes market loss, margin, settlement, and borrow events.

## Illustrative Code
```python
def financing_pnl(
    long_debit: float,
    short_proceeds: float,
    debit_rate: float,
    rebate_rate: float,
    special_short_value: float,
    borrow_fee: float,
    year_fraction: float,
) -> float:
    if min(long_debit, short_proceeds, special_short_value, year_fraction) < 0.0:
        raise ValueError("balances and year fraction must be non-negative")
    return (
        -long_debit * debit_rate * year_fraction
        + short_proceeds * rebate_rate * year_fraction
        - special_short_value * borrow_fee * year_fraction
    )


monthly_pnl = financing_pnl(
    long_debit=20_000_000.0,
    short_proceeds=20_000_000.0,
    debit_rate=0.0575,
    rebate_rate=0.0425,
    special_short_value=5_000_000.0,
    borrow_fee=0.09,
    year_fraction=30.0 / 360.0,
)
assert round(monthly_pnl, 2) == -62_500.00
```

Production code should source effective-dated rates, settled balances, agreement rules, and currency calendars rather than accepting unlabelled scalar inputs.

## References and Further Reading
- Fabozzi and Mann. *Securities Finance: Securities Lending and Repurchase Agreements*.
- ISDA, [Legal and Documentation Resources](https://www.isda.org/category/legal/).
- ISDA, [Standard Initial Margin Model](https://www.isda.org/category/margin/simm/).
- FINRA, [Margin Accounts](https://www.finra.org/investors/investing/investment-products/stocks/margin-accounts).
- Federal Reserve, Regulation T.
- SIFMA, securities-lending and repo market resources.
- Related chapters: [19-financing-repo-and-securities-lending.md](19-financing-repo-and-securities-lending.md) and [21-regulatory-margin-capital.md](21-regulatory-margin-capital.md).
