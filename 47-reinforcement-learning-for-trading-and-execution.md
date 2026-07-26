# Reinforcement Learning for Trading and Execution

Related chapters: [13-risk-and-pnl.md](13-risk-and-pnl.md), [14-testing-and-validation.md](14-testing-and-validation.md), [15-performance-and-production.md](15-performance-and-production.md), [16-portfolio-construction-and-backtesting.md](16-portfolio-construction-and-backtesting.md), [20-execution-microstructure-and-tca.md](20-execution-microstructure-and-tca.md), [40-point-in-time-data-and-event-systems.md](40-point-in-time-data-and-event-systems.md), [41-production-quant-engineering.md](41-production-quant-engineering.md), [44-robust-portfolio-and-research-validation.md](44-robust-portfolio-and-research-validation.md), [46-machine-learning-and-deep-learning-for-trading.md](46-machine-learning-and-deep-learning-for-trading.md), and [48-factor-models-and-systematic-signals.md](48-factor-models-and-systematic-signals.md).

## What This Domain Covers
Reinforcement learning (RL) learns a policy for sequential decisions whose actions affect later state and reward. In markets, that feedback matters when an order changes remaining quantity, queue position, inventory, exposure, market impact, or the opportunities available at the next step.

RL is not a substitute for forecasting, causal identification, market simulation, or risk controls. It is most credible when:

- the decision is genuinely sequential;
- state, actions, constraints, and accounting are explicit;
- a simulator or logged policy has adequate coverage;
- reward reconciles to economic PnL or implementation shortfall;
- a strong non-RL baseline exists;
- deployment can prohibit unsafe exploration.

Execution, market making, dynamic hedging, and constrained allocation are natural candidates. A one-shot directional prediction is normally a supervised-learning or optimization problem; see [46-machine-learning-and-deep-learning-for-trading.md](46-machine-learning-and-deep-learning-for-trading.md).

## Product Taxonomy and Market Structure
An RL problem is usually classified along several dimensions:

| Dimension | Alternatives | Trading implication |
| --- | --- | --- |
| Feedback | Contextual bandit or sequential MDP | Bandits ignore action effects beyond the immediate reward |
| Observability | MDP or partially observed MDP | Latent liquidity, other agents, and hidden orders make markets partially observed |
| Dynamics | Model-free or model-based | A learned transition model introduces model and compounding error |
| Data collection | Online or offline | Unconstrained online market exploration is usually unacceptable |
| Policy relation | On-policy or off-policy | Off-policy learning can reuse logs but needs action support and stable correction |
| Action space | Discrete, continuous, or hybrid | Order type, venue, size, and price offset create mixed actions |
| Objective | Value-based, policy-based, or actor-critic | Algorithm choice depends on action geometry and stability needs |
| Participants | Single-agent or multi-agent | Other traders adapt, so transition dynamics are not stationary |

The main algorithm families are:

- **Q-learning:** tabular, off-policy temporal-difference control for small discrete state/action spaces.
- **Deep Q-Network (DQN):** neural approximation of action values, commonly with replay and a target network; best suited to a manageable discrete action set.
- **Policy gradient:** directly optimizes a parameterized stochastic policy; handles continuous actions but can have high gradient variance.
- **Proximal Policy Optimization (PPO):** an on-policy actor-critic method that limits excessively large policy updates through a clipped surrogate objective.
- **Actor-critic:** learns both a policy (actor) and a value estimate (critic); the critic supplies a lower-variance learning signal.
- **A3C:** parallel asynchronous actor-critic workers learn from multiple environment streams; stale updates and simulator diversity must be managed.
- **Soft Actor-Critic (SAC):** an off-policy actor-critic method for continuous actions that adds an entropy objective and reuses replay data.

Applications require different state and action definitions:

### Execution

State may include remaining quantity and time, side, arrival price, spread, depth, imbalance, queue estimate, volatility, recent trades, forecast volume, alpha decay, fills, and venue status. Actions can select participation, child size, market/limit type, price offset, venue, or cancel/replace. Reward should reconcile to implementation shortfall plus explicit risk and constraint penalties.

### Market Making

State may include inventory, cash, fair value, spread, depth, queue position, order age, recent flow, toxicity indicators, volatility, and risk limits. Actions choose bid/ask offsets, sizes, venue, and cancellations. Reward must distinguish spread capture, adverse selection, fees/rebates, inventory mark, hedge cost, and terminal liquidation.

### Allocation and Hedging

