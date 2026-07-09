# Convertibles and Equity-Linked Notes

Related chapters: [01-options.md](01-options.md), [03-equities.md](03-equities.md), [05-fixed-income.md](05-fixed-income.md), [07-credit.md](07-credit.md), and [18-volatility-products.md](18-volatility-products.md).

## What This Domain Covers
A convertible bond is a bond with an embedded equity option.

The holder owns credit and rate exposure through the bond floor, plus equity upside through the right to convert into shares. That hybrid nature is what makes convertibles useful and difficult. The same instrument responds to equity price, volatility, credit spread, rates, dividends, borrow, calls, puts, and conversion terms.

Equity-linked notes use similar building blocks: a debt host plus payoff exposure to a stock, index, basket, or option strategy. This chapter treats them as hybrid instruments where fixed-income and equity-option logic must agree.

## Product Taxonomy and Market Structure
Start by identifying the embedded equity right and issuer features.

- Convertible bonds.
- Mandatory convertibles.
- Exchangeable bonds.
- Callable and puttable convertibles.
- Equity-linked notes and reverse convertibles.
- Autocallable or barrier-linked notes where equity exposure is embedded in a note.

## Quoting and Market Conventions
- Conversion ratio defines how many shares the bond can convert into.
- Conversion price equals par divided by conversion ratio.
- Parity is the value of shares received on conversion.
- Bond floor is the value of the debt component without conversion upside.
- Issuer call schedules, investor put dates, dividend protection, and make-whole terms matter.
- Borrow cost and stock-loan availability affect hedge economics.

## Core Pricing Framework
A convertible is often decomposed conceptually as:

$$
\text{Convertible Value} \approx \text{Bond Floor} + \text{Equity Option Value} + \text{Issuer/Investor Feature Value}
$$

Parity is:

$$
\text{Parity} = S \times \text{Conversion Ratio}
$$

Conversion premium is:

$$
\frac{\text{Convertible Price} - \text{Parity}}{\text{Parity}}
$$

Production valuation often uses trees, finite-difference methods, or Monte Carlo methods because credit, calls, puts, dividends, and early conversion interact.

## Worked Instrument Example: Conversion Parity
Assume:
- bond par: USD 1,000,
- conversion ratio: 20 shares,
- stock price: USD 45,
- convertible price: USD 1,050.

Parity is:

$$
45 \times 20 = 900
$$

The conversion price is:

$$
\frac{1{,}000}{20} = 50
$$

The conversion premium is:

$$
\frac{1{,}050 - 900}{900} = 16.7\%
$$

The holder is paying above immediate equity parity because the instrument still has bond value, optionality, and time value.

## Key Risk Measures and Sensitivities
- Equity delta and gamma.
- Credit spread sensitivity and jump-to-default exposure.
- Interest-rate duration and curve risk.
- Vega and skew sensitivity.
- Dividend and borrow sensitivity.
- Call, put, and conversion-boundary sensitivity.

## Required Data, Curves, Surfaces, and Calibration Objects
- Bond terms, coupon schedule, maturity, call/put schedule, and covenants.
- Conversion ratio, conversion price, dividend protection, and corporate-action rules.
- Stock price, dividends, borrow, and volatility surface.
- Issuer credit curve or spread assumptions.
- Discount curve and recovery assumptions.

## Numerical and Implementation Approaches
- Start with parity, bond floor, and simple call-option intuition.
- Use lattice or PDE methods when early conversion and issuer calls matter.
- Make corporate-action adjustment rules explicit.
- Separate credit assumptions from equity-volatility assumptions.
- Reconcile hedge ratios to realized convertible-arbitrage PnL.

## Production Pitfalls and Sanity Checks
- Ignoring call schedules that cap upside.
- Treating conversion ratio as static through corporate actions.
- Using equity vol without considering credit-equity correlation.
- Missing borrow cost in hedged convertible strategies.
- Reporting delta without clarifying bond-price, parity, or share-equivalent basis.

## Illustrative Code
```python
def convertible_parity(stock_price: float, conversion_ratio: float) -> float:
    return stock_price * conversion_ratio


def conversion_price(par: float, conversion_ratio: float) -> float:
    if conversion_ratio <= 0.0:
        raise ValueError("conversion_ratio must be positive")
    return par / conversion_ratio
```

## References and Further Reading
- Calamos. *Convertible Securities*
- Tsiveriotis and Fernandes on convertible bond valuation
- Issuer offering memoranda and convertible bond term sheets
