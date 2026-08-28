---
title: "The real asset is the harness, not the chat window"
seo_title: "AI agents: the harness is the company's strategic asset"
slug: "harness-asset-not-chat-window"
date: 2026-09-28
description: "The durable asset in an agent strategy is the enterprise harness and its open contracts, not a vendor's interface."
categories: ["Artificial intelligence", "Software architecture"]
series: ["acp-interface-manquante-des-agents"]
series_order: 6
collection: "ARCHITECTURE"
cover: "/images/articles/acp-06-interface-agents.en.png"
draft: false
---

{{< callout variant="scene" label="What must survive" >}}
A chat window can disappear within months. The way a company prepares an RFP, analyzes an investment, or manages an incident must outlive it.

That capability does not live in the color of a button or the model name displayed above a conversation. It lives in the harness: how a request becomes a task, which tools may be called, which rules apply, who must authorize an action, and which evidence must be retained.

Contracts with interfaces, models, and tools make this harness portable. They are one of its properties, not the whole asset.
{{< /callout >}}

## A conversation can hide two forms of dependency

The first dependency is visible: users work inside a vendor's interface. Sessions, approval dialogs, and collaboration habits belong to that product.

The second is deeper: the business capability itself may have been built inside the vendor's agent. Prompts, connectors, permissions, evaluation logic, and traces are then difficult to extract. Changing the interface means losing part of the way the company works.

ACP addresses the first boundary by defining how clients and agents communicate. MCP addresses another by standardizing access to tools and context where sharing is useful. Neither protocol automatically gives the company ownership of its business logic. That requires deliberately placing the logic in a harness the company controls.

## Owning the harness means owning the way work is done

{{< thesis >}}
An enterprise harness combines instructions, tools, authorization policies, controls, evaluation sets, traces, and escalation mechanisms that turn a model into a business capability.
{{< /thesis >}}

Owning it does not necessarily mean building every component internally. A company can use hosted models, commercial tools, and managed infrastructure. Ownership means retaining the contracts, configuration, evidence, and ability to replace a dependency without rebuilding the whole capability.

This asset improves cumulatively. Expert corrections become tests, incidents become controls, new systems become tools, and policy decisions become reusable rules. A chat window rarely captures that learning by itself.

## The harness connects to tools. ACP connects it to interfaces

```text
business interfaces
        ↕ ACP
enterprise harness
        ↕ model APIs
replaceable models
        ↕ direct calls or MCP
tools, data, and enterprise systems
```

This target architecture separates three cycles of change. Interfaces evolve with user needs. The harness evolves with the business process and its governance. Models evolve with the market. Direct calls and MCP coexist according to simplicity, performance, and interoperability requirements.

The separation also clarifies responsibility. Clients present interactions. The harness decides which action is allowed and records the decision. Models propose and reason. Enterprise systems remain authoritative for identity, policy, and data.

## Available everywhere without giving up guarantees

Making one harness available through several clients must not mean distributing unrestricted access. Every session still needs an identified user, a defined purpose, limited permissions, and traceable actions.

An internal registry can list approved harnesses and clients. Delegated task-scoped credentials can preserve the difference between the user, the agent, and the service. Central policy can constrain what each route may do. Evaluation gates can prevent an untested model version from silently entering production.

Openness is therefore not the absence of control. It is the ability to change components while keeping controls attached to the capability.

## Openness becomes an enterprise capability

Once clients and harnesses share an explicit contract, a company can distribute new business capabilities faster. Teams can create a harness for procurement review, incident analysis, contract verification, or deployment support and make it available in already adopted interfaces.

Users gain choice without each team rebuilding a full product. Technical teams can compare providers and models without moving every conversation. Governance teams can review one controlled capability rather than a collection of hidden prompt integrations.

## Build what must remain

Models will continue to change. Interfaces will too. Some providers will disappear; others will offer capabilities that would be unreasonable to ignore.

{{< callout variant="key" label="Architecture choice" >}}
The answer is not an architecture without dependencies. It is deciding where dependencies are acceptable and where the company must retain control.
{{< /callout >}}

{{< pullquote >}}
The model supplies intelligence. The interface supplies a place to collaborate. The harness carries the way the company works.
{{< /pullquote >}}

ACP and MCP make those boundaries more explicit. They do not remove the need for business APIs, identity, authorization, observability, or evaluation. They provide open contracts around the asset that should survive them all.

{{< closing-question label="Key takeaway" >}}
The real asset is not the window where an employee types a request. It is the harness that carries the business capability, acts under company rules, and continues to exist when that window changes.
{{< /closing-question >}}

---

## Sources

- Model Context Protocol, [Introduction](https://modelcontextprotocol.io/docs/getting-started/intro)
- Agent Client Protocol, [Introduction](https://agentclientprotocol.com/get-started/introduction)
- Agent Client Protocol, [Architecture](https://agentclientprotocol.com/get-started/architecture)
- Agent Client Protocol, [Clients](https://agentclientprotocol.com/get-started/clients)
