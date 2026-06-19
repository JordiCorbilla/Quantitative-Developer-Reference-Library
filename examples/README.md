# Worked Examples

These examples are small by design. They are meant to connect formulas to implementation checks without turning the repository into a full codebase.

## Examples
- [historical-var-es.md](historical-var-es.md) - compute historical VaR and Expected Shortfall from scenario losses.
- [garch-forecast.md](garch-forecast.md) - one-step GARCH(1,1) conditional variance update.
- [regime-switching-probability.md](regime-switching-probability.md) - two-state Markov regime probability update.
- [swap-pv.md](swap-pv.md) - simple fixed-vs-floating swap PV decomposition.
- [vwap-twap-comparison.md](vwap-twap-comparison.md) - compare VWAP and TWAP benchmarks on intraday prints.

## How To Use
- Treat the numbers as sanity-check scaffolding.
- Read the related chapter before relying on an example.
- In production, add conventions, calendars, data lineage, validation tolerances, and error handling.
