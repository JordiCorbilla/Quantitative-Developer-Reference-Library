# One-Period Total Return Swap Example

Related chapter: [../26-equity-swaps-and-total-return-swaps.md](../26-equity-swaps-and-total-return-swaps.md).

Assume:
- notional: USD 10m
- price return: 4%
- dividend return: 1%
- financing return: 2%

```python
notional = 10_000_000
price_return = 0.04
dividend_return = 0.01
financing_return = 0.02

equity_leg = notional * (price_return + dividend_return)
financing_leg = notional * financing_return
net_pnl = equity_leg - financing_leg
```

The receiver of total return earns USD 300,000 before other costs and collateral effects.