State may include current holdings, cash, forecasts, factor exposure, covariance, costs, liquidity, and remaining risk budget. Actions are target weights, trades, or hedge ratios. Reward can use portfolio wealth change less costs and risk penalties. Hard leverage, concentration, turnover, and liquidity constraints should not be left solely to reward shaping.

The exchange, broker, and venue protocols define what an action really means. Requested quantity differs from accepted quantity; accepted quantity differs from displayed quantity; displayed quantity differs from fills. Cancels have latency and may race with executions. An environment that skips these states teaches a policy to exploit fictitious mechanics.

## Quoting and Market Conventions
Specify the decision protocol before training:

- decision clock: fixed interval, event time, volume time, or exchange event;
- observation cutoff and latency from observation to accepted action;
- price units, tick size, lot size, multiplier, currency, and FX conversion;
- inventory sign and units;
- action semantics, allowed order types, time in force, and venue rules;
- fill, partial-fill, rejection, cancel, and queue conventions;
- episode start, termination, truncation, and mandatory liquidation;
- benchmark: arrival, decision, interval VWAP, close, or another executable reference;
- reward units: currency, basis points, return, or normalized training units;
- fee, rebate, spread, impact, borrow, funding, and tax treatment;
- discount convention and step duration.

For irregular time steps, a fixed per-step discount changes the economic horizon when event intensity changes. One consistent convention is:

$$
\gamma(\Delta t)=\exp(-\rho\Delta t)
$$

where $\rho$ is a discount rate in the same time unit as $\Delta t$. If the objective is finite-horizon execution cost, $\gamma=1$ is often easier to reconcile, with urgency represented explicitly through state and penalties.

Reward timing must be unambiguous. State whether $r_{t+1}$ is generated by action $a_t$ and transition from $s_t$ to $s_{t+1}$. Keep raw PnL and cost ledger fields even when the training reward is clipped or normalized.

For a parent buy order of size $Q$ and arrival price $p_0$, implementation shortfall after completion is:

$$
\operatorname{IS}
=
\sum_i q_i(p_i-p_0)
+\text{fees}
+\text{unfilled or opportunity cost}
$$

For a sell, reverse the price-difference sign. Report both currency and basis points of arrival notional. Do not mix a sell-side revenue convention with a buy-side cost convention inside the reward.

## Core Pricing Framework
An MDP is a tuple:

$$
\mathcal M=(\mathcal S,\mathcal A,P,R,\gamma)
$$

where:

- $s_t\in\mathcal S$ is the state;
- $a_t\in\mathcal A(s_t)$ is an admissible action;
- $P(s_{t+1}\mid s_t,a_t)$ is the transition law;
- $R(s_t,a_t,s_{t+1})$ defines reward;
- $\gamma\in[0,1]$ discounts future reward.

A policy $\pi(a\mid s)$ maps states to action probabilities. Its return is:

$$
G_t
=
\sum_{k=0}^{T-t-1}\gamma^k r_{t+k+1}
$$

Let $d_{t+1}=1$ when the transition terminates the episode and zero otherwise. The action-value function satisfies:

$$
Q^\pi(s,a)
=
\mathbb E_\pi
\left[
r_{t+1}
+\gamma(1-d_{t+1})Q^\pi(s_{t+1},a_{t+1})
\mid s_t=s,a_t=a
\right]
$$

In a partially observed market, the observation $o_t$ is not the full state. A history window, recurrent state, belief estimate, or explicit latent-state model may help, but none guarantees the Markov property.

### Q-Learning and DQN

Tabular Q-learning applies:

$$
Q(s_t,a_t)
\leftarrow
Q(s_t,a_t)
+\alpha
\left[
r_{t+1}
+\gamma(1-d_{t+1})\max_{a'}Q(s_{t+1},a')
-Q(s_t,a_t)
\right]
$$

It is useful for small, discretized controls and as a transparent diagnostic baseline. Discretization can erase economically important distinctions or create a state table with little repeated support.

DQN replaces the table with $Q_\theta(s,a)$. A replay buffer reduces adjacent-sample correlation, and a lagged target network stabilizes the bootstrap target:

$$
y_t
=
r_{t+1}
+\gamma(1-d_{t+1})\max_{a'}Q_{\theta^-}(s_{t+1},a')
$$

Replay does not justify random train/test splitting across market time. The environment data, episodes, and regimes still require chronological validation.

### Policy Gradients, PPO, and Actor-Critic

The policy-gradient identity uses an advantage estimate:

