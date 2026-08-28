---
title: "Two Agents. The Same Blind Spot."
slug: "juge-et-partie-agents"
date: 2026-09-01
description: "Having an agent's work reviewed by a copy of the same system multiplies opinions without necessarily reducing their shared blind spots."
categories: ["Artificial Intelligence", "Software Engineering"]
series: ["aucun-harnais-n-est-parfait"]
series_order: 3
collection: "ARCHITECTURE"
cover: "/images/articles/03-juge-et-partie.en.png"
draft: false
---

Asking an agent to review its own work provides a fresh look. It does not provide a different perspective.

The distinction may seem semantic. Yet it determines the robustness of many multi-agent architectures.

The scenario has become common. A first agent produces an answer or a code change. A second is assigned the role of reviewer. It must look for errors, challenge decisions, and suggest corrections. In the diagram, two agents face each other. It is easy to conclude that two perspectives have been brought to bear.

That is not necessarily the case.

## A Different Role Does Not Create Another Brain

If both agents use the same model, they share what matters most: training data, representations, reasoning patterns, and categories of errors.

The review prompt introduces a real difference. It changes the immediate objective and directs attention toward certain flaws. It is like returning to your own work after a few weeks. You notice awkward choices to which you had become blind. You check details that the momentum of writing had obscured.

But you also return with the same underlying convictions. A misinterpretation caused by understanding the problem in a certain way remains difficult to see, because you are still reviewing it from that same understanding.

A new role improves attention. It does not guarantee independence.

## What Self-Correction Without an External Signal Tells Us

Research on the intrinsic self-correction of large models offers a less reassuring result than the usual demonstrations. In their study presented at ICLR 2024, [Huang and coauthors](https://arxiv.org/abs/2310.01798) show that asking a model to correct its reasoning without providing external feedback does not consistently improve the result and can make it worse.

The important word is "external."

A failing test provides new information. A runtime error provides new information. A domain example that contradicts the result provides new information. A simple instruction such as "check again" asks the model to resample what it already knows.

It may find an oversight. It receives no additional means of recognizing as false what it already considers correct.

## The Loop Eliminates the Easy-to-Spot Errors First

This does not mean that critique loops are useless. They can correct many flaws at first: omissions, local inconsistencies, missing imports, straightforward edge cases, or visible contradictions.

Returns then diminish.

Each additional round explores the same distribution with variations in wording and attention. The first passes remove the errors the model knows how to recognize. As the output stabilizes, a greater share of the remaining errors stems from its blind spots. The loop then begins to polish a solution rather than enrich it.

There is no universal number of rounds that marks this plateau. It depends on the model, the task, and the available checks. It can nevertheless be observed: corrections become minor, verdicts converge, and no new facts enter the system.

At that point, requesting an eleventh review mostly buys confidence.

## The Reviewer Must Provide a Verifiable Difference

Before adding a review agent, we should therefore ask what it adds.

Does it bring a different model? A specification that only it can see? Tests beyond the producer's reach? An independent dataset? A deterministic tool? Expertise or instructions developed by another team?

If the answer is no, the reviewer can still be useful as a consistency check. It simply should not be presented as an independent source of truth.

This distinction also helps avoid the decorative multiplication of agents. A "security" agent, an "architecture" agent, and a "quality" agent do not constitute three lines of defense if they all apply the same knowledge with the same access to the same output. They are three lenses within a single system.

That is not nothing. It is not three brains.

## Seek a Signal, Not Approval

The best use of a second review is not always to obtain a final verdict. It may be to produce disagreement.

If two genuinely different evaluators independently reach incompatible conclusions, we do not yet know which one is right. We do, however, know where to focus human review. Disagreement becomes a detector of fragile areas.

This idea reverses the usual instinct. We no longer ask the second agent to reassure the first by signing off on its work. We ask it to reveal where relying on a single source of confidence would be dangerous.

An agent can therefore review its own work. We simply need to understand what that review proves: better internal consistency, sometimes a useful correction, but never, on its own, the absence of a blind spot.

In the next article, the loop encounters another problem. As soon as it is given a clear metric to optimize, the agent can pass the check without accomplishing the mission.

---

## Sources

- Huang et al., *Large Language Models Cannot Self-Correct Reasoning Yet*, ICLR 2024 · https://arxiv.org/abs/2310.01798
- Kamoi et al., *When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-Correction of LLMs*, TACL 2024 · https://aclanthology.org/2024.tacl-1.78/
- Tyen et al., *LLMs Cannot Find Reasoning Errors, but Can Correct Them Given the Error Location*, Findings of ACL 2024 · https://aclanthology.org/2024.findings-acl.826/
- Zhu et al., *Demystifying Multi-Agent Debate: The Role of Confidence and Diversity*, Findings of ACL 2026 · https://aclanthology.org/2026.findings-acl.1694/
