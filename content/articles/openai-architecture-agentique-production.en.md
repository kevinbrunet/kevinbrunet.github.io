---
title: "OpenAI reveals the agentic architecture behind ChatGPT ads"
seo_title: "OpenAI: agentic architecture in production"
slug: "openai-agentic-architecture-in-production"
date: 2026-11-03
description: "An LLM orchestrates, tools retain their responsibilities, and traces inform improvements. ChatGPT’s ad system offers a concrete case of agentic architecture."
categories: ["Artificial intelligence", "Software architecture"]
tags: ["ai-systems-harness-engineering", "ai-observability"]
collection: "ARCHITECTURE"
cover: "/images/articles/openai-architecture-agentique-production.en.png"
draft: false
---

A model interprets a conversation, calls tools, retrieves candidates and assesses their relevance. Yet it does not decide the outcome alone. Business rules eliminate some candidates. An auction mechanism retains final selection. And if the system is too late, it returns nothing.

This architecture runs inside ChatGPT. It selects advertisements.

On October 21, 2026, OpenAI published a [technical account by Ritendra Datta and Karthik Gopalratnam](https://openai.com/index/building-chatgpt-ad-stack/). Its interest extends beyond advertising. It offers a working agentic system to examine, including its dependencies, controls and improvement loop.

{{< thesis >}}
Reliability does not necessarily belong to the component. It can belong to the system around it.
{{< /thesis >}}

This publication gives that idea a concrete form. It also invites us to clarify what we mean by a system that learns from its own operation.

## An orchestrator with defined responsibilities

The system relies on a specialized LLM that interprets conversational context and calls retrieval, filtering and evaluation tools. It nominates candidates for an auction mechanism, which retains pricing and final selection. Further checks follow, including possible contextual rejection by the orchestrator.

The flow can be summarized as follows:

```text
Conversational context
          ↓
LLM orchestrator and tool calls
          ↓
Queries → semantic retrieval
          ↓
Eligibility → relevance assessment
          ↓
Auction → final checks
          ↓
Possible delivery
```

This diagram summarizes responsibilities. The orchestrator can call tools repeatedly.

**The orchestrator can interpret context without taking over every decision in the system.**

I see a transferable design principle here. A model can understand that a request calls for a refund. The payment service must still check the authorized amount, order status and caller permissions. Whether a proposal makes sense and whether its execution is authorized are separate questions.

That separation must exist in interfaces and code. An instruction telling a model to respect a limit cannot replace the component that actually rejects requests exceeding it.

Each boundary still needs examination. A tool called by an LLM is not necessarily deterministic. A relevance score may itself come from a model. The useful question becomes: **which component owns which decision, and what guarantee does it provide?**

## The agent can abstain without making the product fail

OpenAI describes an ad service separate from response generation. Its latency or unavailability must not block ChatGPT. Returning no ad is an acceptable outcome.

These choices reinforce each other. An optional dependency can remain optional if the product knows how to operate without its result.

In our own architectures, we often add an agentic step to an existing workflow, such as suggesting an action, enriching a case or preparing a recommendation. We then need to decide whether that step can interrupt the main service.

{{< callout variant="scene" label="Applying the idea elsewhere" >}}
A support portal uses an agent to suggest documentation when a customer opens an incident. Retrieval may return nothing, exceed its time budget or propose a document with insufficient confidence.

Should the ticket wait? If the suggestion is optional, the portal can record the incident immediately and skip enrichment for this interaction.
{{< /callout >}}

That decision requires more than a timeout. It defines what product success means and what the agent can add to it.

We also need to distinguish reasons for abstention. “No useful suggestion” and “service unavailable” may produce the same screen but call for different interventions. The first outcome may be correct. The second indicates a technical degradation.

## Observe business stages to identify what needs improvement

The events OpenAI describes distinguish, among other outcomes, no advertising opportunity, no retrieval request, retrieval returning no candidates, eligibility rejections and interactions after delivery.

This granularity changes the questions we ask of traces. We can investigate **where the process stops and why**, rather than just counting failed calls.

Consider our support agent again. A single “suggestion displayed” metric cannot distinguish several situations:

| Observed situation | Question to investigate |
|---|---|
| The agent did not start a search | Did it correctly recognize the need? |
| Retrieval returned nothing | Does the content exist, and can it be found? |
| Documents were rejected | Are they outdated, out of scope or incorrectly classified? |
| A suggestion was prepared too late | Does the time budget fit the workflow? |
| The customer dismissed the suggestion | Was it useful in this context? |

This table is a proposal for our example, rather than an additional description of OpenAI’s system.

Each row points toward a different improvement. Expanding the documentation base will not necessarily fix poor recognition of the need. Faster retrieval will not fix documents that are consistently unsuitable.

**A trace becomes useful when it helps distinguish competing explanations of the problem.**

That requires preserving the connection between a stage, its relevant inputs, its outcome and the version of the component involved. A failure count without that attribution can lead us to change the wrong part of the system.

## Traces become raw material for improvement

OpenAI describes a loop combining production events, powerful evaluator models, improvements to smaller models and human feedback. The publication also mentions Codex in development, with delivery safeguards and data analysis tools.

```text
Execution → structured events → evaluation
                                    ↓
                     Evaluator models + human feedback
                                    ↓
                         Component improvements
                                    ↓
                           Subsequent executions
```

This passage is particularly relevant to **crystallization**, by which I mean turning experience into a lasting capability, whether a learned behavior, a procedure or a control.

Production traces can serve purposes beyond diagnosing incidents. Once qualified and selected, they can help build evaluations, identify difficult cases or prepare improvements to a probabilistic component.

But a trace does not automatically carry its own lesson. An ignored recommendation may be poor, arrive too late or address a need that has already been resolved. A click proves an interaction. Establishing satisfaction or decision quality requires additional evidence.

Human feedback provides another perspective, provided we specify what it measures. A survey, an explicit correction and an observed behavior do not answer exactly the same question.

{{< pullquote >}}
Traces can support learning. They cannot decide, on their own, what deserves to be learned.
{{< /pullquote >}}

## Improving models does not demonstrate autonomous harness evolution

The publication describes an improvement loop for the system and its models. It does not demonstrate an autonomous mechanism that modifies and promotes the entire *harness*, the software environment organizing the model’s instructions, tools and controls.

That distinction is essential to this discussion.

Improving a relevance model, changing an instruction and moving an authorization check carry different risks. A measured gain in the first does not validate the other two.

To move toward broader crystallization, I would therefore require an explicit chain of evidence. Which experiences motivated the change? Which component changed? Which independent cases were used to evaluate it? What decision authorized activation?

The current version must be allowed to remain preferable. A proposed improvement must be open to rejection. And if a change degrades actual operation, reverting to the previous state must remain possible.

These are architectural requirements I propose here. This publication alone does not establish that such mechanisms exist in OpenAI’s system.

## Design the boundaries before expanding autonomy

My interpretation of this case comes down to three decisions: define what the model may decide, provide for situations where the system can abstain, and organize the evidence that will guide improvements.

These decisions give reliability an operational form. They let us use the model’s ability to interpret context while retaining verifiable responsibilities around it.

The improvement loop adds another requirement. Controls must also govern changes to the system. An architecture that is reliable during execution can lose its guarantees if its evolution mechanism bypasses them.

{{< closing-question label="The architecture question" >}}
Your system can produce traces and propose improvements. What evidence does it require before turning an experience into lasting behavior?
{{< /closing-question >}}

## Sources

- Ritendra Datta and Karthik Gopalratnam, OpenAI Engineering, [*How we built ChatGPT’s novel ad stack for user trust and relevance*](https://openai.com/index/building-chatgpt-ad-stack/), October 21, 2026.
