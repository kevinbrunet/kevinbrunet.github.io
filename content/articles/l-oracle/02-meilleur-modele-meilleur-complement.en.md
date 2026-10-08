---
title: "The Most Expensive Model May Be Better Left for Last"
seo_title: "AI agents: why the most expensive model may be better left for last"
slug: "most-expensive-model-better-left-last"
date: 2026-10-27
description: "Across 113 DeepSWE tasks, reversing the order of the same models cuts the simulated cost by 36% without losing a single positive verdict."
categories: ["Artificial intelligence", "Software architecture", "Software engineering"]
tags: ["ai-evaluation-evals", "llmops-agentops"]
series: ["l-oracle"]
series_order: 2
collection: "SYSTÈMES"
cover: "/images/articles/meilleur-complement.en.png"
draft: false
---

{{< callout variant="scene" label="From variance to complementarity" >}}
In the first article, we saw that an oracle could give Luna several chances. Across up to four attempts, the model solves at least once **102 tasks out of 113**.

But how can we recover successful outcomes on the remaining 11 tasks?

**By looking for its complement: not the best model in absolute terms, but the one that succeeds precisely where Luna fails.**
{{< /callout >}}

To find it, we need a different ranking: instead of measuring only each model’s average performance, we must compare their error profiles.

## A leaderboard hides error profiles

A leaderboard ranks models along one axis: their average performance.

This metric answers a useful question: if I can run only one attempt, which model has the highest probability of succeeding?

It does not answer another question that is essential to agentic architecture: when a first model fails, which model is most likely to succeed specifically on those failures?

