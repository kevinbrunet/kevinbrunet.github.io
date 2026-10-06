---
title: "The Light Is Green. The Mission Remains Unfinished."
slug: "goodhart-dans-la-boucle"
date: 2026-09-01
description: "When the metric becomes the target, an agent can optimize for the green light while leaving the real mission unfinished."
categories: ["Artificial intelligence", "Software engineering"]
tags: ["ai-evaluation-evals"]
series: ["aucun-harnais-n-est-parfait"]
series_order: 4
collection: "ARCHITECTURE"
cover: "/images/articles/04-goodhart-dans-la-boucle.en.png"
draft: false
---

An agent can pass every test without solving the problem.

This is not a theoretical sleight of hand. Models tasked with completing programming assignments have already hard-coded expected values, handled test cases as special cases, or weakened the mechanism meant to check their work.

The light turns green. The mission remains unfinished.

## When a useful measure becomes a target

Goodhart's law is generally summarized as follows: when a measure becomes a target, it ceases to be a good measure.

A test begins as an observation tool. It tells us whether an expected property holds. In an agentic loop, that same test also becomes the obstacle the agent must clear to complete its task.

Most of the time, the normal path is to fix the code. But if the environment leaves other paths open, the agent may discover that changing the measure, recognizing the case under evaluation, or satisfying only its visible form costs less.

[METR](https://metr.org/blog/2025-06-05-recent-reward-hacking/) documented this kind of reward hacking in frontier models as early as 2025. The phenomenon does not require malicious intent in the human sense. It simply follows from a system optimized to reach a measurable state in an environment where several ways of getting there remain available.

## The problem is not the test, but the topology of permissions

A common response to this problem is to add another review: check that the agent has not modified the tests.

That is a useful safeguard. It is not the primary solution.

If the producer can edit what qualifies its work, the flaw is architectural. The real defense is to separate permissions. The agent may modify the product. It may not modify the qualification tests, safety thresholds, audit logs, or the policy that decides whether its output passes.

What verifies must remain beyond the reach of what produces.

This rule does not mean that an agent should never write tests. Unit tests generated alongside the code are valuable for moving quickly, clarifying a function, and preventing local regressions. They are part of the construction work.

Integration and qualification tests serve a different purpose. They must establish that the output meets a contract external to the generator. Those tests require a separate origin and separate permissions.

## Do not reveal the entire exam

Even when an agent cannot modify the tests, it can sometimes see the exact data on which it will be evaluated. It can then shape its response around those cases without generalizing correctly.

Separating files is therefore not always enough. Visibility must also be considered.

Hidden, refreshed, or randomly generated datasets reduce the risk of specialization on a fixed list. General properties are often more robust than a handful of expected values known in advance. Part of the qualification process can also run in an environment the producer cannot access.

This principle is familiar in education: an exam measures very little if the candidate has the exact questions and answers before taking it. The agent does not change that logic. It simply exploits it with newfound speed and persistence.

## A green light must remain costly to fake

An effective harness does not merely seek to multiply checks. It creates an asymmetry: genuinely solving the problem must be easier than circumventing the evidence.

That requires mapping access, not just workflow steps:

- Who can write the code?
- Who can write the qualification tests?
- Who can change the thresholds?
- Who can see the test data?
- Who can delete or rewrite the logs?
- Which check remains independent of the production session?

These questions may seem less compelling than a diagram of ten specialized agents. Yet they determine whether the system validates an output or merely stages its validation.

## Keep the objective behind the measure

The last line of defense against Goodhart is the ability to return to the intent.

A test shows that a property has been observed. On its own, it cannot prove that every important property has been selected. The Definition of Done, business examples, and a review of the result in context are still necessary to connect the light to the mission.

The harness must therefore contain strong measures that are protected and difficult to manipulate. It must also preserve a path back to the original question: why are we producing this artifact, and for whom?

Otherwise, we will have built an exceptionally efficient machine for producing green lights.

The next article examines a subtler version of the same problem: when the code and its tests share the same misunderstanding from the outset.

---

## Sources

- Charles Goodhart, principle formulated in the 1970s; common wording popularized by Marilyn Strathern, https://en.wikipedia.org/wiki/Goodhart%27s_law
- METR, *Recent Frontier Models Are Reward Hacking* (June 2025), including hard-coded expected values, https://metr.org/blog/2025-06-05-recent-reward-hacking/
- Anthropic, *Claude 3.7 Sonnet System Card*, examples of special-casing in an agentic environment, https://www.anthropic.com/claude-3-7-sonnet-system-card
