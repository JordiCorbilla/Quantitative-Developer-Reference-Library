# Glossary

## A
- **A3C**: Asynchronous Advantage Actor-Critic, an RL method in which parallel workers update a shared actor and critic; worker staleness and genuine environment diversity matter.
- **Active risk**: Tracking error of a portfolio relative to its benchmark.
- **Actor-critic**: Reinforcement-learning architecture with a policy actor and a value or action-value critic that supplies a lower-variance learning signal.
- **Alpha**: Expected return not explained by the chosen benchmark or factor model.
- **Almgren-Chriss model**: Optimal-execution framework balancing expected market-impact cost against the risk of holding unexecuted inventory over time.
- **American option**: Option that can be exercised before expiry.
- **ARIMA**: Autoregressive integrated moving-average model applying ARMA dynamics to a differenced series under a stated order and deterministic-term convention.
- **ARIMAX**: ARIMA with external regressors whose future or contemporaneous values must be available or separately forecast at the decision horizon.
- **Appraisal rights**: Statutory rights that may let eligible shareholders ask a court to determine fair value rather than accept merger consideration; eligibility, deadlines, and jurisdiction matter.
- **As-of query**: Query that reconstructs what a system knew at a specified historical time, rather than returning the latest corrected record.
- **Attachment point**: Portfolio loss level where a structured-credit tranche begins absorbing losses.

## B
- **Bayesian change-point detection**: Probabilistic method for updating the likelihood that model parameters or regimes changed, often through a run-length distribution and hazard assumption.
- **Basis**: Difference between related instruments or curves that should not be collapsed without explanation.
- **Beta**: Sensitivity of an asset or portfolio return to a benchmark return.
- **Bitemporal data**: Data carrying both valid time, when a fact applies in the real world, and system time, when the system learned or stored it.
- **Borrow cost**: Cost of borrowing securities, important for shorts and equity forwards.
- **Black-Litterman model**: Portfolio framework blending equilibrium implied returns with uncertain absolute or relative investor views.
- **Break price**: Estimated value of a target or affected security if a proposed transaction fails, including the market move and changed standalone fundamentals.
- **Brier score**: Mean squared error of probabilistic predictions such as PD forecasts.

## C
- **CAPM**: Capital Asset Pricing Model, relating expected excess return to exposure to a market excess-return factor under its assumptions.
- **Carhart four-factor model**: Fama-French three-factor return model augmented with a momentum factor under a declared construction.
- **Calibration**: Choosing model parameters to fit market-observable prices or quotes.
- **Catalyst**: An identifiable event that can change a security's value or resolve uncertainty, such as earnings, a regulatory decision, refinancing, or a transaction vote.
- **Collar**: Deal or derivative term that changes the exchange ratio or consideration when a reference price moves outside specified thresholds.
- **Copula**: Multivariate distribution on uniform margins that represents dependence separately from the marginal distributions.
- **Clean price**: Bond price excluding accrued interest.
- **CLS**: Continuous Linked Settlement, a settlement system that reduces FX principal settlement risk through payment-versus-payment for eligible currencies and participants.
- **Collateral**: Assets posted to reduce counterparty exposure or support financing.
- **Confirmation**: Counterparty agreement of trade economics after execution.
- **Contingent value right (CVR)**: Security or contractual right paying only if specified milestones, such as an approval or sales threshold, are achieved.
- **Convexity**: Second-order sensitivity; for bonds it captures curvature of price-yield relation.
- **Convertible bond**: Bond with an embedded right to convert into equity under specified terms.
- **Covenant headroom**: Distance between a borrower's current or forecast metric and the threshold allowed by a debt covenant.
- **CS01**: Credit spread sensitivity to a one basis point spread move.
- **Correlation**: Normalized covariance measuring linear association between two variables.
- **Cross-sectional signal**: Score comparing assets at one decision time, with universe, transformations, neutralization, and rank convention defined point in time.
- **Covariance**: Joint variability of two variables around their means.
- **CVA**: Credit Valuation Adjustment, expected discounted loss from counterparty default.

