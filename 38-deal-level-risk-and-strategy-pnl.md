# Deal-Level Risk and Strategy PnL

Related chapters: [12-pricing-architecture.md](12-pricing-architecture.md), [13-risk-and-pnl.md](13-risk-and-pnl.md), [16-portfolio-construction-and-backtesting.md](16-portfolio-construction-and-backtesting.md), [19-financing-repo-and-securities-lending.md](19-financing-repo-and-securities-lending.md), [20-execution-microstructure-and-tca.md](20-execution-microstructure-and-tca.md), [30-trade-lifecycle-and-operations.md](30-trade-lifecycle-and-operations.md), and [44-robust-portfolio-and-research-validation.md](44-robust-portfolio-and-research-validation.md).

## What This Domain Covers
A strategy may combine a core position, market or credit hedges, options, financing, and execution hedges. Deal-level risk groups the legs by economic thesis so payoff, downside, hedge effectiveness, liquidity, and PnL can be assessed together.

Here “deal” means a durable strategy container, not a legal transaction type. It should answer:

- What outcome is the position designed to monetize?
- Which legs are core exposure and which are hedges?
- What can be lost under plausible adverse outcomes and stressed exits?
- Which risk is intentionally retained after hedging?
- Why did the strategy make or lose money today and since inception?
- When should it be resized, reviewed, or closed?

This layer sits between instrument pricing and book risk and must reconcile exactly to both.

## Product Taxonomy and Market Structure
The same data model should support several strategy shapes.

- **Relative value:** long one security and short another security, index, future, swap, or factor basket.
- **Catalyst or event:** positions around a scheduled or conditional outcome, often with discrete success, delay, and break states.
- **Capital structure:** related equity, bond, loan, credit derivative, preferred, or convertible claims.
- **Volatility:** option or variance legs plus dynamic spot hedges.
- **Carry and financing:** cash instruments with repo, securities lending, FX, or rate hedges.
- **Portfolio overlay:** a hedge allocated to several strategies or a book-wide tail hedge.

Distinguish the hierarchy explicitly:

- an **execution** is a fill;
- a **trade** is a booked contract or tax lot;
- a **position** is the net holding in an instrument and account;
- a **leg** is a position allocation with an economic role;
- a **strategy** is a set of legs, scenarios, limits, and a thesis version;
- a **book** aggregates strategies plus any deliberately unallocated exposure.

A trade may not silently belong 100% to two strategies. Shared hedges require an allocation rule whose fractions sum to one, or they remain at book level.

## Quoting and Market Conventions
- Store signed quantity, contract multiplier, price unit, accrued interest, and FX conversion separately. Signed market value is not the same as delta-equivalent exposure.
- Declare whether loss is positive or negative. This chapter uses signed PnL, where losses are negative, and positive loss-limit utilization.
- Report gross/net market value, delta-equivalent and factor exposure, and committed capital separately.
- State whether risk is current, entry-date, or target risk and whether PnL is daily, month-to-date, or inception-to-date.
- Use one official valuation timestamp and base currency for aggregation. Keep local-currency PnL and FX translation as separate explain rows.
- Financing, borrow, dividends, accrual, premium, and settlement cash are economic PnL components.
- Scenario shocks need units: relative spot move, absolute yield or spread basis points, volatility points, recovery rate, FX percentage, or named state transition.
- Define liquidity horizons and exit-price rules. A mark-to-mid scenario and a stressed executable-exit scenario are different controls.

## Core Pricing Framework
For strategy $d$ with legs $i$, its marked value in base currency $b$ is:

$$
V_d(t)=
\sum_{i\in d} a_{i,d}\,q_i m_i P_i(t)X_{c_i\rightarrow b}(t)
+ C_d(t)
$$

where $a_{i,d}$ is the allocation fraction, $q_i$ is signed quantity, $m_i$ is the multiplier, $P_i$ is clean or dirty price under a documented convention, $X$ is the FX conversion, and $C_d$ is the strategy cash/accrual ledger. The allocation fractions for each trade must reconcile across all strategies.

Economic PnL is the change in marked positions plus cash, adjusted for external transfers:

$$
\operatorname{PnL}_{d,t}
=
\left[V_d(t)-V_d(t-1)\right]
-\operatorname{ExternalFlow}_{d,t}
$$

The cash ledger carries executions and lifecycle flows to prevent double counting. The explain decomposes exact PnL:

$$
\operatorname{PnL}
=\operatorname{Market}
+\operatorname{Carry}
+\operatorname{Financing}
+\operatorname{TradingCost}
+\operatorname{Lifecycle}
+\operatorname{ModelDataChange}
+\operatorname{Residual}
$$

For scenario $s$, full-revaluation PnL is:

$$
\Delta V_d^{(s)}
=
\sum_{i\in d}
\left[V_i(x+\Delta x_s,\tau_s)-V_i(x,\tau_0)\right]
+CF_d^{(s)}-U_d^{(s)}
$$

where $CF$ contains scenario cash flows and $U$ is the estimated unwind cost, including spread, impact, borrow close-out, and legging. Define reasonable-worst-case loss and utilization as:

$$
L_{\text{RWC}}=\max_s\left(0,-\Delta V_d^{(s)}\right),
\qquad
u=\frac{L_{\text{RWC}}}{L_{\text{budget}}}
$$

The scenario set, not the formula, determines whether this control is credible. It must include thesis failure, delay, market-factor shocks, liquidity deterioration, hedge failure, and relevant nonlinear interactions.

Factor neutrality is an independent diagnostic. For an equity strategy:

$$
B_d=\sum_i \left(q_i m_i S_i\Delta_i\right)\beta_i
$$

A small $B_d$ means low estimated linear market-beta exposure at that snapshot. It does not eliminate idiosyncratic gaps, changing beta, basis, gamma, skew, correlation, or liquidity risk.

## Worked Instrument Example
Consider a relative-value strategy:

- long 80,000 shares of an asset at USD 50: USD 4.0m market value;
- estimated asset beta: 1.20;
- short 48,000 shares of a USD 100 index fund: USD -4.8m market value;
- index beta: 1.00.

Initial beta-dollar exposure is:

$$
4.0\text{m}\times1.20-4.8\text{m}\times1.00=0
$$

Now full-revalue named scenarios, including estimated carry and exit cost:

| Scenario | Core-leg PnL | Hedge PnL | Carry/exit | Strategy PnL |
| --- | ---: | ---: | ---: | ---: |
| Thesis succeeds: asset +18%, index +4% | USD 720k | USD -192k | USD -18k | USD 510k |
| Thesis fails: asset -25%, index -8% | USD -1,000k | USD 384k | USD -50k | USD -666k |
| Broad rally, no catalyst: asset +5%, index +8% | USD 200k | USD -384k | USD -20k | USD -204k |
| Gap and illiquidity: asset -40%, index -10% | USD -1,600k | USD 480k | USD -120k | USD -1,240k |

With a USD 750k loss budget, RWC utilization is $1{,}240/750=165.3\%$. The initial size fails the control even though it is beta-neutral. Scaling every leg to 60% gives an approximate stressed loss of USD 744k while preserving initial beta neutrality. In practice, rerun full repricing because fixed fees, option nonlinearities, market impact, and minimum trade sizes do not scale perfectly.

For one ordinary day, suppose the asset rises 1.5%, the index rises 1.0%, and financing plus fees cost USD 3k. At full size, PnL is:

$$
60\text{k}-48\text{k}-3\text{k}=9\text{k}
$$

The first 1.2% of the asset move contributes USD 48k and is offset by the hedge. The remaining 0.3% contributes USD 12k of relative performance; after costs, explained PnL is USD 9k.

## Key Risk Measures and Sensitivities
- RWC loss, budget utilization, expected payoff, and payoff asymmetry by named scenario.
- Delta, beta-dollar, PV01, CS01, vega, gamma, correlation, FX, and cross-gamma by strategy and leg role.
- Gross and net exposure, leverage, concentration, and overlap with other strategies.
- Hedge ratio, hedge drift, realized hedge effectiveness, and basis PnL.
- Liquidity horizon, percentage of daily volume, bid-ask cost, market impact, and stressed unwind cost.
- Financing requirement, margin, borrow rate, recall risk, coupon/dividend cash, and counterparty exposure.
- Daily and inception PnL by core leg, hedge, carry, execution, lifecycle, FX, and unexplained residual.

Controls should combine hard limits with review triggers. Examples include loss-budget breaches, factor exposure outside tolerance, hedge drift, scenario deterioration, event-date changes, borrow becoming hard to source, quote staleness, days-to-exit increases, and unexplained PnL above an absolute and relative threshold.

## Required Data, Curves, Surfaces, and Calibration Objects
A `StrategyDefinition` should contain `strategy_id`, owner, mandate, base currency, inception, expected review/exit dates, thesis version, tags, loss budget, approved scenario set, and risk targets.

