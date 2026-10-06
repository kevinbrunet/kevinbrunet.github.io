---
title: "Banning AI fuels shadow IT"
slug: "ai-proxy-shadow-it-official-path"
date: 2026-11-10
description: "A useful, explainable official path helps limit workarounds. An API proxy only covers uses that pass through it."
categories: ["Artificial intelligence", "Cybersecurity", "Software architecture"]
tags: ["ai-security", "ai-risk-governance"]
series: ["quand-le-proxy-comprend-ce-qu-il-protege"]
series_order: 6
collection: "SYSTEMS"
cover: "/images/articles/shieldstral/06.en.png"
draft: false
---

{{< callout variant="scene" label="Starting point" >}}
Nora wants to summarize a file before her meeting. The official tool blocks her chosen model and only displays: “This request violates the security policy.”
{{< /callout >}}

She can give up. She can also open a public service in her personal browser and upload the document, or photograph it with her smartphone and send the image from a personal account.

The second path is much more dangerous than the first. Yet sometimes the prohibition itself made it more likely.

A security policy that ignores the need to work does not eliminate that need. It shifts it into shadow IT.

## Shadow IT rarely starts with malicious intent

The UK's [National Cyber Security Centre](https://www.ncsc.gov.uk/guidance/shadow-it) defines shadow IT as assets used professionally without being known to, or aligned with, the organization's processes. Its definition explicitly includes unauthorized AI technologies, often called shadow AI.

The NCSC emphasizes that these uses rarely result from a desire to bypass security to cause harm. Employees are generally trying to finish their work with official tools that are too slow, incomplete, or unsuitable. They may also not understand the risk created by a personal service.

Nora's case follows this mechanism exactly. She is not trying to exfiltrate an industrial procedure. She wants a summary before a meeting. If the company only gives her a prohibition, a legitimate need remains unmet.

Blocking access to a few domains does not solve the problem permanently. Services change, models become integrated into existing software, and a personal phone can sometimes bypass the information system.

## The proxy must preserve a practical way to work

The architecture described in this series protects the boundary without reducing every incident to a refusal.

The AI proxy centralizes destinations. A specialized engine pseudonymizes recognizable data. Shieldstral compares the meaning of the content against business policy. Segmentation helps isolate sensitive passages. A synthetic response can then present Nora with the remaining permitted paths without calling the requested model.

The message becomes:

> This document contains an internal industrial procedure. The requested external model cannot receive the complete version. You can pseudonymize the relevant passages, use the local model, or cancel.

The expanded proof of concept flagged all 9 sensitive documents and allowed all 5 non-sensitive documents. It produced a local destination decision for a secret without a deterministic form and redacted three cases before rechecking. The median decision took 20 ms, with a 95th percentile of 44 ms; rechecking added 17 to 20 ms. These measurements on short documents cover neither summary generation nor the interactive loop described here.

Security stays firm about the forbidden destination. It becomes flexible about how the work can be done.

That difference matters. Nora should not need to know data center locations, every provider's contractual terms, or Shieldstral's taxonomy. The system translates those constraints into understandable, usable options.

## The API proxy protects uses that pass through it

A request sent from a personal account or through another path escapes this control point. Protecting web usage requires complementary measures and support for users.

Local routing does not constitute user consent either. LiteLLM already offers sensitive data routing based on patterns; Shieldstral adds the semantic signal studied here. After a local turn, the history may still contain the secret. Subsequent turns must be rechecked, and the permitted destination retained for as long as that context remains.

## An explanation is better than an error code

Every proxy intervention can become an opportunity to build awareness. Nora learns that an IBAN is pseudonymized, that a business procedure cannot be detected like a card number, and that a local model can receive a document refused by an external destination.

She also sees the consequences of her choice. Pseudonymization can degrade a summary if the replaced passage was necessary. A local model offers greater protection for the document, but may provide a different experience. Cancellation remains possible.

This guidance should not become a mandatory lesson with every request. A short explanation at the moment of decision directly connects the risk to the action. It gives the user a mental model she can reuse next time.

The proxy does more than enforce policy. It makes it visible and understandable.

## Blocking becomes a source of improvement

Nora's choices also provide valuable information to the company. If many users redirect the same task to the local model, the external tool may not suit that business domain. If everyone rejects proposed pseudonymization, segmentation may remove too much context. If a team repeatedly encounters the same rule, the policy may be poorly explained or too broad.

These traces should be aggregated without turning security into individual surveillance. They can help improve local models, clarify policies, and add official paths where real needs emerge.

The NCSC specifically recommends avoiding unnecessary restrictions, responding promptly to user requests, and developing a culture where problems can be reported without fear of punishment. A poor culture makes shadow IT less visible and therefore harder to secure.

## An informed user is another line of defense

Saying that strong security relies on a trained user does not mean shifting all responsibility onto that person. Nora will never replace access controls, encryption, the proxy, or structural prohibitions. Even an experienced user can make mistakes under pressure.

A sound architecture combines both forms of protection. Technical controls prevent forbidden paths. Explanations help users understand the risk and choose correctly among permitted paths.

This combination changes perceptions. Cybersecurity becomes the system that enables people to work with AI while retaining control of their data.

The series' conclusion rests on this idea: to combat shadow AI, the company must offer more than a prohibition. It must provide a safe path, explain its decisions, and listen to the needs revealed by workarounds.

An informed user then becomes an additional defense because they have the information, tools, and choices needed to act with understanding.

That experience nevertheless depends on a decision invisible to Nora: how the policy was written. In my first run, two out of six sensitive documents were not flagged. The final article opens the proof of concept to explain how the same model went from 67% to 100% recall without increasing observed false positives.

---

{{< closing-question label="Takeaway" >}}
A useful control protects the boundary and preserves a way to work. Explanations reinforce technical protections.
{{< /closing-question >}}

## Sources

- [Shieldstral evaluation report — September 2, 2026](/documents/shieldstral-qualification-2026-09-02.en.md)
- [NCSC — Shadow IT](https://www.ncsc.gov.uk/guidance/shadow-it)
- [NCSC — Using SaaS securely](https://www.ncsc.gov.uk/collection/cloud/using-cloud-services-securely/using-saas-securely)
- [ANSSI — Security recommendations for generative AI systems](https://messervices.cyber.gouv.fr/guides/recommandations-de-securite-pour-un-systeme-dia-generative)
- [LiteLLM — Sensitive Data Routing](https://docs.litellm.ai/docs/proxy/guardrails/sensitive_data_routing)

**Continue reading:** [With the same model, recall increased from 67% to 100%](/en/articles/shieldstral-policy-recall-evaluation/).
