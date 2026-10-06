---
title: "What a Text Watermark Does Not Prove"
slug: "watermark-textuelle-ne-prouve-pas-auteur"
date: 2026-08-12
description: "A watermark can indicate that a text has passed through an AI system without proving who wrote it, what their intent was, or how much work they actually did."
categories: ["Artificial intelligence", "Society"]
tags: ["ai-risk-governance"]
series: ["comprendre-les-watermarks-textuelles"]
series_order: 1
collection: "SYSTÈMES"
cover: "/images/articles/watermark-textuelle-consequences.en.png"
draft: false
---

**A text can bear the mark of an AI system without having been written by one. That distinction could determine a grade, a hiring decision, or an accusation of fraud.**

*Anthropic has just announced the gradual rollout of machine-readable markers in content produced by Claude. In particular, new models launched in the European Union from August 2, 2026, must embed a watermark in the text they generate, regardless of the product through which they are used. Following this announcement, it seemed important to revisit what text watermarks can actually establish and, above all, the conclusions they cannot support.*

{{< callout variant="scene" label="A concrete example" >}}
**You are writing a cover letter.**

The ideas are yours. The examples come from your experience. You chose every argument. Before sending it, you simply ask an artificial intelligence system to correct any errors and smooth out an awkward sentence.
{{< /callout >}}

A few days later, a recruiter runs the letter through a detector. It finds a watermark. **The verdict is swift: "AI-generated text."**

The detector may have identified something correctly. But the recruiter has inferred far too much from it.

{{< thesis >}}
The text did pass through an AI system.  
**That does not mean the AI wrote it.**
{{< /thesis >}}

This is the central ambiguity of text watermarks: they can provide a clue about the path a text has taken, then be used as evidence of who wrote it, how much work that person did, or whether they intended to deceive.

But they prove none of those things.

## A Hidden Pattern in Word Choices

A text watermark is generally neither an invisible character nor a label attached to a file.

When a model writes, it selects each new fragment of text from several possible continuations. After "this solution is," for example, it might continue with "effective," "relevant," "appropriate," or "interesting."

To create a watermark, the system gives certain choices a very slight preference according to a secret rule. No single word is suspicious on its own. But over a sufficiently long text, certain choices appear a little more often than chance would predict.

The detector then looks for this statistical correlation.

It is not finding a signature comparable to a name at the bottom of a contract. It is measuring the probability that a sequence of words contains the expected pattern.

This distinction matters for two reasons.

First, **human-written text can sometimes resemble the target pattern by chance**. Second, extensive rewriting, translation, or repeated paraphrasing can weaken the watermark in a text that was genuinely produced by AI. Google DeepMind acknowledges that SynthID works best on long, varied texts and that its confidence can fall sharply after a thorough rewrite or translation.

{{< callout variant="alert" label="Critical limitation" >}}
A positive result is not absolute certainty.

Nor is a negative result a certificate of human authorship.
{{< /callout >}}

## The Most Serious Problem Is Not the False Positive

Discussion often focuses on the risk of entirely human-written text being flagged by mistake. That risk is real. At scale, even a low error rate will eventually leave many people unfairly suspected.

But a subtler case presents an even harder problem: **a genuine positive result that is misinterpreted.**

Consider the cover letter again. If the AI writing assistant regenerated some of its sentences, the watermark may genuinely be present. The detector was not wrong to find it.

{{< pullquote >}}
What is wrong is the conclusion added afterward:  
**"This person did not write their text."**
{{< /pullquote >}}

The watermark knows nothing about the original draft. It cannot see the hours of work that came before. It does not know what prompt was sent to the model. It cannot tell whether the tool invented the argument, translated an existing text, simplified jargon, or corrected three grammatical agreements.

It offers an imperfect answer to a narrow question: "Does this passage contain the statistical pattern associated with this system?"

It does not answer the question that actually matters to the teacher, recruiter, or editor: "Who developed the ideas and did the intellectual work?"

Moving from the first question to the second requires an investigation of the process. No hidden pattern in the tokens can replace it.

## The Most Legitimate Uses Become the Most Visible

This confusion would not affect everyone equally.

Someone who is completely comfortable with writing can submit a text without assistance, but:

