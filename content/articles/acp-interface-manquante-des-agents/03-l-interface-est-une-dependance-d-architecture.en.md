---
title: "The interface is an architecture dependency"
seo_title: "AI agent interfaces: a hidden architecture dependency"
slug: "interface-agent-architecture-dependency"
date: 2026-09-28
description: "Plans, permissions, tool calls, and sessions form an interface contract that can lock an agent into one vendor."
categories: ["Artificial intelligence", "Software architecture"]
tags: ["agent-protocols", "software-architecture"]
series: ["acp-interface-manquante-des-agents"]
series_order: 3
collection: "ARCHITECTURE"
cover: "/images/articles/acp-03-interface-agents.en.png"
draft: false
---

{{< callout variant="scene" label="Behind the conversation" >}}
An agent interface does more than display text.

It shows that a task has started, receives a plan, follows tool calls, displays changed files, requests permission, and lets users interrupt work. It also finds old sessions and knows how to resume them.

These interactions already form a contract between client and agent. When that contract is private, changing either side often requires adapting the other. ACP gives this contract a name and a shared form.
{{< /callout >}}

## A conversation hides a state machine

Consider a simple editor request: “Add PDF export to this report.”

The agent inspects the project, announces a plan, finds relevant components, proposes changes, and runs tests. Some actions are informational; others await a user decision. The task may end successfully, through interruption, or with an error. The client must understand every state to present it correctly.

```text
request sent
     ↓
progress and plan
     ↓
tool call in progress
     ↓
permission requested → user choice
     ↓
result, cancellation, or error
```

Without a shared protocol, every agent invents events and every interface writes an adapter. The Cancel button must know which message to send; a command card must understand changing states; conversation history must recognize identifiers and metadata created by the agent.

This work is nearly invisible in a demo, but becomes an architecture dependency as soon as several agents or interfaces coexist.

## ACP turns behavior into primitives

The [ACP protocol overview](https://github.com/agentclientprotocol/agent-client-protocol/blob/main/docs/protocol/v1/overview.mdx) describes a bidirectional JSON-RPC conversation.

The client opens a session and sends a request through `session/prompt`. The agent publishes `session/update` notifications for message fragments, visible reasoning, tool calls, plans, and mode changes. In the other direction, the agent can call `session/request_permission`; the client presents choices and returns the user's decision. `session/cancel` transmits an interruption.

Sessions have a contract too. `session/list` discovers known conversations, while `session/resume` reconnects without replaying the full history. A new interface no longer needs to guess how an agent represents progress, permission, and lifecycle; it implements the primitives it supports.

## The interface can innovate independently

An ACP permission may become a dialog in an editor, a card in a web application, or a structured choice in a conversation. Its meaning remains stable while presentation adapts to context.

Clients can also choose how much detail to expose. A developer may want commands, output, and diffs. A business user may prefer the process step, the reason for a request, and the consequences of each choice. The protocol carries the event; the interface makes it understandable.

This separation echoes the Language Server Protocol. ACP's [introduction](https://agentclientprotocol.com/get-started/introduction) explicitly claims that lineage: clients and agents can evolve without coordinating every possible combination.

## An interface contract becomes a company asset

Return to the RFP harness. It must report consulted documents, show progress, request legal validation, and let an expert resume a case.

If those interactions exist only in the sales application, the harness depends on that application. If a vendor's agent alone defines them, the application depends on that agent. A shared contract puts business logic in the right place: the harness decides that validation is required and records the evidence; the client presents the request in a form suited to the user; ACP carries the interaction.

## Standardizing dialogue does not standardize experience

{{< callout variant="alert" label="What the standard does not guarantee" >}}
ACP capabilities are negotiated. Not every agent supports every primitive, and not every client presents them with equal richness. Resuming a session does not guarantee that two interfaces reconstruct exactly the same display.
{{< /callout >}}

{{< thesis >}}
The interface dependency does not disappear. It becomes explicit, observable, and replaceable.
{{< /thesis >}}

{{< closing-question label="Key takeaway" >}}
With a shared dialogue contract, one harness can become available through several entry points without being rewritten for each one.
{{< /closing-question >}}

---

## Sources

- Agent Client Protocol, [Introduction](https://agentclientprotocol.com/get-started/introduction)
- Agent Client Protocol, [Architecture](https://agentclientprotocol.com/get-started/architecture)
- Agent Client Protocol, [Protocol v1 overview](https://github.com/agentclientprotocol/agent-client-protocol/blob/main/docs/protocol/v1/overview.mdx)
- Agent Client Protocol, [Session list stabilized](https://agentclientprotocol.com/announcements/session-list-stabilized)
- Agent Client Protocol, [Session resume stabilized](https://agentclientprotocol.com/announcements/session-resume-stabilized)
