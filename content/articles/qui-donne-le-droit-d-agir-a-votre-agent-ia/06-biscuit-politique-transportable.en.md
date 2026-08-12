---
title: "Biscuit turns a token into portable policy"
slug: "biscuit-politique-transportable"
date: 2026-10-08
description: "Biscuit tokens carry facts, rules, and restrictions with the task, while leaving each API with the final say."
categories: ["Artificial intelligence", "Security", "Software architecture"]
series: ["qui-donne-le-droit-d-agir-a-votre-agent-ia"]
series_order: 6
collection: "ARCHITECTURE"
cover: "/images/articles/06-biscuit-politique-transportable.en.png"
draft: false
---
A JWT generally carries claims:

```text
sub = alice
act = agent-synthese
scope = patient.read
```

Biscuit can carry facts and restrictions interpreted by a logic language:

```datalog
user("alice");
agent("agent-synthese");
right("consultation:2026-07-25-pm", "list_patients");
```

This is more than a difference in syntax. The token can evolve as it travels,
and each origin has a distinct level of trust.

## A token made of blocks

A Biscuit starts with an authority block signed by the issuer. This block defines
the base facts and rules.

The holder can then add a block:

```datalog
check if operation("list_patients");
check if consultation("2026-07-25-pm");
check if time($t), $t < 2026-07-25T18:00:00Z;
```

These checks narrow how the token can be used. For a call to be accepted,
all accumulated checks must succeed.

The list of blocks is protected by a signature chain. Removing or modifying
a block invalidates the proof. The holder can therefore create a narrower
derived token without possessing the root private key.

The [Eclipse Biscuit documentation](https://doc.biscuitsec.org/getting-started/introduction)
calls this property offline attenuation.

## The service retains the final say

The token does not decide on its own.

During a call, the API adds facts that it knows:

```datalog
resource("consultation:2026-07-25-pm");
operation("list_patients");
time(2026-07-25T13:58:00Z);
```

Its *authorizer* then applies the local rules:

```datalog
allow if
  resource($r),
  operation($op),
  right($r, $op);

deny if true;
```

The checks contained in the token are cumulative. The `allow` and `deny`
policies remain on the application side. According to the
[Biscuit authorization policies documentation](https://doc.biscuitsec.org/getting-started/authorization-policies),
a token can add restrictions, but only the application defines the policy that
ultimately approves it.

This separation is essential. The agent carries a capability. The API remains
sovereign over its resources.

## A block can contain facts, rules, and checks

Adding a block does not necessarily mean adding a permission. Biscuit distinguishes several types of statements.

A **fact** asserts that a piece of information is true:

```datalog
right("consultation:2026-07-25-pm", "list_patients");
document_type("clinical_note");
```

A **rule** makes it possible to derive new facts from existing facts:

```datalog
can_read($document) <-
  assigned_document($document),
  document_type($document, "clinical_note");
```

A **check** asserts nothing. It imposes a condition on the use of the token:

```datalog
check if operation("read_document");
check if time($t), $t < 2026-07-25T14:30:00Z;
```

All checks accumulated across the different blocks must succeed. Adding a check therefore does not create the `read_document` right. It only means that the token can be used for this operation, provided that a corresponding right already exists.

Biscuit then examines the origin of the statements. Each fact and each rule remains associated with the block that introduced it. The authorizer can then decide which origins it accepts when making its decision:

- the authority block signed by the issuer
- the facts provided by the authorizer itself
- a block signed by a recognized third party
- or, if the policy explicitly provides for it, other blocks.

This distinction between **nature** and **origin** is essential:

```text
syntax indicates what the statement does
provenance indicates whether the authorizer can trust it.
```

A holder can therefore write a new fact in an ordinary block. But it cannot force the authorizer to use that fact to grant it a right.

Conversely, a check added by the holder is always an additional condition. It can make the token less powerful or even unusable, but it can never give the token more authority.


## Why the agent cannot write its own rights

The signature chain guarantees the integrity and order of the blocks.

Trust and scope rules then determine which origins the authorizer accepts for each decision.

A holder can therefore add:

```datalog
right("patient:P-999", "read");
```

This fact will indeed be present in the token and protected by the cryptographic chain. But its origin remains a block added by the agent.

If the authorization policy trusts only the authority block and the facts provided by the API, it will not take this new right into account.

The agent can write an assertion, but it cannot decide that the API must believe it.

Biscuit associates facts with their block of origin. By default, authorizer policies trust facts from the authority block and facts provided by the authorizer itself. They do not trust arbitrary facts added to an ordinary block unless specifically authorized to do so.

The fraudulent block can be cryptographically valid and logically useless.

However, `check if` statements added to an ordinary block are additional conditions that the token imposes on its own use. They cannot alter the list of rules already issued.

## Attenuation is well suited to sub-agents

With this additive-only block principle, AgentSynthèse can receive a capability that applies to the consultation. Before passing it to AgentExtracteur, it adds, or has a specific authorizer add:

```datalog
check if operation("read_document");
check if document_type("clinical_note");
check if time($t), $t < 2026-07-25T14:30:00Z;
```

AgentExtracteur receives only the derived token. It cannot remove these conditions.

If it creates a subtask itself, it can add another restriction. The architecture thus supports paths that were not known when the root token was issued.

Each link in the chain can pass on less authority without having to contact the issuer again.

## Biscuit performs an intersection within the object

In the OAuth architecture presented earlier, a server computes the intersection
and reissues a token.

With Biscuit, part of the intersection is materialized in the chain:

```text
initial authority
∩ check added by the orchestrator
∩ check added by the sub-agent
∩ request facts
∩ local API policy
```

The two approaches are not at odds. OAuth can establish who is acting for whom
and issue the initial capability. Biscuit can carry restrictions specific to
the task and its subtasks.

## The lesser-known feature: third-party blocks

So far, each added block could only restrict the token.

The specification also provides for *third-party blocks*. An external service
can sign a block intended for a specific token. The authorizer can choose to
trust facts originating from that public key.

This mechanism brings us back to the patient list problem.
The consultation service can attest:

```datalog
listed_patient("task:7841", "P-184");
listed_patient("task:7841", "P-207");
listed_patient("task:7841", "P-311");
```

These facts come from neither the agent nor the initial issuer. They come from a
recognized API, after an actual step in the workflow.

The next article shows how an API response can thus open up new authority
without turning the token into a self-signed permission.

## Sources

- Eclipse Foundation, [Eclipse Biscuit project](https://projects.eclipse.org/projects/technology.biscuit), an Incubating project
- Eclipse Biscuit, [Introduction](https://doc.biscuitsec.org/getting-started/introduction)
- Eclipse Biscuit, [Authorization Policies](https://doc.biscuitsec.org/getting-started/authorization-policies)
- Eclipse Biscuit, [Specifications](https://doc.biscuitsec.org/reference/specifications)
