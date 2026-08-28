---
title: "Sometimes the Right Policy Is: 'This Agent Cannot Call This API'"
slug: "api-interdite-agent-humain"
date: 2026-09-03
description: "Delegated human approval and a strictly human-only endpoint create two different security boundaries."
categories: ["Artificial intelligence", "Security", "Software architecture"]
series: ["qui-donne-le-droit-d-agir-a-votre-agent-ia"]
series_order: 9
collection: "ARCHITECTURE"
cover: "/images/articles/09-api-interdite-agent-et-humain.en.png"
draft: false
---
AgentSynthèse has prepared a draft. It followed the workflow in order. The data
comes from the correct records, and every step has its evidence.

Only the action that actually commits the system remains.

Should we allow the agent to execute it after human approval, or require the
human to call the final API directly?

These two approaches are often conflated under the term *human in the loop*.
They do not provide the same guarantee.

## First model: the human authorizes, the agent executes

The agent prepares an exact action:

```json
{
  "action": "publish_summary",
  "patient": "P-184",
  "draft": "draft:991",
  "version": 3,
  "content_hash": "sha256:..."
}
```

The approval service presents this content to Alice. After she decides, it
produces a signed block:

```datalog
approved(
  "alice",
  "publish_summary",
  "draft:991",
  3,
  "sha256:..."
);
```

The publication policy trusts the approval service's key. AgentSynthèse can
then call the API, but only for the action, version, and content that were
actually approved.

If the agent changes the text after the click, the hash no longer matches. If
it changes the patient, the evidence no longer matches. If it waits too long,
the attestation may expire.

In this model, the human makes the decision and the agent performs the
technical call.

## Second model: the API is human-only

For some actions, the organization may want a stronger boundary:

```text
direct actor = agent  → deny
direct actor = authenticated human → policy evaluation
```

The agent may prepare the information, explain the choice, and open the correct
screen. It never receives the capability to perform the final act.

The policy could state:

```datalog
deny if
  operation("finalize_clinical_decision"),
  actor_type("agent");

allow if
  operation("finalize_clinical_decision"),
  actor_type("human"),
  recent_user_verification(true);
```

Here, no approval attestation turns AgentSynthèse into a human. Alice must
perform a new authenticated act.

This distinction prevents a common sleight of hand: keeping the agent as the
actual actor while recording in the log that "the human approved it."

## A missing policy is not a final denial

When the agent attempts an action subject to approval, the service may respond:

```json
{
  "error": "human_approval_required",
  "action_hash": "sha256:...",
  "approval_service": "/human-approvals",
  "required_approver_role": "clinician",
  "expires_in": 300
}
```

The denial directs the agent to the only path that can produce the missing
evidence.

The approval service does not give it a general `summary.publish` permission.
It provides a narrow attestation for a frozen action.

Here again, the response opens the next step:

```text
final API denies
        ↓
the agent requests the human service
        ↓
the human reviews an exact action
        ↓
the service returns signed evidence
        ↓
the same action becomes eligible for authorization
```

## A human click is not magic evidence

An agent can control an already open session. A "Validate" button that is
clicked automatically does not constitute effective oversight.

For a sensitive action, the service may require recent authentication, user
verification, or proof of presence. The [W3C WebAuthn
standard](https://www.w3.org/TR/webauthn-3/) distinguishes, in particular,
between user presence and user verification. Using them does not prove that the
human decision was sound, but it strengthens the attribution of the act.

The screen design matters as well. The human must see the exact effect, the
origin of the data, the proposed changes, and any relevant uncertainties. A
generic approval for a task that can still change provides no protection.

## Regulation does not choose your protocol

[Article 14 of the European AI
Act](https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX%3A32024R1689)
requires high-risk systems within its scope to include measures that enable
effective oversight by natural persons, proportionate to the risks, level of
autonomy, and context.

A Biscuit block, a passkey, or a human-only endpoint is not enough to establish
compliance. These mechanisms can, however, implement a boundary chosen by the
organization and produce stronger audit trails than a simple instruction:
"the AI prepares, the human approves."

In a medical context, the policy must also fit the framework applicable to the
device, its intended purpose, and the clinical process. Technology does not
replace risk analysis.

## Three models instead of a switch

Not every API needs the same boundary.

```text
1. human or agent
   low-impact reads and computations

2. agent under delegation and, where required, approval
   reversible writes or precisely bounded actions

3. human only
   decision or action that the organization refuses to delegate
```

This classification is not merely an attribute of the agent. It belongs to
each operation.

The same AgentSynthèse can read a document, save a draft after intersecting
policies, publish a version after approval, and be formally denied access to a
final clinical decision.

This is a long way from giving Alice's JWT to the model. The final article will
assemble the complete path and show what this architecture actually solves, as
well as what it leaves unchanged.

## Sources

- European Union, [Regulation (EU) 2024/1689, Article 14: human oversight](https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX%3A32024R1689)
- W3C, [Web Authentication: An API for accessing Public Key Credentials, Level 3](https://www.w3.org/TR/webauthn-3/), used for the concepts of user presence and user verification
- Eclipse Biscuit, [Specifications: third-party blocks](https://doc.biscuitsec.org/reference/specifications)
