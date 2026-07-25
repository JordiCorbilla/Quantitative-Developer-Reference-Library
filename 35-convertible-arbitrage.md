# Convertible Arbitrage

Related chapters: [01-options.md](01-options.md), [03-equities.md](03-equities.md), [05-fixed-income.md](05-fixed-income.md), [07-credit.md](07-credit.md), [13-risk-and-pnl.md](13-risk-and-pnl.md), [18-volatility-products.md](18-volatility-products.md), [19-financing-repo-and-securities-lending.md](19-financing-repo-and-securities-lending.md), and [25-convertibles-and-equity-linked-notes.md](25-convertibles-and-equity-linked-notes.md).

## What This Domain Covers
Convertible arbitrage treats a hybrid security as credit, rates, equity optionality, contractual events, and financing. A common position is long a convertible bond and short underlying shares, controlling first-order equity exposure while retaining convexity, volatility, credit, carry, and terms risk.

“Arbitrage” is market terminology, not a promise of riskless profit. A delta-hedged convertible can lose through default, spread widening, volatility collapse, issuer calls, borrow recall, dividends, model error, liquidity gaps, or transaction costs. Dynamic hedging only monetizes convexity when realized stock movement is sufficient to overcome theta and frictions.

The implementation must parse legal terms, build state-dependent valuation, calculate share-equivalent Greeks, maintain borrow and financing, process corporate actions, rebalance hedge lots, and explain bond-plus-stock PnL.

## Product Taxonomy and Market Structure
- **Plain convertible bond:** optional conversion into a fixed or adjustable number of shares.
- **Exchangeable bond:** converts into shares of an entity other than the debt issuer.
- **Mandatory convertible:** conversion is required, often with different ratios across price regions.
- **Callable or puttable convertible:** issuer call and investor put rights interact with conversion.
- **Contingent convertible:** conversion eligibility depends on stock-price, trading-price, capital, or other triggers.
- **Resettable or dividend-protected convertible:** conversion price or ratio changes according to contractual formulas.
- **Synthetic convertible:** debt and listed or OTC equity options assembled to resemble the hybrid exposure.

The bond normally trades over the counter; its hedge may trade on exchange or through derivatives. Locates, borrow term, rebate, manufactured dividends, margin, financing, and short-sale proceeds determine realized economics.

## Quoting and Market Conventions
- Convertible price is commonly quoted in points per 100 of par, normally clean. Settlement adds accrued interest.
- Conversion ratio \(CR\) is shares received per bond. Conversion price is \(\text{par}/CR\).
- Parity is \(S\times CR\), adjusted for currency and deliverable property where necessary.
- Conversion premium is \((P_{\text{convertible}}-\text{parity})/\text{parity}\).
- Delta must state its basis. “62 delta” may mean 62% of conversion ratio, 12.4 shares per bond with \(CR=20\), or a vendor-specific normalized measure.
- Stock borrow can quote fee or rebate; signs and the treatment of short-sale proceeds differ by agreement.
- Yield-to-maturity, yield-to-put, and yield-to-call depend on clean/full price, day count, settlement, and assumed exercise.
- Calls may require a notice period or a stock-price condition such as 130% of conversion price for 20 of 30 trading days. Make-whole tables can add shares based on call date and stock price.

Terms should be modelled as dated rules, not prose flags. Conversion windows, call tests, puts, dividend adjustments, anti-dilution provisions, merger consideration, cash settlement elections, share caps, and notice periods can all alter the payoff.

## Core Pricing Framework
A useful conceptual decomposition is:

$$
V_{\text{CB}} \approx V_{\text{debt}}
V_{\text{conversion option}}
V_{\text{investor puts}}
-V_{\text{issuer calls}}
V_{\text{other terms}}.
$$

The components are not independent. Default can terminate equity optionality; conversion removes credit exposure; an issuer call changes exercise timing. The Tsiveriotis-Fernandes framework separates a cash-only component exposed to credit from an equity component treated as credit-risk-free:

$$
V = B + E,
$$

and discounts the two components differently. Lattices and finite-difference solvers can implement the coupled problem with discrete dividends and exercise boundaries. More general path-dependent terms may require Monte Carlo with regression-based exercise or a carefully constructed state lattice.

For \(N\) bonds and a model delta expressed as a fraction \(d\) of the conversion ratio, the initial equity hedge is:

$$
Q_{\text{short}} = N\,d\,CR.
$$

