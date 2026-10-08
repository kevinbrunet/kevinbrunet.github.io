---
title: "Who Checks the Oracle?"
seo_title: "Agentic oracles: false positives, retries, and grader reliability"
slug: "who-checks-oracle"
date: 2026-10-27
description: "More attempts pay off only when the verdict is reliable. False positives, grader bugs, and manipulated tests change an agent's search budget."
categories: ["Artificial intelligence", "Software architecture", "Software engineering"]
tags: ["ai-evaluation-evals", "ai-systems-harness-engineering"]
series: ["l-oracle"]
series_order: 3
collection: "SYSTÈMES"
cover: "/images/articles/qui-verifie-oracle.en.png"
draft: false
---

{{< callout variant="scene" label="The verdict becomes the product" >}}
An agent proposes a fix. The tests pass. The system delivers.

A second proposal might have been better. A tenth might have bypassed the check. We will not know: the first positive verdict stopped the search.

**Once the oracle controls the attempts, a verification error becomes a system decision.**
{{< /callout >}}

The first two articles explained the mechanism: several attempts can outperform a premium model on its first try, and another model can then recover the previous model's failures.

One condition remains to be examined: how much is the `OK` that authorizes delivery worth?

## A recorded success is not yet proof

In the DeepSWE data we examined, Luna obtains at least one positive verdict on 102 tasks. With GLM-5.3 Flash, the union reaches 112 of 113. These calculations are reproducible from individual results.

But they count grader acceptances. On their own, they do not demonstrate that 112 requests were correctly completed.

An oracle can err in both directions: accept a bad solution, a **false positive**, or reject a good solution, a **false negative**. The first can let a defect through. The second can trigger unnecessary attempts and escalation.