$$
\nabla_\theta J(\theta)
=
\mathbb E_{\pi_\theta}
\left[
\nabla_\theta\log\pi_\theta(a_t\mid s_t)
\widehat A_t
\right]
$$

An actor-critic estimates both $\pi_\theta$ and $V_\phi$. A one-step temporal-difference error is:

$$
\delta_t
=
r_{t+1}
+\gamma(1-d_{t+1})V_\phi(s_{t+1})
-V_\phi(s_t)
$$

PPO forms the probability ratio:

$$
\rho_t(\theta)
=
\frac{\pi_\theta(a_t\mid s_t)}
{\pi_{\theta_{\text{old}}}(a_t\mid s_t)}
$$

and maximizes the clipped surrogate:

$$
L^{\text{clip}}(\theta)
=
\mathbb E
\left[
\min\left(
\rho_t\widehat A_t,
\operatorname{clip}(\rho_t,1-\epsilon,1+\epsilon)\widehat A_t
\right)
\right]
$$

Clipping limits the training update; it is not a live-trading risk limit. A3C runs actor-critic workers asynchronously on separate environment streams. The streams should represent genuine scenario diversity rather than duplicated paths with different random seeds.

SAC optimizes reward and policy entropy:

$$
J(\pi)
=
\mathbb E_\pi
\left[
\sum_t\gamma^t
\left(
r_{t+1}
+\alpha_{\mathcal H}
\mathcal H(\pi(\cdot\mid s_t))
\right)
\right]
$$

Entropy encourages action diversity during training. It does not authorize unsafe live exploration. SAC's off-policy replay is attractive for continuous controls, but logged or simulated support must cover the learned actions.

### Economic Reward Design

Reward should telescope to an auditable terminal result. For a buy execution, let:

- $C_t$ be cumulative dollars spent on fills;
- $F_t$ be cumulative fees;
- $q_t$ be remaining quantity;
- $m_t$ be the declared reference mark for the unfilled remainder;
- $Qp_0$ be arrival notional.

Define marked completion shortfall:

$$
S_t
=
C_t+F_t+q_t m_t-Qp_0
$$

A dense reward is:

$$
r_t
=
-(S_t-S_{t-1})
-P_t^{\text{inventory}}
-P_t^{\text{tail}}
-P_t^{\text{constraint}}
$$

If the order finishes and penalties are separately reported:

$$
\sum_t r_t
=
-\operatorname{IS}
-\sum_t P_t
$$

This telescoping identity is for the undiscounted economic audit sum, equivalently $\gamma=1$. A discounted training return does not telescope, so retain and reconcile the undiscounted ledger separately. If fees are already included in $S_t$, subtracting them again in $r_t$ double counts them.

The reference-mark policy changes intermediate shaping rewards. A midpoint is transparent for research but is not generally executable; terminal inventory must be liquidated or marked using a conservative side-aware completion price. Record both reference and executable marks when they differ.

For market making, mark economic wealth consistently:

$$
W_t=\text{cash}_t+I_t m_t
$$

and use:

$$
r_t
=
W_t-W_{t-1}
-\text{incremental costs}_t
-P_t^{\text{inventory}}
-P_t^{\text{tail}}
$$

Only subtract costs not already posted to cash. Terminal inventory should be liquidated or marked at a conservative executable price.

For allocation, let $C_t(\Delta w_t)$ be the current rebalance cost in currency units. A unit-consistent log-wealth reward posts that cost exactly once:

$$
r_t
=
\log\left(
\frac{W_t^{\text{pre-cost}}-C_t(\Delta w_t)}
{W_{t-1}^{\text{post-cost}}}
\right)
-\lambda_{\text{risk}}\,\mathcal R_t
$$

Here $W_t^{\text{pre-cost}}$ is marked wealth before the current rebalance cost, $W_{t-1}^{\text{post-cost}}$ is prior post-cost wealth, and $0\leq C_t<W_t^{\text{pre-cost}}$. The risk term must be dimensionless or converted to the same log-return units. If the ledger already supplies $W_t^{\text{post-cost}}=W_t^{\text{pre-cost}}-C_t$, use that value directly and do not subtract cost again. Hard constraints should be enforced through the admissible action set, projection, or a safety layer. A finite penalty does not guarantee compliance.

## Worked Instrument Example
Consider a buy order for 10,000 shares at an arrival price of $100.00. Arrival notional is $1,000,000. The reward uses marked completion shortfall and adds separately specified inventory-risk penalties.

