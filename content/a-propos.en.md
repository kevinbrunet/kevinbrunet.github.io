---
title: "About"
layout: "about"
url: "/en/about/"
seo_title: "Software Architect — Agentic AI Systems & AI Reliability"
description: "Software architect with 18 years of experience: agentic AI systems, harnesses, evals and reliability. An approach grounded in business needs and risk."
---

I am **Kévin Brunet, a software architect**, with **18 years of experience in software development and the architecture of business systems**. My background is rooted in complex information systems, production constraints and the teams that keep them running. C# and .NET are part of that engineering foundation.

Today, I work on **agentic AI systems**, with a particular focus on their reliability and deployment to production. The same questions run through this work and my earlier experience: how do we integrate the system into the business, verify what it does, limit its authority and understand its failures?

What interests me is what technology allows us to build, how it addresses a need and what it entails once in production.

## Architecture must work in the real world

Architecture decisions must account for the business, budget, existing systems and organization. They must also remain understandable to the people who build, operate and evolve the system.

My role often involves bringing these constraints to the same table. I look for a solution that is robust enough to last, but no more complex than necessary. The right choice is not always the most elegant on paper. It is the one a team can explain, implement and take responsibility for over time.

I value principles, models and lessons from experience. They provide a foundation for thinking. They do not replace contextual analysis or the need to examine what happens in practice.

## Different business contexts

I have worked in sectors including healthcare, payroll, energy, insurance and retail. These experiences taught me a great deal because their systems carry different risks and face different constraints.

In healthcare, there are patient risks, fine-grained access rights, the requirements of France's Ségur digital health programme and extensive regulation. Payroll involves working across time, managing retroactive changes, calculating backwards and sometimes changing the past without losing its traceability. Energy raises questions of continuity and operational control. Insurance must assess and price a risk before its actual cost is known, a challenge also found in cybersecurity. Retail handles large volumes of data, as healthcare does, but especially demands responsiveness: everything changes quickly, and the right product must be offered at the right price and time.

I encounter many of these challenges again in AI: risk, access rights, regulation, time, traceability, volume and responsiveness. Those experiences give me a practical framework for addressing them.

## Putting AI in the right place

An AI agent does not remain a simple feature for long. As soon as it accesses data, uses tools or acts for a user, it becomes part of the information system.

That raises concrete questions. Who acts? For what purpose? With which permissions? Based on what information? Who reviews the outcome? What evidence do we retain?

I focus on the transition from demonstration to real-world use. This is where identity, delegation, memory, security, observability and human oversight become essential. Without them, we may have a convincing prototype, but not a system an organization can rely on.

## Building the system around the model

**The model is not the system. Reliability is also built into the architecture around it.**

My work and articles explore several complementary domains:

- **[AI Systems & Harness Engineering](/en/topics/ai-systems-harness-engineering/)**: execution loops, tools, context, memory, orchestration and recovery. The harness organizes the model's work and carries the system's controls.
- **[AI Evaluation / Evals](/en/topics/ai-evaluation-evals/) and [AI Reliability](/en/topics/ai-reliability/)**: oracles, reference cases, regression tests and independent evaluations. A passing test should provide useful evidence about expected behaviour.
- **[AI Observability](/en/topics/ai-observability/) and [LLMOps / AgentOps](/en/topics/llmops-agentops/)**: traces, diagnosis, behavioural monitoring, quality, cost and latency. LLMOps addresses the industrialization of LLM applications; AgentOps extends that monitoring to agent trajectories, decisions and tool calls.
- **[Agent Protocols](/en/topics/agent-protocols/)**: MCP, A2A and ACP, to examine the integration of tools, agents and interfaces while keeping their responsibilities clear.
- **[AI Security](/en/topics/ai-security/) and [AI Risk & Governance](/en/topics/ai-risk-governance/)**: authority boundaries, permissions, isolation, guardrails and human oversight. The level of autonomy must remain consistent with the consequences of an error.

I am developing an approach to moving from prototype to production: start with a business goal, analyse the risks, define expected behaviours and their oracles, evaluate representative cases, then observe the system in operation. Expanding its scope should be grounded in what those observations actually support.

This approach connects **Software Architecture, AI Systems Engineering and AI Platform Engineering**. My articles explain mechanisms, experiments and their limitations; they show how I reason about these systems.

## Experience grounded in business systems

Over 18 years, I have developed business systems and contributed to their architecture in healthcare, payroll, energy, insurance and retail. This work has involved access rights, traceability, continuity and evolving business rules, with concrete consequences for users.

That experience has shaped an architectural practice connecting business needs, code and operations. Understanding existing systems, making responsibilities explicit and choosing controls proportionate to risk are part of that practice. My work on agentic AI systems builds on this experience.

My articles provide examples: [“No Harness Is Perfect”](/en/series/aucun-harnais-n-est-parfait/) examines the limits of validation, [the series on agent authority](/en/series/qui-donne-le-droit-d-agir-a-votre-agent-ia/) explores identity and delegation, and [the ACP series](/en/series/acp-interface-manquante-des-agents/) studies the separation between interface, harness and model.

The same questions run through these articles and my projects: **how do we know it works? What happens when it fails? Who can act, within which limits, and what evidence do we retain?**

## Making mechanisms visible

I write to share what I observe and make technical subjects easier to discuss. A fibre cabinet, a video game or a situation experienced on a project can sometimes explain coupling, visibility or responsibility better than a long theoretical discussion.

I do not try to make complexity disappear. I try to distinguish necessary complexity from what we create ourselves, then find the words and diagrams that make it easier to discuss.

Here you will find articles on software architecture, evolving information systems, AI agents, security and team organization. They are intended both for the people who build these systems and for those who make decisions about them.

The common thread is simple: **understand how a system works so that we can trust it.**
