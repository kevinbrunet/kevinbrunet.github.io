---
title: "Le modèle le plus cher devrait peut-être passer en dernier"
seo_title: "Agents IA : pourquoi le modèle le plus cher peut passer en dernier"
slug: "meilleur-modele-meilleur-complement"
date: 2026-10-01
description: "Après l'échec d'un premier modèle, le meilleur complément est celui dont les angles morts sont différents, pas nécessairement celui qui domine le classement."
categories: ["Intelligence artificielle", "Architecture logicielle", "Ingénierie logicielle"]
series: ["l-oracle"]
series_order: 2
collection: "SYSTÈMES"
cover: "/images/articles/meilleur-complement.fr.png"
draft: false
---

{{< callout variant="scene" label="Onze angles morts" >}}
Après quatre tentatives, GPT-5.6 Luna résout 102 des 113 tâches du benchmark DeepSWE.

Il lui reste 11 angles morts.

On pourrait alors escalader vers le modèle le plus puissant du classement. Pourtant, GPT-6 Astra ne récupère que 5 de ces 11 tâches.

Un modèle beaucoup moins cher fait nettement mieux : **GLM-5.3 Flash en récupère 10**.

**Le meilleur modèle n'est donc pas nécessairement le meilleur complément. Pour construire un système agentique fiable, il faut regarder non seulement le score de chaque modèle, mais aussi la manière dont leurs erreurs se recouvrent.**
{{< /callout >}}

## Un classement cache les profils d'erreurs

Un leaderboard range les modèles sur un axe : leur performance moyenne.

Cette mesure répond à une question utile : si je ne peux lancer qu'une seule exécution, quel modèle possède la meilleure probabilité de réussir ?

Elle ne répond pas à une autre question, pourtant essentielle pour une architecture agentique : lorsqu'un premier modèle échoue, lequel a le plus de chances de réussir précisément sur ses échecs ?

