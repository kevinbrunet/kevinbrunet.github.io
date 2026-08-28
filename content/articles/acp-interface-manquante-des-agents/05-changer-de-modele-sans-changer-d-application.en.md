---
title: "Change the model without changing the application"
seo_title: "Change an AI model without replacing the application"
slug: "change-model-without-changing-application"
date: 2026-09-28
description: "Separating client, harness, and model lets them evolve independently without promising magical interchangeability."
categories: ["Artificial intelligence", "Software architecture"]
series: ["acp-interface-manquante-des-agents"]
series_order: 5
collection: "ARCHITECTURE"
cover: "/images/articles/acp-05-interface-agents.en.png"
draft: false
---

{{< callout variant="scene" label="Two common scenarios" >}}
A new model understands long documents better, costs less, and performs better on complex cases.

The opposite also happens: a provider updates a production model and performance suddenly drops on a specific business use case, even though the application, prompts, and tools have not changed.

In one case, the company wants to adopt the stronger model. In the other, it needs to roll back or switch. Neither change should force employees to move to another application. Conversations, approval requests, history, sources, and harness rules should remain available.
{{< /callout >}}

## The change happens behind the conversation

When client, harness, and model are fused together, a model change becomes a product migration. Sessions move, controls are rewritten, integrations are retested, and users learn a new experience.

With an explicit boundary, the client continues speaking ACP to the harness. The harness continues exposing the same business capability while its model adapter changes. From the user's point of view, the task, progress, permissions, and result keep the same structure.

This does not mean the implementation is trivial. Prompt behavior, tool selection, structured output, latency, and cost may all change. The architectural gain is that these differences are handled inside the harness rather than leaking into every client.

## One case may require several kinds of expertise

Model choice does not have to be global. A fast model can classify documents and extract fields. A stronger model can compare exceptional clauses. A locally hosted model can process especially sensitive data. The harness routes each step while keeping one conversation and one evidence chain.

ACP can already expose related choices. [Session Config Options](https://agentclientprotocol.com/announcements/session-config-options-stabilized) let an agent offer session-specific selectors such as a model, mode, or reasoning level. A business harness can turn those primitives into understandable choices such as “standard review” or “in-depth review.”

## The company changes at its own pace

A new model can first run in shadow mode on historical cases. It can then handle a small percentage of new work, one task category, or one team. The old route remains available while evidence accumulates.

This gradual deployment separates vendor timing from company timing. A provider announcement becomes an input to an evaluation, not an automatic migration deadline.

## Evaluations are the portability mechanism

The harness must define what compatibility means for the business: required facts, acceptable claims, correct tools, valid permissions, trace completeness, latency, and cost. It can replay representative cases and compare both final results and trajectories.

Anthropic's [guidance on agent evaluations](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) distinguishes capability from regression and recommends measuring both outcomes and the paths agents take. OpenAI similarly recommends establishing a quality baseline before substituting smaller models where they remain sufficient.

{{< thesis >}}
Evaluations replace assumed loyalty with demonstrated compatibility.
{{< /thesis >}}

## Portability is a discipline, not a button

{{< callout variant="alert" label="Portability is never automatic" >}}
Models do not follow instructions identically. They may choose different tools, request more context, or produce slightly different formats. A provider may also offer a hard-to-replace feature. The company can accept that dependency for one route while keeping the rest of the harness portable.
{{< /callout >}}

Separation does not promise an instant swap. It provides a place to organize the change, tests to decide whether it is safe, and a way to preserve the previous solution during transition.

{{< pullquote >}}
The goal is not for every model to be equal. It is for each model's value to be measured inside the company's own system.
{{< /pullquote >}}

{{< closing-question label="The strategic question" >}}
If both model and interface can change, which asset must the company truly own?
{{< /closing-question >}}

---

## Sources

- Agent Client Protocol, [Session Config Options stabilized](https://agentclientprotocol.com/announcements/session-config-options-stabilized)
- Anthropic, [*Demystifying evals for AI agents*](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- OpenAI, [*A practical guide to building agents*](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)
