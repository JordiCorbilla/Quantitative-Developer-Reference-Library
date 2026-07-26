# Portfolio Risk Budgeting

Related chapters: [../16-portfolio-construction-and-backtesting.md](../16-portfolio-construction-and-backtesting.md) and [../44-robust-portfolio-and-research-validation.md](../44-robust-portfolio-and-research-validation.md).

Assume two uncorrelated assets have annualized volatilities of \(10\%\) and \(20\%\). Inverse-volatility weights are:

$$
w_1
=
\frac{1/0.10}{1/0.10+1/0.20}
=
\frac{2}{3},
\qquad
w_2=\frac{1}{3}.
$$

The covariance matrix is:

$$
\Sigma=
\begin{bmatrix}
0.10^2 & 0\\
0 & 0.20^2
\end{bmatrix}.
$$

Portfolio volatility is:

$$
\sigma_p
=
\sqrt{w^\top\Sigma w}
=
\sqrt{\frac{4}{9}(0.10)^2+\frac{1}{9}(0.20)^2}
\approx9.43\%.
$$

Volatility contribution is:

$$
RC_i=w_i\frac{(\Sigma w)_i}{\sigma_p}.
$$

Both contributions are approximately \(4.71\%\), half of portfolio volatility.

```python
from math import sqrt

volatility = [0.10, 0.20]
inverse = [1.0 / value for value in volatility]
weights = [value / sum(inverse) for value in inverse]
covariance = [[0.10**2, 0.0], [0.0, 0.20**2]]

marginal_variance = [
    sum(covariance[i][j] * weights[j] for j in range(2))
    for i in range(2)
]
portfolio_variance = sum(
    weights[i] * marginal_variance[i]
    for i in range(2)
)
portfolio_volatility = sqrt(portfolio_variance)
risk_contributions = [
    weights[i] * marginal_variance[i] / portfolio_volatility
    for i in range(2)
]

assert round(weights[0], 6) == round(2.0 / 3.0, 6)
assert round(weights[1], 6) == round(1.0 / 3.0, 6)
assert abs(sum(risk_contributions) - portfolio_volatility) < 1e-12
assert abs(risk_contributions[0] - risk_contributions[1]) < 1e-12
```

Inverse-volatility weights coincide with equal risk contribution in this simple diagonal two-asset case. They are not generally exact risk-parity weights when correlations and multiple assets interact. Production allocation also needs expected costs, leverage, liquidity, factor exposure, stress loss, and weight-stability checks.