This problem is not merely theoretical. In its [review of DeepSWE v1.1](https://epoch.ai/benchmarks/deepswe/review), published on September 7, 2026, Epoch AI documents false negatives on at least 23 of the 113 tasks. Its investigation stopped after reaching the threshold for a “Flawed” verdict. It therefore does not measure the benchmark's false positives.

We must not turn “23 affected tasks” into “20.3% of attempts graded incorrectly.” Those are different denominators.

These data remain useful for exploring the value of retries and identifying possible complementarities between models. They provide architectural hypotheses to test. To determine whether the observed gains correspond to genuinely correct work, we need to fix the identified grader flaws and revalidate the proposals through independent verification.

**The lesson is to qualify the oracle before entrusting it with routing and delivery.** That qualification is what turns recorded coverage into an actionable result.

## Changing tests can also expose a bad grader

The grader must apply the agent's proposal and then run its own verification. That operation can itself break the test environment.

Epoch describes collisions between function names added by the agent and those in hidden tests, as well as helper functions removed when the grader replaces a file. The tested code can then be rejected because of a compilation or test collection error.

In these cases, adding or adapting tests was legitimate development work. The agent was not necessarily trying to deceive the evaluation.

**Touching tests is therefore not enough to establish cheating.** We must inspect what changed and what the subsequent verification measures.

This directly concerns our example. One of Luna's 11 tasks without a success, `obsidian-linter-auto-table-of-contents`, appears in Epoch's list. GLM Flash obtains a recorded success on that task. However, the review cites other configurations: it does not demonstrate that the Luna attempts used here were false negatives.

This overlap justifies inspecting the trajectories. It neither allows us to automatically correct their verdicts nor to attribute GLM's gain to a particular bug.

A false negative can also enlarge the apparent gain from retries: a later proposal can avoid a grader flaw triggered by an earlier one. A better score then does not necessarily mean better work.

## The model that passes most often may also bypass the check

The opposite risk runs the other way. An agent can weaken an assertion, remove a test, hard-code an expected answer, or disable a check. It then obtains the desired verdict without fulfilling the request.

[METR](https://metr.org/blog/2025-06-05-recent-reward-hacking/) has published examples of this reward hacking in coding agents. The possibility therefore exists. It does not prove that Luna or GLM Flash exploited it in the results compared here.

When a model succeeds more often, several explanations remain possible: it completes the task better, its proposals better avoid a grader flaw, or they better exploit a weakness in the check. Harness quality and configuration also contribute to the result.

Without inspecting proposals and performing independent validation, a higher score cannot distinguish these explanations.

{{< pullquote >}}
The model that performs best against the grader is not automatically the one that produces the most correct work.
{{< /pullquote >}}

## More attempts, more opportunities for a false positive

Now suppose that every proposal for a task remains incorrect. Each attempt gives the oracle another opportunity to accept one by mistake.

Let `β` be the probability that it accepts a proposal **given that the proposal is incorrect**. If this probability is constant and acceptance errors are independent across attempts, the risk of at least one false acceptance among `k` incorrect proposals is:

```text
Risk = 1 − (1 − β)^k
```

With a hypothetical rate of `β = 0.5%`, we obtain:

| Incorrect proposals submitted | Risk of at least one false acceptance |
|---|---:|
| 1 | 0.5% |
| 4 | 1.99% |
| 12 | 5.84% |

This table illustrates a mechanism. It is not an estimate of DeepSWE's actual risk.

For small risks, the approximation `k × β` is useful. It becomes less accurate as cumulative risk grows. Above all, independence is not guaranteed: several proposals can share the same defect or exploit the same loophole.

Even a deterministic oracle is affected. Its program does not change, but the proposals submitted to it do. Some errors consistently pass its checks.

Even when attempts are linked, adding their risks can provide a conservative upper bound. Suppose each of four incorrect proposals has at most a 0.5% risk of being accepted. The risk that at least one passes is then at most 2%.

Why an upper bound? Because errors can overlap. If all four attempts encounter exactly the same loophole in the same cases, adding their risks counts those cases several times. At the extreme, if all four false-acceptance events are identical, the total risk remains 0.5%. If each affects different cases, with no overlap, it reaches 2%. The sum therefore remains an upper bound even without knowing how the attempts are linked. It does not give the exact risk.

The essential condition lies in the words **“at most.”** We need to justify that bound for each attempt, on the tasks and under the conditions where the system uses it. An average rate of 0.5% on a benchmark does not guarantee that each escalation stage stays below that threshold. Tasks that resist can concentrate the oracle's weaknesses and carry a higher risk.

**Adding justified upper bounds lets us limit risk. Adding averages measured elsewhere is not enough to guarantee it.**

## A false-positive rate needs its denominator

In its [DeepSWE launch article](https://deepswe.datacurve.ai/blog/deepswe), Datacurve reported approximately 0.3% false positives for DeepSWE, compared with 8.5% for SWE-bench Pro.

The [detailed evaluation results](https://deepswe.datacurve.ai/artifacts/v1/critiques.json) specify the measure: 2 proposals accepted but judged bad out of 735 reviewed rollouts for DeepSWE, compared with 67 out of 789 for SWE-bench Pro. Proposal classification relied on an LLM judge.

These proportions concern **all reviewed rollouts**, not just incorrect proposals. They are therefore not directly the `β` in our formula. They also come from the initial evaluation, not a measurement of errors on the residual tasks in our v1.1 chain.

If `f` denotes the proportion of false positives among all attempts, then, for the same population:

```text
β = f / proportion of incorrect proposals
```

With `f = 0.3%` and a **hypothetical** share of 40% incorrect proposals, we would obtain `β ≈ 0.75%`. The 40% figure is not established here: 0.75% must not become a claimed characteristic of DeepSWE.

The proportion of errors among delivered answers is yet another measure. It depends on the correct solutions produced, false negatives, and the stopping rule. A single “false-positive rate” does not describe the whole system.

## The attempt budget depends on oracle quality

Under the earlier assumption of constant, independent risks, a tolerance `r` gives a maximum number of attempts:

```text
k_max = floor(ln(1 − r) / ln(1 − β))
```

For small risks, `k_max ≈ r / β` gives an order of magnitude. With a 2% tolerance and `β = 0.5%`, four incorrect proposals remain just below the threshold in this model. The fifth exceeds it.

This formula is not enough to set a production policy. We need a conservative estimate of `β` that is relevant to the cases being handled, and must account for its uncertainty and dependence between attempts.

{{< thesis >}}
Oracle quality determines the search budget the system can exploit at a constant accepted risk.

**A better oracle enables more useful attempts.**
{{< /thesis >}}

This constraint reinforces the argument of the first two articles. Reducing verification errors can make more economical attempts available. However, the cost of building, running, and maintaining the oracle belongs in the calculation.

{{< callout variant="key" label="Gross savings are not net gains" >}}
In the previous example, the simulated chain costs approximately **$2,848 less across 113 tasks** than one attempt with the most expensive Claude configuration. That amount is the gross budget available to fund verification.

Net gains must still subtract oracle execution and maintenance, human revalidation, and the expected cost of accepted errors. If those charges exceed that gross saving at a comparable volume, the architecture may improve coverage, but **it does not save money**.
{{< /callout >}}

## Escalation concentrates difficult cases

A chain of three models, each allowed four attempts, can submit up to twelve proposals for a task that passes through every tier.

Using the previous example, if each of the twelve incorrect proposals has a false-acceptance risk capped at 0.5%, the total risk is **at most 6%**, even without independence: `12 × 0.5%`. With constant, independent risks of 0.5%, the exact calculation gives **5.84%**. These figures illustrate the example's assumptions, not the measured risk of our DeepSWE chain.

Not every task receives twelve attempts: a positive verdict stops the chain. But repeatedly rejected cases accumulate opportunities for false acceptance. They are also the cases where verification may be hardest.

We therefore cannot apply a benchmark-wide average rate unchecked to the tasks that remain after eight failures. The relevant rate can depend on the task, model, harness, proposal type, and diagnostics already shared.

Diversifying models can increase coverage. It does not guarantee independent oracle errors: all models can encounter the same incomplete check.

{{< pullquote >}}
For a critical task, automatic escalation can become counterproductive: it multiplies opportunities to accept an error. A human must be involved from the outset.
{{< /pullquote >}}

## What we need to know before entrusting it with delivery

A usable oracle needs a specification sheet, like any critical component:

- **What it verifies**: covered behaviors, requirements left unchecked, edge cases, and environmental dependencies.
- **Its measured errors**: false positives and false negatives, with their denominators, classification method, and uncertainty.
- **Where the measurements apply**: tasks, models, harnesses, and versions used to obtain them, particularly escalation cases.
- **What the agent can change**: code, tests, configuration, and tools. Trusted checks must be protected.
- **Dependence between attempts**: shared defects, diagnostic reuse, and strategy changes.
- **Its full cost**: compute, latency, independent revalidation, maintenance, and incident handling.

Targeted human checks should examine suspicious acceptances and persistent failures. An infrastructure failure must be distinguished from a genuinely incorrect solution.

## The race for oracles starts with their qualification

Coverage figures remain useful for exploring an architecture. They become insufficient when deciding what it can deliver.

The system needs to know how much a proposal costs, which tasks it recovers, and how much confidence its verdict deserves. Together, these three facts determine model order and the number of attempts.

The next frontier therefore involves more than asking an agent to try again. It involves building verification strong enough for retrying to remain a good decision.

{{< closing-question label="Key takeaway" >}}
More attempts can make intelligence cheaper. **Oracle reliability determines how many attempts we can afford.**
{{< /closing-question >}}

---

## Sources

- Datacurve, [DeepSWE v1.1: detailed task and rollout data](https://deepswe.datacurve.ai/data/v1.1), accessed October 6, 2026.
- Epoch AI, [*DeepSWE v1.1 — Benchmark review*](https://epoch.ai/benchmarks/deepswe/review), September 7, 2026.
- Huang et al., [*DeepSWE: Measuring frontier coding agents on original, long-horizon engineering tasks*](https://deepswe.datacurve.ai/blog/deepswe), Datacurve, May 26, 2026.
- Datacurve, [*DeepSWE v1 — critiques.json*](https://deepswe.datacurve.ai/artifacts/v1/critiques.json), results and definitions of false-positive and false-negative proportions.
- METR, [*Recent Frontier Models Are Reward Hacking*](https://metr.org/blog/2025-06-05-recent-reward-hacking/), June 5, 2025.
- Barr et al., [*The Oracle Problem in Software Testing: A Survey*](https://doi.org/10.1109/TSE.2014.2372785), *IEEE Transactions on Software Engineering*, 2015.
