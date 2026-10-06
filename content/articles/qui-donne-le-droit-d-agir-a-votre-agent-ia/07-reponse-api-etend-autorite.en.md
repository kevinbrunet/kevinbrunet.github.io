---
title: "An API response can precisely enable the next step"
slug: "reponse-api-etend-autorite"
date: 2026-09-03
description: "An API can sign proof of its result to authorize exactly the resources discovered in the next step."
categories: ["Artificial intelligence", "Security", "Software architecture"]
tags: ["ai-security"]
series: ["qui-donne-le-droit-d-agir-a-votre-agent-ia"]
series_order: 7
collection: "ARCHITECTURE"
cover: "/images/articles/07-reponse-api-etend-autorite.en.png"
draft: false
---
AgentSynthèse initially has a narrow permission:

```text
list the patients for this afternoon's consultation
```

It has no general permission to read patient records.

The consultation service responds:

```json
{
  "patients": ["P-184", "P-207", "P-311"],
  "authorization_block": "<signed block>"
}
```

The first field is intended for the agent's work. The second is intended for
downstream services.

This response has just changed what the task can do.

## The service attests to what it has just revealed

The signed block can contain:

```datalog
listed_patient("task:7841", "P-184");
listed_patient("task:7841", "P-207");
listed_patient("task:7841", "P-311");
```

The holder adds this block to the Biscuit. The specification binds the third
party's signature to the relevant token through the cryptographic context of
its chain. The block therefore cannot be freely moved to any other Biscuit.

When the agent calls:

```text
GET /patients/P-184
```

the records service applies a rule equivalent to:

```datalog
allow if
  task("task:7841"),
  resource("patient:P-184"),
  listed_patient("task:7841", "P-184")
  trusting <consultation-service-key>;
```

The exact syntax depends on the implementation and the chosen vocabulary. The
important property is the origin of the fact: the records service accepts
`listed_patient` only when it comes from a block signed by the consultation
service.

If the agent adds this itself:

```datalog
listed_patient("task:7841", "P-999");
```

the policy does not trust it. P-999 remains inaccessible.

## The permission does not come from the data alone

It would be dangerous to conclude:

> Because the agent knows a patient identifier, it can open the record.

An identifier is not a capability. It may come from a log, an earlier
conversation, or a hallucination.

Authority emerges only when several conditions intersect:

```text
the initial mandate allows this consultation
∩ AgentSynthèse is approved for this task
∩ the consultation service signed this patient
∩ the token still applies to task:7841
∩ the record policy accepts this evidence
```

We therefore do not replace the intersection with an "added permission." We
add a trusted fact to the existing intersection.

## The response can return a complete token or a block

Two implementation approaches are possible.

The service can return a new Biscuit that has already been extended. This is
simple for the client, but the service must receive and manipulate the token.

It can also return a *third-party block*. The holder first generates a request
bound to its Biscuit. The service signs the content without needing to know the
entire token, and the holder then adds the returned block. This is the flow
described in the
[Biscuit specification](https://doc.biscuitsec.org/reference/specifications).

In both cases, the response carries proof that can be used later.

## One proof does not grant every permission

The signed block attests only that P-184 was included in this afternoon's consultation. This proof does not automatically grant access to the patient's entire record.

The token already contains a precise mandate:

```text
prepare the summary for this afternoon's consultation
```

The records service then verifies that the requested operation remains within the limits of this mandate. For example, it may agree to return:

```text
the patient's identity
and the clinical summary needed to prepare for the consultation
```

but refuse:

```text
the complete medical history
administrative documents
data unrelated to this consultation
```

Authorization therefore results from the combination of several elements:

```text
the token authorizes preparation for this consultation
the consultation service attests that P-184 is included
the request concerns the data covered by this mandate
the token is presented to the service authorized to receive it
the token is still valid
```

Responsibilities remain separate. The consultation service can certify which patients are concerned. It cannot, however, broaden the initial mandate or decide that the agent may read their entire records.

The records service retains the final decision:

```text
the evidence states:
"P-184 is part of the relevant consultation"

the mandate specifies:
"the agent is preparing the summary for this consultation"

the policy concludes:
"P-184's clinical summary may be returned,
but not the complete record"
```

This separation limits the risk of a *confused deputy*. An API with broad access to records must not exercise all its powers at the agent's request. It performs only the operation permitted by both the initial mandate and the proof received.


## Proofs must remain narrow

A list response can contain many patients. Copying it into a token without any
limit creates size, confidentiality, and revocation issues.

Imagine that the API returns a list of 5,000 patients.
The 5,000 identifiers could be added to the token, but this would create three problems:
- the token would become very large
- anyone who obtained the token would discover these identifiers
- a list embedded in a token remains usable until it expires, even if it becomes incorrect in the meantime


Depending on the situation, better options may include:

```text
A separate capability per patient: issue a distinct authorization only for the patient the agent needs to access.
A signed identifier for a materialized result: keep the list on the server and place only a signed identifier such as result:R-42 in the token.
A predicate for a consultation: state "patient participating in consultation C-17" instead of copying every patient. The service then checks whether P-184 belongs to C-17.
A very short-lived block: place a few identifiers in the evidence, but make it valid for only a few minutes.
An opaque reference verified online: place a reference that reveals nothing in the token, then ask the server to verify it at access time.
```

The token is not intended to become a portable database.

The proof must also be bound to the task, an audience, a duration, and sometimes
the exact hash of the request.


In Biscuit, these limits can be expressed through facts and checks concerning, for example, the destination service, the resource, the operation, and the time of the request.

The block signed by a third party is also cryptographically bound to the Biscuit for which it was produced. It therefore cannot be freely transferred to another token.

The application can add two separate protections.

The first restricts the proof to a specific call. A fingerprint is then computed from the significant elements of the request:

```text
HTTP method
+ receiving service
+ route
+ parameters
+ request body, if any
```

The service recomputes this fingerprint when it receives the request. If the method, route, or request content has changed, the proof is rejected.

The second avoids exposing the patient identifier in clear text in the proof. The block can contain a fingerprint of the identifier rather than its value:

```text
patient_ref(<fingerprint of "P-184">)
```

At access time, the service computes the fingerprint of the requested identifier and verifies that it matches the one contained in the proof.

If the identifiers are short or predictable, a simple hash is not enough to conceal them effectively. A fingerprint computed with a secret key, such as an HMAC, or an opaque reference generated by the service is preferable.

These two mechanisms are additional application-level protections. Biscuit can carry the facts and checks needed to verify them, but it does not automatically compute these fingerprints.

## A new way to think about APIs

Until now, an API received authorization and returned data.

It can now return:

```text
data
+ evidence of the completed step
+ the authority strictly required to continue
```

Beyond providing access to discovered resources, this idea also makes it possible to record each completed step.
The next step therefore waits for the proof supplied by the previous one.
The workflow itself can become verifiable.

The agent remains free to reason and choose its tools. But it can no longer
produce effects in an order that the services have not authorized.

## Sources

- Eclipse Biscuit, [Specifications: third-party blocks and trust scopes](https://doc.biscuitsec.org/reference/specifications)
- Eclipse Biscuit, [Datalog reference: block scoping](https://doc.biscuitsec.org/reference/datalog.html)
