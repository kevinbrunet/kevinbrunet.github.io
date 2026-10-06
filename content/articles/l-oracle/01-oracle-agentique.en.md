---
title: "The Oracle, the Real Game Changer in Agentic AI"
seo_title: "Oracles and agentic AI: why verification changes the best model"
slug: "oracle-real-game-changer-agentic-ai"
date: 2026-10-27
description: "With a reliable oracle, several attempts from an economical model can solve more tasks than one attempt from a premium model."
categories: ["Artificial intelligence", "Software architecture", "Software engineering"]
tags: ["ai-systems-harness-engineering", "ai-evaluation-evals"]
series: ["l-oracle"]
series_order: 1
collection: "SYSTÈMES"
cover: "/images/articles/oracle-agentique.en.png"
draft: false
---

{{< callout variant="scene" label="The ranking flips" >}}
One attempt with GPT-6 Astra succeeds more often than one attempt with GPT-5.6 Luna.

Yet up to four attempts with Luna cover more tasks and cost less than a single attempt with Astra.

**This result goes beyond a contest between two models. As soon as a system can automatically verify an answer, their ranking can change.**

This underestimated piece of infrastructure is called **the oracle**.
{{< /callout >}}

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

Costs are estimates based on rollout consumption and the prices used by the DeepSWE interface on October 6, 2026. The four-attempt budget is four times the unrounded mean cost; it assumes no early stopping and excludes the full operating cost of the oracle.

**Four Luna attempts therefore represent approximately $2.42. One Astra attempt represents $4.43.**

{{< thesis >}}
At a lower cost, Luna can explore four solutions and solve a larger share of the tasks. A model that is less reliable on its first attempt can become more valuable inside an architecture built to exploit multiple attempts.
{{< /thesis >}}

That does not make Luna the best model in absolute terms. The result depends on the system built around it.

## A failure can trigger the next attempt

The mechanism has three steps. The agent produces a solution. The oracle returns `OK` or `FAIL`. If the result is accepted, the system stops. If it is rejected, the tests and failure traces feed the next attempt.

A failed first run therefore no longer ends the task. It triggers the next attempt. The success rate of one run is no longer the system's performance ceiling.

Luna's results show the scale of the shift. It succeeds on an average of 67.2% of tasks in one run, then covers 90.3% across four separate runs. On this observed coverage measure, it overtakes Astra.

In software development, the oracle relies on executable tests that verify the expected behavior. Compilation, types, and static analysis provide additional controls, but they are not enough to establish that the task was completed correctly. Other domains have their own oracles: integrity constraints for data, independent recomputation of a calculation, a simulator for a plan, or eligibility rules for a business process.

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

DeepSWE does not provide that number yet. Its coverage across up to four attempts offers a comparison point for separate retries, not the ceiling of an adaptive loop.

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

## Oracle quality becomes decisive

This architecture shifts part of the problem toward verification.

We need to distinguish two failure modes.

