---
title: "Qualifying Model Routing"
seo_title: "AI agents: a method to qualify model routing and the oracle"
slug: "qualify-oracle-driven-routing"
date: 2026-10-27
description: "From complement selection to canary deployment: separate selection from testing, measure small residuals, and check the oracle against an independent reference."
categories: ["Artificial intelligence", "Software architecture", "Software engineering"]
tags: ["ai-evaluation-evals", "ai-reliability"]
series: ["l-oracle"]
series_order: 4
collection: "SYSTÈMES"
cover: "/images/articles/qualifier-routage-oracle.en.png"
draft: false
---

{{< callout variant="scene" label="The choice holds. The evidence still needs building." >}}
GLM Flash recovers ten of Luna's eleven observed failures. But we selected this complement by looking at those very failures.

I therefore repeated the selection, holding out each task in turn, then each repository. **GLM Flash remains selected. Recovery remains ten out of eleven.**

This check strengthens one specific conclusion: the economic choice does not depend on a single task or repository. It does not turn those eleven cases into evidence of production reliability.
{{< /callout >}}

The first three episodes explored [verified attempts](/en/articles/oracle-real-game-changer-agentic-ai/), [model complementarity](/en/articles/most-expensive-model-better-left-last/) and [oracle qualification](/en/articles/who-checks-oracle/).

Here is how to move from a promising architecture to a deployment decision. The protocol must produce two distinct results: a routing policy selected using development data, then a measurement of that policy on held-out cases, with independent verification of its verdicts.

## 1. Write down the decision before looking for a winner

“Find the best complement” does not define an experiment. Should it recover the most tasks, minimize the bill, meet a deadline or limit delivered errors? These objectives can produce different model orders.

A team might, for example, seek the lowest full cost among chains that meet a minimum coverage, a maximum latency and a ceiling on accepted errors. These thresholds come from business requirements. They must be fixed before testing, together with the rule for breaking ties between configurations.

The policy includes the first model, candidate complements, their order, the maximum number of attempts, shared diagnostics and conditions for human escalation. Cost includes oracle execution, revalidation and operations, not just tokens.

