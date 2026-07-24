# Execution Microstructure and Transaction-Cost Analysis

Related chapters: [03-equities.md](03-equities.md), [11-market-data.md](11-market-data.md), [13-risk-and-pnl.md](13-risk-and-pnl.md), [15-performance-and-production.md](15-performance-and-production.md), and [16-portfolio-construction-and-backtesting.md](16-portfolio-construction-and-backtesting.md).

## What This Domain Covers
Execution is where a portfolio decision meets the market.

Before execution, a strategy can look clean: buy this, sell that, rebalance here. After execution, the real result includes spread, market impact, delay, partial fills, fees, taxes, borrow costs, and opportunity cost. Transaction-cost analysis turns that messy reality into something measurable.

This chapter follows the trade from decision price to order instructions to fills to post-trade analysis.

## Product Taxonomy and Market Structure
Start by asking how the order is intended to interact with liquidity.

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
The central execution question is simple: how much did trading cost relative to the benchmark that mattered?

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

## Executing A Large Parent Order
A large order cannot be made invisible merely by dividing it into smaller tickets. The objective is to minimize expected trading cost while controlling the risk that the market moves away before the order is complete. The right choice depends on order size relative to liquidity, urgency, benchmark, volatility, spread, expected intraday volume, and information leakage risk.

![Large order execution decision guide](assets/large-order-execution-decision-guide.svg)

The usual implementation is a **parent order** with controlled **child orders**. A parent order might buy 400,000 shares; the execution algorithm decides how much to send, where, and when. A round lot is the exchange-defined standard trading unit for a market and is not a measure of safe order size. What matters is the parent order's participation in available volume and displayed or hidden liquidity.

### Choosing The Objective

- **VWAP**: appropriate when the mandate is to perform near the session's volume-weighted benchmark and there is time to follow a volume forecast.
- **TWAP**: appropriate when the order should be distributed evenly through a defined time window and a reliable volume forecast is unavailable or unnecessary.
- **POV**: appropriate when trading should scale with observed market activity. The trader sets a maximum participation rate, then the algorithm slows down when the market is quiet.
- **Implementation shortfall (IS)**: appropriate when the decision or arrival price matters and delaying the trade risks losing alpha or increasing portfolio risk. It trades the impact-versus-timing trade-off directly.
- **Passive limit / liquidity seeking**: appropriate when price control matters more than certainty of completion. It reduces crossing cost but accepts adverse selection and opportunity cost.
- **Open or close auction**: appropriate when the benchmark, index event, or available liquidity is concentrated in that auction. Auction participation still carries imbalance and price uncertainty.

No algorithm guarantees that a large trade will not move the price. A good execution plan chooses an explicit trade-off, sets participation and price limits, watches live conditions, and is willing to pause or change course when conditions diverge from the pre-trade model.

### Market Impact And Order Size

For a buy order, implementation shortfall can be separated conceptually into spread, temporary impact, permanent information component, delay, fees, and opportunity cost. The decomposition is model-dependent, but it prevents one number from hiding several causes.

If $Q$ shares were intended, $q_i$ shares were executed at prices $p_i$, and $q_u$ shares remain unfilled and are valued at an end-of-window price $p_T$, a simple buy-side implementation-shortfall representation is:

$$
\text{IS} = \sum_i q_i(p_i-p_0) + q_u(p_T-p_0) + \text{fees},
\qquad Q = \sum_i q_i + q_u
$$

The first term captures executed slippage. The second makes the opportunity cost of the unfilled residual visible. A production TCA must state the chosen end-of-window price and sign convention.

Order size is often normalized by average daily volume:

$$
\text{ADV participation} = \frac{\text{parent order quantity}}{\text{average daily volume}}
$$

This is only a first screen. A 10% ADV order may be manageable in a deep, stable name over a full day, yet highly disruptive if concentrated in a short interval, during a news event, or in a stock with a wide spread and little displayed depth. Pre-trade analysis should use intraday volume curves, volatility, spread, event calendar, borrow status for sells, and a capacity limit by venue.

## Worked Instrument Example: A Buy Program With A Participation Limit
Assume a manager must buy 400,000 shares. Historical ADV is 4,000,000 shares, so the parent order is 10% of ADV. The manager has no immediate alpha-decay concern and chooses a VWAP-style schedule with a maximum 10% participation rate.

If the first two hours are forecast to contain 25% of daily volume, the forecast volume is 1,000,000 shares. The schedule may target no more than:

$$
10\% \times 1{,}000{,}000 = 100{,}000\text{ shares}
$$

in that window, subject to spread, volatility, price, and real-time volume checks. If actual volume is lower than forecast, the algorithm reduces child-order quantity rather than forcing the schedule. If the trade is not complete, the residual is a real decision: continue, increase urgency, use an auction, cross liquidity, or leave the position partly unfilled. It should never be hidden inside a single average fill price.

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
- Parent-order participation, residual quantity, and completion risk.

## Required Data, Curves, Surfaces, and Calibration Objects
- Order and execution ledgers with timestamps.
- Market data around decision, route, fill, and close times.
- Venue, broker, fee, rebate, and tax schedules.
- Volume curves, spread history, volatility, ADV, and intraday participation constraints.
- Order-book or liquidity proxies, auction schedules, corporate-event calendar, and parent-order urgency constraints.
- Corporate-action adjusted identifiers.
- Strategy signal timestamps to detect look-ahead and delay.

## Numerical and Implementation Approaches
- Store decision price, arrival price, fill price, and benchmark price separately.
- Keep side-aware formulas; buy and sell slippage signs differ.
- Match the evaluation benchmark to the algorithm objective: VWAP to VWAP, TWAP to time schedule, implementation shortfall to arrival or decision price.
- Decompose costs before aggregating so model errors are visible.
- Calibrate impact models by liquidity bucket, volatility, urgency, and participation rate.
- Feed post-trade results back into pre-trade cost estimates.
- Record the parent-order objective, constraints, schedule changes, and residual-order decisions so TCA can explain them.

## Production Pitfalls and Sanity Checks
- Measuring slippage to close when the execution objective was arrival price.
- Ignoring unfilled quantity and reporting only completed shares.
- Using post-trade market data in pre-trade models.
- Aggregating buys and sells with inconsistent sign conventions.
- Reporting backtests without realistic turnover, spread, and impact assumptions.
- Treating a fixed participation rate or a round-lot size as proof that an order will be non-disruptive.

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
