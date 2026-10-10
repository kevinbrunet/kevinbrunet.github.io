---
title: "L'oracle, le vrai game changer de l'IA agentique"
seo_title: "Oracle et IA agentique : pourquoi la vérification change le meilleur modèle"
slug: "oracle-game-changer-ia-agentique"
date: 2026-10-27
description: "Des tâches bien délimitées, des résultats vérifiables et davantage de temps de traitement : sur 113 tâches, passer d'environ 1 338 $ pour 74 % de réussite à 76 $ pour 100 %."
categories: ["Intelligence artificielle", "Architecture logicielle", "Ingénierie logicielle"]
tags: ["ai-systems-harness-engineering", "ai-evaluation-evals"]
series: ["l-oracle"]
series_order: 1
collection: "SYSTÈMES"
cover: "/images/articles/oracle-agentique.fr.png"
draft: false
---

{{< callout variant="scene" label="Moins cher, avec davantage de temps de traitement" >}}
**Si les tâches sont bien délimitées et leurs résultats vérifiables, accepter davantage de temps de traitement peut fortement réduire la facture.** Sur les 113 tâches étudiées, **Claude Opus 5 [max], le Claude le mieux classé sur DeepSWE, représente environ 1 338 $ pour 74 % de réussite moyenne sur un essai**. La chaîne rejouée atteint **100 % de réussite pour 76 $**.

Ce résultat devient possible lorsqu’un système sait vérifier automatiquement une réponse, rejeter un échec et poursuivre sa recherche. Cette infrastructure sous-estimée s’appelle **l’oracle**.
{{< /callout >}}

## Se fier aux données plutôt qu'à la réputation

Avant même de multiplier les tentatives, comparer les configurations sur l'ensemble de leurs exécutions permet déjà de choisir un modèle moins coûteux, avec un taux de réussite moyen très proche sur ces tâches :

| Configuration | Taux de réussite moyen d'un essai | Coût moyen estimé d'un essai | Budget estimé pour un essai sur 113 tâches |
|---|---:|---:|---:|
| Claude Opus 5 [max] | 73,6 % | 11,84 $ | 1 338,38 $ |
| GPT-6 Astra [xhigh] | 74,1 % | 4,43 $ | 500,49 $ |

**Remplacer cette configuration Claude par Astra réduit déjà le coût moyen d'un essai de 62,6 %, pour un taux de réussite moyen comparable.**

L'oracle permet ensuite d'aller plus loin : comparer les modèles sur plusieurs tentatives, plutôt que sur leur seule première réponse.

## Le classement change quand on autorise plusieurs essais

