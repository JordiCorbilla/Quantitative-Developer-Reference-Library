# Hidden Markov Model Filtering Update

Related chapter: [../18-volatility-products.md](../18-volatility-products.md).

Suppose a two-state HMM has:
- State 1: calm market
- State 2: stressed market
- Current filtered probability of calm state: 70%
- Transition probabilities:
  - $p_{11}=0.90$: calm stays calm
  - $p_{12}=0.10$: calm moves to stress
  - $p_{21}=0.25$: stress moves to calm
  - $p_{22}=0.75$: stress stays stressed

First predict next-period state probabilities:

$$
P(S_t=\text{calm}) = 0.70 \times 0.90 + 0.30 \times 0.25 = 0.705
$$

$$
P(S_t=\text{stress}) = 0.70 \times 0.10 + 0.30 \times 0.75 = 0.295
$$

Now assume the new observation is a high-volatility return day. The likelihood of that observation is:
- under calm state: 0.20
- under stressed state: 0.80

Bayes update:

$$
P(\text{calm} \mid y_t) =
\frac{0.705 \times 0.20}{0.705 \times 0.20 + 0.295 \times 0.80}
= 0.374
$$

So the filtered calm probability falls from 70.5% before the observation to 37.4% after observing a high-volatility day.

```python
prior_calm = 0.70
prior_stress = 1.0 - prior_calm

p11 = 0.90
p12 = 0.10
p21 = 0.25
p22 = 0.75

predicted_calm = prior_calm * p11 + prior_stress * p21
predicted_stress = prior_calm * p12 + prior_stress * p22

likelihood_high_vol_given_calm = 0.20
likelihood_high_vol_given_stress = 0.80

normalizer = (
    predicted_calm * likelihood_high_vol_given_calm
    + predicted_stress * likelihood_high_vol_given_stress
)

filtered_calm = predicted_calm * likelihood_high_vol_given_calm / normalizer
filtered_stress = predicted_stress * likelihood_high_vol_given_stress / normalizer
```

Implementation notes:
- Use filtered probabilities for live signals.
- Smoothed probabilities use future observations and should not drive historical trading rules without adjustment.
- State labels such as "calm" and "stress" are interpretations of estimated emissions, not guaranteed truths.
