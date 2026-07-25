# Private Credit, Distressed, and Real-Estate Credit

Related chapters: [05-fixed-income.md](05-fixed-income.md), [07-credit.md](07-credit.md), [13-risk-and-pnl.md](13-risk-and-pnl.md), [19-financing-repo-and-securities-lending.md](19-financing-repo-and-securities-lending.md), [22-model-governance-and-ipv.md](22-model-governance-and-ipv.md), [24-structured-credit-and-securitization.md](24-structured-credit-and-securitization.md), [30-trade-lifecycle-and-operations.md](30-trade-lifecycle-and-operations.md), and [34-capital-structure-relative-value.md](34-capital-structure-relative-value.md).

## What This Domain Covers
Private and distressed credit values cashflows dependent on borrower performance, documents, collateral, control rights, and negotiation. Real-estate credit adds property cashflows, leases, appraisals, and mortgage structures.

Private loans may have no reliable daily price. Work starts with underwriting and continues through covenant monitoring, amendments, draws, prepayments, valuation, default, restructuring, and recovery. Model definitions must match executed documents and point-in-time inputs.

Implementation requires document-aware reference data, normalized financials, covenant calculators, cashflow engines, property and rent-roll models, scenario waterfalls, valuation controls, and accounting for funded and unfunded exposure.

## Product Taxonomy and Market Structure
Corporate private credit includes revolvers, delayed-draw, first-lien, unitranche, second-lien, mezzanine, payment-in-kind, preferred, bridge, and asset-based facilities. Tranches can have distinct spread, floor, amortization, maturity, commitment, and seniority.

Distressed credit includes stressed loans, defaulted claims, rescue and debtor-in-possession financing, exit facilities, fulcrum securities, trade claims, and reorganization securities. Purchase price, allowed claim, priority, collateral, timing, and plan consideration often matter more than yield.

Real-estate credit includes senior mortgages, construction and bridge loans, mezzanine loans, B-notes, preferred equity, and warehouses. Securitized exposures add pooling, waterfalls, servicing, and control-party mechanics covered in [24-structured-credit-and-securitization.md](24-structured-credit-and-securitization.md).

Loans may be bilateral, clubbed, or syndicated; an agent maintains lender records and distributes notices and cash. Transfers may require consent and settle by assignment or participation. Workouts add sponsors, advisers, courts, servicers, and intercreditor parties.

## Quoting and Market Conventions
- Loans quote as a percentage of par or commitment and usually pay a floating benchmark plus spread, subject to a floor.
- Original-issue discount, upfront fee, unused commitment fee, exit fee, prepayment premium, and call protection must be separate dated cashflows.
- Cash interest and PIK interest are different: PIK increases principal and compounds according to the agreement.
- Day count is often ACT/360 for floating-rate loans, but the executed agreement controls. Reset dates, observation conventions, business-day adjustment, and fallback language matter.
- Distressed claims commonly quote price as a percentage of allowed face. Yield can be misleading when timing and form of recovery are uncertain.
- Real-estate metrics require defined numerators and denominators. Net operating income (NOI), net cash flow, appraised value, stabilized value, debt service, and loan balance are not interchangeable.
- Commitments, funded principal, face owned, settlement receivable, and unfunded obligations must be tracked separately.

Underwriting measures are:

$$
\text{net leverage}=\frac{\text{debt}-\text{eligible cash}}{\text{adjusted EBITDA}},
$$

$$
\text{interest coverage}=\frac{\text{adjusted EBITDA}}{\text{cash interest}},
$$

$$
\text{LTV}=\frac{\text{loan balance}}{\text{property value}},
\quad
\text{DSCR}=\frac{\text{NOI or NCF}}{\text{debt service}},
\quad
\text{debt yield}=\frac{\text{NOI}}{\text{loan balance}}.
$$

“Adjusted” is not harmless wording. Permitted add-backs, synergies, unrestricted subsidiaries, cash netting caps, annualization, and cure rights come from the agreement.

## Core Pricing Framework
For a floating-rate loan, the cash coupon rate during period \(t\) is often:

$$
c_t=\max(I_t,f)+s,
$$

where \(I_t\) is the benchmark fixing, \(f\) the contractual floor, and \(s\) the spread. Expected value across scenarios is:

$$
V=\sum_k p_k\left[
\sum_t DF_t\,CF_{t,k}
+DF_{\tau_k}\,R_k
\right],
$$

where \(CF_{t,k}\) includes cash interest, PIK, amortization, fees, draws, and prepayments; \(\tau_k\) is a resolution time; and \(R_k\) is recovery or exit consideration. Scenario probabilities and discount rates should not both absorb the same risk premium without a documented convention.

Triangulate illiquid marks from contractual cashflows, comparable spreads, default/recovery scenarios, transactions, and enterprise or collateral value. Report valuation uncertainty and independent-price-verification controls.

