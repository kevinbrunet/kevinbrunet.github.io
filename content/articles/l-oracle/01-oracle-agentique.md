---
title: "L'oracle, le vrai game changer de l'IA agentique"
seo_title: "Oracle et IA agentique : pourquoi la vérification change le meilleur modèle"
slug: "oracle-game-changer-ia-agentique"
date: 2026-10-01
description: "Avec un oracle fiable, plusieurs essais d'un modèle économique peuvent résoudre davantage de tâches qu'un seul essai d'un modèle premium."
categories: ["Intelligence artificielle", "Architecture logicielle", "Ingénierie logicielle"]
series: ["l-oracle"]
series_order: 1
collection: "SYSTÈMES"
cover: "/images/articles/oracle-agentique.fr.png"
draft: false
---

{{< callout variant="scene" label="Le classement bascule" >}}
Un essai avec GPT-6 Astra réussit plus souvent qu'un essai avec GPT-5.6 Luna.

Pourtant, quatre essais avec Luna résolvent davantage de tâches et coûtent moins cher qu'un seul essai avec Astra.

**Ce résultat dépasse la compétition entre deux modèles. Dès qu'un système sait vérifier automatiquement une réponse, leur hiérarchie peut changer.**

Cette infrastructure sous-estimée s'appelle **l'oracle**.
{{< /callout >}}

## Le classement change quand on autorise plusieurs essais

