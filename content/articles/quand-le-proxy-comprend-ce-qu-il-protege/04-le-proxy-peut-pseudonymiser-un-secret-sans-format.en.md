---
title: "Redacting a secret without a fixed format: does the proxy still preserve the task?"
slug: "shieldstral-business-secret-redaction"
date: 2026-11-10
description: "The prototype locates sensitive areas by chunk and rechecks them after redaction, but still removes almost the entire document."
categories: ["Artificial intelligence", "Cybersecurity", "Software architecture"]
tags: ["ai-security"]
series: ["quand-le-proxy-comprend-ce-qu-il-protege"]
series_order: 4
collection: "SYSTEMS"
cover: "/images/articles/shieldstral/04.en.png"
draft: false
---

{{< callout variant="scene" label="Starting point" >}}
Shieldstral indicates that Nora's file contains industrial know-how. The proxy can now go beyond blocking the whole document: look for the relevant areas, replace them, and evaluate whether the transformed version may be allowed to reach an external destination. The prototype does not yet demonstrate that this version remains usable.
{{< /callout >}}

For an IBAN, a specialized engine directly returns a precise position. For a business procedure, sensitivity comes from a combination of sentences. The system must therefore map the document around the signal provided by Shieldstral.

This step turns semantic detection into an area that can be transformed. It still needs to check that the transformation preserves enough of the document to remain useful.

## Pseudonymization preserves a usable document

A recognizable identifier can be replaced without removing the rest of the sentence:

```text
Original: Send payment to Jean at FR76 3000 6000 0112 3456 7890 189
External: Send payment to <PERSON_1> at <IBAN_1>
```

The proxy keeps the mapping table locally. If the model uses `<PERSON_1>` or `<IBAN_1>` in its response, the value can be restored before Nora sees it. Some gateways offer this mechanism directly. LiteLLM, for example, exposes the `output_parse_pii` option through its Presidio integration.

This pseudonymization is possible because the detector knows where each entity starts and ends. The external model retains enough context to perform the task without knowing the original value.

The same principle can be extended to industrial know-how, provided it works at the passage level rather than on an isolated pattern.

## The document is split into segments that retain their positions

The proxy can split the text into paragraphs or token windows. Each segment retains its offsets in the original document. Shieldstral then receives the same business policy with each piece.

```text
original document with positions
        ↓
overlapping segments
        ↓
policy question + segment
        ↓
Shieldstral score per segment
        ↓
merge sensitive areas
        ↓
replace with <BUSINESS_SECRET_1>
```

When a segment exceeds the threshold, the pseudonymization component knows the corresponding area. It can replace it with a pseudonym before the external call.

Shieldstral thus drives semantic pseudonymization without performing it alone. The classifier produces the signal. Segmentation supplies the positions. The proxy applies the transformation.

The result brings together three distinct functions: Shieldstral detects the protected meaning, segmentation provides positions, and the proxy applies the transformation. No single component needs to take on the entire task.

## The proof of concept now exercises the entire pipeline

The first campaign contained 11 documents. It validated decisions to allow, block, or redirect locally, but no case actually followed the semantic pseudonymization branch.

I added three sensitive documents calibrated to reach the policy's intermediate band: a partial description of financial transaction splitting, an Atlas setting included in a report, and a medical file identifiable from initials and context.

On these three cases, the proxy executed the full pipeline:

```text
score one or more chunks
        ↓
locate a sensitive area
        ↓
replace with [REDACTED PASSAGE]
        ↓
Shieldstral recheck
        ↓
permission to transmit to the frontier model
```

The average score fell from 46% before transformation to 3% after rechecking. None of the three rechecks failed. The proof of concept executes localization, redaction, and rechecking. It returns a destination decision; it does not call the frontier model to perform the task.

We must precisely name what the prototype demonstrates. It currently replaces chunks with a removal marker; it does not retain a table that could restore a business secret in the response. This is semantic redaction that validates the mechanism needed for future reversible pseudonymization.

## Overlap reduces the effects of artificial boundaries

A procedure may span several sentences. The first paragraph names the machine. The next gives the temperature. A third explains that the order of steps reduces defects.

