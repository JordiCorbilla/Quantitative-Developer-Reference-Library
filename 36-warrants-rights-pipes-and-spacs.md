# Warrants, Rights, PIPEs, and SPAC Securities

Related chapters: [01-options.md](01-options.md), [03-equities.md](03-equities.md), [13-risk-and-pnl.md](13-risk-and-pnl.md), [19-financing-repo-and-securities-lending.md](19-financing-repo-and-securities-lending.md), [25-convertibles-and-equity-linked-notes.md](25-convertibles-and-equity-linked-notes.md), [30-trade-lifecycle-and-operations.md](30-trade-lifecycle-and-operations.md), and [33-event-driven-and-merger-arbitrage.md](33-event-driven-and-merger-arbitrage.md).

## What This Domain Covers
Warrants, subscription rights, private investments in public equity (PIPEs), and special-purpose acquisition company (SPAC) securities combine equity optionality with financing and corporate-action mechanics. They often trade as families: a unit separates into common shares and fractions of warrants or rights; a financing changes the fully diluted share count; a vote and redemption alter both cash per share and the probability that warrants survive.

The challenge is to preserve contractual identity through that lifecycle. A warrant is not always equivalent to a listed call, and a redeemable share is not ordinary cash equity. Valuation must connect payoff terms, cap-table dilution, event state, borrow, settlement eligibility, and document versions.

## Product Taxonomy and Market Structure
- **Warrants**: issuer-created options that may be detachable or attached, public or private, cash or cashless exercisable, American or European, redeemable, resettable, or subject to anti-dilution adjustments.
- **Subscription rights**: short-dated rights given or sold to existing holders, commonly requiring $r$ rights plus a subscription price to acquire one new share.
- **Units**: packages containing common stock plus a fraction of a warrant, right, or other security. Components may not separate until a stated date and operational instruction.
- **PIPEs**: negotiated purchases of common stock, preferred stock, convertibles, or other equity-linked securities, often conditional on a related transaction and subject to resale-registration or lock-up provisions.
- **SPAC securities**: IPO units, redeemable common shares, public and sponsor warrants, rights, founder or sponsor shares, and securities issued in a business combination or financing.

A typical SPAC lifecycle is IPO and trust funding, unit separation, target search, transaction announcement, proxy or tender process, holder vote and redemption election, financing and closing, then conversion into an operating company. If no transaction closes before the deadline, liquidation generally returns trust cash to eligible common holders while warrants and sponsor instruments may expire worthless.

Market structure spans exchanges, private contracts, transfer agents, custodians, warrant agents, lenders, and corporate-action processors. Similar tickers can hide different identifiers, restrictions, adjustments, or settlement eligibility.

## Quoting and Market Conventions
Common shares, units, warrants, and rights normally quote per security, but their economic units differ. Always store:

- shares delivered per warrant and exercise price per delivered share;
- number of rights required per subscription share;
- warrant or right fraction contained in one unit;
- earliest separation, exercise, and expiry dates;
- cashless-exercise formula, redemption trigger, notice period, and redemption price;
- trust cash per redeemable share, expected taxes or permitted withdrawals, and redemption deadline;
- PIPE purchase price, funded amount, security type, closing condition, resale or lock-up terms, and beneficial-ownership cap.

Ticker suffixes are vendor conventions, not durable identifiers. Unit separation may require an instruction, whole-number quantities, fees, and processing time.

Rights are sensitive to record, ex-rights, subscription, oversubscription, and expiration dates. Warrants may adjust for splits, extraordinary dividends, tender offers, below-market issuances, or reorganizations. Terms in the governing agreement override generic option assumptions.

## Core Pricing Framework
Under simple assumptions, a unit containing one common share and $w$ warrants satisfies:

```math
U \approx S + wW + rR + A
```

where $U$ is unit value, $S$ common value, $W$ warrant value, $R$ right value, and $A$ is the value of restrictions, fees, separation timing, and settlement optionality. A non-zero package residual is not automatically executable arbitrage.

For $N$ existing shares and $M$ identical one-for-one European corporate warrants, start with the exercise proceeds. In a simple debt-free, no-dividend firm-value model with no other claims, write $X_T$ for equity value before the exercise cash arrives. Each exercised warrant receives a new share and pays $K$, so its expiry payoff is:

```math
W_T=\max\left(\frac{X_T+MK}{N+M}-K,0\right)
=\frac{N}{N+M}\max\left(\frac{X_T}{N}-K,0\right).
```