| Step | Fill | Fill price | End reference mid | Cumulative fees | Marked shortfall $S_t$ | Risk penalty | Reward |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | - | $100.00 | $0 | $0 | $0 | - |
| 1 | 2,000 | $100.04 | $100.02 | $10 | $250 | $40 | -$290 |
| 2 | 5,000 | $100.07 | $100.05 | $35 | $615 | $15 | -$380 |
| 3 | 3,000 | $100.06 | $100.06 | $50 | $660 | $0 | -$45 |

At step 1:

$$
S_1
=
(2{,}000)(100.04)+10+(8{,}000)(100.02)-1{,}000{,}000
=
\$250
$$

so $r_1=-(250-0)-40=-\$290$. The midpoint is used only as the declared intermediate shaping mark; a production environment should also test side-aware executable completion marks. At completion, aggregate fill-price slippage is $610, equivalent to $0.061$ per share or $6.10$ bp of arrival notional, and fees are $50:

$$
\operatorname{IS}
=
\$610+\$50
=
\$660
=
6.60\text{ bp}
$$

The dense rewards sum to:

$$
-290-380-45=-\$715
$$

which reconciles to $-\$660$ implementation shortfall and $-\$55$ of explicit inventory penalties. The ledger keeps those components separate, even if the learner sees only their sum. See [examples/reinforcement-learning-reward-accounting.md](examples/reinforcement-learning-reward-accounting.md) for executable accounting code.

## Key Risk Measures and Sensitivities
Economic and control metrics:

- implementation shortfall in currency and basis points;
- spread, impact, delay, opportunity cost, fees/rebates, and adverse-selection attribution;
- completion rate, time to completion, participation, fill ratio, cancel ratio, and rejection rate;
- mean, peak, and terminal inventory; inventory duration; hedge cost;
- gross/net exposure, leverage, turnover, factor risk, and liquidity use;
- PnL, drawdown, expected shortfall, gap loss, and named stress scenarios;
- constraint interventions, projected actions, kill-switch events, and fallback usage.

Learning and evaluation metrics:

- undiscounted economic return and discounted training return;
- episode-return distribution, not only its mean;
- value/advantage error, Bellman residual, policy entropy, and action concentration;
- performance dispersion by day, instrument, venue, volatility, spread, liquidity, and regime;
- sensitivity to simulator seeds, latency, impact, queue model, reward weights, and terminal marks;
- action-support coverage and state distance from training data;
- offline importance-weight distribution, effective sample size, and confidence intervals;
- simulator-to-live gaps in fills, costs, inventory, actions, and state transitions.

Benchmark against simple controls such as TWAP, VWAP, POV, an implementation-shortfall schedule, fixed market-making quotes, or a constrained myopic optimizer. Compare at the same risk, completion, exposure, and action constraints. A lower simulated cost achieved by leaving orders unfinished is not an improvement.

## Required Data, Curves, Surfaces, and Calibration Objects
Every transition record should contain:

- episode and parent-decision ID;
- state timestamp, observation cutoff, exchange timestamp, and receive/send/acknowledgement latency;
- raw observation, transformed state, missingness/staleness flags, and state version;
- admissible-action mask, proposed action, projected action, accepted action, and policy probability or density;
- order IDs, venue, side, type, limit, size, time in force, cancel/replace chain, and rejections;
- fills, partial fills, fees/rebates, queue estimate, and market response;
- inventory, cash, mark, exposure, remaining objective, and risk limits;
- raw reward ledger components, normalized reward, discount, terminal reason, and next state;
- behavior-policy ID and action propensity when offline evaluation may be required.

Versioned objects should include:

- `EnvironmentSpec`: event ordering, fill/queue/impact models, latency, fees, market data, and randomization;
- `StateSpec`: feature definitions, point-in-time rules, lookbacks, transforms, and masks;
- `ActionSpec`: bounds, discretization, projections, and venue constraints;
- `RewardSpec`: accounting equations, units, penalty coefficients, clipping, normalization, and terminal treatment;
- `EpisodeManifest`: date, instruments, regimes, initial state, data versions, seed, and exclusions;
- `PolicyArtifact`: architecture, parameters, transforms, action distribution, training code/config, and checksum;
- `SafetyPolicy`: limits, overrides, fallback policy, escalation, and kill-switch criteria;
- `EvaluationReport`: baselines, chronological folds, scenario tests, uncertainty, and known unsupported states.

Historical depth alone is insufficient. Execution and market-making environments need trades, quotes, depth where available, message ordering, tick/lot rules, venue status, fee schedules, and realistic latency. Allocation environments need point-in-time holdings, prices, corporate actions, borrow/funding, liquidity, and risk model versions.