After hedging first-order equity exposure, a one-period PnL approximation is:

$$
\Delta\Pi \approx
\frac{1}{2}\Gamma(\Delta S)^2
\text{Vega}\,\Delta\sigma
\text{CS01}\,\Delta s
\text{DV01}\,\Delta r
\Theta\Delta t
\text{coupon}
-\text{borrow}
-\text{funding}
-\text{costs}
+\text{residual}.
$$

Every term must use a declared sign and unit. Gamma may be shares per currency unit per bond; vega may be currency per one volatility point; CS01 may be currency per basis point. Credit-equity cross-effects and changing exercise boundaries make the Taylor explain incomplete in large moves.

### Position and Hedge Logic

1. Resolve all terms from source documents and independently reproduce parity, conversion price, accrued interest, call/put dates, and ratio adjustments.
2. Calibrate rates, credit, dividends, borrow, and the equity volatility surface as separate, versioned objects.
3. Price the bond and compute share-equivalent delta, gamma, vega, CS01, DV01, and scenario values.
4. Short stock to the chosen target delta. A trader may deliberately under- or over-hedge to preserve an equity view, but the target must be recorded.
5. Add rate, credit, FX, or volatility hedges only when they correspond to unwanted risks and remain liquid under stress.
6. Rebalance according to a band, time, or risk threshold that accounts for spread, borrow, and market impact.
7. Run gap scenarios before sizing: default, equity jump, volatility crush, credit widening, call, put, conversion, borrow recall, dividend change, and corporate action.

## Worked Instrument Example
Assume each bond has:

- USD 1,000 par and a 2.5% annual coupon,
- clean price 108, or USD 1,080,
- conversion ratio 20 shares,
- stock price USD 48,
- model delta \(d=0.62\),
- model gamma \(0.18\) shares per USD stock move per bond.

Parity is USD 960, conversion price is USD 50, and conversion premium is:

$$
\frac{1{,}080-960}{960}=12.5\%.
$$

A position of 5,000 bonds has USD 5m face and costs USD 5.4m clean. The delta hedge is:

$$
5{,}000\times0.62\times20=62{,}000\text{ shares short}.
$$

The short market value is USD 2.976m. If short-sale proceeds are credited against the long position, simplified financed capital is USD 2.424m. At 6% funding, 4% stock-borrow fee, and ACT/360, daily carry is approximately:

$$
\frac{5m\times2.5\%-2.424m\times6\%-2.976m\times4\%}{360}
=-388.
$$

Now let the stock rise from USD 48 to USD 50 with all other model inputs unchanged. The initial delta terms cancel. Approximate convexity PnL is:

$$
\frac{1}{2}\times0.18\times(2)^2\times5{,}000
=USD\ 1{,}800.
$$

After one day of carry, approximate PnL before execution costs is USD 1,412.56. Delta rises by \(0.18\times2=0.36\) shares per bond, so restoring neutrality requires another 1,800 shares short. A reversal may monetize that rebalance; execution costs or falling implied volatility can still overwhelm it.

The calculation is reproduced in [examples/convertible-arbitrage-hedge-pnl.md](examples/convertible-arbitrage-hedge-pnl.md).

## Key Risk Measures and Sensitivities
- Share-equivalent equity delta, gamma, and higher-order spot convexity.
- Vega by expiry and strike region; skew, term-structure, and vol-of-vol exposure.
- Credit CS01, hazard-rate sensitivity, jump-to-default, and recovery sensitivity.
- Rate DV01 and key-rate risk; interaction between rates and call/put boundaries.
- Theta, coupon carry, bond financing, stock-borrow fee, rebate, and expected dividends.
- Call probability, soft-call trigger distance, notice-period exposure, put value, and conversion-boundary distance.
- Borrow utilization, days-to-cover, locate concentration, recall probability, and buy-in loss.
- Basis between cash bond, issuer CDS, stock, and listed-option hedges.
- Scenario loss for default with stock gap, new issuance, takeover, special dividend, tender, exchange, or forced conversion.

Default scenarios should value debt recovery, termination of conversion rights, CDS or option hedges, equity-short gain, close-out timing, and borrow settlement together. Capping equity-short gains at the stock price is essential; it cannot offset an arbitrarily large bond loss.

## Required Data, Curves, Surfaces, and Calibration Objects
Legal data includes coupon and maturity; currency; conversion ratio; settlement election; conversion periods; calls, puts, soft-call tests, and notice; make-whole grids; dividend and anti-dilution formulas; resets; contingent conversion; change of control; and deliverable property.

