---
title: "À propos"
layout: "about"
seo_title: "Software Architect — Agentic AI Systems & AI Reliability"
description: "Architecte logiciel, 18 ans d'expérience : systèmes IA agentiques, harnesses, evals et fiabilité. Une approche guidée par le métier et le risque."
---

Je suis **Kévin Brunet, architecte logiciel**, avec **18 ans d'expérience en développement et en architecture de systèmes métier**. Mon parcours s'est construit sur les systèmes d'information complexes, leurs contraintes de production et les équipes qui les font vivre. C# et .NET font partie de ce socle d'ingénierie.

Je travaille aujourd'hui sur les **systèmes IA agentiques**, avec une attention particulière à leur fiabilité et à leur mise en production. J'y retrouve les questions qui traversent mon parcours : comment intégrer le système au métier, vérifier ce qu'il fait, limiter son pouvoir d'action et comprendre ses défaillances ?

Ce qui m'intéresse, ce n'est pas la technologie pour elle-même. C'est ce qu'elle permet de construire, la manière dont elle répond à un besoin et ce qu'elle implique une fois en production.

## Une architecture doit fonctionner dans la vraie vie

Une décision d'architecture doit tenir compte du métier, du budget, de l'existant et de l'organisation. Elle doit aussi rester compréhensible par les personnes qui vont développer, exploiter et faire évoluer le système.

Mon rôle consiste souvent à remettre ces contraintes autour de la même table. Je cherche une solution assez solide pour durer, mais pas plus complexe que nécessaire. Le bon choix n'est pas toujours le plus élégant sur le papier. C'est celui que l'équipe peut expliquer, mettre en œuvre et assumer dans le temps.

J'accorde beaucoup d'importance aux principes, aux modèles et aux retours d'expérience. Ils donnent une base pour réfléchir. Ils ne remplacent pas l'analyse du contexte et ne dispensent jamais de regarder le terrain.

## Des contextes métiers différents

J'ai travaillé dans des secteurs comme la santé, la paie, l'énergie, les assurances et le retail. Ces expériences m'ont beaucoup appris, parce que les systèmes n'y portent pas les mêmes risques et ne répondent pas aux mêmes contraintes.

Dans la santé, il y a le risque patient, des droits d'accès fins, les exigences du Ségur du numérique en santé et une réglementation très présente. Dans la paie, il faut naviguer dans le temps, gérer la rétroactivité, effectuer des calculs à rebours et parfois modifier le passé sans jamais perdre sa traçabilité. L'énergie pose des questions de continuité et de maîtrise des opérations. Les assurances doivent évaluer et tarifer un risque avant d'en connaître le coût réel, une problématique que l'on retrouve dans la cybersécurité. Le retail traite d'importants volumes de données, comme la santé, mais impose surtout une grande réactivité : tout change vite et il faut proposer le bon produit, au bon prix et au bon moment.

Je retrouve aujourd'hui beaucoup de ces problématiques dans l'IA. Elle concentre des questions de risque, de droits d'accès, de réglementation, de temporalité, de traçabilité, de volume et de réactivité. Ces expériences me donnent un cadre concret pour les aborder.

## Mettre l'IA au bon endroit

Un agent IA ne reste pas longtemps une simple fonctionnalité. Dès qu'il consulte des données, utilise des outils ou agit pour un utilisateur, il fait partie du système d'information.

Il faut alors répondre à des questions concrètes. Qui agit ? Dans quel but ? Avec quelles autorisations ? À partir de quelles informations ? Qui contrôle le résultat ? Que garde-t-on comme trace ?

Je m'intéresse surtout à ce passage entre la démonstration et l'usage réel. C'est là que l'identité, la délégation, la mémoire, la sécurité, l'observabilité et la supervision humaine deviennent importantes. Sans ces éléments, on peut obtenir un prototype convaincant, mais pas un système sur lequel une organisation peut compter.

## Construire le système autour du modèle

**Le modèle n'est pas le système. La fiabilité se construit aussi dans l'architecture qui l'entoure.**

Mes travaux et mes articles portent sur plusieurs domaines complémentaires :

