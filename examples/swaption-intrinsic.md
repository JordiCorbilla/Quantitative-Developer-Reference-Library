# Payer Swaption Intrinsic Value Example

Related chapter: [../28-rates-options-caps-floors-swaptions.md](../28-rates-options-caps-floors-swaptions.md).

Assume:
- annuity: USD 4.5m per 1.00 rate unit
- expiry swap rate: 4.20%
- strike: 4.00%

```python
annuity = 4_500_000
swap_rate = 0.042
strike = 0.040

intrinsic = annuity * max(swap_rate - strike, 0.0)
assert abs(intrinsic - 9_000.0) < 1e-9
```

The payer swaption intrinsic value is USD 9,000.
