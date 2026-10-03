# Quantitative Developer Reference Library

Practical reference material for quant developers, engineering-minded quants, and anyone building pricing, risk, and market data systems. The goal is not to be a textbook. The goal is to compress the parts that matter in production: market conventions, pricing intuition, implementation shape, validation checks, and failure modes.

Start with [00-overview.md](00-overview.md). It defines the shared notation, discounting language, curve and surface glossary, and the overall map of the library.

Read the library through a problem you need to solve. A trader's call loses money even though the stock rises: follow the [options risk story](01-options.md#worked-risk-story-right-on-direction-losing-on-the-call), then [reprice the position](examples/option-greeks-and-earnings-repricing.md). A swap changes value between quoted maturities: follow [curve construction](06-interest-rates.md#curve-construction-between-market-nodes-interpolation-versus-fitting), then reproduce the off-node arithmetic. A backtest looks unusually strong: follow [point-in-time data](40-point-in-time-data-and-event-systems.md) and [research validation](44-robust-portfolio-and-research-validation.md) before trusting the result. Each route moves from a question to assumptions, a calculation, and a control.

## Project Navigation
- [INDEX.md](INDEX.md) - topic index across products, engineering, risk, execution, and governance
- [READING-PATHS.md](READING-PATHS.md) - guided paths for interviews, pricing, risk, rates, portfolio engineering, and volatility
- [INTERVIEW-GUIDE.md](INTERVIEW-GUIDE.md) - common interview questions and what strong answers should cover
- [GLOSSARY.md](GLOSSARY.md) - core terms, acronyms, and working definitions
- [examples/README.md](examples/README.md) - compact worked examples
- [CAPSTONE-PROJECTS.md](CAPSTONE-PROJECTS.md) - runnable project specifications that connect data, valuation, hedging, risk, PnL, and controls
- [CONTRIBUTING.md](CONTRIBUTING.md) - contribution rules, style guidance, and quality checks
- [CHANGELOG.md](CHANGELOG.md) - notable project changes
- [DOCUMENTATION-REVIEW.md](DOCUMENTATION-REVIEW.md) - dated review scope, factual corrections, options coverage, and limits of validation

## Library Map

### Core Instruments
- [00-overview.md](00-overview.md) - shared notation, discounting language, curve and surface vocabulary, sanity checks, and reading paths
- [01-options.md](01-options.md) - calls, puts, exercise styles, payoff mechanics, volatility surfaces, Greeks, theta/gamma carry, dynamic hedging, and listed contract multipliers
- [02-futures.md](02-futures.md) - forwards and futures as linear future-price agreements, including carry, basis, daily margining, contract multipliers, and rolls
- [03-equities.md](03-equities.md) - direct share ownership, long/short PnL, dividends, corporate actions, borrow costs, execution, and factor risk
- [04-fx.md](04-fx.md) - currency-pair orientation, spot, forwards, swaps, NDFs, FX option conventions, premium currency, and settlement calendars
- [05-fixed-income.md](05-fixed-income.md) - bonds as dated cashflows, clean vs dirty price, yield, duration, convexity, spreads, schedules, and curve inputs
- [06-interest-rates.md](06-interest-rates.md) - swaps, FRAs, short-rate futures, caps/floors, swaptions, multi-curve pricing, fixing logic, and rate-vol surfaces
- [07-credit.md](07-credit.md) - CDS protection, default probability, recovery, credit curves, bond-CDS basis, indices, and structured-credit framing
- [08-commodities.md](08-commodities.md) - commodity futures and options, delivery months, storage, convenience yield, event calendars, signed prices, limit states, gaps, and physical optionality
- [09-cross-asset.md](09-cross-asset.md) - hybrid payoffs, correlation, funding, collateral, counterparty exposure, xVA, and multi-asset scenario dependencies
- [10-numerical-methods.md](10-numerical-methods.md) - Monte Carlo, PDE, trees, interpolation, calibration, convergence, and numerical validation
- [17-inflation-products.md](17-inflation-products.md) - inflation-linked bonds, CPI swaps, indexation lags, seasonality, and real-rate risk
- [18-volatility-products.md](18-volatility-products.md) - variance products, EWMA, HAR-RV, GARCH, stochastic volatility, mixture/change-point regimes, and volatility-surface risk
- [19-financing-repo-and-securities-lending.md](19-financing-repo-and-securities-lending.md) - repo, reverse repo, securities lending, collateral, haircuts, borrow cost, and financing curves
- [24-structured-credit-and-securitization.md](24-structured-credit-and-securitization.md) - ABS, MBS, CLOs, tranche waterfalls, attachment/detachment, and securitized-credit risk
- [25-convertibles-and-equity-linked-notes.md](25-convertibles-and-equity-linked-notes.md) - convertible bonds, parity, bond floor, conversion features, and equity-linked notes
- [26-equity-swaps-and-total-return-swaps.md](26-equity-swaps-and-total-return-swaps.md) - equity swaps, TRS, synthetic financing, resets, dividends, and funding legs
- [27-cross-currency-swaps.md](27-cross-currency-swaps.md) - cross-currency swaps, basis, notional exchanges, resettable notionals, and collateral currency
- [28-rates-options-caps-floors-swaptions.md](28-rates-options-caps-floors-swaptions.md) - caps, floors, swaptions, normal/Black vols, annuity measure, and rates optionality
- [29-etfs-index-products-and-rebalances.md](29-etfs-index-products-and-rebalances.md) - ETFs, index products, NAV, creation/redemption, tracking error, and rebalances

