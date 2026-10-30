---
title: "An agent that learns on its own? It’s more complex than we think."
seo_title: "Self-learning AI agents: who validates the lessons?"
slug: "self-learning-agent-harness"
date: 2026-11-02
lastmod: 2026-10-30T18:30:36+01:00
description: "A new study shows that accumulating more experience can degrade a harness. Learning from mistakes also requires knowing which lessons to keep."
categories: ["Artificial intelligence", "Software architecture"]
tags: ["ai-systems-harness-engineering", "ai-evaluation-evals"]
collection: "ARCHITECTURE"
cover: "/images/articles/agent-auto-apprentissage-harness.en.png"
draft: false
---

A new study, [*Forging More Tasks into Better Harnesses*](https://arxiv.org/html/2610.28815v1), published on October 20, 2026, reports a counterintuitive result: **giving an agent more experience to improve how it operates can degrade its performance.** Several methods for evolving the *harness*, the software environment that directs the model, regress as the number of tasks used increases.

The promise is appealing: let an agent work, learn from its failures, enrich its instructions, and create new *skills*, reusable procedures. The more experience it accumulates, the more capable it should become.

The study highlights the difficulty: **which experiences deserve to become rules for the next ones?**

{{< callout variant="scene" label="One mistake. One lesson. Another mistake?" >}}
An agent fails after a database migration. It analyzes its trace, identifies the problem, and adds an instruction to its memory: “Always check migrations before running the tests.”

The next attempt succeeds. Then the rule is applied to a project without a database. The agent searches for migrations that do not exist, wastes time, and drifts away from the problem it needs to solve.

It has stored a lesson. Has it improved its behavior?
{{< /callout >}}

Between “this strategy worked once” and “this strategy should guide my next decisions,” something still needs to be demonstrated.

{{< thesis >}}
The problem of self-learning begins when an experience becomes a rule for the next ones.
{{< /thesis >}}

Here, the agent evolves its harness: instructions, memory, skills, and tool use. **The model weights remain fixed.** It changes how it works based on its experiences, without retraining.

## Five times as many tasks do not guarantee a better harness

The researchers start with a simple question: does an agent get better when it has more experience available to evolve its harness? They vary the number of tasks whose traces are used to propose changes, then evaluate the resulting harness on other tasks.

With **AHE**, an existing method, the harness succeeds on **63%** of evaluation tasks after using experience from **80 tasks**. When it is given experience from **200 tasks**, the success rate falls to **57.7%**. Here, more experience produces a less effective harness.

The authors explain this regression through the way experiences are selected. Redundant or conflicting traces can obscure which changes should be made. Their analysis shows that a carefully chosen subset can lead to a better harness than using all the available experiences.

**The problem is therefore deciding which experiences to use together to guide each change.**

## Select experiences, then compare the changes

To address this problem, the authors propose **Successive Scale Racing (SSR)**. The method ranks experiences by quality and the diversity of situations they cover. It uses groups of different sizes to produce several modified versions of the harness, then compares them on shared tasks and progressively eliminates the weaker versions.

With SSR, the success rate rises from **64.3% to 68.3%** as the available experiences come from **40, then 200 tasks**. This time, the method benefits from the growing amount of experience.

The execution budget increases with the number of tasks used. This experiment therefore does not measure a gain at constant cost.

The work covers three benchmarks and two execution setups.

The reported **60% reduction in validation executions** concerns a separate audit: 12 candidates, 160 tasks, and a comparison against full evaluation. This figure does not mean a 60% reduction in the agent’s total cost.

These results describe the conditions studied. They do not prove that experience always hurts, or that SSR solves every self-learning problem.

For a team designing its system, the question becomes concrete: **which experiences inform each change, and how should the proposed changes be compared?**

## Capture, qualify, select, promote

I propose separating four decisions in the architecture of an agent that builds on its experience.

| Decision | Question to answer | Migration example |
|---|---|---|
| **Capture** | What happened? | Keep the trace, project context, failure, and intervention. |
| **Qualify** | What conclusions does this experience support? | Distinguish the observed fact from the hypothesis about its cause and specify which projects it concerns. |
| **Select** | Which experiences should be combined to guide the proposed change? | Choose complementary migration cases, without letting multiple traces of the same failure dominate the proposal. |
| **Promote** | Can the lesson change future behavior? | Evaluate a conditional instruction before activating it. |

This separation prevents a confidently written summary from immediately becoming a permanent instruction.

Qualifying an experience establishes what can be concluded from it. Selecting it means deciding whether it is relevant to the proposed change and what it adds to the other selected experiences. A reliable experience can be redundant or concern a different context.

Memory can retain a hypothesis without imposing it. It should be able to state: “In a project using this migration mechanism, this check helped resolve this failure.” The context of application remains explicit, allowing the hypothesis to be tested against subsequent experiences.

A skill requires the same discipline. Its trigger, prerequisites, and success criteria are part of what needs to be examined. A procedure that works well for one type of repository may be useless elsewhere.

## A change must be allowed to lose

To make improvement measurable, the system must retain the ability to reject what the agent proposes.

In our example, one candidate might add: “If the project uses migrations and the change affects the schema, check their consistency before running the full suite.” Another might propose a targeted automated check. The current version must remain a point of comparison.

The evaluation should exercise the cases that motivated the change, along with situations where it could impose a cost: a project without a database, a documentation change, or a schema that is already up to date. Success, duration, and tool calls provide different information. A gain on migrations can hide a general slowdown.

The candidate should have a version and a readable diff. The experiences behind the proposal, the evaluations performed, and their results make it possible to understand why it was selected. If behavior deteriorates after activation, the previous version should remain recoverable.

These are architectural choices proposed here, beyond the SSR method. Their purpose is to turn an intuition into a change that can be compared, observed, and reversed.

{{< pullquote >}}
An agent can propose a change, but its merit must be evaluated independently.
{{< /pullquote >}}

That independence can come from deterministic tests, tasks reserved for evaluation, or human review for sensitive changes. Having the same model rephrase the same justification provides little additional evidence.

## What if it mainly learns to pass our tests?

By repeatedly consulting the same test set, an improvement loop can adapt to its particular features. A rising score then does not guarantee better results on the next tasks.

Another study, [*Rethinking the Evaluation of Harness Evolution for Agents*](https://arxiv.org/html/2607.12227v1), asks a concrete question: **with the same compute budget, is it better to modify the harness or let the current agent try several times?**

The researchers compare these options on Terminal-Bench 2.1, a set of tasks performed in a terminal. They give the methods comparable computational resources and information about whether attempts succeed or fail. Modifying the harness does not consistently outperform keeping its configuration and trying several solutions, or correcting an initial attempt.

This possibility particularly interests me: **using response variance to search for a solution the first attempt did not find.** The same model can follow different paths across executions. If a reliable check can recognize an acceptable solution, the system can benefit from that diversity and stop when it finds one. This is the principle developed in [The Oracle]({{< relref "/series/l-oracle" >}}), a series examining verified attempts and model complementarity. Additional attempts are most useful when they explore different paths and their results can be verified.

The study’s authors also evaluate the modified harness on tasks that were not used to guide its changes. **On these new tasks, the improvement remains small.** Gains on the exercises used to modify the agent therefore do not guarantee better performance on subsequent ones.

This work is not an experimental refutation of SSR: the protocols and configurations differ. It establishes a useful requirement for assessing any claimed improvement: separating transferable gains from the effects of extra computation and adaptation to the evaluated cases.

In an operational architecture, I would therefore keep tasks independent of the optimization loop, track regressions by category, and compare against the simple option: keeping the current harness and spending the same budget on solving the task more effectively.

A test set effectively becomes an optimization tool once its results are regularly used to choose changes. Another measure needs to be preserved to estimate what the system has actually gained.

## Automate learning, demonstrate progress

Automating experience capture is useful. Automating change proposals is useful too. But their value depends on the mechanism that decides which lessons deserve to persist.

In [No Harness Is Perfect]({{< relref "/series/aucun-harnais-n-est-parfait" >}}), reliability already depends on the limits of our controls. Self-learning adds a responsibility: checking that the changes emerging from those controls improve subsequent executions.

Engineering shifts toward selecting experiences, comparing candidates, and monitoring effects. It also needs to know how to forget a rule that has become wrong or too costly.

**An agent that changes on its own does not necessarily get better. The architecture must provide evidence that it does.**

{{< closing-question label="The architecture question" >}}
Your agent can record a new lesson. What mechanism can demonstrate that it deserves to guide subsequent tasks, then remove it if it makes them worse?
{{< /closing-question >}}

## Sources

- Jingzhe Liu et al., [*Forging More Tasks into Better Harnesses: Agentic Harness Evolution via Successive Scale Racing*](https://arxiv.org/html/2610.28815v1), arXiv:2610.28815v1, October 20, 2026.
- Yike Wang et al., [*Rethinking the Evaluation of Harness Evolution for Agents*](https://arxiv.org/html/2607.12227v1), arXiv:2607.12227v1, July 14, 2026.
