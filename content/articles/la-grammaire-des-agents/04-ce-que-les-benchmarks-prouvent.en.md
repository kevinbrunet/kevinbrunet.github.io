---
title: "What grammars actually save"
slug: "what-grammars-actually-save"
date: 2026-11-05
description: "Measure the total cost of a usable output and distinguish schema compliance from business correctness."
categories: ["Artificial intelligence", "Software architecture"]
series: ["la-grammaire-des-agents"]
series_order: 4
collection: "ARCHITECTURE"
cover: "/images/articles/la-grammaire-des-agents/04-ce-que-les-benchmarks-prouvent.en.png"
draft: false
---

For a single search for Camille Martin, building a constraint generator would be excessive. The equation changes when the agent assists Maya's entire team and repeats the same workflow every day.

A dynamic grammar requires a contract, tests, a versioning strategy and runtime validation. Its value therefore depends on the cost it adds and the failures it avoids.

## The wrong calculation: tokens per second

The first temptation is to measure only decoding speed. Since some tokens are forbidden, the model would have fewer choices and should respond faster.

The engine does not work that way. The Transformer still computes the logits for its vocabulary. The grammar intervenes afterwards to determine which continuations are compatible with the prefix and mask the others. It therefore does not shrink the model's main computation. It even adds work between tokens.

The [llama.cpp documentation](https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md) warns that some constructions are expensive. We must therefore benchmark the exact combination of model, tokenizer, engine and schema.

This overhead is not necessarily significant. The [XGrammar](https://arxiv.org/abs/2411.15100) engine preanalyzes part of the vocabulary, maintains persistent parsing structures and can run grammar checking in parallel with GPU inference. Its authors report up to a hundredfold reduction in cost compared with certain earlier constraint engines and near-zero end-to-end overhead in their configurations. The constraint can therefore become almost free without accelerating the model compared with unconstrained generation.

Return on investment is measured further down the chain.

[XGrammar-2](https://arxiv.org/abs/2601.04426) extends this work to agents whose contracts vary between requests and during generation. Its authors report compilation more than six times faster than the engines compared, and near-zero end-to-end overhead in their configurations. Reusing substructures across grammars makes it possible to prepare a new contract without starting all the work again.

Another case deserves a specialized engine: selecting among thousands of permitted values. The preprint [Trie Automata for Constrained Decoding over Large Finite Sets](https://arxiv.org/abs/2608.12574), published on August 12, 2026, exploits common prefixes in these strings to prepare token masks. It reports compilation and throughput gains over XGrammar in its configurations. These results concern finite sets and their server integration; they do not prove that a general SQL grammar accelerates unconstrained generation.

## The retries that disappear

Without constraints, each response opens up a range of cases: text before the JSON, a missing property, an approximate name, a value outside the list, SQL mixed with an explanation or a tool call that cannot be parsed. Client code adds extractors, repair mechanisms, retries and fallbacks.

These layers consume tokens, computation time and, above all, engineering time. They also complicate observability, because a repaired result is no longer exactly what the model proposed.

A guaranteed output eliminates repairs to its form. A contract generated from the system also reduces vocabulary errors. The cumulative gain comes from these failure paths disappearing.

## Measure form and correctness separately

A [September 20, 2026 preprint](https://arxiv.org/abs/2609.23742) evaluates five small models, from 0.6 to 4 billion parameters, on fourteen structured tasks. In this protocol, Outlines and XGrammar achieve 100% schema compliance, compared with 78.6 to 92.9% without these constraints. Content errors nevertheless persist, particularly in tasks requiring multiple function calls.

The agent can therefore produce perfectly compliant JSON while searching for Camille in the wrong district. There is no longer a parsing error, but Maya's need remains unmet.

We must measure both outcomes: the proportion of compliant outputs and the proportion of correct decisions. The cost of a usable output includes the validation and retries still needed to obtain the right business result. The benchmark reinforces this distinction; its rates are not a guarantee for all models and workflows.

## Why this is not already used everywhere

Constrained JSON outputs and tool calls are common. Custom and dynamic grammars are less common because they move the work from the prompt to infrastructure.

The contract must be built from a reliable source, converted into the engine's dialect and tested for supported features. Not all backends implement the same subset of JSON Schema.

Size matters too. A JSON grammar with a few properties is easy to compile. A grammar containing an entire framework API, thousands of symbols or many optional parameters can be expensive to build and traverse. It often needs to be divided by task, or combine a stable cached part with a small dynamic part.

Finally, a grammar guarantees a form, not a good decision. Many teams therefore stick to prompts and subsequent validation, which are easier to prototype. The cost of retries becomes apparent mainly as usage increases.

## Cases where you should not use it

Constrained generation is not suited to every kind of output. An article, a summary or creative exploration needs a broad space for expression. A business grammar that is too narrow may prevent the model from expressing a new action the system should learn to support.

A constraint can also create a false sense of security. Valid JSON can contain an absurd amount. A command permitted during generation may no longer be permitted at execution time. A backend may support only part of the schema. Domain validation, authorization and tests remain essential.

## What we have actually moved

Without a grammar, the model first generates its response. The software then checks its form and retries the model when it is unusable.

With a grammar, the software describes the acceptable form before generation. The decoder then prevents the model from producing an unknown field, an incorrect type or a token outside the permitted language.

This shift does not give the model a better understanding of the business. It does not decide whether Maya has the right to close a record or whether the action remains valid at execution time. These checks stay in the application.

The established benefit is more precise: when the expected output has a structure or closed vocabulary, the grammar prevents some impossible responses before they are formulated. It thus reduces repairs and retries associated with form.

It can also reduce the scope of action. A SQL grammar limited to `SELECT` prevents `DELETE`, `UPDATE` and `DROP`. For a `grep` tool, the contract can limit paths to a directory and reject `..` or absolute paths.

This restriction remains active in the face of a prompt injection asking to delete a table or escape the sandbox. The injection may redirect the choice among permitted actions, but cannot reintroduce forbidden tokens. The grammar thus limits the attack's scope.

That is the power of a grammar: the dangerous output is not rejected afterwards; it never exists. The model simply cannot produce it.

So far, the grammar mainly guarantees syntax and a closed vocabulary. For code generation, that is not enough. A method can be spelled correctly without existing, a call can target the wrong version of a framework, and two valid types can remain incompatible.

Can we strengthen the grammar with compiler information to help the model produce code that actually uses the right APIs?

That is the direction explored in the next article.

---

## Sources

- [llama.cpp, GBNF Guide](https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md)
- [Dong et al., XGrammar: Flexible and Efficient Structured Generation Engine for Large Language Models (2024)](https://arxiv.org/abs/2411.15100)
- [Li et al., XGrammar-2: Dynamic and Efficient Structured Generation Engine for Agentic LLMs (2026)](https://arxiv.org/abs/2601.04426)
- [Xu and Bouyarmane, Trie Automata for Constrained Decoding over Large Finite Sets (preprint, August 2026)](https://arxiv.org/abs/2608.12574)
- [Chavan, Constrained Decoding Eliminates Structural Failures in Small LLMs but Reveals a Scale-Dependent Semantic Gap (preprint, September 2026)](https://arxiv.org/abs/2609.23742)
