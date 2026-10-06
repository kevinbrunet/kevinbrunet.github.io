---
title: "With the same model, recall increased from 67% to 100%"
slug: "shieldstral-policy-recall-evaluation"
date: 2026-11-10
description: "On the exploratory set, clarifying the policy fixes two leaks. These results still require an independent, representative evaluation."
categories: ["Artificial intelligence", "Cybersecurity", "Software architecture"]
tags: ["ai-security", "ai-evaluation-evals"]
series: ["quand-le-proxy-comprend-ce-qu-il-protege"]
series_order: 7
collection: "SYSTEMS"
cover: "/images/articles/shieldstral/07.en.png"
draft: false
---

{{< callout variant="scene" label="Starting point" >}}
My Shieldstral proxy was working. That was precisely the problem.
{{< /callout >}}

It blocked explicit secrets. It allowed ordinary documents. It also detected identifiable medical information. Yet two out of six sensitive documents still passed the check.

Recall reached 67%. The false positive rate was zero. A quick reading might have focused only on that second figure and declared the test encouraging.

Instead, I examined the two leaks.

## An initial campaign of eleven cases

The evaluation set contained 11 documents: 6 expected to be sensitive and 5 expected to be non-sensitive. It covered three domains: Atlas for industry, financial compliance, and medical information.

The Atlas cases contrasted an explicit procedure, a paraphrase of the same process, temperatures without a procedure, isolated values, a public result, and a secret without numbers. The set added an API key, general financial advice, a specific inducement to fraud, identifiable medical information, and an anonymous medical text.

The proxy first ran a deterministic detector. The API key was blocked at this stage without calling the model. The other ten documents were sent to Shieldstral with a policy question. The proxy's engine could turn the score into permission, redaction, local redirection, or blocking.

This first campaign only exercised three paths: permission to use the frontier model, blocking, and redirection to the local model. No document entered the redaction branch followed by a recheck. The complete pipeline was only tested with the three cases added later.

That separation matters. Shieldstral produced a score. The proxy retained the decision and path.

## Paraphrasing was not the real problem

The explicit Atlas procedure was detected correctly. Its paraphrase scored only 0.037 with the official BF16 weights. In finance, the inducement to conceal funds scored 0.223. Both scores remained below the intervention thresholds.

I first suspected language. Translating the Atlas paraphrase from French into English only raised its score from 0.037 to 0.107.

I then added a warning to the policy that documents might paraphrase to evade detection. The score remained at 0.023.

These two experiments were insufficient to attribute the failure to language. The generic warning about evasion did not correct it either.

The problem was in the question.

## “Industrial procedure” remained too abstract

The first Atlas policy asked whether the document described a detailed industrial procedure or internal know-how. The category seemed relevant. Yet it remained too far removed from the elements observable in the text.

I replaced it with a question naming the classes of parameters being sought: temperature stages, cooling rate, and the combination of those steps.

The document did not change. The model did not change. The threshold did not change. The paraphrase's score rose from 0.037 to 0.967.

The negative control containing temperatures without a process remained at 0.001. The added precision therefore did not turn every temperature into a secret on this set.

I observed the same shift in finance. When the policy named structuring transfers below a threshold and using shell companies, the sensitive case's score rose from 0.223 to 0.994. General financial advice remained at 0.000.

## Policy is part of performance

After this rewrite, all 6 sensitive documents were flagged and all 5 non-sensitive documents correctly allowed. Recall rose from 67% to 100%. The observed false positive rate remained at 0%.

| Measure on the initial 11 cases | Initial policy | Clarified policy |
|---|---|---|
| Sensitive documents flagged by the pipeline | 4 out of 6 | 6 out of 6 |
| Pipeline recall | 67% | 100% |
| Observed false positives | 0 out of 5 | 0 out of 5 |

The pipeline includes the API key blocked without Shieldstral. These results measure safety decisions on the observed set, rather than guaranteeing the absence of leaks in use.

The classification from this first campaign was reproduced with official BF16 weights served by vLLM and with a community GGUF Q8_0 quantization. On the initial GGUF run, median latency for the ten model calls was 20 ms and the 95th percentile was 31 ms.

The most important result is neither the 100% nor the latency. It is the difference achieved without modifying the model.

A security policy is more than legal text turned into a question. It becomes an executable specification. It must connect risk to business objects actually observable in the document.

For Atlas, “protect industrial know-how” expresses intent. “Look for temperature stages and a cooling rate forming a manufacturing sequence” gives the control something concrete to identify in the content.

