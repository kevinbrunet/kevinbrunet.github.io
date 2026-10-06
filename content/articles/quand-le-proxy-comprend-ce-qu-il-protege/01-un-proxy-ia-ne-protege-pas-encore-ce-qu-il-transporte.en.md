---
title: "An AI proxy only protects what it is configured to check"
slug: "ai-proxy-content-controls"
date: 2026-11-10
description: "The proxy centralizes access to models. Content protection depends on the controls enabled and how they are evaluated."
categories: ["Artificial intelligence", "Cybersecurity", "Software architecture"]
tags: ["ai-platform-engineering", "llmops-agentops"]
series: ["quand-le-proxy-comprend-ce-qu-il-protege"]
series_order: 1
collection: "SYSTEMS"
cover: "/images/articles/shieldstral/01.en.png"
draft: false
---

{{< callout variant="scene" label="Starting point" >}}
Nora uses Codex or Claude Code on her work computer to summarize a file. The tool is not configured to call OpenAI or Anthropic directly. It sends its requests to the company's LiteLLM proxy.
{{< /callout >}}

Nora authenticates with LiteLLM using a virtual key associated with her account, team, or project. The proxy can check that this key grants access to the requested model, enforce the configured quotas, and forward the request to the appropriate provider.

The path is straightforward:

```text
Codex or Claude Code
        ↓
company LiteLLM proxy
        ↓
OpenAI, Anthropic, Bedrock, Vertex AI, or a local model
```

This proxy is the point where the company can protect requests before sending them to a provider. It still needs controls that decide what may leave.

Those mechanisms already exist: LiteLLM offers guardrail integrations and an LLM judge that can evaluate a request against custom criteria before the main call; Kong offers semantic similarity filtering; Bedrock Guardrails lets administrators define denied topics in natural language. The cited documentation does not, however, present benchmarks evaluating their effectiveness on business secrets like those in Nora's file. Shieldstral has a benchmark published by Mistral that includes a `Trade Secrets` category, with an F1 score of 92.1%. That published result motivates its evaluation in the prototype, without establishing superiority over other gateways.

This series examines one approach: adding Shieldstral to the gateway, a small model trained for policy-based safety classification that can run locally and has published benchmarks. The value lies in this specialized detector and its evaluation, rather than the invention of semantic controls inside a proxy.

## A common entry point for several models

Providers offer different APIs, formats, and authentication mechanisms. Without a common layer, each application must manage these differences and store the keys needed to access the models.

LiteLLM provides that common layer. I use it as a concrete example in this series, but it is not the only option. Many other AI gateways are available, whether commercial, open source, or built internally. They do not all offer the same features, but they occupy the same position between applications and model providers.

Codex lets users define a custom provider and its API address. Claude Code lets users replace the Anthropic API address with a gateway address. Both tools can therefore send requests to LiteLLM.

LiteLLM receives the request, recognizes the virtual key, and selects the deployment associated with the model name. It can then call OpenAI, Anthropic, Azure OpenAI, Amazon Bedrock, Google Vertex AI, or a local model, depending on the company's configuration.

## The proxy first controls the path

At this central point, the company can apply rules that would be difficult to maintain in each application. LiteLLM can restrict which models a key may access, track costs, enforce quotas, distribute load, and fall back to another deployment when one fails.

This centralization avoids storing provider keys on every workstation and having each team invent its own routing. It also creates a place where decisions can be logged consistently.

But knowing the path does not mean understanding what travels along it. In the starting configuration used here, LiteLLM manages access and destinations; no check on the contents of Nora's file has been enabled yet.

The first protection to add is the simplest: recognizing secrets with an identifiable form. The next article measures precisely what this filtering stops and, above all, what it still lets through.

---

{{< closing-question label="Takeaway" >}}
A common entry point makes control possible. Only an enforced policy protects what passes through it.
{{< /closing-question >}}

## Sources

- [Mistral AI — Shieldstral, Table 12](https://arxiv.org/html/2607.25857v2)
- [LiteLLM — LLM-as-a-Judge](https://docs.litellm.ai/docs/proxy/guardrails/llm_as_a_judge)
- [Kong — AI Semantic Prompt Guard](https://developer.konghq.com/plugins/ai-semantic-prompt-guard/)
- [Amazon Bedrock — Denied topics](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-denied-topics.html)
- [LiteLLM — Documentation](https://docs.litellm.ai/)
- [OpenAI — Codex configuration reference](https://developers.openai.com/codex/config-reference)
- [Anthropic — Claude Code, LLM gateway](https://docs.anthropic.com/en/docs/claude-code/llm-gateway)

**Continue reading:** [Ten out of eleven documents pass the pattern filter](/en/articles/ai-proxy-pattern-filter-limits/).
