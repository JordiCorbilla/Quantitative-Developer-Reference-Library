# Equity Swaps and Total Return Swaps

Related chapters: [03-equities.md](03-equities.md), [04-fx.md](04-fx.md), [09-cross-asset.md](09-cross-asset.md), [13-risk-and-pnl.md](13-risk-and-pnl.md), and [19-financing-repo-and-securities-lending.md](19-financing-repo-and-securities-lending.md).

## What This Domain Covers
An equity swap lets one party receive equity performance without directly owning the shares.

In a total return swap, one leg pays the total return of an asset: price move plus dividends or coupons. The other leg usually pays financing, such as overnight rate plus spread. The economic story is synthetic ownership funded through a swap.

These instruments are common in prime brokerage, hedge funds, financing, synthetic index exposure, and balance-sheet management. For a quant developer, the key is to model the equity leg, financing leg, resets, dividends, collateral, and counterparty exposure consistently.

## Product Taxonomy and Market Structure
Start by asking what return is transferred.

- Single-name equity swaps.
- Index total return swaps.
- Basket swaps.
- Bond or loan total return swaps.
- Funded vs unfunded swaps.
- Price-return vs total-return structures.

## Quoting and Market Conventions
- Equity leg may be price return or total return.
- Financing leg may reference SOFR, ESTR, SONIA, or another overnight/index rate plus spread.
- Reset frequency determines when notional or equity quantity is refreshed.
- Dividends, withholding tax, corporate actions, and borrow cost affect economics.
- Collateral, margin, and close-out terms matter for counterparty exposure.

## Core Pricing Framework
At a high level, the swap value is:

$$
\text{TRS Value} = PV(\text{equity total return leg}) - PV(\text{financing leg})
$$

For one period, an equity total return leg can be approximated as:

$$
N \times \left(\frac{S_1 - S_0}{S_0} + \text{dividend yield over period}\right)
$$

The financing leg is:

$$
N \times (\text{reference rate} + \text{spread}) \times \text{year fraction}
$$

## Worked Instrument Example: One-Period Equity TRS
Assume:
- notional: USD 10m,
- stock return over period: 4%,
- dividend return: 1%,
- financing cost: 2%.

Equity total return is:

$$
10{,}000{,}000 \times (4\% + 1\%) = 500{,}000
$$

Financing leg is:

$$
10{,}000{,}000 \times 2\% = 200{,}000
$$

Net receiver-of-equity-return PnL is:

$$
500{,}000 - 200{,}000 = 300{,}000
$$

## Key Risk Measures and Sensitivities
- Equity delta and beta.
- Dividend sensitivity.
- Financing spread and rate sensitivity.
- Borrow and short-rebate sensitivity.
- Counterparty exposure and wrong-way risk.
- Reset, gap, and corporate-action risk.

## Required Data, Curves, Surfaces, and Calibration Objects
- Underlying price, corporate actions, dividends, and index membership where relevant.
- Financing curve and spread terms.
- Reset schedule, payment schedule, and day count.
- Collateral and CSA terms.
- FX rates for cross-currency or non-base exposures.

## Numerical and Implementation Approaches
- Represent equity leg and financing leg separately.
- Make total-return vs price-return convention explicit.
- Model resets as lifecycle events, not just valuation-date recalculations.
- Reuse equity ledger logic for dividends and corporate actions.
- Track exposure profiles for xVA and collateral workflows.

## Production Pitfalls and Sanity Checks
- Dropping dividends from a total-return leg.
- Applying price-return index data to a total-return swap.
- Ignoring withholding tax or dividend adjustment language.
- Missing notional resets or reset-date fixings.
- Treating TRS exposure as identical to direct share ownership without funding and counterparty effects.

## Illustrative Code
```python
def one_period_trs_pnl(notional: float, price_return: float, dividend_return: float, financing_return: float) -> float:
    equity_leg = notional * (price_return + dividend_return)
    financing_leg = notional * financing_return
    return equity_leg - financing_leg
```

## References and Further Reading
- Prime brokerage and equity derivatives product documentation
- ISDA equity derivatives definitions
- Equity swap and total return swap term sheets