Les données détaillées de [DeepSWE 1.1](https://deepswe.datacurve.ai/) permettent de l'observer. Chaque configuration a été exécutée jusqu'à quatre fois sur 113 tâches de génie logiciel. Luna `[max]` en résout au moins une fois 102. Onze tâches résistent à ses quatre exécutions.

Parmi les 70 configurations présentes dans les données, GLM-5.3 Flash `[max]` est celle qui complète le mieux Luna : il réussit au moins une fois 10 de ces 11 tâches.

Il faut bien lire ce résultat comme une escalade. GLM Flash ne reprend pas les 113 tâches depuis le début. Il reçoit seulement les 11 tâches que Luna n'a résolues lors d'aucune de ses quatre exécutions. On regarde ensuite à quelle tentative de GLM Flash chacune de ces tâches est réussie pour la première fois.

| Étape | Nouvelles tâches récupérées à cet essai | Échecs de Luna récupérés au total | Tâches encore non résolues | Couverture combinée Luna + GLM Flash |
|---|---:|---:|---:|---:|
| Avant GLM Flash | — | 0 sur 11 | 11 | 102 sur 113, soit 90,3 % |
| **Essai 1** | **5** | **5 sur 11** | 6 | 107 sur 113, soit 94,7 % |
| **Essai 2** | **2** | **7 sur 11** | 4 | 109 sur 113, soit 96,5 % |
| **Essai 3** | **1** | **8 sur 11** | 3 | 110 sur 113, soit 97,3 % |
| **Essai 4** | **2** | **10 sur 11** | **1** | **112 sur 113, soit 99,1 %** |

Dès la première tentative de GLM Flash, 5 des 11 blocages persistants de Luna disparaissent. Une deuxième tentative en récupère 2 de plus. La troisième en ajoute 1, puis la quatrième les 2 derniers succès observés. Il ne reste alors qu'une seule tâche non résolue par ce couple de modèles.

Ce tableau ne donne donc pas quatre scores indépendants. Il montre la progression cumulative permise par l'oracle : après chaque échec, une nouvelle tentative n'est lancée que pour les tâches qui résistent encore.

| Modèle ajouté après Luna | Échecs de Luna récupérés | Couverture combinée |
|---|---:|---:|
| **GLM-5.3 Flash [max]** | **10 sur 11** | **112 sur 113, soit 99,1 %** |
| Claude Opus 5 [medium] | 9 sur 11 | 111 sur 113, soit 98,2 % |
| Claude Sonnet 5 [max] | 8 sur 11 | 110 sur 113, soit 97,3 % |
| GPT-6 Astra [xhigh] | 5 sur 11 | 107 sur 113, soit 94,7 % |

{{< thesis >}}
Ces chiffres ne disent pas que GLM-5.3 Flash est meilleur qu'Astra dans l'absolu. Ils montrent que ses forces tombent beaucoup plus souvent dans les angles morts de Luna.

**C'est une autre définition de la diversité.**
{{< /thesis >}}

## La diversité ne se compte pas en modèles

Deux modèles peuvent produire des réponses différentes tout en échouant sur les mêmes problèmes. À l'inverse, un modèle moins performant en moyenne peut apporter énormément s'il réussit là où le premier bloque.

Compter les modèles ne suffit donc pas. Il faut mesurer la complémentarité de leurs erreurs.

Cette idée était au cœur de ma série [« Aucun harness n'est parfait »](/series/aucun-harnais-n-est-parfait/). Dans [« Pourquoi ajouter des agents ne crée pas forcément de diversité »](/articles/plusieurs-agents-points-de-vue/), je défendais que la diversité devait devenir une propriété empirique du système, observée à travers les désaccords et les erreurs utiles.

DeepSWE en fournit ici une illustration particulièrement nette. Astra obtient un meilleur score que Luna sur une exécution moyenne. Pourtant, lorsqu'on lui présente uniquement les échecs persistants de Luna, il apporte moins de couverture supplémentaire que GLM-5.3 Flash.

La bonne question n'est donc plus : quel est le meilleur modèle ?

{{< pullquote >}}
Quel modèle réduit le mieux le risque qui reste après le passage du précédent ?
{{< /pullquote >}}

## L'oracle transforme la diversité en routage

Cette complémentarité ne devient exploitable que si le système sait reconnaître un échec.

Sans oracle, il faudrait lancer plusieurs modèles puis demander à une personne de déterminer quelle réponse est correcte. Le coût de supervision augmenterait avec le nombre de propositions.

Avec des tests capables d'accepter ou de rejeter automatiquement le résultat, le harness peut s'arrêter au premier succès et n'escalader que les tâches qui résistent.

Le système n'a donc pas besoin de payer systématiquement quatre nouvelles tentatives. Comme le montre la progression précédente, l'oracle arrête GLM Flash dès qu'une tâche est validée et réserve les essais suivants aux seuls cas encore en échec.

```text
Luna, jusqu'à quatre tentatives
        ↓ échec vérifié
GLM-5.3 Flash, jusqu'à quatre tentatives
        ↓ échec vérifié
Dernier niveau de secours
```

L'architecture n'oppose plus un modèle économique à un modèle premium. Elle compose plusieurs profils d'erreurs et réserve chaque étage aux cas que le précédent n'a pas résolus.

## Le modèle le moins cher peut passer en premier

Une fois cette logique admise, une autre question apparaît : dans quel ordre faut-il appeler les modèles ?

Luna possède la meilleure couverture individuelle des deux, mais GLM-5.3 Flash coûte moins cher. Il peut donc être économiquement préférable de commencer par GLM Flash, puis d'envoyer uniquement ses échecs à Luna.

À partir des rollouts publiés par DeepSWE, avec arrêt au premier succès, la chaîne rétrospective suivante donne :

| Étape | Tâches reçues | Tâches résolues à cette étape | Tentatives exécutées | Coût observé |
|---|---:|---:|---:|---:|
| GLM-5.3 Flash [max] | 113 | 96 | 206 | 47,70 $ |
| Luna [max] sur les échecs | 17 | 16 | 30 | 20,15 $ |
| GLM-5.2 [max] sur le dernier cas | 1 | 1 | 1 | 6,02 $ |
| **Total rétrospectif** | **113** | **113** | **237** | **73,87 $** |

Cela représente environ 0,65 dollar par tâche soumise. La valeur de la chaîne ne vient pas d'un nombre réduit d'appels : elle effectue en moyenne 2,10 tentatives par tâche.

{{< callout variant="key" label="Le coût change d'étage" >}}
La valeur vient du fait que **236 des 237 appels sont confiés aux deux modèles économiques**.
{{< /callout >}}

L'ordre inverse, Luna puis GLM Flash, consomme moins de tentatives mais coûte 123,05 dollars. Commencer par GLM Flash économise ainsi environ 40 %, au prix de 26 appels supplémentaires et d'une latence potentiellement supérieure.

Le meilleur ordre dépend donc de la boussole choisie : coût, latence, consommation de calcul ou niveau de risque accepté.

## Le 113 sur 113 dont il faut se méfier

La chaîne GLM Flash → Luna → GLM-5.2 couvre les 113 tâches du benchmark dans les données observées.

Ce résultat est spectaculaire. Il ne constitue pas une promesse de réussite parfaite.

Les modèles, leur configuration et leur ordre ont été choisis après avoir examiné leurs résultats sur ces mêmes 113 tâches. La chaîne bénéficie donc d'une optimisation *a posteriori*. Elle peut avoir appris les particularités du benchmark plutôt qu'une stratégie qui se généralisera.

Le résultat défendable est double :

- l'union observée de Luna et GLM-5.3 Flash atteint 99,1 % ;
- leurs profils d'erreurs sont suffisamment différents pour qu'un routage avec oracle mérite d'être testé prospectivement.

Pour estimer la performance réelle, il faudrait choisir la politique sur un premier ensemble de tâches, puis la rejouer sans modification sur un échantillon inédit provenant du trafic visé. On mesurerait alors sa couverture, son coût, sa latence, ses faux positifs et ses faux négatifs.

Cette précaution n'est pas un détail statistique. Une architecture agentique est elle-même une hypothèse qu'il faut soumettre à un oracle extérieur.

## Le benchmark le plus utile peut venir de votre production

DeepSWE constitue ici un exemple public. Il ne représente évidemment pas les tâches, les contraintes et les risques propres à chaque organisation.

Mais un système agentique en production génère précisément la matière nécessaire pour construire un benchmark interne : demandes réelles, contexte disponible, résultats produits, verdicts de l'oracle, corrections humaines, coûts, latence et motifs d'escalade.

En collectant ces scénarios, puis en les anonymisant et en les rendant rejouables, une équipe peut progressivement constituer un jeu de qualification représentatif de son utilisation. Les cas fréquents y conservent leur poids réel. Les incidents, les cas limites et les tâches à fort impact peuvent y être surreprésentés volontairement pour refléter le risque qu'ils portent.

Il devient alors possible de reproduire la même analyse que sur DeepSWE :

- exécuter plusieurs modèles et configurations sur les mêmes scénarios ;
- observer non seulement leur score moyen, mais aussi leurs angles morts respectifs ;
- mesurer quels modèles récupèrent réellement les échecs des autres ;
- simuler plusieurs ordres de routage avec arrêt au premier succès ;
- comparer la couverture obtenue au coût, à la latence et au risque résiduel.

L'optimisation ne porte plus sur « le meilleur modèle du marché ». Elle porte sur **la meilleure combinaison de modèles pour une utilisation précise**.

Ce benchmark doit rester vivant. Les nouveaux scénarios, les reprises humaines et les incidents enrichissent continuellement la carte des erreurs. Une partie des données peut servir à choisir la stratégie ; une autre doit rester à l'écart pour vérifier qu'elle fonctionne encore sur des cas qu'elle n'a pas utilisés pour s'optimiser.

Le trafic de production ne fournit donc pas seulement des tâches à traiter. Bien instrumenté, il fournit aussi le banc d'essai qui permet d'améliorer le système à partir de sa propre réalité.

## Après le choix du modèle, le choix du portefeuille

DeepSWE n'est donc pas une recette universelle. Il montre une méthode que chaque organisation peut appliquer à ses propres scénarios.

Nous comparons encore souvent les modèles comme s'il fallait élire un vainqueur unique.

Une architecture agentique pose un problème différent. Elle peut essayer, vérifier, recommencer et changer de stratégie. Sa performance dépend alors autant de l'ordre des modèles, de la complémentarité de leurs erreurs et de la qualité de l'oracle que du score individuel de chacun.

Le premier modèle doit résoudre la majorité des tâches à faible coût. Le suivant doit surtout voir ce que le premier ne voit pas. Le modèle premium ou l'humain n'intervient que sur le résidu réellement difficile.

On ne cherche plus seulement le meilleur modèle. On construit un portefeuille de capacités dont les risques sont imparfaitement corrélés.

La prochaine frontière ne sera peut-être pas gagnée par le modèle placé en tête d'un classement public. Elle pourrait l'être par le système qui saura apprendre de ses scénarios réels, mesurer ses erreurs, acheter la bonne diversité et router chaque échec vers le complément le plus utile.

{{< closing-question label="À retenir" >}}
Un modèle économique couvre 102 tâches. Un second modèle Flash récupère 10 de ses 11 angles morts. Grâce à l'oracle, leur couverture combinée atteint 99,1 %.
{{< /closing-question >}}

---

## Sources

- DeepSWE, [classement v1.1, méthodologie et coûts](https://deepswe.datacurve.ai/), 113 tâches issues de 91 dépôts open source et couvrant cinq langages, mise à jour du 22 septembre 2026.
- DeepSWE, [données détaillées des tâches et des rollouts](https://deepswe.datacurve.ai/data/v1.1), calculs de couverture, de complémentarité et de coût avec arrêt au premier succès.
- Kévin Brunet, [« Pourquoi ajouter des agents ne crée pas forcément de diversité »](/articles/plusieurs-agents-points-de-vue/), diversité mesurée par les désaccords et les erreurs utiles.
- Kévin Brunet, [« Décorréler à l'aveugle »](/articles/decorreler-a-l-aveugle/), routage des désaccords et adaptation du coût de validation à l'information obtenue.
