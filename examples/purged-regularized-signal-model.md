# Purged Regularized Signal Model

Related chapters: [../46-machine-learning-and-deep-learning-for-trading.md](../46-machine-learning-and-deep-learning-for-trading.md), [../44-robust-portfolio-and-research-validation.md](../44-robust-portfolio-and-research-validation.md), and [../40-point-in-time-data-and-event-systems.md](../40-point-in-time-data-and-event-systems.md).

This example combines three controls that belong together:

1. define every label by its information-realization interval;
2. purge overlapping labels and apply any justified embargo;
3. fit scaling and regularization only on the surviving training rows.

## Fold Construction

Suppose a research fold tests observations whose labels use returns from day 10 through day 14, inclusive. Candidate training observations include:

| Row | Feature day | Label interval | Fold treatment | Reason |
| --- | ---: | --- | --- | --- |
| A | 3 | [4, 6] | Train | Label finishes before test information |
| B | 5 | [6, 9] | Train | Label finishes before test information |
| C | 7 | [8, 10] | Purge | Label overlaps test at day 10 |
| D | 9 | [10, 12] | Purge | Label overlaps test |
| E | 12 | [13, 15] | Test/purge | Inside or overlapping test |
| F | 15 | [16, 18] | Embargo | Feature day is in a two-day post-test embargo |
| G | 17 | [18, 20] | Eligible only for two-sided research CV | Outside purge and embargo |

If the embargo runs through day 16, row F is excluded even though its label begins after the test interval. Row G can be used in a symmetric purged research fold, but not in a production-style walk-forward fit for a decision on day 10: it is future history. Purging controls label overlap; it does not permit training on the future.

The overlap rule for closed intervals $[a,b]$ and $[c,d]$ is:

```math
a\leq d\quad\text{and}\quad c\leq b
```

Persist the endpoint convention. If a return interval is half-open, the boundary comparison changes.

## Ridge Calculation

After fold construction, assume the training-only transformation produces two centered, standardized features:

- $x_1$: momentum;
- $x_2$: value.

The centered training matrix and target, measured in basis points, are:

```math
X=
\begin{bmatrix}
1&1\\
1&-1\\
-1&1\\
-1&-1
\end{bmatrix},
\qquad
y=
\begin{bmatrix}
30\\
10\\
-10\\
-30
\end{bmatrix}
```

Then:

```math
X^\top X=
\begin{bmatrix}
4&0\\
0&4
\end{bmatrix},
\qquad
X^\top y=
\begin{bmatrix}
80\\
40
\end{bmatrix}
```

With ridge penalty $\lambda=4$:

```math
\widehat\beta
=
(X^\top X+\lambda I)^{-1}X^\top y
=
\begin{bmatrix}
10\\
5
\end{bmatrix}
\text{ bp}
```

For a new point with standardized features $(0.5,-0.2)$:

```math
\widehat y
=
(0.5)(10)+(-0.2)(5)
=
4\text{ bp}
```

If round-trip costs are 6 bp and the uncertainty buffer is 2 bp, the deployable edge is:

```math
4-6-2=-4\text{ bp}
```

so the correct action is no trade. Regularization is judged through net decisions, not by whether it produces a nonzero forecast.

## Nested Selection Protocol

For a real study:

1. reserve a chronological outer fold;
2. create inner chronological folds entirely within the outer training history;
3. for each candidate $\lambda$, purge label overlap and apply the documented embargo in every inner fold;
4. fit imputation, scaling, clipping, and the ridge model on each inner-training fold;
5. score inner out-of-fold predictions using the intended cost-aware metric;
6. select $\lambda$ without consulting the outer fold;
7. refit the locked pipeline on permitted outer-training history;
8. evaluate the outer fold once and retain all trial records.

The cost model, decision threshold, feature set, and embargo are hyperparameters if they were varied. They belong in the trial count.

## Illustrative Code

