# Sources, Claims, And Conventions

A useful quant reference tells you which statements survive a change of contract, model, or date. Start by classifying the claim: a mathematical identity, a model result, a contract rule, an empirical observation, or a legal/accounting requirement. These need different evidence. The register below records the primary sources checked in the documentation review; it is a selected claim register, not a certification of every bibliography item.

## Reviewed Claim Register

| Claim and repository location | Primary authority | Boundary to preserve |
| --- | --- | --- |
| Local option sensitivities and their units in [options](01-options.md) | [OIC Greeks](https://www.optionseducation.org/advancedconcepts/understanding-options-greeks) | The chapter's exact formulas assume European Black-Scholes, continuous carry, and specified shock coordinates; classroom sign intuition is not universal |
| Equity rho and longer-tenor intuition in [options](01-options.md) | [OIC rho](https://www.optionseducation.org/advancedconcepts/rho) | Spot-fixed equity rho differs from forward-fixed Black discount rho; a yield-curve bump needs a curve definition |
| Long-dated equity LEAPS in [options](01-options.md) | [OIC LEAPS](https://www.optionseducation.org/optionsoverview/how-leaps-work) | Equity exercise and settlement follow the actual listed series; the European teaching engine does not implement early exercise |
| Earnings-style repricing in [the worked example](examples/option-greeks-and-earnings-repricing.md) | [OIC earnings questions](https://www.optionseducation.org/news/may-office-hours-faqs) | The example is synthetic; an implied-volatility decline is possible, not guaranteed |
| Independent binomial benchmark in [tree convergence](examples/option-tree-convergence.md) | [Cox, Ross, Rubinstein author paper reprint, 1979](https://bpb-us-w2.wpmucdn.com/u.osu.edu/dist/7/36891/files/2017/07/CRR79-1yy8av8.pdf) | Same constant-parameter European model, independent numerical method; finite-grid error remains |
| Calibration quote residuals in [rates](06-interest-rates.md) and [bootstrap example](examples/curve-bootstrap-and-quote-risk.md) | [QuantLib maintainer's curve guide](https://www.quantlibguide.com/Curve%20bootstrapping.html) | Simplified single-curve examples do not stand in for actual OIS/projection schedules and fixing conventions |
| Physical/cash swaption annuity distinction in [rates options](28-rates-options-caps-floors-swaptions.md) | [QuantLib Black swaption engine source](https://github.com/lballabio/QuantLib/blob/master/ql/pricingengines/swaption/blackswaptionengine.hpp) | Implementation source can evolve; production comparisons must record the deployed QuantLib version or commit and settlement method |
| Shares, weights, and index divisors in [index products](29-etfs-index-products-and-rebalances.md) | [S&P Index Mathematics methodology](https://www.spglobal.com/spdji/en/methodology/article/index-mathematics-methodology/) | Select the actual index methodology and revision date; an illustrative basket is not every index's rulebook |
| Prudent valuation versus booked adjustments in [governance](22-model-governance-and-ipv.md) | [Basel CAP50, published/in force 15 December 2019](https://www.bis.org/committees/bcbs/basel-framework/standard/cap/50/inforce/2019-12-15/published/2019-12-15) | This is a dated framework reference, not a claim about today's local legal implementation or accounting ledger |
| Least squares fitting versus inference in [statistics](23-probability-statistics-and-regression.md) | [NIST linear least squares](https://www.itl.nist.gov/div898/handbook/pmd/section1/pmd141.htm) | Optimization, unbiasedness, and exact inference require separate assumptions |
| Firm-value dilution benchmark in [warrants](36-warrants-rights-pipes-and-spacs.md) | [Olvik and Kangro, 2015, section 3.1](https://arxiv.org/html/1503.05139) | The simple derivation assumes its stated firm-value model; observed stock and firm value are different inputs |
| Correct PIPEs book identity in [warrants and PIPEs](36-warrants-rights-pipes-and-spacs.md) | [Publisher record, second edition 2005](https://www.wiley-vch.de/en?isbn=9781576601945&option=com_eshop&title=PIPEs&view=product) | Dresner and Kim edited the book; the separate publication name is not a substitute book citation |

Sources in this register were consulted for the October 2026 review. Dynamic links identify their owning authority; they do not freeze future page contents. The numerical assertions in the examples are the repository's own checks, not results copied from these sources.

## Apply The Right Version

For a contract convention, record exchange/product/series, exercise style, multiplier, quotation and settlement units, currency, calendar, and effective specification date. For a model result, record assumptions, input units, day count, differentiation coordinates, calibration instruments, tolerances, and implementation version. For a regulatory or accounting requirement, record jurisdiction, scope, reporting date, authoritative text, and effective version. This is especially important for SIMM, capital rules, and local implementation of international frameworks.

For an empirical result, keep the data snapshot, observation and availability timestamps, sampling and cost assumptions, and out-of-sample evidence. A synthetic illustration should say so beside the calculation. A chapter's bibliography directs further reading; it does not by itself establish every sentence as a sourced fact.

## Maintain The Evidence

When changing a consequential formula or rule, update the nearby qualification, the relevant register row, and the executable control together. Do not replace an old dated claim with the word “current” without checking the new source. Store original explanations and lawful references rather than attached source documents. Run the [repository check](QUICKSTART.md) before committing.
