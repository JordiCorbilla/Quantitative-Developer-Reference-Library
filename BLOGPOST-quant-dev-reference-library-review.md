# A Practical Reference Library for Quant Developers

Quantitative finance has a strange documentation problem.

There is plenty of material on the mathematics. There are books on option pricing, fixed income, stochastic calculus, portfolio construction, numerical methods, and risk. There are also plenty of code snippets scattered across notebooks, tutorials, and old internal tools.

What is harder to find is a practical reference that connects the whole workflow:

- what the product is,
- how the market quotes it,
- what data the system needs,
- how the pricing logic is usually implemented,
- what risk measures matter,
- how PnL should be explained,
- and what tends to break in production.

That is the gap this repository is trying to close.

The **Quantitative Developer Reference Library** is a Markdown-first reference for people building pricing, risk, market data, and portfolio analytics systems. It is written from the point of view of a quant developer: someone who needs enough theory to implement the model correctly, enough market knowledge to avoid convention errors, and enough engineering discipline to make the result reproducible.

## Why I Built It

Most quant finance knowledge is fragmented.

A textbook might derive a pricing equation beautifully but say little about production market data. A code example might price a vanilla option but ignore calendars, dividends, volatility-surface conventions, and validation. A desk wiki might contain useful practical knowledge, but it is usually private, incomplete, and hard to reuse.

The pain shows up in the same places again and again:

- a curve is built from the wrong quote convention,
- a volatility surface looks smooth but gives unstable Greeks,
- a pricing model works for clean examples but fails on real trade data,
- PnL explain does not reconcile to official marks,
- market data is present but not analytically trustworthy,
- risk reports look precise but hide missing factors or stale inputs.

The repo is built around a simple idea: quantitative correctness is not just the formula. It is the formula, the convention, the data, the implementation, the controls, and the explanation.

## What Is In The Repository

The library is organized into product chapters and engineering chapters.

The product side covers:

- options,
- futures and forwards,
- equities,
- FX,
- fixed income,
- interest rates,
- credit,
- commodities,
- and cross-asset topics.

The engineering side covers:

- market data,
- pricing architecture,
- risk and PnL,
- testing and validation,
- performance and production,
- and portfolio construction and backtesting.

There is also a numerical methods chapter because serious pricing work eventually runs into trees, PDEs, Monte Carlo, interpolation, calibration, convergence checks, and numerical stability.

The structure is intentionally consistent. Each chapter tries to answer the same practical questions:

- What does this domain cover?
- What are the main product types?
- How is it quoted?
- What is the core pricing framework?
- What risks matter?
- What data is required?
- What implementation approach is usually sensible?
- What are the common production pitfalls?
- What small code example helps anchor the concept?

That structure is useful because it lets the repository grow without becoming a pile of unrelated notes.

## Recent Additions: VaR, Expected Shortfall, and Beta

The risk and PnL chapter now has a more complete treatment of **Value at Risk**, **Expected Shortfall**, and **beta**.

VaR answers a threshold question:

> At a chosen confidence level and horizon, where does the loss tail begin?

Expected Shortfall answers a severity question:

> Once losses are beyond the VaR threshold, how bad are they on average?

That distinction matters. VaR is useful for limits, exception monitoring, and summary reporting. Expected Shortfall is more informative when the concern is tail severity, diversification failure, and stress-style risk management.

The beta addition makes the equity risk story clearer. Beta is not VaR by itself. It is a way to map an equity position or portfolio to a broad market factor:

```text
stock return = alpha + beta * market return + residual
```

A beta of 1.0 means the position tends to move broadly in line with the benchmark. A beta of 0.5 means it tends to move about half as much. A beta of 1.5 means it tends to move about 50% more.

In a simple factor VaR approximation, beta scales the market-factor shock:

```text
market loss ~= position value * beta * market-factor shock
```

That is useful, but it is incomplete. A proper risk view still needs residual volatility, sector factors, liquidity, concentration, nonlinear exposures, stress scenarios, and backtesting against realized PnL.

This is exactly the style of explanation I want the repository to support: not just the definition, but the implementation meaning and the limitations.

## What The Visuals Are For

The repo uses simple SVG diagrams throughout the chapters.

They are not meant to be decorative. They are there to make the mental model faster:

- payoff diagrams for options,
- lifecycle diagrams for futures margining,
- curve dependency diagrams for rates,
- cashflow diagrams for bonds,
- workflow diagrams for market data, pricing architecture, PnL explain, and validation,
- VaR and Expected Shortfall diagrams for tail-risk interpretation,
- beta visuals for market-factor sensitivity.

For a technical reference, visuals are useful when they compress an idea that would otherwise take several paragraphs. A good diagram should help a reader remember the structure of the problem before they go into the details.

