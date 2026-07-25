# Capital-Structure Relative Value

Related chapters: [03-equities.md](03-equities.md), [05-fixed-income.md](05-fixed-income.md), [07-credit.md](07-credit.md), [09-cross-asset.md](09-cross-asset.md), [13-risk-and-pnl.md](13-risk-and-pnl.md), [19-financing-repo-and-securities-lending.md](19-financing-repo-and-securities-lending.md), and [30-trade-lifecycle-and-operations.md](30-trade-lifecycle-and-operations.md).

## What This Domain Covers
Capital-structure relative value asks whether securities issued by the same economic enterprise imply consistent views of asset value, default probability, recovery, volatility, and control rights. The opportunity may sit between a loan and a bond, cash bonds and CDS, debt and equity, an operating company and its holding company, or adjacent maturities and seniorities.

This is not simply a screen for the widest spread. A valid comparison must identify the exact borrower, guarantors, collateral, priority, currency, maturity, covenants, deliverability, liquidity, and financing of every leg. Two instruments bearing the same issuer name can have materially different claims.

For a quant developer, the domain joins reference-data modelling, credit curves, equity and option risk, legal-document extraction, financing, multi-leg position management, recovery waterfalls, scenario PnL, and historical replay. The system must preserve both the economic thesis and the contractual facts that can invalidate it.

## Product Taxonomy and Market Structure
An issuer stack commonly contains:

- Revolvers, first-lien term loans, second-lien loans, and other secured facilities.
- Senior unsecured, subordinated, and structurally subordinated bonds.
- Preferred stock, convertible debt, warrants, and common equity.
- Single-name CDS, credit indices, equity options, and total return swaps used as hedges.
- Claims at different legal entities, including operating-company and holding-company debt.

Common trade families include:

- **Bond-CDS basis:** compare a cash bond's credit spread with protection on a contractually eligible reference entity and seniority.
- **Loan-CDS or loan-bond relative value:** express a view on collateral, covenant protection, liquidity, or recovery.
- **Seniority and curve trades:** long one claim and short another while controlling rate and broad spread exposure.
- **Credit-equity trades:** compare credit-implied distress with equity value or volatility, often using stock or options as the hedge.
- **Holding-company/operating-company trades:** isolate structural subordination and upstreaming risk.
- **Recovery trades:** position for the distribution of enterprise value following restructuring rather than for small spread convergence.

The relevant market is fragmented. Loans may settle by assignment or participation, bonds through dealer markets, CDS under standardized definitions, and equities or listed options on exchanges. Liquidity, margin, settlement timing, and close-out rights differ across legs.

## Quoting and Market Conventions
- Bonds normally quote clean price as a percentage of par; settlement cash includes accrued interest. Spread may mean government spread, interpolated spread, Z-spread, asset-swap spread, or option-adjusted spread.
- Loans generally quote in points of par and pay a floating benchmark plus spread, often subject to a benchmark floor. Delayed settlement compensation and assignment fees matter.
- CDS may quote running spread or upfront plus a standard coupon. The protection buyer pays premium and gains when the quoted spread widens or a covered credit event occurs.
- Equity quotes per share; options add contract multiplier, expiry, strike, exercise style, and volatility-surface conventions.
- Yield and spread comparisons require aligned day count, calendars, settlement date, currency discount curve, accrued-interest treatment, and embedded-option assumptions.
- Recovery must specify the claim, valuation date, and denominator. Recovery of 40% of face is not the same as a 40% return on an 80-price purchase.

Risk reports should state signs explicitly. One useful convention defines DV01 and CS01 as the dollar *gain* for a one-basis-point fall in rates or credit spreads. CDS protection then has negative signed CS01 under that convention because it gains when spreads rise. Other conventions are valid, but mixing them silently is not.

## Core Pricing Framework
### One Enterprise, Several Claims

Let distributable value in scenario \(k\) be enterprise value after administrative costs and higher-priority leakage:

$$
A_k = \max(EV_k - C_k, 0).
$$

For claim \(i\), ordered from most senior to most junior, with allowed amount \(F_i\), a simple absolute-priority waterfall gives:

$$
R_{i,k} = \min\left(F_i,\max\left(A_k-\sum_{j<i}R_{j,k},0\right)\right).
$$

Its recovery rate is \(R_{i,k}/F_i\). Real restructurings can deviate because of collateral silos, guarantees, adequate-protection claims, disputed amounts, new-money priority, valuation negotiation, and plan consideration paid as cash, debt, or equity. The waterfall is therefore a scenario engine, not a legal conclusion.

### Relative-Value Portfolio

