---
title: "Ten out of eleven documents pass the pattern filter"
slug: "ai-proxy-pattern-filter-limits"
date: 2026-11-10
description: "On the prototype's initial eleven cases, the deterministic filter blocks an API key and leaves five other sensitive documents for further analysis."
categories: ["Artificial intelligence", "Cybersecurity", "Software architecture"]
tags: ["ai-security"]
series: ["quand-le-proxy-comprend-ce-qu-il-protege"]
series_order: 2
collection: "SYSTEMS"
cover: "/images/articles/shieldstral/02.en.png"
draft: false
---

{{< callout variant="scene" label="Starting point" >}}
Nora's LiteLLM proxy knows her project, the requested model, and the request's destination. It can now perform an initial check before any external call: look for secrets with a recognizable form.
{{< /callout >}}

An API key often has a characteristic prefix. An IBAN follows a structure. An email address or phone number can be located in text. These cases do not require understanding Nora's business domain.

## The first layer looks for patterns

To measure what it actually protects, I prepared 11 documents: six contained sensitive information and five could be transmitted. I first submitted them to a deterministic check looking for known patterns.

This check recognized and blocked an API key. The other ten documents passed the filter. Yet five of them were sensitive: two descriptions of the Atlas process, a business secret without numbers, an inducement to financial fraud, and an identifiable medical record.

```text
11 documents
    ↓ pattern check
1 API key blocked
10 documents passed to the next stage
    ├── 5 allowed
    └── 5 sensitive
```

{{< callout variant="key" label="What the measurement covers" >}}
These figures describe the prototype's limited detector. They do not measure the performance of all DLP engines or of Presidio, which combines several methods, including entity recognition models.
{{< /callout >}}

The filter therefore made a conclusive decision in one out of eleven cases. Used alone, it would not have prevented five sensitive documents from reaching an external provider.

This initial campaign explains the article's title. The proof of concept was later expanded to 14 documents to test semantic redaction and rechecking. The finding at this first stage remains the same: the API key is still the only case stopped without calling Shieldstral; the other 13 reach semantic analysis.

## What can be located can be pseudonymized

An engine such as Presidio can recognize certain entities and replace them with pseudonyms:

```text
Original: Nora's account is FR76 3000 6000 0112 3456 7890 189
External: <PERSON_1>'s account is <IBAN_1>
```

The frontier model receives a usable sentence without seeing the original values. The proxy keeps the mapping locally and, if the architecture supports it, can restore the pseudonyms in the response delivered to an authorized user.

This protection remains essential. When a pattern is sufficient to apply the rule, it is preferable to retain that deterministic check. Recognizing an entity does not always establish whether it may be transmitted, however. Most sensitive cases in the test set did not have a form that the initial filter could recognize.

## A document can be sensitive without an obvious pattern

Nora's file belongs to the fictional Atlas project. It describes an industrial sequence, several temperatures, and a cooling rate. No individual element is secret. The same numbers could appear in a weather report or a maintenance table.

What is protected is their combination within a specific procedure. Company policy prohibits transmitting that know-how to an external system.

The proxy can extract numbers. It can know that the destination is an external provider. It does not automatically connect this passage to the concept of industrial know-how defined by the company.

Adding “confidential,” “process,” or “internal” to a list does not solve the problem. A document can avoid those words. The same list can also block ordinary texts that use them without revealing a secret.

## The next protection must evaluate meaning

The prototype configuration sits in the right place, but it still lacks a capability: comparing a document's meaning against a business policy.

This is where Shieldstral enters the architecture. The company describes in natural language what it wants to protect, and the model evaluates that question on the ten documents the first filter could not resolve.

The next article shows what Shieldstral actually adds, how the policy becomes a question asked of the document, and why this new layer does not replace deterministic checks.

---

{{< closing-question label="Takeaway" >}}
Patterns protect secrets recognizable by their form. Business secrets also require an evaluation of the content.
{{< /closing-question >}}

## Sources

- [Shieldstral evaluation report — September 2, 2026](/documents/shieldstral-qualification-2026-09-02.en.md)
- [Microsoft — Presidio](https://microsoft.github.io/presidio/)

**Continue reading:** [Shieldstral adds a local classifier driven by business policy](/en/articles/shieldstral-local-business-policy-classifier/).
