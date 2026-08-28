---
title: "Pourquoi ajouter des agents ne crée pas forcément de diversité"
seo_title: "Systèmes multi-agents : plusieurs agents, mêmes biais"
slug: "plusieurs-agents-points-de-vue"
date: 2026-09-01
description: "Multiplier les agents ne crée pas automatiquement de diversité lorsque leurs modèles, contextes et critères restent corrélés."
categories: ["Intelligence artificielle", "Ingénierie logicielle"]
series: ["aucun-harnais-n-est-parfait"]
series_order: 6
collection: "ARCHITECTURE"
cover: "/images/articles/06-plusieurs-agents-ne-font-pas-plusieurs-points-de-vue.fr.png"
draft: false
---

Dix agents construits sur le même modèle peuvent produire dix réponses et un seul angle mort.

Les interfaces multi-agents donnent facilement l'impression inverse. Un agent propose, un autre critique, un troisième arbitre. Chacun possède un nom, un rôle et parfois une personnalité. Le diagramme ressemble à une équipe.

Mais la diversité d'un organigramme ne garantit pas la diversité des erreurs.

## Multiplier les tirages dans le même paquet

Faire travailler plusieurs instances d'un modèle apporte de la variance. Les formulations changent, les trajectoires diffèrent et certaines erreurs d'inattention disparaissent. Pour les problèmes où chaque tentative possède une probabilité indépendante de trouver la bonne réponse, l'agrégation peut être très efficace.

Le problème apparait lorsque les erreurs ne sont pas indépendantes.

Des agents fondés sur le même modèle partagent leur entrainement, leurs représentations et une partie de leurs biais. Si une classe de problème se trouve dans un angle mort commun, le vote majoritaire ne la corrige pas. Il peut même transformer l'erreur en consensus.

Le théorème du jury de Condorcet est souvent invoqué pour justifier la sagesse des foules. On oublie sa condition essentielle : les votants doivent être meilleurs que le hasard et leurs jugements suffisamment indépendants. Cent copies du même juge ne constituent pas une foule au sens qui rend le théorème utile.

## Le consensus peut masquer l'absence d'information

Une réponse répétée dix fois parait plus solide qu'une réponse isolée. Pourtant, si les dix réponses proviennent de la même cause d'erreur, leur nombre n'apporte presque aucune information supplémentaire.

C'est le même problème qu'une panne commune dans un système redondant. Trois serveurs identiques ne protègent pas d'un défaut logiciel présent sur les trois. Ils protègent surtout de pannes matérielles indépendantes.

La littérature récente sur les débats multi-agents documente cette limite. Le vote majoritaire peut échouer lorsque les modèles partagent les mêmes biais ou lorsque la bonne réponse reste minoritaire. Les échanges peuvent aussi provoquer de la sycophancie : les agents se rallient progressivement à une position dominante, y compris lorsqu'elle est fausse.

Le débat donne alors une illusion de délibération. Il homogénéise les positions plus qu'il ne produit de l'information.

## Les rôles restent utiles, mais pour une autre raison

Il ne faut pas en conclure que les agents spécialisés sont inutiles.

Attribuer un rôle "sécurité" peut forcer une passe dédiée sur les permissions, les secrets et les entrées non fiables. Un rôle "architecture" peut examiner les dépendances et les frontières de modules. Ces focales augmentent la couverture des contrôles connus.

Elles ne doivent simplement pas être confondues avec des sources indépendantes.

Un système peut donc combiner deux mécanismes :

- des agents homogènes spécialisés, qui appliquent systématiquement plusieurs grilles de lecture ;
- des évaluateurs réellement hétérogènes, mobilisés pour rechercher des erreurs corrélées.

Les premiers améliorent la discipline. Les seconds améliorent la capacité de surprise.

## Mesurer la diversité par les désaccords utiles

Compter les agents est une mauvaise mesure de diversité. Compter les modèles ne suffit pas toujours non plus. Deux modèles distincts peuvent avoir été entrainés sur des corpus proches, utiliser des méthodes similaires et converger sur les mêmes conventions.

Une mesure plus opérationnelle consiste à observer les désaccords.

Sur quelles catégories de cas deux évaluateurs divergent-ils ? Leurs divergences révèlent-elles des erreurs réelles après revue ? Un nouvel évaluateur détecte-t-il des défauts que le dispositif existant laissait passer ? Son coût apporte-t-il une information nouvelle ou seulement une reformulation ?

La diversité devient alors une propriété empirique du système, pas une étiquette d'architecture.

Cette approche permet aussi d'arrêter une boucle homogène. Lorsque les sorties successives convergent fortement et qu'aucun signal extérieur n'apparait, un tour supplémentaire a peu de chances d'apporter un nouveau point de vue. Il devient plus rationnel de changer de référence, d'outil ou de modèle.

## La bonne question à poser avant d'ajouter un agent

Avant de créer un nouveau rôle dans le workflow, demandons :

> Quelle erreur ce nouvel agent peut-il voir que les autres ont des raisons structurelles de manquer ?

Si la réponse concerne seulement une consigne oubliée, un rôle spécialisé peut suffire. Si elle concerne un biais commun, il faut introduire une différence plus profonde.

Le prochain article traite précisément de cette architecture. Elle ne consiste pas à faire débattre les agents plus longtemps. Elle consiste à préserver leur indépendance jusqu'au moment où leurs verdicts sont comparés.

---

## Sources

- Théorème du jury de Condorcet, indépendance des erreurs comme condition centrale
- *Multi-Agent Debate for LLM Judges*, NeurIPS 2025 · https://arxiv.org/pdf/2510.12697
- *The Deliberative Illusion*, sur attrition factuelle et homogénéisation des positions en débat multi-agents · https://arxiv.org/pdf/2606.03032
- *When Does Delegation Beat Majority?*, limites du vote majoritaire selon la structure des erreurs · https://arxiv.org/pdf/2606.08098
- Mesure de la diversité par les désaccords utiles : proposition opérationnelle issue du manuscrit BYOAI ~