### Strategy And Special-Situation Workflows
- [33-event-driven-and-merger-arbitrage.md](33-event-driven-and-merger-arbitrage.md) - cash and stock deals, collars, tenders, spreads, completion/break scenarios, event states, and hedging
- [34-capital-structure-relative-value.md](34-capital-structure-relative-value.md) - issuer-level relationships across loans, bonds, CDS, converts, preferreds, and equity
- [35-convertible-arbitrage.md](35-convertible-arbitrage.md) - convertible term analysis, valuation, stock and credit hedges, financing, and strategy PnL
- [36-warrants-rights-pipes-and-spacs.md](36-warrants-rights-pipes-and-spacs.md) - warrants, rights, private placements, PIPEs, SPAC units, redemptions, dilution, and lifecycle risk
- [37-volatility-relative-value-and-event-volatility.md](37-volatility-relative-value-and-event-volatility.md) - surface relative value, forward/event variance, gamma scalping, theta break-even, tail sizing, dispersion, and correlation
- [38-deal-level-risk-and-strategy-pnl.md](38-deal-level-risk-and-strategy-pnl.md) - idea-level loss budgets, related hedges, scenario PnL, financing, liquidity, and live controls
- [39-private-credit-distressed-and-real-estate-credit.md](39-private-credit-distressed-and-real-estate-credit.md) - loan underwriting, covenant headroom, restructuring, recoveries, CRE credit, and distressed scenarios
- [42-fundamental-catalyst-equity-analysis.md](42-fundamental-catalyst-equity-analysis.md) - financial statements, valuation bridges, estimates, catalysts, dilution, and point-in-time fundamentals
- [43-prime-brokerage-counterparty-and-funding.md](43-prime-brokerage-counterparty-and-funding.md) - stock loan, financing, margin, collateral, counterparty exposure, and liquidity

### Quant Engineering
- [11-market-data.md](11-market-data.md) - identifiers, symbology, time series, curves, surfaces, and data quality
- [12-pricing-architecture.md](12-pricing-architecture.md) - trade models, market state, pricing engines, and library design
- [13-risk-and-pnl.md](13-risk-and-pnl.md) - sensitivities, PnL explain, historical/parametric/Monte Carlo VaR, expected shortfall, stress risk, and controls
- [14-testing-and-validation.md](14-testing-and-validation.md) - numerical tests, model validation, and release discipline
- [15-performance-and-production.md](15-performance-and-production.md) - latency, throughput, observability, and operational resilience
- [16-portfolio-construction-and-backtesting.md](16-portfolio-construction-and-backtesting.md) - Markowitz, Black-Litterman, risk parity, Kelly, HRP, turnover, costs, constraints, and backtesting
- [20-execution-microstructure-and-tca.md](20-execution-microstructure-and-tca.md) - Kyle impact, Almgren-Chriss, order-book imbalance, VWAP/TWAP/POV, implementation shortfall, and TCA
- [21-regulatory-margin-capital.md](21-regulatory-margin-capital.md) - variation margin, initial margin, SIMM, FRTB, capital, stress, and margin explain
- [22-model-governance-and-ipv.md](22-model-governance-and-ipv.md) - model inventory, documentation, validation, IPV, reserves, approvals, and monitoring
- [23-probability-statistics-and-regression.md](23-probability-statistics-and-regression.md) - probability, statistics, OLS regression, diagnostics, beta estimation, and model evaluation
- [30-trade-lifecycle-and-operations.md](30-trade-lifecycle-and-operations.md) - trade initiation, capture, confirmation, settlement, lifecycle events, reconciliation, and operational controls
- [31-statistical-arbitrage-and-pairs-trading.md](31-statistical-arbitrage-and-pairs-trading.md) - pair selection, correlation versus cointegration, stateful mean-reversion trading, Engle-Granger/Johansen, OU/Kalman/PCA methods, execution, and failure controls
- [32-dependence-modelling-and-copulas.md](32-dependence-modelling-and-copulas.md) - copulas, tail dependence, joint simulation, calibration, and dependence-model risk
- [40-point-in-time-data-and-event-systems.md](40-point-in-time-data-and-event-systems.md) - bitemporal data, immutable events, as-of queries, security masters, corrections, and deterministic replay
- [41-production-quant-engineering.md](41-production-quant-engineering.md) - typed model libraries, SQL, distributed risk, testing, CI, profiling, deployment, and observability
- [44-robust-portfolio-and-research-validation.md](44-robust-portfolio-and-research-validation.md) - robust dependence, downside-aware optimization, multiple testing, and point-in-time research validation
- [45-time-series-forecasting-and-state-space-models.md](45-time-series-forecasting-and-state-space-models.md) - ARIMA/SARIMA/ARIMAX, VAR/VECM, stationarity, cointegration, state-space models, Kalman filters, and ordered validation
- [46-machine-learning-and-deep-learning-for-trading.md](46-machine-learning-and-deep-learning-for-trading.md) - regularized regression, trees and boosting, SVM/kNN/Naive Bayes, neural and sequence models, and leakage-safe deployment
- [47-reinforcement-learning-for-trading-and-execution.md](47-reinforcement-learning-for-trading-and-execution.md) - Q-learning, DQN, policy gradients, PPO, actor-critic, A3C/SAC, simulator discipline, offline evaluation, and safe controls
- [48-factor-models-and-systematic-signals.md](48-factor-models-and-systematic-signals.md) - CAPM, Fama-French, Carhart, Barra-style risk, momentum, reversal, breakout, trend, seasonality, and cross-sectional ranking