## D
- **Deal spread**: Difference between a transaction's current market-implied value and the target security's price, adjusted for consideration terms, time, and distributions.
- **Delta**: First-order sensitivity of option value to the underlying price or chosen forward proxy.
- **Dividend yield**: Annual cash dividends per share divided by current share price; it does not measure total shareholder return or prove how retained cash is used.
- **Detachment point**: Portfolio loss level where a structured-credit tranche is fully exhausted.
- **Dirty price**: Bond price including accrued interest.
- **Discount factor**: Present value of one unit of currency paid at a future date.
- **DSCR**: Debt-service coverage ratio, typically cash flow available for debt service divided by scheduled interest and principal; the exact numerator and denominator must be defined.
- **DQN**: Deep Q-Network, a neural action-value method typically using replay data and a target network for discrete actions.
- **DV01 / PV01**: Present-value change for a one basis point rate move.

## E
- **Earnings per share (EPS)**: Profit attributable to common shareholders divided by weighted average common shares; diluted EPS reflects potential share-count dilution.
- **Event time**: Time an event occurred in the source domain, distinct from when it was published, received, or processed.
- **Elastic net**: Linear-model regularization combining lasso's \(L_1\) penalty with ridge's \(L_2\) penalty.
- **Engle-Granger procedure**: Two-step cointegration method estimating a long-run relation and testing its fitted residual for a unit root with appropriate critical values.
- **EWMA volatility**: Exponentially weighted moving-average variance estimate whose decay parameter is tied to the sampling frequency.
- **Expected Shortfall (ES)**: Average of the worst specified probability mass of a loss distribution; with discrete mass at VaR, the boundary mass must be included fractionally as required by the declared quantile convention.
- **Exposure**: Value at risk to a counterparty or risk factor.
- **ETF premium/discount**: Difference between ETF market price and NAV, usually expressed as a percentage of NAV.

## F
- **Factor model**: Representation of returns or covariance through common drivers and a residual or specific-risk component; exact factor definitions and exposures must be stated.
- **Fama-French factors**: Published asset-pricing factor families including market, size, value, profitability, and investment factors under specific construction rules.
- **Filtered state**: Latent-state estimate using observations available only through the current timestamp; distinct from a retrospectively smoothed state.
- **Forward price**: Price agreed today for future delivery or settlement.
- **Forward points**: Difference between an FX outright forward rate and spot rate, usually quoted in scaled points for the currency pair.
- **FRTB**: Fundamental Review of the Trading Book, a market-risk capital framework.
- **FX swap**: Transaction with a near-leg exchange of two currencies and a far-leg reversal at a pre-agreed forward rate.

## G
- **GARCH**: Generalized autoregressive conditional heteroskedasticity, a family of conditional volatility models.
- **Gamma**: Sensitivity of delta to the underlying.
- **Gamma scalping**: Dynamic delta-hedging of a gamma position to realize pathwise hedge PnL; profitability still depends on theta, volatility, jumps, surface moves, and trading costs.
- **Gaussian mixture model**: Weighted mixture of Gaussian component distributions used for flexible density or regime approximation; component labels are not intrinsically stable.
- **Gerber co-movement statistic**: Robust dependence measure that counts joint threshold exceedances and ignores small central moves; its threshold and estimator variant must be stated.

## H
- **HAR-RV**: Heterogeneous autoregressive realized-volatility model combining daily, weekly, and monthly realized-variance components.
- **Haircut**: Reduction applied to collateral value in financing or margin.
- **Hazard rate**: Default intensity used in credit modelling.
- **Heston model**: Stochastic-volatility option model with mean-reverting variance and correlated spot/variance shocks.
- **Hidden Markov Model (HMM)**: Probabilistic sequence model with hidden states, initial probabilities, transition probabilities, and a state-dependent emission distribution. In markets, HMMs are often used to estimate regime probabilities from returns, volatility, volume, or spread data.
- **Hierarchical Risk Parity (HRP)**: Cluster-based allocation method using dependence distances and recursive risk allocation without directly inverting the complete covariance matrix.
- **Heteroskedasticity**: Non-constant residual variance, common in financial time series.
- **Hull-White model**: Short-rate model with time-dependent drift commonly used for curve-consistent rates derivatives pricing.

## I
- **Idempotency**: Property that retrying an operation with the same identity does not create an additional economic or processing effect.
- **Implementation shortfall**: Execution cost relative to the decision or arrival price.
- **Implied volatility**: Volatility input that makes an option model match market price.
- **IPV**: Independent price verification.

