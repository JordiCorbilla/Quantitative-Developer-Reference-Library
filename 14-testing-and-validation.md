# Testing and Validation

Related chapters: [10-numerical-methods.md](10-numerical-methods.md), [11-market-data.md](11-market-data.md), [12-pricing-architecture.md](12-pricing-architecture.md), and [13-risk-and-pnl.md](13-risk-and-pnl.md).

## What This Domain Covers
Testing protects correctness at the code level. Validation protects correctness at the model and workflow level. Quant platforms need both. A system can have full unit-test coverage and still be wrong in production because conventions, data lineage, or model assumptions are mis-specified.

## Product Taxonomy and Market Structure
- Unit tests for formulas and utilities
- Regression tests for products and portfolios
- Numerical convergence tests
- Golden-copy reconciliation tests
- Model validation and challenger benchmarking
- Release and change-control checks

## Quoting and Market Conventions
- Test fixtures must include quote conventions and metadata, not just numbers.
- Golden datasets should include the market context required to reproduce the result.
- Tolerance policy should reflect business materiality and method noise.

## Core Pricing Framework
Testing layers should answer different questions:
- unit tests: does this function obey its local contract?
- integration tests: does the full pricing path work with realistic objects?
- regression tests: did behavior change unexpectedly?
- validation tests: does the model remain appropriate for its stated use?

Useful validation categories:
- analytic benchmark vs implementation,
- cross-engine comparison,
- market-quote repricing,
- stress and limit-case behavior,
- sensitivity stability under bump-size variation.

## Key Risk Measures and Sensitivities
- Price error against benchmarks
- Greek stability and symmetry checks
- Calibration residuals
- Repricing error on market instruments
- Scenario consistency and explain residual behavior

## Required Data, Curves, Surfaces, and Calibration Objects
- Stable fixture datasets with versioning
- Benchmark parameter sets and expected outputs
- Historical snapshots for replayable regression tests
- Model documentation linking each test family to a product or risk assumption
- Release metadata showing what changed in code, data, or configuration

## Numerical and Implementation Approaches
- Use closed-form cases as anchors even when production uses more complex methods.
- Keep deterministic tests for stochastic engines by fixing seeds and path configs.
- Add metamorphic tests: monotonicity, parity, homogeneity, and boundary behavior.
- Compare multiple independent implementations when the product is business-critical.
- Automate regression packs that cover both price and risk, not just price.

## Production Pitfalls and Sanity Checks
- Tolerances widened until failing tests disappear.
- Golden files updated without understanding why results moved.
- Validation treated as a one-time sign-off instead of continuous change control.
- Missing tests for calendars, schedules, and quote-convention transformations.
- Stochastic tests that flap because variance budgets were never defined.

## Illustrative Code
```python
def assert_close(actual: float, expected: float, tolerance: float, label: str) -> None:
    if abs(actual - expected) > tolerance:
        raise AssertionError(f"{label}: expected {expected}, got {actual}, tolerance {tolerance}")
```

## References and Further Reading
- Model risk management guidance in your jurisdiction
- Numerical-analysis texts on convergence and error control
- Chapter links: [10-numerical-methods.md](10-numerical-methods.md), [13-risk-and-pnl.md](13-risk-and-pnl.md)