## Three new cases test the next step

The set was then expanded from 11 to 14 documents. The three new cases are sensitive but less explicit: financial transaction splitting described without directly mentioning money laundering, a partial Atlas setting buried in a report, and a medical file identifiable from initials and context.

They were chosen to reach the band where the proxy attempts redaction. The expanded set therefore contains 9 sensitive and 5 non-sensitive documents. The pipeline retains 100% recall and no false positives were observed.

```text
14 documents
    ├── 9 out of 9 sensitive documents flagged
    ├── 5 out of 5 non-sensitive documents allowed
    └── 1 Shieldstral call avoided by the deterministic filter
```

This extension primarily revealed a new blind spot. A sensitive passage scoring 0.42 when evaluated alone dropped to 0.003 when buried in a neutral document. The policy could be precise and the model able to recognize the passage, yet a single call on the complete document diluted the signal.

The proxy now evaluates overlapping chunks before making its decision and retains the score of the most sensitive chunk. This correction has a cost proportional to document length: a short text produces only one chunk, while a long document requires several calls.

In the new run, decision latency remains 20 ms at the 50th percentile and reaches 44 ms at the 95th percentile. The three redactions then required an additional recheck of 17 to 20 ms.

## What these figures do not prove

{{< callout variant="alert" label="An exploratory result" >}}
Fourteen cases do not constitute production qualification. The specific policies were written after observing the documents that failed. The three new cases were themselves calibrated to exercise the redaction branch. The result exercises a pipeline and reveals its flaws; it does not yet measure generalization.
{{< /callout >}}

At a minimum, a held-out set is needed, with more formulations for each risk, long documents, adversarial cases, and examples using the company's real vocabulary. I propose at least 50 labeled examples as the next exploratory step before reconsidering the thresholds of 0.35, 0.60, and 0.85. This number is neither a standard nor proof of production qualification: the size and composition must depend on the risks and acceptable level of leakage.

Redaction must also be evaluated beyond its recheck alone. In the three new cases, it removes between 99% and 100% of the document. The recheck no longer flags sensitive content, but that does not prove the absence of leaks. Too little material remains to demonstrate that the task is still feasible.

One path is to replace this mechanical removal with rewriting by a local LLM. It would receive the complete document and be tasked with removing critical information while retaining useful context. The resulting version would then be submitted to Shieldstral again and could reach the frontier model only if it passed that recheck.

The proxy can also return control to the user who initiated the call. Instead of silently modifying the text, it explains that some elements cannot be transmitted and asks for a new version. Nora often knows better than the system what can be removed without distorting her need. Her rewrite passes through exactly the same controls before any external transmission.

The two approaches are complementary. Local rewriting automates the transformation; user rewriting preserves control over meaning and avoids letting a model decide alone what is incidental. In both cases, rechecking remains mandatory.

Automatic rewriting does not remove the need for evaluation. The LLM may retain the secret in another form, remove too much information, or invent information. It nevertheless offers an interesting path toward a genuinely usable document where chunk-based redaction currently erases almost everything. These branches still need to be added and measured in the proof of concept.

The conclusion remains useful for designing the system. Evaluating only the model is insufficient. The model-policy pair must be evaluated, while retaining deterministic controls and routing around it.

The series' final rule becomes: the proxy understands what it protects only when policy translates risk into objects the classifier can actually look for.

## The next experiment: Jev

The benchmark presented here was conducted between late August and early September 2026. [Jev, TypeSafe AI's decision model](https://typesafe.ai/blog/introducing-system-one-models-and-jev), was not yet publicly available: its early-access launch was on September 15.

Its approach opens another avenue for this kind of architecture: asking questions of content and receiving structured decisions that software can use directly. I look forward to testing it in this context with the same business policies and documents, to measure what it detects, what it misses, and the cost of its decisions. Shieldstral already provides interesting results; Jev will be an opportunity to continue the experiment and compare approaches on concrete cases.

{{< closing-question label="Takeaway" >}}
Policy is part of performance. The model, question, thresholds, and effects of the decision on the task must all be evaluated.
{{< /closing-question >}}

## Sources

- [Shieldstral evaluation report — September 2, 2026](/documents/shieldstral-qualification-2026-09-02.en.md)
- [Mistral AI — Shieldstral](https://arxiv.org/html/2607.25857v2)
- [TypeSafe AI — Introducing System One Models & Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev)
