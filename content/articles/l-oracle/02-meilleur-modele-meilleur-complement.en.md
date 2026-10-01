---
title: "The Most Expensive Model May Be Better Left for Last"
seo_title: "AI agents: why the most expensive model may be better left for last"
slug: "most-expensive-model-better-left-last"
date: 2026-10-01
description: "After one model fails, the best complement is the one with different blind spots—not necessarily the model at the top of the leaderboard."
categories: ["Artificial intelligence", "Software architecture", "Software engineering"]
series: ["l-oracle"]
series_order: 2
collection: "SYSTÈMES"
cover: "/images/articles/meilleur-complement.en.png"
draft: false
---

{{< callout variant="scene" label="Eleven blind spots" >}}
After four attempts, GPT-5.6 Luna solves 102 of the 113 tasks in the DeepSWE benchmark.

Eleven blind spots remain.

The obvious next step might be to escalate to the most powerful model on the leaderboard. Yet GPT-6 Astra recovers only 5 of those 11 tasks.

A far cheaper model does much better: **GLM-5.3 Flash recovers 10**.

**The best model is not necessarily the best complement. To build a reliable agentic system, we must examine not only each model's score, but also how their errors overlap.**
{{< /callout >}}

## A leaderboard hides error profiles

A leaderboard ranks models along one axis: their average performance.

This metric answers a useful question: if I can run only one attempt, which model has the highest probability of succeeding?

It does not answer another question that is essential to agentic architecture: when a first model fails, which model is most likely to succeed specifically on those failures?

