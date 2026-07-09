# Structured Credit Tranche Loss Example

Related chapter: [../24-structured-credit-and-securitization.md](../24-structured-credit-and-securitization.md).

Assume:
- portfolio loss: 5%
- tranche attachment: 3%
- tranche detachment: 7%

```python
def tranche_loss_percent(portfolio_loss: float, attachment: float, detachment: float) -> float:
    width = detachment - attachment
    if width <= 0.0:
        raise ValueError("detachment must exceed attachment")
    return min(max(portfolio_loss - attachment, 0.0), width) / width


loss = tranche_loss_percent(0.05, 0.03, 0.07)
```

The tranche loses 50% because the portfolio loss has moved halfway through the 3%-7% tranche.
