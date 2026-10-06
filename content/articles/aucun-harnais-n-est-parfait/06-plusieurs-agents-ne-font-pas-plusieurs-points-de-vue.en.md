---
title: "Why Adding Agents Does Not Necessarily Create Diversity"
slug: "plusieurs-agents-points-de-vue"
date: 2026-09-01
description: "Multiplying agents does not automatically create diversity when their models, contexts, and criteria remain correlated."
categories: ["Artificial intelligence", "Software engineering"]
tags: ["ai-reliability"]
series: ["aucun-harnais-n-est-parfait"]
series_order: 6
collection: "ARCHITECTURE"
cover: "/images/articles/06-plusieurs-agents-ne-font-pas-plusieurs-points-de-vue.en.png"
draft: false
---

Ten agents built on the same model can produce ten answers and share a single blind spot.

Multi-agent interfaces readily create the opposite impression. One agent proposes, another critiques, and a third arbitrates. Each has a name, a role, and sometimes a personality. The diagram looks like a team.

But diversity on an organizational chart does not guarantee diversity of errors.

## Drawing More Times from the Same Deck

Running several instances of a model introduces variance. The wording changes, the trajectories differ, and some careless mistakes disappear. For problems where each attempt has an independent probability of finding the right answer, aggregation can be highly effective.

The problem arises when the errors are not independent.

Agents based on the same model share their training, representations, and some of their biases. If a class of problems falls within a common blind spot, majority voting will not correct it. It may even turn the error into consensus.

Condorcet's jury theorem is often invoked to justify the wisdom of crowds. Its essential condition is easily forgotten: voters must be better than chance, and their judgments must be sufficiently independent. A hundred copies of the same judge do not constitute a crowd in the sense that makes the theorem useful.

## Consensus Can Conceal a Lack of Information

An answer repeated ten times seems more reliable than an isolated answer. Yet if all ten answers stem from the same source of error, their number provides almost no additional information.

This is the same problem as a common-mode failure in a redundant system. Three identical servers do not protect against a software defect present on all three. They mainly protect against independent hardware failures.

Recent research on multi-agent debate documents this limitation. Majority voting can fail when models share the same biases or when the correct answer remains in the minority. Exchanges can also produce sycophancy: agents gradually fall in line with a dominant position, even when it is wrong.

The debate then creates an illusion of deliberation. It homogenizes positions more than it produces information.

## Roles Are Still Useful, but for a Different Reason

This does not mean that specialized agents are useless.

Assigning a "security" role can enforce a dedicated pass over permissions, secrets, and untrusted inputs. An "architecture" role can examine dependencies and module boundaries. These perspectives increase coverage of known checks.

They simply should not be confused with independent sources.

A system can therefore combine two mechanisms:

- specialized homogeneous agents that systematically apply several analytical lenses;
- genuinely heterogeneous evaluators tasked with finding correlated errors.

The first improve discipline. The second improve the capacity for surprise.

## Measure Diversity Through Useful Disagreements

Counting agents is a poor measure of diversity. Counting models is not always enough either. Two distinct models may have been trained on similar corpora, use similar methods, and converge on the same conventions.

A more practical measure is to observe disagreements.

Across which categories of cases do two evaluators diverge? Do their disagreements reveal genuine errors after review? Does a new evaluator detect defects that the existing system allowed through? Does its cost bring new information, or merely a rephrasing?

Diversity then becomes an empirical property of the system, not an architectural label.

This approach also provides a way to stop a homogeneous loop. When successive outputs converge strongly and no external signal appears, another round is unlikely to offer a new point of view. It becomes more rational to change the reference, tool, or model.

## The Right Question to Ask Before Adding an Agent

Before creating a new role in the workflow, ask:

> What error can this new agent see that the others have structural reasons to miss?

If the answer concerns only an overlooked instruction, a specialized role may be enough. If it concerns a shared bias, a deeper difference must be introduced.

The next article addresses precisely this architecture. It does not consist in making agents debate for longer. It consists in preserving their independence until the moment their verdicts are compared.

---

## Sources

- Condorcet's jury theorem, with independence of errors as a central condition
- *Multi-Agent Debate for LLM Judges*, NeurIPS 2025, https://arxiv.org/pdf/2510.12697
- *The Deliberative Illusion*, on factual attrition and the homogenization of positions in multi-agent debate, https://arxiv.org/pdf/2606.03032
- *When Does Delegation Beat Majority?*, on the limits of majority voting according to error structure, https://arxiv.org/pdf/2606.08098
- Measuring diversity through useful disagreements: an operational proposal from the BYOAI manuscript
