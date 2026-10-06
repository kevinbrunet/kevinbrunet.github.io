---
title: "Blind Decorrelation"
slug: "decorreler-a-l-aveugle"
date: 2026-09-01
description: "Independent evaluation requires preserving disagreements before allowing agents to interact or seeking consensus."
categories: ["Artificial intelligence", "Software engineering"]
tags: ["ai-evaluation-evals", "ai-reliability"]
series: ["aucun-harnais-n-est-parfait"]
series_order: 7
collection: "ARCHITECTURE"
cover: "/images/articles/07-decorreler-a-l-aveugle.en.png"
draft: false
---

To obtain two independent opinions, do not begin by having the two evaluators discuss the issue.

This conclusion runs counter to the seductive image of multi-agent debate. We picture several models exchanging arguments, correcting one another, then converging on a better answer.

The exchange can help. It can also destroy the very property we were seeking: independence of judgment.

## Disagreement needs time to exist

Suppose two different models examine a sensitive change. The first concludes that it is safe. The second detects a risk.

If the second immediately sees the first model's conclusion, its analysis no longer begins from the same point. It may seek to confirm the opinion already expressed, adopt a compelling line of reasoning, or focus its attention on the elements selected by the other model.

The first opinion becomes an anchor.

Conversely, if the two models work separately, each must construct its own representation of the problem. The final comparison preserves more information. Agreement is more valuable because it was not negotiated. Disagreement is even more valuable, since it reveals an area where at least one understanding is inadequate.

Blind decorrelation therefore means producing judgments separately, without access to the other model's conclusion or reasoning, and then comparing the verdicts.

## Disagreement is not an error to eliminate

In many workflows, disagreement immediately triggers an arbiter tasked with choosing the right answer. This step may be necessary. It must not erase the signal.

Disagreement is an observation about the validation system itself. It indicates that the case lies near a boundary between two representations. Even if verification clearly establishes that one model is right, the discrepancy should be logged.

Over time, these discrepancies form an empirical map:

- which categories of requests divide evaluators
- which model regularly misses which type of defect
- which disagreements foreshadow a real incident
- which divergences remain purely stylistic
- which cases should now require human assessment

This map cannot be drawn entirely in advance. Knowing every blind spot before beginning would mean having none in the first place.

## A minimal architecture

A decorrelated loop can remain simple.

The producer generates an artifact. Two evaluators receive that artifact and the assessment criteria separately. They return a structured verdict: accepted, rejected, or uncertain, together with the properties that support their decision.

A deterministic mechanism then compares the results.

If both evaluations are favorable, the workflow continues according to the level of risk. If both are unfavorable, the output is sent back for correction. If they disagree, the system routes the case to human review, an additional test, or a third evaluator.

The "leader" does not need to be an agent presumed to be wiser. It can be a routing function with no opinion of its own. Its role is not to produce the truth. It is to recognize the configuration that requires more information.

This idea echoes several older architectures. Mixture of experts systems use a gating function to choose which expert to engage. Boosting readjusts classifier weights based on observed errors. Fault-tolerant systems seek to prevent a single source of failure from contaminating the entire decision.

The vocabulary changes. The principle remains: robustness comes not only from the number of components, but from the structure of their dependencies.

## Not all differences are equal

Using two model brands does not guarantee sufficient decorrelation. For a given task, several dimensions must be examined:

- model family and training data
- the evaluator's prompt and role
- available tools
- references used for judgment
- visibility into tests and production
- the team that maintains the criteria
- type of control, whether probabilistic or deterministic

A static analyzer sometimes provides more independence than a second large model. An independent business example can provide more value than a lengthy debate. A hidden test can expose a blind spot that three conversational reviewers had reinforced together.

The right combination therefore depends on the risk class, not on a dogma of "always use two models."

## Start by sampling

Running multiple evaluators on every output can be expensive. An organization can begin with sampling: a percentage of cases receives a second independent review, with higher sampling rates for risky or poorly understood domains.

Disagreements are preserved, examined, and linked to actual outcomes. If one category accounts for a concentration of useful divergences, the second check becomes systematic for that category. If an evaluator produces no new information, it is replaced.

The harness thus learns where to buy diversity.

Blind decorrelation is not a ceremony in which two models vote. It is a design discipline: protect independence before comparison, treat disagreement as data, and adapt the cost of validation to what experience reveals.

This discipline leads to the conclusion of the series. Since no system sees everything, diversity must be organized at the enterprise level without creating chaos that is impossible to govern.
That is what we will explore next week.

---

## Sources

- *The Deliberative Illusion*, April/June 2026 depending on the version, on majority conformity and homogenization in multi-agent debate: https://arxiv.org/pdf/2606.03032
- Jacobs, Jordan, Nowlan, and Hinton, *Adaptive Mixtures of Local Experts* (1991), gating function
- Freund and Schapire, AdaBoost (1997), aggregation weighted by observed error
- Lamport, Shostak, and Pease, *The Byzantine Generals Problem* (1982), robustness against distributed failures
- The specific architecture proposed here, particularly disagreement logging and routing: a proposal to be tested empirically
