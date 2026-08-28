---
title: "The interface enforced a workflow without saying so"
slug: "interface-protegeait-workflow"
date: 2026-09-03
description: "By calling APIs directly, an agent can bypass the order of actions that the interface silently imposed on the user."
categories: ["Artificial intelligence", "Security", "Software architecture"]
series: ["qui-donne-le-droit-d-agir-a-votre-agent-ia"]
series_order: 2
collection: "ARCHITECTURE"
cover: "/images/articles/02-interface-protegeait-le-workflow.en.png"
draft: false
---
In Alice's application, preparing a summary followed a simple workflow:

```text
open the consultation
        ->
display the patient list
        ->
open a patient record
        ->
prepare a draft
        ->
request a review
        ->
publish
```

No one called this a security policy. It was "how the screen worked."

Yet the interface imposed constraints. The Publish button did not appear before
the review. The patient record had to come from the open consultation. The draft
had to exist before it could be approved.

Then we exposed the same actions to the agent:

```text
list_patients
read_patient
create_draft
request_review
publish_summary
```

For the model, these are no longer the steps in a workflow. They are five
independent tools.

## The same actions, in the wrong order

The agent can call `publish_summary` before `request_review`. It can retain a
patient identifier obtained in an earlier conversation. It can retry an
operation with a different parameter after a refusal.

Each call may appear valid when considered in isolation:

```text
Alice is allowed to read patient records
Alice is allowed to create drafts
Alice is allowed to publish
```

And yet the complete sequence is invalid.

The problem arises because traditional authorization often considers one
request at a time:

```text
actor + action + resource -> permit or deny
```

The workflow adds another dimension:

```text
actor + action + resource + state reached -> permit or deny
```

`publish_summary` is not a prohibited action. It is an action that is prohibited
now, until a valid review exists.

## The interface was not the rule

We could ask the agent to follow the manual:

> Always list the patients before opening a patient record. Always request a
> review before publishing.

This instruction is useful for guiding the model. It is not the guarantee.

A prompt can be forgotten, contradicted, or misinterpreted. Another agent can
call the API directly. A new interface can ignore the convention. An attacker
will probably not use the screen.

OWASP devotes a category in its API ranking to
[insufficiently protected sensitive business flows](https://owasp.org/API-Security/editions/2023/en/0xa6-unrestricted-access-to-sensitive-business-flows/).
The key point goes beyond the automated fraud described in those examples: a
legitimate operation is not necessarily legitimate at every point in the
process.

If order matters, the rule must live behind the interface, at the boundary that
produces the effect.

We agree that best practices require this kind of precaution, but throughout my
career I have often seen APIs that did not meet this constraint. Often enough
that it seemed essential to revisit the subject in this article, because an
agent unleashed on poorly designed APIs can wreak havoc in a company.

## A refusal must teach the next step

Moving the rule into the API does not mean responding with an opaque
`403 Forbidden`.

An agent needs an actionable error:

```json
{
  "error": "workflow_order_violation",
  "current_state": "draft_created",
  "required_state": "review_approved",
  "allowed_next_action": "request_review",
  "rule": "A summary must be reviewed before publication."
}
```

The API refuses the request and describes the permitted path forward. The same
rule then supports security, orchestration, and explanation.

This reflects a broader transformation: the business rule should no longer be
written only in a wiki that the model is expected to have read. It can be
compiled into the service and surface at the exact moment an attempt violates
it. We will return to this idea in another series.

## A state machine is still not enough

We could store this on the server side:

```text
task-7841 = review_approved
```

Then check that state before publication. This is a perfectly valid solution.
However, it becomes more complex when the workflow crosses multiple services,
multiple organizations, or multiple subagents.

Who owns the state? How does service B know that service A really completed the
previous step? How do we prevent a task identifier from being reused in another
context? How do we transmit the proof without giving every service direct access
to the same central database?

We will not answer these questions just yet. First, we are missing a more
fundamental piece of information.

In the previous examples, every API still sees only Alice. Even an excellent
state machine cannot distinguish a publication made directly by Alice from one
chosen by her agent.

The next step is therefore to make the delegate visible: the agent must no
longer act as Alice, but for Alice.

## Sources

- OWASP, [API6:2023: Unrestricted Access to Sensitive Business Flows](https://owasp.org/API-Security/editions/2023/en/0xa6-unrestricted-access-to-sensitive-business-flows/)