The detailed [**DeepSWE 1.1**](https://deepswe.datacurve.ai/) data lets us follow up to four runs of each configuration, task by task. We focus on the 11 tasks where Luna receives no positive verdict. They constitute its observed “blind spots” on this benchmark (not an absolute inability).

As in the first article, a “solved” task means a positive grader verdict. All results compared here use the same harness, `mini-swe-agent`, with the stated effort levels.

To find that complement, we can compare every configuration along two axes: the number of Luna failures it recovers and the cost of that escalation. Four configurations with one missing attempt cost are excluded. The other 66 appear in the chart.

{{< scatter-chart
  dataset="deepswe-luna-cost-recovery"
  title="Which model complements Luna at the best cost?"
  description="Each point represents one configuration applied to Luna's 11 failures. The higher it is, the more tasks it recovers. The farther left it is, the less that escalation costs."
  x-label="Estimated escalation cost on Luna's 11 failures ($)"
  y-label="Luna failures recovered, out of 11"
  x-min="0.5" x-max="500"
  y-min="0" y-max="11"
  regression="none"
  primary="mini_swe_agent_glm_5_3_flash_max"
  count-label="configurations with complete costs"
  y-total="11"
  x-format="currency"
  x-scale="log"
  tooltip-x="Escalation cost"
  tooltip-y="Failures recovered"
  tooltip-ratio="Cost per recovered failure"
  tooltip-attempts="Attempts executed"
  attempts-label="Attempts executed"
  details-label="View all 66 configurations"
>}}
GLM-5.3 Flash [max], shown in blue, offers the best balance here between recovered failures and escalation cost. The cost axis is logarithmic so that inexpensive and costly models remain readable. Costs simulate stopping at the first success on Luna's 11 failures. The pricing convention is the one used by the analysis on October 6, 2026.
{{< /scatter-chart >}}

By simulating a GLM Flash retry on the 11 tasks Luna did not solve, we can chain up to four additional attempts and stop at the first positive verdict.

| Stage | New tasks recovered on this attempt | Luna failures recovered in total | Tasks still unresolved | Combined Luna + GLM Flash coverage |
|---|---:|---:|---:|---:|
| Before GLM Flash | — | 0 of 11 | 11 | 102 of 113, or 90.3% |
| **Attempt 1** | **3** | **3 of 11** | 8 | 105 of 113, or 92.9% |
| **Attempt 2** | **7** | **10 of 11** | 1 | 112 of 113, or 99.1% |
| **Attempt 3** | 0 | 10 of 11 | 1 | 112 of 113, or 99.1% |
| **Attempt 4** | 0 | **10 of 11** | **1** | **112 of 113, or 99.1%** |

In this replay order, GLM Flash’s first attempt recovers 3 of Luna’s 11 failures. The second adds 7. Later attempts add no further success.

{{< thesis >}}
These figures do not mean that GLM-5.3 Flash is better than Astra in absolute terms. They show that its recorded successes overlap more with Luna’s observed failures.

**This is another definition of diversity.**
{{< /thesis >}}

## Diversity is not a model count

Two models can produce different answers while failing on the same problems. Conversely, a model with lower average performance can add enormous value if it succeeds where the first one stalls.

Counting models is not enough. We must measure the complementarity of their errors.

This idea was central to my series [“No Harness Is Perfect”](/en/series/aucun-harnais-n-est-parfait/). In [“Why Adding Agents Does Not Necessarily Create Diversity”](/en/articles/plusieurs-agents-points-de-vue/), I argued that diversity should become an empirical property of the system, observed through disagreements and useful errors.

DeepSWE provides an especially clear illustration. Astra achieves a higher average score than Luna on a single run. Yet when we examine only Luna’s persistent failures, it adds less coverage than GLM-5.3 Flash.

The right question is no longer: which model is best?

{{< pullquote >}}
Which model best recovers the failures that remain after the previous one?
{{< /pullquote >}}

## The oracle turns diversity into routing

This complementarity becomes useful only when the system can recognize a failure.

Without an oracle, we would have to run several models and then ask a person to determine which answer is correct. The supervision cost would rise with the number of proposals.

With tests that can automatically accept or reject a result, the harness can stop at the first success and escalate only the tasks that resist.

```text
Luna, up to four attempts
        ↓ verified failure
GLM-5.3 Flash, up to four attempts
        ↓ verified failure
Final fallback tier
```

The architecture no longer pits an economical model against a premium model. It composes several error profiles and reserves each tier for the cases the previous one could not solve.

## Once the complement is known, order still matters

Once we accept this logic, another question appears: in what order should the models be called?

Luna has the better individual coverage of the two, but GLM-5.3 Flash is cheaper. It can therefore make economic sense to begin with GLM Flash, then send only its failures to Luna.

On an average run, GLM Flash succeeds on 63.4% of tasks for approximately $0.24, compared with 67.2% for $0.61 with Luna. The system gives up only 3.8 percentage points of average first-pass success while cutting the mean cost of an attempt by about 60%. The oracle can then recover the failures instead of paying for Luna on every task.

{{< cost-comparison
  dataset="deepswe-routing-orders"
  title="The same coverage at 36% lower cost"
  description="Both chains earn 113 positive verdicts. Changing only the order of GLM Flash and Luna lowers estimated cost from $119.31 to $76.46."
  x-label="Estimated cost across 113 tasks ($)"
  primary="glm-first"
  cost-label="Estimated cost"
  coverage-label="Positive verdicts"
  attempts-label="Attempts executed"
  scenario-label="Routing order"
  count-label="orders compared"
  details-label="View both scenarios"
>}}
Each bar represents the total cost of a replay that stops at the first success. Both orders use the same three configurations and reach the same observed coverage. Only their sequence changes.
{{< /cost-comparison >}}

After GLM Flash and Luna have run, only one task remains without a positive verdict. For this final case, it can make sense to pay for a more premium model. In this example, I chose GLM-5.2 [max].

As always, using the rollouts published by DeepSWE and stopping at the first success, the following retrospective chain produces these results:

| Stage | Tasks received | Tasks solved at this stage | Attempts executed | Estimated cost |
|---|---:|---:|---:|---:|
| GLM-5.3 Flash [max] | 113 | 96 | 204 | $49.74 |
| Luna [max] on the failures | 17 | 16 | 34 | $20.71 |
| GLM-5.2 [max] on the final case | 1 | 1 | 1 | $6.02 |
| **Retrospective total** | **113** | **113** | **239** | **$76.46** |

These costs are estimated from rollout consumption, using the prices applied by the DeepSWE interface on October 6, 2026. They exclude the full cost of the oracle and its operation.

That is approximately $0.68 per submitted task and 2.12 attempts per task. An attempt is an agent execution, which can make several model calls.

{{< callout variant="key" label="$42.85 saved across 113 tasks" >}}
The reverse order costs $119.31. Starting with GLM Flash brings the estimated bill down to $76.46: **$42.85 less, or about 36% in savings**, with the same observed coverage.

At a comparable volume and workload distribution, that gap would represent approximately **$3,792 in gross savings per 10,000 tasks**, before the cost of the oracle. The value comes from the fact that **238 of its 239 attempts go to the two economical models**.
{{< /callout >}}

The GLM Flash → Luna → GLM-5.2 order does, however, require 30 additional attempts and may increase latency.

The best order depends on our chosen objective: cost, latency, compute consumption, or accepted risk.

## The most useful benchmark may come from your production traffic

DeepSWE is a public example. It obviously does not represent the tasks, constraints, and risks specific to every organization.

But an agentic system in production generates exactly the raw material needed to build an internal benchmark: real requests, available context, produced results, oracle verdicts, human corrections, costs, latency, and escalation reasons.

By collecting these scenarios, anonymizing them, and making them replayable, a team can gradually build a qualification set that represents its actual use. Frequent cases retain their real weight. Incidents, edge cases, and high-impact tasks can deliberately be overrepresented to reflect the risk they carry. This practice belongs to **AI Evals** and, more broadly, **AI Reliability**.

The team can then reproduce the same analysis performed on DeepSWE:

- run several models and configurations on the same scenarios
- observe not only their average score, but also their respective blind spots
- measure which models actually recover the failures of the others
- simulate several routing orders with early stopping
- compare achieved coverage with cost, latency, and residual risk.

Optimization is no longer about “the best model on the market.” It is about **the best combination of models for a specific use case**.

This benchmark must remain alive. New scenarios, human rework, and incidents continuously enrich the error map. Some of the data can be used to choose the strategy. Another portion must remain held out to verify that the strategy still works on cases it did not use for optimization.

Production traffic therefore supplies more than tasks to process. Properly instrumented, it also supplies the test bench that lets the system improve from its own reality.

## After model selection comes portfolio selection

The method applied to DeepSWE is therefore not a universal recipe. It demonstrates an approach that each organization can apply to its own scenarios.

We still often compare models as though we had to elect a single winner.

An agentic architecture poses a different problem. It can try, verify, retry, and change strategy. Its performance then depends as much on model order, error complementarity, and oracle quality as on each model's individual score.

The first model should solve most tasks at low cost. The next one should primarily see what the first one misses. The premium model or a human should intervene only on the genuinely difficult remainder.

We are no longer merely looking for the best model. We are building a portfolio of capabilities whose risks are imperfectly correlated.

The next frontier may not be won by the model at the top of a public leaderboard. It may be won by the system that can learn from its real scenarios, measure its errors, buy the right diversity, and route each failure to the most useful complement.

{{< closing-question label="Key takeaway" >}}
One economical model covers 102 tasks. A second Flash model recovers 10 of its 11 observed failures. By putting the cheapest model first, the simulated chain preserves its coverage and costs **36% less**, saving $42.85 across these 113 tasks.

The next question becomes decisive: **who checks the oracle?**
{{< /closing-question >}}

---

## Sources

- DeepSWE, [v1.1 leaderboard, methodology, and costs](https://deepswe.datacurve.ai/), 113 tasks from 91 open-source repositories across five languages, accessed October 6, 2026.
- DeepSWE, [detailed task and rollout data](https://deepswe.datacurve.ai/data/v1.1), coverage, complementarity, and early-stopping cost calculations.