If $X_t/N$ follows the required lognormal pricing dynamics, a corresponding benchmark is $W_0=N/(N+M)\,C(X_0/N,K,T,\sigma_X,r,0)$. The call's underlying is equity value per existing share **before allocating value to warrants**, not automatically the observed stock price. In this model $X_0=NS_0+MW_0$; using observed $S_0$ and stock volatility without this distinction is only a heuristic. The [Olvik and Kangro paper, section 3.1](https://arxiv.org/html/1503.05139) derives the payoff and explains why warrants alter stock-price dynamics.

Production valuation must add redemption barriers, notice periods, cashless exercise, share-price averaging, changing share count, private-warrant transfer features, and event-dependent survival. These can dominate the benchmark. Bank-issued covered warrants that transfer existing shares do not introduce this corporate dilution mechanism.

For a rights issue in which $r$ old shares each receive one right and $r$ rights buy one new share at subscription price $K$, the theoretical ex-rights price is:

```math
\text{TERP}=\frac{rS_0+K}{r+1}
```

and the theoretical value of one right before the stock goes ex-rights is:

```math
R=\frac{S_0-K}{r+1}
```

A redeemable SPAC common share can be decomposed as:

```math
S = p_{\text{redeem}}V_{\text{trust}}
+p_{\text{close}}V_{\text{post-close}}
+p_{\text{liquidate}}V_{\text{liquidation}}
-\text{frictions}
```

with mutually exclusive branches defined at the holder level. The holder's redemption election, transaction outcome, and ability to keep or separate warrants must be modelled explicitly.

## Worked Instrument Example
Assume a separable unit trades at USD 10.38. Its common share trades at USD 10.06 and each unit contains one-half of a public warrant. Ignoring rights and frictions, the warrant value implied by the unit is:

```math
W_{\text{implied}}
=\frac{10.38-10.06}{0.5}
=\text{USD }0.64
```

If the separately traded warrant is USD 0.58, the marked component package is:

```math
10.06+0.5(0.58)=\text{USD }10.35
```

so the unit carries a USD 0.03 premium. That premium must be compared with bid-ask spreads, separation fees, whole-unit constraints, processing time, borrow, and settlement risk before it is considered tradeable.

Suppose estimated net trust value on a redemption date 120 days away is USD 10.12. The common's simple trust discount is USD 0.06, and the frictionless annualized convergence rate is:

```math
\left(\frac{10.12}{10.06}\right)^{365/120}-1=1.83\%
```

It is not risk-free: trust value may change, instructions can fail, and a holder who does not redeem owns the post-combination share. See the executable [SPAC unit and warrant example](examples/spac-unit-and-warrant.md).

As a separate rights check, if four rights permit purchase of one share at USD 8 while the cum-rights stock is USD 10, TERP is USD 9.60 and each right is theoretically worth USD 0.40.

## Key Risk Measures and Sensitivities
- **Warrant delta, gamma, vega, theta, and gap risk**, including exposure around redemption triggers and notice periods.
- **Dilution sensitivity** to exercise, sponsor shares, earn-outs, PIPE conversion, employee awards, and anti-dilution resets.
- **Trust basis**: common price less estimated net redemption proceeds, with timing and eligibility.
- **Transaction and liquidation scenarios**: value every security family under close, high redemption, delayed close, termination, extension, and liquidation.
- **Redemption and float risk**: redemptions can sharply reduce public float and make borrow, price, and volatility discontinuous.
- **Borrow and recall risk**: hedges may become expensive or unavailable exactly when a financing or business combination closes.
- **Registration and liquidity risk**: resale effectiveness, lock-ups, transfer restrictions, and share-delivery timing affect hedgeability.
- **Concentration and ownership limits**: beneficial-ownership blockers or position limits can prevent exercise or settlement.

PnL attribution should separate common stock, warrant optionality, trust accrual, unit/component basis, corporate-action conversion, borrow, funding, PIPE mark, dilution-model change, event probability, execution, and unexplained residual.

## Required Data, Curves, Surfaces, and Calibration Objects
Build a security-family model rather than independent ticker rows. Required fields include:

- issuer, legal security identifier, share class, listing, currency, and parent unit;
- unit composition and separation eligibility by date;
- warrant ratio, strike, expiry, exercise style, share-settlement rules, cashless tables, redemption tests, notice period, and anti-dilution clauses;
- rights ratio, subscription price, key dates, transferability, proration, and oversubscription rules;
- trust balance, redeemable share count, accrued income, taxes, permitted withdrawals, extension contributions, and estimated redemption value;
- proposed transaction milestones, redemption results, votes, financing commitments, closing conditions, and liquidation deadline;
- basic and fully diluted share-count waterfall, earn-outs, sponsor holdings, lock-ups, PIPE terms, and resale-registration state;
- point-in-time prices, option surface, rates, dividends, locate and borrow data, corporate actions, and settlement status.

