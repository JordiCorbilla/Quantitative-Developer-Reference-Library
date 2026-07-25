# Event-Driven Investing and Merger Arbitrage

Related chapters: [03-equities.md](03-equities.md), [13-risk-and-pnl.md](13-risk-and-pnl.md), [16-portfolio-construction-and-backtesting.md](16-portfolio-construction-and-backtesting.md), [19-financing-repo-and-securities-lending.md](19-financing-repo-and-securities-lending.md), [20-execution-microstructure-and-tca.md](20-execution-microstructure-and-tca.md), and [30-trade-lifecycle-and-operations.md](30-trade-lifecycle-and-operations.md).

## What This Domain Covers
Event-driven investing values securities around a discrete change in corporate state. Merger arbitrage is the canonical case: after an acquisition is announced, the target normally trades below the contractual consideration because completion is uncertain, takes time, and incurs financing and implementation costs.

The analytical task is not merely to calculate the headline spread. A useful system must represent the legal terms, closing conditions, alternative outcomes, event timeline, stock and cash legs, dividends, borrow, funding, currency, and information available at each historical timestamp. The result is a scenario distribution whose probabilities and values change when a vote, regulatory decision, financing condition, court ruling, or revised offer arrives.

This is an event-state and claims-analysis problem. The same framework extends to tender offers, exchange offers, spin-offs, recapitalizations, liquidations, rights distributions, contested situations, and other corporate actions with path-dependent payoffs.

## Product Taxonomy and Market Structure
The first classification is the form of consideration.

- **Cash merger**: each target share receives a fixed cash amount.
- **Fixed-ratio stock merger**: each target share converts into a fixed number of acquirer shares. The arbitrage position normally buys target and shorts the contractual number of acquirer shares.
- **Fixed-value or collar structure**: the exchange ratio changes with the acquirer price, often between upper and lower thresholds.
- **Mixed consideration**: cash, stock, contingent value rights, loan notes, or other securities are combined.
- **Election and proration deal**: holders choose among alternatives, but aggregate caps may cause the final mix to differ from the election.
- **Tender or exchange offer**: holders tender directly; minimum participation, withdrawal, extension, and proration rules matter.
- **Contested, bumped, or topping-bid situation**: more than one bid or an activist process creates additional branches.

Pre-announcement event strategies seek an event before definitive terms exist. Post-announcement arbitrage underwrites a documented contract. They must not share the same probability model or backtest labels.

Participants include target and acquirer shareholders, arbitrageurs, market makers, lenders of stock, options dealers, legal and regulatory advisers, and sometimes competing bidders. Trading continues while legal milestones occur outside market hours, so event time and market time need separate representations.

## Quoting and Market Conventions
For a cash offer \(C\) and target price \(P_T\), the simple spread is:

$$
\text{Spread} = C-P_T, \qquad
\text{Gross Return} = \frac{C-P_T}{P_T}
$$

An annualized return requires an assumed settlement date:

$$
\text{Annualized Return}
=
\left(\frac{C-\text{costs}}{P_T}\right)^{365/d}-1
$$

where \(d\) is calendar days to cash receipt. This is a scenario metric, not a promised yield. A delayed close can sharply reduce it.

For a fixed-ratio stock deal with exchange ratio \(r\), cash component \(c\), and acquirer price \(P_A\):

$$
\text{Current Consideration}=rP_A+c
$$

The contractual hedge is short \(r\) acquirer shares per target share. A beta or minimum-variance hedge answers a different question and leaves contractual closing exposure. Reports should name the convention.

Quotes must also declare treatment of expected target and acquirer dividends, withholding tax, borrow fee, funding rate, commissions, foreign-exchange conversion, settlement lag, and fractional shares. Deal dates should be stored as ranges or distributions when management only gives a quarter or long-stop date.

## Core Pricing Framework
A merger position is a discounted scenario tree:

$$
V_0 =
\sum_{i=1}^{n} p_i
\frac{V_i + D_i - H_i - K_i}{(1+r_i)^{t_i}}
$$