If each sentence is evaluated in isolation, none necessarily contains enough context to appear sensitive. But evaluating only the complete document creates the opposite problem: the signal can be diluted in mostly neutral text.

The proof of concept measured this blind spot. A sensitive sentence scored 0.42 alone, then only 0.003 when surrounded by neutral text. The locator therefore evaluates every chunk before the decision and retains the highest score. Segments overlap so that the end of one window reappears at the start of the next.

Overlap reduces the effects of artificial boundaries. It does not guarantee detection of a secret that requires several windows to understand. This method also has a cost: a short document fits in one chunk, while a long document requires one Shieldstral call per chunk, even if it is ultimately allowed.

## The result must be checked a second time

After replacement, the proxy reassembles the document and subjects it to another check. This pass looks for a sensitive signal in the reassembled text. It does not prove that every reconstruction of the secret is impossible. In the proof of concept, it adds 17 to 20 ms to the three relevant cases.

Segment analysis serves to locate; the final check examines the text whose transmission would be authorized. The same classifier can repeat the same error: residual leaks must also be measured through an independent evaluation.

The system must also keep pseudonyms consistent. If the same client appears five times, `<CLIENT_1>` must refer to the same entity throughout. This stability lets the model reason about relationships without knowing the original identity.

## The mechanism works, but still removes the task

The goal remains to transmit much of the document without exposing the protected process. For a general summary, replacing a few passages with `<BUSINESS_SECRET_1>` might preserve enough context to produce a useful result.

{{< callout variant="alert" label="The measured limitation" >}}
The current result does not yet meet that goal. On the three new documents, the locator removed between 99% and 100% of the text. All three rechecks passed, mainly because almost nothing remained to evaluate. The report therefore classifies all three as potentially excessive redactions.
{{< /callout >}}

This limitation partly comes from the set: the documents are short, and the locator works at chunk granularity rather than locating the exact passage inside each chunk. The three redacted versions pass the prototype's recheck. That result establishes neither the absence of every residual leak, nor the document's usefulness, nor its actual transmission to a destination model. To measure usefulness, we need long documents with expected sensitive positions and must check that the non-sensitive context remains genuinely usable.

Detection remains useful even when automatic redaction is too broad. The proxy can tell Nora the nature and location of the issue, then return control so she can reword the document herself. She often knows better than the system which information can be removed without distorting her request. The new version then passes through Shieldstral again before any transmission to the frontier model.

This path turns the semantic signal into decision support without letting the proxy silently rewrite the content. It still needs testing in the proof of concept, and the level of detail the explanation can provide without revealing more of the secret must be defined.

One limitation remains: the removed passage may be essential to the task. If Nora asks to compare the parameters of two procedures, the frontier model cannot produce a complete analysis from `<BUSINESS_SECRET_1>`. Restoring the passage in the response cannot repair reasoning performed without it.

In that case, a local model becomes a better solution than pseudonymization. In other cases, the passage is incidental and the transformed version is sufficient.

The proxy does not always know Nora's intent precisely enough to choose between these treatments. Deciding alone would silently change her task.

The advance is nevertheless concrete: the proxy can now detect, locate by chunk, redact, and recheck a secret with no prefix, fixed format, or obvious regular expression. The next improvement is to make localization precise enough to preserve the task. Until then, when transformation removes too much context, the user must be able to choose local processing or cancellation.

The next article shows how the proxy can ask that question in the existing interface by responding itself, without calling the requested model.

---

{{< closing-question label="Takeaway" >}}
Detection, localization, and transformation are three distinct responsibilities. Redaction that passes a recheck must still preserve useful work.
{{< /closing-question >}}

## Sources

- [Shieldstral evaluation report — September 2, 2026](/documents/shieldstral-qualification-2026-09-02.en.md)
- [LiteLLM — Presidio integration types](https://github.com/BerriAI/litellm/blob/litellm_internal_staging/litellm/types/guardrails.py)
- [Mistral AI — Shieldstral](https://arxiv.org/abs/2607.25857)

**Continue reading:** [The proxy can respond without calling the model](/en/articles/ai-proxy-synthetic-response-user-choice/).
