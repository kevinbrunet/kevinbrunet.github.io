---
title: "The workflow can become a chain of evidence"
slug: "workflow-chaine-de-preuves"
date: 2026-09-03
description: "When every call requires evidence from the previous one, the system enforces the workflow order without relying on the agent's compliance."
categories: ["Artificial intelligence", "Security", "Software architecture"]
tags: ["ai-security", "software-architecture"]
series: ["qui-donne-le-droit-d-agir-a-votre-agent-ia"]
series_order: 8
collection: "ARCHITECTURE"
cover: "/images/articles/08-workflow-chaine-de-preuves.en.png"
draft: false
---
At the beginning of this series, the interface enforced this sequence:

```text
list the patients
        ↓
open a record
        ↓
create a draft
        ↓
obtain a review
        ↓
publish
```

When we gave the APIs to the agent, these steps became independent tools. The
model could call the right actions in the wrong order.

Signed responses now make it possible to reconstruct that constraint without
returning to a rigid interface.

## Each step provides the evidence required by the next

The query service returns a signed block:

```datalog
patients_listed("task:7841", "result:42");
```

The records service accepts a read only if this signed result contains the
requested patient. After the read, it returns in turn:

```datalog
record_read("task:7841", "P-184", "version:7");
```

The draft service requires this evidence before accepting `create_draft`. It
then signs:

```datalog
draft_created("task:7841", "draft:991", "input-version:7");
```

The review service requires the draft. The publishing service requires a
review of the same version.

```text
list evidence
      ↓
read evidence
      ↓
draft evidence
      ↓
review evidence
      ↓
authorization to publish
```

The agent can still decide when to call the tools. It can no longer fabricate
the state required for the next step.

## The order no longer lives in the prompt

We can continue to write in the instructions:

> Always have a summary reviewed before publishing it.

This sentence helps the model plan. The guarantee lies elsewhere:

```datalog
allow if
  operation("publish"),
  resource("draft:991"),
  reviewed("draft:991", "version:3")
  trusting <review-service-key>;
```

Without evidence of a review, the API refuses the request. A prompt injection
can persuade the agent that the review is unnecessary. It cannot sign on
behalf of the review service.

The policy becomes a distributed state machine with proven transitions.

## The cryptographic detail that makes the order credible

A simple certificate stating "the review was completed" can be copied to
another task or associated with a modified draft.

The evidence must therefore bind:

```text
the task identifier
the exact resource
its version or hash
the previous step
the next audience
an expiration time
```

In Biscuit, a third-party block request contains the context of the token's
previous signature. According to the
[specification](https://doc.biscuitsec.org/reference/specifications), the
external signature is thus attached to a specific Biscuit. To build a
sequential chain, the request sent to the next service is generated after the
previous block has been added.

The append-only structure does not by itself prove that a business process was
executed correctly. It provides the foundation for chaining attestations that
each service signs after performing its own verification.

## A refusal becomes a proposed transition

If AgentSynthèse attempts to publish too early, the API can respond:

```json
{
  "error": "missing_authorization_evidence",
  "missing_fact": "reviewed(draft:991, version:3)",
  "allowed_next_action": "request_review",
  "approval_endpoint": "/reviews"
}
```

This error does not ask the model to memorize general documentation. It
presents the rule at the moment of the violation and identifies the permitted
transition.

The policy therefore does more than close a door. It exposes the graph of the
next legitimate moves.

## The workflow can branch

A state machine does not have to be linear.

After a record has been read, the policy can allow:

```text
extract allergies
or
prepare the summary
or
request a missing document
```

It can then require certain evidence to be assembled before proceeding:

```datalog
allow if
  operation("request_review"),
  draft_created($draft, $version),
  allergies_checked($patient, $source_version),
  based_on($draft, $source_version);
```

The logic describes preconditions, not a single script. The agent retains
freedom within the permitted space.

This is precisely what the traditional interface struggled to do. It often
enforced a single path because representing several was costly. A declarative
policy can allow multiple paths while prohibiting dangerous shortcuts.

## This mechanism does not eliminate all state

Some properties cannot be guaranteed by a self-contained token.

If a piece of evidence must be consumed only once, the service must record its
use. If a review is revoked, verifiers must learn about that revocation. If two
agents work concurrently on the same version, concurrency must be managed. If
the record changes after the review, its hash or version number must make the
previous evidence unusable.

The workflow carried by the evidence therefore does not replace transactions,
idempotency, or concurrency control. Its primary benefit is preventing
progress from relying on the model's goodwill.

## The next step is not always automatic

We now know how to enforce:

```text
list before read
read before draft
review before publication
```

But who produces the review evidence?

In some cases, another automated service is enough. In others, the rule
requires a human decision.

Two architectures are then possible. The human can sign an approval that
authorizes the agent to perform a specific effect. Alternatively, the final
API can formally reject any agentic actor and require a direct human call.

This distinction is the final leap in the series.

## Sources

- Eclipse Biscuit, [Specifications: signature chain and third-party blocks](https://doc.biscuitsec.org/reference/specifications)
- OWASP, [API6:2023: Unrestricted Access to Sensitive Business Flows](https://owasp.org/API-Security/editions/2023/en/0xa6-unrestricted-access-to-sensitive-business-flows/)