The first comes from the oracle itself. Incomplete tests can accept an incorrect program simply because the faulty behavior was never translated into a check. This is the [*oracle problem*](https://doi.org/10.1109/TSE.2014.2372785), long studied in software engineering and explored in my series [“No Harness Is Perfect”](/en/series/aucun-harnais-n-est-parfait/).

The second appears when the agent discovers that it can satisfy or manipulate the metric instead of solving the task. It can hard-code expected values, weaken tests to obtain a favorable verdict, or disable the grader. This is *reward hacking*, a mechanism I examined in [“The Light Is Green. The Mission Remains Unfinished.”](/en/articles/goodhart-dans-la-boucle/).

These behaviors have been observed in practice. [METR](https://metr.org/blog/2025-06-05-recent-reward-hacking/) published cases of agents modifying evaluation code or retrieving the expected answer directly. The [Claude 3.7 Sonnet system card](https://www.anthropic.com/claude-3-7-sonnet-system-card) describes hard-coded test values and tests modified after repeated failures. [OpenAI](https://openai.com/index/how-we-monitor-internal-coding-agents-misalignment/) also classifies test modification and disabled checks among the rare but severe forms of reward hacking observed with its internal coding agents.

The problem exists even without explicit modification of the grader. [SpecBench](https://arxiv.org/abs/2605.21384) shows that agents can saturate visible tests while still failing hidden tests that recombine the same features in more realistic uses.

{{< pullquote >}}
A poor oracle does not make the system safe. It industrializes two kinds of error: false positives, when it accepts a bad answer, and false negatives, when it rejects a good solution.
{{< /pullquote >}}

The acceptable number of attempts therefore depends on verdict reliability. The third article will examine this constraint, the known flaws in DeepSWE’s grader, and the precautions needed before acting on these figures.

Building a good oracle requires defining what must be true, testing edge cases, and—when the stakes justify it—combining several independent checks.

{{< callout variant="key" label="A favorable domain" >}}
Software development is therefore fertile ground for agents. It lets us express the expected result as automated tests, then supplement that verification with compilation, types, static analysis, and continuous integration.
{{< /callout >}}

In many other fields, the main obstacle may not be model quality. It may be the absence of an automatable definition of work done well.

## After the race for models comes the race for oracles

We have grown accustomed to evaluating AI like a candidate sitting an exam: one question, one answer, one grade. An agent can try, observe a failure, change its approach, and try again. Its value depends as much on the system organizing that search as on its first answer.

A cheaper, more variable model can then become preferable, provided that its work can be verified.

The next stage of agentic AI will not consist solely of producing ever more intelligent models. It will also involve building environments that can tell them when their work is acceptable and when they must try again.

After the race for models will probably come the race for oracles.

Those who can automatically verify agent work will be able to run more experiments, use less expensive models, and reserve premium intelligence for the genuinely difficult cases.

One limitation remains. Across the published runs, Luna still leaves 11 tasks without a recorded success. These observed failures give us a lead for choosing the next model, without proving that Luna would be unable to solve them.

{{< closing-question label="In the next article" >}}
The next question is no longer: how many times should we retry? It is: **which other model sees what Luna misses?**

The DeepSWE data contains a second surprise. Luna's best complement is neither the highest-ranked nor the most expensive model.
{{< /closing-question >}}

---

## Sources

- DeepSWE, [v1.1 leaderboard, methodology, and costs](https://deepswe.datacurve.ai/), 113 tasks, 91 repositories, five languages, displayed scores and costs, accessed October 6, 2026.
- DeepSWE, [detailed task and rollout data](https://deepswe.datacurve.ai/data/v1.1), calculation of tasks solved at least once across up to four runs: Luna 102/113, Astra 91/113.
- OpenAI, [GPT-5.6 Luna documentation and pricing](https://developers.openai.com/api/docs/models/gpt-5.6-luna), $0.20 per million input tokens, $0.02 for cached input, and $1.20 for output.
- Barr et al., [*The Oracle Problem in Software Testing: A Survey*](https://doi.org/10.1109/TSE.2014.2372785), *IEEE Transactions on Software Engineering*, 2015.
- METR, [*Recent Frontier Models Are Reward Hacking*](https://metr.org/blog/2025-06-05-recent-reward-hacking/), June 5, 2025, examples of test, score, and evaluation-environment manipulation.
- Anthropic, [*Claude 3.7 Sonnet System Card*](https://www.anthropic.com/claude-3-7-sonnet-system-card), “Excessive Focus on Passing Tests,” including hard-coded values and modified tests.
- OpenAI, [*How we monitor internal coding agents for misalignment*](https://openai.com/index/how-we-monitor-internal-coding-agents-misalignment/), test modification and disabled checks classified as reward hacking.
- Zhao et al., [*SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents*](https://arxiv.org/abs/2605.21384), preprint, 2026, comparison between visible and hidden tests.