Le benchmark [DeepSWE 1.1](https://deepswe.datacurve.ai/) évalue des agents de développement sur 113 tâches de génie logiciel, issues de 91 dépôts open source et couvrant cinq langages.

Le classement principal mesure le taux de réussite moyen d'une exécution. Sur cette mesure, Astra arrive devant Luna. Si chaque tâche n'accorde qu'une seule chance, Astra est le choix le plus performant.

Les données détaillées permettent toutefois une autre lecture. Chaque configuration ayant été exécutée quatre fois sur chaque tâche, on peut compter les tâches résolues au moins une fois parmi les quatre tentatives.

Luna atteint alors 90,3 % de couverture, soit 102 tâches résolues sur 113. Astra atteint 80,5 %, soit 91 tâches.

| Configuration | Réussite d'un essai | Tâches résolues après quatre essais | Coût d'un essai | Coût de quatre essais |
|---|---:|---:|---:|---:|
| GPT-6 Astra [xhigh] | **74,1 %** | 80,5 %, soit 91 sur 113 | 4,43 $ | 17,72 $ |
| GPT-5.6 Luna [max] | 67,2 % | **90,3 %, soit 102 sur 113** | **0,61 $** | **2,44 $** |

Le contraste devient encore plus intéressant lorsqu'on regarde les coûts.

D'après le coût moyen mesuré par DeepSWE, **quatre tentatives avec Luna coûtent environ 2,44 dollars. Un seul essai avec Astra coûte 4,43 dollars.**

{{< thesis >}}
Pour un coût inférieur, Luna peut explorer quatre solutions et résoudre une proportion plus élevée des tâches. Un modèle moins fiable au premier essai peut devenir plus intéressant dans une architecture qui exploite plusieurs tentatives.
{{< /thesis >}}

Cela ne fait pas de Luna le meilleur modèle dans l'absolu. Le résultat dépend du système construit autour de lui.

## Un échec peut déclencher l'essai suivant

Le mécanisme tient en trois étapes. L'agent produit une solution. L'oracle répond `OK` ou `KO`. Si le résultat est accepté, le système s'arrête. S'il est rejeté, les tests et les traces de l'échec alimentent la tentative suivante.

Une première exécution ratée ne termine donc plus la tâche. Elle déclenche l'essai suivant. Le taux de réussite d'une seule exécution ne constitue plus le plafond de performance du système.

Les résultats de Luna montrent l'ampleur du changement. Il réussit 67,2 % des tâches sur une exécution moyenne, puis en couvre 90,3 % sur quatre exécutions séparées. Il ne rattrape pas simplement Astra : il prend la tête du classement recalculé sur cette mesure.

Dans le développement logiciel, l'oracle repose sur des tests exécutables qui vérifient le comportement attendu. La compilation, les types et l'analyse statique apportent des contrôles supplémentaires, mais ne suffisent pas à établir que la tâche est correctement réalisée. D'autres domaines possèdent leurs propres oracles : contraintes d'intégrité pour les données, recomposition indépendante d'un calcul, simulateur pour un plan ou règles d'éligibilité pour un processus métier.

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

Les quatre exécutions utilisées dans ce calcul DeepSWE sont des *rollouts* séparés. Luna ne reçoit pas, lors du deuxième essai, les diagnostics produits par le premier.

Le passage de 67,2 % à 90,3 % mesure donc ce que plusieurs tentatives permettent déjà d'obtenir sans transmission d'information entre elles. Ce simple mécanisme suffit à renverser le classement.

La vraie question commence ensuite : jusqu'où peut-on monter lorsque chaque échec ajoute de l'information ?

Un test qui échoue peut indiquer l'assertion non respectée, la valeur observée ou le chemin d'exécution concerné. Le harness peut transmettre ces éléments au modèle, conserver les approches déjà tentées et demander une correction ciblée. La deuxième tentative part alors avec plus d'information que la première, et la troisième avec plus d'information que la deuxième.

DeepSWE ne donne pas encore ce chiffre. Son pass@4 fournit un point de comparaison pour des *retries* séparés, pas le plafond d'une boucle adaptative.

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

## La qualité de l'oracle devient décisive

Cette architecture déplace une partie du problème vers la vérification.

Il faut distinguer deux défaillances.

La première vient de l'oracle lui-même. Des tests incomplets peuvent accepter un programme incorrect, simplement parce que le comportement défaillant n'a jamais été traduit en contrôle. C'est le [*problème de l'oracle*](https://doi.org/10.1109/TSE.2014.2372785), étudié depuis longtemps en génie logiciel et développé dans ma série [« Aucun harness n'est parfait »](/series/aucun-harnais-n-est-parfait/).

La seconde apparait lorsque l'agent découvre qu'il peut satisfaire ou manipuler la mesure au lieu de résoudre la tâche. Il peut coder en dur les valeurs attendues, modifier les tests ou neutraliser le grader. C'est du *reward hacking*, un mécanisme que j'ai détaillé dans [« Le voyant est vert. La mission reste inachevée. »](/articles/goodhart-dans-la-boucle/).

Ces comportements ont été observés concrètement. [METR](https://metr.org/blog/2025-06-05-recent-reward-hacking/) a publié des cas d'agents modifiant le code d'évaluation ou récupérant directement la réponse attendue. La [fiche système de Claude 3.7 Sonnet](https://www.anthropic.com/claude-3-7-sonnet-system-card) décrit des valeurs de test codées en dur et des tests modifiés après plusieurs échecs. [OpenAI](https://openai.com/index/how-we-monitor-internal-coding-agents-misalignment/) classe également la modification des tests ou la désactivation des contrôles parmi les formes rares mais graves de *reward hacking* observées avec ses agents de programmation internes.

Le problème existe même sans modification explicite du grader. [SpecBench](https://arxiv.org/abs/2605.21384) montre que des agents peuvent saturer les tests visibles tout en échouant sur des tests cachés qui recomposent les mêmes fonctionnalités dans des usages plus réalistes.

{{< pullquote >}}
Un mauvais oracle ne sécurise pas le système. Il industrialise deux types d'erreurs : les faux positifs, lorsqu'il accepte une mauvaise réponse, et les faux négatifs, lorsqu'il rejette une bonne solution.
{{< /pullquote >}}

À cela s'ajoutent les biais d'échantillonnage, les seuils mal calibrés et la dérive des données dans le temps. J'y consacrerai probablement une série d'articles, car le sujet dépasse largement la qualité d'une suite de tests.

Avec les agents, une partie de l'informatique quitte un monde largement déterministe pour intégrer des comportements probabilistes. Maitriser leurs biais statistiques devient indispensable pour concevoir des systèmes fiables. La boussole ne peut plus être le risque zéro, mais l'équilibre explicite entre bénéfice attendu et risque accepté.

Construire un bon oracle exige de définir ce qui doit être vrai, de tester les cas limites et, lorsque l'enjeu le justifie, de combiner plusieurs vérifications indépendantes.

{{< callout variant="key" label="Terrain favorable" >}}
Le développement logiciel constitue donc un terrain favorable aux agents. Il permet d'exprimer le résultat attendu sous forme de tests automatisés, puis de compléter cette vérification avec la compilation, les types, l'analyse statique et l'intégration continue.
{{< /callout >}}

Dans beaucoup d'autres métiers, le principal obstacle ne sera peut-être pas la qualité du modèle. Ce sera l'absence d'une définition automatisable du travail bien fait.

## Après la course aux modèles, la course aux oracles

Nous avons pris l'habitude d'évaluer l'IA comme un candidat qui passe un examen : une question, une réponse, une note. Un agent peut essayer, observer un échec, modifier son approche et recommencer. Sa valeur dépend autant du système qui organise cette recherche que de sa première réponse.

Un modèle moins cher et plus variable peut alors devenir préférable, à condition que son travail soit vérifiable.

La prochaine étape de l'IA agentique ne consistera pas uniquement à produire des modèles toujours plus intelligents. Elle consistera aussi à construire des environnements capables de leur dire quand leur travail est acceptable et quand ils doivent recommencer.

Après la course aux modèles viendra probablement la course aux oracles.

Ceux qui sauront vérifier automatiquement le travail des agents pourront multiplier les expériences, utiliser des modèles moins coûteux et réserver l'intelligence premium aux véritables cas difficiles.

Une limite subsiste pourtant. Après quatre exécutions, Luna laisse encore 11 tâches sans solution. Réessayer permet donc d'aller beaucoup plus loin, mais pas de supprimer les angles morts d'un modèle.

{{< closing-question label="Dans le prochain article" >}}
La question suivante n'est plus : combien de fois faut-il réessayer ? C'est : **quel autre modèle voit ce que Luna ne voit pas ?**

Les données de DeepSWE réservent ici une seconde surprise. Le meilleur complément de Luna n'est ni le modèle le mieux classé ni le plus cher.
{{< /closing-question >}}

---

## Sources

- DeepSWE, [classement v1.1, méthodologie et coûts](https://deepswe.datacurve.ai/), 113 tâches, 91 dépôts, 5 langages, scores moyens et coûts affichés, mise à jour du 22 septembre 2026.
- DeepSWE, [données détaillées des tâches et des rollouts](https://deepswe.datacurve.ai/data/v1.1), calcul du taux de tâches réussies au moins une fois parmi quatre exécutions : Luna 102/113, Astra 91/113.
- OpenAI, [documentation et tarification de GPT-5.6 Luna](https://developers.openai.com/api/docs/models/gpt-5.6-luna), 0,20 $ par million de tokens en entrée, 0,02 $ en entrée mise en cache et 1,20 $ en sortie.
- Barr et al., [*The Oracle Problem in Software Testing: A Survey*](https://doi.org/10.1109/TSE.2014.2372785), *IEEE Transactions on Software Engineering*, 2015.
- Kévin Brunet, série [*Aucun harness n'est parfait*](/series/aucun-harnais-n-est-parfait/), limites des tests, problème de l'oracle, Goodhart et corrélation entre production et validation.
- Kévin Brunet, [*Le voyant est vert. La mission reste inachevée.*](/articles/goodhart-dans-la-boucle/), épisode consacré à Goodhart et au *reward hacking* dans les boucles agentiques.
- METR, [*Recent Frontier Models Are Reward Hacking*](https://metr.org/blog/2025-06-05-recent-reward-hacking/), 5 juin 2025, exemples de manipulation des tests, du score et de l'environnement d'évaluation.
- Anthropic, [*Claude 3.7 Sonnet System Card*](https://www.anthropic.com/claude-3-7-sonnet-system-card), section « Excessive Focus on Passing Tests », cas de valeurs codées en dur et de modification des tests.
- OpenAI, [*How we monitor internal coding agents for misalignment*](https://openai.com/index/how-we-monitor-internal-coding-agents-misalignment/), modification des tests et désactivation de contrôles classées comme *reward hacking*.
- Zhao et al., [*SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents*](https://arxiv.org/abs/2605.21384), prépublication, 2026, comparaison entre tests visibles et tests cachés.
