---
title: "One enterprise harness, several entry points"
seo_title: "One enterprise agent available through several interfaces"
slug: "enterprise-harness-several-interfaces"
date: 2026-09-28
description: "ACP makes it possible to expose one business harness through several clients without rebuilding every experience."
categories: ["Artificial intelligence", "Software architecture"]
series: ["acp-interface-manquante-des-agents"]
series_order: 4
collection: "ARCHITECTURE"
cover: "/images/articles/acp-04-interface-agents.en.png"
draft: false
---

{{< callout variant="scene" label="Starting principle" >}}
An enterprise harness should not become yet another application everyone must learn.

It should meet employees where their work already happens. The same agent can be useful in a sales application, a knowledge base, a messaging tool, or a specialized client. Its presentation changes with context; its rules, tools, and controls remain the same.

ACP makes this idea concrete: the harness becomes a capability available through several conversations rather than a product locked inside one window.
{{< /callout >}}

## The same need from different applications

A salesperson receives an RFP in the CRM and asks the harness to prepare an answer. The client automatically adds the customer record and opportunity. The harness retrieves approved references, identifies missing information, and starts a draft.

A lawyer later resumes the same case from a legal workspace. This client emphasizes clauses, sources, and approval requests rather than sales data. A subject-matter expert may join from a general conversational client and answer one question without learning a new application.

The business process is the same. Each client contributes useful local context and presents the interaction in its own language. ACP provides the shared conversation contract. Client-specific context remains the responsibility of each integration, while MCP may let the harness retrieve data not already supplied with the request.

## The ACP ecosystem already demonstrates diverse entry points

The official [client list](https://agentclientprotocol.com/get-started/clients) includes editors, Obsidian, desktop and web clients, mobile applications, notebooks, and messaging gateways. They do not all offer the same experience, but they can communicate with compatible agents through the same protocol.

The [ACP Registry](https://agentclientprotocol.com/get-started/registry) adds a discovery and configuration mechanism. In an enterprise setting, the same principle can support an internal catalog: approved harnesses, fixed versions, permitted clients, owners, and declared capabilities.

## The client adapts the experience; the harness keeps the decision

Moving the interface must not move the policy. If a confidential reference requires legal approval, that rule belongs in the harness. A sales client may display it as a compact card, while a legal client includes the full rationale and source. Both return the decision through ACP; neither decides whether approval was required.

This separation preserves consistent behavior. Identity, authorization, evidence, and escalation remain attached to the business capability even when the user changes entry point.

## Conversation becomes a distribution channel

Traditional internal tools carry a high adoption cost: navigation, training, identity integration, maintenance, and support. A conversational interface already present in daily work changes that cost. Employees describe their goal; the harness turns it into a workflow, asks for missing information, exposes its actions, and requests validation.

{{< thesis >}}
A new harness does not necessarily require a complete new interface. It primarily needs a clear client contract, reliable tools, an authorization policy, and a way to prove what it did.
{{< /thesis >}}

## Start before everything is stabilized

{{< callout variant="alert" label="Start with a controlled scope" >}}
ACP is currently most mature around coding agents, and remote transport is still being standardized. A company can nevertheless begin with one managed client, one pilot team, and non-critical cases, while complementing ACP with its existing security infrastructure.
{{< /callout >}}

Identity can be connected through OIDC or OAuth and passed to the harness through a task-scoped delegated token. Ephemeral session environments can isolate execution. An internal registry can pin agent versions and authorized clients. Correlation identifiers can connect ACP sessions, model calls, MCP tools, and writes to enterprise systems.

{{< pullquote >}}
Let ACP carry the client-agent contract, and leave identity, isolation, policy, and evidence to systems designed for them.
{{< /pullquote >}}

{{< closing-question label="The next question" >}}
How can the company change models without forcing users to change interfaces or lose their way of working?
{{< /closing-question >}}

---

## Sources

- Agent Client Protocol, [Clients](https://agentclientprotocol.com/get-started/clients)
- Agent Client Protocol, [Registry](https://agentclientprotocol.com/get-started/registry)
- Agent Client Protocol, [Introduction](https://agentclientprotocol.com/get-started/introduction)
- Agent Client Protocol, [Transports working group](https://agentclientprotocol.com/announcements/transports-working-group)
