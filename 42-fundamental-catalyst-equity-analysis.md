# Fundamental Catalyst Equity Analysis

Related chapters: [03-equities.md](03-equities.md), [11-market-data.md](11-market-data.md), [13-risk-and-pnl.md](13-risk-and-pnl.md), [16-portfolio-construction-and-backtesting.md](16-portfolio-construction-and-backtesting.md), [20-execution-microstructure-and-tca.md](20-execution-microstructure-and-tca.md), [29-etfs-index-products-and-rebalances.md](29-etfs-index-products-and-rebalances.md), and [33-event-driven-and-merger-arbitrage.md](33-event-driven-and-merger-arbitrage.md).

## What This Domain Covers
Fundamental catalyst analysis connects a change in business expectations to financial statements, valuation, and a tradeable security. The catalyst may be an earnings release, guidance update, product launch, contract award, price change, cost programme, investor presentation, regulatory decision, capital return, refinancing, management transition, or sector data release.

The quant-development problem is to make the reasoning reproducible. Raw filings, estimates, transcripts, prices, share counts, and sector indicators arrive on different clocks. Reported numbers may later be restated. “Adjusted” metrics use definitions that change. A robust system must reconstruct exactly what was known before the catalyst, bridge the new information into forecasts, update enterprise and equity value, and attribute subsequent PnL without hindsight.

The output should expose assumptions, scenarios, uncertainty, liquidity, and the difference between a good business result and one already priced into the security.

## Product Taxonomy and Market Structure
Catalysts can be grouped by the part of the forecast they change:

- **Demand and revenue**: units, price, mix, market share, backlog, churn, utilization, store or customer additions, and foreign exchange.
- **Margins and costs**: input prices, productivity, labour, freight, restructuring, fixed-cost absorption, and operating leverage.
- **Capital intensity and cash conversion**: working capital, capital expenditure, depreciation, tax, and cash restructuring charges.
- **Capital structure**: debt issuance or repayment, refinancing, buybacks, dividends, equity compensation, and convertible dilution.
- **Strategic or regulatory state**: approvals, litigation, product milestones, disposals, spin-offs, and management or governance changes.
- **Scheduled information events**: earnings, guidance, investor days, industry statistics, index changes, and lock-up expiries.

The timing hierarchy matters: a release, filed statement, prepared remarks, and answers on a later call are distinct information states.

Sector models need different operating units. Banks emphasize net interest income, credit losses, capital, and tangible book value; insurers use underwriting and reserve metrics; subscription businesses use recurring revenue, retention, and customer economics; commodity producers use volume, realized price, cost curves, and reserves. A generic schema should support sector extensions rather than force every issuer into one KPI list.

## Quoting and Market Conventions
Financial data must declare its basis.

- Fiscal period, period end, filing or release time, source currency, scale, and restatement version.
- Reported accounting basis versus management-adjusted basis, with an explicit reconciliation.
- Basic versus diluted shares and EPS; actual weighted-average shares versus period-end shares.
- Trailing-twelve-month (TTM), next-twelve-month (NTM), fiscal-year, and calendar-year values.
- Actual, company guidance, individual analyst estimate, consensus snapshot, and internal forecast.
- Reported growth, organic growth, constant-currency growth, and acquisition contribution using the issuer's stated definitions.
- Share, ADR, or depositary receipt ratio; split and corporate-action adjustment policy.

Consensus is a timestamped distribution. Store contributor count, mean, median, range, dispersion, and constituents where licensed. A surprise such as:

```math
\text{Surprise}=\frac{\text{Actual}-\text{Consensus}}{|\text{Consensus}|}
```

is unstable near zero or across a sign change. Then report an absolute difference and business-scale denominator. Preserve guidance ranges rather than silently substituting their midpoint.

Enterprise value conventions also need labels:

```math
EV=\text{Equity Value}+\text{Debt}+\text{Preferred}
+\text{Non-controlling Interest}-\text{Cash}
```

Lease liabilities, pensions, associates, restricted cash, and financial subsidiaries may require adjustments. Comparable-company multiples are meaningless if numerator and denominator use inconsistent definitions.

## Core Pricing Framework
Start with an operating model. Revenue can be decomposed by segment $j$:

```math
R_t=\sum_j Q_{j,t}P_{j,t}FX_{j,t}
```

The income and cash-flow bridge is:

```math
\text{EBIT}=R-\text{COGS}-\text{Operating Expenses}
```