## Current Coverage Review
The library now covers the main building blocks a quant developer usually needs first: probability and statistics; classical time-series and state-space forecasting; statistical arbitrage; factor and systematic signal research; machine learning, deep learning, and reinforcement learning; robust point-in-time validation; options and volatility carry; linear derivatives; cash equities and commodities; FX, rates, credit, and structured products; event, relative-value, and catalyst strategies; historical, parametric, Monte Carlo, and stress risk; portfolio construction; market microstructure and execution; financing; production engineering; lifecycle operations; regulation; and model governance.

The main future direction remains executable depth:
- more worked end-to-end examples that connect market inputs, pricing, risk, and validation,
- deeper calibration case studies for curves, volatility surfaces, and credit curves,
- broader stress-testing examples across market, liquidity, and counterparty risk,
- crypto and digital-asset market structure if the library scope expands into that asset class,
- runnable implementations of the specifications in [CAPSTONE-PROJECTS.md](CAPSTONE-PROJECTS.md).

## How To Use This Repo
- Read the overview once, then use chapters as standalone references.
- Treat each chapter as a practitioner checklist: what gets quoted, what gets built, what breaks.
- Use the embedded SVG diagrams as quick mental models for payoff shapes, cashflow timing, curve dependencies, volatility products, financing, trade lifecycle, market-data pipelines, pricing architecture, risk explain, margin, governance, and validation workflows.
- Follow the cross-links. Options, fixed income, rates, numerical methods, and pricing architecture are intentionally tightly connected.
- Use the code snippets as sanity-check scaffolding, not as production-ready libraries.
- Use [CAPSTONE-PROJECTS.md](CAPSTONE-PROJECTS.md) to turn the chapters into package, data, test, and review deliverables.

## Design Principles
- Markdown-first, no docs toolchain required.
- Broad coverage first, then depth in the most implementation-dense areas.
- Theory only where it helps build or validate systems.
- Conventions and edge cases matter as much as formulas.
- The repo should keep growing without changing its basic structure.

## Evidence And Maintenance
The library distinguishes contract facts, mathematical identities, model assumptions, empirical heuristics, and synthetic examples. Read the qualification beside a formula before using it. Source documents and current product specifications determine conventions; regulatory chapters are conceptual guides whose rules must be checked for the jurisdiction, methodology version, and reporting date.

The automated checks validate structure, local links and heading anchors, SVG metadata, and runnable snippets. Worked examples contain assertions, but passing them is not independent validation of every model or a guarantee that a trading strategy works. The [documentation review](DOCUMENTATION-REVIEW.md) records what was checked and what still needs deeper evidence. Historical blog posts describe earlier snapshots rather than the current inventory.

## Contribution Direction
- Preserve the chapter template so readers always know where to find pricing, risk, data, and implementation guidance.
- Prefer short, precise examples over long tutorials.
- Add links between related chapters whenever a concept depends on another domain.
- Keep notation consistent with [00-overview.md](00-overview.md).
