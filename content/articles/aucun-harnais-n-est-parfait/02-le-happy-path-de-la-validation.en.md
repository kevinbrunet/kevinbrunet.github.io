---
title: "Your Tests Pass. Reality Can Still Deviate."
slug: "happy-path-validation"
date: 2026-09-01
description: "A harness only tests errors that have been turned into checks, leaving out situations that no one has imagined yet."
categories: ["Artificial intelligence", "Software engineering"]
series: ["aucun-harnais-n-est-parfait"]
series_order: 2
collection: "ARCHITECTURE"
cover: "/images/articles/02-le-happy-path-de-la-validation.en.png"
draft: false
---

A harness tests the errors that someone thought to turn into checks.

This statement is not an indictment of testing. It is simply a reminder of its limits.

We have grown accustomed to setting fragile code against rigorous validation. The contrast is reassuring: if AI makes production faster, strengthening the checks should be enough to retain control. Yet validation has a happy path of its own.

## Expectations Meet Reality

A test is the executable expression of an expectation. It can check a nominal result, an empty input, a known error, a volume limit, or guard against the recurrence of a past incident.

Writing that test required someone to imagine the scenario.

The harness can run this check a thousand times without tiring. But repetition alone cannot make it invent a deviation that appears in none of the examples, rules, or datasets it was given.

This is the familiar happy path problem. A system can cover the vast majority of situations in isolation and still fail across a large share of real-world journeys. If ten steps each have a 90% chance of remaining within their nominal case, the probability that all ten will do so is only 0.9 to the power of 10, or about 35%.

An exceptional journey is therefore not necessarily rare. It can be an ordinary combination of small, commonplace exceptions.

## A Harness Inherits Its Designer's Perspective

The most useful checks often come from experience. A failure occurs, the team understands its mechanism, then adds a test to prevent it from recurring. The harness gradually becomes an executable record of the problems encountered.

That is a considerable strength. It is also evidence that the harness does not always precede reality.

Before the first incident, the team did not necessarily know that this class of failure existed. Afterward, they can name it, reproduce it, and add it to their line of defense. The harness learns, but some of that learning is retrospective.

The right question, then, is not: "Do our tests pass?" It is: "What could be wrong while still allowing our tests to pass?"

This question changes the review process. It no longer looks only for missing checks around known behavior. It searches for the unspoken assumptions underlying the very definition of success.

## More Tests Do Not Automatically Solve the Problem

AI can generate a large number of tests at low cost. This is useful for expanding input combinations, strengthening regression testing, and exploring cases to which a developer might not have devoted time.

But quantity does not guarantee an independent perspective.

If the same model reads the request, writes the code, and then produces a hundred tests based on its own understanding, those hundred tests may explore a shared misunderstanding in great depth. Coverage increases. Alignment with the actual need may not have changed at all.

A thousand variations on an assumption do not amount to verifying that assumption.

This distinction makes it possible to allocate checks more effectively. Unit tests can accompany production and help the agent stabilize its code. Integration and acceptance tests should be grounded more firmly in external references: anonymized real-world data, examples provided by domain experts, independent API contracts, properties defined by someone else, or outcomes observable outside the generator's session.

## A Good Harness Organizes Around Its Own Incompleteness

The answer is not to promise perfect coverage. That promise would be self-contradictory: a perfect harness would have to contain tests for everything its designers failed to imagine.

The answer is to organize the learning process.

Incidents, discrepancies between expected and actual results, human interventions, and cases in which an agent expressed high confidence before proving wrong must all be retained. Every surprise can become a future check. Over time, the organization builds an empirical taxonomy of its blind spots.

This discipline keeps the harness alive. It prevents teams from treating it as a finished product that can be installed once and for all.

It also demands a degree of operational humility. A success rate measures what was tested, against observed distributions, using the available criteria. It does not measure all the ways in which the system could be wrong.

The first trap of the harness, then, is to confuse the repeatability of validation with its exhaustiveness.

The second is more subtle. If the generator knows its own output so well, why not ask it to review that output itself?
That is what we will explore in the next article in this series.

---

## Sources

- Composite journey calculation: 0.9¹⁰ ≈ 34.9%
- Huang et al., *Large Language Models Cannot Self-Correct Reasoning Yet*, ICLR 2024, on the limits of self-correction without external feedback: https://arxiv.org/abs/2310.01798
- The principle of an empirical taxonomy of blind spots: an original concept developed in the BYOAI manuscript, to be validated experimentally
