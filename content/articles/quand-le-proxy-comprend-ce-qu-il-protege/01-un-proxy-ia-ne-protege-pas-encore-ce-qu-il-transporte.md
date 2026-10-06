---
title: "Un proxy IA ne protège que ce qu’on lui apprend à contrôler"
slug: "proxy-ia-controles-contenu"
date: 2026-11-10
description: "Le proxy centralise les accès aux modèles. La protection du contenu dépend des contrôles activés et de leur qualification."
categories: ["Intelligence artificielle", "Cybersécurité", "Architecture logicielle"]
tags: ["ai-platform-engineering", "llmops-agentops"]
series: ["quand-le-proxy-comprend-ce-qu-il-protege"]
series_order: 1
collection: "SYSTÈMES"
cover: "/images/articles/shieldstral/01.png"
draft: false
---

{{< callout variant="scene" label="Point de départ" >}}
Nora utilise Codex ou Claude Code sur son ordinateur professionnel pour résumer un dossier. L'outil n'est pas configuré pour appeler directement OpenAI ou Anthropic. Il envoie ses requêtes au proxy LiteLLM de l'entreprise.
{{< /callout >}}

Nora s'authentifie auprès de LiteLLM avec une clé virtuelle associée à son compte, à son équipe ou à son projet. Le proxy peut alors vérifier que cette clé donne accès au modèle demandé, appliquer les quotas configurés et transmettre la requête au fournisseur concerné.

Le trajet est donc simple :

```text
Codex ou Claude Code
        ↓
proxy LiteLLM de l'entreprise
        ↓
OpenAI, Anthropic, Bedrock, Vertex AI ou modèle local
```

Ce proxy constitue le point de passage où l'entreprise pourra protéger les requêtes avant leur envoi au fournisseur. Encore faut-il configurer les contrôles qui décideront ce qui peut sortir.

Ces mécanismes existent déjà : LiteLLM propose des intégrations de guardrails et un juge LLM capable d'évaluer une requête selon des critères personnalisés avant l'appel principal ; Kong propose un filtrage par similarité sémantique ; Bedrock Guardrails permet de définir des thèmes interdits en langage naturel. Les documentations citées ne présentent toutefois pas de benchmark évaluant leur efficacité sur la détection de secrets métier comme ceux du dossier de Nora. Shieldstral dispose, lui, d'un benchmark publié par Mistral qui inclut une catégorie `Trade Secrets`, avec un score F1 de 92,1 % : ce résultat publié motive son évaluation dans le prototype, sans établir sa supériorité sur les autres passerelles.

Cette série examine une approche particulière : ajouter à la passerelle Shieldstral, un petit modèle entraîné pour la classification de sécurité selon une politique, exécutable localement et accompagné de benchmarks publiés. L'intérêt se trouve dans ce détecteur spécialisé et dans sa qualification, pas dans l'invention du contrôle sémantique au sein d'un proxy.

## Une entrée commune vers plusieurs modèles

Les fournisseurs proposent des API, des formats et des mécanismes d'authentification différents. Sans couche commune, chaque application doit gérer ces particularités et conserver les clés nécessaires pour accéder aux modèles.

LiteLLM fournit cette couche commune. Je l'utilise comme exemple concret dans cette série, mais ce n'est pas le seul choix possible. Il existe de nombreuses autres passerelles IA, commerciales, open source ou développées en interne. Elles n'offrent pas toutes les mêmes fonctions, mais elles occupent le même emplacement entre les applications et les fournisseurs de modèles.

Codex permet de définir un fournisseur personnalisé et l'adresse de son API. Claude Code permet de remplacer l'adresse de l'API Anthropic par celle d'une passerelle. Les deux outils peuvent donc envoyer leurs requêtes à LiteLLM.

LiteLLM reçoit la requête, reconnait la clé virtuelle utilisée et sélectionne le déploiement associé au nom du modèle. Il peut ensuite appeler OpenAI, Anthropic, Azure OpenAI, Amazon Bedrock, Google Vertex AI ou un modèle local, selon la configuration de l'entreprise.

## Le proxy contrôle d'abord le trajet

À ce point central, l'entreprise peut appliquer des règles qui seraient difficiles à maintenir dans chaque application. LiteLLM peut limiter les modèles accessibles avec une clé, suivre les coûts, appliquer des quotas, répartir la charge et basculer vers un autre déploiement en cas de panne.

Cette centralisation évite que chaque poste conserve les clés des fournisseurs et que chaque équipe invente son propre routage. Elle crée aussi un endroit où les décisions peuvent être journalisées de manière cohérente.

Mais connaitre le trajet ne signifie pas comprendre ce qui voyage. Dans la configuration de départ retenue ici, LiteLLM organise les accès et les destinations ; aucun contrôle du contenu du dossier de Nora n'a encore été activé.

La première protection à ajouter est la plus simple : reconnaitre les secrets qui possèdent une forme identifiable. Le prochain article mesure précisément ce que ce filtrage arrête et, surtout, ce qu'il laisse encore passer.

---

{{< closing-question label="À retenir" >}}
Un point de passage commun rend le contrôle possible. Seule une politique effectivement appliquée protège ce qui le traverse.
{{< /closing-question >}}

## Sources

- [Mistral AI — Shieldstral, tableau 12](https://arxiv.org/html/2607.25857v2)
- [LiteLLM — LLM-as-a-Judge](https://docs.litellm.ai/docs/proxy/guardrails/llm_as_a_judge)
- [Kong — AI Semantic Prompt Guard](https://developer.konghq.com/plugins/ai-semantic-prompt-guard/)
- [Amazon Bedrock — Denied topics](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-denied-topics.html)
- [LiteLLM — Documentation](https://docs.litellm.ai/)
- [OpenAI — Codex, référence de configuration](https://developers.openai.com/codex/config-reference)
- [Anthropic — Claude Code, LLM gateway](https://docs.anthropic.com/en/docs/claude-code/llm-gateway)

**Pour continuer :** [Dix documents sur onze passent le filtre par motifs](/articles/proxy-ia-limites-filtre-motifs/).
