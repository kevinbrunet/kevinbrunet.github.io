---
title: "Un agent qui apprend tout seul ? C’est plus complexe qu’on ne le pense."
seo_title: "Auto-apprentissage des agents IA : qui valide les leçons ?"
slug: "agent-auto-apprentissage-harness"
date: 2026-11-02
lastmod: 2026-10-30T18:30:36+01:00
description: "Une nouvelle étude montre qu’accumuler davantage d’expériences peut dégrader un harness. Apprendre de ses erreurs demande aussi de savoir quelles leçons retenir."
categories: ["Intelligence artificielle", "Architecture logicielle"]
tags: ["ai-systems-harness-engineering", "ai-evaluation-evals"]
collection: "ARCHITECTURE"
cover: "/images/articles/agent-auto-apprentissage-harness.fr.png"
draft: false
---

Une nouvelle étude, [*Forging More Tasks into Better Harnesses*](https://arxiv.org/html/2610.28815v1), publiée le 20 octobre 2026, montre un résultat contre-intuitif : **donner davantage d’expériences à un agent pour améliorer son fonctionnement peut dégrader ses performances.** Plusieurs méthodes d’évolution du *harness*, l’environnement logiciel qui pilote le modèle, régressent lorsque le nombre de tâches utilisées augmente.

La promesse est pourtant séduisante : laisser un agent travailler, apprendre de ses échecs, enrichir ses instructions et fabriquer de nouvelles *skills*, des procédures réutilisables. Plus il accumulerait d’expérience, plus il deviendrait compétent.

Le résultat de l’étude met en lumière la difficulté : **quelles expériences méritent de devenir des règles pour les suivantes ?**

{{< callout variant="scene" label="Une erreur. Une leçon. Une nouvelle erreur ?" >}}
Un agent échoue après une migration de base de données. Il analyse sa trace, identifie le problème et ajoute une consigne à sa mémoire : « Toujours vérifier les migrations avant de lancer les tests. »

La tentative suivante réussit. Puis la règle s’applique à un projet sans base de données. L’agent cherche des migrations inexistantes, perd du temps et s’éloigne du problème à résoudre.

Il a conservé une leçon. A-t-il amélioré son comportement ?
{{< /callout >}}

Entre « cette stratégie a fonctionné une fois » et « cette stratégie doit guider mes prochaines décisions », il manque une démonstration.

{{< thesis >}}
Le problème de l’auto-apprentissage commence au moment où une expérience devient une règle pour les suivantes.
{{< /thesis >}}

Ici, l’agent fait évoluer son harness : instructions, mémoire, skills et usage des outils. **Les poids du modèle restent fixes.** Il change sa manière de travailler à partir de ses expériences, sans réentraînement.

## Cinq fois plus de tâches ne garantissent pas un meilleur harness

Les chercheurs partent d’une question simple : un agent devient-il meilleur lorsqu’il dispose de davantage d’expériences pour faire évoluer son harness ? Ils font varier le nombre de tâches dont les traces servent à proposer des modifications, puis évaluent le harness obtenu sur d’autres tâches.

Avec **AHE**, une méthode existante, le harness réussit **63 %** des tâches évaluées après avoir utilisé les expériences de **80 tâches**. En lui fournissant les expériences de **200 tâches**, le taux de réussite tombe à **57,7 %**. Davantage d’expériences aboutit ici à un harness moins performant.

Les auteurs expliquent cette régression par la manière dont les expériences sont sélectionnées. Des traces redondantes ou contradictoires peuvent brouiller les changements à apporter. Leur analyse montre qu’un sous-ensemble bien choisi peut conduire à un meilleur harness que l’ensemble des expériences disponibles.

**Le problème est donc de choisir quelles expériences utiliser ensemble pour guider chaque modification.**

## Sélectionner les expériences, puis comparer les changements

C’est pour répondre à ce problème que les auteurs proposent **Successive Scale Racing (SSR)**. La méthode classe les expériences selon leur qualité et la diversité des situations couvertes. Elle utilise des groupes de tailles différentes pour produire plusieurs versions modifiées du harness, puis les compare sur des tâches communes et élimine progressivement les moins performantes.

Avec SSR, le taux de réussite passe de **64,3 % à 68,3 %** lorsque les expériences disponibles proviennent de **40, puis de 200 tâches**. Cette fois, la méthode parvient à tirer parti du nombre croissant d’expériences.

Le budget d’exécution augmente avec le nombre de tâches utilisées. Cette expérience ne mesure donc pas un gain à coût constant.

Le travail couvre trois benchmarks et deux configurations d’exécution.

Les **60 % d’exécutions de validation économisées** concernent un audit distinct : 12 candidats, 160 tâches et une comparaison à l’évaluation complète. Ce chiffre ne mesure pas une réduction de 60 % du coût total de l’agent.

Ces résultats décrivent les conditions étudiées. Ils ne prouvent ni que l’expérience nuit toujours, ni que SSR résout tout auto-apprentissage.

Pour une équipe qui conçoit son système, la question devient concrète : **quelles expériences alimentent chaque modification, et comment départager les changements proposés ?**

## Conserver, qualifier, sélectionner, promouvoir

Je propose de séparer quatre décisions dans l’architecture d’un agent qui capitalise son expérience.

| Décision | Question à résoudre | Exemple de la migration |
|---|---|---|
| **Conserver** | Que s’est-il passé ? | Garder la trace, le contexte du projet, l’échec et l’intervention. |
| **Qualifier** | Que permet d’en conclure cette expérience ? | Distinguer le fait observé de l’hypothèse sur sa cause et préciser les projets concernés. |
| **Sélectionner** | Quelles expériences réunir pour guider le changement envisagé ? | Retenir des cas de migration complémentaires, sans laisser plusieurs traces du même échec dominer la proposition. |
| **Promouvoir** | La leçon peut-elle modifier le comportement futur ? | Évaluer une consigne conditionnelle avant de l’activer. |

Cette séparation évite qu’un résumé rédigé avec assurance devienne immédiatement une instruction permanente.

Qualifier une expérience établit ce qu’elle permet de conclure. La sélectionner consiste à décider si elle est pertinente pour le changement envisagé et ce qu’elle apporte aux autres expériences retenues. Une expérience fiable peut être redondante ou concerner un autre contexte.

La mémoire peut ainsi conserver une hypothèse sans l’imposer. Elle devrait pouvoir exprimer : « Dans un projet utilisant ce mécanisme de migration, cette vérification a aidé à résoudre cet échec. » Le contexte d’application reste explicite, ce qui permet de confronter l’hypothèse aux expériences suivantes.

Une skill demande la même discipline. Son déclenchement, ses prérequis et ses critères de réussite font partie de ce qu’il faut examiner. Une procédure efficace sur un type de dépôt peut être inutile ailleurs.

## Une modification doit pouvoir perdre

Pour rendre l’amélioration mesurable, il faut conserver la possibilité de rejeter ce que l’agent propose.

Dans notre exemple, un candidat pourrait ajouter : « Si le projet utilise des migrations et que la modification touche au schéma, vérifier leur cohérence avant la suite complète. » Un autre pourrait proposer un contrôle automatisé ciblé. La version actuelle doit rester un point de comparaison.

Il faut alors exercer les cas qui ont motivé le changement, mais aussi des situations où celui-ci pourrait coûter quelque chose : projet sans base de données, modification de documentation, schéma déjà à jour. Réussite, durée et appels d’outils apportent des informations différentes. Un gain sur les migrations peut masquer un ralentissement général.

Le candidat doit être associé à une version et à un différentiel lisible. Les expériences à l’origine de la proposition, les évaluations effectuées et leurs résultats permettent de comprendre pourquoi il a été retenu. Si le comportement se dégrade après activation, la version précédente doit rester récupérable.

Ce sont des choix d’architecture proposés ici, au-delà de la méthode SSR. Leur objectif est de transformer une intuition en changement comparable, observable et réversible.

{{< pullquote >}}
Un agent peut proposer une évolution, mais son bien-fondé doit être évalué indépendamment.
{{< /pullquote >}}

Cette indépendance peut venir de tests déterministes, de tâches réservées à l’évaluation ou d’une revue humaine pour les changements sensibles. Faire reformuler la même justification par le même modèle apporte peu de preuves supplémentaires.

## Et s’il apprenait surtout à réussir nos tests ?

À force de consulter le même jeu de tests, une boucle d’amélioration peut s’adapter à ses particularités. Un score en hausse ne garantit alors pas de meilleurs résultats sur les prochaines tâches.

Une autre étude, [*Rethinking the Evaluation of Harness Evolution for Agents*](https://arxiv.org/html/2607.12227v1), pose une question concrète : **avec le même budget de calcul, vaut-il mieux modifier le harness ou laisser l’agent actuel essayer plusieurs fois ?**

Les chercheurs comparent ces options sur Terminal-Bench 2.1, un ensemble de tâches à réaliser dans un terminal. Ils donnent aux méthodes des moyens de calcul et des informations comparables sur la réussite ou l’échec des tentatives. Modifier le harness ne fait pas systématiquement mieux que conserver sa configuration et essayer plusieurs solutions, ou corriger une première tentative.

Cette possibilité m’intéresse particulièrement : **exploiter la variance des réponses pour chercher une solution que la première tentative n’a pas trouvée.** Un même modèle peut suivre des chemins différents d’une exécution à l’autre. Si un contrôle fiable permet de reconnaître une solution acceptable, le système peut profiter de cette diversité et s’arrêter lorsqu’il la trouve. C’est le principe développé dans la série [L’oracle]({{< relref "/series/l-oracle" >}}), qui examine les tentatives vérifiées et la complémentarité des modèles. Multiplier les essais aide surtout lorsqu’ils explorent des pistes différentes et que l’on sait en vérifier le résultat.

Les auteurs de l’étude évaluent aussi le harness modifié sur des tâches qui n’ont pas servi à guider ses changements. **Sur ces nouvelles tâches, l’amélioration reste faible.** Un gain sur les exercices utilisés pour modifier l’agent ne garantit donc pas qu’il réussira mieux les suivants.

Ce travail ne constitue pas une réfutation expérimentale de SSR : les protocoles et les configurations diffèrent. Il pose une exigence utile pour apprécier toute amélioration annoncée : séparer le gain transférable de l’effet du calcul supplémentaire et de l’adaptation aux cas évalués.

Dans une architecture opérationnelle, je conserverais donc des tâches indépendantes de la boucle d’optimisation, un suivi des régressions par catégorie et une comparaison avec l’option simple : garder le harness actuel et consacrer le même budget à mieux résoudre la tâche.

Un ensemble de tests devient de fait un outil d’optimisation dès que ses résultats servent régulièrement à choisir les modifications. Il faut préserver une autre mesure pour estimer ce que le système a réellement gagné.

## Automatiser l’apprentissage, démontrer le progrès

Automatiser la capture d’expérience est utile. Automatiser la proposition de changements l’est aussi. Mais leur valeur dépend du mécanisme qui décide quelles leçons méritent de devenir durables.

Dans la série [Aucun harnais n’est parfait]({{< relref "/series/aucun-harnais-n-est-parfait" >}}), la fiabilité dépend déjà des limites de nos contrôles. L’auto-apprentissage ajoute une responsabilité : vérifier que les changements issus de ces contrôles améliorent les prochaines exécutions.

L’ingénierie se déplace vers la sélection des expériences, la comparaison des candidats et la surveillance des effets. Elle doit aussi savoir oublier une règle devenue fausse ou trop coûteuse.

**Un agent qui change tout seul ne devient pas forcément meilleur. C’est à l’architecture d’en apporter la preuve.**

{{< closing-question label="La question d’architecture" >}}
Votre agent sait enregistrer une nouvelle leçon. Quel mécanisme peut démontrer qu’elle mérite de guider les tâches suivantes, puis la retirer si elle les dégrade ?
{{< /closing-question >}}

## Sources

- Jingzhe Liu et al., [*Forging More Tasks into Better Harnesses: Agentic Harness Evolution via Successive Scale Racing*](https://arxiv.org/html/2610.28815v1), arXiv:2610.28815v1, 20 octobre 2026.
- Yike Wang et al., [*Rethinking the Evaluation of Harness Evolution for Agents*](https://arxiv.org/html/2607.12227v1), arXiv:2607.12227v1, 14 juillet 2026.
