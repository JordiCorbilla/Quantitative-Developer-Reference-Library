# Capstone Projects

These are six implementation exercise specifications, not completed packages included in the checkout. They turn the reference chapters into reviewable, runnable work when implemented. Each capstone should use synthetic or appropriately licensed data, a versioned input snapshot, automated tests, and a short technical report explaining assumptions and limitations. For calculations that already run, start with the [worked examples](examples/README.md) and [quickstart](QUICKSTART.md).

The objective is not to reproduce a trading strategy. It is to demonstrate that market conventions, valuation, hedging, data lineage, risk, PnL, and production controls can be connected coherently.

## Shared Engineering Contract
Every project should include:

- a typed Python package rather than only a notebook;
- SQL DDL or an equivalent explicit persisted-data schema;
- immutable input fixtures and a reproducible build command;
- unit, property, integration, and golden-result tests;
- structured diagnostics and validation failures;
- point-in-time timestamps and dependency identifiers;
- a command-line or service entry point;
- profiling output for the main workload;
- a README stating conventions, limitations, and known failure modes.

A recommended layout is:

```text
project/
  pyproject.toml
  src/
  tests/
  fixtures/
  sql/
  notebooks/
  reports/
```

Notebooks may explore and explain results, but package code should own reusable logic.

## Capstone 1: Merger-Arbitrage Event Engine

Related chapters: [33-event-driven-and-merger-arbitrage.md](33-event-driven-and-merger-arbitrage.md), [36-warrants-rights-pipes-and-spacs.md](36-warrants-rights-pipes-and-spacs.md), [40-point-in-time-data-and-event-systems.md](40-point-in-time-data-and-event-systems.md), and [42-fundamental-catalyst-equity-analysis.md](42-fundamental-catalyst-equity-analysis.md).

### Build
- A normalized deal model for cash, stock, mixed-consideration, collar, tender, and CVR structures.
- An immutable event stream for announcement, amendment, vote, regulatory milestone, extension, completion, and break.
- Point-in-time deal terms and market observations.
- Spread, annualized return, stock hedge ratio, implied completion probability, and scenario expected value.
- Calendar-aware expected close dates, dividends, borrow, and financing.
- Position-level PnL explain for market moves, changing probability, time passage, hedge PnL, financing, and lifecycle events.

### Acceptance Tests
- Cash-deal spread and annualization reconcile to hand calculations.
- Stock-deal consideration updates correctly when the acquirer moves.
- A collar produces the correct piecewise exchange ratio.
- A late amendment is invisible before its publication timestamp.
- Completion and break events generate the correct cash, security, and position transitions.
- Expected value remains inside scenario payoff bounds.
- A broken hedge or missing borrow produces an explicit failed status.

### Extension
Add tender proration, appraisal rights, competing bids, regulatory-state probabilities, and a portfolio view of shared antitrust or financing risk.

## Capstone 2: Convertible-Arbitrage Book

Related chapters: [25-convertibles-and-equity-linked-notes.md](25-convertibles-and-equity-linked-notes.md), [35-convertible-arbitrage.md](35-convertible-arbitrage.md), [37-volatility-relative-value-and-event-volatility.md](37-volatility-relative-value-and-event-volatility.md), and [43-prime-brokerage-counterparty-and-funding.md](43-prime-brokerage-counterparty-and-funding.md).

### Build
- A typed term-sheet model covering coupon, maturity, conversion ratio, call/put schedules, soft-call triggers, make-whole terms, dividend protection, and anti-dilution.
- A simple lattice or finite-difference engine with separable equity, rates, credit, dividend, and borrow inputs.
- A stock hedge and optional credit hedge.
- Daily PnL attribution across delta, gamma, vega, theta/carry, rates, credit, borrow, financing, trade activity, and residual.
- Scenarios for default, call, put, conversion, dividend change, volatility shock, borrow repricing, and recall.
- A multi-bond portfolio with consistent share-equivalent risk units.

### Acceptance Tests
- Conversion parity, bond floor, and trivial value bounds hold.
- Increasing stock price does not reduce a plain convertible's value, absent unusual contractual effects.
- The hedge quantity reconciles to the declared delta convention.
- A parallel stock-and-hedge move produces plausible first- and second-order PnL.
- Call and put boundaries behave consistently around effective dates.
- Financing accrual uses settled stock borrow and effective-dated rates.
- Full revaluation reconciles to explained PnL within a documented tolerance.