Each `StrategyLeg` needs trade and instrument identifiers, allocation fraction, role (`core`, `hedge`, `financing`, or `execution_hedge`), signed quantity, multiplier, account, model, market-data mapping, and effective timestamps. Allocation changes are immutable events, not overwritten fields.

Store versioned:

- positions, executions, cash, corporate actions, coupons, dividends, borrow, funding, and margin;
- official and intraday market snapshots, curves, surfaces, FX, and factor models;
- scenario definitions with shock units, dependencies, valuation time, liquidity rules, and approvals;
- `RiskSnapshot` rows by strategy, leg, risk factor, and scenario;
- `PnLExplain` rows with component, amount, method, market-data versions, and residual status;
- limit records with effective dates, warnings, breach status, acknowledgement, and remediation.

## Numerical and Implementation Approaches
Use one authoritative hierarchy service for book, strategy, leg, and allocation data. Pricing engines should return instrument value and risk; a separate aggregation layer applies allocations and FX. Do not embed mutable strategy ownership inside product pricers.

Run local sensitivities for speed and full revaluation for named outcomes. Scenario definitions should support correlated factor shocks and discrete state changes such as default, cancellation, conversion, exercise, or borrow recall. Cache base valuations, but key caches by complete model and market-data versions.

Maintain a double-entry-style cash and position ledger. Reconcile strategy PnL upward to the book and downward to trades every day. The residual must be calculated, thresholded, and investigated rather than force-allocated.

Pre-trade checks should evaluate the proposed post-trade strategy: loss budget, factor tolerances, liquidity, financing, and concentration. Intraday monitoring should recalculate when a material market move, fill, event update, or data-quality alert occurs.

## Production Pitfalls and Sanity Checks
- Assigning a hedge to several strategies without allocations that reconcile.
- Assuming beta neutrality means limited loss.
- Calculating scenario PnL from standalone Greeks when the instruments have gap or path dependence.
- Omitting spread, impact, borrow close-out, or legging from the loss estimate.
- Comparing current risk with an entry-date limit or stale scenario snapshot.
- Moving a losing leg to a different strategy and rewriting historical attribution.
- Mixing clean bond price, dirty value, accrued cash, and coupon PnL.
- Double counting execution consideration as both position PnL and cash PnL.
- Netting risks across currencies before exposing FX translation.
- Proportionally scaling a nonlinear strategy without rerunning prices and margins.
- Accepting a small aggregate residual that hides large offsetting leg-level residuals.

Daily sanity checks should prove that leg allocations sum correctly, strategy values reconcile to the book, cash and positions roll from executions and lifecycle events, scenario ordering is economically plausible, limits use the current approved version, and PnL explain ties to official PnL within tolerance.

## Illustrative Code
```python
from dataclasses import dataclass


@dataclass(frozen=True)
class ScenarioResult:
    name: str
    pnl: float


def beta_dollar_exposure(
    signed_delta_equivalents: list[float],
    betas: list[float],
) -> float:
    if len(signed_delta_equivalents) != len(betas):
        raise ValueError("exposures and betas must align")
    return sum(exposure * beta for exposure, beta in zip(signed_delta_equivalents, betas))


def loss_budget_metrics(
    scenarios: list[ScenarioResult],
    loss_budget: float,
) -> tuple[float, float, float]:
    if not scenarios or loss_budget <= 0.0:
        raise ValueError("scenarios and a positive loss budget are required")
    rwc_loss = max(0.0, max(-scenario.pnl for scenario in scenarios))
    utilization = rwc_loss / loss_budget
    scale_to_limit = min(1.0, loss_budget / rwc_loss) if rwc_loss else 1.0
    return rwc_loss, utilization, scale_to_limit
```

## References and Further Reading
- Glasserman. *Monte Carlo Methods in Financial Engineering*.
- Jorion. *Value at Risk: The New Benchmark for Managing Financial Risk*.
- Grinold and Kahn. *Active Portfolio Management*.
- Cont and Tankov. *Financial Modelling with Jump Processes*.
- [Minimum capital requirements for market risk](https://www.bis.org/bcbs/publ/d457.htm), especially stress, liquidity-horizon, expected-shortfall, and model-data principles.
- Related material: [13-risk-and-pnl.md](13-risk-and-pnl.md), [30-trade-lifecycle-and-operations.md](30-trade-lifecycle-and-operations.md), and [examples/deal-level-loss-budget.md](examples/deal-level-loss-budget.md).
