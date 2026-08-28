---
title: "You Do Not Always Know the Right Permissions at the Start of a Task"
slug: "permissions-decouvertes-pendant-tache"
date: 2026-09-03
description: "A task sometimes discovers its scope while it is running: authority must be able to evolve without becoming a master key."
categories: ["Artificial intelligence", "Security", "Software architecture"]
series: ["qui-donne-le-droit-d-agir-a-votre-agent-ia"]
series_order: 5
collection: "ARCHITECTURE"
cover: "/images/articles/05-permissions-decouvertes-pendant-la-tache.en.png"
draft: false
---
Alice asks:

> Prepare the summaries for my consultations this afternoon.

At this point, the agent does not know any patient identifiers. It must begin
by calling:

```text
list_patients(consultation = "2026-07-25-pm")
```

The response contains:

```text
P-184
P-207
P-311
```

These three identifiers change the task. Before the response, the agent was
allowed to search for the consultation. After the response, it must be able to
read three specific records.

The required authority has just changed.

## The initial token dilemma

We can issue a very broad token at the outset:

```text
patient.read
```

The agent will always find the records it needs. It will also be able to try to
read many others.

Alternatively, we can create an authorization limited to known identifiers.
But there are none yet.

The problem does not arise from a lack of precision in the prompt. It occurs in
every task where an initial step discovers the resources needed by subsequent
steps:

```text
search for patients, then open their records
list anomalous invoices, then download their supporting documents
find a service's incidents, then inspect their logs
identify the affected repositories, then prepare changes
```

A fully static authorization forces a choice between two flaws: too much power
at the outset, or a round trip to a central server after every discovery.

## The response must be able to modify the future

The interesting idea is to stop treating an API response as mere data.

The consultation service is precisely the component that knows which patients
belong to the requested consultation. Its response can therefore provide two
things:

```text
the identifiers the model needs
+ evidence that subsequent APIs can use
```

Conceptually:

```json
{
  "patients": ["P-184", "P-207", "P-311"],
  "authorization_evidence": "<signed evidence>"
}
```

The model reads the list. The authorization layer uses the evidence.

The records service can then accept P-184, P-207, and P-311, but reject P-999.
The agent has not received a general `patient.read` scope. It has received the
authorized continuation of a specific step.

## Is this really "adding permissions"?

Yes, from the task's perspective: before the call, it could not open P-184;
after the response, it can.

But we must avoid dangerous wording. The agent does not grant itself new
permissions. A service already recognized as an authority produces a signed
fact, and another service has decided in advance to trust that type of fact.

The new authority therefore comes from the intersection of:

```text
Alice's initial mandate
∩ AgentSynthèse's policy
∩ the consultation service's signed result
∩ the records service's local policy
```

Here again, we find the intersection. New evidence does not replace the
previous limits. It satisfies a condition that was missing.

## A JWT could carry this evidence

This architecture does not necessarily require Biscuit. The service can ask the
authorization server to reissue a JWT limited to the three patients. It can
issue separate capabilities for each patient. It can store the list in a
server-side session and return only an opaque identifier.

These options are valid. They have one thing in common: a central component or
the business service must reconstruct a new credential after each step.

The challenge grows when the task branches:

```text
one agent finds the patients
another extracts the documents
a third prepares the summaries
a fourth checks for inconsistencies
```

Each subagent must receive less authority than its predecessor while still
benefiting from legitimate facts discovered by the services.

## What we are looking for now

We need an object that can carry:

```text
the initial mandate
the accumulated restrictions
the discovered resources
the origin of each fact
evidence signed by different services
```

And we must prevent the agent from adding:

```text
patient_accessible("P-999")
```

itself, as though this assertion came from the consultation service.

This distinction between "a block added by the holder" and "a block signed by
a recognized authority" is central to Biscuit.

The next article introduces the mechanism without discussing workflows yet. We
will first see how a token can carry a policy while ensuring that an ordinary
holder can only restrict it.

## Sources

- IETF, [RFC 9396: OAuth 2.0 Rich Authorization Requests](https://www.rfc-editor.org/rfc/rfc9396), used here to contextualize structured authorization requests
- Eclipse Biscuit, [Specifications](https://doc.biscuitsec.org/reference/specifications), source for the third-party block and signature mechanism introduced in the next article
