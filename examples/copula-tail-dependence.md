# Copula Tail Dependence

Related chapter: [32-dependence-modelling-and-copulas.md](../32-dependence-modelling-and-copulas.md).

For a Clayton copula with positive parameter $\theta$:

$$
\lambda_L = 2^{-1/\theta}
$$

At $\theta=2$:

$$
\lambda_L = 2^{-1/2} \approx 0.7071,
\qquad \lambda_U=0
$$

```python
def clayton_lower_tail_dependence(theta: float) -> float:
    if theta <= 0:
        raise ValueError("theta must be positive")
    return 2.0 ** (-1.0 / theta)


value = clayton_lower_tail_dependence(2.0)
assert abs(value - 0.7071067811865476) < 1e-12
```

The coefficient is a limiting conditional probability on the uniform marginal scale. It is not the unconditional probability of a market crash, and it does not validate the marginal loss distributions.
