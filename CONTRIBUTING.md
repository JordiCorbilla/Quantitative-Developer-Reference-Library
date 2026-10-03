# Contributing

This repository is a practitioner reference for quant developers. Contributions should make the library clearer, more useful, or more reliable for people building pricing, risk, market data, execution, and portfolio analytics systems.

## Contribution Standards
- Keep the writing practical. Explain what a concept means for implementation, validation, and production use.
- Prefer short worked examples over long theoretical derivations.
- Tell each chapter as a connected practitioner story: start with the decision or problem, then move through contract or question, quote and data, model or signal, worked example, hedge or decision, and lifecycle controls.
- Define a concept before writing its formula, interpret the result immediately afterward, and state material assumptions next to the claim they qualify.
- Separate facts, identities, model assumptions, heuristics, and illustrative scenarios. Cite primary sources for claims that are empirical, regulatory, convention-dependent, or likely to change.
- Verify bibliographic titles and authors against a publisher or the original paper. For a reviewed claim, link the relevant source beside it; a general reading list alone does not substantiate a specific convention or empirical result.
- Qualify sign rules and monotonicity claims with the model, input coordinates, and parameter domain. Add a counterexample or limit-case check when a common shorthand has a material exception.
- Reconcile examples to full economic value and cashflows before splitting PnL into attribution buckets. Label units and distinguish a price, a payoff, a derivative, and a finite-shock explain.
- Add cross-links when a topic depends on another chapter.
- Use consistent notation with [00-overview.md](00-overview.md).
- Add repository-native SVG diagrams under `assets/` when a visual model materially improves the explanation.
- Do not add screenshots, social-media images, or third-party copyrighted diagrams.

## Chapter Template
New chapters should follow [CHAPTER-TEMPLATE.md](CHAPTER-TEMPLATE.md). Existing chapters use the same contract:

1. What This Domain Covers
2. Product Taxonomy and Market Structure
3. Quoting and Market Conventions
4. Core Pricing Framework
5. Worked Instrument Example where useful
6. Key Risk Measures and Sensitivities
7. Required Data, Curves, Surfaces, and Calibration Objects
8. Numerical and Implementation Approaches
9. Production Pitfalls and Sanity Checks
10. Illustrative Code
11. References and Further Reading

## Diagram Guidelines
- Use SVG so diagrams remain diffable and render directly on GitHub.
- Keep text concise and readable at normal Markdown width.
- Include `<title>` and `<desc>` elements for accessibility.
- Use diagrams to clarify dependency flow, payoff shape, schedule logic, model structure, or control workflow.
- Avoid decorative diagrams that do not add technical understanding.

## Quality Checks
Before opening a PR or committing a large documentation change, run:

```powershell
python scripts/validate_docs.py
python -m pip install -r requirements-validation.txt
python scripts/execute_python_fences.py
```

The execution check runs repository-authored code from the Markdown files. Review incoming documentation changes before running it on an untrusted branch.

The script checks:
- local Markdown links and heading anchors,
- image references,
- SVG XML validity,
- duplicate top-level headings,
- expected chapter sections and narrative openings for numbered chapters,
- balanced code and display-math fences,
- Python snippet syntax,
- an executable Python fence with at least one assertion in every standalone worked example,
- placeholder text and ambiguous numeric currency notation,
- navigation coverage for chapters and worked examples,
- SVG accessibility IDs and duplicate IDs.

## Style Notes
- Use `USD 10m` rather than a bare dollar sign before `10m` in prose to avoid Markdown math ambiguity.
- Use formulas where they clarify implementation, not as decoration.
- If a metric depends on convention, state the convention explicitly.
- If a model has a common failure mode, include it in the production pitfalls section.