Comparing many configurations and reporting the winner's score on the same cases favors the one that benefited from the chance composition of that sample. This selection bias, often called the *winner's curse*, is documented notably by [Cawley and Talbot](https://www.jmlr.org/papers/v11/cawley10a.html).

**The selection rule must be executable without consulting the results of held-out cases.**

## 2. Build a dataset that also represents cases missing from the logs

Production traces provide an excellent starting point: request, context available at that moment, proposals, verdicts, human corrections, costs, durations and reasons for escalation.

They nevertheless inherit the system that produced them. If the old routing never sent certain cases to the agent, their trajectories are missing. If it sent difficult requests straight to a human, automatic outcomes mainly describe easy cases. The absence of a recorded incident can also reflect a lack of follow-up.

Sample at the entry point, before the routing decision, and include requests that were rejected, abandoned or handled by a person. A final human answer must not automatically become the label of an earlier proposal: that proposal needs to be examined in its own context.

Frequent cases retain their real weight. A separate stress set can overrepresent incidents and critical tasks. If these populations are mixed, retaining sampling probabilities enables weighted results; the enriched set's raw rate does not represent traffic.

## 3. Separate groups, time and uses of the data

A nearly identical ticket in both selection data and the test can make generalization artificially easy. Define relevant groups — customer, repository, template, request family — before splitting, then prevent overlap when the objective is generalization to new groups. The [scikit-learn documentation](https://scikit-learn.org/stable/modules/cross_validation.html) describes group and temporal splitting.

To measure future behavior, hold out a more recent period. If the objective also concerns new customers or repositories, combine both constraints. For future traffic from existing customers, state that scope explicitly rather than claiming to measure new customers.

Keep three uses distinct:

| Dataset | Permitted use |
|---|---|
| Development | Explore models, prompts and escalation rules |
| Validation | Choose order, attempt budget and thresholds |
| Held-out test | Evaluate the frozen policy once |

With little data, internal cross-validation can replace the validation set. It does not remove the need for evaluation outside selection.

**A test consulted to swap two models or add an attempt becomes development data.** After a change decided from its results, a new untouched test is needed. “Once” means a campaign planned in advance, which may include multiple executions per case, without adapting the policy between them.

## 4. Size the residual, not just the benchmark

If the first model covers about 90% of cases, a 200-task test leaves only about twenty observations for evaluating the complement. Its overall score can look stable while recovery depends on a handful of cases.

On ten independent cases, nine recoveries give 90%, but a 95% Wilson interval of approximately **60–98%**. For ten out of eleven, the interval is approximately **62–98%**. These calculations use the method presented by [NIST](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm).

False-positive qualification requires another denominator. The previous episode's `β` is the probability of accepting a proposal **given that it is incorrect**. Estimating it requires proposals independently established to be incorrect, then observing the oracle's verdict.

With zero false acceptances among `n` independent, representative incorrect proposals, the one-sided 95% binomial upper bound is:

```text
β_upper = 1 − 0.05^(1/n)
        ≈ 3 / n
```

Aiming for a 0.5% bound therefore requires about **600 incorrect proposals**, with no observed false acceptance. These are neither 600 tasks nor 600 accepted proposals. With correlated errors or a population different from actual escalations, this calculation is insufficient to qualify risk.

The sampling plan must anticipate volumes at each stage. If escalation receives too few cases, the honest conclusion is “insufficient precision.”

## 5. Give the oracle an independent reference

Holding out tasks protects against part of the selection bias. It does not protect against an oracle sharing the same blind spot across selection and test data.

If all configurations are selected and evaluated by this check, the one maximizing acceptances might perform the work best, but its proposals might also exploit the check's gaps best. The test then measures agreement with the check. The [oracle problem in software testing](https://doi.org/10.1109/TSE.2014.2372785) makes this distinction central.

Plan a sample examined against an independent business rubric by qualified people, hiding the initial verdict and model identity where possible. A second check helps locate disagreements; sharing the same tests or assumptions does not make it independent by default.

The sample must include a random portion of acceptances and rejections, supplemented by more late acceptances at attempts three and four, disagreements between checks and persistent escalations. Targeted cases help discover defects; estimating the overall rate requires appropriate weighting and population coverage.

Document actual recovery, errors among delivered answers, false negatives and false acceptances among incorrect proposals separately. Each measure has its own denominator. Held-out proposals and their independent labels must not be used to repair the oracle during the final campaign.

{{< pullquote >}}
A held-out task can check complement selection. Only an independent reference can check whether the verdict is correct.
{{< /pullquote >}}

## 6. Repeat executions without artificially multiplying the evidence

An agent can succeed once and fail the next time. Plan multiple executions on held-out cases, with the same budget across policies and a frozen stopping rule. If attempts share diagnostics, reproduce that actual loop: DeepSWE's independent rollouts do not simulate it.

Measure correct coverage, conditional recovery on first-stage failures, full cost, the latency distribution and delivered errors. Compare policies on the same cases.

Repeated executions of one task do not become independent tasks. Estimate uncertainty while preserving this structure, for example by resampling repositories or case families, then executions within those groups where the data supports it. A small residual remains small even after many rollouts.

## What we actually tested on DeepSWE

To check complement selection, I fixed Luna `[max]` first and reused the 66 configurations with complete costs from episode two's chart. The rule minimizes **estimated cost per recovered failure** on the training residual, stopping at the first positive verdict and using up to four published attempts.

For each task, the complement is selected on the other 112. The entire procedure is then repeated while holding out a whole repository.

| Check | GLM-5.3 Flash selected | Held-out Luna failures recovered |
|---|---:|---:|
| One task held out | 113 selections out of 113 | 10 out of 11 |
| One repository held out | 91 selections out of 91 | 10 out of 11 |

The 102 tasks already accepted with Luna do not invoke the complement. Recovery evaluations therefore concern **eleven tasks across ten repositories**, rather than 113 recovery observations.

On the complete residual, GLM costs approximately $0.479 per recovered task, versus $0.792 for the runner-up, DeepSeek V4 Flash `[max]`. In the fold with the closest competition, GLM remains at approximately $0.495 versus $0.672. Its economic advantage does not disappear when a task is removed.

The [detailed calculation report](/downloads/l-oracle/complement-selection.json) retains each selection, exclusions and pricing conventions. Results by [task](/downloads/l-oracle/leave-one-task-out.csv) and [repository](/downloads/l-oracle/leave-one-repository-out.csv) are also available.

**This is a retrospective stability check.** Luna, the candidates and the objective were defined after exploring the data; candidate eligibility uses cost availability on the complete residual. The check validates neither grader correctness, the reverse routing order nor the third stage. The Wilson interval above illustrates the small residual; it is not a calibrated future-performance interval for this selection and these dependent tasks.

## After testing: shadow mode, then a canary

In shadow mode, the candidate policy handles a representative fraction of traffic without controlling the delivered answer. Actions and their effects remain isolated. Compare proposals, verdicts, cost and latency against the current system, with independent review of sensitive cases.

If the planned criteria are met, a limited canary can then handle a small share of eligible cases. Scope, exposure ceilings, stop thresholds and fallback to the previous system must be operational before launch. A critical case can remain assigned to a human from the outset.

Qualification applies to a version of the model, prompt, harness, tools and oracle within a defined task scope. A change requires requalification appropriate to its impact before expanding delivery. Traffic drift must also trigger renewed evaluation.

{{< callout variant="key" label="The qualification record to retain" >}}
Keep the frozen policy and its versions; case provenance and splits; decision criteria; verdicts and independent labels; results with denominators and uncertainty; and the conditions for shadow mode, canary deployment and rollback.

This record enables another person to understand why the chain was selected and under what conditions its results remain valid.
{{< /callout >}}

{{< closing-question label="Key takeaway" >}}
The benchmark suggests a portfolio. Qualification must establish **what it delivers correctly, on which cases, at what cost and with what uncertainty**.

The protocol begins before choosing the winner and continues after its first deployment.
{{< /closing-question >}}

---

## Sources

- Datacurve, [DeepSWE v1.1: detailed task and rollout data](https://deepswe.datacurve.ai/data/v1.1).
- [DeepSWE complement selection report, by task and repository](/downloads/l-oracle/complement-selection.json).
- Cawley and Talbot, [*On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation*](https://www.jmlr.org/papers/v11/cawley10a.html), JMLR, 2010.
- NIST/SEMATECH, [*Confidence intervals*](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm).
- scikit-learn, [*Cross-validation: evaluating estimator performance*](https://scikit-learn.org/stable/modules/cross_validation.html).
- Barr et al., [*The Oracle Problem in Software Testing: A Survey*](https://doi.org/10.1109/TSE.2014.2372785), IEEE Transactions on Software Engineering, 2015.
