---
title: "The model is not the agent"
seo_title: "Model, agent, and harness: understanding the difference"
slug: "model-is-not-the-agent"
date: 2026-09-28
description: "The model is only one component: the durable value of an enterprise agent lies in the harness around it."
categories: ["Artificial intelligence", "Software architecture"]
series: ["acp-interface-manquante-des-agents"]
series_order: 2
collection: "ARCHITECTURE"
cover: "/images/articles/acp-02-interface-agents.en.png"
draft: false
---

{{< callout variant="scene" label="Starting point" >}}
Replacing an agent's model should not erase everything the company has taught it.

Its business rules, access rights, controls, and evidence are not properties of the model. They belong to the system built around it: the harness.

This distinction changes how companies invest in AI. If the agent is confused with its model, every market advance looks like a migration. If the company owns the harness, a new model becomes a component to evaluate.
{{< /callout >}}

## An answer does not reveal the system that produced it

Imagine two assistants answering the same request for proposals with the same model and question.

The first generates text from its general context. The second identifies the client and industry, retrieves only approved commercial references, checks clauses against the legal knowledge base, marks claims that require evidence, asks for approval before using confidential material, and records every source.

The second answer deserves more trust, but not necessarily because of a better model. The difference comes from the harness organizing the work around it.

Vendor guidance describes the same composition. OpenAI's [guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/) separates models, tools, and instructions, then adds orchestration and guardrails. [Anthropic](https://www.anthropic.com/engineering/building-effective-agents) describes the basic agentic building block as an LLM augmented with retrieval, tools, and memory.

The model reasons. The surrounding system decides what it may use, within which limits, and which evidence it must produce.

## The harness contains the company's executable knowledge

In our example, the harness is not merely a carefully written prompt. Instructions encode the RFP method. Tools provide access to CRM, approved references, documents, and validation workflows. Authorization rules decide who may read or transmit information. Controls verify sources, structure, and sensitive claims. Traces explain which document and decision produced each part of the result.

This architecture turns scattered expertise into a reusable capability. Legal knowledge no longer lives only in corrections, sales methods no longer depend only on memory, and security rules participate in execution instead of being recalled at the end.

```text
user interface
      ↕ ACP
instructions + context + tools
permissions + controls + traces
          = harness
              ↕
            model
              ↕ MCP
enterprise systems and data
```

This is an architecture choice, not a topology imposed by ACP or MCP. It places in the harness everything the company wants to keep when an interface or model changes.

## The model can become a local decision

Not every RFP step needs the same capability. Extracting dates and amounts may use a fast, inexpensive model. Comparing an unusual clause with company policy may justify a stronger one. Highly sensitive material may be routed to a model running in a controlled environment.

In a separated architecture, this choice can be made task by task. The company does not replace its agent every time it changes a model. It keeps the process, tools, and guarantees, then selects the right engine for each step.

The same separation allows a new model generation to be tested without immediately moving every user. A sample of cases can be replayed, measured against business criteria, and promoted only after it meets the expected thresholds.

## What the company truly accumulates

The original model may eventually disappear. Response rules, connectors, evaluation sets, authorization decisions, and traces remain useful.

That is where the cumulative advantage lies. Every expert correction can improve an instruction or test. Every incident can add a control. Every new system can expand the available tools. The harness accumulates executable company knowledge without requiring the model to be trained on company data.

## Replaceable does not mean identical

Changing models will always require evaluations. Models interpret instructions differently, choose different tools, and produce uneven results. Some also provide proprietary functions the harness may deliberately use.

{{< callout variant="alert" label="Essential distinction" >}}
The goal is not to make models indistinguishable. It is to make their differences measurable and replacement possible, instead of silently merging the whole business capability into one model.
{{< /callout >}}

{{< pullquote >}}
The model provides intelligence available on the market. The harness turns that intelligence into the company's own way of working.
{{< /pullquote >}}

{{< closing-question label="The next question" >}}
Even with a harness separated from the model, an agent remains captive if only one application understands its plans, permissions, and sessions.
{{< /closing-question >}}

---

## Sources

- OpenAI, [*A practical guide to building agents*](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)
- Anthropic, [*Building Effective AI Agents*](https://www.anthropic.com/engineering/building-effective-agents)
