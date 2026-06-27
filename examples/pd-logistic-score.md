# Logistic PD Score Example

Related chapter: [../07-credit.md](../07-credit.md).

A simple logistic PD model maps borrower variables to default probability:

$$
PD = \frac{1}{1 + e^{-z}}
$$

where:

$$
z = \beta_0 + \beta_1 x_1 + \beta_2 x_2
$$

Assume:
- intercept: -3.0
- leverage coefficient: 0.8
- delinquency coefficient: 1.2
- leverage score: 1.5
- delinquency flag: 1.0

```python
import math

z = -3.0 + 0.8 * 1.5 + 1.2 * 1.0
pd = 1.0 / (1.0 + math.exp(-z))
```

Result:

$$
z = -0.6
$$

$$
PD \approx 35.4\%
$$

Implementation notes:
- Coefficients and variables must be calibrated on a defined default horizon and default definition.
- This is a toy example; production scorecards require validation, overrides, monitoring, and calibration to observed default rates.
