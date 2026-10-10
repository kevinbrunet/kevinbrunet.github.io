---
title: "The Oracle, the Real Game Changer in Agentic AI"
seo_title: "Oracles and agentic AI: why verification changes the best model"
slug: "oracle-real-game-changer-agentic-ai"
date: 2026-10-27
description: "Well-defined tasks, verifiable results, and more processing time: across 113 tasks, move from about $1,338 for 74% success to $76 for 100%."
categories: ["Artificial intelligence", "Software architecture", "Software engineering"]
tags: ["ai-systems-harness-engineering", "ai-evaluation-evals"]
series: ["l-oracle"]
series_order: 1
collection: "SYSTÈMES"
cover: "/images/articles/oracle-agentique.en.png"
draft: false
---

{{< callout variant="scene" label="Lower cost, with more processing time" >}}
**If tasks are well defined and their results can be verified, allowing more processing time can substantially reduce the bill.** Across the 113 tasks studied, **Claude Opus 5 [max], the highest-ranked Claude configuration on DeepSWE, represents approximately $1,338 for a 74% average single-attempt success rate**. The replayed chain achieves **100% success for $76**.

This becomes possible when a system can automatically verify an answer, reject a failure, and continue its search. This underestimated piece of infrastructure is called **the oracle**.
{{< /callout >}}

## Follow the data rather than reputation

Even before adding attempts, comparing configurations across their available runs already identifies a less expensive model with a very similar average success rate on these tasks:

| Configuration | Average single-attempt success rate | Estimated mean cost per attempt | Estimated budget for one attempt across 113 tasks |
|---|---:|---:|---:|
| Claude Opus 5 [max] | 73.6% | $11.84 | $1,338.38 |
| GPT-6 Astra [xhigh] | 74.1% | $4.43 | $500.49 |

**Replacing this Claude configuration with Astra already reduces the mean cost per attempt by 62.6%, with a comparable average success rate.**

The oracle then allows us to go further: compare models over multiple attempts rather than only their first answer.

## The ranking changes when multiple attempts are allowed

