---
title: "I Gave My JWT to My Agent. I Also Erased the Agent."
slug: "jwt-agent-efface-agent"
date: 2026-09-03
description: "Passing a user's JWT to an agent gives it an identity that is too broad and makes the real actor invisible in the logs."
categories: ["Artificial intelligence", "Security", "Software architecture"]
series: ["qui-donne-le-droit-d-agir-a-votre-agent-ia"]
series_order: 1
collection: "ARCHITECTURE"
cover: "/images/articles/01-j-ai-donne-mon-jwt-a-mon-agent.en.png"
draft: false
---
Alice is a clinician. She opens her business application and authenticates. Her
browser holds a JWT that allows her to view the patient records she is
authorized to access.

She now asks an agent:

> Prepare summaries for the patients I will see this afternoon.

The first integration seems almost obvious. The application passes Alice's token
to the agent. The agent can then call the same APIs as the user interface.

```text
Alice signs in
        ↓
the application receives her JWT
        ↓
it hands that JWT to the agent
        ↓
the agent calls the APIs as Alice
```

Everything works. That is precisely why the problem is likely to reach
production.

## A Narrow Task Receives a Broad Identity

The task assigned to the agent is limited. It concerns one clinic session, a
list of patients, and the preparation of summaries.

Alice's token knows nothing about any of that. It was designed for a full
interactive session:

```json
{
  "sub": "alice",
  "aud": "patient-api",
  "scope": "patient.read summary.write"
}
```

It expresses what Alice can do in the application. It does not express what
this task must do.

If Alice can view a thousand records as part of her work, the agent potentially
has the same scope. A poor tool selection, a hallucinated parameter, or a
hostile instruction hidden in a document can exploit all of that latitude.

Yet the JWT itself may be flawless. Its signature is valid. Its audience is
correct. It has not expired.

The cryptography correctly answers the question it was asked. The question
itself was too weak:

```text
Can Alice call this API?
```

The useful question was:

```text
can this agent perform this operation
for the specific task Alice has just assigned to it?
```

## In the Logs, Alice Does Everything

Suppose the agent reads the correct record, prepares the summary, and then
publishes it before the expected review.

Each time, the API receives:

```text
sub = alice
```

Its logs therefore say:

```text
14:02 Alice viewed record P-184
14:04 Alice created the summary
14:05 Alice published the summary
```

The last line is technically accurate and operationally misleading. Alice
asked for preparation. She did not choose the publishing tool, its parameters,
or the time of the call. The agent made those decisions.

After an incident, the log can no longer distinguish among four scenarios:
Alice published the summary herself, the agent misinterpreted the request, a
document hijacked its reasoning, or another component reused the Bearer token.

[RFC 6750](https://www.rfc-editor.org/rfc/rfc6750) highlights the fundamental
property of a Bearer token: the component that possesses it can use it. The
token does not prove that the hand triggering the call is still Alice's.

By passing her JWT to the agent, we did not merely pass along her permissions.
We erased the software exercising them.

## The Problem Is Not Limited to Auditing

If the agent and Alice share the same identity, applying different policies to
them becomes difficult.

We may want to allow Alice to approve a summary while limiting her agent to
preparation. We may want to revoke AgentSynthèse without ending Alice's session.
We may want to cap the number of records read by an automated task without
limiting normal use of the application.

With `sub = alice` everywhere, these distinctions arrive too late. As far as
the API is concerned, there is only one actor.

This confusion is often described as a traceability problem. It runs deeper
than that. A system cannot apply a rule to an entity it cannot name.

## First Rule: Never Confuse the Principal with the Agent

The design must preserve two answers:

```text
on whose behalf is the work performed?  Alice
who actually executes the calls?         AgentSynthèse
```

This still does not tell us what AgentSynthèse can do. We have not solved the
granularity of permissions, the workflow order, or human approval. But we have
discovered the first invariant:

> No agent should receive its user's raw token.

We need a delegation that preserves Alice as the source of authority and
AgentSynthèse as the actual actor.

Before building that delegation, another flaw in the initial design deserves
attention. By giving the agent access to the application's APIs, we also gave
it a freedom the user never had: the freedom to call the right actions in any
order.

That is the subject of the next article.

## Sources

- IETF, [RFC 6750: OAuth 2.0 Bearer Token Usage](https://www.rfc-editor.org/rfc/rfc6750)
- IETF, [RFC 7519: JSON Web Token](https://www.rfc-editor.org/rfc/rfc7519)
