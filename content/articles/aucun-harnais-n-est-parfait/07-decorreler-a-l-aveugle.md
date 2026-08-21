---
title: "Décorréler à l'aveugle"
seo_title: "Évaluation d'agents IA : préserver des avis indépendants"
slug: "decorreler-a-l-aveugle"
date: 2026-10-13
description: "Une évaluation indépendante exige de préserver les désaccords avant de faire dialoguer les agents ou de chercher un consensus."
categories: ["Intelligence artificielle", "Ingénierie logicielle"]
series: ["aucun-harnais-n-est-parfait"]
series_order: 7
collection: "ARCHITECTURE"
cover: "/images/articles/07-decorreler-a-l-aveugle.fr.png"
draft: false
---

Pour obtenir deux avis indépendants, il ne faut pas commencer par faire discuter les deux évaluateurs.

Cette conclusion va contre l'image séduisante du débat multi-agents. On imagine plusieurs modèles échangeant leurs arguments, se corrigeant mutuellement puis convergeant vers une réponse supérieure.

L'échange peut aider. Il peut aussi détruire précisément la propriété que l'on cherchait : l'indépendance des jugements.

## Le désaccord doit avoir le temps d'exister

Supposons que deux modèles différents examinent une modification sensible. Le premier conclut qu'elle est sûre. Le second détecte un risque.

Si le second voit immédiatement la conclusion du premier, son analyse ne part plus du même point. Il peut chercher à confirmer l'opinion déjà exprimée, se rallier à un raisonnement convaincant ou concentrer son attention sur les éléments choisis par l'autre.

Le premier avis devient une ancre.

À l'inverse, si les deux modèles travaillent séparément, chacun doit construire sa propre représentation du problème. La comparaison finale conserve davantage d'information. Un accord a plus de valeur parce qu'il n'a pas été négocié. Un désaccord a plus de valeur encore, puisqu'il révèle une zone où au moins une compréhension est insuffisante.

Décorréler à l'aveugle signifie donc : produire les jugements séparément, sans accès à la conclusion ou au raisonnement de l'autre, puis comparer les verdicts.

## Le désaccord n'est pas une erreur à faire disparaitre

Dans beaucoup de workflows, le désaccord déclenche immédiatement un arbitre chargé de choisir la bonne réponse. Cette étape peut être nécessaire. Elle ne doit pas effacer le signal.

Le désaccord est une observation sur le système de validation lui-même. Il indique que le cas se trouve près d'une frontière entre deux représentations. Même si l'un des modèles a clairement raison après vérification, l'écart mérite d'être journalisé.

Avec le temps, ces écarts dessinent une carte empirique :

- quelles catégories de demandes divisent les évaluateurs
- quel modèle manque régulièrement quel type de défaut
- quels désaccords annoncent un incident réel
- quelles divergences restent purement stylistiques
- quels cas doivent désormais recevoir une qualification humaine

Cette carte ne peut pas être entièrement dessinée à l'avance. Connaitre tous les angles morts avant de commencer supposerait précisément de ne plus en avoir.

## Une architecture minimale

Une boucle décorrélée peut rester simple.

Le producteur génère un artefact. Deux évaluateurs reçoivent séparément cet artefact ainsi que les critères de qualification. Ils rendent un verdict structuré : accepté, refusé ou incertain, avec les propriétés qui motivent leur décision.

Un mécanisme déterministe compare ensuite les résultats.

En cas d'accord favorable, le workflow continue selon le niveau de risque. En cas d'accord défavorable, la production repart en correction. En cas de désaccord, le système route vers une revue humaine, un test supplémentaire ou un troisième évaluateur.

Le "chef" n'a pas besoin d'être un agent supposé plus sage. Il peut être une fonction de routage sans opinion propre. Son rôle n'est pas de produire la vérité. Il est de reconnaitre la configuration qui exige davantage d'information.

Cette idée rejoint plusieurs architectures plus anciennes. Les systèmes de mixture of experts utilisent une fonction de gating pour choisir quel expert mobiliser. Le boosting réévalue le poids des classifieurs à partir des erreurs observées. Les systèmes tolérants aux pannes cherchent à éviter qu'une source unique de défaillance contamine toute la décision.

Le vocabulaire change. Le principe reste : la robustesse ne vient pas seulement du nombre de composants, mais de la structure de leurs dépendances.

## Toutes les différences ne se valent pas

Utiliser deux marques de modèles ne garantit pas une décorrélation suffisante. Pour une tâche donnée, il faut examiner plusieurs dimensions :

- famille et données d'entrainement
- prompt et rôle de l'évaluateur
- outils accessibles
- références utilisées pour juger
- visibilité sur les tests et la production
- équipe qui entretient les critères
- type de contrôle, probabiliste ou déterministe

Un analyseur statique apporte parfois plus d'indépendance qu'un deuxième grand modèle. Un exemple métier indépendant peut apporter plus qu'un long débat. Un test caché peut casser un angle mort que trois reviewers conversationnels renforçaient ensemble.

La bonne combinaison dépend donc de la classe de risque, pas d'un dogme "toujours deux modèles".

## Commencer par échantillonner

Faire tourner plusieurs évaluateurs sur toutes les productions peut coûter cher. Une organisation peut commencer par un échantillonnage : un pourcentage de cas reçoit un second regard indépendant, avec suréchantillonnage des domaines risqués ou mal connus.

Les désaccords sont conservés, examinés et reliés aux résultats réels. Si une catégorie concentre les divergences utiles, le second contrôle devient systématique pour cette catégorie. Si un évaluateur ne produit aucune information nouvelle, il est remplacé.

Le harness apprend ainsi où acheter de la diversité.

Décorréler à l'aveugle n'est donc pas une cérémonie où deux modèles votent. C'est une discipline de conception : protéger l'indépendance avant la comparaison, traiter le désaccord comme une donnée et adapter le coût de validation à ce que l'expérience révèle.

Cette discipline conduit à la conclusion de la série. Puisqu'aucun dispositif ne voit tout, la diversité doit être organisée à l'échelle de l'entreprise sans devenir un chaos impossible à gouverner.
C'est ce que nous verrons la semaine prochaine.

---

## Sources

- *The Deliberative Illusion*, avril/juin 2026 selon version, sur la conformité majoritaire et l'homogénéisation en débat multi-agents · https://arxiv.org/pdf/2606.03032
- Jacobs, Jordan, Nowlan et Hinton, *Adaptive Mixtures of Local Experts* (1991), fonction de gating
- Freund et Schapire, AdaBoost (1997), agrégation pondérée par l'erreur observée
- Lamport, Shostak et Pease, *The Byzantine Generals Problem* (1982), robustesse face aux défaillances distribuées
- Architecture précise proposée ici, notamment journalisation et routage du désaccord : proposition à tester empiriquement ~