The [DeepSWE 1.1](https://deepswe.datacurve.ai/) benchmark evaluates development agents on 113 software engineering tasks drawn from 91 open-source repositories and spanning five languages.

The main leaderboard measures the average success rate of a single run. By that measure, Astra ranks ahead of Luna. On this task set and between these two configurations, Astra therefore achieves the better average result with a single chance.

The detailed data allows another reading. Each configuration has up to four runs per task. We can count tasks accepted at least once across the available attempts.

In this article, “solved” means accepted by the benchmark’s grader, the program that issues the verdict. The reliability of that verdict will be examined in [the third article](/en/articles/who-checks-oracle/).

Luna then reaches 90.3% coverage, solving 102 of 113 tasks. Astra reaches 80.5%, or 91 tasks.

| Configuration | Single-attempt success | Coverage across up to four attempts | Estimated mean cost per attempt | Estimated budget for four attempts |
|---|---:|---:|---:|---:|
| GPT-6 Astra [xhigh] | **74.1%** | 80.5%, or 91 of 113 | $4.43 | $17.72 |
| GPT-5.6 Luna [max] | 67.2% | **90.3%, or 102 of 113** | **$0.61** | **$2.42** |

The contrast becomes even more interesting when we look at cost.

Costs are estimates based on rollout consumption and the prices used by the DeepSWE interface on October 6, 2026. The four-attempt budget is four times the unrounded mean cost.

{{< cost-comparison
  dataset="deepswe-luna-astra-budget"
  title="A 45% lower budget"
  description="Four Luna attempts cost approximately $2.42 per task, compared with $4.43 for one Astra attempt. Luna reaches 90.3% coverage across four chances; Astra succeeds on an average 74.1% of tasks with one chance."
  x-label="Estimated budget per task ($)"
  primary="luna-four"
  cost-label="Estimated budget per task"
  coverage-label="Coverage or mean success"
  coverage-suffix="%"
  attempts-label="Attempts allowed"
  scenario-label="Configuration"
  count-label="budgets compared"
  details-label="View both budgets"
>}}
The bars compare budgets only. Across 113 tasks billed at these mean costs, the theoretical gap reaches $227.13. Luna’s 90.3% is the observed union across four runs; Astra’s 74.1% is the mean success rate of one run.
{{< /cost-comparison >}}

A model that is less reliable on its first attempt can therefore become more valuable inside an architecture built to exploit multiple attempts.

That does not make Luna the best model in absolute terms. The result depends on the system built around it.

## A failure can trigger the next attempt

The mechanism has three steps. The agent produces a solution. The oracle returns `OK` or `FAIL`. If the result is accepted, the system stops. If it is rejected, another attempt can be launched.

In a real agentic loop, tests and failure traces could feed that next attempt. **This does not happen in the DeepSWE data used here**: the rollouts are independent and do not share diagnostics. I will need to test this information-sharing loop under the benchmark conditions to determine whether it increases coverage, reduces the number of attempts, or lowers total cost.

A failed first run therefore no longer ends the task. It triggers the next attempt. The success rate of one run is no longer the system's performance ceiling.

Luna's results show the scale of the shift. It succeeds on an average of 67.2% of tasks in one run, then covers 90.3% across four separate runs. On this observed coverage measure, it overtakes Astra.

An oracle is a mechanism that can automatically decide whether a proposal satisfies the expected conditions of the solution. It turns an answer into a verdict the system can act on: accept, reject, or request another check.

In software engineering, that oracle can combine compilation, type checking, unit tests, integration tests, and interface or API tests. In other fields, it might verify that accounts balance, reconcile a total against an independent source, enforce integrity constraints, or confirm that a case meets eligibility rules. The oracle automatically guarantees compliance with the encoded criteria; its reliability depends on how accurately those criteria represent the expected result.

When a reliable oracle exists, generation becomes a search loop:

```text
Produce a proposal
        ↓
Verify the result
        ↓
   Valid result?
   ├─ yes → deliver
   └─ no  → retain diagnostics
                    ↓
              correct and retry
```

The oracle decides whether the work is acceptable. The harness retains errors, test output, and useful traces. The next attempt therefore does not necessarily start from scratch.

## DeepSWE still measures separate attempts

The runs used in this DeepSWE calculation are separate rollouts, up to four per task. On its second attempt, Luna does not receive the diagnostics produced by the first.

The increase from 67.2% to 90.3% therefore measures what multiple attempts already achieve without sharing information between them. This simple mechanism is enough to reverse the ranking.

The real question begins after that: how far can we go when every failure adds information?

A failed test can identify the unmet assertion, the observed value, or the relevant execution path. The harness can pass these details to the model, retain the approaches already attempted, and request a targeted correction. The second attempt then starts with more information than the first, and the third with more than the second.

DeepSWE does not provide that number. It already lets us test the most basic case: what happens when a model is allowed to fail and try again? Its coverage across up to four attempts offers a comparison point for separate retries, not the ceiling of an adaptive loop.

## Variance is not enough: the system must buy the right diversity

Luna’s additional attempts raise its observed coverage from an average 67.2% on one run to 90.3% across the four available runs. Yet 11 tasks still have no recorded success.

Asking the same model to keep trying is therefore not necessarily the best use of the budget. The next step is to find another model whose errors overlap as little as possible with Luna’s: not the model that ranks highest overall, but the one that succeeds specifically where Luna fails.

The oracle makes that complementarity measurable. For every candidate model, the system can count recovered failures, required attempts, and cost. Once the right pair is known, it can still compare routing orders, placing the more economical model first and paying for the next one only on the remainder.

{{< pullquote >}}
The best model is not necessarily the one that succeeds most often on its own. It is the one that adds the most successful outcomes to the system for every dollar spent.
{{< /pullquote >}}

## Another way to buy intelligence

This interpretation suggests an architecture that differs from the reflex of sending every task to the best model available.

A system can begin with an economical model, verify every result, and stop at the first success. Tasks that resist can then be escalated to a premium model or a person.

```text
Verifiable task
      ↓
Fast, economical model
      ↓
Oracle
├─ result accepted → deliver
└─ result rejected → diagnostics + another attempt
                         ↓
                  limit reached?
                  ├─ no  → new strategy
                  └─ yes → premium model or human
```

Performance then comes from a combination: an economical model, diverse attempts, a reliable oracle, early stopping, and escalation. The most expensive intelligence intervenes only on the cases that resisted.

## After the race for models comes the race for oracles

We have grown accustomed to evaluating AI like a candidate sitting an exam: one question, one answer, one grade. An agent can try, observe a failure, change its approach, and try again. Its value depends as much on the system organizing that search as on its first answer.

A cheaper, more variable model can then become preferable, provided that its work can be verified.

The next stage of agentic AI will not consist solely of producing ever more intelligent models. It will also involve building environments that can tell them when their work is acceptable and when they must try again.

After the race for models will probably come the race for oracles.

Those who can automatically verify agent work will be able to run more experiments, use less expensive models, and reserve premium intelligence for the genuinely difficult cases.

{{< closing-question label="In the next article" >}}
The next question is no longer: how many times should we retry? It is: **which other model sees what Luna misses?**

The DeepSWE data contains a second surprise. Luna's best complement is neither the highest-ranked nor the most expensive model.

We will then see that once this complement has been found, **reversing the chain order cuts its bill by another 36%**.
{{< /closing-question >}}

---

## Sources

- DeepSWE, [v1.1 leaderboard, methodology, and costs](https://deepswe.datacurve.ai/), 113 tasks, 91 repositories, five languages, displayed scores and costs, accessed October 6, 2026.
- DeepSWE, [detailed task and rollout data](https://deepswe.datacurve.ai/data/v1.1), calculation of tasks solved at least once across up to four runs: Luna 102/113, Astra 91/113.
- OpenAI, [GPT-5.6 Luna documentation and pricing](https://developers.openai.com/api/docs/models/gpt-5.6-luna), $0.20 per million input tokens, $0.02 for cached input, and $1.20 for output.
