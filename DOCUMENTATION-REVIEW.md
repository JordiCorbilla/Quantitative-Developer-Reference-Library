# Documentation Review: 3 October 2026

The review found specific errors and ambiguous assumptions worth correcting. The library has a useful practitioner structure, but its breadth and passing snippets should not be mistaken for independent validation of every statement. This record separates repository-wide mechanical checks from the deeper financial review.

## Scope And Method

The repository contains one overview and 48 subject chapters. Mechanical validation covers repository Markdown navigation and image references, chapter structure and narrative openings, fence balance, Python syntax, example assertions, and SVG metadata. The execution runner covers every Python fence in the numbered chapters and standalone worked examples. The review also inspected chapter openings, core formula/convention sections, references, and worked-example claims, with deeper checks around options, valuation ledgers, rates, index mechanics, statistics, and warrant dilution.

Primary sources were checked for the corrections below. Examples are synthetic unless their text explicitly identifies sourced observations. No attached source document, extracted text, or copied illustration belongs in the repository.

## Corrections And Their Consequences

| Area | Issue found | Resulting explanation or check |
| --- | --- | --- |
| [Options](01-options.md) | Finishing-probability and zero-volatility language needed exact qualifications; common sign rules were incomplete | Risk-neutral $N(d_2)$ versus spot delta, distinct zero-time/zero-volatility limits, four-position sign table, positive-put-theta counterexample, and spot-fixed versus forward-fixed rho |
| [Options risk story](examples/option-greeks-and-earnings-repricing.md) | No complete worked example connecting favorable direction with a volatility-crush loss | Full European call repricing, telescoping sequential explain, finite-difference Greeks, parity, and PDE checks |
| [Greek visual](assets/options-greeks-dashboard.svg) | Rho graph's axis and unqualified maturity statement could imply a universal rule | Spot axis consistent with the schematic curves; qualified tenor wording and explicit model-coordinate assumptions |
| [Rates options](28-rates-options-caps-floors-swaptions.md) | Annuity-scaled expectation omitted its measure and blurred exercise value with cash payment | Annuity measure, time-zero versus exercise-time annuity, normal-vol units, physical versus cash settlement, and checked ATM normal premium |
| [Indices](29-etfs-index-products-and-rebalances.md) | A weighted sum of prices conflated market-value weights with constituent share quantities | Share/float/divisor formula, lagged-weight return identity, and a worked split/replacement reconciliation |
| [Governance](22-model-governance-and-ipv.md) | Adding adjustments and reserves as separate universal layers could count the same reserve twice | Signed incremental adjustments, explicit ledger destinations, and accounting versus prudential treatment |
| [Statistics](23-probability-statistics-and-regression.md) | Fitting, coefficient interpretation, and inference needed separate assumptions | Exogeneity and rank, normality for classical exact inference, heteroskedasticity/autocorrelation controls, and a qualified beta interpretation |
| [Warrants and PIPEs](36-warrants-rights-pipes-and-spacs.md) | Dilution benchmark lacked a firm-value input definition; PIPEs bibliography mixed a publication with a book and wrong co-author | Exercise-proceeds derivation, equity value versus traded stock input, and publisher-verified Dresner/Kim reference |
| [Private credit](39-private-credit-distressed-and-real-estate-credit.md) | Adding accretion and credit loss to full mark changes could count the same economics twice | Value-change-plus-cash identity and explicit PIK/default attribution examples |

## Options Teaching Coverage

The supplied ten-page Greeks primer was compared by topic with the options chapter. Its substantive teaching points are now covered in original repository prose and executable examples; promotional instructions and copied graphics are excluded.