## Numerical and Implementation Approaches
Start with an explicit event and accounting engine. The order of market observation, agent decision, latency, exchange acknowledgement, market events, fills, cancels, marking, and reward calculation must be deterministic for a fixed event stream.

Use staged model development:

1. reproduce a deterministic baseline in the environment;
2. verify reward-to-PnL or reward-to-shortfall telescoping on hand calculations;
3. train on varied but documented episodes;
4. tune only inside chronological training/validation periods;
5. test on untouched later periods and severe counterfactual scenarios;
6. run shadow mode with live observations and no agent orders;
7. use a constrained canary with strict exposure and loss limits;
8. scale only after simulator-to-live reconciliation.

Simulator fidelity is policy-dependent. A replay that fills every limit order when the historical trade touches its price ignores queue priority and the fact that the agent's order was absent from history. A policy may exploit this error by posting unrealistic size. Model:

- queue position, partial fills, cancellations, rejects, and time priority;
- latency and cancel/fill races;
- spread, tick, lot, auction, halt, and venue rules;
- self-impact and opportunity cost;
- adverse selection after a fill;
- other-agent response and regime changes.

Calibrate simulator distributions on held-out episodes, but do not claim that matching unconditional fill rates proves counterfactual validity. Stress parameters and randomize plausible domains. Performance should remain acceptable under worse latency, thinner depth, larger impact, stale signals, and gaps.

Offline policy evaluation (OPE) is difficult because historical rewards reveal only actions taken by the behavior policy $\mu$. A trajectory importance-sampling estimator uses:

$$
\widehat V_{\text{IS}}(\pi)
=
\frac{1}{N}
\sum_{i=1}^{N}
G_i
\prod_t
\frac{\pi(a_{i,t}\mid s_{i,t})}
{\mu(a_{i,t}\mid s_{i,t})}
$$

It requires known behavior propensities and support wherever $\pi$ acts; weights often have extreme variance. Weighted importance sampling, doubly robust estimators, fitted value evaluation, and model-based OPE introduce different bias/variance assumptions. Report diagnostics and confidence intervals. No OPE method recovers reliable counterfactuals where action support is absent.

Reward design needs an independent accounting review. Common penalties include:

- inventory magnitude and duration;
- unfilled terminal quantity at a conservative forced-liquidity price;
- market impact, participation, or excessive message traffic;
- drawdown, downside shortfall, expected-shortfall proxy, or limit breach;
- leverage, concentration, factor, and liquidity use.

Keep penalty units commensurate, test extreme states, and report economic PnL before penalties. Detect reward hacking by checking independent KPIs the agent cannot redefine.

Safe deployment enforces action bounds outside the learned policy. Reject stale or invalid states, project actions to hard constraints, rate-limit messages, cap participation and inventory, stop on loss/latency/data thresholds, and fall back to a deterministic policy. Log both proposed and executed actions so overrides are visible in evaluation.

## Production Pitfalls and Sanity Checks
- Treating a contextual prediction problem as an MDP without meaningful action feedback.
- Including future trades, fills, or end-of-interval statistics in the state.
- Filling a posted limit order whenever historical price touches it, without queue or size.
- Letting the simulator ignore the policy's own impact.
- Training and testing on randomly mixed episodes from the same market period.
- Omitting behavior-policy probabilities while claiming importance-sampling evaluation.
- Evaluating actions outside logged-policy support.
- Using a reward that does not reconcile to PnL or implementation shortfall.
- Counting fees, rebates, inventory marks, or spread capture twice.
- Omitting terminal liquidation so the agent parks unwanted inventory at episode end.
- Rewarding low execution cost without penalizing unfilled quantity.
- Letting a policy earn rebates through excessive messages or exploit stale midpoint marks.
- Normalizing reward differently in training and live scoring without preserving raw units.
- Using a per-event discount factor that changes the economic horizon with message intensity.
- Treating PPO clipping as an exposure or loss limit.
- Allowing online exploration in live markets because the training algorithm expects it.
- Comparing policies with different completion, risk, participation, or action constraints.
- Ignoring exchange rejects, cancel races, halts, auctions, and restart recovery.
- Deploying a policy in unseen states without a distance, confidence, or fallback rule.
- Updating a simulator and policy together without retaining the old environment for comparison.

