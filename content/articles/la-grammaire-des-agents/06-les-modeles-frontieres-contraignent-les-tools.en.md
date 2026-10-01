---
title: "How to constrain a frontier model"
slug: "how-to-constrain-a-frontier-model"
date: 2026-10-01
description: "Compare structured outputs, strict tools and custom grammars in frontier model APIs."
categories: ["Artificial intelligence", "Software architecture"]
series: ["la-grammaire-des-agents"]
series_order: 6
collection: "ARCHITECTURE"
cover: "/images/articles/la-grammaire-des-agents/06-les-modeles-frontieres-contraignent-les-tools-v2.en.png"
draft: false
---

Maya asks the support agent to find Camille Martin in the area corresponding to postal code `69003`. The application already has a stable operation for this need: searching for customers by name and postal code.

So far, we have built a dynamic grammar around SQL, then considered samplers as a chain of middleware. An objection quickly arises: in businesses, many agents use a frontier model through an API. The team has access to neither the logits nor the sampler. It therefore cannot customize this chain token by token.

It does not necessarily need to. But the three architectures seen in article 2 are not supported in the same way.

## First mode: constrain the response directly

The model can produce a structured response compliant with a JSON Schema. To search for Camille Martin, we can request this result:

```json
{
  "operation": "search_customers",
  "name": "Camille Martin",
  "postalCode": "69003",
  "maxResults": 5
}
```

