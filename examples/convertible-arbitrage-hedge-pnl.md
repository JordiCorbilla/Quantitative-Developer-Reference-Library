# Convertible-Arbitrage Hedge and PnL

Related chapter: [../35-convertible-arbitrage.md](../35-convertible-arbitrage.md).

This example converts a model delta into a stock hedge and separates convexity from one day of carry. It assumes all credit, rate, volatility, dividend, and legal-term inputs remain unchanged.

Assume each convertible bond has:

- par: USD 1,000,
- clean price: 108 points, or USD 1,080,
- annual coupon: 2.5%,
- conversion ratio: 20 shares,
- stock price: USD 48,
- delta: 0.62 of the conversion ratio,
- gamma: 0.18 shares per USD stock move per bond.

The position contains 5,000 bonds.

## Parity and Initial Hedge

Parity and conversion premium are:

$$
\text{parity}=48\times20=USD\ 960,
$$

$$
\text{premium}=\frac{1{,}080-960}{960}=12.5\%.
$$

Share-equivalent delta per bond is:

$$
0.62\times20=12.4\text{ shares}.
$$

The delta-neutral hedge is therefore:

$$
5{,}000\times12.4=62{,}000\text{ shares short}.
$$

The long convert costs USD 5.4m and the short stock has USD 2.976m market value. For this simplified example, short-sale proceeds offset financing, leaving USD 2.424m of net financed capital.

## One-Day Carry

Assume 6% financing, a 4% stock-borrow fee, and ACT/360:

| Component | Calculation | Daily PnL |
| --- | --- | ---: |
| Coupon accrual | \(5m\times2.5\%/360\) | USD 347.22 |
| Financing | \(-2.424m\times6\%/360\) | USD -404.00 |
| Stock borrow | \(-2.976m\times4\%/360\) | USD -330.67 |
| Net carry | sum | USD -387.44 |

Actual prime-broker treatment may restrict short-sale proceeds or quote a rebate rather than a fee. The agreement, not this simplification, determines carry.

## Stock Move and Rehedge

Let the stock rise USD 2 to USD 50. Initial long-convert delta PnL and short-stock delta PnL cancel. Remaining second-order PnL is approximately:

$$
\frac{1}{2}\times0.18\times(2)^2\times5{,}000
=USD\ 1{,}800.
$$

Approximate PnL after one day of carry and before trading costs is:

$$
1{,}800-387.44=USD\ 1{,}412.56.
$$

Delta per bond increases by:

$$
0.18\times2=0.36\text{ shares}.
$$

Restoring neutrality requires another \(0.36\times5{,}000=1{,}800\) shares short, bringing the hedge to 63,800 shares.

```python
bond_count = 5_000
par = 1_000.0
clean_price_points = 108.0
coupon = 0.025
conversion_ratio = 20.0
stock_price = 48.0
delta_fraction = 0.62
gamma = 0.18  # shares / USD stock move / bond
stock_move = 2.0

convert_cost = bond_count * par * clean_price_points / 100.0
initial_short = bond_count * conversion_ratio * delta_fraction
short_value = initial_short * stock_price
financed_capital = convert_cost - short_value

coupon_carry = bond_count * par * coupon / 360.0
funding_cost = financed_capital * 0.06 / 360.0
borrow_cost = short_value * 0.04 / 360.0
net_carry = coupon_carry - funding_cost - borrow_cost

gamma_pnl = 0.5 * bond_count * gamma * stock_move**2
new_short = initial_short + bond_count * gamma * stock_move
approximate_pnl = gamma_pnl + net_carry

assert initial_short == 62_000
assert new_short == 63_800
assert round(gamma_pnl, 2) == 1_800.00
assert round(approximate_pnl, 2) == 1_412.56
```

This is not a full PnL explain. Production analysis must also include vega and skew, credit CS01, rates, theta, accrued interest, dividends, transaction costs, borrow changes, corporate actions, calls/puts, model recalibration, and residual. A default or borrow-recall scenario requires full revaluation rather than a gamma approximation.