where \(p_i\) is the probability of scenario \(i\), \(V_i\) its terminal consideration or security value, \(D_i\) dividends received net of dividends owed on hedges, \(H_i\) financing and borrow cost, \(K_i\) transaction and settlement cost, and \(t_i\) time in years. Scenarios should include at least close, break, and delay; material cases may require price bump, revised terms, proration, divestiture, litigation, or competing bid branches.

For a two-state cash deal, ignoring discounting and costs, the market-implied completion probability is:

$$
p_{\text{implied}}=\frac{P_T-B}{C-B}
$$

where \(B\) is the estimated unaffected or break price. This is an inversion of assumptions, not an observable probability. If \(B\) is wrong or embeds a changed market, \(p_{\text{implied}}\) is wrong.

For a fixed-ratio stock merger with cash consideration \(c\), buying one target share and shorting \(r\) acquirer shares creates a net entry cash outlay:

$$
C_0=P_T-rP_A.
$$

On clean completion the received acquirer shares cover the short and the locked convergence amount is

$$
G_{\text{close}}=rP_A+c-P_T=c-C_0.
$$

This is before dividends, borrow, funding, and execution costs; whether short-sale proceeds are available to fund the purchase is an agreement-specific financing question. On failure, both legs remain exposed and may gap in opposite directions. Scenario valuation must therefore forecast both security prices in every branch rather than assume the hedge survives a break.

## Worked Instrument Example
Consider a cash offer of USD 50 per target share. The target trades at USD 46.20, an estimated break value is USD 35.40, expected closing is in 120 days, and expected all-in carry and trading costs are USD 0.20 per share.

The headline spread and annualized convergence return are:

$$
50-46.20=\text{USD }3.80
$$

$$
\left(\frac{49.80}{46.20}\right)^{365/120}-1=25.5\%
$$

The simplified market-implied completion probability is:

$$
\frac{46.20-35.40}{50.00-35.40}=74.0\%
$$

Suppose independent underwriting assigns 82% to completion at USD 50, 6% to a nine-month delayed close worth USD 48.60 after incremental carry, and 12% to a break at USD 35.40. The probability-weighted terminal value is:

$$
0.82(50.00)+0.06(48.60)+0.12(35.40)=48.164
$$

After USD 0.20 base costs, expected PnL is USD 1.764 per share, or 3.82% of entry price. The 12% break branch loses USD 10.80 before costs. A high expected return therefore coexists with severe downside asymmetry. The companion [merger-arbitrage scenario example](examples/merger-arbitrage-scenario.md) makes these assumptions executable.

## Key Risk Measures and Sensitivities
- **Completion probability and break value**: report expected value sensitivity to both; they are usually the dominant model inputs.
- **Time-to-resolution**: track PnL and annualized return under closing-date delays, not only the base date.
- **Deal delta**: sensitivity to acquirer price for stock and collar structures, including changing exchange ratios.
- **Jump-to-break loss**: mark the full scenario loss, gross and net of hedges, at position and portfolio level.
- **Regulatory and legal concentration**: aggregate exposure by regulator, jurisdiction, industry issue, vote date, financing source, and common catalyst.
- **Borrow and funding**: measure fee carry, locate availability, recall or buy-in stress, and collateral requirements.
- **Liquidity and crowding**: compare exit size with ADV, spread, options liquidity, and likely gap behavior.
- **Dividend, FX, and basis risk**: model ex-dates on every leg and the currency in which consideration is paid.

Daily PnL should separate target mark, acquirer hedge, market/sector hedges, probability or scenario revaluation, time carry, dividends, borrow, funding, FX, execution, and residual. “Spread tightening” is not an adequate PnL explain for a multi-leg position.

## Required Data, Curves, Surfaces, and Calibration Objects
The minimum point-in-time model includes:

- security and issuer identifiers for every consideration and hedge leg;
- announced, amended, unaffected, vote, regulatory, long-stop, expected-close, and settlement dates;
- exchange ratios, collars, elections, proration, dividends, CVR terms, termination fees, financing conditions, and material closing conditions;
- official filings, court and regulator documents, shareholder communications, and a versioned analyst interpretation;
- raw prices, FX, volume, volatility surfaces, borrow availability and fees, funding curves, dividends, and corporate actions;
- scenario probabilities, terminal values, rationale, owner, approval state, and `known_at` timestamp.

