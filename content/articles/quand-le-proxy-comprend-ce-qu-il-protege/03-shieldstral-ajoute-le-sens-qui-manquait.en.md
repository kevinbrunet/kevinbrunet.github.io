---
title: "Shieldstral adds a local classifier driven by business policy"
slug: "shieldstral-local-business-policy-classifier"
date: 2026-10-01
description: "A specialized 3-billion-parameter classifier evaluates content locally against a safety question defined by the company."
categories: ["Artificial intelligence", "Cybersecurity", "Software architecture"]
series: ["quand-le-proxy-comprend-ce-qu-il-protege"]
series_order: 3
collection: "SYSTEMS"
cover: "/images/articles/shieldstral/03.en.png"
draft: false
---

{{< callout variant="scene" label="Starting point" >}}
Nora's proxy knows she is requesting a frontier model. It also recognizes an IBAN, an email address, and certain API keys. It still does not know that three paragraphs in her file describe industrial know-how forbidden at that destination.
{{< /callout >}}

Shieldstral adds precisely that perspective to the configuration studied here.

Gateways can already integrate semantic controls. LiteLLM, for example, offers an LLM judge with custom criteria. This mechanism lets administrators ask the question; its effectiveness depends on the model chosen and how it is evaluated. The integration's documentation does not provide a comparative benchmark on the Atlas project's business secrets.

Shieldstral is interesting because the model is trained specifically to compare content against a safety question. Mistral's paper reports an average F1 of 84.9% on text benchmarks and 91.3% on its policy adaptation evaluation. These are published results supporting this specialized 3-billion-parameter classifier, rather than proof of superiority over every possible general-purpose judge.

Instead of locking every rule into a taxonomy chosen before training, it receives a safety question together with the content to examine. Business policy becomes a model input.

## Policy becomes a question asked of the document

For the fictional Atlas project, the company can formulate the following rule:

> Does this content describe protected parameters of the Atlas process, including temperature stages, a cooling rate, or their sequence, which must not be sent to an external provider?

