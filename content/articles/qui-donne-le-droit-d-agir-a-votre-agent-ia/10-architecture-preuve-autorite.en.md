---
title: "In the end, the agent no longer has a role. It builds proof of authority."
slug: "architecture-preuve-autorite"
date: 2026-09-03
description: "Identity, policy intersection, capabilities, and signed proofs combine to form progressive, verifiable, and revocable authority."
categories: ["Artificial intelligence", "Security", "Software architecture"]
tags: ["ai-security", "software-architecture"]
series: ["qui-donne-le-droit-d-agir-a-votre-agent-ia"]
series_order: 10
collection: "ARCHITECTURE"
cover: "/images/articles/10-architecture-preuve-autorite.en.png"
draft: false
---
We started with the simplest arrangement:

```text
Alice gives her JWT to AgentSynthèse
```

We end up with a very different architecture:

```text
the agent has its own identity
the task receives a narrow mandate
each delegation reduces authority
APIs add signed facts to their responses
the next step requires evidence of the previous one
a sensitive action requires exact approval
some APIs always deny agents
```

This progression is not the story of a token evolving. It is the story of the
transition from static access control to an authority protocol.

## Before: having the right role

The traditional model asks:

```text
Does Alice have the role that allows patient.read?
```

The agent then inherits the token or a service account. Its rights are known
before the task begins and remain broadly stable throughout its execution.

This model works for predefined workflows. It becomes fragile when the software
selects its own tools, creates subtasks, and discovers the resources it needs as
it proceeds.

## After: presenting the proofs that make this call legitimate

When the API receives a request, it can verify:

```text
Is Alice authorized for this resource?
Is AgentSynthèse approved for this operation?
Did Alice actually delegate this task?
Does the resource come from a legitimate step?
Are all subtask restrictions satisfied?
Was the correct version reviewed?
Does the human approval cover this exact effect?
does the local policy still accept the whole set?
```

Authority is no longer contained in a single `scope` field. It results from
the intersection of multiple policies and multiple proofs.

## Two mechanisms converge

The first approach extends OAuth and JWT. The authorization server knows the
user, the agent, the consent, and the policy. It computes a reduced scope and
reissues a token.

IETF drafts focused on agents are now exploring multi-hop delegation,
structured capabilities, and monotonic reduction. The
[*Cross-Domain AuthZ Information Sharing for Agents*](https://datatracker.ietf.org/doc/draft-diaconu-agents-authz-info-sharing/)
draft explicitly defines an intersection formula involving the parent's
delegable scope, the recipient's intrinsic scope, the explicit delegation, and
the receiving domain's policy.

The second approach is based on attenuable capabilities. With Biscuit, the
holder can add restrictions offline but cannot remove existing ones. Trusted
services can also sign third-party blocks whose facts will be accepted by
certain policies.

The two approaches can be combined:

```text
OAuth / JWT
    user identity
    agent identity
    consent and organizational boundary
                  ↓
issue an initial Biscuit capability
                  ↓
Biscuit
    task restrictions
    attenuation toward subagents
    evidence signed by APIs
    workflow preconditions
                  ↓
local authorizer
    fresh facts
    resource policy
    final allow or deny
```

JWT explains who is acting on whose behalf. Biscuit can carry what this task is
still allowed to do and what it has legitimately accomplished.

## The token becomes a useful history, not a complete log

It would be tempting to add every observation to the Biscuit. That would be a
mistake.

The token should carry the facts required for subsequent decisions, not the
entire conversation. A list of thousands of patients, clinical content, or
detailed traces have no place in a Bearer token that will circulate among
services.

It can carry:

```text
a result identifier
a version hash
a short attestation
an expiration time
a delegation reference
```

Large or sensitive data can remain behind the APIs.

## The five points where the architecture can still fail

The first is bypass. If a secondary API still accepts Alice's general-purpose
JWT, all the sophisticated policies on the primary path become optional.

The second is freshness. A signed proof can remain cryptographically valid
after a business-level revocation. Volatile facts require short-lived tokens,
introspection, a revocation list, or an online check.

The third is trust between keys. A policy that trusts too many services
recreates global authority. Each type of fact must have a legitimate issuer and
a clear audience.

The fourth is complexity. Rules need tests, versions, explanation tools, and
governance. Moving a rule from code to a policy language does not automatically
make it correct.

The fifth is the data produced. Perfect authorization for every read does not
guarantee that a synthesis will not reveal sensitive information through
combination. Authorization bounds operations. It does not validate every model
inference.

## What this architecture changes nonetheless

It moves security outside the agent's probabilistic reasoning.

The model may select the wrong tool. The API rejects the call if the proof is
missing.

The model may try to skip the review. Publication requires the signed block
from the review service.

The model may invent a patient identifier. The service accepts only patients
attested for this task.

The model may request a prohibited action. The response directs it to a human,
or the policy permanently closes that path to agentic actors.

We no longer ask AI to guard its own freedom.

## The task becomes the true unit of authorization

The starting point of this series was a user with a role.

The endpoint is a task that accumulates proofs:

```text
Alice's mandate
∩ AgentSynthèse's identity
∩ delegation restrictions
∩ patients actually listed
∩ versions actually read
∩ steps actually completed
∩ approval obtained where required
∩ current API policy
```

Such an architecture does not eliminate identity, OAuth, or roles. It places
them within a richer calculation.

The fundamental shift can be expressed in one sentence:

> An agent should not arrive at an API with its user's general permission. It
> should arrive with proof that this call is the authorized continuation of
> this task.

## Sources

- IETF, [RFC 8693: OAuth 2.0 Token Exchange](https://www.rfc-editor.org/rfc/rfc8693)
- IETF Internet-Draft, [Cross-Domain AuthZ Information Sharing for Agents](https://datatracker.ietf.org/doc/draft-diaconu-agents-authz-info-sharing/), a working document and not an established standard
- Eclipse Foundation, [Eclipse Biscuit project](https://projects.eclipse.org/projects/technology.biscuit)
- Eclipse Biscuit, [Specifications](https://doc.biscuitsec.org/reference/specifications)
- Eclipse Biscuit, [Authorization Policies](https://doc.biscuitsec.org/getting-started/authorization-policies)