```math
\text{EPS}
=
\frac{(\text{EBIT}-\text{Net Interest}+\text{Other Pretax}) (1-\tau)}
{\text{Diluted Weighted-Average Shares}}
```

```math
\text{Unlevered FCF}
=\text{EBIT}(1-\tau)+D\&A-\text{Capex}-\Delta NWC
```

A discounted cash-flow cross-check is:

```math
EV_0=\sum_{t=1}^{T}\frac{FCF_t}{(1+WACC)^t}
+\frac{TV_T}{(1+WACC)^T}
```

Equity value follows by subtracting net debt and other senior claims and adding non-operating assets. Per-share value must use a scenario-consistent diluted share count.

For a multiple framework $P=M E$, the exact one-period price bridge is:

```math
\Delta P
=M_0\Delta E+E_0\Delta M+\Delta E\Delta M
```

where $E$ is forward EPS and $M$ the forward P/E multiple. This separates estimate revision from re-rating and their interaction. Catalysts often improve earnings while reducing the multiple, or vice versa.

Valuation should be scenario based:

```math
\mathbb{E}[P_T]=
\sum_i p_i
\left(
\text{Equity Value from operating scenario }i
\right)
```

Each scenario links operating assumptions, statements, capital structure, valuation, probability, and horizon.

## Worked Instrument Example
Suppose pre-release consensus expects quarterly revenue of USD 1,000m, gross margin of 40%, operating expense of USD 250m, net interest expense of USD 20m, a 25% tax rate, and 100m diluted shares.

Consensus EBIT, net income, and EPS are:

```math
\text{EBIT}=1{,}000(40\%)-250=150
```

```math
\text{Net Income}=(150-20)(1-25\%)=97.5
```

```math
\text{EPS}=97.5/100=\text{USD }0.975
```

The company reports revenue of USD 1,060m, gross margin of 41%, operating expense of USD 265m, the same interest and tax assumptions, and 102m diluted shares. Reported gross profit is USD 434.6m, EBIT is USD 169.6m, net income is USD 112.2m, and EPS is USD 1.10: a 12.8% beat.

The operating bridge is more informative than the beat:

| Driver | EBIT effect |
| --- | ---: |
| USD 60m revenue increase at prior 40% margin | +USD 24.0m |
| 1 percentage point gross-margin increase on reported revenue | +USD 10.6m |
| USD 15m operating-expense increase | -USD 15.0m |
| Total EBIT change | +USD 19.6m |

At the prior 100m-share denominator, the net-income increase would add USD 0.147 of EPS. Dilution to 102m shares subtracts USD 0.022, leaving the observed USD 0.125 increase.

Assume NTM EPS guidance moves from USD 4.00 to USD 4.30 and the pre-event share price is USD 60, or 15 times forward EPS. Holding the multiple constant gives USD 64.50, while a de-rating to 14.5 times gives USD 62.35. The earnings revision is not the same thing as the expected price move. The [catalyst earnings bridge example](examples/catalyst-equity-earnings-bridge.md) reproduces these calculations.

## Key Risk Measures and Sensitivities
- **Estimate sensitivity** to volume, price, mix, FX, margin, tax, working capital, capex, and diluted shares.
- **Valuation sensitivity** to WACC, terminal growth, target multiple, net debt, and non-operating claims.
- **Scenario gap risk** around releases, guidance, rulings, and other discontinuous events.
- **Accounting-quality risk** from accruals, capitalization policy, reserves, one-offs, revenue recognition, related parties, or weak cash conversion.
- **Balance-sheet and refinancing risk**, including covenants, maturities, liquidity, variable rates, and collateral.
- **Factor and crowding risk**: beta, sector, style, index, options-implied move, short interest, borrow fee, and positioning proxies.
- **Liquidity and implementation risk**: ADV, spread, depth, auction behavior, borrow, and expected market impact.

PnL attribution can combine market, sector and factor returns with issuer residual, estimate revision, multiple change, dividend, FX, borrow, financing, and execution. Do not label the entire residual “fundamental”; event timing and model error should remain visible.

## Required Data, Curves, Surfaces, and Calibration Objects
Required sources include point-in-time financial statements and footnotes, segment and KPI disclosures, guidance history, estimate snapshots, capital structure, prices and corporate actions, transcripts or prepared remarks where licensed, sector data, rates, credit spreads, FX, options-implied distributions, borrow, and liquidity.

A durable fact record should include:

`issuer_id`, `metric_id`, `segment_id`, `period_start`, `period_end`, `fiscal_label`, `value`, `unit`, `currency`, `accounting_basis`, `filed_at`, `known_at`, `restatement_version`, `source_document`, and `source_locator`.