For quantities \(q_i\), full prices \(P_i\), and financing cash account \(B\), current value is:

$$
V = \sum_i q_i P_i + B.
$$

Under scenario \(k\):

$$
\Delta V_k = \sum_i q_i(P_{i,k}-P_i)
 + \text{carry}_k - \text{funding}_k - \text{transaction costs}_k.
$$

A trade is sized against the whole distribution of \(\Delta V_k\), not just the expected convergence. Local hedges can be obtained by solving:

$$
\mathbf{A}\mathbf{h}=-\mathbf{r},
$$

where \(\mathbf{r}\) contains the core position's rate DV01, credit CS01, equity delta, FX delta, or sector beta, and columns of \(\mathbf{A}\) contain candidate hedge sensitivities. Liquidity limits and hedge bounds turn this into a constrained least-squares problem. Default, restructuring, call, and borrow-recall scenarios remain necessary because local sensitivities do not describe gaps.

For a bond-CDS comparison, a screening measure is:

$$
\text{net basis}
\approx s_{\text{bond}}-s_{\text{CDS}}
-c_{\text{funding}}-c_{\text{borrow}}-c_{\text{delivery}}-c_{\text{liquidity}}.
$$

The bond spread must be option- and curve-consistent, and the adjustment terms cannot be treated as universal constants. Positive carry is not arbitrage if default settlement, cheapest-to-deliver optionality, funding, or legal basis can overwhelm it.

### Trade Construction Checklist

1. Map every security to its borrower, reference entity, guarantors, collateral, and claim priority.
2. State the catalyst and what observable relationship should converge.
3. Value each leg from a common market snapshot, with separate credit, rate, volatility, liquidity, and financing inputs.
4. Neutralize only the intended local risks; preserve the exposure named in the thesis.
5. Run recovery waterfalls, rating migration, spread gaps, equity gaps, rate moves, FX moves, and liquidity/financing stresses.
6. Size to a documented loss limit and record hedge ratios, rebalance rules, exit criteria, and invalidation conditions.

## Worked Instrument Example
Consider an issuer with USD 300m first-lien debt, USD 400m senior unsecured debt, and USD 250m subordinated debt. A downside case assumes enterprise value of USD 570m and USD 20m of administrative and restructuring costs.

Distributable value is USD 550m. The first lien receives USD 300m, the unsecured class receives the remaining USD 250m, and the subordinated class receives zero. Waterfall recoveries are therefore 100%, 62.5%, and 0%.

Suppose USD 10m face of the unsecured bond trades at 82 clean and an investor buys USD 10m of matched unsecured CDS protection. Ignoring accrued interest, the bond costs USD 8.2m. If a covered credit event occurs and the CDS auction recovery is also 62.5%, the bond is worth USD 6.25m and CDS pays:

$$
10m\times(1-62.5\%)=3.75m.
$$

The two default settlements total USD 10m before premium, funding, settlement, and delivery effects. The apparent USD 1.8m uplift over purchase price compensates for CDS premium and the many ways the assumptions can fail.

If the bond's comparable spread is 760 bps, CDS costs 620 bps, annualized bond funding consumes 65 bps, and liquidity/delivery reserves consume 25 bps, estimated net carry is:

$$
760-620-65-25=50\text{ bps},
$$

or about USD 50,000 per year on USD 10m face before convexity, accrual, and trading costs. The trade is not risk-free: the CDS may reference a different entity, an obligation may be non-deliverable, the auction price may differ from the owned bond's value, or the bond may be called before convergence.

A reproducible waterfall for this example is in [examples/capital-structure-recovery-waterfall.md](examples/capital-structure-recovery-waterfall.md).

## Key Risk Measures and Sensitivities
- Rate DV01 and key-rate duration by cash instrument.
- Credit CS01 by issuer, curve tenor, seniority, and instrument.
- Jump-to-default and recovery sensitivity by legal claim.
- Equity delta, gamma, vega, and credit-equity cross-risk.
- Curve, seniority, cash-CDS, holding-company/operating-company, and cross-currency basis.
- Carry, roll-down, coupon accrual, financing, borrow, and margin consumption.
- Liquidity: bid-ask, days to liquidate, dealer concentration, and settlement latency.
- Scenario loss under downgrade, default, restructuring, priming debt, collateral leakage, and covenant amendment.
- Hedge slippage when CS01, beta, conversion delta, or deliverability changes.

## Required Data, Curves, Surfaces, and Calibration Objects
Static and legal data should be effective-dated and sourced to documents:

- Issuer and legal-entity hierarchy; domicile; entity identifiers; guarantor relationships.
- Security, facility, and tranche identifiers; borrower; currency; face; maturity; coupon; call/put terms.
- Lien rank, collateral package, guarantee coverage, structural priority, intercreditor terms, covenants, and baskets.
- CDS reference entity, tier, restructuring clause, standard coupon, covered events, and deliverable-obligation characteristics.
- Corporate actions, exchange offers, tenders, amendments, consent deadlines, and bankruptcy milestones.

Market and model state includes:

- Bond and loan bid/ask/size, accrued interest, settlement assumptions, and evaluated-price lineage.
- CDS curves, recovery assumptions, discount curves, repo/funding curves, stock borrow, equity prices, dividends, and volatility surfaces.
- Hazard curves by entity and seniority, rate curves, equity-credit dependency assumptions, liquidity adjustments, and recovery scenarios.

A useful schema separates `legal_entity`, `security`, `claim`, `guarantee`, `collateral_link`, `covenant_version`, `market_quote`, `position_leg`, `hedge_link`, and `scenario_result`. Each legal fact should carry `effective_from`, `effective_to`, `known_at`, `source_document_id`, and clause/page provenance. This prevents a later amendment or entity remap from leaking into an earlier backtest.

## Numerical and Implementation Approaches
- Build a security master around legal entities and claims, not ticker strings.
- Bootstrap rates and hazard curves independently, then reconcile cash and derivative marks without forcing liquidity basis into default probability.
- Implement the recovery waterfall as an auditable allocation graph supporting collateral silos, guarantees, claim caps, and alternative plan consideration.
- Store risk on both native and normalized bases: face, market value, CS01, DV01, equity delta, and scenario loss.
- Use full revaluation for default, exchange, tender, call, and restructuring scenarios. Sensitivity approximations are adequate only for small continuous shocks.
- Attribute daily PnL to rate curve, credit curve, equity, volatility, carry/accrual, financing, trade activity, legal/reference-data changes, and residual.
- Archive raw quotes, normalized marks, curves, terms, model version, and position snapshot so any historical recommendation can be replayed.

## Production Pitfalls and Sanity Checks
- Matching issuer names while missing different borrowers, guarantors, or collateral silos.
- Assuming “senior unsecured” means equal recovery across operating and holding entities.
- Using clean bond price in cash settlement or omitting accrued interest.
- Comparing Z-spread with CDS spread without curve, option, and funding adjustments.
- Hedging face notional instead of CS01, then assuming local spread neutrality.
- Treating CDS as a perfect hedge without checking reference entity, tier, restructuring clause, expiry, and deliverability.
- Ignoring embedded calls, make-wholes, tenders, loan prepayments, or change-of-control puts.
- Applying one recovery rate to secured, unsecured, and subordinated claims.
- Double-counting coupon accrual and carry in PnL explain.
- Backtesting with today's entity hierarchy, covenants, or amended terms.
- Ignoring loan settlement delays, short-bond availability, CDS margin, and close-out basis.

Sanity checks should enforce that waterfall allocations never exceed distributable value or allowed claims, junior recoveries do not appear before senior claims are satisfied unless an explicit rule permits it, hedge risk signs are consistent, and scenario PnL reconciles leg-by-leg to portfolio PnL.

## Illustrative Code
```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Claim:
    name: str
    allowed_amount: float


def absolute_priority_waterfall(
    enterprise_value: float,
    costs: float,
    claims: list[Claim],
) -> dict[str, float]:
    remaining = max(enterprise_value - costs, 0.0)
    recoveries: dict[str, float] = {}
    for claim in claims:  # most senior first
        payment = min(max(claim.allowed_amount, 0.0), remaining)
        recoveries[claim.name] = payment
        remaining -= payment
    return recoveries
```

Production code should also represent collateral silos, guarantees, disputed claims, new-money priority, and non-cash plan consideration.

## References and Further Reading
- Merton. “On the Pricing of Corporate Debt: The Risk Structure of Interest Rates.” *Journal of Finance*, 1974.
- Duffie and Singleton. *Credit Risk: Pricing, Measurement, and Management*.
- O'Kane. *Modelling Single-name and Multi-name Credit Derivatives*.
- Altman and Hotchkiss. *Corporate Financial Distress, Restructuring, and Bankruptcy*.
- International Swaps and Derivatives Association. *2014 ISDA Credit Derivatives Definitions* and auction settlement materials.
- Loan Syndications and Trading Association and Loan Market Association documentation and settlement guidance.
- The relevant executed credit agreements, indentures, guarantees, security agreements, intercreditor agreements, and offering documents.
