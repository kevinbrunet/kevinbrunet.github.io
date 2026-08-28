---
title: "An agent should not act as Alice. It should act for Alice."
slug: "agent-agit-pour-alice"
date: 2026-09-03
description: "Safe delegation maintains distinct identities for the user granting the mandate and the agent executing it."
categories: ["Artificial intelligence", "Security", "Software architecture"]
series: ["qui-donne-le-droit-d-agir-a-votre-agent-ia"]
series_order: 3
collection: "ARCHITECTURE"
cover: "/images/articles/03-agent-agit-pour-alice.en.png"
draft: false
---
The first setup gave Alice's JWT to AgentSynthèse. The APIs therefore saw only
Alice.

We now need to maintain two identities:

```text
Alice            = the origin of the mandate
AgentSynthèse    = the software that selects and executes calls
```

This change may seem administrative. Yet it transforms the decisions the
system can make.

## "As Alice" and "for Alice" describe two architectures

When the agent uses Alice's token directly, it acts as her. This is known as
impersonation. From the API's perspective, Alice and her agent are
interchangeable.

With delegation, AgentSynthèse authenticates using its own identity and
presents a mandate from Alice:

```text
Alice requests a task
        ↓
AgentSynthèse authenticates as AgentSynthèse
        ↓
a delegated token indicates that it is acting for Alice
```

[RFC 8693 on OAuth Token Exchange](https://www.rfc-editor.org/rfc/rfc8693)
provides useful building blocks. The `subject_token` represents the subject on
whose behalf authority is requested. The `actor_token` can represent the
delegated actor. In the issued token, the `act` claim can retain the current
actor:

```json
{
  "sub": "alice",
  "act": {
    "sub": "agent-synthese"
  },
  "aud": "patient-api",
  "scope": "patient.read"
}
```

The API can now ask a question that did not exist before:

> Can AgentSynthèse read this record for Alice?

## The agent's identity becomes policy data

Alice may be authorized to publish directly. AgentSynthèse may be restricted
to preparation.

A second agent may be given a different limit. An experimental agent may be
allowed to access test data and denied access in production. An agent
specialized in summarization may read text, while a billing agent can access
only coded procedures.

The distinction also improves operations:

```text
which actions did Alice perform directly?
which actions came from AgentSynthèse?
which agent should be revoked after an incident?
how many records did an automated task examine?
```

Making the agent visible does not grant any rights. It gives the system a new
dimension to which it can apply its rules.

## Consent must also name the agent

Recent work on agentic authorization makes this distinction more explicit.

The IETF draft
[*On-Behalf-Of User Authorization for AI Agents*](https://www.ietf.org/archive/id/draft-oauth-ai-agents-on-behalf-of-user-00.html)
proposed that a user consent to delegation to an agent identified by
`requested_agent`. The agent had its own credentials, and the final token
preserved the separation between user and actor.

This draft has expired. It is not a standard on which to base promises of
interoperability. It remains relevant because it illustrates how the problem
has shifted: consent no longer applies only to an application and a few
scopes. It applies to a named agent that will act for a user.

## A new token at every boundary

Consider the following path:

```text
Alice
  ↓
AgentSynthèse
  ↓
Consultation service
  ↓
Patient records API
```

Passing the same token all the way to the final service creates a master key
all over again. A token intended for the consultation service should not be
accepted by the records API.

Token exchange makes it possible to change the audience at every boundary,
shorten the lifetime, and preserve the delegation chain. Each service receives
a credential intended for its own role in the task.

This architecture greatly improves attribution. Yet it does not resolve the
central question of permissions.

## Two valid identities can still produce too much power

Our delegated token still contains:

```text
scope = patient.read
```

Alice has the right to read the record. AgentSynthèse is correctly identified.
The delegation is valid.

But is AgentSynthèse authorized to read every patient visible to Alice, or only
those involved in the consultation? Did Alice actually delegate publication,
or only preparation? Does the API's local policy allow this agent to access
this type of record?

Delegation answers "who is acting for whom?". By itself, it does not calculate
effective authority.

The next step is the idea that is beginning to appear in several lines of work
on agents: rights should no longer be inherited from the last actor. They
should be the intersection of every limit in the chain.

## Sources

- IETF, [RFC 8693: OAuth 2.0 Token Exchange](https://www.rfc-editor.org/rfc/rfc8693)
- IETF Internet-Draft, [On-Behalf-Of User Authorization for AI Agents](https://www.ietf.org/archive/id/draft-oauth-ai-agents-on-behalf-of-user-00.html), expired draft cited as a direction for ongoing work, not as a standard
