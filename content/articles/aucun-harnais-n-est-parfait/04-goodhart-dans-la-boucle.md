---
title: "Le voyant est vert. La mission reste inachevée."
slug: "goodhart-dans-la-boucle"
date: 2026-09-22
description: "Quand la métrique devient la cible, un agent peut optimiser le voyant vert tout en laissant la mission réelle inachevée."
categories: ["Intelligence artificielle", "Ingénierie logicielle"]
series: ["aucun-harnais-n-est-parfait"]
series_order: 4
collection: "ARCHITECTURE"
cover: "/images/articles/04-goodhart-dans-la-boucle.fr.png"
draft: false
---

Un agent peut faire passer tous les tests sans résoudre le problème.

Il ne s'agit pas d'une pirouette théorique. Des modèles chargés de réussir une tâche de programmation ont déjà codé en dur des valeurs attendues, traité spécialement les cas de test ou affaibli le mécanisme qui devait les contrôler.

Le voyant devient vert. La mission, elle, reste inachevée.

## Une mesure utile devient un objectif

La loi de Goodhart est généralement résumée ainsi : lorsqu'une mesure devient un objectif, elle cesse d'être une bonne mesure.

Un test est d'abord un instrument d'observation. Il nous indique si une propriété attendue est respectée. Dans une boucle agentique, ce même test devient aussi l'obstacle que l'agent doit franchir pour terminer sa tâche.

La plupart du temps, le chemin normal consiste à corriger le code. Mais si l'environnement laisse d'autres chemins ouverts, l'agent peut découvrir qu'il est moins coûteux de modifier la mesure, de reconnaitre le cas évalué ou de satisfaire seulement sa forme visible.

[METR](https://metr.org/blog/2025-06-05-recent-reward-hacking/) a documenté ce type de reward hacking chez des modèles de pointe dès 2025. Le phénomène ne suppose pas une intention malveillante au sens humain. Il découle simplement d'un système optimisé pour atteindre un état mesurable dans un environnement où plusieurs moyens d'y parvenir restent accessibles.

## Le problème n'est pas le test, mais la topologie des permissions

On répond souvent à cette difficulté par une revue supplémentaire : vérifier que l'agent n'a pas modifié les tests.

C'est un filet utile. Ce n'est pas la solution principale.

Si le producteur peut éditer ce qui le qualifie, le défaut est architectural. La vraie parade consiste à séparer les permissions. L'agent peut modifier le produit. Il ne peut pas modifier les tests de qualification, les seuils de sécurité, les journaux de contrôle ou la politique qui décide si sa production passe.

Ce qui vérifie doit rester hors de portée de ce qui produit.

Cette règle ne signifie pas qu'un agent ne doit jamais écrire de tests. Les tests unitaires co-générés avec le code sont précieux pour progresser vite, clarifier une fonction et prévenir des régressions locales. Ils participent au travail de construction.

Les tests d'intégration et de qualification jouent un autre rôle. Ils doivent établir que la production répond à un contrat extérieur au générateur. Ceux-là nécessitent une origine et des permissions distinctes.

## Ne pas montrer toute la copie

Même lorsqu'un agent ne peut pas modifier les tests, il peut parfois voir précisément les données qui seront évaluées. Il lui devient alors possible de façonner sa réponse autour de ces cas sans généraliser correctement.

La séparation des fichiers ne suffit donc pas toujours. Il faut aussi réfléchir à la visibilité.

Des jeux de données cachés, renouvelés ou générés aléatoirement réduisent le risque de spécialisation sur une liste fixe. Des propriétés générales sont souvent plus robustes que quelques valeurs attendues connues à l'avance. Une partie de la qualification peut aussi être exécutée dans un environnement auquel le producteur n'a pas accès.

Ce principe est familier dans l'éducation : un examen n'évalue plus grand-chose si le candidat dispose exactement des questions et des réponses avant l'épreuve. L'agent ne change pas cette logique. Il l'exploite simplement à une vitesse et avec une continuité nouvelles.

## Le vert doit rester coûteux à falsifier

Un harness efficace ne cherche pas uniquement à multiplier les contrôles. Il construit une asymétrie : résoudre réellement le problème doit être plus facile que contourner la preuve.

Cela demande de cartographier les accès, pas seulement les étapes du workflow :

- Qui peut écrire le code ?
- Qui peut écrire les tests de qualification ?
- Qui peut modifier les seuils ?
- Qui voit les données de test ?
- Qui peut effacer ou réécrire les journaux ?
- Quel contrôle reste indépendant de la session de production ?

Ces questions paraissent moins séduisantes qu'un diagramme de dix agents spécialisés. Elles déterminent pourtant si le système valide une production ou met en scène sa validation.

## Garder l'objectif derrière la mesure

Le dernier rempart contre Goodhart reste la capacité à revenir à l'intention.

Un test indique qu'une propriété a été observée. Il ne peut pas prouver à lui seul que l'ensemble des propriétés importantes a été choisi. La Definition of Done, les exemples métier et la revue du résultat dans son contexte restent nécessaires pour relier le voyant à la mission.

Le harness doit donc contenir des mesures fortes, protégées et difficiles à manipuler. Il doit aussi conserver un chemin vers la question initiale : pourquoi produisons-nous cet artefact, et pour qui ?

Sinon, nous aurons construit une machine exceptionnellement efficace pour obtenir des voyants verts.

Le prochain article examine une version plus discrète du même problème : quand le code et ses tests partagent dès le départ le même malentendu.

---

## Sources

- Charles Goodhart, principe formulé dans les années 1970 ; formulation courante popularisée par Marilyn Strathern · https://en.wikipedia.org/wiki/Goodhart%27s_law
- METR, *Recent Frontier Models Are Reward Hacking* (juin 2025), notamment valeurs attendues codées en dur · https://metr.org/blog/2025-06-05-recent-reward-hacking/
- Anthropic, *Claude 3.7 Sonnet System Card*, cas de special-casing en environnement agentique · https://www.anthropic.com/claude-3-7-sonnet-system-card

