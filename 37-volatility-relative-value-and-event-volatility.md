# Volatility Relative Value and Event Volatility

Related chapters: [01-options.md](01-options.md), [10-numerical-methods.md](10-numerical-methods.md), [11-market-data.md](11-market-data.md), [13-risk-and-pnl.md](13-risk-and-pnl.md), [18-volatility-products.md](18-volatility-products.md), and [38-deal-level-risk-and-strategy-pnl.md](38-deal-level-risk-and-strategy-pnl.md).

## What This Domain Covers
Volatility relative value asks whether one part of an option surface is expensive or cheap relative to another observable or forecastable quantity. Event volatility isolates uncertainty concentrated around a known or suspected catalyst. Both require more than comparing two implied-volatility numbers: the maturities, forwards, strikes, Greeks, event calendars, transaction costs, and realized-variance conventions must be comparable.

Typical questions include:

- Is implied variance rich or cheap relative to a point-in-time forecast of realized variance?
- Is a forward volatility interval mispriced relative to adjacent expiries?
- Does index volatility imply a plausible level of constituent correlation?
- How much jump variance is assigned to a scheduled announcement?
- Is skew compensating for crash risk, supply and demand, or a stale surface?

The engineering objective is a replayable pipeline from raw option quotes and event records to clean surfaces, risk, scenario PnL, and daily attribution. A trade is not validated merely because its entry z-score is large.

## Product Taxonomy and Market Structure
Volatility relative-value positions can be organized by the quantity they compare.

- **Implied versus realized:** delta-hedged options, straddles, variance swaps, or option strips versus a realized-volatility forecast.
- **Term structure:** calendars, diagonals, forward-starting options, and forward variance between two expiries.
- **Smile and skew:** risk reversals, butterflies, put-skew or call-skew spreads, and relative-value trades across standardized deltas.
- **Dispersion and correlation:** index variance against weighted constituent variance, with residual correlation, skew, dividend, and rebalance exposure.
- **Volatility of volatility:** option structures whose value depends materially on how the surface itself moves.
- **Scheduled event volatility:** expiries bracketing earnings, economic releases, court decisions, votes, regulatory decisions, or product results.
- **Unscheduled jump risk:** takeovers, guidance changes, defaults, geopolitical shocks, and other events whose timing is uncertain.

Listed options provide transparent contract terms but fragmented liquidity across strikes and expiries. Over-the-counter variance and volatility products can isolate exposures more directly, but add documentation, counterparty, collateral, and valuation-control requirements. Event trades are often most liquid near at-the-money strikes, while their worst loss can be driven by wings, gaps, or post-event skew.

## Quoting and Market Conventions
- Implied volatility is normally annualized; record whether time uses calendar days, trading days, or exact minutes.
- Total implied variance is $\sigma^2T$, not $\sigma T$. Calendar comparisons should usually be made in total variance.
- Store spot, forward, log-moneyness, and delta. A 25-delta option is not a stable identifier unless the delta convention and surface snapshot are known.
- Record whether realized variance uses log or arithmetic returns, close-to-close or intraday samples, and how overnight moves and corporate actions are treated.
- Event timestamps need a time zone and session classification such as before open, during session, or after close. A date without a time can map the event to the wrong expiry.
- Equity option values depend on discounting, expected dividends, borrow, settlement style, exercise style, multiplier, and deliverable adjustments.
- A variance notional per decimal variance differs by a factor of 10,000 from a notional per variance point. Make the unit part of the type or schema.
- Mid, natural, and executable prices answer different questions. Research should retain bid, ask, sizes, quote age, and the chosen marking rule.
- Calendar decay and variance time are not interchangeable defaults. Store whether each interval uses calendar days, trading sessions, exact timestamps, or a calibrated event/weekend clock.
- A Friday-to-Monday change in implied volatility is not itself the weekend PnL. Separate premium change, passage of time, forward/curve roll, surface re-mark, and event variance; there is no universal convention that volatility must be marked down before every weekend.

## Core Pricing Framework
For an expiry $T$, define total implied variance:

$$
W(T,k) = \sigma_{\text{imp}}^2(T,k)T
$$