| Teaching topic | Where to read it | Qualification preserved |
| --- | --- | --- |
| Why Greeks help explain price changes | Key Risk Measures and Sensitivities | Local derivatives under specified model and shock coordinates |
| Delta definition, small price move, and hedge intuition | Reading The Dashboard One Shock At A Time; formula reference | Multiplier/quantity scaling, approximate half-delta, and delta versus probability |
| Gamma as change in delta and near-ATM concentration | Dashboard, formula reference, and rehedging discussion | Second-order price contribution; peak and expiry intuition are conditional |
| Theta, daily decay, near-expiry behavior | Dashboard and Decay by Moneyness, Tenor, and Clock | Calendar theta, roll PnL, carry exceptions, and variance clock |
| Vega, a one-volatility-point shock, and tenor intuition | Dashboard and Black-Scholes Greek Formula Reference | Decimal versus percentage-point shocks and non-universal tenor comparisons |
| Rho, call/put signs, and longer-tenor exposure | Long And Short Vanilla Sign Reference | Spot-fixed equity rho differs from forward-fixed discount rho and curve risk |
| Earnings and Greeks changing together | Worked Risk Story: Right On Direction, Losing On The Call | Full repricing, possible rather than inevitable volatility crush, and order-dependent attribution |
| Long/short call and put sign reference | Long And Short Vanilla Sign Reference | Exact vanilla-model signs separated from typical theta signs |
| Memory aid and combined PnL approximation | Sign reference and Taylor expansion | Mnemonic aids reading; full revaluation handles large/discontinuous shocks |

## Readability Changes

The reading route follows a concrete question through inputs, assumptions, arithmetic, interpretation, and a control. The README offers three such routes: a losing call after a stock rise, off-node swap valuation, and an unusually strong backtest. The options example and index example end by explaining what their calculations establish and what production data or conventions they still need. Private-credit and research-validation openings now start with a scenario before introducing technical objects.

Existing short chapters retain their common structure so readers can find conventions, pricing, risk, data, and failure modes consistently. No wholesale rewrite is required to improve a reference whose basic organization already works.

## Reproduce The Checks

Follow the [clean-checkout quickstart](QUICKSTART.md), then run:

```powershell
python scripts/check_repository.py
git diff --check
```

The final execution set contains 97 Python fences across one overview, 48 subject chapters, and 49 standalone worked examples. Local Markdown heading fragments are checked as well as target-file existence; Python comments inside fences are excluded from heading counts. Three tooling regressions check fragment handling, duplicate/code-block headings, and exclusion of environment documentation. The altered Greek SVG was rendered and visually inspected. CI installs the declared dependencies and runs the same release check on Windows and Linux; remote runs are separate from locally completed validation.

The complete check also passed from a separate copy of the release files, without Git metadata or ignored local notes, using a fresh Python 3.12.14 environment with NumPy 2.5.3 and pandas 3.0.6 installed from the declared requirements. `pip check` reported no broken requirements. Invoking the check from outside that copy verified working-directory independence. The release command rejects optimized Python execution, which would otherwise skip example assertions.

Passing code verifies the assertions that were actually written. The options derivative checks exercise mathematical identities against the chapter implementation. The separate CRR tree benchmark checks twelve call/put cases at 256, 1024, and 4096 steps; the largest final absolute price error was 0.00048820 per underlying unit. The curve bootstrap repriced all four synthetic quotes with maximum absolute rate residual below 5e-17, valued the off-node bond at 0.98305591 per principal unit, and reconciled its five-year quote signed PV01 of -329.4894 with actual upward-bump PnL of -329.4632 on one million principal. These are bounded model checks, not production engine certification. Mechanical link checks cover local links, not universal availability or correctness of external references.

## Release Scope And Maintenance

The review is a broad consistency and risk-focused factual pass, not a line-by-line external-source certification. It does not establish that no factual errors remain, that every bibliography entry has been independently verified, or that any strategy has a live edge. Historical blog articles remain snapshots; their counts should not be used as current inventory.

The reference release includes an independent European tree benchmark, a complete simplified curve calibration with quote residuals and rebuilt risk, a selected primary-source claim register, and a clean setup/verification path. Capstones are explicitly published as six implementation exercise specifications. The existing volatility and credit examples remain bounded teaching calculations; full production surface/credit calibration and completed capstone platforms are extensions to this reference, not undisclosed artifacts promised by this release. Maintain source versions and executable controls together through the contribution process.