### Covenant Headroom

For a maximum leverage covenant:

$$
\text{headroom}_{x}
=L_{\max}-L_{\text{actual}},
$$

and debt-capacity headroom, holding the agreement-defined EBITDA and cash constant, is:

$$
\text{headroom}_{\$}
=L_{\max}\times EBITDA-(debt-\text{eligible cash}).
$$

For minimum coverage, headroom is actual minus required coverage. First determine whether the test is active, its entities and adjustments, cure rights, and reporting period.

### Distressed Recovery and Position PnL

Recovery follows the claim and collateral waterfall described in [34-capital-structure-relative-value.md](34-capital-structure-relative-value.md). Expected recovery value for purchased face \(F\) is:

$$
EV_{\text{recovery}}=\sum_k p_k F r_k DF(\tau_k),
$$

where \(r_k\) includes both cash and the fair value of securities received under a plan.

Total loan PnL should reconcile:

$$
\text{PnL}=
\text{cash interest}
+\text{PIK accretion}
+\text{fee/OID accretion}
+\text{mark change}
+\text{FX}
-\text{funding}
-\text{hedge cost}
-\text{credit loss}
+\text{trade/lifecycle effects}.
$$

Credit-index, CDS, equity, rate, or macro hedges introduce basis risk. They do not transfer covenants, amendment risk, unfunded obligations, or exact recovery.

## Worked Instrument Example
### Corporate Covenant Stress

A borrower reports USD 50m of agreement-defined EBITDA, USD 225m of debt, and USD 15m of eligible cash. Its maximum net-leverage covenant is 5.25x.

$$
\text{net leverage}=\frac{225-15}{50}=4.20x.
$$

Headroom is 1.05x, or:

$$
5.25\times50-(225-15)=USD\ 52.5m.
$$

If EBITDA falls 25% to USD 37.5m with debt and cash unchanged, leverage becomes 5.60x and breaches by 0.35x. Before assuming acceleration, check cures, test dates, grace periods, waivers, and add-backs. A reusable calculator appears in [examples/private-credit-covenant-headroom.md](examples/private-credit-covenant-headroom.md).

### Real-Estate Refinance Stress

Consider an interest-only property loan with USD 120m balance, USD 12m annual NOI, 8% interest rate, and property value based on a 7.5% capitalization rate:

$$
\text{value}=\frac{12m}{7.5\%}=USD\ 160m.
$$

Initial LTV is 75%, DSCR is \(12/9.6=1.25x\), and debt yield is 10%.

Now reduce NOI by 15% to USD 10.2m and increase the capitalization rate to 9%. Implied value falls to USD 113.3m, LTV rises to 105.9%, and DSCR falls to 1.06x. Debt yield falls to 8.5%. The loan may remain current while being unable to refinance at maturity, illustrating why payment status alone is a weak risk signal.

## Key Risk Measures and Sensitivities
- Probability of default, loss given default, expected loss, recovery timing, and migration risk.
- Gross/net leverage, fixed-charge and interest coverage, liquidity runway, free cash flow, and covenant headroom.
- Funded exposure, unfunded commitment, utilization, future draws, and concentration by borrower, sponsor, sector, geography, and vintage.
- Spread duration, benchmark-rate sensitivity, floor value, prepayment/call risk, extension risk, and funding cost.
- Enterprise-value, EBITDA multiple, collateral-value, and waterfall sensitivity.
- Mark uncertainty, comparable dispersion, stale-price age, and liquidation horizon.
- For real estate: occupancy, rent collections, lease rollover, tenant concentration, NOI, cap rate, appraisal age, LTV, DSCR, debt yield, refinance gap, construction cost, and interest-reserve depletion.
- Workout scenarios: amendment, covenant cure, payment default, acceleration, priming debt, asset sale, liquidation, reorganization, and debt-for-equity exchange.

Scenario reporting should show cash needs as well as present-value loss. A delayed-draw facility can require additional funding precisely when borrower credit and market liquidity deteriorate.

## Required Data, Curves, Surfaces, and Calibration Objects
Corporate data includes entity and guarantor maps; tranche terms; commitment, funding, amortization, benchmark, floor, spread, fees, PIK, calls, collateral, liens, covenants, amendments, and notices. Preserve reported financials, agreement adjustments, forecasts, lender cases, and lineage.

Real-estate data includes ownership, property attributes, rent rolls, leases, tenants, occupancy, concessions, operating statements, capital expenditure, appraisals, reports, reserves, construction budgets and draws, and intercreditor terms.

Calibration includes rate and funding curves, comparable marks, default and recovery data, valuation multiples, cap rates, rent and vacancy, sale costs, recovery timing, and scenario probabilities.

A practical schema separates:

- `borrower`, `legal_entity`, `guarantee`, `facility`, `tranche`, `commitment`, and `position`.
- `rate_term`, `fee_term`, `amortization_event`, `draw`, `payment`, `notice`, and `amendment`.
- `covenant_definition`, `covenant_component`, `test_period`, `reported_value`, `adjustment`, `cure`, and `test_result`.
- `property`, `lease`, `tenant`, `rent_roll_snapshot`, `operating_statement`, `appraisal`, `reserve`, and `construction_draw`.
- `valuation_case`, `cashflow`, `recovery_waterfall`, `plan_security`, and `scenario_result`.

Items need effective dates, knowledge timestamps, currency, units, source, and approval. Revisions and amendments create versions rather than overwrite history.

## Numerical and Implementation Approaches
- Build contractual cashflows before default models. Test floors, resets, PIK, amortization, fees, draws, and prepayments independently.
- Implement covenant formulas as versioned expression graphs with named components and a trace showing every source value and adjustment.
- Maintain base, downside, and severe borrower models with linked income statement, balance sheet, cash flow, debt schedule, and liquidity runway.
- Use scenario trees for amendments, prepayment, default, recovery form, and resolution timing. Use Monte Carlo only when the added distributional detail can be calibrated and explained.
- Value real-estate collateral using both direct capitalization and discounted cash flow, then stress NOI, cap rate, lease rollover, concessions, capital expenditure, and sale timing.
- Compute IRR or XIRR from dated investor cashflows, but pair it with multiple on invested capital, expected loss, downside recovery, and time-to-resolution.
- Mark illiquid assets with explicit hierarchy, comparable selection, valuation range, override approval, and model-version lineage.
- Reconcile positions to agent notices and cash daily; reconcile covenant inputs to signed financial certificates and source statements each test period.

## Production Pitfalls and Sanity Checks
- Using management EBITDA rather than the agreement-defined covenant measure.
- Accepting add-backs without caps, sunsets, or supporting detail.
- Missing springing covenants, restricted-group changes, builder baskets, cure rights, holidays, or amendment versions.
- Applying the benchmark floor to benchmark-plus-spread instead of to the benchmark.
- Treating PIK as cash income or failing to compound it into principal.
- Calculating interest on commitment rather than funded principal, while omitting the separate unused fee.
- Losing delayed-draw and revolving unfunded exposure from risk reports.
- Using today's financial revision, rent roll, appraisal, or amendment in a historical valuation.
- Treating stale broker indications as transactions or marking to one favorable comparable.
- Confusing property NOI with loan-document net cash flow.
- Mixing interest-only and amortizing debt service in DSCR.
- Applying a cap rate as a whole percentage rather than a decimal, or ignoring appraisal and sale dates.
- Assuming current payment means refinance viability.
- Applying collateral value at one entity to debt at another without guarantees or liens.
- Ignoring default interest, professional fees, adequate-protection payments, settlement delay, and non-cash recovery.

Sanity checks should confirm principal roll-forward, cashflow conservation, covenant numerator and denominator lineage, no recovery above allowed claim without explicit post-petition items, LTV and debt-yield denominator consistency, and portfolio PnL equal to the sum of position and lifecycle components.

## Illustrative Code
```python
def floating_coupon(index_rate: float, floor: float, spread: float) -> float:
    return max(index_rate, floor) + spread


def leverage_headroom(
    debt: float,
    eligible_cash: float,
    covenant_ebitda: float,
    maximum_leverage: float,
) -> tuple[float, float]:
    if covenant_ebitda <= 0.0:
        raise ValueError("covenant EBITDA must be positive")
    net_debt = debt - eligible_cash
    actual = net_debt / covenant_ebitda
    return maximum_leverage - actual, maximum_leverage * covenant_ebitda - net_debt


def property_metrics(
    loan_balance: float,
    noi: float,
    property_value: float,
    annual_debt_service: float,
) -> dict[str, float]:
    return {
        "ltv": loan_balance / property_value,
        "dscr": noi / annual_debt_service,
        "debt_yield": noi / loan_balance,
    }
```

Production code must use document-defined metrics, dated cashflows, currency-aware amounts, and explicit missing-data handling.

## References and Further Reading
- Loan Syndications and Trading Association. *The Complete Credit Agreement Guide* and settlement guidance.
- Loan Market Association. Recommended forms, secondary trading documentation, and market guides.
- Altman and Hotchkiss. *Corporate Financial Distress, Restructuring, and Bankruptcy*.
- Moyer. *Distressed Debt Analysis: Strategies for Speculative Investors*.
- Geltner, Miller, Clayton, and Eichholtz. *Commercial Real Estate Analysis and Investments*.
- Commercial Real Estate Finance Council. Investor Reporting Package and industry guidance.
- The relevant executed credit agreement, security and guarantee documents, intercreditor agreement, compliance certificates, appraisal, servicing reports, and court filings.