A useful data contract separates `deal_master`, versioned `deal_terms`, immutable `event_log`, `scenario_set`, `security_leg`, and `position_snapshot`. Every record should carry both an effective business time and a system knowledge time. That bitemporal distinction prevents a backtest from using a later amendment or final closing date.

## Numerical and Implementation Approaches
Represent the lifecycle as a state machine: rumoured, announced, definitive agreement, filed, reviewing, approved, voted, closing, closed, terminated, or withdrawn. Store events rather than overwriting the latest status, and derive state as of a requested timestamp.

Use a scenario engine rather than embedding probabilities in spreadsheets. Each scenario should provide a resolution date and terminal value for every leg. The engine can then compute expected value, quantiles, stress loss, carry, and sensitivities consistently. For collars and complex elections, evaluate contractual payoff functions directly across an acquirer-price grid. Monte Carlo is useful only when the dependence between time, acquirer price, financing, and deal outcome is material and defensible.

Document extraction can propose terms, but high-impact fields require source-page lineage and review. A one-character error in an exchange ratio or collar threshold can reverse a hedge.

Backtests must reconstruct the investable universe, event state, terms, borrow, prices, and consensus closing date as known at each decision time. Train and test by deal, not by daily row, because daily observations from one transaction are not independent.

## Production Pitfalls and Sanity Checks
- Treating the headline price as cash-equivalent when consideration includes stock, rights, elections, or contingent value.
- Using the final close date, final terms, or later break reason in historical features.
- Omitting target or acquirer dividends from the spread and hedge ledger.
- Assuming an announced deal has a stable break price through market and fundamental changes.
- Applying the contractual stock hedge to a collar without recalculating the exchange ratio.
- Annualizing a short-dated spread without displaying absolute downside and delay cases.
- Counting a locate as durable borrow, or using the latest borrow fee throughout history.
- Leaving stale positions live after a tender, proration, ticker change, or share conversion.

Minimum controls include consideration recomputation from raw terms, scenario probabilities summing to one, dates ordered consistently, stock hedge quantities reconciling to exchange terms, PnL reconciling to leg-level ledgers, and a no-look-ahead test on every point-in-time field. Prices above stated consideration or implied probabilities outside \([0,1]\) should be investigated, not silently clipped; they can signal a competing bid, dividend, optionality, bad terms, or bad data.

## Illustrative Code
```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Scenario:
    name: str
    probability: float
    terminal_value: float
    costs: float = 0.0


def expected_pnl(entry_price: float, scenarios: list[Scenario]) -> float:
    probability = sum(s.probability for s in scenarios)
    if abs(probability - 1.0) > 1e-10:
        raise ValueError("scenario probabilities must sum to one")
    expected_terminal = sum(
        s.probability * (s.terminal_value - s.costs) for s in scenarios
    )
    return expected_terminal - entry_price


def implied_completion_probability(
    market_price: float, close_value: float, break_value: float
) -> float:
    if close_value == break_value:
        raise ValueError("close and break values must differ")
    return (market_price - break_value) / (close_value - break_value)
```

## References and Further Reading
- U.S. Securities and Exchange Commission. Regulation M-A, Schedules TO and 14D-9, merger proxy statements, and registration statements.
- U.S. Department of Justice and Federal Trade Commission. *Merger Guidelines* and Hart-Scott-Rodino premerger notification materials.
- European Commission. EU merger-control procedures and published case decisions.
- DePamphilis. *Mergers, Acquisitions, and Other Restructuring Activities*.
- Gaughan. *Mergers, Acquisitions, and Corporate Restructurings*.
- Primary merger agreements, tender documents, proxy statements, court opinions, and regulator decisions for the transaction being modelled.
- [Trade Lifecycle and Operations](30-trade-lifecycle-and-operations.md) for event-state controls and [Financing, Repo, and Securities Lending](19-financing-repo-and-securities-lending.md) for short-stock economics.
