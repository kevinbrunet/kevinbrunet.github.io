---
title: "No Harness Is Magic"
slug: "aucun-harnais-n-est-magique"
date: 2026-09-01
description: "No harness covers every risk: robustness comes from governance capable of organizing multiple lines of defense."
categories: ["Artificial intelligence", "Software engineering"]
tags: ["ai-systems-harness-engineering", "ai-risk-governance"]
series: ["aucun-harnais-n-est-parfait"]
series_order: 8
collection: "ARCHITECTURE"
cover: "/images/articles/08-aucun-harnais-n-est-magique.en.png"
draft: false
---

Choosing a single harness for the entire company can simplify governance and create systemic risk.

The contradiction is only apparent.

An organization has good reasons to standardize: auditing, support, costs, skills, traceability, and security. When every team is free to assemble its own models, tools, and controls, the landscape quickly becomes impossible to read.

But standardizing every component of the harness does more than create order. It also embeds the same blind spots everywhere.

## Monoculture Is Efficient Until It Isn't

Agricultural monoculture makes work easier, improves yields, and simplifies treatment. It becomes fragile when a pest can exploit the precise characteristics shared by every plant.

A homogeneous population of agents follows the same logic.

The same model misinterprets a category of requests. The same reviewer misses the error. The same tests were generated from the same interpretation. The same validation policy declares the results acceptable. The incident no longer affects a single isolated user. It can spread across the entire organization without producing any internal disagreement.

Diversity is therefore more than a freedom granted to teams. It can provide a defense against correlated failures.

## Standardize the Chassis, Not Every Perspective

Two levels must be distinguished.

The harness chassis can be shared. The company can prescribe how a system is installed, declares its models, logs its actions, protects its secrets, separates production from qualification, measures its costs, and reports its incidents.

This chassis makes diversity governable. It provides a common interface for auditing without imposing a single configuration.

Within it, several elements can vary: producer model, reviewer model, prompts, deterministic tools, qualification datasets, security configuration, and domain references. This plurality has value only if it actually produces fewer correlated errors. It must therefore be measured, not celebrated on principle.

The goal is not "everyone does whatever they want." The goal is "multiple systems can demonstrate how they work and what they contribute that is different."

## Diversity as a Risk Policy

A mature policy does not ask which model is best in general. It asks which combinations reduce risk for a class of tasks.

For routine code, a fast producer combined with deterministic tests and occasional reviewer sampling may be enough. Transforming sensitive data may require a second model, an isolated environment, and an independent qualification dataset. For a decision that affects others, an individual harness may never constitute sufficient evidence.

Diversity becomes a portfolio of controls.

As in finance, we do not diversify because every asset is superior. We diversify because imperfectly correlated risks prevent a single event from taking down the whole portfolio.

This logic also assigns a clear responsibility to the operator. The harness is a tool, not an alibi. Its operator must understand the regime in which it can be used, the controls it runs, and the limits that have been observed. When an individual tool is promoted to the team or company level, its maintenance and accountability must scale with it.

## Map the Blind Spots

A company will not discover its blind spots by decree. It will find them in disagreements, incidents, human rework, and gaps between stated confidence and actual results.

This suggests a new governance function.

Someone must observe the population of harnesses rather than a single pipeline. Which systems let the same defects through? Where does one model correct another? Which controls no longer produce a useful signal? Which incident reveals a weakness shared by multiple teams?

This person is not merely trying to clear a backlog of problems. They are looking for the shared causes that produce them. They act like an epidemiologist: an isolated case matters less for its volume than for what it reveals about the population.

Diversity without this observation remains noise. With it, local errors become material for collective learning.

## A Falsifiable Thesis

The idea can and should be tested.

For the same class of tasks, two comparable groups can use either a homogeneous harness or several governed but genuinely different systems. The organization can then measure defects detected before production, incidents after production, disagreements that led to useful corrections, the total cost of validation, and resolution time.

If diversity does not improve detection or costs more than the protection it provides, the policy must be reconsidered. If it produces only stylistic differences, it is not a defense. If it reveals classes of errors invisible to the dominant system, it becomes a security asset.

This requirement for measurement protects the thesis from its own rhetoric. "Diversity is resilient" must not become another slogan that cannot be challenged.

## No Harness Is Perfect. That Is an Architectural Property.

A harness industrializes validation. It eliminates errors, enforces invariants, and enables agentic production to scale.

Yet it verifies what it has been taught to verify. It can review with the same blind spots, optimize the measure instead of the mission, and produce artificial consensus among correlated agents.

The right answer is neither the absence of a harness nor the search for a magic harness.

It is to protect controls, anchor qualification in external references, preserve the independence of evaluators, learn from disagreements, and maintain multiple perspectives within a governable chassis.

We have long treated uniformity as a prerequisite for control. With agents, it can also become the quietest way to share the same error.

---

## Sources

- Condorcet's jury theorem, independence of errors condition
- 2025-2026 literature on the limits of multi-agent voting and debate: synthesis in *The Deliberative Illusion* and *When Does Delegation Beat Majority?*: https://arxiv.org/pdf/2606.03032; https://arxiv.org/pdf/2606.08098
- Monoculture/diversification analogy: a conceptual analogy, not empirical evidence specific to harnesses
- Prediction that organizations with diverse harnesses detect more anomalies: a falsifiable hypothesis proposed by the BYOAI manuscript, not yet demonstrated