Sanity tests should cover zero action, immediate completion, no fills, full fills, price gaps, locked/crossed markets, fee sign, buy/sell symmetry, partial-fill conservation, terminal liquidation, inventory/cash conservation, deterministic replay, hard-limit projection, reward telescoping, and restart from a persisted state.

## Illustrative Code
```python
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class BuyExecutionStep:
    fill_quantity: int
    fill_price: float
    fee: float
    end_reference_mark: float
    risk_penalty: float


def buy_execution_rewards(
    parent_quantity: int,
    arrival_price: float,
    steps: list[BuyExecutionStep],
) -> tuple[list[float], float, float]:
    if parent_quantity <= 0 or arrival_price <= 0.0:
        raise ValueError("positive parent quantity and arrival price required")
    remaining = parent_quantity
    dollars_spent = 0.0
    fees = 0.0
    previous_shortfall = 0.0
    rewards: list[float] = []
    total_penalties = 0.0

    for step in steps:
        if not 0 <= step.fill_quantity <= remaining:
            raise ValueError("invalid fill quantity")
        numeric_values = (
            step.fill_price,
            step.fee,
            step.end_reference_mark,
            step.risk_penalty,
        )
        if not all(math.isfinite(value) for value in numeric_values):
            raise ValueError("execution inputs must be finite")
        if step.fill_price <= 0.0 or step.end_reference_mark <= 0.0:
            raise ValueError("prices must be positive")
        if step.fee < 0.0 or step.risk_penalty < 0.0:
            raise ValueError("fees and penalties must be non-negative")

        dollars_spent += step.fill_quantity * step.fill_price
        fees += step.fee
        remaining -= step.fill_quantity
        marked_cost = (
            dollars_spent
            + fees
            + remaining * step.end_reference_mark
        )
        shortfall = marked_cost - parent_quantity * arrival_price
        reward = -(shortfall - previous_shortfall) - step.risk_penalty
        rewards.append(reward)
        total_penalties += step.risk_penalty
        previous_shortfall = shortfall

    if remaining != 0:
        raise ValueError("episode ended with unfilled quantity")
    implementation_shortfall = previous_shortfall
    return rewards, implementation_shortfall, total_penalties


def q_learning_update(
    current_q: float,
    reward: float,
    best_next_q: float,
    learning_rate: float,
    discount: float,
    terminal: bool,
) -> float:
    if not all(
        math.isfinite(value)
        for value in (current_q, reward, best_next_q, learning_rate, discount)
    ):
        raise ValueError("Q-learning inputs must be finite")
    if not 0.0 < learning_rate <= 1.0:
        raise ValueError("learning_rate must be in (0, 1]")
    if not 0.0 <= discount <= 1.0:
        raise ValueError("discount must be in [0, 1]")
    target = reward if terminal else reward + discount * best_next_q
    return current_q + learning_rate * (target - current_q)


def elapsed_time_discount(rate: float, elapsed: float) -> float:
    if not math.isfinite(rate) or not math.isfinite(elapsed):
        raise ValueError("rate and elapsed time must be finite")
    if rate < 0.0 or elapsed < 0.0:
        raise ValueError("rate and elapsed time must be non-negative")
    return math.exp(-rate * elapsed)
```

## References and Further Reading
- Sutton and Barto. *Reinforcement Learning: An Introduction*, second edition.
- Watkins and Dayan. "Q-learning." *Machine Learning*, 1992.
- Mnih et al. "Human-level Control through Deep Reinforcement Learning." *Nature*, 2015.
- Williams. "Simple Statistical Gradient-Following Algorithms for Connectionist Reinforcement Learning." *Machine Learning*, 1992.
- Mnih et al. "Asynchronous Methods for Deep Reinforcement Learning." ICML, 2016.
- Schulman et al. "Proximal Policy Optimization Algorithms." 2017.
- Haarnoja et al. "Soft Actor-Critic: Off-Policy Maximum Entropy Deep Reinforcement Learning with a Stochastic Actor." ICML, 2018.
- Almgren and Chriss. "Optimal Execution of Portfolio Transactions." *Journal of Risk*, 2001.
- Nevmyvaka, Feng, and Kearns. "Reinforcement Learning for Optimized Trade Execution." ICML, 2006.
- Moody and Saffell. "Learning to Trade via Direct Reinforcement." *IEEE Transactions on Neural Networks*, 2001.
- Levine et al. "Offline Reinforcement Learning: Tutorial, Review, and Perspectives on Open Problems." 2020.
- Related example: [examples/reinforcement-learning-reward-accounting.md](examples/reinforcement-learning-reward-accounting.md).
