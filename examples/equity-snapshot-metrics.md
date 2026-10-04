# Equity Snapshot Metrics

Related chapter: [03-equities.md](../03-equities.md).

Assume a fictional company has a USD 80 share price, 250m shares outstanding, USD 4.00 trailing EPS, USD 5.00 forecast EPS, and USD 1.20 annual dividend per share.

```math
\text{market cap} = 80 \times 250{,}000{,}000 = \text{USD }20\text{bn}
```

```math
\text{trailing P/E} = \frac{80}{4.00} = 20.0, \qquad
\text{forward P/E} = \frac{80}{5.00} = 16.0
```

```math
\text{dividend yield} = \frac{1.20}{80} = 1.5\%
```

```python
def equity_snapshot_metrics(price: float, shares: float, trailing_eps: float, forecast_eps: float, annual_dividend: float) -> dict[str, float]:
    if price <= 0 or shares <= 0:
        raise ValueError("price and shares must be positive")
    return {
        "market_cap": price * shares,
        "trailing_pe": price / trailing_eps if trailing_eps > 0 else float("nan"),
        "forward_pe": price / forecast_eps if forecast_eps > 0 else float("nan"),
        "dividend_yield": annual_dividend / price,
    }


metrics = equity_snapshot_metrics(80.0, 250_000_000.0, 4.0, 5.0, 1.2)
assert abs(metrics["market_cap"] - 20_000_000_000.0) < 1e-6
assert abs(metrics["trailing_pe"] - 20.0) < 1e-12
assert abs(metrics["forward_pe"] - 16.0) < 1e-12
assert abs(metrics["dividend_yield"] - 0.015) < 1e-12
```

These outputs are descriptors, not an investment recommendation. The next questions are why forecast earnings differ from reported earnings, whether the dividend is sustainable, and how debt, cash flow, dilution, and valuation compare with relevant peers.
