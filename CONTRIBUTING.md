# Contributing

This repository is a practitioner reference for quant developers. Contributions should make the library clearer, more useful, or more reliable for people building pricing, risk, market data, execution, and portfolio analytics systems.

## Contribution Standards
- Keep the writing practical. Explain what a concept means for implementation, validation, and production use.
- Prefer short worked examples over long theoretical derivations.
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
```

The script checks:
- local Markdown links,
- image references,
- SVG XML validity,
- duplicate top-level headings,
- expected chapter sections for numbered chapters.

## Style Notes
- Use `USD 10m` rather than `$10m` in prose to avoid Markdown math ambiguity.
- Use formulas where they clarify implementation, not as decoration.
- If a metric depends on convention, state the convention explicitly.
- If a model has a common failure mode, include it in the production pitfalls section.
