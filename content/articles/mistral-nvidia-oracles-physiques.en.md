---
title: "Mistral and NVIDIA: can physics serve as an oracle for AI agents?"
seo_title: "Mistral and NVIDIA: AI agents, simulation and physical oracles"
slug: "mistral-nvidia-physical-oracles"
date: 2026-10-30T18:45:00+01:00
publishDate: 2026-10-30T18:45:00+01:00
lastmod: 2026-10-30T18:45:52+01:00
description: "Connecting an agent to a simulator lets it test its proposals. Reliability still depends on assumptions, acceptance criteria and comparisons with the real world."
categories: ["Artificial Intelligence", "Software Architecture", "Software Engineering"]
tags: ["ai-evaluation-evals", "ai-systems-harness-engineering"]
collection: "SYSTÈMES"
cover: "/images/articles/mistral-nvidia-oracles-physiques.en.png"
draft: false
---

{{< callout variant="scene" label="A lighter part. A verdict to interpret." >}}
An agent proposes a lighter mechanical part. It runs a simulation. The calculated stresses remain below the permitted threshold.

Is the proposal acceptable? That also depends on the simulated load, the material, the fixtures and the phenomena represented by the model.

**A calculation can be correct within its model and still be insufficient for a real-world decision.**
{{< /callout >}}

We are working to make models capable of reasoning, planning and using tools. Yet one question determines the value of all these capabilities: **how do we know whether the result is correct?**

