---
title: "How to Hide a Watermark in AI-Generated Text"
slug: "comment-cacher-watermark-texte-ia"
date: 2026-08-13
description: "A text watermark is hidden in a sequence of statistically biased choices, not in an invisible character. Here is how this signal works."
categories: ["Artificial intelligence", "Software engineering"]
series: ["comprendre-les-watermarks-textuelles"]
series_order: 2
collection: "ARCHITECTURE"
cover: "/images/articles/watermark-textuelle-technique.en.png"
draft: false
---

**There is usually no invisible character to find. The mark is hidden in a sequence of statistically biased choices.**

*Anthropic has just announced that new Claude models launched in the European Union from August 2, 2026, will include machine-readable marks, including a watermark embedded directly in generated text. The company has not yet published the details of its algorithm. But this announcement makes the subject very concrete, so it seemed important to revisit the general mechanism that makes it possible to hide such a mark in a sequence of words.*

{{< callout variant="scene" label="Starting point" >}}
Consider this unfinished sentence:

**"This method is particularly..."**
{{< /callout >}}

A language model could continue it with "effective," "useful," "suitable," "relevant," or dozens of other fragments.

To generate the continuation, it assigns a probability to each possibility. For example, it might estimate that "effective" has a 23% chance of being a good choice, "relevant" 18%, "useful" 15%, and "suitable" 12%.

A text watermark operates within this space of choices.

It does not necessarily add information to the file. Nor does it slip a secret alphabet into the text. It slightly changes how the model selects its next tokens so that, over a sufficiently long sequence, a pattern emerges that only a properly configured detector can measure.

## A model does not choose words directly

A language model splits text into units called *tokens*. A token can correspond to a whole word, part of a word, a punctuation mark, or sometimes a space attached to the fragment that follows.

At each step, the model calculates a probability distribution over the tokens that could continue the sequence. It selects one, adds it to the text, then starts again from the new sequence.

Generation therefore resembles this loop:

1. read the tokens already present;
2. calculate the possible continuations;
3. choose the next token;
4. add it to the context;
5. repeat.

The watermark acts at the third step.

It uses a secret key to gently bias certain choices. Depending on the context, the system may treat some tokens as temporarily favored. The model continues to produce natural sentences because it does not choose arbitrary tokens: it only increases the likelihood of certain continuations that were already plausible.

The word "effective" is therefore never evidence on its own. In another context, or after a different sequence of tokens, it might not be favored at all.

{{< thesis >}}
What constitutes the mark  
**is the accumulation of choices.**
{{< /thesis >}}

{{< zoomable-figure src="/images/articles/schema-selection-token-watermark.en.png" alt="Token selection process used to create a text watermark" action="Enlarge" label="View the token selection diagram at full size" >}}
The secret key does not impose an arbitrary word: it gently biases the choice among tokens that are already plausible. Repeated over a sufficiently long text, this preference produces a detectable statistical pattern.
{{< /zoomable-figure >}}

## The signal emerges through repetition

For simplicity, imagine that half of the possible tokens are favored at each position.

An unwatermarked text should fall into this group about half the time. A watermarked model might do so slightly more often: 55%, 60%, or more, depending on the chosen settings.

Across ten tokens, this difference means almost nothing. Chance can easily produce six or seven matches.

Across several hundred tokens, a repeated preference becomes harder to explain by chance. The detector then processes the text, reconstructs at each position the choices that the key would have favored, and counts the matches.

It converts this count into a statistical score. The further the score deviates from the behavior expected of unwatermarked text, the more likely the watermark is considered to be present.

{{< callout variant="alert" label="The detector's question" >}}
It does not ask: "Does this sentence contain the secret code?"

It asks: "Is this long sequence of choices unusually consistent with the preferences produced by this key?"
{{< /callout >}}

## Why the key depends on context

A naive method would always favor the same list of tokens. It would create biases that were easy to observe and perhaps exploit.

Modern methods vary their preferences according to the context already generated. A pseudorandom function combines the secret key with certain preceding tokens to produce new scores at each position.

Two occurrences of the same word therefore do not necessarily receive the same treatment. After a given sequence, "relevant" may be favored. Three lines later, in a different context, it may not be.

This variation distributes the mark throughout the generated text without turning a few specific words into a permanent signature.

It also creates an important property: when a token is changed, the calculation for subsequent positions may change as well, because it is now based on a different context.

## SynthID makes several candidates compete

The SynthID-Text method published by Google DeepMind does more than add a fixed bonus to a list of tokens.

The model samples several candidates from its normal distribution. These candidates then compete in a pseudorandom tournament determined by the key. In each round, candidates are compared in pairs and one of each pair is retained. The last survivor becomes the generated token.

With three rounds, eight initial candidates are successively reduced to four, then two, then one.

This mechanism influences the final choice while starting from candidates genuinely proposed by the model. It can be configured to preserve the original distribution on average: across many generations, a token does not become more frequent overall simply because it belongs to a fixed list.

The detector that knows the key can, however, recalculate the pseudorandom results associated with the observed tokens. By aggregating their scores, it looks for the correlation introduced by the successive tournaments.

