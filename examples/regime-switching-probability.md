# Two-State Regime Probability Update

Related chapter: [../18-volatility-products.md](../18-volatility-products.md).

Suppose a two-state model has:
- State 1: calm market
- State 2: stressed market
- Current probability of calm state: 70%
- Probability of staying calm: $p_{11} = 0.90$
- Probability of moving from stress to calm: $p_{21} = 0.25$

The next-period probability of the calm state is:

$$
P(S_{t+1}=1) = P(S_t=1)p_{11} + P(S_t=2)p_{21}
$$

```python
current_calm_probability = 0.70
p11 = 0.90
p21 = 0.25

next_calm_probability = current_calm_probability * p11 + (1.0 - current_calm_probability) * p21
```

Result:

$$
0.70 \times 0.90 + 0.30 \times 0.25 = 0.705
$$

So the one-step-ahead calm-regime probability is 70.5%.

Implementation notes:
- In live systems, use filtered probabilities based only on information available at the time.
- Smoothed probabilities use future observations and can introduce look-ahead bias in backtests.
- State labels are model interpretations; the model estimates probabilities, not absolute truth.
