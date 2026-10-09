# Le choix de GLM Flash dépend-il des tâches évaluées ?

Contrôle rétrospectif effectué sur les données DeepSWE v1.1 conservées dans le dépôt. Aucune nouvelle exécution de modèle et aucune modification des verdicts du grader.

## Protocole fixé pour ce calcul

- Premier étage fixé : GPT-5.6 Luna `[max]`, jusqu'à quatre tentatives publiées.
- Ensemble de comparaison figé : les 66 configurations du graphique de l'article 2 dont le coût du rejeu sur les 11 échecs de Luna est complet. Les quatre configurations exclues restent exclues. Luna `[max]` ne peut pas être son propre complément et ne récupère de toute façon aucun de ses échecs.
- Choix du complément : minimiser le coût total estimé du rejeu sur les échecs d'apprentissage, divisé par le nombre de ces échecs récupérés. Les configurations ne récupérant rien sont écartées. En cas d'égalité : davantage de récupérations, coût total inférieur, puis identifiant de configuration.
- Pour chaque tâche réservée, les 112 autres servent à définir le résidu de Luna et à choisir le complément. La tâche réservée reçoit Luna, puis le complément si aucun verdict positif n'est enregistré chez Luna.
- Arrêt au premier verdict positif, tri des tentatives par `started_at`, puis `trial_name`. Les essais absents ne sont pas inventés. Un verdict absent n'établit pas que la proposition est incorrecte.
- Convention de coût de l'article : Luna × 0,2, GLM Flash × 0,5, autres coûts bruts. Cette revalorisation partielle ne représente pas les prix actuels du marché et exclut le coût de l'oracle.
- Sensibilité supplémentaire : réserver toutes les tâches d'un même dépôt, choisir le complément sur les autres dépôts, puis évaluer les tâches réservées. Les 113 tâches appartiennent à 91 dépôts.

## Résultats

| Mesure | Choix sur toutes les tâches | Une tâche réservée | Un dépôt réservé |
|---|---:|---:|---:|
| Sélections de GLM-5.3 Flash `[max]` | 1/1 | 113/113 | 91/91 |
| Sélections sur les partitions comportant un échec réservé de Luna | 1/1 | 11/11 | 10/10 |
| Échecs de Luna récupérés lors de l'évaluation | 10/11 | 10/11 | 10/11 |
| Couverture combinée | 112/113 | 112/113 | 112/113 |
| Coût estimé du complément sur le résidu | 4,78595718 $ | 4,78595718 $ | 4,78595718 $ |
| Tentatives exécutées par le complément | 21 | 21 | 21 |

Les 102 tâches déjà acceptées chez Luna ne sollicitent jamais le complément. Les retirer laisse le résidu d'apprentissage inchangé : les 113 sélections ne constituent donc pas 113 tests distincts de récupération. Les 11 tâches résiduelles sont réparties sur 10 dépôts ; deux proviennent de `platers/obsidian-linter`.

Sur l'ensemble du résidu, GLM Flash coûte environ **0,479 $ par tâche récupérée**, contre **0,792 $** pour le deuxième, DeepSeek V4 Flash `[max]`, qui en récupère quatre. Ce classement optimise un rapport économique ; il ne garantit pas une couverture minimale ni un niveau de risque acceptable.

Quand on retire une tâche récupérée par GLM, il est choisi sur les dix autres échecs de Luna, dont il récupère neuf. Quand on retire `gql-incremental-graphql-delivery`, sur laquelle il n'a aucun succès enregistré, il est choisi sur les dix autres, qu'il récupère tous. La récupération évaluée sur les tâches réservées reste ainsi de dix sur onze.

La concurrence la plus proche apparaît quand on réserve `koota-query-predicates` : coût par récupération d'apprentissage d'environ **0,495 $** pour GLM, contre **0,672 $** pour DeepSeek. Même dans cette partition, GLM conserve un avantage d'environ 26 % sur ce rapport.

## Détail des onze évaluations réservées

Dans chaque ligne, GLM Flash a été choisi sans utiliser les résultats de la tâche réservée. Il reste également choisi lorsqu'on réserve le dépôt correspondant.

| Tâche réservée | Échecs d'apprentissage récupérés par GLM | Verdict positif sur la tâche réservée |
|---|---:|---|
| bandit-structured-nosec-directives | 9/10 | Oui |
| clack-async-autocomplete-options | 9/10 | Oui |
| gql-incremental-graphql-delivery | 10/10 | Non |
| happy-dom-deterministic-intersectionobserver | 9/10 | Oui |
| helm-array-merge-strategies | 9/10 | Oui |
| kea-atomic-signal-selectors | 9/10 | Oui |
| koota-query-predicates | 9/10 | Oui |
| obsidian-linter-auto-table-of-contents | 9/10 | Oui |
| obsidian-linter-scoped-ignore-markers | 9/10 | Oui |
| pest-character-class-coalescing | 9/10 | Oui |
| textual-kitty-key-phases | 9/10 | Oui |

## Ce que le contrôle apporte

Le choix économique de GLM Flash ne dépend pas de la présence d'une seule tâche, ni d'un seul dépôt, dans les données de choix. Avec cette règle, exclure les tâches évaluées ne réduit pas la récupération observée. Le diagnostic ne détecte donc aucune fragilité de sélection à cette échelle.

Cela ne supprime pas tout biais de sélection : Luna, la fonction objectif et les candidats ont été fixés après exploration de ces données. L'éligibilité des candidats repose aussi sur la disponibilité des coûts sur le résidu complet. Ce contrôle n'est pas un test prospectif resté intact et ne valide ni l'ordre inverse de routage ni le troisième étage GLM-5.2.

Les verdicts viennent toujours du même oracle. Les partitions partagent largement leurs données d'apprentissage et ne créent aucune nouvelle observation. Le découpage par dépôt ne fournit pas de test temporel et n'élimine pas toutes les dépendances possibles entre dépôts.

Pour situer la petitesse du résidu, l'intervalle binomial de Wilson à 95 % pour 10/11 vaut environ **62,3–98,4 %**. Il est descriptif : sans indépendance pertinente et sans tenir compte de la sélection et des dépendances entre tâches, ce n'est pas un intervalle calibré de performance future du routage.

Formulation justifiée : **« Avec la règle du coût par échec récupéré, GLM Flash reste sélectionné lorsque chaque tâche, puis chaque dépôt, est exclu du choix. La récupération sur les tâches réservées reste de 10 sur 11 ; ce contrôle rétrospectif établit la stabilité du choix sur ce jeu, pas la justesse des verdicts ni sa performance future. »**

Pour progresser ensuite : figer cette politique, l'évaluer sur de nouvelles tâches représentatives et faire contrôler indépendamment les propositions, notamment celles acceptées après escalade.

## Reproduction et vérification

Depuis la racine du dépôt, avec Python 3 et sa bibliothèque standard :

```powershell
python scripts/check-deepswe-complement-selection.py
```

Le script produit `complement-selection.json`, `leave-one-task-out.csv` et `leave-one-repository-out.csv`. Le JSON conserve la règle de choix, les empreintes des entrées, les candidats, les exclusions, les limites et chaque évaluation.

Vérification effectuée séparément : recalcul des 113 partitions par tâche et des 91 partitions par dépôt en retirant physiquement les lignes réservées avant de déterminer les échecs d'apprentissage et de classer les candidats. Les choix et les rapports économiques concordent avec le rapport. Le classement de départ et les 66 candidats concordent aussi avec le graphique de l'article 2.