### Extension
Parse a synthetic offering memorandum into the internal trade schema and produce a field-by-field exception report for ambiguous or unsupported terms.

## Capstone 3: Capital-Structure Relative-Value Monitor

Related chapters: [07-credit.md](07-credit.md), [34-capital-structure-relative-value.md](34-capital-structure-relative-value.md), [38-deal-level-risk-and-strategy-pnl.md](38-deal-level-risk-and-strategy-pnl.md), and [39-private-credit-distressed-and-real-estate-credit.md](39-private-credit-distressed-and-real-estate-credit.md).

### Build
- An issuer and legal-entity graph connecting loans, secured and unsecured bonds, converts, preferreds, CDS references, and equity.
- A claims hierarchy with guarantees, collateral, structural subordination, and recovery priority.
- Bond spread, CDS spread, equity value, enterprise value, and simple recovery-scenario analytics.
- Relative-value screens such as bond-CDS basis and cross-security scenario residuals.
- Hedge sizing and scenario PnL for spread convergence, default, refinancing, asset sale, dilution, and restructuring.
- Liquidity, bid/ask, financing, and executable-size adjustments.

### Acceptance Tests
- Security-level values aggregate to the declared enterprise-value bridge.
- Recovery allocations conserve distributable value and respect priority.
- Hedge ratios state their units and reference market levels.
- Default and recovery scenarios do not double-count equity value.
- The screen rejects stale or legally incompatible instruments.
- Position PnL separates market spread, rates, carry, default/recovery, financing, and residual.

### Extension
Add covenant headroom, maturity walls, restricted-payment capacity, and a point-in-time document-term store.

## Capstone 4: Event-Volatility and Dispersion Lab

Related chapters: [01-options.md](01-options.md), [18-volatility-products.md](18-volatility-products.md), [32-dependence-modelling-and-copulas.md](32-dependence-modelling-and-copulas.md), and [37-volatility-relative-value-and-event-volatility.md](37-volatility-relative-value-and-event-volatility.md).

### Build
- Option-chain normalization with bid/ask, forward, dividends, borrow, and no-arbitrage validation.
- A volatility surface or total-variance grid.
- Expected-move and event-variance decomposition around scheduled announcements.
- Delta-hedged option PnL and gamma/theta attribution.
- Index-versus-constituent dispersion with implied-correlation approximation.
- Scenario shocks for spot, skew, term structure, correlation, dividend, borrow, and post-event volatility crush.

### Acceptance Tests
- Put-call parity and vertical/calendar arbitrage diagnostics are visible.
- Variance units and notional conventions are explicit.
- Removing an event variance contribution changes only the intended expiry region.
- Delta-hedged PnL reconciles to full revaluation for small moves within tolerance.
- Dispersion weights and correlation exposure reconcile to the index variance identity.
- Missing or crossed option quotes do not silently enter calibration.

### Extension
Compare a model-free variance estimate with a calibrated-model estimate and explain the differences due to strike truncation, interpolation, and tails.

## Capstone 5: Point-in-Time Distributed Risk and Funding Platform

Related chapters: [40-point-in-time-data-and-event-systems.md](40-point-in-time-data-and-event-systems.md), [41-production-quant-engineering.md](41-production-quant-engineering.md), [43-prime-brokerage-counterparty-and-funding.md](43-prime-brokerage-counterparty-and-funding.md), and [44-robust-portfolio-and-research-validation.md](44-robust-portfolio-and-research-validation.md).

### Build
- Bitemporal schemas for market data, reference data, corporate events, financing rates, and model configuration.
- A deterministic snapshot builder.
- A worker protocol for pricing trades under scenarios.
- Cost-aware deterministic partitioning, idempotent retries, and expected-shard validation.
- Portfolio aggregation with additive and non-additive measure handling.
- Financing, stock-loan, margin, and counterparty exposure overlays.
- Structured logs, metrics, traces, and dependency lineage.

### Acceptance Tests
- A historical run cannot see later corrections or restatements.
- Replaying the same snapshot and code version yields the same result hash within declared numeric tolerance.
- Duplicate shard output is rejected.
- Missing or failed shards prevent an apparently complete portfolio result.
- Worker and aggregate snapshot IDs must match.
- Financing accrual reconciles to settled balances, effective rates, and day count.
- A combined market-loss, margin, borrow-recall, and collateral-haircut scenario produces a cash-liquidity projection.

