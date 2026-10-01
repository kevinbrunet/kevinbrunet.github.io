---
title: "Advice can be forgotten. A grammar forbids."
slug: "advice-can-be-forgotten-a-grammar-forbids"
date: 2026-10-01
description: "A grammar removes forbidden tokens before selection, avoiding retries caused by invalid outputs."
categories: ["Artificial intelligence", "Software architecture"]
series: ["la-grammaire-des-agents"]
series_order: 1
collection: "ARCHITECTURE"
cover: "/images/articles/la-grammaire-des-agents/01-un-llm-ne-choisit-jamais-une-phrase.en.png"
draft: false
---

Maya works in customer support. She asks her new agent to find Camille Martin's record in Lyon. The application expects a JSON object containing the search text and the maximum number of results.

The team controls this output the way it still controls many agents: through advice. The prompt asks for JSON only. A skill specifies that `maxResults` must be an integer. A rules file forbids additional properties.

Then we hope the model remembers at the right moment.

## Advice can be ignored

The model receives a request, rules, context and sometimes several tools. It must decide what matters, resolve contradictions and produce a response. The instruction is in its context, but it is not a barrier.

It can therefore add a sentence before the JSON. It can write `maxResults` as text. It can forget a required property or invent one that seems useful.

The usual approach is to check its response afterwards.

The parser rejects the JSON. The validator reports that `maxResults` must be an integer or that a property does not exist. The harness turns this error into a new message: “Your response is invalid for this reason. Try again and follow the instruction.”

The agent generates a second response. Sometimes a third.

```text
prompt + rules + skill
          ↓
       generation
          ↓
       validation
          ↓
         error
          ↓
   new prompt with the error
          ↓
      new generation
```

This loop works. It also costs a fortune when multiplied by the number of tasks, agents and workflow steps.

Each failure consumes a complete generation. It increases latency. It occupies the model with a correction that adds nothing to the business need. It also forces the system to provide retry strategies, attempt limits and abandonment cases.

We pay the model to produce an error, then to understand the error it just produced, then to try not to repeat it.

## Prevent rather than remind

A grammar intervenes before the error.

Its purpose is not to explain the rule better to the model. Its purpose is to prevent it from emitting a token incompatible with the expected output.

Consider a simplified [JSON Schema](https://json-schema.org/understanding-json-schema/reference/numeric#integer):

```json
{
  "type": "object",
  "properties": {
    "maxResults": {
      "type": "integer"
    }
  },
  "required": ["maxResults"]
}
```

Once generation has produced:

```json
{"maxResults":
```

the engine knows it expects an integer. The model still computes a probability for the tokens in its vocabulary. But the decoder applies a mask before the final selection.

Tokens that can continue an integer remain available. Those that would begin a string, an object or the word `bonjour` receive an effective probability of zero.

The model can no longer choose from its entire vocabulary. It must choose from continuations still compatible with an integer.

The example is often summarized as “only digits from 0 to 9 remain possible.” In a real implementation, the engine must also handle the sign, permitted whitespace, the end of the number and the fact that a token can contain several characters. The principle remains the same: any continuation that would make the document incompatible with the grammar is removed before sampling.

## The model still chooses

The grammar does not decide that Maya wants five results.

It only defines the form of admissible responses. Among the numbers still possible, the model retains its probabilities and chooses the one that best fits the context.

This is the essential distinction. The grammar does not replace the model's intelligence. It reduces the space in which that intelligence can operate.

The [llama.cpp documentation](https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md) describes this mechanism through the GBNF format and also allows part of JSON Schema to be converted into a grammar. [vLLM](https://docs.vllm.ai/en/latest/features/structured_outputs/) offers several output constraints: a closed set of choices, a regular expression, a JSON Schema or a grammar.

## What we stop paying for

With an appropriate grammar, malformed JSON never comes out. A forbidden property never comes out. A value outside a closed set of choices never comes out.

We therefore no longer need to detect these errors, explain them to the model and restart the entire generation. The gain does not necessarily come from faster token-by-token decoding. Computing the constraint has a cost of its own.

The gain comes mainly from the loops that disappear.

The validator remains useful, but it no longer handles errors the decoder could make impossible. It can focus on constraints the grammar cannot express: is this age plausible, does this person exist, may this user modify their record?

## Syntax is only the beginning

A static schema can guarantee that `maxResults` is an integer. But the system often knows much more.

It knows which tables actually exist. It knows the methods accessible in a project. It knows the commands compatible with the state of Camille's record. It knows Maya's rights and the capabilities granted to the agent.

This knowledge can be used to build the grammar at request time.

The model would no longer merely be prevented from producing invalid JSON. It could be prevented from proposing an operation that does not exist in the current context.

Before going that far, however, we must solve a problem: a grammar intended for the final response must not prevent the model from reasoning freely before it answers.

That is the topic of the next article.

---

## Sources

- [llama.cpp, GBNF Guide](https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md)
- [vLLM, Structured Outputs](https://docs.vllm.ai/en/latest/features/structured_outputs/)
- [JSON Schema, integer type](https://json-schema.org/understanding-json-schema/reference/numeric#integer)
