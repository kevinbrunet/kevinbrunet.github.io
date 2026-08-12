---
title: "An agent's rights are an intersection, not a role"
slug: "droits-agent-intersection"
date: 2026-09-24
description: "An agent's effective permissions result from the intersection of the user, agent, delegation, task, and resource policies."
categories: ["Artificial intelligence", "Security", "Software architecture"]
series: ["qui-donne-le-droit-d-agir-a-votre-agent-ia"]
series_order: 4
collection: "ARCHITECTURE"
cover: "/images/articles/04-droits-agent-policy-intersection.en.png"
draft: false
---
We now know that AgentSynthèse is acting on Alice's behalf. Both identities are
visible.

What remains is to determine what this chain is actually allowed to do.

The standard RBAC reflex is to look for a role:

```text
Alice             → caregiver
AgentSynthèse     → clinical agent
```

Then permissions are added together or passed along. For a delegated agent,
that is precisely what must not be done.

## No actor should lend what another does not have

Consider four cases.

Alice can access patient P-184, but AgentSynthèse is not approved to handle
health data. The request must be denied.

AgentSynthèse is authorized to read records, but Alice cannot access P-184.
The request must be denied.

Alice and the agent both have read access, but Alice only requested a summary
of P-184. A request to read P-991 must be denied.

Finally, local policy may prohibit this use for a record subject to special
restrictions. The request must again be denied.

Effective authority therefore looks like this:

```text
effective_permissions =
    user_permissions
    ∩ agent_ceiling
    ∩ explicit_delegation
    ∩ task_requirements
    ∩ resource_policy
```

Each term can narrow the result. None can broaden it on its own.

Several recent efforts are beginning to formalize this logic as a *policy
intersection*: the final permission does not belong to any actor in isolation.
It exists only in the common subset of their policies.

## The intersection is starting to be spelled out

[RFC 8693](https://www.rfc-editor.org/rfc/rfc8693) supports token exchange and
the representation of the subject and actor. It does not define a universal
algorithm for intersecting rights. The resulting token depends on the
authorization server's policy.

More recent IETF work makes this rule explicit. The draft
[*Cross-Domain AuthZ Information Sharing for Agents*](https://datatracker.ietf.org/doc/draft-diaconu-agents-authz-info-sharing/),
published in February 2026, proposes calculating a recipient agent's rights as
the intersection of four sets:

```text
delegable scope of the parent agent
∩ intrinsic scope of the receiving agent
∩ explicit delegation for this invocation
∩ policy of the receiving domain
```

The document also requires the scope to either decrease or remain unchanged at
each delegation.

This is an Internet-Draft, so it is a work in progress rather than an
established standard. Still, it is noteworthy that this formula appears in a
document specifically about agents. It directly reflects the principle of
attenuable capabilities such as Macaroons and Biscuit, which the draft itself
cites as conceptual references.

This is not convergence on a format. It is convergence on an invariant:

> Delegation must never create power by addition.

## Why the agent's role is not enough

A role describes relatively stable authority. A task is far narrower and far
shorter-lived.

The `agent-clinique` role may indicate that AgentSynthèse is technically
authorized to handle certain health data. It does not prove that Alice asked it
to read P-184 today. Alice's rights likewise do not prove that this particular
agent is acceptable.

The agent must therefore not receive:

```text
Alice's permissions
```

or even:

```text
the permissions of the clinical-agent role
```

It must receive their intersection, narrowed by the task's mandate and the
API's policy.

## The authorization server can calculate this intersection

In an OAuth architecture, a central component collects the required elements
and issues a restricted token:

```text
Alice's token
+ AgentSynthèse's identity
+ consent
+ structured request
+ policy
        ↓
authorization server
        ↓
limited delegated token
```

[RFC 9396 on Rich Authorization Requests](https://www.rfc-editor.org/rfc/rfc9396)
makes it possible to express a request in a more structured form than a simple
scope string: action type, location, amount, or other domain-specific details.

This brings the token closer to the task. Security still depends on the quality
of the central policy and the data available when the token is issued.

If AgentSynthèse has a more powerful service account elsewhere, it can bypass
the carefully restricted token. If an endpoint still accepts Alice's general
JWT, the weaker path remains. The intersection must be a property of every
access path, not just the nominal flow.

## The limitation that intersection does not solve

When Alice starts the task, we may not yet know which patients are involved.

She asks:

> Prepare summaries for my appointments this afternoon.

The exact list will be provided by an initial API. Should the agent be given
access from the outset to every patient Alice might be able to see? That would
be too broad. Should it be given no access at all? Then the task cannot begin.

The authorization server can calculate an intersection based on the facts it
knows. The agentic workflow reveals new facts during execution.

This brings us to the next limitation: a task's authority cannot always be
fully calculated at the outset. It may need to evolve based on the responses
received.

## Sources

- IETF, [RFC 8693: OAuth 2.0 Token Exchange](https://www.rfc-editor.org/rfc/rfc8693)
- IETF Internet-Draft, [Cross-Domain AuthZ Information Sharing for Agents](https://datatracker.ietf.org/doc/draft-diaconu-agents-authz-info-sharing/), February 2026 version, an ongoing proposal rather than an established standard
- IETF, [RFC 9396: OAuth 2.0 Rich Authorization Requests](https://www.rfc-editor.org/rfc/rfc9396)