That is the subtlety: the overall distribution may look normal even though individual choices remain correlated with secret information.

## Some texts offer more room than others

{{< pullquote >}}
A watermark needs choices.
{{< /pullquote >}}

In a story, an email, or a detailed explanation, several phrasings can usually continue each sentence without compromising its meaning. The system therefore has some freedom to bias the selection.

In a highly constrained answer, that freedom disappears. When asked "What is the capital of France?", a useful answer must include "Paris." For an exact quotation, a mathematical formula, highly rigid code, or a list of precise facts, changing the tokens may undermine the accuracy of the result.

If only one token is genuinely acceptable, no selection technique can hide much information in it.

This is why Google DeepMind says that SynthID works better on long, varied responses than on factual or very short ones.

## Copying preserves the mark, rewriting weakens it

The watermark belongs to the sequence of tokens, not to the file that contains them.

Copying and pasting therefore preserves the signal. Changing the font, converting a document, or publishing the text on another platform generally does not alter the tokens being analyzed.

A few isolated corrections may also leave enough watermarked choices for detection to remain possible.

Extensive rewriting creates a different problem. Consider these two sentences:

> This method considerably reduces the time required.

> This approach makes it possible to complete the task much faster.

The meaning remains similar, but almost the entire token sequence has changed. A translation or complete paraphrase can therefore erase much of the correlation the detector is looking for.

When the calculation depends on several preceding tokens, a single change can also disrupt the scores of subsequent positions. The system may later resynchronize if the sequence becomes identical again, but regularly distributed changes obscure a substantial part of the signal.

{{< callout variant="key" label="Structural limitation" >}}
**This is not merely an implementation flaw.**
{{< /callout >}}

Language makes it possible to preserve an idea approximately while changing its form almost entirely. A watermark resistant to every rephrasing would have to recognize the idea itself rather than the sequence that expresses it. At that point, it would no longer truly be a watermark: it would become a semantic comparison system, with a different set of uncertainties.

## The threshold creates the tradeoff

Even without a watermark, a text may happen to contain many tokens consistent with the key. The detector must therefore set a threshold above which it considers the signal significant.

A low threshold detects more watermarked texts but produces more false positives. A high threshold reduces unwarranted alerts but allows more genuinely watermarked texts to go undetected.

Better marketing language does not make this tradeoff disappear.

Text length also matters. In a short passage, the detector has few observations. A handful of chance matches can cause the score to vary considerably. A responsible response should then be "insufficient signal" rather than "human" or "AI."

Multiple testing makes the problem even worse. If an organization splits a document into dozens of passages, tries the keys of many providers, and keeps only the highest score, it multiplies the opportunities to find a correlation by chance. The threshold must account for this overall procedure, not just for each test considered in isolation.

## Watermarks and metadata serve different purposes

Cryptographic provenance, such as the information a file may carry under the C2PA standard, works differently.

A service signs a declaration stating the origin of the file or the processing applied to it. When the signature is valid, the verifier can check that this declaration has not been altered. It does not look for a statistical anomaly in the content.

This precision comes at a cost: metadata can be removed during conversion, copying and pasting, or resaving. A text watermark survives the separation of content from its file more effectively, but it provides a probabilistic signal and can be weakened by rewriting.

The two approaches therefore address different problems:

- the signature states precisely what a service attests to, as long as that attestation still accompanies the file;
- the watermark looks for a pattern embedded in the content, even after copying and pasting;
- neither one proves on its own who developed the ideas or why the tool was used.

## A low-bandwidth statistical channel

Perhaps the most accurate way to understand a text watermark is as a small communication channel hidden in the model's choices.

Each token carries very little information. The signal becomes readable only by accumulating many decisions. The more the signal is strengthened, the greater the risk of constraining generation or changing its quality. The more the model's normal freedom is preserved, the longer the text required for detection and the more sensitive the signal remains to transformations.

A text watermark is therefore neither magic nor useless.

It is an engineering tradeoff among four partially competing goals: keeping the mark invisible, preserving text quality, resisting modifications, and limiting detection errors.

Understanding this mechanism helps avoid two symmetrical extremes: believing that a watermark is infallible cryptographic proof, or assuming that it provides no information at all.

{{< closing-question label="Key takeaway" >}}
It provides a real signal under certain conditions, with a measurable level of confidence and measurable limitations.

Things start to go wrong when the last part is forgotten.
{{< /closing-question >}}

---

## Sources

- Dathathri et al., [*Scalable watermarking for identifying large language model outputs*](https://www.nature.com/articles/s41586-024-08025-4), *Nature*, 2024.
- Google DeepMind, [*Watermarking AI-generated text and video with SynthID*](https://deepmind.google/blog/watermarking-ai-generated-text-and-video-with-synthid/), May 14, 2024.
- Google DeepMind, [*SynthID: A tool to watermark and identify content generated through AI*](https://deepmind.google/models/synthid/).
- OpenAI, [*Understanding the source of what we see and hear online*](https://openai.com/index/understanding-the-source-of-what-we-see-and-hear-online/), updated August 4, 2024.
- Anthropic, [*How Claude marks AI-generated content*](https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content), August 2026.
