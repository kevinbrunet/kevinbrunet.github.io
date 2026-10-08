---
title: "Qui vérifie l'oracle ?"
seo_title: "Oracle agentique : faux positifs, retries et fiabilité du grader"
slug: "qui-verifie-oracle"
date: 2026-10-27
description: "Multiplier les essais n'est rentable que si le verdict est fiable. Faux positifs, bugs du grader et tests manipulés changent le budget de recherche d'un agent."
categories: ["Intelligence artificielle", "Architecture logicielle", "Ingénierie logicielle"]
tags: ["ai-evaluation-evals", "ai-systems-harness-engineering"]
series: ["l-oracle"]
series_order: 3
collection: "SYSTÈMES"
cover: "/images/articles/qui-verifie-oracle.fr.png"
draft: false
---

{{< callout variant="scene" label="Le verdict devient le produit" >}}
Un agent propose une correction. Les tests passent. Le système livre.

Une deuxième proposition aurait peut-être été meilleure. Une dixième aurait peut-être contourné le contrôle. Nous ne le saurons pas : le premier verdict positif a arrêté la recherche.

**Dès que l'oracle pilote les essais, une erreur de vérification devient une décision du système.**
{{< /callout >}}

Les deux premiers articles montraient la mécanique : plusieurs tentatives peuvent dépasser un modèle premium au premier essai, puis un autre modèle peut récupérer les échecs du précédent.

Il reste une condition à examiner : que vaut le `OK` qui autorise la livraison ?

## Un succès enregistré n'est pas encore une preuve

Dans les données DeepSWE étudiées, Luna obtient au moins un verdict positif sur 102 tâches. Avec GLM-5.3 Flash, l'union atteint 112 sur 113. Ces calculs sont reproductibles à partir des résultats individuels.

Mais ils comptent les acceptations du grader. Ils ne démontrent pas, à eux seuls, que 112 demandes ont été correctement réalisées.

Un oracle peut se tromper dans les deux sens : accepter une mauvaise solution, le **faux positif**, ou rejeter une bonne solution, le **faux négatif**. Le premier peut laisser passer un défaut. Le second peut déclencher des tentatives et une escalade inutiles.

Ce problème n'est pas seulement théorique. Dans sa [revue de DeepSWE v1.1](https://epoch.ai/benchmarks/deepswe/review), publiée le 7 septembre 2026, Epoch AI documente des faux négatifs sur au moins 23 des 113 tâches. Sa recherche s'est arrêtée après avoir atteint le seuil justifiant son verdict « Flawed ». Elle ne mesure donc pas les faux positifs du benchmark.

Il ne faut pas transformer « 23 tâches concernées » en « 20,3 % des tentatives mal évaluées ». Ce sont deux dénominateurs différents.

Ces données restent utiles pour explorer la valeur des nouvelles tentatives et repérer des complémentarités possibles entre modèles. Elles fournissent des hypothèses d'architecture à tester. Pour savoir si les gains observés correspondent à du travail réellement correct, il faut corriger les défauts identifiés du grader et revalider les propositions avec une vérification indépendante.

**La leçon est de qualifier l'oracle avant de lui confier le routage et la livraison.** C'est cette qualification qui permet de transformer une couverture enregistrée en résultat exploitable.

## Modifier les tests peut aussi révéler un mauvais grader

Le grader doit appliquer la proposition de l'agent puis exécuter sa propre vérification. Cette opération peut elle-même casser l'environnement de test.

Epoch décrit notamment des collisions entre les noms de fonctions ajoutées par l'agent et ceux des tests cachés, ainsi que des fonctions auxiliaires supprimées lorsque le grader remplace un fichier. Le code testé peut alors être rejeté pour une erreur de compilation ou de collecte des tests.

Dans ce cas, ajouter ou adapter des tests était une démarche de développement légitime. L'agent n'avait pas nécessairement essayé de tromper l'évaluation.

**Toucher aux tests ne suffit donc pas à établir une triche.** Il faut regarder ce qui a changé et ce que la vérification mesure ensuite.