The [announcement by Mistral and NVIDIA on October 21, 2026](https://mistral.ai/fr/news/mistral-nvidia-ai-for-industrial-engineering/) provides a concrete setting for examining this question. Connecting agents to engineering tools could allow their proposals to be tested against calculations and explicit constraints.

In [The Oracle](/en/series/l-oracle/), I examine how an actionable verdict makes it possible to organize multiple attempts and combine models. [No Harness Is Perfect](/en/series/aucun-harnais-n-est-parfait/) highlights the limits: checks inherit their designers’ assumptions and blind spots. Physical engineering brings these two questions together.

## What Mistral and NVIDIA are announcing

The partnership aims to build workflows connecting AI models, simulation and design. It plans public benchmarks and open datasets to evaluate physical models. Agents will also be evaluated in mechanical computer-aided design (CAD), computer-aided engineering (CAE) and electronic design automation (EDA).

For agents, the announced evaluations will cover tool use, multi-step tasks, technical correctness, execution time and computational cost.

**The announcement does not provide results from these future benchmarks.** The proposed work still needs to establish agents’ reliability on these tasks.

Designing such a loop requires deciding how to use its results and under what conditions to accept its verdicts.

## The potential gain: running more experiments

Imagine an engineer trying to reduce a part’s weight without exceeding its allowable deformation. An agent connected to a simulation environment could:

1. Propose a geometry and prepare the parameters.
2. Run the calculation in a controlled environment.
3. Compare the results against the authorized criteria.
4. Use the discrepancies to propose another variant.
5. Stop when a result is acceptable, the budget is exhausted or a review is requested.

The gain could come from exploring more hypotheses, automating calculation setup and comparing trade-offs. It would depend on simulation costs and the quality of the integration. An additional variant has value only if evaluating it provides useful information.

This is the principle developed in [The Oracle, the Real Game Changer in Agentic AI](/en/articles/oracle-real-game-changer-agentic-ai/): when a system can check a proposal, it can organize a search instead of relying solely on the first answer.

In physical engineering, that search must still preserve the connection between **what is being optimized and the conditions under which the result remains valid**.

## The solver calculates. The oracle delivers a verdict.

A simulator produces results: displacements, temperatures, stresses, consumption or propagation delays. These values alone do not establish whether a design can be accepted.

The oracle is the mechanism that compares them against the required properties. It may check a threshold, a margin, convergence or a validity condition. Its verdict therefore also depends on the specification and the chosen tolerances.

| Element | Role in the loop | Example |
| --- | --- | --- |
| Agent | Propose and revise a solution | Modify a part’s geometry |
| Engineering tool | Run the calculation | Estimate its deformation under load |
| Oracle | Interpret results against explicit criteria | Check deformation and calculation validity |
| Harness | Organize attempts and enforce their limits | Protect criteria, bound the budget, retain traces |
| Expert | Qualify the setup and decide on exceptions | Examine a result outside the validated domain |

Compilation, an automated test, a simulation or a measurement can all contribute to an oracle. None of these methods automatically covers every requirement.

{{< pullquote >}}
Physics constrains the real system. Our oracle can access only what our models and instruments allow us to verify.
{{< /pullquote >}}

## A simulation is not reality

In numerical simulation, NASA [distinguishes verification of the model’s implementation from validation through comparison with experiments](https://www.grc.nasa.gov/www/wind/valid/tutorial/overview.html). Solving the chosen equations correctly and representing the phenomenon well enough are two different questions.

Consider our part again. Suppose the calculation covers a static load, while actual use also involves repeated cycles. A variant may satisfy the calculated threshold while remaining insufficiently evaluated for its intended use. The calculation has not necessarily failed: the check did not cover everything that matters.

This is the boundary described in [Your Tests Pass. Reality Can Still Deviate.](/en/articles/happy-path-validation/): repeating a check does not verify the assumptions it leaves outside its scope.

Loads, boundary conditions, parameters, approximations and the validated domain of use must therefore be documented. Comparison with measurements or an independent reference can challenge an assumption shared by several calculations.

Running two solvers with the same incorrect boundary conditions is not enough to produce two independent confirmations.

## Three outcomes, beyond a green or red light

A useful loop must distinguish three states:

- **Compliant with the checked criteria**: the checks pass within the documented domain.
- **Non-compliant**: a usable calculation reveals an unmet requirement.
- **Indeterminate**: the calculation diverges, data is missing, uncertainty prevents a conclusion or the case falls outside the validated domain.

The third state prevents a calculation failure from being confused with a poor design, or an absent result with validation. The harness must then provide for investigation, another method or human review.

It must also protect acceptance criteria. If the agent can reduce the load, change the material or raise the threshold to obtain a favorable result, it can shift the problem instead of solving it. Some changes may be legitimate, but they alter the design contract and require explicit authorization within the workflow.

This is the risk examined in [The Light Is Green. The Mission Remains Unfinished.](/en/articles/goodhart-dans-la-boucle/): optimizing the measure can move the result away from the actual need.

## A benchmark must also test its oracle

A public benchmark can provide common ground for comparison. Interpreting its score requires knowing which tasks it covers, how correctness is established, which checks remain independent of the agent and how indeterminate calculations are handled.

The question developed in [Who Checks the Oracle?](/en/articles/who-checks-oracle/) becomes very concrete here: does a positive verdict correspond to a correct design for its intended use, or merely to compliance with the encoded criteria?

The full cost matters too. Generating more variants consumes computation, storage and sometimes expert revalidation. The time and cost measurements announced in the evaluation program will be useful, but their scope will need to be explicit.

Deciding on industrial use will then require qualifying the chain on its own cases: model and tool versions, physical assumptions, requirements, attempt budgets and review conditions. An aggregate score cannot replace that qualification.

## The next frontier could be the quality of verification

Bringing agents and engineering tools together opens an interesting possibility: exploring more solutions while retaining measurable results at every step.

Engineers will still need to define what is worth optimizing, what can be checked automatically and what requires experimental comparison or human judgment. The harness organizes attempts and reviews according to that division of responsibilities. Oracle verdicts allow the search to continue, stop or request further examination.

{{< thesis >}}
An actionable oracle turns generation into guided search.

**Its qualification determines which decisions that search can justify.**
{{< /thesis >}}

The promise therefore extends beyond more capable models. It also rests on our ability to build relevant checks, retain their evidence and recognize situations in which they cannot support a conclusion.

{{< closing-question label="The architecture question" >}}
If your agent finds a design that passes every check, **what have you established about its real-world behavior and under what conditions?**
{{< /closing-question >}}

---

## Sources

- Mistral AI, [*Mistral fait avancer l’IA pour l’ingénierie avec NVIDIA*](https://mistral.ai/fr/news/mistral-nvidia-ai-for-industrial-engineering/), October 21, 2026.
- NASA Glenn Research Center, [*Overview of CFD Verification & Validation*](https://www.grc.nasa.gov/www/wind/valid/tutorial/overview.html).
