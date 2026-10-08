---
title: "Le modèle le plus cher devrait peut-être passer en dernier"
seo_title: "Agents IA : pourquoi le modèle le plus cher peut passer en dernier"
slug: "meilleur-modele-meilleur-complement"
date: 2026-10-27
description: "Sur 113 tâches DeepSWE, inverser l’ordre des mêmes modèles réduit le coût simulé de 36 %, sans perdre un seul verdict positif."
categories: ["Intelligence artificielle", "Architecture logicielle", "Ingénierie logicielle"]
tags: ["ai-evaluation-evals", "llmops-agentops"]
series: ["l-oracle"]
series_order: 2
collection: "SYSTÈMES"
cover: "/images/articles/meilleur-complement.fr.png"
draft: false
---

{{< callout variant="scene" label="De la variance à la complémentarité" >}}
Dans le premier article, nous avons vu qu’un oracle permettait de donner plusieurs chances à Luna. Avec jusqu’à quatre essais, le modèle résout au moins une fois **102 tâches sur 113**.

Mais comment aller chercher la réussite sur les 11 tâches restantes ?

**En cherchant son complément : non pas le meilleur modèle dans l’absolu, mais celui qui réussit précisément là où Luna échoue.**
{{< /callout >}}

Pour le trouver, il faut changer de classement : ne plus mesurer seulement la performance moyenne de chaque modèle, mais comparer les profils d’erreurs.

## Un classement cache les profils d'erreurs

Un leaderboard range les modèles sur un axe : leur performance moyenne.

Cette mesure répond à une question utile : si je ne peux lancer qu'une seule exécution, quel modèle possède la meilleure probabilité de réussir ?

Elle ne répond pas à une autre question, pourtant essentielle pour une architecture agentique : lorsqu'un premier modèle échoue, lequel a le plus de chances de réussir précisément sur ses échecs ?

