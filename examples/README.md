# Worked Examples

These examples are small by design. They are meant to connect formulas to implementation checks without turning the repository into a full codebase.

## Examples
- [historical-var-es.md](historical-var-es.md) - compute historical VaR and Expected Shortfall from scenario losses.
- [garch-forecast.md](garch-forecast.md) - one-step GARCH(1,1) conditional variance update.
- [regime-switching-probability.md](regime-switching-probability.md) - two-state Markov regime probability update.
- [hmm-filter-update.md](hmm-filter-update.md) - one-step Hidden Markov Model filtering update from state transitions and observation likelihoods.
- [linear-regression-beta.md](linear-regression-beta.md) - estimate beta as an OLS regression slope.
- [option-strategy-payoffs.md](option-strategy-payoffs.md) - compute a bull call spread payoff at expiry.
- [heston-variance-step.md](heston-variance-step.md) - one-step Heston variance process update.
- [pd-logistic-score.md](pd-logistic-score.md) - map borrower variables to a toy logistic PD estimate.
- [simple-cva.md](simple-cva.md) - compute a one-period simplified CVA from exposure, default probability, and LGD.
- [vasicek-rate-step.md](vasicek-rate-step.md) - one-step short-rate update under a Vasicek-style model.
- [swap-pv.md](swap-pv.md) - simple fixed-vs-floating swap PV decomposition.
- [vwap-twap-comparison.md](vwap-twap-comparison.md) - compare VWAP and TWAP benchmarks on intraday prints.

## How To Use
- Treat the numbers as sanity-check scaffolding.
- Read the related chapter before relying on an example.
- In production, add conventions, calendars, data lineage, validation tolerances, and error handling.
