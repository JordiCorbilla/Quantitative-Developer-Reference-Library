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
- [tranche-loss.md](tranche-loss.md) - compute loss allocation for an attachment/detachment tranche.
- [convertible-parity.md](convertible-parity.md) - compute convertible bond parity and conversion price.
- [trs-one-period.md](trs-one-period.md) - compute a one-period total return swap net payoff.
- [vasicek-rate-step.md](vasicek-rate-step.md) - one-step short-rate update under a Vasicek-style model.
- [swaption-intrinsic.md](swaption-intrinsic.md) - compute payer swaption intrinsic value from annuity, swap rate, and strike.
- [swap-pv.md](swap-pv.md) - simple fixed-vs-floating swap PV decomposition.
- [fx-swap-forward-points.md](fx-swap-forward-points.md) - compute FX swap forward points and explain near/far leg cashflows.
- [vwap-twap-comparison.md](vwap-twap-comparison.md) - compare VWAP and TWAP benchmarks on intraday prints.

## How To Use
- Treat the numbers as sanity-check scaffolding.
- Read the related chapter before relying on an example.
- In production, add conventions, calendars, data lineage, validation tolerances, and error handling.
