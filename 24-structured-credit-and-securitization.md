# Structured Credit and Securitization

Related chapters: [05-fixed-income.md](05-fixed-income.md), [07-credit.md](07-credit.md), [09-cross-asset.md](09-cross-asset.md), [13-risk-and-pnl.md](13-risk-and-pnl.md), and [21-regulatory-margin-capital.md](21-regulatory-margin-capital.md).

## What This Domain Covers
Structured credit turns pools of loans, mortgages, receivables, or bonds into securities with different risk layers.

The basic story is a waterfall. Cash comes in from the asset pool. Fees and senior notes get paid first. Junior notes and equity absorb losses first. The same pool can therefore create a senior tranche with low expected loss and an equity tranche with high leverage to defaults, recoveries, prepayments, and timing.

For a quant developer, this is where fixed-income cashflows, credit modelling, legal structure, and scenario engines meet. The hard part is not one formula. It is modelling collateral performance, tranche priority, triggers, prepayments, defaults, recoveries, and reporting dates consistently.

## Product Taxonomy and Market Structure
Start with the collateral pool and the capital structure.

- ABS: asset-backed securities backed by receivables such as auto loans, credit-card balances, or consumer loans.
- MBS / RMBS: mortgage-backed securities backed by residential mortgages.
- CMBS: commercial mortgage-backed securities.
- CLOs: collateralized loan obligations backed by leveraged loans.
- CDOs and synthetic CDOs: structured exposures to credit portfolios or CDS references.
- Tranches: senior, mezzanine, junior, and equity layers with different loss priority.

## Quoting and Market Conventions
- Bonds may quote price, spread, discount margin, yield, or tranche spread.
- Attachment and detachment points define synthetic tranche loss exposure.
- Prepayment speed, default rate, delinquency, recovery, and loss severity assumptions must be explicit.
- Payment waterfalls, triggers, reinvestment rules, and call features are legal terms, not optional notes.
- Vintage, collateral type, manager, servicer, and deal documentation can matter as much as headline spread.

## Core Pricing Framework
Structured credit pricing starts from collateral cashflows and allocates them through the waterfall.

A simplified tranche loss for portfolio loss $L$ with attachment $A$ and detachment $D$ is:

$$
\text{TrancheLoss}(L) = \min(\max(L - A, 0), D - A)
$$

The tranche loss percentage is:

$$
\frac{\text{TrancheLoss}(L)}{D - A}
$$

Cash products also need interest collections, principal collections, fees, expenses, reserve accounts, triggers, and reinvestment rules. Synthetic tranches need default timing, recovery, discounting, and premium/protection legs.

## Worked Instrument Example: Synthetic Tranche Loss
Assume:
- attachment point: 3%,
- detachment point: 7%,
- portfolio loss: 5%,
- tranche notional: USD 10m.

The tranche absorbs losses above 3% and below 7%:

$$
\text{loss inside tranche} = 5\% - 3\% = 2\%
$$

The tranche width is:

$$
7\% - 3\% = 4\%
$$

So the tranche loss percentage is:

$$
\frac{2\%}{4\%} = 50\%
$$

The dollar loss is:

$$
10{,}000{,}000 \times 50\% = 5{,}000{,}000
$$

## Key Risk Measures and Sensitivities
- Collateral default, delinquency, recovery, and prepayment sensitivity.
- Tranche attachment/detachment leverage.
- Spread duration and discount-margin sensitivity.
- Correlation and default-clustering risk.
- Trigger breach and waterfall path sensitivity.
- Servicer, manager, and documentation risk.

## Required Data, Curves, Surfaces, and Calibration Objects
- Loan or collateral pool characteristics.
- Deal waterfall, tranche priority, fees, triggers, and reinvestment rules.
- Historical performance data by vintage, collateral type, sector, region, and rating.
- Default, recovery, prepayment, and delinquency assumptions.
- Discount curves, spread curves, and market comparables.
- Scenario definitions for stress testing.

## Numerical and Implementation Approaches
- Represent the waterfall explicitly rather than hiding it in spreadsheet-style formulas.
- Separate collateral simulation from tranche allocation.
- Run scenario grids over defaults, recoveries, prepayments, and correlation.
- Keep reporting dates, payment dates, accrual periods, and trigger tests deterministic.
- Validate simple tranche-loss formulas before adding full cashflow complexity.

## Production Pitfalls and Sanity Checks
- Treating tranche rating as a substitute for waterfall modelling.
- Applying one default assumption across collateral vintages with different behavior.
- Ignoring prepayment timing in amortizing pools.
- Misreading attachment/detachment as notional percentages rather than loss layers.
- Missing trigger logic that redirects cashflows in stress.
- Comparing spreads across deals without adjusting for collateral, vintage, structure, and liquidity.

## Illustrative Code
```python
def tranche_loss_percent(portfolio_loss: float, attachment: float, detachment: float) -> float:
    if detachment <= attachment:
        raise ValueError("detachment must exceed attachment")
    tranche_width = detachment - attachment
    loss_in_tranche = min(max(portfolio_loss - attachment, 0.0), tranche_width)
    return loss_in_tranche / tranche_width
```

## References and Further Reading
- Fabozzi. *The Handbook of Fixed Income Securities*
- Tavakoli. *Structured Finance and Collateralized Debt Obligations*
- Deal prospectuses, trustee reports, and rating-agency methodology documents