The detailed [DeepSWE 1.1](https://deepswe.datacurve.ai/) data lets us examine this. Each configuration was run up to four times on 113 software engineering tasks. Luna `[max]` solves 102 of them at least once. Eleven tasks resist all four attempts.

Among the 70 configurations in the dataset, GLM-5.3 Flash `[max]` complements Luna best: it succeeds at least once on 10 of those 11 tasks.

This result must be read as an escalation. GLM Flash does not start over with all 113 tasks. It receives only the 11 tasks that Luna failed to solve in any of its four runs. We then identify the first GLM Flash attempt that succeeds on each task.

| Stage | New tasks recovered on this attempt | Luna failures recovered in total | Tasks still unresolved | Combined Luna + GLM Flash coverage |
|---|---:|---:|---:|---:|
| Before GLM Flash | — | 0 of 11 | 11 | 102 of 113, or 90.3% |
| **Attempt 1** | **5** | **5 of 11** | 6 | 107 of 113, or 94.7% |
| **Attempt 2** | **2** | **7 of 11** | 4 | 109 of 113, or 96.5% |
| **Attempt 3** | **1** | **8 of 11** | 3 | 110 of 113, or 97.3% |
| **Attempt 4** | **2** | **10 of 11** | **1** | **112 of 113, or 99.1%** |

On its first attempt, GLM Flash clears 5 of Luna's 11 persistent blockers. A second attempt recovers 2 more. The third adds 1, and the fourth produces the final 2 observed successes. Only one task remains unresolved by this pair of models.

The table does not show four independent scores. It shows the cumulative progress enabled by the oracle: after each failure, another attempt is launched only for the tasks that still resist.

| Model added after Luna | Luna failures recovered | Combined coverage |
|---|---:|---:|
| **GLM-5.3 Flash [max]** | **10 of 11** | **112 of 113, or 99.1%** |
| Claude Opus 5 [medium] | 9 of 11 | 111 of 113, or 98.2% |
| Claude Sonnet 5 [max] | 8 of 11 | 110 of 113, or 97.3% |
| GPT-6 Astra [xhigh] | 5 of 11 | 107 of 113, or 94.7% |

{{< thesis >}}
These figures do not mean that GLM-5.3 Flash is better than Astra in absolute terms. They show that its strengths land far more often in Luna's blind spots.

**This is another definition of diversity.**
{{< /thesis >}}

## Diversity is not a model count

Two models can produce different answers while failing on the same problems. Conversely, a model with lower average performance can add enormous value if it succeeds where the first one stalls.

Counting models is not enough. We must measure the complementarity of their errors.

This idea was central to my series [“No Harness Is Perfect”](/en/series/aucun-harnais-n-est-parfait/). In [“Why Adding Agents Does Not Necessarily Create Diversity”](/en/articles/plusieurs-agents-points-de-vue/), I argued that diversity should become an empirical property of the system, observed through disagreements and useful errors.

DeepSWE provides an especially clear illustration. Astra achieves a higher average score than Luna on a single run. Yet when it is given only Luna's persistent failures, it adds less coverage than GLM-5.3 Flash.

The right question is no longer: which model is best?

{{< pullquote >}}
Which model best reduces the risk that remains after the previous one?
{{< /pullquote >}}

## The oracle turns diversity into routing

This complementarity becomes useful only when the system can recognize a failure.

Without an oracle, we would have to run several models and then ask a person to determine which answer is correct. The supervision cost would rise with the number of proposals.

With tests that can automatically accept or reject a result, the harness can stop at the first success and escalate only the tasks that resist.

The system therefore does not have to pay for four additional attempts every time. As the progression above shows, the oracle stops GLM Flash as soon as a task is validated and reserves later attempts for the cases that are still failing.

```text
Luna, up to four attempts
        ↓ verified failure
GLM-5.3 Flash, up to four attempts
        ↓ verified failure
Final fallback tier
```

The architecture no longer pits an economical model against a premium model. It composes several error profiles and reserves each tier for the cases the previous one could not solve.

## The cheapest model can go first

Once we accept this logic, another question appears: in what order should the models be called?

Luna has the better individual coverage of the two, but GLM-5.3 Flash is cheaper. It can therefore make economic sense to begin with GLM Flash, then send only its failures to Luna.

Using the rollouts published by DeepSWE and stopping at the first success, the following retrospective chain produces these results:

| Stage | Tasks received | Tasks solved at this stage | Attempts executed | Observed cost |
|---|---:|---:|---:|---:|
| GLM-5.3 Flash [max] | 113 | 96 | 206 | $47.70 |
| Luna [max] on the failures | 17 | 16 | 30 | $20.15 |
| GLM-5.2 [max] on the final case | 1 | 1 | 1 | $6.02 |
| **Retrospective total** | **113** | **113** | **237** | **$73.87** |

That is approximately $0.65 per submitted task. The chain's value does not come from making fewer calls: it executes an average of 2.10 attempts per task.

{{< callout variant="key" label="The cost shifts tiers" >}}
The value comes from the fact that **236 of its 237 calls go to the two economical models**.
{{< /callout >}}

The reverse order—Luna followed by GLM Flash—uses fewer attempts but costs $123.05. Starting with GLM Flash therefore saves about 40%, at the price of 26 additional calls and potentially higher latency.

The best order depends on the compass we choose: cost, latency, compute consumption, or accepted risk.

## The 113 out of 113 to be wary of

In the observed data, the GLM Flash → Luna → GLM-5.2 chain covers all 113 benchmark tasks.

That result is spectacular. It is not a promise of perfect success.

The models, their configurations, and their order were selected after examining their results on those same 113 tasks. The chain therefore benefits from *a posteriori* optimization. It may have learned the peculiarities of the benchmark rather than a strategy that will generalize.

Two claims remain defensible:

- the observed union of Luna and GLM-5.3 Flash reaches 99.1%;
- their error profiles differ enough for oracle-based routing to deserve prospective testing.

To estimate real-world performance, we would need to choose the policy on one set of tasks, then replay it unchanged on a fresh sample from the target workload. We could then measure its coverage, cost, latency, false positives, and false negatives.

This precaution is not a statistical footnote. An agentic architecture is itself a hypothesis that must be tested against an external oracle.

## The most useful benchmark may come from your production traffic

DeepSWE is a public example. It obviously does not represent the tasks, constraints, and risks specific to every organization.

But an agentic system in production generates exactly the raw material needed to build an internal benchmark: real requests, available context, produced results, oracle verdicts, human corrections, costs, latency, and escalation reasons.

By collecting these scenarios, anonymizing them, and making them replayable, a team can gradually build a qualification set that represents its actual use. Frequent cases retain their real weight. Incidents, edge cases, and high-impact tasks can deliberately be overrepresented to reflect the risk they carry.

The team can then reproduce the same analysis performed on DeepSWE:

- run several models and configurations on the same scenarios;
- observe not only their average score, but also their respective blind spots;
- measure which models actually recover the failures of the others;
- simulate several routing orders with early stopping;
- compare achieved coverage with cost, latency, and residual risk.

Optimization is no longer about “the best model on the market.” It is about **the best combination of models for a specific use case**.

This benchmark must remain alive. New scenarios, human rework, and incidents continuously enrich the error map. Some of the data can be used to choose the strategy; another portion must remain held out to verify that the strategy still works on cases it did not use for optimization.

Production traffic therefore supplies more than tasks to process. Properly instrumented, it also supplies the test bench that lets the system improve from its own reality.

## After model selection comes portfolio selection

DeepSWE is therefore not a universal recipe. It demonstrates a method that each organization can apply to its own scenarios.

We still often compare models as though we had to elect a single winner.

An agentic architecture poses a different problem. It can try, verify, retry, and change strategy. Its performance then depends as much on model order, error complementarity, and oracle quality as on each model's individual score.

The first model should solve most tasks at low cost. The next one should primarily see what the first one misses. The premium model or a human should intervene only on the genuinely difficult remainder.

We are no longer merely looking for the best model. We are building a portfolio of capabilities whose risks are imperfectly correlated.

The next frontier may not be won by the model at the top of a public leaderboard. It may be won by the system that can learn from its real scenarios, measure its errors, buy the right diversity, and route each failure to the most useful complement.

{{< closing-question label="Key takeaway" >}}
One economical model covers 102 tasks. A second Flash model recovers 10 of its 11 blind spots. Thanks to the oracle, their combined coverage reaches 99.1%.
{{< /closing-question >}}

---

## Sources

- DeepSWE, [v1.1 leaderboard, methodology, and costs](https://deepswe.datacurve.ai/), 113 tasks from 91 open-source repositories across five languages, updated September 22, 2026.
- DeepSWE, [detailed task and rollout data](https://deepswe.datacurve.ai/data/v1.1), coverage, complementarity, and early-stopping cost calculations.
- Kévin Brunet, [“Why Adding Agents Does Not Necessarily Create Diversity”](/en/articles/plusieurs-agents-points-de-vue/), diversity measured through disagreements and useful errors.
- Kévin Brunet, [“Blind Decorrelation”](/en/articles/decorreler-a-l-aveugle/), routing disagreements and adapting validation cost to the information obtained.