## J
- **Johansen procedure**: Multivariate likelihood-based method for estimating cointegration rank and vectors in a vector error-correction system.

## K
- **Kalman filter**: Recursive state-space estimator that predicts and updates a continuous latent state and its covariance using a process and observation model.
- **Kelly criterion**: Allocation objective maximizing expected log wealth; estimated full-Kelly weights can be highly sensitive to return, tail, and dependence assumptions.
- **Knowledge time**: Timestamp representing when information became available to a researcher or system, used to prevent look-ahead in historical analysis.
- **Kyle lambda**: Estimated price response per unit of signed order flow under declared price, flow, and interval units; an empirical slope is not automatically a causal impact estimate.

## L
- **Lasso**: Linear-model estimator using an \(L_1\) coefficient penalty that can shrink some coefficients to zero.
- **LGD**: Loss given default, equal to one minus recovery rate.
- **Locate**: Confirmation from a broker or lender that shares may be available to borrow for a short sale; it is not a guarantee that borrow remains available.
- **Longstaff-Schwartz**: Monte Carlo regression method for estimating continuation values in Bermudan-style exercise problems.
- **LSTM**: Long short-term memory recurrent neural network using gates to retain and update sequence state.
- **LTV**: Loan-to-value ratio, generally debt divided by eligible collateral or property value under a stated valuation convention.

## M
- **Market data snapshot**: Versioned set of market inputs used for valuation or risk.
- **Market capitalization**: Current share price multiplied by shares outstanding; it measures equity value and differs from enterprise value and free-float market cap.
- **Markov decision process (MDP)**: Sequential-decision model defined by state, action, transition, reward, and discount structure.
- **Momentum signal**: Rule using the persistence of past relative or own-history returns under a declared lookback, skip period, rebalance, and cost convention.
- **Model governance**: Controls around model inventory, approval, validation, limitations, and monitoring.
- **MVA**: Margin valuation adjustment for the funding cost of initial margin.

## N
- **Naive Bayes**: Probabilistic classifier combining class priors and conditionally independent feature likelihoods; correlated features can double-count evidence.
- **Neural network**: Layered nonlinear function approximator whose architecture, inputs, targets, regularization, training data, and deployment controls determine its economic meaning.

## O
- **Order-book imbalance**: Normalized difference between declared bid and ask depth or flow; feed sequencing, levels, cancellations, venue coverage, and latency determine the feature.
- **OLS**: Ordinary least squares, a regression method that minimizes squared residuals.
- **Ornstein-Uhlenbeck process**: Continuous-time mean-reverting diffusion often used as an approximation for a spread; its half-life is a model diagnostic, not a guaranteed trade duration.

## P
- **P/E ratio**: Current share price divided by EPS. Trailing P/E uses reported earnings; forward P/E uses forecasts and is undefined or uninformative when EPS is non-positive.
- **Payment-versus-payment (PvP)**: Settlement mechanism in which one currency payment is final only if the other currency payment is also final.
- **PD**: Probability of Default over a specified horizon and default definition.
- **PCA**: Principal component analysis, an orthogonal variance-decomposition method whose loadings can rotate across windows and need not be predictive.
- **PFE**: Potential future exposure, a high-quantile estimate of counterparty exposure over a future horizon under stated netting, collateral, and simulation assumptions.
- **PIPE**: Private investment in public equity, often used to finance a transaction or recapitalization and subject to negotiated terms, registration mechanics, and dilution.
- **Point-in-time data**: Historical data stored with enough timing and version information to reproduce what was knowable at each decision date.
- **PnL explain**: Decomposition of profit and loss into market moves, carry, trades, lifecycle events, and residual.
- **Policy gradient**: Reinforcement-learning method that directly optimizes a parameterized policy using sampled return or advantage estimates.
- **POV**: Percentage-of-volume execution algorithm.
- **PPO**: Proximal Policy Optimization, an on-policy actor-critic method limiting large training updates with a clipped surrogate objective; clipping is not a live risk limit.
- **Point-in-time PD**: PD estimate reflecting current borrower and macro conditions.
- **Prime broker**: Broker providing an investment manager with services such as custody, financing, securities lending, clearing, reporting, and synthetic exposure.
- **Purging**: Removing training observations whose label intervals overlap a validation or test interval; distinct from an embargo around fold boundaries.