- **[AI Systems & Harness Engineering](/sujets/ai-systems-harness-engineering/)** : boucle d'exécution, outils, contexte, mémoire, orchestration et reprise après échec. Le harness organise le travail du modèle et porte les contrôles du système.
- **[AI Evaluation / Evals](/sujets/ai-evaluation-evals/) et [AI Reliability](/sujets/ai-reliability/)** : oracles, cas de référence, tests de régression et indépendance des évaluations. Un test qui passe doit apporter une preuve utile sur le comportement attendu.
- **[AI Observability](/sujets/ai-observability/) et [LLMOps / AgentOps](/sujets/llmops-agentops/)** : traces, diagnostic, suivi du comportement, qualité, coût et latence. LLMOps concerne l'industrialisation des applications LLM ; AgentOps étend ce suivi aux trajectoires, aux décisions et aux appels d'outils des agents.
- **[Agent Protocols](/sujets/agent-protocols/)** : MCP, A2A et ACP, pour réfléchir à l'intégration des outils, des agents et des interfaces sans confondre leurs responsabilités.
- **[AI Security](/sujets/ai-security/) et [AI Risk & Governance](/sujets/ai-risk-governance/)** : frontières d'autorité, permissions, isolation, guardrails et supervision humaine. Le niveau d'autonomie doit rester cohérent avec les conséquences d'une erreur.

Je formalise une démarche de passage du prototype à la production : partir d'un objectif métier, analyser les risques, définir les comportements attendus et leurs oracles, évaluer sur des cas représentatifs, puis observer le système en fonctionnement. L'élargissement de son périmètre doit s'appuyer sur ce que ces observations permettent réellement de conclure.

Cette démarche relie **Software Architecture, AI Systems Engineering et AI Platform Engineering**. Mes articles exposent les mécanismes, les expérimentations et leurs limites ; ils donnent à voir ma manière de raisonner sur ces systèmes.

## Une expérience ancrée dans les systèmes métier

Pendant 18 ans, j'ai développé et participé à l'architecture de systèmes métier dans la santé, la paie, l'énergie, les assurances et le retail. Ce parcours m'a confronté aux questions de droits d'accès, de traçabilité, de continuité et d'évolution des règles métier, avec des conséquences concrètes pour les utilisateurs.

J'en ai tiré une pratique de l'architecture qui relie le besoin métier, le code et l'exploitation. Comprendre l'existant, expliciter les responsabilités et choisir des contrôles proportionnés au risque font partie de cette pratique. C'est sur cette expérience que s'appuie mon travail sur les systèmes IA agentiques.

Mes articles en donnent des exemples : [« Aucun harnais n'est parfait »](/series/aucun-harnais-n-est-parfait/) examine les limites de la validation, [« Qui donne le droit d'agir à votre agent IA ? »](/series/qui-donne-le-droit-d-agir-a-votre-agent-ia/) détaille l'identité et la délégation, et [la série sur ACP](/series/acp-interface-manquante-des-agents/) étudie la séparation entre interface, harness et modèle.

Le fil conducteur de ces travaux reste celui de mes projets : **comment savons-nous que cela fonctionne ? Que se passe-t-il quand cela échoue ? Qui peut agir, jusqu'où, et quelle preuve gardons-nous ?**

## Rendre les mécanismes visibles

J'écris pour partager ce que j'observe et pour rendre les sujets techniques plus faciles à discuter. Une armoire fibre, un jeu vidéo ou une situation vécue dans un projet peuvent parfois mieux expliquer un problème de couplage, de visibilité ou de responsabilité qu'un long discours théorique.

Je ne cherche pas à faire disparaître la complexité. J'essaie de distinguer celle qui est nécessaire de celle que nous créons nous-mêmes, puis de trouver les mots et les schémas qui permettent d'en parler simplement.

Vous trouverez ici des articles sur l'architecture logicielle, l'évolution des systèmes d'information, les agents IA, la sécurité et l'organisation des équipes. Ils s'adressent aux personnes qui construisent ces systèmes comme à celles qui doivent prendre des décisions à leur sujet.

Le fil conducteur est simple : **comprendre comment un système fonctionne pour pouvoir lui faire confiance.**
