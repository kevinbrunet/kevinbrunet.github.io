---
title: "Can IntelliSense guide the model?"
slug: "can-intellisense-guide-the-model"
date: 2026-10-01
description: "Combine syntax constraints, compiler information and sampler choices to improve code generation."
categories: ["Artificial intelligence", "Software architecture"]
series: ["la-grammaire-des-agents"]
series_order: 5
collection: "ARCHITECTURE"
cover: "/images/articles/la-grammaire-des-agents/05-intellisense-peut-guider-le-sampler.en.png"
draft: false
---

A C# grammar can prevent a misplaced parenthesis or an impossible keyword. It does not know that `customer.GetBalance()` does not exist, that `Close()` is inaccessible or that the project uses another version of the framework.

To help the model produce code, we therefore need to go beyond the language's general syntax. We must account for types, methods actually available and the exact position in the file.

One tool already does part of this work for developers: IntelliSense.

## IntelliSense knows the program

When a developer writes `customer.`, IntelliSense does not suggest every word in C#. It looks for members accessible on the type of `customer`, in this project and at this position.

[Roslyn](https://github.com/dotnet/roslyn/blob/main/docs/wiki/Roslyn-Overview.md) represents the solution, its projects, their references and open documents. Its [`SemanticModel`](https://learn.microsoft.com/en-us/dotnet/api/microsoft.codeanalysis.semanticmodel?view=roslyn-dotnet-4.14.0) connects the text to symbols and types from compilation.

It can therefore know that `customer` is a `SupportCustomer`, that `AddNote()` is public, that `Deactivate()` is internal and that `GetOutstandingAmountAsync()` returns a `Task<decimal>`.

This knowledge would be valuable to a model. It comes from the code actually being compiled, rather than from a list of methods copied into a prompt and potentially outdated.

## A completion list is not a grammar

The temptation would be to use IntelliSense suggestions directly as a list of permitted tokens. This does not work.

IntelliSense suggests what seems useful at a position. It does not describe every sequence of characters that can lead to a valid program. After `customer.`, the developer can call a member, but elsewhere they can introduce a variable, start a lambda, write a constant or create a new identifier.

The segmentation also differs. Roslyn works with characters and C# syntactic units. The model generates tokens from its own vocabulary. `GetOutstandingAmountAsync` may be split into several fragments. After the first fragment, the code is incomplete without being doomed.

Finally, IntelliSense works on a temporarily invalid document and recalculates its suggestions as the developer progresses. Turning every generated token into a document modification, a new compilation and a new completion list would create an expensive loop.

IntelliSense therefore cannot be plugged in as a grammar as it stands.

## Help rather than forbid

This limitation does not make its information useless. It changes how we should use it.

A grammar applies a hard constraint. If a token cannot lead to any valid output, its effective probability becomes zero. The model must choose among the remaining continuations.

IntelliSense could provide a softer signal. An accessible method suited to the expected type receives a bonus. An obsolete API receives a penalty. A member from the right framework version is favored. Other possibilities remain available when the model needs to introduce new code.

We no longer ask IntelliSense to define the entire possible language. We ask it to help the model choose among several syntactically valid continuations.

## The sampler becomes the extension point

The model produces a score for each possible next token. A sampler then transforms this distribution before selecting one.

[`llama-server`](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md) already allows several samplers, such as Top-K, Top-P, Min-P and temperature, to be ordered. [vLLM](https://docs.vllm.ai/en/stable/design/logits_processors/), meanwhile, exposes custom `LogitsProcessor` implementations capable of modifying the logits tensor before softmax.

We can see them as a chain of middleware:

```text
model
  ↓
logits
  ↓
C# grammar: forbids the impossible
  ↓
IntelliSense signal: favors the relevant
  ↓
repetition policy
  ↓
temperature
  ↓
selected token
```

The grammar and IntelliSense no longer play the same role. The first closes paths. The second helps rank those that remain open.

A [September 2026 preprint, CLAMP](https://arxiv.org/abs/2609.08602), experiments with this combination in action planning from a visual scene. Observed objects and a symbolic action model provide the constraints. A mask removes invalid candidates, then a mechanism that accounts for state and goal adjusts the probabilities of the remaining candidates. This provides an example of combining a hard constraint with contextual ranking. The result does not yet demonstrate the benefit of an IntelliSense integration for code.

This architecture deserves an entire series of its own: we will need to examine processor order, their state, the tokenizer, Roslyn's cost and how to convert a completion into a logits bias.

## IntelliSense can also propose what comes next

Another integration is even closer to human autocompletion. After `customer.`, IntelliSense could propose several tokens corresponding to `GetOutstandingAmountAsync()` instead of modifying their probabilities one by one.

The main model receives this sequence as a draft. It checks several tokens in one pass, accepts the prefix compatible with its own distribution and resumes generation at the first disagreement. This is the principle of speculative decoding.

[vLLM](https://docs.vllm.ai/en/v0.22.0/features/speculative_decoding/) currently exposes an experimental `custom proposer`. A custom class implements a `propose` method and supplies candidate tokens. IntelliSense could therefore become the proposal engine for code fragments it knows how to complete.

[llama.cpp](https://github.com/ggml-org/llama.cpp/blob/master/docs/speculative.md) also supports speculative decoding. Drafts can come from a small model, an n-gram cache or patterns found in text already produced. It does not document the same generic custom proposer interface, but the integration point is similar in nature.

This approach does not replace the sampler. The logits processor helps the model prefer a continuation. The proposer tries to guess several tokens ahead to accelerate their validation. IntelliSense could serve both purposes, with two different effects: guiding the choice or anticipating the sequence.

## The compiler can also intervene during generation

Access to the sampler is not the only way to exploit compiler knowledge. The preprint [Generative Compilation](https://arxiv.org/abs/2607.13921), published in July 2026, proposes checking Rust code before the program is complete.

Its mechanism transforms a partial program into a form the compiler can diagnose. It seeks to detect errors that are already inevitable without rejecting a prefix that could still be completed correctly. The authors evaluate this approach with open-weight models and frontier models accessed as black boxes.

This approach lets the compiler participate in generation even when the application cannot modify logits. It supplies intermediate diagnostics; it does not provide access to the sampler and does not replace the IntelliSense proposer considered here.

## Control over the sampler remains a limitation

This chain assumes that we control inference. With llama.cpp or vLLM, we can choose the grammar, add a logits processor and decide their order.

But many teams use a frontier model behind an API. They see neither the logits nor the sampler. They cannot plug IntelliSense or their own generation policy into it.

Before exploring samplers in detail, we must therefore answer a more immediate question: how far do frontier models actually let us constrain their output?

That is the topic of the final article.

---

## Sources

- [.NET Roslyn, Roslyn Overview](https://github.com/dotnet/roslyn/blob/main/docs/wiki/Roslyn-Overview.md)
- [Microsoft Learn, SemanticModel API](https://learn.microsoft.com/en-us/dotnet/api/microsoft.codeanalysis.semanticmodel?view=roslyn-dotnet-4.14.0)
- [llama.cpp, llama-server documentation](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)
- [vLLM, custom logits processors](https://docs.vllm.ai/en/stable/design/logits_processors/)
- [vLLM, speculative decoding and custom proposer](https://docs.vllm.ai/en/v0.22.0/features/speculative_decoding/)
- [llama.cpp, speculative decoding](https://github.com/ggml-org/llama.cpp/blob/master/docs/speculative.md)
- [Ma and Kordjamshidi, CLAMP: Constrained Decoding for Vision-Language Embodied Planning (preprint, September 2026)](https://arxiv.org/abs/2609.08602)
- [Mündler-Sasahara et al., Generative Compilation: On-the-Fly Compiler Feedback as AI Generates Code (preprint, July 2026)](https://arxiv.org/abs/2607.13921)
