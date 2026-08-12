---
title: "An Agent Without a Harness Is Not a Production System"
slug: "un-agent-sans-harnais"
date: 2026-09-01
description: "A successful demonstration is not enough: an agent becomes a production system when a harness makes its errors visible and its checks repeatable."
categories: ["Artificial Intelligence", "Software Engineering"]
series: ["aucun-harnais-n-est-parfait"]
series_order: 1
collection: "ARCHITECTURE"
cover: "/images/articles/01-un-agent-sans-harness.en.png"
draft: false
---

A successful demonstration proves almost nothing about an agent's ability to deliver.

It proves that the agent succeeded once, under the watch of someone who knew what they wanted to achieve. In production, it has to succeed again tomorrow on a slightly different case, without breaking what worked yesterday or silently bypassing a constraint.

That is where the harness begins.

## The Model Is Only an Engine

When we watch an agent work, what we mainly see is the model. It receives a request, explores files, writes code, runs a few commands, and announces that the work is complete. This part is spectacular because it looks like human activity compressed into a short span of time.

But a team does not put a developer into production simply because they can write quickly. It relies on an architecture, conventions, tests, security controls, review, and a shared definition of what can be shipped. The agent needs that same environment, made executable.

This is what the industry increasingly calls a harness. [Thoughtworks](https://martinfowler.com/articles/harness-engineering.html) describes it as a combination of guides that direct the agent and sensors that observe what it produces. The former tell it how to work. The latter confront it with reality: compilation, static analysis, tests, security policies, architectural boundaries, and quality criteria.

The harness does not make the model more intelligent. It makes its errors visible early enough to reduce their cost.

## A Loop, Not a List of Rules

A development guide stored in a wiki does not constitute a harness. Neither does a checklist that users have to remember to apply.

The system becomes valuable when the checks take part in the production loop. The agent attempts a change. The system runs the checks. A type error, a regression, or a prohibited dependency triggers a rejection. The agent receives that signal, makes a correction, and tries again.

The difference may seem slight. It is decisive.

In the first case, quality depends on each user's memory and discipline. In the second, some of that discipline becomes a property of the environment. The same rules apply to the first attempt and the fiftieth, at ten in the morning and in the middle of the night.

The accounts published by [OpenAI](https://openai.com/index/harness-engineering/) and [Stripe](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents) in 2026 give a sense of this shift in scale. Volumes of code or pull requests naturally attract attention. Yet the important point lies beneath the numbers: these organizations did not simply connect a better model to their repositories. They built a production line around it.

## What the Harness Really Automates

The harness automates the execution of checks. It does not decide on its own what deserves to be checked.

Someone has to choose the architectural invariants. Someone has to decide which behaviors constitute a regression, which data must never appear in a log, and what level of performance is acceptable. Someone also has to recognize when a technically valid result does not meet the need.

In other words, the harness does not eliminate the cost of validation. It shifts it.

Instead of manually reviewing every output, the team invests in reusable checks. That cost can be shared and the checks can be improved over time. They become a production asset rather than a chore repeated for every delivery.

This shift also changes the engineer's role. The job is no longer simply to produce the artifact. It is to build the environment that makes rapid production compatible with an explicit level of confidence.

## The Harness Is a Tool, Not an Excuse

A green light assumes no responsibility.

The operator remains responsible for what emerges from the loop because they are responsible for the very definition of that green light. They choose the checks, accept their limitations, and decide when the result can be used.

This distinction guards against a common misunderstanding. Industrializing validation does not mean delegating judgment. It means giving human judgment enough reach to keep pace with the new rate of production.

Without a harness, an agent remains an impressive generator whose every output must be handled as an isolated case. With a harness, it becomes part of a production system.

But that system has a less visible weakness: it mainly checks for deviations its designers thought to teach it about.

That is the subject of the next article.

---

## Sources

- Thoughtworks / Martin Fowler, Birgitta Böckeler, *Harness engineering for coding agent users* (April 2, 2026) · https://martinfowler.com/articles/harness-engineering.html
- OpenAI, Ryan Lopopolo, *Harness engineering: leveraging Codex in an agent-first world* (February 11, 2026) · https://openai.com/index/harness-engineering/
- Stripe, Alistair Gray, *Minions: Stripe's one-shot, end-to-end coding agents* (February 9, 2026) · https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents
- DORA / Google Cloud, *State of AI-assisted Software Development 2025*, AI as an amplifier of existing strengths and weaknesses · https://dora.dev/research/2025/dora-report/