Ce point concerne directement notre exemple. Une des 11 tâches sans succès chez Luna, `obsidian-linter-auto-table-of-contents`, figure dans la liste d'Epoch. GLM Flash obtient un succès enregistré sur cette tâche. La revue cite toutefois d'autres configurations : elle ne démontre pas que les tentatives de Luna utilisées ici étaient des faux négatifs.

Le rapprochement justifie d'inspecter ces trajectoires. Il ne permet ni de corriger automatiquement leurs verdicts, ni d'attribuer le gain de GLM à un bug précis.

Un faux négatif peut aussi grossir le gain apparent des nouvelles tentatives : une proposition ultérieure peut éviter un défaut du grader que la précédente déclenchait. L'amélioration du score ne correspond alors pas nécessairement à une amélioration du travail réalisé.

## Le modèle qui passe le mieux peut aussi contourner le contrôle

L'autre risque va dans le sens opposé. Un agent peut affaiblir une assertion, supprimer un test, coder en dur une réponse attendue ou neutraliser un contrôle. Il obtient alors le verdict recherché sans satisfaire la demande.

[METR](https://metr.org/blog/2025-06-05-recent-reward-hacking/) a publié des exemples de ce *reward hacking* chez des agents de programmation. La possibilité existe donc. Elle ne prouve pas que Luna ou GLM Flash l'a exploitée dans les résultats comparés ici.

Lorsqu'un modèle réussit davantage, plusieurs explications restent possibles : il réalise mieux la tâche, ses propositions évitent mieux un défaut du grader, ou elles exploitent mieux une faiblesse du contrôle. La qualité du harness et la configuration contribuent également au résultat.

Sans inspection des propositions et validation indépendante, un meilleur score ne permet pas de départager ces explications.

{{< pullquote >}}
Le modèle le plus performant devant le grader n'est pas automatiquement celui qui produit le travail le plus correct.
{{< /pullquote >}}

## Plus d'essais, plus d'occasions de faux positif

Supposons maintenant une tâche pour laquelle toutes les propositions restent incorrectes. Chaque essai offre une nouvelle occasion à l'oracle d'en accepter une par erreur.

Appelons `β` la probabilité qu'il accepte une proposition **sachant qu'elle est incorrecte**. Si cette probabilité est constante et si les erreurs d'acceptation sont indépendantes entre essais, le risque d'au moins une fausse acceptation parmi `k` propositions incorrectes vaut :

```text
Risque = 1 − (1 − β)^k
```

Avec un taux hypothétique de `β = 0,5 %`, cela donne :

| Propositions incorrectes soumises | Risque d'au moins une fausse acceptation |
|---|---:|
| 1 | 0,5 % |
| 4 | 1,99 % |
| 12 | 5,84 % |

Ce tableau illustre un mécanisme. Ce n'est pas une estimation du risque réel de DeepSWE.

Pour des risques faibles, l'approximation `k × β` est utile. Elle cesse d'être précise lorsque le cumul augmente. Surtout, l'indépendance n'est pas acquise : plusieurs propositions peuvent partager le même défaut ou exploiter la même faille.

Même un oracle déterministe est concerné. Son programme ne change pas, mais les propositions qu'on lui soumet changent. Certaines erreurs passent systématiquement ses contrôles.

Même lorsque les essais sont liés, additionner leurs risques peut donner un plafond prudent. Supposons que chacune de quatre propositions incorrectes ait au maximum 0,5 % de risque d'être acceptée. Le risque qu'au moins une passe est alors au maximum de 2 %.

Pourquoi un plafond ? Parce que les erreurs peuvent se recouvrir. Si les quatre essais rencontrent exactement la même faille dans les mêmes cas, additionner leurs risques revient à compter plusieurs fois ces cas. À l'extrême, si les quatre événements de fausse acceptation sont identiques, le risque total reste de 0,5 %. Si chacun touche des cas différents, sans recouvrement, il atteint 2 %. La somme reste donc un plafond, même sans connaître les liens entre les essais. Elle ne donne pas le risque exact.

La condition essentielle se trouve dans les mots **« au maximum »**. Il faut pouvoir justifier ce plafond pour chaque essai, sur les tâches et dans les conditions où le système l'utilise. Un taux moyen de 0,5 % sur un benchmark ne garantit pas que chaque étape d'une escalade reste sous ce seuil. Les tâches qui résistent peuvent concentrer les faiblesses de l'oracle et présenter un risque supérieur.

**Additionner des plafonds justifiés permet de limiter le risque. Additionner des moyennes prises ailleurs ne suffit pas à le garantir.**

## Le taux de faux positifs exige son dénominateur

Datacurve annonçait, dans son [article de lancement de DeepSWE](https://deepswe.datacurve.ai/blog/deepswe), environ 0,3 % de faux positifs pour DeepSWE, contre 8,5 % pour SWE-bench Pro.

Les [résultats détaillés de cette évaluation](https://deepswe.datacurve.ai/artifacts/v1/critiques.json) précisent la mesure : 2 propositions acceptées mais jugées mauvaises sur 735 rollouts examinés pour DeepSWE, contre 67 sur 789 pour SWE-bench Pro. La qualification des propositions reposait sur un juge LLM.

Ces proportions portent sur **tous les rollouts examinés**, pas seulement sur les propositions incorrectes. Elles ne sont donc pas directement le `β` de notre formule. Elles proviennent en outre de l'évaluation initiale, pas d'une mesure des erreurs sur les tâches résiduelles de notre chaîne v1.1.

Si `f` désigne la proportion de faux positifs parmi toutes les tentatives, alors, sur une même population :

```text
β = f / proportion de propositions incorrectes
```

Avec `f = 0,3 %` et une part **hypothétique** de 40 % de propositions incorrectes, on obtiendrait `β ≈ 0,75 %`. Le chiffre de 40 % n'est pas établi ici : 0,75 % ne doit pas devenir une caractéristique annoncée de DeepSWE.

La proportion d'erreurs parmi les réponses livrées est encore une autre mesure. Elle dépend des bonnes solutions produites, des faux négatifs et de la règle d'arrêt. Un seul « taux de faux positifs » ne décrit pas tout le système.

## Le budget d'essais dépend de la qualité de l'oracle

Sous l'hypothèse précédente de risques constants et indépendants, une tolérance `r` donne un nombre maximal d'essais :

```text
k_max = partie entière de ln(1 − r) / ln(1 − β)
```

Pour des risques faibles, `k_max ≈ r / β` donne un ordre de grandeur. Avec une tolérance de 2 % et `β = 0,5 %`, quatre propositions incorrectes restent juste sous le seuil dans ce modèle. La cinquième le dépasse.

Cette formule ne suffit pas à fixer une politique de production. Il faut une estimation prudente de `β`, pertinente pour les cas traités, et tenir compte de son incertitude et de la dépendance entre essais.

{{< thesis >}}
La qualité de l'oracle détermine le budget de recherche que le système peut exploiter à risque accepté constant.

**Un meilleur oracle permet davantage d'essais utiles.**
{{< /thesis >}}

C'est pourquoi cette contrainte renforce la thèse des deux premiers articles. Réduire les erreurs de vérification peut rendre accessibles davantage de tentatives économiques. Le coût de construction, d'exécution et de maintenance de l'oracle fait toutefois partie du calcul.

{{< callout variant="key" label="L’économie brute n’est pas le gain net" >}}
Dans l’exemple précédent, la chaîne simulée coûte environ **2 848 dollars de moins sur 113 tâches** qu’un essai de la configuration Claude la plus coûteuse. Cette somme constitue le budget brut disponible pour financer la vérification.

Le gain net retranche encore l’exécution et la maintenance de l’oracle, les revalidations humaines et le coût attendu des erreurs acceptées. Si ces charges dépassent cette économie brute sur un volume comparable, l’architecture améliore peut-être la couverture, mais **elle ne fait pas économiser d’argent**.
{{< /callout >}}

## L'escalade concentre les cas difficiles

Une chaîne de trois modèles, chacun autorisé à tenter quatre fois, peut soumettre jusqu'à douze propositions pour une tâche qui traverse tous les étages.

En reprenant l'exemple précédent, si chacune des douze propositions incorrectes présente un risque de fausse acceptation plafonné à 0,5 %, le risque total est **au maximum de 6 %**, même sans indépendance : `12 × 0,5 %`. Avec des risques constants et indépendants de 0,5 %, le calcul exact donne **5,84 %**. Ces chiffres illustrent les hypothèses de l'exemple, pas le risque mesuré de notre chaîne DeepSWE.

Toutes les tâches ne reçoivent pas douze essais : un verdict positif arrête la chaîne. Mais les cas rejetés à répétition accumulent les occasions de fausse acceptation. Ce sont aussi ceux pour lesquels la vérification peut être la plus difficile.

On ne peut donc pas appliquer sans contrôle un taux moyen du benchmark aux tâches qui restent après huit échecs. Le taux pertinent peut dépendre de la tâche, du modèle, du harness, du type de proposition et des diagnostics déjà transmis.

Diversifier les modèles peut augmenter la couverture. Cela ne garantit pas que les erreurs de l'oracle deviennent indépendantes : tous les modèles peuvent rencontrer le même contrôle incomplet.

{{< pullquote >}}
Sur une tâche critique, l'escalade automatique peut devenir contre-productive : elle multiplie les occasions d'accepter une erreur. L'humain doit être saisi dès le départ.
{{< /pullquote >}}

## Ce qu'il faut connaître avant de lui confier la livraison

Un oracle exploitable a besoin d'une fiche de caractéristiques, comme tout composant critique :

- **Ce qu'il vérifie** : comportements couverts, exigences laissées hors contrôle, cas limites et dépendances à l'environnement.
- **Ses erreurs mesurées** : faux positifs et faux négatifs, avec leurs dénominateurs, la méthode de qualification et l'incertitude.
- **Les conditions de validité** : tâches, modèles, harness et versions sur lesquels ces mesures ont été obtenues, notamment les cas d'escalade.
- **Ce que l'agent peut modifier** : code, tests, configuration et outils. Les contrôles de confiance doivent être protégés.
- **La dépendance entre essais** : défauts communs, réutilisation des diagnostics et changements de stratégie.
- **Son coût complet** : calcul, latence, revalidation indépendante, maintenance et traitement des incidents.

Des vérifications humaines ciblées doivent examiner les acceptations suspectes et les échecs persistants. Une panne d'infrastructure doit être distinguée d'une solution réellement incorrecte.

## La course aux oracles commence par leur qualification

Les chiffres de couverture restent utiles pour explorer une architecture. Ils deviennent insuffisants lorsqu'on veut décider de ce qu'elle peut livrer.

Le système doit savoir combien coûte une proposition, quelles tâches elle récupère et quelle confiance mérite son verdict. Ces trois informations déterminent ensemble l'ordre des modèles et le nombre d'essais.

La prochaine frontière ne consiste donc pas seulement à demander à un agent de recommencer. Elle consiste à construire une vérification assez solide pour que recommencer reste une bonne décision.

{{< closing-question label="À retenir" >}}
Multiplier les essais peut rendre l'intelligence moins chère. **La fiabilité de l'oracle détermine combien d'essais nous pouvons nous permettre.**
{{< /closing-question >}}

---

## Sources

- Datacurve, [DeepSWE v1.1 : données détaillées des tâches et des rollouts](https://deepswe.datacurve.ai/data/v1.1), consultation du 6 octobre 2026.
- Epoch AI, [*DeepSWE v1.1 — Benchmark review*](https://epoch.ai/benchmarks/deepswe/review), 7 septembre 2026.
- Huang et al., [*DeepSWE: Measuring frontier coding agents on original, long-horizon engineering tasks*](https://deepswe.datacurve.ai/blog/deepswe), Datacurve, 26 mai 2026.
- Datacurve, [*DeepSWE v1 — critiques.json*](https://deepswe.datacurve.ai/artifacts/v1/critiques.json), résultats et définitions des proportions de faux positifs et de faux négatifs.
- METR, [*Recent Frontier Models Are Reward Hacking*](https://metr.org/blog/2025-06-05-recent-reward-hacking/), 5 juin 2025.
- Barr et al., [*The Oracle Problem in Software Testing: A Survey*](https://doi.org/10.1109/TSE.2014.2372785), *IEEE Transactions on Software Engineering*, 2015.