Recommended tables are `security_family`, `instrument_terms`, `unit_component`, `cap_table_claim`, `trust_snapshot`, `event_log`, and `restriction_state`. Retain source locator, effective time, and `known_at` for every material term.

## Numerical and Implementation Approaches
Use a terms engine that evaluates payoffs from contract fields, not product-name shortcuts. A cap-table engine should reconcile basic shares to fully diluted shares under selectable scenarios, including net share settlement, cash exercise proceeds, conversion, redemptions, earn-outs, and ownership caps.

An option model provides a baseline. A lattice is more useful when redemption can force early exercise after a price test; Monte Carlo may help when triggers use multi-day averages. Publish model value alongside intrinsic and unit-implied value.

Model the lifecycle as events: issuance, listing, separation, exercise eligibility, adjustment, redemption notice, exercise, expiry, vote, redemption, conversion, and liquidation. Corporate actions must create auditable position transformations rather than overwrite symbols.

Document parsing should extract candidate terms with confidence and citations. Terms affecting cash or shares require human validation and dual control. Reconcile expected component quantities to transfer-agent or custodian records before trading a package.

## Production Pitfalls and Sanity Checks
- Valuing every warrant as a vanilla listed call and omitting issuer dilution or forced redemption.
- Treating public and privately placed warrants as fungible despite transfer-dependent terms.
- Assuming a unit can be separated immediately, automatically, or without fees.
- Using announced trust cash indefinitely without updating taxes, extensions, withdrawals, and share count.
- Forgetting that warrants usually receive no liquidation distribution.
- Applying one ticker's price history across a unit-to-components identifier change.
- Counting PIPE shares in float before closing or resale eligibility.
- Using maximum fully diluted shares in one report and treasury-stock or if-converted shares in another without labels.
- Ignoring fractional entitlements and rounding at exercise or unit separation.

Sanity checks should enforce `unit quantity × component fraction = expected entitlement`, reconcile trust assets to redeemable shares, test warrant payoff monotonicity in stock price, reproduce published adjustment examples, and bridge every cap-table version. Unit value should approximately reconcile to marked components after known frictions. Negative time value, unexplained strike changes, or a warrant surviving a liquidation scenario should trigger review.

## Illustrative Code
```python
def unit_implied_warrant(
    unit_price: float, common_price: float, warrants_per_unit: float
) -> float:
    if warrants_per_unit <= 0.0:
        raise ValueError("warrants_per_unit must be positive")
    return (unit_price - common_price) / warrants_per_unit


def theoretical_ex_rights_price(
    cum_rights_price: float, subscription_price: float, rights_required: int
) -> float:
    if rights_required <= 0:
        raise ValueError("rights_required must be positive")
    return (
        rights_required * cum_rights_price + subscription_price
    ) / (rights_required + 1)


def unit_component_residual(
    unit_price: float,
    common_price: float,
    warrant_price: float,
    warrants_per_unit: float,
) -> float:
    return unit_price - common_price - warrants_per_unit * warrant_price
```

## References and Further Reading
- U.S. Securities and Exchange Commission. *Special Purpose Acquisition Companies, Shell Companies, and Projections*, Release No. 33-11265, and related investor bulletins.
- U.S. Securities and Exchange Commission. Forms S-1, S-4, 8-K, proxy and tender-offer filings, and Securities Act resale-registration requirements.
- NYSE and Nasdaq listing manuals for warrants, shareholder approval, equity issuance, and acquisition-company requirements.
- Options Clearing Corporation information memoranda for listed-option adjustments after rights issues, mergers, and reorganizations.
- Primary prospectuses, warrant agreements, rights offering documents, subscription agreements, charter documents, and transfer-agent notices.
- Steven Dresner and E. Kurt Kim, editors. [*PIPEs: A Guide to Private Investments in Public Equity*](https://www.wiley-vch.de/en?isbn=9781576601945&option=com_eshop&title=PIPEs&view=product), second edition, 2005. *The PIPEs Report* is a separate publication, not this book's title.
- Olvik and Kangro. [*Pricing of Warrants with Stock Price Dependent Threshold Conditions*](https://arxiv.org/abs/1503.05139), 2015, especially the classical corporate-warrant benchmark in section 3.1.
- [Options](01-options.md) for baseline option sensitivities and [Convertibles and Equity-Linked Notes](25-convertibles-and-equity-linked-notes.md) for hybrid security modelling.
