---
title: "Tests from the Same Mind"
slug: "tests-du-meme-cerveau"
date: 2026-09-29
description: "Tests generated alongside the code can consistently confirm a flawed understanding of the need."
categories: ["Artificial intelligence", "Software engineering"]
series: ["aucun-harnais-n-est-parfait"]
series_order: 5
collection: "ARCHITECTURE"
cover: "/images/articles/05-les-tests-du-meme-cerveau.en.png"
draft: false
---

Tests generated alongside the code can prove that the code perfectly matches a flawed understanding of the need.

This is one of the most subtle traps of modern harnesses. It does not necessarily produce a visible failure, cheating, or a red warning light. On the contrary, everything can be remarkably consistent.

The request is misunderstood. The code implements that understanding. The tests verify that the code matches it. The loop corrects the remaining discrepancies and delivers a clean, stable, and incorrect whole.

## Consistency Is Not Conformity

When the same model receives a request, writes the code, and generates the tests in the same session, all three share a common context.

This proximity offers real advantages. Tests can be created immediately. They follow structural changes. They catch local errors and document the behavior the model believes it is supposed to produce.

But that is precisely the limitation: they document what the model believes it is supposed to produce.

If it interprets "active customer" as "customer who has already placed an order," the code will apply that definition. The tests will create examples in which the two concepts coincide. Coverage may reach 100% without any check asking the decisive question: is a newly registered customer who has not placed an order active?

The code-test suite is internally consistent. It does not conform to the business need.

## Not All Tests Serve the Same Purpose

The answer is not to prohibit co-generation. It is to distinguish between levels of evidence.

Unit tests accompany development. They check components, accelerate fixes, and protect against local regressions. Producing them in the same loop as the code is often efficient.

Integration tests verify that multiple components honor their contracts when working together. They begin to test the output against an environment broader than its local logic.

Qualification tests answer a different question: does the system satisfy the need that justifies its existence? Their reference point should come from outside. Validated business cases, real-world examples, properties defined by the requester, independent data, or expected results developed separately.

A unit test can assist the producer. A qualification test must remain evidence that can be held against the producer.

## Make the Need Executable

The phrase "human intervention" is too vague to solve this problem. Someone can approve a list of tests without noticing that they all rest on the same implicit assumption.

The most valuable contribution from domain experts often comes earlier: providing examples that force a decision.

Which cases should be accepted? Which should be rejected? What result would be surprising? What exception is common in practice but absent from the official procedure? At what point does a decision change state?

These examples are not decorative documentation. They form a qualification dataset that the generator must not be allowed to reinterpret silently.

Properties can also be used instead of fixed cases: an amount must never become negative, a canceled decision must no longer have any effect, two equivalent operations must produce the same result, and sensitive data must never appear in any log.

Properties make the need harder to circumvent than a handful of expected answers.

## Introduce a Genuine Difference in Origin

Independence does not depend solely on the model being used. It depends on where the criteria come from.

A second model that generates its tests from the same ambiguous statement may reproduce the same misunderstanding. Conversely, the same model can provide a useful check if it receives an independent source: a separately validated specification, an API contract, an incident history, or examples the producer has not seen.

Two forms of correlation therefore need to be examined:

1. engine correlation, when production and validation use the same model;
2. reference correlation, when they rely on the same initial understanding of the need.

Changing the engine without changing the reference is not always enough. Changing the reference can sometimes contribute more than adding another model.

## Test the Misunderstanding

A robust review does not merely ask, "Does the code do what the tests say?" It also asks, "What do these tests assume without saying so?"

This question is uncomfortable because it cannot be fully automated. It requires returning to actual practice, users, incidents, and cases that resist neat categories.

But that is precisely where the value of the harness lies. It must do more than accelerate production. It must create repeated points of contact between production and a reality the generator does not control.

Tests from the same mind strengthen internal consistency. Verifying conformity requires at least one reference from elsewhere.

What if we simply added several agents to multiply those reference points? That would work on one rarely satisfied condition: they must not repeat the same perspective under different names.
That is the subject of the next article.

---

## Sources

- Proposed distinction between unit tests, integration tests, and qualification tests: established terminology, applied to harnesses in the BYOAI manuscript
- Thoughtworks, *Harness engineering for coding agent users*, distinction between computational and inferential checks: https://martinfowler.com/articles/harness-engineering.html
- Principle that internal consistency does not equal conformity to the need: conceptual development, to be illustrated with real-world cases before possible long-form publication