## What The Repository Is Good At Today

The current version is strongest as a practical map.

It gives a quant developer a clear path through:

- core instruments,
- pricing intuition,
- quote and convention discipline,
- market-data dependencies,
- implementation patterns,
- risk measures,
- validation checks,
- and production failure modes.

It is especially useful for people who already know some finance or software engineering and want to connect the two. It is not trying to replace a textbook. It is trying to help someone build and reason about real analytics systems.

The strongest areas today are:

- options and volatility-surface basics,
- fixed income and rates foundations,
- numerical methods,
- market data and pricing architecture,
- risk, PnL explain, VaR, Expected Shortfall, and beta,
- portfolio construction and backtesting.

The Markdown-first format is also deliberate. There is no heavy documentation toolchain. The repo can be read directly, reviewed in GitHub, and extended chapter by chapter.

## What Is Still Missing

The quick review also makes the next gaps clear.

The biggest missing standalone areas are:

- inflation products, including CPI swaps, seasonality, index lags, and inflation-linked derivatives,
- volatility products, including variance swaps, VIX products, volatility futures, and dispersion,
- repo, reverse repo, securities lending, and financing analytics,
- regulatory and margin analytics, including SIMM, FRTB, stress capital, and margin explain,
- independent price verification and model governance workflows,
- execution microstructure and transaction-cost modelling as a deeper standalone topic,
- crypto and digital-asset market structure if the scope expands into modern multi-asset coverage.

There is also room for more worked examples. The repo already has illustrative snippets, but the next stage should include more end-to-end examples: small but complete calculations that connect inputs, conventions, valuation, risk, and validation.

Examples that would add real value:

- a bond clean/dirty price and duration walk-through,
- a swap valuation with projection and discount curves,
- a CDS spread-to-hazard example,
- a historical VaR and Expected Shortfall calculation,
- a factor model risk contribution example,
- a small backtest with turnover and cost accounting,
- a market-data cleaning example that shows what can go wrong.

Those examples would make the repo more concrete without turning it into a full code library.

## The Design Standard

The standard I want this project to meet is practical usefulness.

A section is not done just because it defines the concept. It should also help answer:

- What can go wrong?
- What does the system need to know?
- What assumptions are hidden?
- How would this be validated?
- How does this show up in risk or PnL?
- What should a developer be careful about?

That is the difference between a glossary and a reference.

For example, explaining beta should not stop at "beta measures sensitivity to the market." It should also explain that beta depends on benchmark choice, lookback window, return frequency, currency, and regression method. It should say that beta does not capture idiosyncratic risk, liquidity, event risk, or nonlinear payoffs. It should show how beta enters a factor VaR approximation, and why that approximation still needs residual risk and stress testing.

That is the level of explanation the repo is aiming for.

## Who This Is For

This repository is for:

- quant developers,
- engineering-minded quants,
- developers moving into front-office analytics,
- people building pricing, risk, or market-data systems,
- practitioners preparing for interviews or system design discussions,
- and anyone who wants a more implementation-grounded way to study quantitative finance.

It should be useful both as a learning path and as a reference you return to while building.

## Where It Goes Next

The next phase should deepen the repo in three directions.

First, add missing product areas: inflation, volatility derivatives, financing, and regulatory margin.

Second, add more worked examples that start from concrete market inputs and end with pricing, risk, and sanity checks.

Third, strengthen the engineering layer: model governance, independent price verification, data lineage, observability, and reproducibility.

The long-term goal is not to make the largest quant finance repo. The goal is to make a reference that is clear, practical, and reliable enough that a quant developer can use it as a map.

## Closing Thought

Quantitative finance is full of details that look small until they break a system.

A day-count convention. A stale curve node. A benchmark mismatch. A volatility quote in the wrong units. A VaR number without a clear horizon. A beta estimate with the wrong benchmark. A backtest that silently uses data it could not have known at the time.

The point of this library is to make those details visible.

Not to remove the complexity, but to structure it.

That is what makes a reference useful: it helps you see the whole problem, not just the equation in the middle.

---

## Short Version

I have been building a **Quantitative Developer Reference Library**: a practical Markdown-first repo for quant developers working on pricing, risk, market data, numerical methods, and production analytics.

It covers core products such as options, futures, equities, FX, fixed income, rates, credit, commodities, and cross-asset topics, plus engineering chapters on market data, pricing architecture, risk and PnL, testing, production, and portfolio construction.

Recent additions include clearer documentation and visuals for VaR, Expected Shortfall, and beta in equity VaR.

The goal is to bridge the gap between "I understand the formula" and "I can build, validate, and operate this correctly."
