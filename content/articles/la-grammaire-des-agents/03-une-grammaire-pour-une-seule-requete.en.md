---
title: "A grammar built for a single request"
slug: "a-grammar-built-for-a-single-request"
date: 2026-11-05
description: "Generate context and constraints from the actual schema, permissions and available capabilities."
categories: ["Artificial intelligence", "Software architecture"]
series: ["la-grammaire-des-agents"]
series_order: 3
collection: "ARCHITECTURE"
cover: "/images/articles/la-grammaire-des-agents/03-une-grammaire-pour-une-seule-requete.en.png"
draft: false
---

The agent's SQL grammar now guarantees that its response begins with `SELECT`. Yet, while searching for Camille Martin, it requests a `customer_addresses` table that does not exist. The database uses two separate tables, `customers` and `addresses`.

The query is syntactically valid. It remains impossible to execute, because the grammar describes SQL in general rather than this particular database.

The architectural leap is to build the constraint from the actual schema at request time, then discard it after use.

## From the general language to the actual context

A static grammar can usefully limit the output to `SELECT`, but the model can still invent a table, use a hidden column or join two entities without a relevant relationship.

At request time, the application knows much more: the database catalog, exposed views, the user's role, the current tenant, volume limits and permitted functions. It can compute a contract containing only this subset.

The model no longer receives “SQL.” It receives the SQL possible here and now.

## The grammar does not inform the model

We must distinguish two flows here.

The grammar is used by the decoding engine. It lets the engine remove tokens incompatible with the permitted tables and columns. But it is not necessarily part of the prompt. The model therefore does not read it as a description of the database.

The [llama.cpp documentation](https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md) makes this explicit for JSON Schema: the schema supplied to constrain output is not injected into the prompt. The model does not know its structure unless the application also presents it in its instructions. Tool definitions are a different case, because their schemas are generally added to the model's context.

If we provide only the dynamic SQL grammar, the resulting query will remain valid, but the prediction may be poor. The model computes probabilities without knowing the meaning of the available tables. The decoder then masks forbidden tokens and chooses among those that remain.

The selected token is therefore the best permitted choice, but it may have had a very low probability in the original distribution. The grammar guarantees output compliance. It does not give the model the knowledge needed to make a relevant choice.

To obtain a good decision, the system must therefore produce two artifacts from the same source:

```text
actual database schema
        ↓
context for the model
tables, columns, relationships, descriptions
        +
constraint for the decoder
permitted tokens and structures
```

The prompt guides probability towards the right query. The grammar prevents impossible queries from being emitted.

The two mechanisms do not replace each other. A description without a constraint remains advice the model can ignore. A constraint without a description closes doors without telling it which one leads to the expected result.

The same principle applies to an API. An OpenAPI document describes all public operations. The support agent may only have access to reading a record and adding a note. The generator turns these two capabilities into structured calls. A cancellation operation absent from the contract cannot be selected.

## An intersection of contributors

The dynamic grammar does not need to be produced by an omniscient component. It can result from several sets that narrow one another:

```text
product capabilities
∩ visible data
∩ user permissions
∩ agent mandate
∩ current state
= expressible decisions
```

Each contributor retains ownership of its knowledge. The catalog knows which columns exist. The authorization engine knows which are visible. The workflow knows which transitions begin from the current state. The agent's configuration knows which operations it has been entrusted with.

The generator assembles these constraints into a grammar. Depending on the engine, it may take the form of a JSON Schema, a list of choices, a formal grammar or a tool definition.

## One protection among others

As we saw in the [series on authentication and authorization](/en/series/qui-donne-le-droit-d-agir-a-votre-agent-ia/), protecting an agent relies on several mechanisms. A grammar replaces neither permissions, business validation nor checks at the execution point.

It helps obtain a usable response immediately. It avoids some exchanges between the system and the model, then reduces validation and correction work at the end of processing.

## The more precise the grammar, the sooner it becomes stale

Adding permitted tables and columns reduces incorrect queries. Adding the state of the record, Maya's rights and available values further narrows the generation space. But each detail also makes the grammar become stale sooner.

If the system must rebuild a complete grammar for every request, the preparation cost may eventually cancel out the gain from avoided errors. Conversely, a grammar that is too stable ignores part of the context and lets more incorrect outputs reach validation.

The current compromise often consists of caching a stable base, such as SQL syntax and the general schema, then recomputing only a smaller layer associated with the request. [XGrammar-2](https://arxiv.org/abs/2601.04426) offers reuse at the level of substructures through its `Cross-Grammar Cache`. Two different contracts can thus share part of the preparation work.

A [July 2026 preprint on decode-time grammars](https://arxiv.org/abs/2607.18357) explores another dimension: fragments instantiated during generation from the current environment. Declarations already produced can enrich this environment and determine which references are subsequently permitted. This direction remains experimental.

For now, we must therefore balance two costs: incorrect queries the grammar still allows and the barrier that must be rebuilt to prevent them.

## Limit the scope of action before the query

The grammar also protects the output flow. A SQL grammar limited to `SELECT` removes `DELETE`, `UPDATE` and `DROP` from the generation space. The model is not simply instructed to avoid them. It cannot formulate these queries.

The constraint can also remove sensitive tables and limit accessible columns. The agent's scope of action is reduced before its response reaches the database.

This mechanism replaces neither permissions nor server validation. It provides an additional barrier, particularly useful when an AI agent can act on a real system. Trust no longer rests solely on its ability to follow an instruction. Some dangerous actions become impossible to express.

We must now check whether this protection is worth its cost. The model still computes logits for its entire vocabulary, while the engine must compile the grammar, track the prefix state and filter tokens at each step.

The right question is therefore not merely: “Is the output valid?” We must measure the cost of obtaining a usable output, including compilation, decoding, validation, repairs and any retries.

That is what we will examine in the next article.

---

## Sources

- [llama.cpp, GBNF Guide](https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md)
- [vLLM, Structured Outputs](https://docs.vllm.ai/en/latest/features/structured_outputs/)
- [Li et al., XGrammar-2: Dynamic and Efficient Structured Generation Engine for Agentic LLMs (2026)](https://arxiv.org/abs/2601.04426)
- [Zhang et al., Decode-Time Grammars: Constrained LLM Generation over a Refinement Order of Grammar Fragments (preprint, July 2026)](https://arxiv.org/abs/2607.18357)
