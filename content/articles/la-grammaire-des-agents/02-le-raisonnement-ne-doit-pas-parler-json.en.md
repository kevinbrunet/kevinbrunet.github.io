---
title: "Reasoning should not have to speak JSON"
slug: "reasoning-should-not-have-to-speak-json"
date: 2026-11-05
description: "Keep reasoning free and constrain only the message the software needs to consume."
categories: ["Artificial intelligence", "Software architecture"]
series: ["la-grammaire-des-agents"]
series_order: 2
collection: "ARCHITECTURE"
cover: "/images/articles/la-grammaire-des-agents/02-le-raisonnement-ne-doit-pas-parler-json.en.png"
draft: false
---

In the previous article, we saw that a grammar could remove forbidden tokens from a model's output. When a field expects an integer, incompatible continuations receive an effective probability of zero.

But which output do we want to constrain?

The answer depends on the architecture. The model may return the SQL query directly. It may call a tool that executes it against the database. It may also run on an API that does not offer the type of structured call we need.

These three cases do not place the grammar in the same location.

## First case: the model returns the result directly

To find Camille Martin, Maya's agent can produce a SQL query itself. Before answering, it must examine the schema, connect customers to their addresses and distinguish people with the same name.

Its reasoning might begin: “I need to filter the name, then use the city stored in the address.” The expected response, however, must begin with `SELECT` and follow the permitted SQL grammar.

```text
free reasoning
      ↓
end of reasoning
      ↓
constrained SQL query
```

The grammar must not be activated at the very first token. The decoder would immediately expect `SELECT` and prevent the model from analyzing the problem.

Reasoning models make this boundary visible. The [Qwen documentation](https://github.com/QwenLM/Qwen3/blob/main/docs/source/getting_started/concepts.md), for example, describes the `<think>` and `</think>` tags. The [Qwen API](https://docs.qwencloud.com/developer-guides/text-generation/thinking) exposes `reasoning_content` and `content` separately.

An engine can use this separation to leave the first channel free and constrain the second. [vLLM](https://docs.vllm.ai/en/latest/features/structured_outputs/) documents combining a reasoning parser with structured outputs.

[XGrammar-2](https://arxiv.org/abs/2601.04426) also addresses changes in structure during generation. Its `TagDispatch` mechanism selects a structure based on a tag. This provides a building block for alternating free text and constrained regions; the application must still define the boundary that matches the model's protocol.

## Second case: the model calls a tool

The application can also expose an `execute_query` tool. The model builds the same SQL query, but instead of returning it as the final response, it places it in the call's arguments:

```json
{
  "name": "execute_query",
  "arguments": {
    "sql": "SELECT ... FROM customers ..."
  }
}
```

The name must match an available tool and the arguments must follow its JSON Schema. The server executes the query, then returns the resulting rows to the model.

Here, the constraint applies to the tool call. Its exact scope depends on the model and server being used. Some constrain only the JSON structure of the arguments. Others accept regular expressions or more precise grammars. Each provider has its own limitations, which we will examine in article 6.

A compliant output obviously does not guarantee that the action is legitimate. The query may target a nonexistent table, request forbidden data or exceed Maya's rights. The server must still validate the query before execution.

After execution, the main response remains free. The agent can explain normally to Maya which records match Camille Martin.

```text
free reasoning
      ↓
constrained tool call
      ↓
execution by the application
      ↓
free main response
```

This distinction matters with frontier models. The provider can guarantee the structure of the tool call without imposing the same format on the response intended for the user. Article 6 will return to the strict modes and grammars exposed by their APIs.

## Third case: the required tool call is unavailable

Some models or APIs do not offer tool calling. Others can call tools but cannot properly combine the chosen reasoning mode with the expected constraint.

We can then separate the work into two calls.

The first lets the model analyze the request and prepare the query. The second receives this analysis, runs without explicit reasoning and generates only the constrained SQL.

```text
call 1: free reasoning
              ↓
      intermediate plan
              ↓
call 2: constrained generation
              ↓
       valid SQL or JSON
```

This is a fallback solution. It adds a generation, latency and an intermediate artifact to transmit. It remains useful when the API provides no usable boundary between reasoning, the structured call and the main response.

Some models that expose their reasoning in a dedicated region allow this behavior to be disabled. Qwen, for example, offers the `enable_thinking` parameter. For a simple task, the model can then produce the constrained output directly, without a reasoning channel to separate.

## Constrain the right message

The rule is therefore not “apply the grammar to the model's entire response.” We must identify the message the software needs to consume.

If the model returns SQL directly, the grammar protects the final SQL. If it acts through a tool, it protects the name and arguments of the call. If this interface does not exist, two calls can recreate the boundary at an additional cost.

In our case, we now know how to let the agent reason freely and then constrain its SQL query. One limitation remains: the grammar knows SQL in general, but still ignores the tables and columns actually present in the support database.

The next article starts from that limitation.

---

## Sources

- [Qwen, Qwen3 concepts](https://github.com/QwenLM/Qwen3/blob/main/docs/source/getting_started/concepts.md)
- [Qwen, Thinking](https://docs.qwencloud.com/developer-guides/text-generation/thinking)
- [vLLM, Structured Outputs](https://docs.vllm.ai/en/latest/features/structured_outputs/)
- [Li et al., XGrammar-2: Dynamic and Efficient Structured Generation Engine for Agentic LLMs (2026)](https://arxiv.org/abs/2601.04426)