Keep separate tables for `reported_fact`, `estimate_snapshot`, `guidance_range`, `operating_kpi`, `capital_structure_snapshot`, `valuation_assumption`, and `event_log`. Never overwrite an originally filed value with a restatement. Store the new version and its knowledge time.

Forecast objects should retain formulas and dependencies. Each run needs input snapshot, code and definition versions, scenario set, and output lineage.

## Numerical and Implementation Approaches
Build a normalized three-statement model with sector-specific extensions. Map filing tags and issuer labels into a controlled metric taxonomy, but retain raw tags and source facts because taxonomy mappings change. Validate the accounting identities before calculating valuation.

Calendarize fiscal estimates into NTM measures using explicit weights for completed and forecast quarters. Do not splice a later estimate into an earlier historical snapshot. For each catalyst, freeze a pre-event snapshot immediately before public release and a sequence of post-event snapshots as new information arrives.

Implement bridges as dependency graphs: unit and price to revenue, revenue and cost drivers to profit, profit and balance-sheet drivers to cash flow, then cash flow and capital structure to equity value. This makes sensitivities explainable and avoids hard-coded spreadsheet plugs.

Use scenario matrices for discrete outcomes and sensitivities for continuous inputs. DCF, multiples, and sum-of-the-parts should share an enterprise-to-equity bridge. Backtests need delisted issuers, original filings, historical estimate vintages, release timestamps, tradeable prices, and costs.

## Production Pitfalls and Sanity Checks
- Using restated history or the latest consensus in a point-in-time backtest.
- Comparing reported adjusted EPS with consensus GAAP EPS, or vice versa.
- Mixing fiscal and calendar periods or comparing a 53-week year with a 52-week year.
- Losing currency, scale, sign, ADR ratio, or split adjustments during ingestion.
- Using period-end shares for EPS instead of diluted weighted-average shares.
- Treating stock compensation as both an expense and a dilution adjustment inconsistently.
- Calling acquisition revenue “organic” or double-counting FX and price/mix effects.
- Calculating EV with current share price and stale debt or cash.
- Applying industrial-company EV/EBITDA logic mechanically to banks or insurers.
- Converting guidance range midpoints without preserving the stated range and definition.

Minimum checks include assets equalling liabilities plus equity, cash-flow change reconciling to balance-sheet cash, annual values reconciling to quarters where definitions permit, margins staying dimensionally consistent, EPS reconciling to attributable income and diluted shares, and the enterprise-to-equity bridge reproducing market capitalization at the current price. Flag large unexplained “other” bridge items, tag-mapping changes, negative denominators, stale estimates, and timestamps after the decision cutoff.

## Illustrative Code
```python
from dataclasses import dataclass


@dataclass(frozen=True)
class EarningsCase:
    revenue: float
    gross_margin: float
    operating_expense: float
    net_interest: float
    tax_rate: float
    diluted_shares: float

    def eps(self) -> float:
        ebit = self.revenue * self.gross_margin - self.operating_expense
        net_income = (ebit - self.net_interest) * (1.0 - self.tax_rate)
        return net_income / self.diluted_shares


def forward_price(forward_eps: float, forward_pe: float) -> float:
    return forward_eps * forward_pe


consensus = EarningsCase(1_000.0, 0.40, 250.0, 20.0, 0.25, 100.0)
reported = EarningsCase(1_060.0, 0.41, 265.0, 20.0, 0.25, 102.0)
eps_surprise = reported.eps() / consensus.eps() - 1.0
```

## References and Further Reading
- U.S. Securities and Exchange Commission. EDGAR, Inline XBRL data, Regulation S-K, Regulation S-X, and Regulation FD.
- Financial Accounting Standards Board. *Accounting Standards Codification*; International Accounting Standards Board. *IFRS Accounting Standards*.
- CFA Institute. *Equity Asset Valuation*.
- Penman. *Financial Statement Analysis and Security Valuation*.
- Koller, Goedhart, and Wessels. *Valuation: Measuring and Managing the Value of Companies*.
- Damodaran. *Investment Valuation*.
- Primary annual and interim reports, earnings releases, proxy statements, debt documents, and regulator filings for the issuer being modelled.
- [Cash Equities and Equity Analytics](03-equities.md) for security-ledger foundations and [Portfolio Construction and Backtesting](16-portfolio-construction-and-backtesting.md) for point-in-time research controls.