- a person with dyslexia may need a writing assistant;
- an international student may have mastered the subject without yet mastering every nuance of the language;
- a person with a disability may use a rewriting tool as assistive technology;
- a skilled technician may want to make an explanation easier to understand without delegating the underlying reasoning.

{{< callout variant="key" label="Key distinction" >}}
AI can shape the **form** without necessarily originating the **substance**.
{{< /callout >}}

If the mere presence of a watermark becomes evidence of cheating, an institution is no longer penalizing only the delegation of work. **It risks penalizing the tool that enables some people to express their own work in the expected form.**

OpenAI itself cited this danger in its research on text watermarking: the technique could stigmatize the use of AI as a writing tool by people writing in a language that is not their own.

The paradox is stark: users who deliberately seek to deceive may try to remove the watermark through rewriting or translation. Honest users, by contrast, often submit the corrected text directly. The system then becomes more restrictive for those who disclose or acknowledge their use of assistance than for those who set out to circumvent it.

## A Watermark Can Travel Without Its Author

Even when a watermark is correctly detected, it does not prove who requested the generation.

A watermarked passage may be quoted in a thesis, copied into an email, included in a collaborative document, or sent by a colleague. Someone may also use AI to rewrite a text written by another person. The watermark follows the words; it does not establish the identity or intent of the person who submits them.

It can therefore reveal technical processing without reconstructing the chain of responsibility.

This is the difference between provenance and authorship. Provenance describes the tools a piece of content encountered. Authorship asks who conceived, decided, and formulated its essential substance. The two may overlap, but they are not interchangeable.

## The Process Is What Should Be Assessed

If a school prohibits all outside assistance during an exam, passing text through a model may be enough to establish a violation of that specific rule. But in most real-world situations, usage is not so binary.

Correcting spelling, translating, brainstorming ideas, drafting an outline, producing a first draft, and writing an entire assignment do not represent the same degree of delegation.

A serious policy must therefore define what it is assessing before selecting a detector.

Is the goal to assess spelling proficiency? The ability to make an argument? Knowledge of a subject? The quality of an application? Compliance with an instruction that explicitly prohibits any tool?

Without that clarification, the watermark provides a technical answer to a question that no one has properly asked.

At a minimum, its use should follow a few principles:

1. Never turn a detection into standalone proof of fraud.
2. Report a confidence level, not a verdict presented as certain.
3. Decline to draw a conclusion when the text is too short or the signal too weak.
4. Allow the person concerned to provide drafts and explain their process.
5. Explicitly distinguish language assistance from the delegation of reasoning.
6. Provide for human review before any consequential decision.
7. Test error rates for the language, type of text, and population actually concerned.

These safeguards do not make watermarks useless. They simply put them in their proper place.

## Evidence of a Text's Journey, Not a Truth Detector

Text watermarks can help researchers study the spread of generated content, indicate that text probably passed through a service, or supplement other evidence of provenance.

On their own, they cannot tell the full story of a text.

A positive result proves neither that AI was the primary author nor that its user intended to deceive. A negative result does not prove that the text is human-written: the model may not have applied a watermark, the passage may have been too short, or the watermark may have been altered.

The decisive question is therefore not: "Has AI touched this text?"

In a world where writing assistants, translation tools, and accessibility technologies will increasingly incorporate generative models, almost every text may one day have been "touched" by AI.

{{< closing-question label="The right question" >}}
"What did the tool do, what did the person do, and what ability are we actually trying to assess?"
{{< /closing-question >}}

A watermark can contribute to that investigation. It cannot deliver the verdict.

## Sources

- Google DeepMind, [*Watermarking AI-generated text and video with SynthID*](https://deepmind.google/blog/watermarking-ai-generated-text-and-video-with-synthid/), May 14, 2024.
- Dathathri et al., [*Scalable watermarking for identifying large language model outputs*](https://www.nature.com/articles/s41586-024-08025-4), *Nature*, 2024.
- OpenAI, [*Understanding the source of what we see and hear online*](https://openai.com/index/understanding-the-source-of-what-we-see-and-hear-online/), updated August 4, 2024.
- Anthropic, [*How Claude marks AI-generated content*](https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content), August 2026.
