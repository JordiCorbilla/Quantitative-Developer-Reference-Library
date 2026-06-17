# Execution Microstructure and Transaction-Cost Analysis

Related chapters: [03-equities.md](03-equities.md), [11-market-data.md](11-market-data.md), [13-risk-and-pnl.md](13-risk-and-pnl.md), [15-performance-and-production.md](15-performance-and-production.md), and [16-portfolio-construction-and-backtesting.md](16-portfolio-construction-and-backtesting.md).

## What This Domain Covers
Execution analytics connect portfolio decisions to realized trades. A strategy can look profitable before costs and fail after spread, impact, delay, borrow, fees, and incomplete fills. Transaction-cost analysis makes those costs measurable and reproducible.

## Product Taxonomy and Market Structure
- Lit venues, dark pools, auctions, RFQ, and OTC execution.
- Market, limit, stop, VWAP, TWAP, participation, and implementation-shortfall algorithms.
- Pre-trade cost models and post-trade TCA.
- Venue analysis, fill-quality analysis, and broker scorecards.
- Slippage, spread cost, impact, delay cost, and opportunity cost.

## Quoting and Market Conventions
- Bid, ask, mid, last, official close, and arrival price answer different questions.
- TCA benchmark choice must match the execution objective.
- Fees, rebates, taxes, and borrow costs may be venue-specific.
- Volume curves and market sessions matter for participation strategies.
- Corporate actions and symbol changes must not break historical execution analysis.

## Core Pricing Framework
Implementation shortfall compares executed value to the decision-time benchmark:

$$
\text{shortfall} = \sum_i q_i(p_i - p_0)
$$

for a buy order, where $p_0$ is the decision or arrival price. A complete TCA decomposes shortfall into spread, impact, delay, fees, and opportunity cost.

### Visual Execution Reference

![Execution and TCA workflow](assets/execution-tca-workflow.svg)

TCA is useful when it connects decisions, order instructions, market conditions, realized fills, and model feedback.

## VWAP, TWAP, POV, and Implementation Shortfall
VWAP and TWAP belong in this repo because they are the simplest bridge between trading strategy, microstructure, and measurable execution quality. They also come up often in interviews because they test whether a candidate understands benchmarks, schedules, volume curves, and cost trade-offs rather than only formulas.

### VWAP
Volume-weighted average price measures the average traded price weighted by market volume:

$$
\text{VWAP} = \frac{\sum_i p_i v_i}{\sum_i v_i}
$$

A VWAP execution algorithm tries to trade in line with the expected intraday volume curve. If 12% of the day's volume usually trades in the first interval, a VWAP schedule may target roughly 12% of the parent order in that interval. VWAP is useful when the objective is to perform near the market's volume-weighted benchmark and avoid being too visible relative to normal liquidity.

### TWAP
Time-weighted average price slices an order evenly through time:

$$
\text{TWAP} = \frac{1}{n}\sum_i p_i
$$

A TWAP execution schedule is simple: trade the same quantity every time bucket. It is easy to explain and does not require a strong volume forecast, but it can overtrade quiet periods and undertrade liquid periods.

### POV and Implementation Shortfall
Percentage-of-volume (POV) trades a target participation rate of observed market volume. If market volume accelerates, the order trades faster; if market volume dries up, the order slows down. Implementation shortfall algorithms use the decision or arrival price as the benchmark and typically balance market impact against alpha decay and timing risk.

![VWAP and TWAP execution schedules](assets/vwap-twap-execution-schedules.svg)

![Execution algorithm decision map](assets/execution-algo-decision-map.svg)

Interview framing:
- VWAP: "match the market's volume profile and benchmark to volume-weighted price."
- TWAP: "slice evenly through time when simplicity matters or volume forecasts are weak."
- POV: "participate in real-time liquidity at a controlled participation rate."
- Implementation shortfall: "trade faster when waiting risk and alpha decay matter more than impact cost."
- Limit or passive execution: "control price, but accept fill uncertainty and opportunity cost."

Common mistakes:
- Comparing a VWAP algo to arrival price and calling it bad even though it optimized a different benchmark.
- Using TWAP for an illiquid name without checking whether equal time slices exceed available liquidity.
- Forgetting that VWAP is only known after the trading window finishes.
- Ignoring partial fills, fees, spread, and market impact when comparing algorithms.
- Treating a broker's algo label as enough; the actual schedule, constraints, and venue behavior still matter.

## Worked Instrument Example: Buy Order Shortfall
Assume:
- decision price: USD 50.00,
- executed quantity: 100,000 shares,
- average execution price: USD 50.08.

Implementation shortfall is:

$$
100{,}000 \times (50.08 - 50.00) = 8{,}000
$$

The number is only interpretable if the benchmark, side, fees, partial fills, and currency are defined.

## Key Risk Measures and Sensitivities
- Spread cost and effective spread.
- Market impact and participation-rate sensitivity.
- VWAP, TWAP, POV, and arrival-price slippage.
- Delay cost and alpha decay.
- Opportunity cost from unfilled quantity.
- Venue fill quality and adverse selection.
- Capacity and liquidity limits.

## Required Data, Curves, Surfaces, and Calibration Objects
- Order and execution ledgers with timestamps.
- Market data around decision, route, fill, and close times.
- Venue, broker, fee, rebate, and tax schedules.
- Volume curves, spread history, volatility, ADV, and intraday participation constraints.
- Corporate-action adjusted identifiers.
- Strategy signal timestamps to detect look-ahead and delay.

## Numerical and Implementation Approaches
- Store decision price, arrival price, fill price, and benchmark price separately.
- Keep side-aware formulas; buy and sell slippage signs differ.
- Match the evaluation benchmark to the algorithm objective: VWAP to VWAP, TWAP to time schedule, implementation shortfall to arrival or decision price.
- Decompose costs before aggregating so model errors are visible.
- Calibrate impact models by liquidity bucket, volatility, urgency, and participation rate.
- Feed post-trade results back into pre-trade cost estimates.

## Production Pitfalls and Sanity Checks
- Measuring slippage to close when the execution objective was arrival price.
- Ignoring unfilled quantity and reporting only completed shares.
- Using post-trade market data in pre-trade models.
- Aggregating buys and sells with inconsistent sign conventions.
- Reporting backtests without realistic turnover, spread, and impact assumptions.

## Illustrative Code
```python
def buy_shortfall(quantity: float, decision_price: float, average_fill_price: float) -> float:
    return quantity * (average_fill_price - decision_price)


def sell_shortfall(quantity: float, decision_price: float, average_fill_price: float) -> float:
    return quantity * (decision_price - average_fill_price)


def vwap(prices: list[float], volumes: list[float]) -> float:
    traded_volume = sum(volumes)
    if traded_volume == 0:
        raise ValueError("VWAP requires positive total volume")
    return sum(price * volume for price, volume in zip(prices, volumes)) / traded_volume


def twap(prices: list[float]) -> float:
    if not prices:
        raise ValueError("TWAP requires at least one price")
    return sum(prices) / len(prices)
```

## References and Further Reading
- Kissell. *The Science of Algorithmic Trading and Portfolio Management*
- Market microstructure and execution-algorithm methodology notes.
- Broker and venue TCA documentation.
