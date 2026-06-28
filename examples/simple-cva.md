# Simple CVA Example

Related chapter: [../09-cross-asset.md](../09-cross-asset.md).

Assume:
- expected exposure: USD 1,000,000
- one-year marginal default probability: 2%
- recovery rate: 40%
- discount factor: 1.00

Loss given default:

$$
LGD = 1 - 40\% = 60\%
$$

CVA:

$$
1{,}000{,}000 \times 2\% \times 60\% \times 1.00 = 12{,}000
$$

```python
exposure = 1_000_000
marginal_default_probability = 0.02
lgd = 0.60
discount_factor = 1.00

cva = exposure * marginal_default_probability * lgd * discount_factor
```

Interpretation:
- The clean derivative value is reduced by USD 12,000 for expected counterparty default loss.
- Real CVA uses exposure profiles through time, netting, collateral, wrong-way risk, discounting, and calibrated default curves.