### Extension
Run a controlled load test, identify the slowest product or shard, improve it, and document both the speedup and the numerical-regression evidence.

## Capstone 6: Point-in-Time Systematic Research and Execution Platform

Related chapters: [13-risk-and-pnl.md](13-risk-and-pnl.md), [16-portfolio-construction-and-backtesting.md](16-portfolio-construction-and-backtesting.md), [20-execution-microstructure-and-tca.md](20-execution-microstructure-and-tca.md), [40-point-in-time-data-and-event-systems.md](40-point-in-time-data-and-event-systems.md), [44-robust-portfolio-and-research-validation.md](44-robust-portfolio-and-research-validation.md), [45-time-series-forecasting-and-state-space-models.md](45-time-series-forecasting-and-state-space-models.md), [46-machine-learning-and-deep-learning-for-trading.md](46-machine-learning-and-deep-learning-for-trading.md), [47-reinforcement-learning-for-trading-and-execution.md](47-reinforcement-learning-for-trading-and-execution.md), and [48-factor-models-and-systematic-signals.md](48-factor-models-and-systematic-signals.md).

### Build
- Point-in-time security, price, factor, fundamental, event, borrow, and execution datasets with immutable forecast origins.
- A typed feature and label registry containing formula, units, availability lag, horizon, universe, transformations, and version.
- Classical baselines including a naive forecast, AR/ARIMA or HAR-RV model, and a filtered state-space/Kalman model where economically appropriate.
- Cross-sectional factor and signal research with CAPM/multi-factor attribution, neutralized rankings, turnover, capacity, and cost estimates.
- At least one regularized linear model and one nonlinear supervised candidate evaluated with nested, chronological, purged folds.
- Portfolio construction comparing constrained mean-variance with at least two of Black-Litterman, risk budgeting, fractional Kelly, or HRP.
- Pre-trade impact and execution logic using implementation shortfall, Kyle-style signed-flow diagnostics, an Almgren-Chriss-style schedule objective, and order-book controls where data permits.
- Historical, parametric, and Monte Carlo VaR/ES plus named market, liquidity, borrow, and gap stresses on executed holdings.
- A trial registry, target/executed position ledger, PnL attribution, model cards, shadow-run report, and deterministic fallback.

### Acceptance Tests
- Adding data strictly after a historical forecast origin does not change its features, fitted transforms, filtered state, prediction, or target order.
- Smoothed states, revised facts, future constituents, and overlapping label information cannot enter historical decisions.
- Every complex forecast is compared with the same-observation naive or linear baseline and reports outer-fold dispersion, calibration where relevant, and net value after costs.
- Factor, gross/net, concentration, liquidity, borrow, turnover, and portfolio-risk constraints reconcile before and after execution.
- For every selected allocation method, the applicable Black-Litterman view units and confidence, risk-budget contributions, Kelly fraction, or HRP hierarchy are visible and stable under declared perturbations.
- Historical, parametric, Monte Carlo, and named-stress results use the same position population and report intentional methodology differences.
- Order quantity is conserved from parent through fills and residual; side-aware implementation shortfall, fees, penalties, and PnL reconcile exactly.
- Replaying the same snapshot, manifest, code, configuration, and seeds reproduces artifacts within declared numerical tolerances.
- Unsupported market states, stale features, missing borrow, failed constraints, or unavailable liquidity trigger no-trade or deterministic fallback rather than a silent model decision.

### Extension
Add an RL execution policy only in a simulator and shadow environment. Compare it with deterministic VWAP, POV, and implementation-shortfall baselines; perform offline-support diagnostics, reward-hacking tests, domain stress, proposed-versus-executed action logging, and safety-layer overrides before considering any constrained canary.

## Review Standard
A capstone is ready for review when another developer can:

1. create the environment from documented commands;
2. rebuild the fixtures or verify their hashes;
3. run all tests;
4. reproduce the report;
5. trace every reported number to input data, configuration, and code;
6. identify the model and operational limitations without reading the implementation.

That standard is deliberately stricter than producing a plausible chart. Quantitative engineering is complete only when the result is reproducible, explainable, and safe to operate.