Les données détaillées de [**DeepSWE 1.1**](https://deepswe.datacurve.ai/) permettent de suivre, tâche par tâche, jusqu’à quatre exécutions de chaque configuration. Nous nous concentrons sur les 11 tâches où Luna n’obtient aucun verdict positif. Elles constituent ses « angles morts » observés sur ce benchmark (pas une incapacité absolue).

Comme dans le premier article, une tâche « résolue » désigne un verdict positif du grader. Tous les résultats comparés ici utilisent le même harness, `mini-swe-agent`, avec les niveaux d’effort indiqués.

Pour trouver ce complément, nous pouvons comparer chaque configuration sur deux axes : le nombre d’échecs de Luna qu’elle récupère et le coût de cette escalade. Quatre configurations dont le coût d’un essai manque sont exclues. Les 66 autres apparaissent dans le graphique.

{{< scatter-chart
  dataset="deepswe-luna-cost-recovery"
  title="Quel modèle complète Luna au meilleur coût ?"
  description="Chaque point représente une configuration appliquée aux 11 échecs de Luna. Plus il est haut, plus il récupère de tâches. Plus il est à gauche, moins cette escalade coûte."
  x-label="Coût estimé de l’escalade sur les 11 échecs ($)"
  y-label="Échecs de Luna récupérés, sur 11"
  x-min="0.5" x-max="500"
  y-min="0" y-max="11"
  regression="none"
  primary="mini_swe_agent_glm_5_3_flash_max"
  count-label="configurations aux coûts complets"
  y-total="11"
  x-format="currency"
  x-scale="log"
  tooltip-x="Coût de l’escalade"
  tooltip-y="Échecs récupérés"
  tooltip-ratio="Coût par échec récupéré"
  tooltip-attempts="Essais exécutés"
  attempts-label="Essais exécutés"
  details-label="Consulter les 66 configurations"
>}}
GLM-5.3 Flash [max], en bleu, offre ici le meilleur rapport entre le nombre d’échecs récupérés et le coût de l’escalade. L’axe des coûts est logarithmique afin de rendre lisibles les modèles bon marché comme les plus coûteux. Les coûts simulent un arrêt au premier succès sur les 11 échecs de Luna. La convention tarifaire est celle de l’analyse au 6 octobre 2026.
{{< /scatter-chart >}}

En simulant une reprise par GLM Flash sur les 11 tâches non résolues par Luna, on peut enchaîner jusqu’à quatre essais supplémentaires et s’arrêter dès le premier verdict positif.

| Étape | Nouvelles tâches récupérées à cet essai | Échecs de Luna récupérés au total | Tâches encore non résolues | Couverture combinée Luna + GLM Flash |
|---|---:|---:|---:|---:|
| Avant GLM Flash | — | 0 sur 11 | 11 | 102 sur 113, soit 90,3 % |
| **Essai 1** | **3** | **3 sur 11** | 8 | 105 sur 113, soit 92,9 % |
| **Essai 2** | **7** | **10 sur 11** | 1 | 112 sur 113, soit 99,1 % |
| **Essai 3** | 0 | 10 sur 11 | 1 | 112 sur 113, soit 99,1 % |
| **Essai 4** | 0 | **10 sur 11** | **1** | **112 sur 113, soit 99,1 %** |

Dans cet ordre de rejeu, la première tentative de GLM Flash récupère 3 des 11 échecs de Luna. La deuxième en ajoute 7. Les suivantes n’apportent aucun succès supplémentaire.

{{< thesis >}}
Ces chiffres ne disent pas que GLM-5.3 Flash est meilleur qu'Astra dans l'absolu. Ils montrent que ses succès enregistrés recouvrent davantage les échecs observés de Luna.

**C'est une autre définition de la diversité.**
{{< /thesis >}}

## La diversité ne se compte pas en modèles

Deux modèles peuvent produire des réponses différentes tout en échouant sur les mêmes problèmes. À l'inverse, un modèle moins performant en moyenne peut apporter énormément s'il réussit là où le premier bloque.

Compter les modèles ne suffit donc pas. Il faut mesurer la complémentarité de leurs erreurs.

Cette idée était au cœur de ma série [« Aucun harness n'est parfait »](/series/aucun-harnais-n-est-parfait/). Dans [« Pourquoi ajouter des agents ne crée pas forcément de diversité »](/articles/plusieurs-agents-points-de-vue/), je défendais que la diversité devait devenir une propriété empirique du système, observée à travers les désaccords et les erreurs utiles.

DeepSWE en fournit ici une illustration particulièrement nette. Astra obtient un meilleur score que Luna sur une exécution moyenne. Pourtant, lorsqu’on examine uniquement les échecs persistants de Luna, il apporte moins de couverture supplémentaire que GLM-5.3 Flash.

La bonne question n'est donc plus : quel est le meilleur modèle ?

{{< pullquote >}}
Quel modèle récupère le mieux les échecs qui restent après le passage du précédent ?
{{< /pullquote >}}

## L'oracle transforme la diversité en routage

Cette complémentarité ne devient exploitable que si le système sait reconnaître un échec.

Sans oracle, il faudrait lancer plusieurs modèles puis demander à une personne de déterminer quelle réponse est correcte. Le coût de supervision augmenterait avec le nombre de propositions.

Avec des tests capables d'accepter ou de rejeter automatiquement le résultat, le harness peut s'arrêter au premier succès et n'escalader que les tâches qui résistent.

```text
Luna, jusqu'à quatre tentatives
        ↓ échec vérifié
GLM-5.3 Flash, jusqu'à quatre tentatives
        ↓ échec vérifié
Dernier niveau de secours
```

L'architecture n'oppose plus un modèle économique à un modèle premium. Elle compose plusieurs profils d'erreurs et réserve chaque étage aux cas que le précédent n'a pas résolus.

## Une fois le complément trouvé, il faut encore choisir l’ordre

Une fois cette logique admise, une autre question apparaît : dans quel ordre faut-il appeler les modèles ?

Luna possède la meilleure couverture individuelle des deux, mais GLM-5.3 Flash coûte moins cher. Il peut donc être économiquement préférable de commencer par GLM Flash, puis d'envoyer uniquement ses échecs à Luna.

Sur une exécution moyenne, GLM Flash réussit 63,4 % des tâches pour environ 0,24 dollar, contre 67,2 % pour 0,61 dollar avec Luna. Le système abandonne seulement 3,8 points de réussite moyenne au premier passage, mais réduit d’environ 60 % le coût moyen d’un essai. L’oracle permet de récupérer ensuite les échecs au lieu de payer Luna sur toutes les tâches.

{{< cost-comparison
  dataset="deepswe-routing-orders"
  title="Même couverture, 36 % de coût en moins"
  description="Les deux chaînes obtiennent 113 verdicts positifs. Changer uniquement l’ordre de GLM Flash et Luna fait passer le coût estimé de 119,31 à 76,46 dollars."
  x-label="Coût estimé sur 113 tâches ($)"
  primary="glm-first"
  cost-label="Coût estimé"
  coverage-label="Verdicts positifs"
  attempts-label="Tentatives exécutées"
  scenario-label="Ordre de routage"
  count-label="ordres comparés"
  details-label="Consulter les deux scénarios"
>}}
Chaque barre représente le coût total d’un rejeu avec arrêt au premier succès. Les deux ordres utilisent les mêmes trois configurations et atteignent la même couverture observée. Seule leur séquence change.
{{< /cost-comparison >}}

Après le passage de GLM Flash puis de Luna, une seule tâche reste sans verdict positif. Pour ce dernier cas, on peut accepter de payer un modèle plus premium. Dans cet exemple, j’ai choisi GLM-5.2 [max].

Comme toujours, à partir des rollouts publiés par DeepSWE, avec arrêt au premier succès, la chaîne rétrospective suivante donne :

| Étape | Tâches reçues | Tâches résolues à cette étape | Tentatives exécutées | Coût estimé |
|---|---:|---:|---:|---:|
| GLM-5.3 Flash [max] | 113 | 96 | 204 | 49,74 $ |
| Luna [max] sur les échecs | 17 | 16 | 34 | 20,71 $ |
| GLM-5.2 [max] sur le dernier cas | 1 | 1 | 1 | 6,02 $ |
| **Total rétrospectif** | **113** | **113** | **239** | **76,46 $** |

Ces coûts sont estimés à partir de la consommation des rollouts, avec les tarifs utilisés par l’interface DeepSWE au 6 octobre 2026. Ils excluent le coût complet de l’oracle et de son exploitation.

Cela représente environ 0,68 dollar par tâche soumise et 2,12 tentatives par tâche. Une tentative correspond à une exécution de l’agent, qui peut effectuer plusieurs appels au modèle.

{{< callout variant="key" label="42,85 dollars économisés sur 113 tâches" >}}
L’ordre inverse coûte 119,31 dollars. Commencer par GLM Flash ramène la facture estimée à 76,46 dollars : **42,85 dollars de moins, soit environ 36 % d’économie**, avec la même couverture observée.

À volume et répartition comparables, cet écart représenterait environ **3 792 dollars d’économie brute pour 10 000 tâches**, avant le coût de l’oracle. La valeur vient du fait que **238 des 239 tentatives sont confiées aux deux modèles économiques**.
{{< /callout >}}

L’ordre GLM Flash → Luna → GLM-5.2 exige toutefois 30 tentatives supplémentaires et peut augmenter la latence.

Le meilleur ordre dépend donc de l’objectif choisi : coût, latence, consommation de calcul ou niveau de risque accepté.

## Le benchmark le plus utile peut venir de votre production

DeepSWE constitue ici un exemple public. Il ne représente évidemment pas les tâches, les contraintes et les risques propres à chaque organisation.

Mais un système agentique en production génère précisément la matière nécessaire pour construire un benchmark interne : demandes réelles, contexte disponible, résultats produits, verdicts de l'oracle, corrections humaines, coûts, latence et motifs d'escalade.

En collectant ces scénarios, puis en les anonymisant et en les rendant rejouables, une équipe peut progressivement constituer un jeu de qualification représentatif de son utilisation. Les cas fréquents y conservent leur poids réel. Les incidents, les cas limites et les tâches à fort impact peuvent y être surreprésentés volontairement pour refléter le risque qu'ils portent. Cette démarche relève des **AI Evals** et, plus largement, de l’**AI Reliability**.

Il devient alors possible de reproduire la même analyse que sur DeepSWE :

- exécuter plusieurs modèles et configurations sur les mêmes scénarios
- observer non seulement leur score moyen, mais aussi leurs angles morts respectifs
- mesurer quels modèles récupèrent réellement les échecs des autres
- simuler plusieurs ordres de routage avec arrêt au premier succès
- comparer la couverture obtenue au coût, à la latence et au risque résiduel.

L'optimisation ne porte plus sur « le meilleur modèle du marché ». Elle porte sur **la meilleure combinaison de modèles pour une utilisation précise**.

Ce benchmark doit rester vivant. Les nouveaux scénarios, les reprises humaines et les incidents enrichissent continuellement la carte des erreurs. Une partie des données peut servir à choisir la stratégie. Une autre doit rester à l'écart pour vérifier qu'elle fonctionne encore sur des cas qu'elle n'a pas utilisés pour s'optimiser.

Le trafic de production ne fournit donc pas seulement des tâches à traiter. Bien instrumenté, il fournit aussi le banc d'essai qui permet d'améliorer le système à partir de sa propre réalité.

## Après le choix du modèle, le choix du portefeuille

La méthode appliquée à DeepSWE n’est donc pas une recette universelle. Elle montre une méthodologie que chaque organisation peut appliquer à ses propres scénarios.

Nous comparons encore souvent les modèles comme s'il fallait élire un vainqueur unique.

Une architecture agentique pose un problème différent. Elle peut essayer, vérifier, recommencer et changer de stratégie. Sa performance dépend alors autant de l'ordre des modèles, de la complémentarité de leurs erreurs et de la qualité de l'oracle que du score individuel de chacun.

Le premier modèle doit résoudre la majorité des tâches à faible coût. Le suivant doit surtout voir ce que le premier ne voit pas. Le modèle premium ou l'humain n'intervient que sur le résidu réellement difficile.

On ne cherche plus seulement le meilleur modèle. On construit un portefeuille de capacités dont les risques sont imparfaitement corrélés.

La prochaine frontière ne sera peut-être pas gagnée par le modèle placé en tête d'un classement public. Elle pourrait l'être par le système qui saura apprendre de ses scénarios réels, mesurer ses erreurs, acheter la bonne diversité et router chaque échec vers le complément le plus utile.

{{< closing-question label="À retenir" >}}
Un modèle économique couvre 102 tâches. Un second modèle Flash récupère 10 de ses 11 échecs observés. En plaçant le modèle le moins cher en premier, la chaîne simulée conserve sa couverture et coûte **36 % de moins**, soit 42,85 dollars économisés sur ces 113 tâches.

La question suivante devient alors décisive : **qui vérifie l’oracle ?**
{{< /closing-question >}}

---

## Sources

- DeepSWE, [classement v1.1, méthodologie et coûts](https://deepswe.datacurve.ai/), 113 tâches issues de 91 dépôts open source et couvrant cinq langages, consultation du 6 octobre 2026.
- DeepSWE, [données détaillées des tâches et des rollouts](https://deepswe.datacurve.ai/data/v1.1), calculs de couverture, de complémentarité et de coût avec arrêt au premier succès.