where $k=\log(K/F_T)$ is log-forward moneyness. At a fixed moneyness, the forward variance between $T_1$ and $T_2$ is:

$$
v_{T_1,T_2} =
\frac{W(T_2,k)-W(T_1,k)}{T_2-T_1}
$$

The calculation is simple; using incompatible moneyness, forwards, or interpolation rules is not. Negative forward variance is either a data or construction error, or evidence that the fitted surface violates calendar arbitrage.

For one known event before expiry, a useful *Gaussian-equivalent* first model decomposes Black total variance into diffuse variance and one effective event-variance parameter:

$$
W(T) = \int_0^T v_{\text{diffuse}}(u)\,du
+ \mathbf{1}_{\{\tau_{\text{event}}\leq T\}}q_{\text{event}}^{\text{eff}}
$$

Under an independent Gaussian log-jump model, $q_{\text{event}}^{\text{eff}}=\operatorname{Var}^Q(J)$. It is not generally $E^Q[J^2]$, because a nonzero risk-neutral mean contributes to the second moment without becoming Black variance. More broadly, generic jumps, skew, and strike-dependent implied volatility do not collapse exactly into one additive ATM-variance number. With expiries bracketing the event and an estimated diffuse variance $\bar v$, desks often use the following explicitly model-dependent screen:

$$
\widehat q_{\text{event}}^{\text{eff}}
= W(T_2)-W(T_1)-\bar v(T_2-T_1)
$$

The corresponding Gaussian-equivalent one-standard-deviation log move is approximately:

$$
m_{\text{event}}=\sqrt{\max(\widehat q_{\text{event}}^{\text{eff}},0)}
$$

For small moves, traders may read this as an approximate percentage move, but it is not a model-free event distribution. A model-free expected-variance estimate requires a strip of out-of-the-money options across strikes, as in variance-swap replication; subtracting two ATM Black variances is only a screening heuristic. The at-the-money straddle premium divided by spot is another useful shorthand, but it is not algebraically identical: it reflects discounting, diffuse volatility, skew, tails, and option convexity.

For a locally delta-hedged option in a continuous interval, the familiar approximation is:

$$
d\Pi \approx
\frac{1}{2}\Gamma S^2
\left(\sigma_{\text{realized}}^2-\sigma_{\text{implied}}^2\right)dt
$$

For one discrete step of variance time $\Delta\tau$, after carry and financing are handled consistently, the same local comparison can be written:

$$
\Delta\Pi
\approx
\frac{1}{2}\Gamma
\left[(\Delta S)^2-S^2\sigma_{\text{imp}}^2\Delta\tau\right].
$$

The corresponding close-to-close absolute move that offsets the model theta is:

$$
|\Delta S|_{\text{BE}}
\approx S\sigma_{\text{imp}}\sqrt{\Delta\tau}.
$$

This is a local gamma/theta break-even, not the premium break-even at expiry. It assumes compatible Greek units, the same volatility clock, continuous local dynamics, no surface move, and costless delta hedging. A long-gamma hedge sells underlying after rises and buys after falls; a short-gamma hedge must buy after rises and sell after falls. Gaps occur before either side can trade, so realized close-to-close variance does not by itself determine executable hedge PnL. The full derivation and code are in [examples/theta-gamma-daily-breakeven.md](examples/theta-gamma-daily-breakeven.md).

Around a discrete event, full repricing under jump scenarios is preferable. A Taylor approximation can be badly wrong when spot crosses strikes, skew shifts, or the option changes exercise behavior.

## Worked Instrument Example
Suppose two at-the-money expiries bracket one scheduled event:

| Input | Before-event expiry | After-event expiry |
| --- | ---: | ---: |
| Time to expiry | 20/365 | 27/365 |
| Implied volatility | 30% | 44% |

Assume diffuse volatility over the seven-day interval is 28%. The total variances are:

$$
W_1=0.30^2\frac{20}{365}=0.004932
$$

$$
W_2=0.44^2\frac{27}{365}=0.014321
$$

The inferred event variance is:

$$
\widehat q_{\text{event}}
=0.014321-0.004932-0.28^2\frac{7}{365}
=0.007886
$$

Therefore the risk-neutral RMS implied log jump is about:

$$
\sqrt{0.007886}=8.88\%
$$

For an illustrative event-variance position with USD 10m notional per unit of decimal variance, ignoring continuous variance and costs:

| Realized absolute log jump | Event-variance PnL |
| ---: | ---: |
| 5% | USD -53,860 |
| 8.88% | approximately zero |
| 12% | USD 65,140 |
| 18% | USD 245,140 |

Real option PnL will also reflect the entry spread, discrete hedge fills, pre-event surface repricing, post-event volatility collapse, skew, and any difference between the assumed and realized event time.

## Key Risk Measures and Sensitivities
- Spot delta, gamma, vega, theta, vanna, volga, and charm by expiry and strike.
- Parallel volatility, skew, smile curvature, and term-structure bucket shocks.
- Forward-variance and event-variance exposure rather than only raw vega.
- Gap scenarios combining spot jump, skew rotation, post-event volatility, and bid-ask widening.
- Dispersion correlation exposure and constituent/index basis risk.
- Realized-versus-implied variance accrual under the exact sampling convention.
- Hedge slippage, overnight delta, pin risk, early exercise, and assignment exposure.
- Liquidity indicators: spread, displayed size, open interest, quote age, and days to exit.

Daily PnL should separate spot/delta, realized gamma, surface level, skew, term roll, event-variance repricing, theta/carry, hedge trading, fees, lifecycle events, and residual. A falling headline implied volatility can coexist with positive PnL if the position owns the relevant forward or event variance.

Short volatility should be evaluated as an asymmetric distribution, not described only by its average carry. A strategy can collect small theta amounts across many quiet observations and lose several months or years of carry in one jump, volatility-surface dislocation, or failed hedge. The local loss grows quadratically with the move; beyond the local region, full repricing and option payoff bounds take over.

Tail-first sizing starts with a scenario set $\mathcal S$ that includes gaps, skew rotations, volatility jumps, wider execution, delayed hedging, and any market closure or price-limit state. If $L_{\max}$ is the allowed loss and $\operatorname{PnL}_{1}(s)$ is the full-revalued PnL of one trade unit, a basic hard cap is:

$$
N_{\max}
=
\left\lfloor
\frac{L_{\max}}
{\max_{s\in\mathcal S}\left[-\operatorname{PnL}_{1}(s)\right]}
\right\rfloor.
$$

Apply concentration, liquidity, model-risk, and wrong-way-risk add-ons after this calculation. Premium received, historical hit rate, and normal-day theta do not increase $L_{\max}$ automatically.

## Required Data, Curves, Surfaces, and Calibration Objects
A useful option-quote record includes `instrument_id`, underlying, venue, timestamp, expiry timestamp, strike, call/put, exercise and settlement style, multiplier, bid, ask, sizes, last trade, open interest, and deliverable version. Retain raw and normalized symbols.

An event record should include `event_id`, entity or macro series, event type, announced-at time, expected event time, confidence/status, source, revision time, and the trading session affected. Never overwrite a rescheduled event; append a new version so historical research remains point-in-time correct.

Surface snapshots need:

- spot, discount curve, forward, dividends, borrow, and funding inputs;
- cleaned quotes with exclusion reasons;
- implied volatilities or option prices on a documented coordinate system;
- calibration method, parameters, fit residuals, and no-arbitrage diagnostics;
- calendar and corporate-action versions;
- publish time and the latest source timestamp included.

Realized-volatility data needs unadjusted and adjusted prices, session calendars, sample timestamps, corporate-action handling, and a late/corrected-print policy. Event studies also need the information-availability timestamp, not only the economic effective date.

## Numerical and Implementation Approaches
Use a staged pipeline: normalize contracts, construct forwards, reject invalid quotes, fit each expiry, enforce or diagnose butterfly arbitrage, then join expiries with calendar controls. Preserve every intermediate artifact for replay.

Represent total variance as the primary term-structure object. Infer diffuse variance from neighboring non-event intervals, a cross-sectional peer model, or a jointly calibrated event-aware surface. Compare methods; a single adjacent expiry can contain its own supply-demand distortion.