Market and model data includes the full bond quote and accrued interest, equity bid/ask, dividends and corporate actions, equity volatility surface, issuer credit curve, rate and repo curves, FX curves for cross-currency instruments, stock-borrow fee and availability, bond financing, and liquidity reserves.

An implementation should separate:

- `convertible_terms` and immutable document provenance.
- Dated `conversion_window`, `call_rule`, `put_rule`, `ratio_adjustment`, and `make_whole_grid`.
- `corporate_action` with announcement, ex, record, payable, and knowledge timestamps.
- `borrow_contract`, daily inventory, fee/rebate, term, counterparty, and recall state.
- `position_leg` and `hedge_lot` linking each stock execution to its strategy and model delta.
- `market_snapshot`, `model_config`, `valuation_result`, `risk_result`, and `pnl_explain`.

Both effective time and knowledge time are needed. A backtest must not use a special dividend, call notice, or borrow recall before it was known.

## Numerical and Implementation Approaches
- Use a straight-bond and vanilla-option decomposition only as a diagnostic benchmark.
- Use a binomial/trinomial lattice or finite-difference method for coupled credit, conversion, call, and put decisions.
- Represent discrete dividends and trading-day trigger histories explicitly; continuous dividend yield is often inadequate near calls or corporate actions.
- Calibrate equity volatility to liquid options while testing whether the convertible's implied volatility is stable under alternate credit and borrow assumptions.
- Treat recovery, credit-equity dependency, and post-default stock behavior as scenario assumptions, not universally observable parameters.
- Calculate Greeks by stable bumps and compare with algorithmic or analytic sensitivities where available. Bumps must preserve or intentionally recalibrate dependent inputs.
- Backtest hedge rules with executable bid/ask, borrow availability, corporate actions, settlement, and point-in-time terms.
- Return exercise decisions, boundary diagnostics, convergence error, and input lineage with every price.

## Production Pitfalls and Sanity Checks
- Parsing a headline conversion ratio but missing cash settlement, share caps, or make-whole shares.
- Applying corporate-action adjustments on announcement rather than the contractually effective event.
- Treating a soft-call flag as a simple date and ignoring its rolling observation window.
- Reporting “delta” without unit, conversion-ratio basis, or accrued-interest treatment.
- Using today's borrow fee or availability in historical tests.
- Assuming short-sale proceeds are freely available when financing agreements restrict them.
- Omitting manufactured dividends or taxes on the short.
- Calibrating equity volatility while silently changing the credit spread, producing unstable implied vol.
- Using a fixed recovery for a subordinated convertible without checking guarantees and legal entity.
- Double-counting coupon, theta, accrued interest, or financing in PnL.
- Rebalancing on theoretical mid prices with no market impact or locate constraint.
- Failing to cap or validate monotonicity: convertible value should normally be at least a consistently modelled bond floor and should not fall when conversion terms improve, all else equal.

## Illustrative Code
```python
def shares_to_short(
    bond_count: int,
    conversion_ratio: float,
    delta_fraction: float,
) -> float:
    return bond_count * conversion_ratio * delta_fraction


def delta_hedged_gamma_pnl(
    bond_count: int,
    gamma_shares_per_dollar: float,
    stock_move: float,
) -> float:
    return 0.5 * bond_count * gamma_shares_per_dollar * stock_move**2


def new_hedge_after_move(
    old_short: float,
    bond_count: int,
    gamma_shares_per_dollar: float,
    stock_move: float,
) -> float:
    return old_short + bond_count * gamma_shares_per_dollar * stock_move
```

These functions illustrate units; they are not a convertible valuation model.

## References and Further Reading
- Calamos. *Convertible Securities: The Latest Instruments, Portfolio Strategies, and Valuation Analysis*.
- Tsiveriotis and Fernandes. “Valuing Convertible Bonds with Credit Risk.” *Journal of Fixed Income*, 1998.
- Ayache, Forsyth, and Vetzal. “Valuation of Convertible Bonds with Credit Risk.” *Journal of Derivatives*, 2003.
- Ingersoll. “A Contingent-Claims Valuation of Convertible Securities.” *Journal of Financial Economics*, 1977.
- International Securities Lending Association guidance on securities lending and stock borrow.
- The relevant prospectus, indenture, supplemental indenture, pricing term sheet, corporate-action notice, and stock-loan agreement.
