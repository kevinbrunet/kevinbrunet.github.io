---
title: "Aucun harness n'est magique"
seo_title: "Fiabilité des agents IA : aucun harnais n'est magique"
slug: "aucun-harnais-n-est-magique"
date: 2026-09-01
description: "Aucun harnais ne couvre tous les risques : la robustesse vient d'une gouvernance capable d'organiser plusieurs lignes de défense."
categories: ["Intelligence artificielle", "Ingénierie logicielle"]
series: ["aucun-harnais-n-est-parfait"]
series_order: 8
collection: "ARCHITECTURE"
cover: "/images/articles/08-aucun-harnais-n-est-magique.fr.png"
draft: false
---

Choisir un seul harness pour toute l'entreprise peut simplifier la gouvernance et créer un risque systémique.

La contradiction n'est qu'apparente.

Une organisation a de bonnes raisons de standardiser : audit, support, coûts, compétences, traçabilité et sécurité. Lorsque chaque équipe assemble librement ses modèles, ses outils et ses contrôles, le paysage devient rapidement illisible.

Mais standardiser tous les contenus du harness ne produit pas seulement de l'ordre. Cela installe aussi les mêmes angles morts partout.

## La monoculture est efficace jusqu'au jour où elle ne l'est plus

Une monoculture agricole facilite le travail, améliore les rendements et simplifie les traitements. Elle devient fragile lorsqu'un parasite sait exploiter précisément les caractéristiques partagées par toutes les plantes.

Un parc d'agents homogène suit la même logique.

Le même modèle comprend mal une catégorie de demandes. Le même reviewer ne voit pas l'erreur. Les mêmes tests ont été générés à partir de la même interprétation. La même politique de validation déclare les résultats acceptables. L'incident ne touche plus un utilisateur isolé. Il peut traverser toute l'organisation sans produire de désaccord interne.

La diversité n'est donc pas seulement une liberté accordée aux équipes. Elle peut constituer une défense contre les défaillances corrélées.

## Standardiser le châssis, pas tous les regards

Il faut distinguer deux niveaux.

Le châssis du harness peut être commun. L'entreprise peut imposer la manière dont un dispositif s'installe, déclare ses modèles, journalise ses actions, protège ses secrets, sépare production et qualification, mesure ses coûts et remonte ses incidents.

Ce châssis rend la diversité gouvernable. Il fournit une interface commune à l'audit sans imposer un seul contenu.

À l'intérieur, plusieurs éléments peuvent varier : modèle producteur, modèle reviewer, prompts, outils déterministes, jeux de qualification, configuration de sécurité et références métier. Cette pluralité n'a de valeur que si elle produit effectivement des erreurs moins corrélées. Elle doit donc être mesurée, pas célébrée par principe.

L'objectif n'est pas "chacun fait ce qu'il veut". L'objectif est "plusieurs dispositifs peuvent démontrer comment ils travaillent et ce qu'ils apportent de différent".

## La diversité comme politique de risque

Une politique mature ne demande pas quel modèle est le meilleur en général. Elle demande quelles combinaisons réduisent le risque sur une classe de tâches.

Pour du code courant, un producteur rapide associé à des tests déterministes et à un reviewer échantillonné peut suffire. Pour une transformation de données sensibles, un second modèle, un environnement isolé et un jeu de qualification indépendant peuvent être nécessaires. Pour une décision qui engage autrui, le harness individuel ne constitue peut-être jamais une preuve suffisante.

La diversité devient un portefeuille de contrôles.

Comme en finance, on ne diversifie pas parce que chaque actif est supérieur. On diversifie parce que des risques imparfaitement corrélés évitent qu'un seul événement emporte l'ensemble.

Cette logique donne aussi une responsabilité précise au pilote. Le harness est un outillage, pas un alibi. Celui qui le pilote doit connaitre le régime dans lequel il peut être utilisé, les contrôles qu'il exécute et les limites observées. Lorsqu'un outil individuel est promu au niveau de l'équipe ou de l'entreprise, sa maintenance et sa responsabilité doivent monter ensemble.

## Construire la carte des angles morts

Une entreprise ne connaitra pas ses angles morts par décret. Elle les découvrira dans les désaccords, les incidents, les reprises humaines et les écarts entre confiance annoncée et résultat réel.

Cela suggère une fonction nouvelle de gouvernance.

Quelqu'un doit observer la population des harness plutôt qu'un seul pipeline. Quels dispositifs laissent passer les mêmes défauts ? Où un modèle en corrige-t-il un autre ? Quels contrôles ne produisent plus de signal utile ? Quel incident révèle une faiblesse commune à plusieurs équipes ?

Cette personne ne cherche pas seulement à vider un backlog de problèmes. Elle recherche les causes partagées qui les produisent. Elle agit comme un épidémiologiste : un cas isolé intéresse moins par son volume que par ce qu'il révèle sur la population.

La diversité sans cette observation reste du bruit. Avec elle, les erreurs locales deviennent une matière d'apprentissage collectif.

## Une thèse falsifiable

L'idée peut et doit être testée.

Deux groupes comparables peuvent utiliser, pour une même classe de tâches, soit un harness homogène, soit plusieurs dispositifs gouvernés mais réellement différents. On mesure ensuite les défauts détectés avant production, les incidents après production, les désaccords ayant conduit à une correction utile, le coût total de validation et le temps de résolution.

Si la diversité n'améliore pas la détection ou coûte davantage qu'elle ne protège, la politique doit être revue. Si elle ne produit que des divergences stylistiques, elle n'est pas une défense. Si elle révèle des classes d'erreurs invisibles au dispositif dominant, elle devient un actif de sécurité.

Cette exigence de mesure protège la thèse contre sa propre rhétorique. "La diversité est résiliente" ne doit pas devenir un nouveau slogan impossible à contredire.

## Aucun harness n'est parfait. C'est une propriété de l'architecture.

Un harness industrialise la validation. Il élimine des erreurs, impose des invariants et permet à la production agentique de changer d'échelle.

Il vérifie néanmoins ce qu'on lui a appris à vérifier. Il peut relire avec les mêmes angles morts, optimiser la mesure au lieu de la mission et produire un consensus artificiel entre agents corrélés.

La bonne réponse n'est ni l'absence de harness ni la recherche d'un harness magique.

Elle consiste à protéger les contrôles, ancrer la qualification dans des références extérieures, préserver l'indépendance des évaluateurs, apprendre des désaccords et maintenir plusieurs regards dans un châssis gouvernable.

Nous avons longtemps traité l'uniformité comme la condition de la maitrise. Avec les agents, elle peut aussi devenir la manière la plus silencieuse de partager la même erreur.

---

## Sources

- Théorème du jury de Condorcet, condition d'indépendance des erreurs
- Littérature 2025-2026 sur les limites du vote et du débat multi-agents : synthèse dans *The Deliberative Illusion* et *When Does Delegation Beat Majority?* · https://arxiv.org/pdf/2606.03032 ; https://arxiv.org/pdf/2606.08098
