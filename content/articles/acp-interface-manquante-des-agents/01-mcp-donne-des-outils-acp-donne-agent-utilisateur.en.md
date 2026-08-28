---
title: "MCP gives the agent tools. ACP gives the user the agent."
seo_title: "ACP and MCP: two complementary interfaces for AI agents"
slug: "mcp-tools-acp-agent-user"
date: 2026-09-28
description: "MCP connects the agent to tools; ACP connects the agent to its user and preserves the interface when the agent changes."
categories: ["Artificial intelligence", "Software architecture"]
series: ["acp-interface-manquante-des-agents"]
series_order: 1
collection: "ARCHITECTURE"
cover: "/images/articles/acp-01-interface-agents.en.png"
draft: false
---

{{< callout variant="scene" label="Starting point" >}}
Choosing an agent should not mean choosing its window.

Yet much of the market still works that way. An agent arrives with its interface, sessions, action displays, and dialog boxes. Using another agent often means changing environments or building a dedicated integration.

ACP already offers another experience. In a compatible client, users can launch different agents, send a request, follow progress, inspect tool calls, authorize an action, and resume a session. The interface remains familiar; the agent behind it changes.
{{< /callout >}}

## Today, ACP lets developers choose an agent inside their editor

The first concrete ACP use case is software development. Editors such as [Zed and JetBrains](https://agentclientprotocol.com/get-started/clients) can host several compatible agents. Developers stay in their editor, open a conversation, and choose which agent should handle the task.

They may ask it to understand a project, find the cause of a bug, or change several files. The agent explores the repository, reports its progress, presents tool calls, and displays changes in the interface. When a command requires authorization, the editor presents the choices and sends the user's decision back to the agent.

The [Agent Client Protocol](https://agentclientprotocol.com/get-started/architecture) makes this experience portable. The client sends a request through `session/prompt`; the agent streams progress through `session/update` and requests approval through `session/request_permission`. The client can interrupt work with `session/cancel`, while users can later find and resume sessions.

Developers can therefore try another agent without leaving their editor, shortcuts, open files, or preferred way of following work. Conversely, a compatible agent can join another editor without its team rebuilding the entire integration.

{{< thesis >}}
ACP does not carry only an answer. It carries the duration of the task, its actions, intermediate decisions, and the control returned to the user.
{{< /thesis >}}

## The harness connects to tools. ACP connects it to the user

To act, a harness may call tools directly or use the [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro). MCP is especially useful when access must be standardized and shared across several agents or environments.

ACP opens the other side. It lets several interfaces communicate with an agent through a shared contract.

```text
user
  ↕
client ── ACP ── agent
                  ↕
        direct calls or MCP
                  ↕
           tools and context
```

The harness decides how to give the agent the means to act. MCP standardizes that connection when it needs to be shared. ACP gives users the means to steer the agent. Together, they support an architecture open on both sides without forcing every tool through the same standardization layer.

## The same protocol is already used for writing, not only coding

Obsidian is a useful example. It is primarily used to write, organize, and connect Markdown notes rather than as an IDE.

The community [Agent Client for Obsidian](https://community.obsidian.md/plugins/agent-client) turns a note vault into an ACP client. From a side panel, users can choose among compatible agents, mention a note with `@`, attach an image, launch several sessions, and find previous conversations.

The agent can read and edit notes through the vault API. Permission requests appear in the interface, and conversations can be saved as Markdown notes. The same protocol that presents a code diff can therefore support writing and knowledge-management work.

Obsidian remains the workspace. Users keep their notes, habits, and interface while Claude Code, Codex, or Gemini CLI can take turns as the agent. The engine changes, not the place where work happens.

## Tomorrow, one enterprise harness behind several conversations

Consider a company harness built to prepare responses to requests for proposals. It retrieves approved references, applies legal rules, drafts an answer, requests validation before using a sensitive document, and records the sources used.

Tomorrow, this harness could become a conversational service rather than remain locked inside one assistant. A salesperson could invoke it from a sales application, a lawyer could resume the same session from another workspace, and a specialist could continue from a dedicated client. In every interface, the harness would show progress, request the required permissions, and preserve the same business logic.

This also changes how internal capabilities are distributed. If the company already operates conversational clients that can communicate with its agents, a new harness can be delivered through conversation. The interface already exists; the new value lies in the business capability.

## Separation becomes a strategic choice

{{< callout variant="alert" label="Current limitation" >}}
ACP currently connects mainly code editors and coding agents. Version 2 is being prepared but remains a draft. Other business uses are possible, yet still require specific integration for domain interactions, fine-grained permissions, user identity propagation, and traceability. A shared interface also does not make all agents equivalent: each harness-and-model combination still needs evaluation on its intended business tasks.
{{< /callout >}}

The direction is nevertheless clear. The client owns the user experience. The harness owns the rules, context, tools, controls, and evidence. The model contributes reasoning and generation. MCP connects the harness to data, tools, and enterprise services; ACP connects it to interfaces.

{{< closing-question label="Key takeaway" >}}
The model is only one component. The company's durable asset is the harness built around it.
{{< /closing-question >}}

---

## Sources

- Model Context Protocol, [Introduction](https://modelcontextprotocol.io/docs/getting-started/intro), architecture and the tools, resources, and prompts primitives
- Agent Client Protocol, [Architecture](https://agentclientprotocol.com/get-started/architecture), client-agent separation, UX-first philosophy, and complementarity with MCP
- Agent Client Protocol, [Protocol v1 overview](https://github.com/agentclientprotocol/agent-client-protocol/blob/main/docs/protocol/v1/overview.mdx)
- Agent Client Protocol, official lists of compatible [clients](https://agentclientprotocol.com/get-started/clients) and [agents](https://agentclientprotocol.com/get-started/agents)
- Agent Client Protocol, [Registry](https://agentclientprotocol.com/get-started/registry)
- Obsidian, [Agent Client](https://community.obsidian.md/plugins/agent-client)
- RAIT-09, [Obsidian Agent Client](https://github.com/RAIT-09/obsidian-agent-client), source repository and documentation
- Applying ACP beyond coding agents is a BYOAI architecture proposal presented as an extrapolation
