---
title: "When the proxy understands what it protects"
seo_title: "Shieldstral: business policies inside an AI proxy"
description: "Seven articles on integrating a local classifier into an AI gateway: detection, redaction, user choice, and policy evaluation."
weight: 6
---

Nora wants to summarize a file from the fictional Atlas project. Her company's gateway manages access to models; it must also enforce confidentiality policies before the document leaves the infrastructure.

Gateways can already integrate semantic checks, transform data, and select a destination. This series examines a specific approach: adding Shieldstral, a specialized local classifier driven by a business policy question, then measuring how its decisions affect the requested work.

The seven installments move from pattern filtering to semantic detection, then localization, redaction, and explicit user choice. The last examines the prototype's results: on the initial test set, clarifying the policy increased the pipeline's recall from 67% to 100%. The expanded set contains 14 cases; it remains exploratory, and the three redactions still remove almost all of the text.

The guiding question: how can we protect data while preserving a useful, explainable way to work?
