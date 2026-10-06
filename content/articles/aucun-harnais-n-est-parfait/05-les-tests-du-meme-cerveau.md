---
title: "Les tests du même cerveau"
seo_title: "Tests générés par IA : le risque du juge et partie"
slug: "tests-du-meme-cerveau"
date: 2026-09-01
description: "Des tests générés avec le code peuvent confirmer avec une parfaite cohérence une mauvaise compréhension du besoin."
categories: ["Intelligence artificielle", "Ingénierie logicielle"]
tags: ["ai-evaluation-evals", "ai-reliability"]
series: ["aucun-harnais-n-est-parfait"]
series_order: 5
collection: "ARCHITECTURE"
cover: "/images/articles/05-les-tests-du-meme-cerveau.fr.png"
draft: false
---

Des tests générés avec le code peuvent prouver que le code correspond parfaitement à une mauvaise compréhension du besoin.

C'est l'un des pièges les plus discrets des harness modernes. Il ne produit pas forcément un échec visible, une triche ou un voyant rouge. Au contraire, tout peut être remarquablement cohérent.

La demande est mal comprise. Le code implémente cette compréhension. Les tests vérifient que le code lui correspond. La boucle corrige les derniers écarts et livre un ensemble propre, stable et faux.

## La cohérence n'est pas la conformité

Lorsqu'un même modèle reçoit une demande, écrit le code et génère les tests dans la même session, les trois objets partagent un contexte commun.

Cette proximité a de vrais avantages. Les tests peuvent être créés immédiatement. Ils suivent les changements de structure. Ils attrapent des erreurs locales et documentent le comportement que le modèle croit devoir produire.

Mais c'est précisément la limite : ils documentent ce que le modèle croit devoir produire.

S'il interprète "client actif" comme "client ayant déjà passé une commande", le code appliquera cette définition. Les tests fabriqueront des exemples où les deux notions coïncident. La couverture pourra atteindre 100 % sans qu'aucun contrôle ne pose la question décisive : un client nouvellement inscrit, sans commande, est-il actif ?

La suite code-tests est cohérente. Elle n'est pas conforme au métier.

## Tous les tests n'ont pas la même fonction

La solution n'est pas d'interdire la co-génération. Elle est de distinguer les niveaux de preuve.

Les tests unitaires accompagnent le développement. Ils vérifient les composants, accélèrent les corrections et protègent contre les régressions locales. Les produire dans la même boucle que le code est souvent efficace.

Les tests d'intégration vérifient que plusieurs composants respectent leurs contrats lorsqu'ils travaillent ensemble. Ils commencent à confronter la production à un environnement plus large que sa logique locale.

Les tests de qualification répondent à une question différente : le système satisfait-il le besoin qui justifie son existence ? Leur référence devrait venir du dehors. Cas métier validés, exemples réels, propriétés définies par le demandeur, données indépendantes ou résultats attendus construits séparément.

Un test unitaire peut être une aide du producteur. Un test de qualification doit rester une preuve opposable au producteur.

## Rendre le besoin exécutable

L'expression "intervention humaine" est trop vague pour résoudre ce problème. Une personne peut approuver une liste de tests sans voir que tous reposent sur la même hypothèse implicite.

La contribution la plus précieuse du métier arrive souvent plus tôt : fournir des exemples qui obligent à trancher.

Quels dossiers doivent être acceptés ? Lesquels doivent être refusés ? Quel résultat serait surprenant ? Quelle exception est fréquente sur le terrain mais absente de la procédure officielle ? À quel moment une décision change-t-elle d'état ?

Ces exemples ne sont pas une documentation décorative. Ils constituent un jeu de qualification que le générateur ne doit pas pouvoir réinterpréter silencieusement.

On peut aussi utiliser des propriétés plutôt que des cas fixes : une somme ne doit jamais devenir négative, une décision annulée ne doit plus produire d'effet, deux opérations équivalentes doivent aboutir au même résultat, une donnée sensible ne doit apparaitre dans aucun journal.

Les propriétés rendent le besoin plus difficile à contourner qu'une poignée de réponses attendues.

## Introduire une vraie différence d'origine

L'indépendance ne dépend pas seulement du modèle utilisé. Elle dépend de la provenance des critères.

Un second modèle qui génère ses tests à partir du même énoncé ambigu peut reproduire le même contresens. À l'inverse, le même modèle peut apporter un contrôle utile s'il reçoit une source indépendante : une spécification validée séparément, un contrat d'API, un historique d'incidents ou des exemples que le producteur n'a pas vus.

Il faut donc examiner deux formes de corrélation :

1. la corrélation des moteurs, lorsque production et validation utilisent le même modèle ;
2. la corrélation des références, lorsqu'elles utilisent la même compréhension initiale du besoin.

Changer de moteur sans changer de référence ne suffit pas toujours. Changer de référence peut parfois apporter davantage qu'un modèle supplémentaire.

## Tester le malentendu

Une revue robuste ne demande pas seulement "le code fait-il ce que disent les tests ?" Elle demande aussi "qu'est-ce que ces tests supposent sans le dire ?"

Cette question est inconfortable parce qu'elle ne se laisse pas automatiser entièrement. Elle oblige à retourner vers le terrain, les utilisateurs, les incidents et les cas qui résistent aux catégories propres.

Mais c'est précisément là que réside la valeur du harness. Il ne doit pas seulement accélérer la production. Il doit créer des points de contact répétés entre la production et une réalité que le générateur ne contrôle pas.

Les tests du même cerveau renforcent la cohérence interne. Pour vérifier la conformité, il faut au moins une référence venue d'ailleurs.

Et si nous ajoutions simplement plusieurs agents pour multiplier ces références ? Ce serait efficace à une condition rarement vérifiée : qu'ils ne répètent pas le même point de vue sous plusieurs noms.
C'est le sujet du prochain article.
---

## Sources

- Thoughtworks, *Harness engineering for coding agent users*, distinction entre contrôles computationnels et inférentiels · https://martinfowler.com/articles/harness-engineering.html