## Q
- **Q-learning**: Off-policy temporal-difference control method updating an action-value estimate toward observed reward plus discounted best next-state value.

## R
- **Recall risk**: Risk that a securities lender asks for borrowed shares to be returned, forcing replacement borrow or a short close-out.
- **Reinforcement learning**: Learning a sequential policy from rewards when actions affect later state; market use requires simulator, support, accounting, offline-evaluation, and safety controls.
- **Regime model**: Model that lets parameters or dynamics change across latent market states.
- **Regime-switching GARCH**: GARCH model where volatility parameters depend on an unobserved regime.
- **Repo**: Financing transaction where securities are sold and later repurchased.
- **Ridge regression**: Linear regression with an \(L_2\) coefficient penalty that shrinks correlated or noisy estimates without usually setting them exactly to zero.
- **Risk parity**: Portfolio construction targeting equal or specified component risk contributions under a declared covariance model; inverse-volatility weighting is not generally identical.
- **Residual PnL**: PnL not explained by known risk factors or lifecycle changes.
- **Rights offering**: Capital raise granting existing holders transferable or non-transferable rights to buy new securities at stated terms before expiry.
- **Rho**: Sensitivity of option value to interest rates, often replaced by curve-bucket risk for rates-heavy books.
- **R-squared**: Share of target variance explained by a regression model in sample.
- **Roll-down**: PnL from moving along a curve or surface as time passes.

## S
- **SAC**: Soft Actor-Critic, an off-policy continuous-action actor-critic method adding policy entropy to reward.
- **SARIMA**: Seasonal ARIMA model with declared seasonal period, seasonal differencing, and seasonal AR/MA orders.
- **Settlement risk**: Risk that one side of a trade pays or delivers but does not receive the expected cash or asset.
- **SIMM**: Standard Initial Margin Model.
- **Skew**: Variation of implied volatility across strike or delta.
- **SPAC**: Special purpose acquisition company that raises cash in an IPO to pursue a business combination, usually with units that may separate into shares and warrants and with redemption rights governed by transaction documents.
- **Stock borrow**: Arrangement that supplies shares for a short position in return for collateral and a lending fee or rebate.
- **Stress test**: Scenario designed to measure loss under severe market conditions.
- **State-space model**: Model separating latent state dynamics from an observation equation; filtering and smoothing answer different information-set questions.
- **SVM**: Support-vector machine, a margin-based supervised model whose scaling, kernel, class weights, and probability calibration require explicit validation.
- **System time**: Interval during which a stored version was believed by the system, including later corrections and restatements.

## T
- **Tail dependence**: Limiting tendency for variables to experience joint extreme quantile events; upper and lower tails may differ.
- **Theta**: Sensitivity of option value to time passage under a specified model or market-data roll convention.
- **Temporal CNN**: Causal convolutional sequence model whose receptive field, dilation, padding, and mask must prevent future-data leakage.
- **Through-the-cycle PD**: PD estimate smoothed across the economic cycle for long-run risk views.
- **Trade lifecycle**: Sequence of trade states from pre-trade and execution through booking, confirmation, settlement, lifecycle events, reconciliation, and close-out.
- **Total return swap (TRS)**: Swap where one leg pays the total return of an asset and the other leg usually pays financing.
- **Transformer**: Attention-based sequence model using token/time encodings and masks; additional flexibility requires enough data and leakage-safe horizon design.
- **Tranche**: Structured-finance layer that absorbs losses between attachment and detachment points.
- **TWAP**: Time-weighted average price.

## V
- **VAR**: Vector autoregression modelling a stationary vector from its own lags under a declared lag order and deterministic specification.
- **VaR**: Value at Risk, a loss threshold at a specified confidence level and horizon.
- **VECM**: Vector error-correction model representing differences and adjustment toward one or more cointegrating relations.
- **Vasicek model**: Mean-reverting short-rate model with normally distributed rate changes.
- **Vega**: Sensitivity of value to volatility.
- **Variance risk premium**: Difference between option-implied variance and expected or subsequently realized variance, subject to horizon, sampling, and risk-neutral versus physical-measure conventions.
- **VWAP**: Volume-weighted average price.

## W
- **Warrant**: Security giving the holder the right to buy an issuer's shares under contractual strike, expiry, adjustment, redemption, and exercise terms.