The following code implements closed-interval purging and a compact ridge fit. Future training rows are disabled by default for a chronological outer holdout; the opt-in two-sided mode exists only for explicitly declared research cross-validation. Scaling parameters are estimated from the supplied training rows only.

```python
from dataclasses import dataclass
import math
from numbers import Integral


@dataclass(frozen=True)
class Observation:
    feature_time: int
    label_start: int
    label_end: int
    features: tuple[float, ...]
    target: float


@dataclass(frozen=True)
class RidgeModel:
    means: tuple[float, ...]
    scales: tuple[float, ...]
    target_mean: float
    coefficients: tuple[float, ...]


def overlaps(left_start: int, left_end: int,
             right_start: int, right_end: int) -> bool:
    return left_start <= right_end and right_start <= left_end


def purged_indices(
    observations: list[Observation],
    test_indices: set[int],
    embargo_end: int,
    allow_future_training: bool = False,
) -> list[int]:
    if not test_indices:
        raise ValueError("test_indices cannot be empty")
    if any(
        not isinstance(i, Integral)
        or isinstance(i, bool)
        or i < 0
        or i >= len(observations)
        for i in test_indices
    ):
        raise ValueError("test index is out of range")
    if not isinstance(allow_future_training, bool):
        raise ValueError("allow_future_training must be boolean")
    if (
        not isinstance(embargo_end, Integral)
        or isinstance(embargo_end, bool)
    ):
        raise ValueError("embargo_end must be a finite integer")
    for observation in observations:
        timestamps = (
            observation.feature_time,
            observation.label_start,
            observation.label_end,
        )
        if any(
            not isinstance(value, Integral) or isinstance(value, bool)
            for value in timestamps
        ):
            raise ValueError("observation timestamps must be finite integers")
        if (
            observation.feature_time > observation.label_start
            or observation.label_start > observation.label_end
        ):
            raise ValueError("observation timestamps are not chronologically ordered")
        if not all(
            math.isfinite(value)
            for value in (*observation.features, observation.target)
        ):
            raise ValueError("features and targets must be finite")
    test_intervals = [
        (observations[i].label_start, observations[i].label_end)
        for i in test_indices
    ]
    first_test_feature = min(observations[i].feature_time for i in test_indices)
    first_test_start = min(start for start, _ in test_intervals)
    last_test_end = max(end for _, end in test_intervals)
    if allow_future_training and embargo_end < last_test_end:
        raise ValueError("embargo_end cannot precede the test-label window")
    kept: list[int] = []

    for i, candidate in enumerate(observations):
        if i in test_indices:
            continue
        if not allow_future_training:
            if (
                candidate.feature_time >= first_test_feature
                or candidate.label_end >= first_test_start
            ):
                continue
        label_overlap = any(
            overlaps(
                candidate.label_start,
                candidate.label_end,
                test_start,
                test_end,
            )
            for test_start, test_end in test_intervals
        )
        test_or_embargo_window = (
            allow_future_training
            and first_test_feature <= candidate.feature_time <= embargo_end
        )
        if not label_overlap and not test_or_embargo_window:
            kept.append(i)
    return kept


def solve_linear_system(
    matrix: list[list[float]],
    vector: list[float],
) -> list[float]:
    n = len(vector)
    if n == 0 or len(matrix) != n or any(len(row) != n for row in matrix):
        raise ValueError("square matrix and aligned vector required")
    if not all(
        math.isfinite(value)
        for row in matrix
        for value in row
    ) or not all(math.isfinite(value) for value in vector):
        raise ValueError("linear-system inputs must be finite")
    augmented = [matrix[i][:] + [vector[i]] for i in range(n)]
    for column in range(n):
        pivot = max(range(column, n), key=lambda row: abs(augmented[row][column]))
        if abs(augmented[pivot][column]) < 1e-12:
            raise ValueError("singular system")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        pivot_value = augmented[column][column]
        augmented[column] = [value / pivot_value for value in augmented[column]]
        for row in range(n):
            if row == column:
                continue
            multiple = augmented[row][column]
            augmented[row] = [
                value - multiple * pivot_row_value
                for value, pivot_row_value
                in zip(augmented[row], augmented[column])
            ]
    return [augmented[row][-1] for row in range(n)]


def fit_ridge(
    feature_rows: list[tuple[float, ...]],
    targets: list[float],
    penalty: float,
) -> RidgeModel:
    if not feature_rows or len(feature_rows) != len(targets):
        raise ValueError("aligned non-empty data required")
    if not math.isfinite(penalty) or penalty < 0.0:
        raise ValueError("penalty must be non-negative")
    width = len(feature_rows[0])
    if width == 0 or any(len(row) != width for row in feature_rows):
        raise ValueError("inconsistent feature dimensions")
    if not all(
        math.isfinite(value)
        for row in feature_rows
        for value in row
    ) or not all(math.isfinite(target) for target in targets):
        raise ValueError("training data must be finite")

    count = len(feature_rows)
    means = tuple(
        sum(row[j] for row in feature_rows) / count for j in range(width)
    )
    scales = tuple(
        math.sqrt(
            sum((row[j] - means[j]) ** 2 for row in feature_rows) / count
        )
        for j in range(width)
    )
    if any(scale <= 0.0 for scale in scales):
        raise ValueError("constant feature in training fold")

    standardized = [
        tuple((row[j] - means[j]) / scales[j] for j in range(width))
        for row in feature_rows
    ]
    target_mean = sum(targets) / count
    centered_targets = [target - target_mean for target in targets]

    gram = [[0.0 for _ in range(width)] for _ in range(width)]
    cross = [0.0 for _ in range(width)]
    for row, target in zip(standardized, centered_targets):
        for j in range(width):
            cross[j] += row[j] * target
            for k in range(width):
                gram[j][k] += row[j] * row[k]
    for j in range(width):
        gram[j][j] += penalty

    coefficients = tuple(solve_linear_system(gram, cross))
    return RidgeModel(means, scales, target_mean, coefficients)


def predict(model: RidgeModel, features: tuple[float, ...]) -> float:
    if len(features) != len(model.coefficients):
        raise ValueError("feature dimension mismatch")
    model_values = (
        *model.means,
        *model.scales,
        model.target_mean,
        *model.coefficients,
        *features,
    )
    if not all(math.isfinite(value) for value in model_values):
        raise ValueError("model and feature values must be finite")
    if any(scale <= 0.0 for scale in model.scales):
        raise ValueError("model scales must be positive")
    standardized = [
        (value - mean) / scale
        for value, mean, scale in zip(features, model.means, model.scales)
    ]
    return model.target_mean + sum(
        coefficient * value
        for coefficient, value in zip(model.coefficients, standardized)
    )


ridge_example = fit_ridge(
    [(1.0, 1.0), (1.0, -1.0), (-1.0, 1.0), (-1.0, -1.0)],
    [30.0, 10.0, -10.0, -30.0],
    penalty=4.0,
)
assert all(
    abs(actual - expected) < 1e-12
    for actual, expected in zip(ridge_example.coefficients, (10.0, 5.0))
)
assert abs(predict(ridge_example, (0.5, -0.2)) - 4.0) < 1e-12
```

## Checks Before Trusting the Result

- Verify every feature availability timestamp is no later than its decision timestamp.
- Print purged and embargoed row IDs for every fold.
- Confirm transformations differ when training windows differ.
- Confirm the outer test has no influence on feature selection, penalty, cost model, or threshold.
- Compare ridge with an intercept-only forecast, OLS, and a simple trading rule.
- Report fold dispersion, coefficient stability, turnover, cost sensitivity, and capacity.
- Recalculate PnL from lagged executed positions and actual fills.
- Retain the dataset, fold, transform, model, and trial manifests needed to reproduce the decision.