[Shieldstral](https://arxiv.org/abs/2607.25857) receives this question together with the document. It evaluates both and produces a binary answer with a continuous score derived from the probabilities of `yes` and `no`.

This formulation changes the rule creation process. The company does not need to anticipate every sentence that could express a temperature, a production rate, or a manufacturing sequence. It must, however, name the class of information being sought.

In the proof of concept, the ten documents unresolved by pattern filtering were submitted to this semantic question. Shieldstral assigns a score; the proxy then compares it against policy thresholds to allow, transform, redirect, or block the request.

That is the significant advance: business policy becomes executable before the document is sent. The proxy no longer only looks for a known form. It can check whether a text describes specific know-how, even if it contains neither the word “secret” nor the expected vocabulary.

## Distinguishing two texts that look alike

Consider two documents containing temperatures and a rate:

```text
Document A: several temperature stages and a cooling rate
            describe the Atlas industrial process.

Document B: several temperatures and a wind speed
            describe the weather forecast.
```

A pattern filter sees numbers and units in both texts. An overly broad rule blocks both. An overly narrow rule lets the Atlas process through as soon as its wording changes.

Shieldstral evaluates another question: does the document describe protected parameters of the Atlas process? The proxy can then treat document A as a business secret and allow document B through.

This is the benefit of the added control: among the ten documents patterns could not resolve, the proxy now has a signal related to their meaning. The decision engine can allow ordinary content, request a transformation, designate a local model, or block transmission according to company policy.

```text
before: recognized form or no decision
after: meaning evaluated against a business rule
```

## The result holds on a set expanded to fourteen documents

The first campaign contained 11 documents: six sensitive and five allowed. After the deterministic blocking of the API key, Shieldstral evaluated the remaining ten.

The set now includes three additional sensitive cases designed to exercise the intermediate band where the proxy attempts a transformation rather than blocking. In this expanded run, the complete pipeline flagged all nine sensitive documents and correctly allowed all five non-sensitive documents. Recall therefore remains 100%, with 0% observed false positives on this small set. Decision latency reaches 44 ms at the 95th percentile.

```text
9 sensitive documents     → 9 flagged
5 non-sensitive documents → 5 allowed
14 cases                  → p95 latency: 44 ms
1 case                    → no Shieldstral call
```

These figures describe decisions made by the complete pipeline, which includes the deterministic filter; they are not Shieldstral-only recall. They show the intended benefit: sensitive content that patterns do not recognize can now trigger a safety decision. They do not establish readiness for production: fourteen cases remain an exploratory set.

A legal team can ask about specific contract clauses. A research team can protect results before publication. Another policy may depend on the destination: a complete document is allowed to reach a local model but prohibited from reaching an external API.

## Control stays within the company

Shieldstral has 3 billion parameters according to Mistral's published paper. That size makes local execution more feasible than with a large general-purpose frontier model.

Its placement is essential:

```text
Nora's application
        ↓
enterprise AI proxy
        ↓
deterministic checks
        ↓
local Shieldstral + business policy
        ↓
allowed destination
```

The document is evaluated before leaving the infrastructure. The external provider is not asked to decide, after receipt, whether the data should have been transmitted. The company's proxy retains control of the question, threshold, and destination.

Mistral's published benchmark contains a `Trade Secrets` category. Shieldstral achieves an F1 score of 92.1% on it in the authors' fine-grained evaluation. Trade secrets are therefore among the risks for which the model has explicitly been evaluated.

## Deterministic rules do not disappear

Shieldstral does not replace Presidio, regular expressions, or classification labels. An IBAN still has a form that is simpler and more reliable to detect with a specialized tool. A structurally forbidden destination does not need a probabilistic score.

The proxy gains two complementary perspectives:

```text
known pattern: a locatable fact
Shieldstral policy: a semantic relationship
decision engine: an allowed action
```

Deterministic checks come first. Shieldstral is called when form alone is insufficient to apply business policy. The decision engine then turns the score into permission, blocking, or a request for different processing.

This division avoids entrusting all security to a probabilistic model. It also limits cost and latency by reserving semantic analysis for content and policies that need it.

## Detection is not pseudonymization

This capability provides a probabilistic detection signal; it does not solve the entire processing pipeline. Shieldstral can conclude that a document contains protected know-how, but it does not necessarily provide the exact location of every sensitive passage.

This difference is invisible in a binary demonstration:

```text
Question: does the document contain protected Atlas process parameters?
Answer: yes, with a score sent to the decision engine
```

It becomes decisive when Nora wants to continue with the frontier model. The proxy cannot cleanly replace a secret with a pseudonym if it does not know which characters or sentences make up that secret.

Pseudonymizing an IBAN is straightforward because the detector returns its boundaries. Pseudonymizing a business procedure first requires isolating it without deleting the whole document.

Shieldstral therefore does not become the pseudonymization engine, router, or policy owner. It provides a local semantic signal. The surrounding architecture retains the other responsibilities.

## The proxy gains a control it did not have

In our initial configuration, the proxy mainly recognized formats and predefined categories. With Shieldstral, it can connect a document's meaning to a rule written by the company before any external transmission. A team can evolve that rule by describing more precisely what it protects, without rebuilding a classifier for each new business secret.

The mechanism remains probabilistic: an imprecise question produces an imprecise boundary, and thresholds must be evaluated on representative cases. The final article will show how to measure them and improve the policy.

This capability leads directly to the next stage: to turn the signal into pseudonymization, the proxy must split the text, retain positions, and ask Shieldstral which segments match the policy.

Localization is the next step in the architecture.

---

{{< closing-question label="Takeaway" >}}
Shieldstral provides a local semantic signal. The decision engine remains responsible for the action and destination.
{{< /closing-question >}}

## Sources

- [Shieldstral evaluation report — September 2, 2026](/documents/shieldstral-qualification-2026-09-02.en.md)
- [Mistral AI — Shieldstral](https://arxiv.org/abs/2607.25857)
- [Microsoft — Presidio](https://microsoft.github.io/presidio/)

**Continue reading:** [Redacting a secret without a fixed format: does the proxy still preserve the task?](/en/articles/shieldstral-business-secret-redaction/).
