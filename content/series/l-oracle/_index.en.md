---
title: "The Oracle"
seo_title: "Oracles and model routing for AI agents"
description: "Four articles on verified retries, model complementarity, oracle reliability, and a method to qualify agentic routing."
weight: 5
---

This series shows how an oracle turns generation into a search loop, then routes failures toward the models that best recover them in observed results.

The first article examines the value of verified retries. The second explains why the model at the top of a leaderboard is not necessarily the model that best complements the previous one. The third examines oracle reliability: grader bugs, false positives, and an acceptable attempt budget.

The fourth proposes a qualification protocol: separate selection from testing, measure the residual, check verdicts against an independent reference, and move from shadow mode to a canary. It includes the stability check of GLM Flash selection on DeepSWE.