Build an event engine that maps each event version to affected sessions and expiries. Scenario rows should specify spot jump, post-event surface, passage of time, dividend/borrow changes, liquidity haircut, and hedge execution assumptions. Full-revalue the actual legs under every scenario.

Backtests must use quotes and event timestamps available at the simulated decision time. Execute at bid/ask or a documented fill model, include delta-hedge turnover, and test sensitivity to delayed entry, wider spreads, and revised event dates.

## Production Pitfalls and Sanity Checks
- Subtracting implied volatilities instead of total variances to infer forward or event risk.
- Treating an event date scraped today as if it had been known historically.
- Mapping an after-close event to an option that expires earlier that session.
- Comparing delta-matched options whose delta conventions or forwards differ.
- Fitting stale, crossed, zero-bid, or corporate-action-adjusted contracts as ordinary quotes.
- Inferring a negative event variance and silently flooring it without alerting on the cause.
- Using a smooth surface that violates monotonicity in total variance or convexity in strike.
- Pricing from mid while assuming all hedges execute at mid during a gap.
- Calling a trade delta-neutral while ignoring vanna, charm, discrete hedging, and overnight gap delta.
- Attributing all post-event volatility collapse to theta instead of an explicit event-variance factor.
- Comparing model theta with a one-day roll whose curves, forwards, surface coordinates, or event flags changed.
- Annualizing realized moves on 252 sessions while charging theta on a 365-day clock without a documented bridge.
- Sizing short-gamma carry from a normal-return covariance matrix while omitting gap and unavailable-hedge states.

Minimum controls include put-call parity residuals, nonnegative calendar forward variance, monotone/convex call-price checks, surface residuals versus bid-ask, quote-age limits, event-version reconciliation, scenario price bounds, theta-gamma reconciliation on a common clock, explicit holiday/weekend roll tests, tail-loss limits with delayed hedges, and actual-versus-explained PnL.

## Illustrative Code
```python
from dataclasses import dataclass
from math import sqrt


@dataclass(frozen=True)
class EventVarianceEstimate:
    event_variance: float
    implied_log_move: float


def infer_event_variance(
    t_before: float,
    vol_before: float,
    t_after: float,
    vol_after: float,
    diffuse_vol: float,
) -> EventVarianceEstimate:
    if not 0.0 < t_before < t_after:
        raise ValueError("expiries must be positive and ordered")
    if min(vol_before, vol_after, diffuse_vol) < 0.0:
        raise ValueError("volatilities must be non-negative decimals")

    total_before = vol_before * vol_before * t_before
    total_after = vol_after * vol_after * t_after
    diffuse_between = diffuse_vol * diffuse_vol * (t_after - t_before)
    event_variance = total_after - total_before - diffuse_between
    if event_variance < 0.0:
        raise ValueError("negative event variance: inspect quotes, forwards, and baseline")
    return EventVarianceEstimate(event_variance, sqrt(event_variance))


def event_variance_pnl(
    variance_notional: float,
    realized_log_jump: float,
    implied_event_variance: float,
) -> float:
    return variance_notional * (
        realized_log_jump * realized_log_jump - implied_event_variance
    )
```

## References and Further Reading
- [Cboe Volatility Index Mathematics Methodology](https://cdn.cboe.com/resources/indices/Cboe_Volatility_Index_Mathematics_Methodology.pdf) for option-strip implied-variance construction.
- Carr and Madan. “Towards a Theory of Volatility Trading,” in *Volatility* (1998).
- Demeterfi, Derman, Kamal, and Zou. “More Than You Ever Wanted to Know About Volatility Swaps” (1999).
- Gatheral. *The Volatility Surface: A Practitioner's Guide*.
- Sinclair. *Volatility Trading*.
- Leung and Santoli. [“Accounting for Earnings Announcements in the Pricing of Equity Options”](https://doi.org/10.1142/S2345768614500165).
- [Official exchange volatility-index mathematics methodology](https://cdn.cboe.com/resources/indices/Cboe_Volatility_Index_Mathematics_Methodology.pdf).
- Related material: [18-volatility-products.md](18-volatility-products.md), [examples/event-volatility-implied-move.md](examples/event-volatility-implied-move.md), and [examples/theta-gamma-daily-breakeven.md](examples/theta-gamma-daily-breakeven.md).
