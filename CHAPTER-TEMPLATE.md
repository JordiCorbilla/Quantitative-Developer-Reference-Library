# Chapter Title

Related chapters: [00-overview.md](00-overview.md).

## What This Domain Covers
Open with the practitioner's problem: who uses the product or method, what decision they are trying to make, and what can go wrong. Then tell the chapter as one continuous workflow:

**contract or question -> quote and data -> model or signal -> worked example -> hedge or decision -> lifecycle controls**

Define each idea before introducing its formula. After every important formula, translate the result back into plain language and state the assumptions that make it valid.

## Product Taxonomy and Market Structure
- Main product or workflow categories.
- Market participants, venues, or workflow boundaries where relevant.
- Important distinctions that change pricing, risk, or implementation.

## Quoting and Market Conventions
- Quote units and market-standard formats.
- Calendars, day-counts, settlement, multipliers, or benchmark definitions.
- Any convention that can silently change results.

## Core Pricing Framework
Introduce the core valuation, risk, or workflow equation. Keep it practical and tie it to implementation inputs.

## Worked Instrument Example
Use a compact numerical example when it helps anchor the chapter. Carry one set of inputs through the calculation, interpret the answer in market units, and end with the decision or control the number informs. Label hypothetical names and data as illustrative.

## Key Risk Measures and Sensitivities
- First-order and second-order risk measures.
- Scenario or stress measures.
- Operational or data-quality risk indicators where relevant.

## Required Data, Curves, Surfaces, and Calibration Objects
- Market data.
- Static data.
- Model or calibration objects.
- Trade, position, or workflow metadata.

## Numerical and Implementation Approaches
- Recommended decomposition.
- Data structures or services that should be explicit.
- Approximation choices and when they are acceptable.

## Production Pitfalls and Sanity Checks
- Common implementation errors.
- Reconciliation checks.
- Data and convention traps.
- Scope limits: distinguish identities from approximations, model outputs from observations, and illustrative examples from empirical claims.

## Illustrative Code
```python
def example() -> None:
    pass
```

## References and Further Reading
- Practitioner documentation and textbooks.
- Related chapters.
