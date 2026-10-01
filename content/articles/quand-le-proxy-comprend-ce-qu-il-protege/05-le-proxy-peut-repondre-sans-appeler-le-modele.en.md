---
title: "The proxy can respond without calling the model"
slug: "ai-proxy-synthetic-response-user-choice"
date: 2026-11-10
description: "A synthetic response can explain a decision and offer permitted paths. Its integration depends on the client's protocol."
categories: ["Artificial intelligence", "Cybersecurity", "Software architecture"]
series: ["quand-le-proxy-comprend-ce-qu-il-protege"]
series_order: 5
collection: "SYSTEMS"
cover: "/images/articles/shieldstral/05.en.png"
draft: false
---

{{< callout variant="scene" label="Starting point" >}}
Nora asks Claude Code to summarize a file using a frontier model. LiteLLM intercepts the request and Shieldstral detects a confidential industrial process.
{{< /callout >}}

The company can handle this situation in two ways. It can keep Claude Code and ask the proxy to respond in place of the model. It can also provide, alongside the proxy, an agent compatible with the Agent Client Protocol. An ACP client can then display explanations, options, and permission requests in an interface designed for them.

The ACP agent offers a richer integration, but requires Nora to use a compatible client. A synthetic response targets an existing interface and is the first path to integrate and test.

The proxy could simply block the call with an error. Nora would know her request failed, but not how to proceed. It can do better: contact no provider and return a response itself in the format Claude Code expects.

> I did not send this document to the requested model because it contains a confidential process. You can ask me to pseudonymize the sensitive passages, use the local model, or cancel.

To Nora, this text appears as an ordinary assistant response. In reality, no general-purpose model produced it.

## LiteLLM can produce a response without calling the provider

LiteLLM allows a hook to run immediately before a model call. For Chat Completions calls, this hook can return a string instead of the modified request. LiteLLM then builds an assistant response in the endpoint's format, including streaming.

LiteLLM also supports registering a custom provider. This component receives the request and can either call the authorized model or directly return a `ModelResponse`. The documentation also shows how to transform this response for Anthropic's `/v1/messages` endpoint, which Claude Code uses when going through a gateway.

The necessary mechanism therefore exists, but it requires code inside or around LiteLLM. Shieldstral computes the decision; a hook or custom provider builds the safety response.

```text
Claude Code
    ↓
LiteLLM + Shieldstral check
    ├── allowed → model call
    └── choice required → synthetic response, no model call
```

## The question remains textual

Claude Code displays this response, but does not automatically turn the options into buttons. Nora replies in the next message:

> Use the local model.

or:

> Pseudonymize the sensitive passages, then continue.

The proxy must recognize this resumption. It cannot simply look for the words “local model” in the text: a document sent by Nora could contain the same phrase.

The synthetic response must therefore be associated with a temporary decision stored on the server:

```text
decision identifier
document fingerprint
Nora's key or identity
originally requested model
permitted options
expiration date
```

On the next message, the proxy checks that the choice corresponds to that decision, that the document has not changed, and that authorization has not expired.

## Choice never bypasses policy

The proxy only offers paths that are already permitted. If the frontier model cannot receive the complete document, Nora never sees a “send it anyway” option.

The choices can be:

- pseudonymize the located passages, then call the requested model;
- use a local model with the complete document;
- cancel.

If Nora chooses pseudonymization, the transformed content is checked a second time before leaving. If she chooses the local model, LiteLLM routes the request to the authorized deployment. If she cancels, no model is called.

## This solution does not work uniformly across clients

LiteLLM's documentation establishes that it can return a regular rejection response for Chat Completions and shows how a custom provider can serve Anthropic's `/v1/messages` endpoint. These mechanisms make integration with Claude Code conceivable. They do not by themselves demonstrate the interactive resumption described here: the client, endpoint, streaming, and decision state must be tested together.

Codex now uses the Responses API for its custom providers. The hook shortcut that returns a string is not documented for that endpoint. To offer the same experience in Codex, a layer must produce a valid Responses API response and handle streaming. This compatibility must not be presented as established without testing the deployed version.

This difference does not change the architectural principle: the control point can respond in place of the model. It requires adapting the response to the protocol the client actually uses.

## An ACP agent can offer a richer integration

The company can also distribute an ACP agent that calls LiteLLM on the user's behalf. When the proxy requires a choice, this agent can adapt the decision to `session/request_permission`, after checking that the options and their scope match that contract. An ACP client can then present structured options, receive Nora's selection, and resume the task.

```text
ACP client
    ↓
ACP agent supplied with the proxy
    ↓
LiteLLM + Shieldstral
```

This architecture does not turn LiteLLM into an ACP proxy. It adds an agent above the gateway. LiteLLM retains policy enforcement; the agent adapts its decisions to the client's interaction protocol.

This second path suits a company that controls the tool distributed to its users. It requires more development, but can replace a textual question with an explicit interaction. For other clients, the synthetic response remains a path to integrate and evaluate separately.

## Blocking without abandoning the user

Useful security explains what was not sent and identifies the paths that remain available.

Here, the proxy remains the gatekeeper: it checks the content, determines the options, and verifies resumption. The synthetic response simply makes that decision visible in an interface that has no dedicated mechanism to display it.

This transparency also reduces the incentive to bypass the official tool. The next article examines the connection between opaque blocking and shadow IT.

---

{{< closing-question label="Takeaway" >}}
User choice concerns permitted paths. It can never override a transmission prohibition.
{{< /closing-question >}}

## Sources

- [LiteLLM — Modify / Reject Incoming Requests](https://docs.litellm.ai/docs/proxy/call_hooks)
- [LiteLLM — Custom API Server](https://docs.litellm.ai/docs/providers/custom_llm_server)
- [Anthropic — Claude Code, LLM gateway](https://docs.anthropic.com/en/docs/claude-code/llm-gateway)
- [OpenAI — Codex configuration reference](https://developers.openai.com/codex/config-reference)
- [Agent Client Protocol — Architecture](https://agentclientprotocol.com/get-started/architecture)

**Continue reading:** [Banning AI fuels shadow IT](/en/articles/ai-proxy-shadow-it-official-path/).
