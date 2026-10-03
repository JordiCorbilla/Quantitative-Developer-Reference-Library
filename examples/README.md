# Worked Examples

These examples are focused and self-contained. They connect formulas to implementation checks without pretending to be production libraries.

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
- [pairs-trading-spread-signal.md](pairs-trading-spread-signal.md) - calculate a standardized residual signal for a pairs-trading workflow.
- [cointegrated-pair-trade-lifecycle.md](cointegrated-pair-trade-lifecycle.md) - run a synthetic KO/PEP pair through cointegration-hedge sizing, stateful entry/exit/stop rules, and leg-level PnL.
- [equity-snapshot-metrics.md](equity-snapshot-metrics.md) - calculate market cap, P/E ratios, and dividend yield from a fictional equity snapshot.
- [large-order-participation.md](large-order-participation.md) - calculate a participation-limited child-order quantity from a parent order and volume forecast.
- [copula-tail-dependence.md](copula-tail-dependence.md) - calculate the lower-tail dependence coefficient of a Clayton copula and interpret it carefully.
- [merger-arbitrage-scenario.md](merger-arbitrage-scenario.md) - calculate deal spread, implied completion probability, and expected value across close and break scenarios.
- [capital-structure-recovery-waterfall.md](capital-structure-recovery-waterfall.md) - allocate enterprise value through a claims hierarchy and inspect cross-security recovery.
- [convertible-arbitrage-hedge-pnl.md](convertible-arbitrage-hedge-pnl.md) - size a stock hedge and decompose simplified convertible-arbitrage PnL.
- [spac-unit-and-warrant.md](spac-unit-and-warrant.md) - separate SPAC unit components and examine redemption and warrant dilution mechanics.
- [event-volatility-implied-move.md](event-volatility-implied-move.md) - estimate an option-implied event move and isolate event variance.
- [deal-level-loss-budget.md](deal-level-loss-budget.md) - aggregate core and hedge legs under named scenarios and enforce an idea-level loss budget.
- [private-credit-covenant-headroom.md](private-credit-covenant-headroom.md) - calculate leverage and coverage covenant headroom under base and downside cases.
- [bitemporal-asof-replay.md](bitemporal-asof-replay.md) - retrieve the data version that was knowable at a historical decision cutoff.
- [distributed-risk-partition.md](distributed-risk-partition.md) - partition heterogeneous risk work while checking complete, non-duplicate assignment.
- [catalyst-equity-earnings-bridge.md](catalyst-equity-earnings-bridge.md) - bridge revenue, margins, share count, EPS, and valuation under catalyst scenarios.
- [prime-broker-financing-comparison.md](prime-broker-financing-comparison.md) - compare financing, borrow, margin-liquidity, and allocation costs.
- [gerber-co-movement.md](gerber-co-movement.md) - compute thresholded robust co-movement while separating signal-sized moves from noise.
- [theta-gamma-daily-breakeven.md](theta-gamma-daily-breakeven.md) - derive the local delta-hedged move required to offset one interval of theta.
- [commodity-option-event-gap.md](commodity-option-event-gap.md) - stress a short commodity straddle through event gaps, locked hedges, signed prices, and tail-first sizing.
- [ewma-har-rv-forecast.md](ewma-har-rv-forecast.md) - compare transparent EWMA and HAR-RV next-day variance forecasts.
- [kalman-filter-dynamic-hedge-ratio.md](kalman-filter-dynamic-hedge-ratio.md) - update a time-varying hedge ratio with a scalar Kalman filter.
- [purged-regularized-signal-model.md](purged-regularized-signal-model.md) - fit and evaluate a regularized signal model with nested, purged time splits.
- [reinforcement-learning-reward-accounting.md](reinforcement-learning-reward-accounting.md) - reconcile execution economics, penalties, and a telescoping RL reward ledger.
- [factor-signal-neutralization.md](factor-signal-neutralization.md) - neutralize cross-sectional scores by group and verify gross/net exposures.
- [portfolio-risk-budgeting.md](portfolio-risk-budgeting.md) - calculate inverse-volatility weights and equal risk contributions in a controlled case.
- [order-book-impact-tradeoff.md](order-book-impact-tradeoff.md) - compare temporary-impact exposure, remaining inventory, and displayed imbalance.
- [parametric-monte-carlo-var.md](parametric-monte-carlo-var.md) - reconcile normal parametric VaR/ES with a seeded Monte Carlo estimate.
- [yield-curve-interpolation-comparison.md](yield-curve-interpolation-comparison.md) - compare linear-zero and log-linear-discount-factor interpolation at an off-node maturity.

- [option-greeks-and-earnings-repricing.md](option-greeks-and-earnings-repricing.md) - fully reprice a rising-stock, losing-call scenario and verify Greek derivatives, parity, units, and sign exceptions.
- [index-divisor-and-weights.md](index-divisor-and-weights.md) - reconcile share quantities, portfolio weights, a split, and a continuity-preserving divisor adjustment.

## How To Use
Use the options repricing example to follow a complete question-to-control story; use the other examples to isolate a specific calculation.

- Treat the numbers as sanity-check scaffolding.
- Read the related chapter before relying on an example.
- In production, add conventions, calendars, data lineage, validation tolerances, and error handling.