[OpenAI](https://developers.openai.com/api/docs/guides/structured-outputs), [Anthropic](https://platform.claude.com/docs/en/build-with-claude/structured-outputs), [Gemini](https://ai.google.dev/gemini-api/docs/generate-content/structured-output) and [Mistral](https://docs.mistral.ai/studio-api/conversations/structured-output/custom) all offer some form of structured JSON output. This is sufficient when the software expects an object. It does not necessarily allow a SQL string, Markdown or a domain language to be constrained directly.

OpenAI accepts `pattern`, formats, numeric bounds and array bounds. Anthropic also guarantees its structured outputs and accepts simple regular expressions in `pattern`, but excludes lookarounds and references to captured groups, among other constructs. Gemini documents `enum`, `minimum`, `maximum`, `minItems` and `maxItems`, among others. Mistral accepts a schema described in JSON Schema, Pydantic or Zod.

The portable core therefore remains limited: objects, required properties, simple types, arrays and `enum`. To remain compatible with multiple providers, it is better to produce the small JSON tree above, then let a deterministic compiler build the SQL.

## Second mode: constrain the tool call

The application can expose `search_customers` directly. The model selects the tool and produces its arguments; its main response remains free after execution.

OpenAI and Anthropic have a `strict: true` mode to guarantee arguments within their subset of JSON Schema. [Gemini](https://ai.google.dev/gemini-api/docs/function-calling) also documents a `validated` mode ensuring compliance with the function schema. Mistral accepts function declarations through schemas. We must therefore check the guarantee and activation mode specific to the model and API being used.

OpenAI goes further: a custom tool can receive a `regex` or `lark` grammar. We can therefore constrain a textual input such as SQL. The regex nevertheless follows Rust syntax without lookarounds, and the Lark dialect is partial. Anthropic compiles the schema into a grammar itself, but does not let us submit our own. Gemini and Mistral do not expose a comparable general grammar in their documented APIs either.

Our regex `^[0-9]{5}$` thus falls within the simple patterns documented by OpenAI and Anthropic. For our postal code, both can constrain the `postalCode` field with `pattern`. The difference appears when we want to supply a complete textual grammar for the SQL query: OpenAI exposes this entry point on its custom tools, while Anthropic receives a JSON Schema. In both cases, the server must still check that the search and its scope are authorized.

## Third mode: separate reasoning from formalization

If the API cannot constrain either the final language or the tool as required, we return to the double call from article 2.

The frontier model performs the reasoning. A second call transforms its result into structured output. This second call can use a small local model equipped with a constrained decoder.

This last solution is less satisfactory than it appears. If the small model chooses the tool and reformulates its arguments, it takes over part of the decision. A poor translation can degrade sound reasoning from the frontier model.

A [September 2026 benchmark on small models](https://arxiv.org/abs/2609.23742) confirms the importance of separating compliance and correctness: constraints eliminate schema errors in its tasks, but content errors remain. The second call must therefore be evaluated for fidelity to the first model's decision, in addition to JSON or SQL validity.

The double call therefore does not eliminate exchanges. It replaces an unpredictable loop of validation, errors and retries with two generations planned from the outset. The first model reasons freely. The second receives that reasoning and directly produces SQL under constraint.

The price remains high: an additional generation, more latency and a handoff between two models. It is a fallback when the frontier model cannot constrain either its SQL response or the tool call. It is not the architecture to favor when either of the first two modes is available.

## Coverage remains very uneven

| Provider | Constrained JSON response | Strict tool | Custom grammar |
| --- | --- | --- | --- |
| OpenAI | Yes | Yes | `regex` or `lark` on a custom tool |
| Anthropic | Yes | Yes | Not exposed |
| Gemini | Yes | Schema compliance in `validated` mode, depending on the API | Not exposed |
| Mistral | Yes | Function schema | Not exposed |
| Qwen via Model Studio | JSON mode; strict JSON Schema on compatible models | Function schema | Not exposed by the hosted API |
| Kimi via Moonshot | Not documented as strict | Tool calling | Not exposed by the hosted API |

Chinese models add an important distinction. [Qwen via Model Studio](https://help.aliyun.com/en/model-studio/qwen-structured-output) now distinguishes two modes. `json_object` requests valid JSON without guaranteeing compliance with our contract. `json_schema` with `strict: true` constrains the structure on compatible models. Availability depends on the model and input mode; the documentation notably mentions a fallback to `json_object` for multimodal inputs. Actual support must be checked before relying on this guarantee.

[Kimi K2](https://github.com/MoonshotAI/Kimi-K2) and Kimi K2.5 can call tools, but Moonshot does not document a strict mode or custom grammar comparable to OpenAI's. Their hosted API therefore does not necessarily offer more control than Western platforms.

Qwen and Kimi nevertheless have another advantage: several of their models are available with their weights. By serving them with [vLLM](https://docs.vllm.ai/en/latest/features/structured_outputs/), the team chooses its own structured output engine and can apply a JSON Schema, regex or grammar independently of the creator's API limitations. The capability then comes as much from the inference server as from the model.

## The model's intelligence remains our main corrective mechanism

At present, many teams limit errors by choosing a more intelligent model. If that is not enough, they validate the response, return the error to the model and pay for another round. In both cases, reliability rises with the bill: either tokens cost more, or more of them must be consumed.

The grammar follows the opposite logic. It removes forbidden outputs before generation and reduces tokens spent on errors, explanations and new attempts. A cheaper model can then suffice for some formalization steps.

This mechanism is therefore not naturally aligned with the business model of an API billed per token. A provider can sell a more powerful model or several exchanges to reach the result. Exposing a constraint that achieves it on the first attempt reduces precisely that consumption.

A grammar is therefore particularly useful with a self-hosted model. The team controls the inference engine and chooses where to apply a JSON Schema, regex or complete grammar. The capability no longer depends on what a remote API chooses to offer.

With a frontier model, integration becomes more complicated. We must work with each provider's JSON Schema subset, reasoning modes and endpoints. OpenAI stands out here through a specific extension point: its custom tools directly accept a regex or Lark grammar, whereas the other platforms compared mainly expose structured JSON and function calling.

The series therefore ends on this limitation. In self-hosting, grammars, samplers and logits processors can form a customized chain. With a frontier model, this chain remains behind the API. The developer can only use the extension points the provider decides to expose.

The frontier model brings greater reasoning capacity. In exchange, it removes some control over how its logits become an action. That is why constrained generation is currently more powerful in self-hosting, even though OpenAI significantly narrows the gap.

---

## Sources

- [OpenAI, Function calling](https://developers.openai.com/api/docs/guides/function-calling)
- [OpenAI, Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
- [Anthropic, Strict tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use)
- [Anthropic, Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
- [Anthropic, Troubleshooting tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/troubleshooting-tool-use)
- [Google, Structured outputs](https://ai.google.dev/gemini-api/docs/generate-content/structured-output)
- [Google, Function calling](https://ai.google.dev/gemini-api/docs/function-calling)
- [Mistral, Custom Structured Outputs](https://docs.mistral.ai/studio-api/conversations/structured-output/custom)
- [Alibaba Cloud Model Studio, Qwen Structured Output](https://help.aliyun.com/en/model-studio/qwen-structured-output)
- [Moonshot AI, Kimi K2](https://github.com/MoonshotAI/Kimi-K2)
- [vLLM, Structured Outputs](https://docs.vllm.ai/en/latest/features/structured_outputs/)
- [Chavan, Constrained Decoding Eliminates Structural Failures in Small LLMs but Reveals a Scale-Dependent Semantic Gap (preprint, September 2026)](https://arxiv.org/abs/2609.23742)