Le benchmark [DeepSWE 1.1](https://deepswe.datacurve.ai/) évalue des agents de développement sur 113 tâches de génie logiciel, issues de 91 dépôts open source et couvrant cinq langages.

Le classement principal mesure le taux de réussite moyen d'une exécution. Sur cette mesure, Astra arrive devant Luna. Sur cet ensemble de tâches et entre ces deux configurations, Astra obtient donc le meilleur résultat moyen avec une seule chance.

Les données détaillées permettent toutefois une autre lecture. Chaque configuration possède jusqu’à quatre exécutions par tâche. On peut compter les tâches acceptées au moins une fois parmi les tentatives disponibles.

Dans cet article, « résolue » signifie acceptée par le grader du benchmark, le programme qui rend le verdict. La fiabilité de ce verdict sera examinée dans [le troisième article](/articles/qui-verifie-oracle/).

Luna atteint alors 90,3 % de couverture, soit 102 tâches résolues sur 113. Astra atteint 80,5 %, soit 91 tâches.

| Configuration | Réussite d'un essai | Couverture sur jusqu’à quatre essais | Coût moyen estimé d’un essai | Budget estimé de quatre essais |
|---|---:|---:|---:|---:|
| GPT-6 Astra [xhigh] | **74,1 %** | 80,5 %, soit 91 sur 113 | 4,43 $ | 17,72 $ |
| GPT-5.6 Luna [max] | 67,2 % | **90,3 %, soit 102 sur 113** | **0,61 $** | **2,42 $** |

Le contraste devient encore plus intéressant lorsqu'on regarde les coûts.

Les coûts sont des estimations à partir de la consommation des rollouts et des tarifs utilisés par l’interface DeepSWE au 6 octobre 2026. Le budget de quatre essais vaut quatre fois le coût moyen non arrondi.

{{< cost-comparison
  dataset="deepswe-luna-astra-budget"
  title="45 % de budget en moins"
  description="Quatre essais Luna coûtent environ 2,42 dollars par tâche, contre 4,43 dollars pour un seul essai Astra. Luna atteint 90,3 % de couverture sur quatre chances ; Astra réussit en moyenne 74,1 % des tâches sur une chance."
  x-label="Budget estimé par tâche ($)"
  primary="luna-four"
  cost-label="Budget estimé par tâche"
  coverage-label="Couverture ou réussite moyenne"
  coverage-suffix=" %"
  attempts-label="Essais autorisés"
  scenario-label="Configuration"
  count-label="budgets comparés"
  details-label="Consulter les deux budgets"
>}}
Les barres comparent uniquement les budgets. Sur 113 tâches facturées à ces coûts moyens, l’écart théorique atteint 227,13 dollars. Les 90,3 % de Luna correspondent à l’union observée de quatre exécutions ; les 74,1 % d’Astra à la réussite moyenne d’une exécution.
{{< /cost-comparison >}}

Un modèle moins fiable au premier essai peut donc devenir plus intéressant dans une architecture qui exploite plusieurs tentatives.

Cela ne fait pas de Luna le meilleur modèle dans l'absolu. Le résultat dépend du système construit autour de lui.

## Un échec peut déclencher l'essai suivant

Le mécanisme tient en trois étapes. L'agent produit une solution. L'oracle répond `OK` ou `KO`. Si le résultat est accepté, le système s'arrête. S'il est rejeté, une nouvelle tentative peut être lancée.

Dans une véritable boucle agentique, les tests et les traces de l’échec pourraient alimenter cette tentative suivante. **Ce n’est pas le cas dans les données DeepSWE utilisées ici** : les rollouts sont indépendants et ne se transmettent pas leurs diagnostics. Il faudra que j’expérimente ce partage d’information dans les conditions du benchmark pour mesurer s’il augmente la couverture, réduit le nombre d’essais ou diminue le coût total.

Une première exécution ratée ne termine donc plus la tâche. Elle déclenche l'essai suivant. Le taux de réussite d'une seule exécution ne constitue plus le plafond de performance du système.

Les résultats de Luna montrent l'ampleur du changement. Il réussit 67,2 % des tâches sur une exécution moyenne, puis en couvre 90,3 % sur quatre exécutions séparées. Sur cette couverture observée, il dépasse Astra.

Un oracle est un mécanisme capable de décider automatiquement si une proposition satisfait les conditions attendues de la solution. Il transforme donc une réponse en verdict exploitable par le système : accepter, rejeter ou demander un nouveau contrôle.

En génie logiciel, cet oracle peut combiner la compilation, le typage, les tests unitaires, les tests d’intégration et des tests d’interface ou d’API. Dans d’autres métiers, il peut vérifier qu’une comptabilité est à l’équilibre, rapprocher un total avec une source indépendante, contrôler des contraintes d’intégrité ou confirmer qu’un dossier respecte des règles d’éligibilité. L’oracle garantit alors automatiquement le respect des critères encodés ; sa fiabilité dépend de leur capacité à représenter correctement le résultat attendu.

Lorsqu'un oracle fiable existe, la génération devient une boucle de recherche :

```text
Produire une proposition
        ↓
Vérifier le résultat
        ↓
   Résultat valide ?
   ├─ oui → livrer
   └─ non → conserver les diagnostics
                    ↓
             corriger et recommencer
```

L'oracle décide si le travail est acceptable. Le harness conserve les erreurs, les sorties de tests et les traces utiles. L'essai suivant ne repart donc pas nécessairement de zéro.

## DeepSWE ne mesure encore que des tentatives séparées

Les exécutions utilisées dans ce calcul DeepSWE sont des *rollouts* séparés, jusqu’à quatre par tâche. Luna ne reçoit pas, lors du deuxième essai, les diagnostics produits par le premier.

Le passage de 67,2 % à 90,3 % mesure donc ce que plusieurs tentatives permettent déjà d'obtenir sans transmission d'information entre elles. Ce simple mécanisme suffit à renverser le classement.

La vraie question commence ensuite : jusqu'où peut-on monter lorsque chaque échec ajoute de l'information ?

Un test qui échoue peut indiquer l'assertion non respectée, la valeur observée ou le chemin d'exécution concerné. Le harness peut transmettre ces éléments au modèle, conserver les approches déjà tentées et demander une correction ciblée. La deuxième tentative part alors avec plus d'information que la première, et la troisième avec plus d'information que la deuxième.

DeepSWE ne donne pas ce chiffre. Il permet déjà de tester le cas le plus basique : que se passe-t-il lorsqu’on donne au modèle le droit à l’erreur ? Sa couverture sur jusqu’à quatre essais fournit un point de comparaison pour des *retries* séparés, pas le plafond d’une boucle adaptative.

## La variance ne suffit pas : il faut acheter la bonne diversité

Les essais supplémentaires de Luna font passer sa couverture observée de 67,2 % en moyenne sur une exécution à 90,3 % sur les quatre exécutions disponibles. Mais ils laissent encore 11 tâches sans succès enregistré.

Continuer à demander au même modèle de recommencer n’est donc pas nécessairement la meilleure dépense. L’étape suivante consiste à chercher un autre modèle dont les erreurs se recouvrent le moins possible avec les siennes : non pas le mieux classé en général, mais celui qui réussit précisément là où Luna échoue.

L’oracle rend cette complémentarité mesurable. Pour chaque modèle candidat, le système peut compter les échecs récupérés, le nombre d’essais nécessaires et leur coût. Une fois la bonne paire identifiée, il peut encore comparer les ordres de routage afin de placer le modèle le plus économique devant et de ne payer le suivant que sur le résidu.

{{< pullquote >}}
Le meilleur modèle n’est pas forcément celui qui réussit le plus souvent seul. C’est celui qui apporte au système le plus de réussites supplémentaires pour chaque dollar dépensé.
{{< /pullquote >}}

## Une autre manière d'acheter de l'intelligence

Cette lecture suggère une architecture différente du réflexe qui consiste à envoyer chaque tâche au meilleur modèle disponible.

Un système peut commencer avec un modèle économique, vérifier chaque résultat et s'arrêter au premier succès. Les tâches qui résistent sont ensuite transmises à un modèle premium ou à une personne.

```text
Tâche vérifiable
      ↓
Modèle rapide et économique
      ↓
Oracle
├─ résultat accepté → livraison
└─ résultat rejeté → diagnostics + nouvelle tentative
                         ↓
                 limite atteinte ?
                 ├─ non → nouvelle stratégie
                 └─ oui → modèle premium ou humain
```

La performance vient alors d'une combinaison : modèle économique, tentatives diverses, oracle fiable, arrêt anticipé et escalade. L'intelligence la plus coûteuse intervient seulement sur les cas qui ont résisté.

## Après la course aux modèles, la course aux oracles

Nous avons pris l'habitude d'évaluer l'IA comme un candidat qui passe un examen : une question, une réponse, une note. Un agent peut essayer, observer un échec, modifier son approche et recommencer. Sa valeur dépend autant du système qui organise cette recherche que de sa première réponse.

Un modèle moins cher et plus variable peut alors devenir préférable, à condition que son travail soit vérifiable.

La prochaine étape de l'IA agentique ne consistera pas uniquement à produire des modèles toujours plus intelligents. Elle consistera aussi à construire des environnements capables de leur dire quand leur travail est acceptable et quand ils doivent recommencer.

Après la course aux modèles viendra probablement la course aux oracles.

Ceux qui sauront vérifier automatiquement le travail des agents pourront multiplier les expériences, utiliser des modèles moins coûteux et réserver l'intelligence premium aux véritables cas difficiles.

{{< closing-question label="Dans le prochain article" >}}
La question suivante n'est plus : combien de fois faut-il réessayer ? C'est : **quel autre modèle voit ce que Luna ne voit pas ?**

Les données de DeepSWE réservent ici une seconde surprise. Le meilleur complément de Luna n'est ni le modèle le mieux classé ni le plus cher.

Nous verrons ensuite qu’une fois ce complément trouvé, **inverser l’ordre de la chaîne réduit encore sa facture de 36 %**.
{{< /closing-question >}}

---

## Sources

- DeepSWE, [classement v1.1, méthodologie et coûts](https://deepswe.datacurve.ai/), 113 tâches, 91 dépôts, 5 langages, scores et coûts affichés, consultation du 6 octobre 2026.
- DeepSWE, [données détaillées des tâches et des rollouts](https://deepswe.datacurve.ai/data/v1.1), calcul du taux de tâches réussies au moins une fois parmi jusqu’à quatre exécutions : Luna 102/113, Astra 91/113.
- OpenAI, [documentation et tarification de GPT-5.6 Luna](https://developers.openai.com/api/docs/models/gpt-5.6-luna), 0,20 $ par million de tokens en entrée, 0,02 $ en entrée mise en cache et 1,20 $ en sortie.
