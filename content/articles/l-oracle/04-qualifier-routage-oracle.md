---
title: "Construire un routage piloté par l'oracle"
seo_title: "Agents IA : comment construire un routage piloté par l'oracle"
slug: "qualifier-routage-oracle"
date: 2026-10-27
description: "Une méthode pour composer plusieurs modèles autour d'un oracle : cas réels, critères de réussite, essais, complémentarité, qualification et déploiement progressif."
categories: ["Intelligence artificielle", "Architecture logicielle", "Ingénierie logicielle"]
tags: ["ai-evaluation-evals", "ai-reliability"]
series: ["l-oracle"]
series_order: 4
collection: "SYSTÈMES"
cover: "/images/articles/qualifier-routage-oracle.fr.png"
draft: false
---

{{< callout variant="scene" label="De l'idée au système" >}}
Vous voulez confier la majorité des demandes à un modèle économique, lui donner plusieurs chances et réserver les modèles plus coûteux aux cas qui résistent.

Pour que cette chaîne fonctionne, il faut savoir reconnaître une solution acceptable, mesurer ce que chaque modèle apporte et décider quand arrêter les essais ou passer la main.

**Voici une méthode pour construire ce routage à partir de vos propres tâches, puis établir dans quelles conditions vous pouvez lui confier la livraison.**
{{< /callout >}}

Les trois premiers épisodes ont montré l'intérêt des [tentatives vérifiées](/articles/oracle-game-changer-ia-agentique/), de la [complémentarité des modèles](/articles/meilleur-modele-meilleur-complement/) et de la [qualification de l'oracle](/articles/qui-verifie-oracle/).

Le travail consiste à construire ensemble trois éléments : un jeu de cas représentatif, un oracle capable de contrôler les propositions et une politique qui choisit les modèles, leurs essais et les escalades. Leur qualification précède le déploiement progressif.

## 1. Définir les tâches et les conditions de livraison

Commencer par une famille de tâches délimitée : corriger un défaut logiciel, rapprocher des écritures comptables ou produire un dossier conforme à un schéma. Pour chaque demande, préciser les informations disponibles, les actions autorisées et les critères qui rendent le résultat acceptable.

Identifier ce qui peut être contrôlé automatiquement et ce qui exige un jugement humain. Une compilation réussie ne couvre pas toutes les exigences d'une correction. Un total équilibré ne prouve pas que les écritures ont été affectées aux bons comptes. Les critères laissés hors de l'oracle déterminent ce que le système peut livrer seul.

« Trouver le meilleur complément » ne définit pas une expérience. Faut-il récupérer le plus de tâches, minimiser la facture, respecter un délai ou limiter les erreurs livrées ? Ces objectifs peuvent donner des ordres différents.

Une équipe peut, par exemple, chercher le coût complet le plus faible parmi les chaînes qui respectent une couverture minimale, une latence maximale et un plafond d'erreurs acceptées. Ces seuils relèvent du besoin métier. Ils doivent être fixés avant le test, avec la règle qui départage deux configurations.

Fixer aussi les limites : budget par demande, délai maximal, erreurs acceptables et cas confiés directement à une personne. Le coût inclut l'exécution de l'oracle, les revalidations et l'exploitation, pas seulement les tokens. Ces conditions deviennent les critères de choix de l'architecture.

### Pourquoi le gagnant doit être évalué ailleurs

Un benchmark est un échantillon de tâches. Il peut contenir davantage de demandes d'un certain type, moins de cas difficiles pour un modèle ou quelques tâches sur lesquelles une configuration réussit exceptionnellement bien. Les exécutions des agents ajoutent leur propre variabilité.

Prenons un exemple fictif : vingt configurations possèdent toutes une probabilité de réussite de 80 % sur la population visée. Sur un petit jeu de cas, leurs scores observés peuvent différer. Si nous choisissons celle qui obtient le meilleur score, nous choisissons aussi celle qui a bénéficié de la fluctuation la plus favorable. Son score sur ce jeu peut donc surestimer sa performance future, même sans aucune erreur dans les calculs.

Les configurations réelles ne sont pas identiques. Le score du gagnant mélange alors son avantage réel et l'effet favorable de l'échantillon. Plus nous explorons de modèles, de prompts, d'ordres et de budgets d'essais, plus nous avons d'occasions de retenir une combinaison qui convient particulièrement aux cas déjà vus. Ce biais de sélection, souvent appelé *winner's curse*, est documenté notamment par [Cawley et Talbot](https://www.jmlr.org/papers/v11/cawley10a.html).

C'est la limite des comparaisons rétrospectives des deux premiers épisodes : nous avons observé les résultats disponibles pour repérer des complémentarités et comparer des chaînes, puis calculé leurs gains sur ce même jeu. Ces gains décrivent le rejeu effectué. Ils fournissent des hypothèses d'architecture, mais ne mesurent pas encore la performance d'une politique choisie à l'avance sur de nouvelles demandes. Le troisième épisode ajoute une autre exigence : vérifier que les acceptations de l'oracle correspondent bien à du travail correct.

Pour construire le système, cette exploration est utile. Elle permet de choisir les candidats et les règles à essayer. Il faut ensuite séparer deux opérations : **utiliser certains cas pour décider de la politique, puis utiliser d'autres cas pour mesurer la politique décidée**.

Concrètement, fixer l'objectif et la règle de départage, choisir les modèles, leur ordre et le nombre d'essais sur les données de développement et de validation, puis figer la chaîne avant d'ouvrir le test réservé. Si nous changeons ensuite l'ordre parce qu'il donne un meilleur résultat sur ce test, ses résultats ont participé au choix : il faut de nouveaux cas réservés pour évaluer la nouvelle politique.

**La règle de choix doit pouvoir être exécutée sans consulter les résultats des cas réservés. Le test évalue la décision obtenue ; il ne doit pas servir à la prendre.**

## 2. Construire un jeu qui représente aussi les cas absents des logs

Les traces de production sont un excellent point de départ : demande, contexte disponible à cet instant, propositions, verdicts, corrections humaines, coûts, durées et motifs d'escalade.

Elles héritent toutefois du système qui les a produites. Si l'ancien routage ne soumettait jamais certains cas à l'agent, leurs trajectoires manquent. S'il envoyait immédiatement les demandes difficiles à l'humain, les résultats automatiques décrivent surtout les cas faciles. L'absence d'incident enregistré peut aussi refléter une absence de suivi.

Il faut donc échantillonner au point d'entrée, avant la décision de routage, et inclure les demandes refusées, abandonnées ou reprises par une personne. Une réponse finale humaine ne doit pas devenir automatiquement le label d'une proposition antérieure : il faut examiner cette proposition dans son contexte.

Les cas fréquents conservent leur poids réel. Un jeu de résistance séparé peut surreprésenter incidents et tâches critiques. Si ces populations sont mélangées, conserver leurs probabilités d'échantillonnage permet de pondérer les résultats ; le taux brut du jeu enrichi ne représente pas le trafic.

## 3. Séparer les groupes, le temps et les usages des données

Un ticket presque identique dans les données de choix et dans le test peut rendre la généralisation artificiellement facile. Définir les groupes pertinents (client, dépôt, gabarit, famille de demandes) avant le découpage, puis empêcher leur chevauchement lorsque l'objectif est de mesurer la généralisation à de nouveaux groupes. La [documentation de scikit-learn](https://scikit-learn.org/stable/modules/cross_validation.html) décrit les découpages par groupe et par temps.

Pour mesurer le comportement futur, réserver une période plus récente. Si l'objectif porte aussi sur de nouveaux clients ou dépôts, combiner les deux contraintes. Pour le trafic futur de clients connus, annoncer explicitement ce périmètre plutôt que prétendre mesurer les nouveaux clients.

Trois usages doivent rester distincts :

| Jeu | Usage autorisé |
|---|---|
| Développement | Explorer les modèles, prompts et règles d'escalade |
| Validation | Choisir l'ordre, le budget d'essais et les seuils |
| Test réservé | Évaluer une fois la politique figée |

Avec peu de données, une validation croisée interne peut remplacer le jeu de validation. Elle ne dispense pas d'une évaluation externe à la sélection.

**Un test qu'on consulte pour inverser deux modèles ou ajouter un essai devient un jeu de développement.** Après un changement décidé sur ses résultats, il faut un nouveau test intact. « Une fois » désigne ici une campagne prévue à l'avance, qui peut comprendre plusieurs exécutions par cas, sans adaptation intermédiaire de la politique.

## 4. Construire l'oracle et lui donner un étalon indépendant

Traduire les critères de livraison en contrôles exécutables : tests de comportement, contraintes d'intégrité, rapprochements avec des données de référence, règles d'éligibilité. Chaque contrôle doit produire un résultat et un diagnostic utilisables par le harness.

Prévoir au moins trois issues : proposition acceptée, proposition rejetée et vérification impossible. Une panne de l'environnement ou une donnée manquante ne doit pas devenir un verdict sur la qualité de la proposition. Le harness doit pouvoir interrompre la chaîne, rétablir l'environnement ou demander une intervention.

Protéger les contrôles de confiance : l'agent ne doit pas pouvoir modifier les critères qui autorisent sa propre livraison. Tester l'oracle sur des propositions correctes et incorrectes déjà qualifiées, y compris des défauts plausibles que les contrôles superficiels laisseraient passer.

Réserver des tâches protège contre une partie du biais de sélection. Cela ne protège pas d'un oracle qui partage le même angle mort sur les données de choix et de test.

Si toutes les configurations sont sélectionnées et évaluées par ce contrôle, celle qui maximise les acceptations peut être celle qui réalise le mieux le travail, mais aussi celle dont les propositions exploitent le mieux ses lacunes. Le test mesure alors l'accord avec le contrôle. Le [problème de l'oracle en test logiciel](https://doi.org/10.1109/TSE.2014.2372785) rend cette distinction centrale.

Prévoir un échantillon examiné selon une grille métier indépendante, par des personnes qualifiées, sans leur montrer le verdict initial ni l'identité du modèle lorsque c'est possible. Un deuxième contrôle aide à repérer les désaccords ; partager les mêmes tests ou les mêmes hypothèses ne le rend pas indépendant par défaut.

L'échantillon doit contenir une part aléatoire des acceptations et des rejets, complétée par davantage d'acceptations tardives, aux essais trois et quatre, de désaccords entre contrôles et d'escalades persistantes. Les cas ciblés servent à découvrir des défauts ; une estimation du taux global exige des pondérations adaptées et une couverture de la population.

Cette revue indépendante permet de répondre à quatre questions différentes :

- Parmi les tâches sans verdict positif au premier étage, combien le complément résout-il réellement ? C'est la récupération sur le résidu.
- Parmi les réponses livrées, combien sont incorrectes ? C'est le taux d'erreurs qui atteint l'utilisateur.
- Parmi les propositions jugées correctes par la revue indépendante, combien l'oracle a-t-il rejetées ? Ce sont ses faux négatifs.
- Parmi les propositions jugées incorrectes par cette revue, combien l'oracle a-t-il acceptées ? Ce sont ses faux positifs.

Il faut conserver ces mesures séparément : elles ne portent pas sur les mêmes ensembles de tâches ou de propositions. Un faible taux d'erreurs parmi les réponses livrées ne suffit donc pas à décrire la qualité de tous les verdicts de l'oracle.

Prenons une correction logicielle : les tests de l'oracle passent, mais une personne constate qu'une exigence de la demande n'est pas satisfaite. La proposition a été acceptée à tort. Réserver cette tâche pour le test n'aurait pas suffi à découvrir l'erreur si nous avions seulement compté les tests réussis. C'est l'examen indépendant du résultat qui révèle le défaut du contrôle.

Cette découverte peut conduire à ajouter un test à l'oracle. Il faut alors distinguer la mesure de la version initiale et celle de la version corrigée. Le cas qui a servi à corriger l'oracle devient un cas de développement ; pour évaluer la version corrigée, il faut de nouveaux cas réservés. Sinon, nous mesurons aussi sa capacité à reconnaître les défauts que nous venons de lui apprendre à détecter.

{{< pullquote >}}
Tester la chaîne sur de nouvelles tâches permet de mesurer ses résultats sur des cas qui n'ont pas servi à la choisir. Pour savoir si les réponses acceptées sont réellement correctes, il faut aussi les vérifier indépendamment de l'oracle.
{{< /pullquote >}}

## 5. Mesurer les modèles et construire la chaîne

Sur les cas de développement, exécuter les configurations candidates avec le contexte, les outils et les budgets envisagés en production. Une configuration comprend le modèle, son niveau d'effort, le prompt et le harness : changer l'un de ces éléments peut modifier le profil d'erreurs.

Conserver pour chaque tentative la proposition, le verdict, les diagnostics, le coût et la durée. Mesurer la réussite au premier essai, puis le gain apporté par les essais suivants. Si un modèle récupère peu de tâches au troisième passage, ce passage doit justifier son coût et sa latence.

Pour choisir un complément, examiner uniquement les cas que le premier étage n'a pas récupérés. Comparer la couverture supplémentaire, son coût et la qualité des propositions. Répéter sur le nouveau résidu pour décider si un troisième étage apporte assez de valeur ou si l'humain doit prendre la suite.

Comparer ensuite plusieurs ordres sur le jeu de validation, avec arrêt au premier verdict positif. Le modèle qui couvre le plus de cas seul n'est pas nécessairement le meilleur premier étage : commencer par un modèle moins cher peut réduire la facture totale, mais augmenter le nombre d'essais et le délai.

Le résultat attendu est une politique explicite : modèles et configurations, ordre de passage, budget d'essais par étage, diagnostics transmis, conditions d'arrêt et recours à l'humain. Elle doit respecter les critères fixés au départ, notamment les contraintes de fiabilité, avant d'être figée pour le test réservé.

Tester ensuite la chaîne complète sur les cas réservés, dans les conditions prévues pour la production, avec plusieurs exécutions par cas pour mesurer la variabilité. Ces répétitions ne doivent pas être comptées comme autant de tâches indépendantes.

## 6. Dimensionner le résidu, pas seulement le benchmark

Si le premier modèle couvre environ 90 % des cas, un test de 200 tâches ne laisse qu'environ vingt observations pour évaluer le complément. Son score global peut paraître stable alors que sa récupération repose sur quelques cas.

Supposons que le complément résolve neuf des dix cas reçus. **90 % décrit cet échantillon.** Pour estimer son taux de récupération sur la population visée, il faut tenir compte de l'incertitude due au petit nombre de cas.

L'**intervalle de Wilson** est une méthode statistique qui calcule une borne basse et une borne haute pour estimer une proportion, à partir du nombre de réussites et du nombre de cas observés. Ici, la proportion recherchée est le taux de récupération du complément. Au lieu de fournir seulement un chiffre, la méthode donne une plage qui exprime l'incertitude de cette estimation. Elle reste utilisable avec de petits échantillons et conserve ses bornes entre 0 et 100 %.

Avec neuf réussites sur dix, cet intervalle donne des bornes d'environ **60–98 %**, dont le détail du calcul se trouve sur le site du [NIST](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm). Avec seulement dix observations, l'estimation reste très imprécise.

Pour un même taux observé de 90 %, augmenter le nombre de cas resserre l'intervalle :

| Récupérations observées | Taux observé | Intervalle de Wilson à 95 % |
|---|---:|---:|
| 9 sur 10 | 90 % | 59,6–98,2 % |
| 90 sur 100 | 90 % | 82,6–94,5 % |
| 900 sur 1 000 | 90 % | 88,0–91,7 % |

Si l'objectif exige au moins 85 % de récupération, neuf réussites sur dix ne suffisent donc pas à l'étayer : la borne basse reste loin du seuil. Il faut davantage de cas résiduels pour décider avec cette précision.

Ces calculs supposent des cas indépendants et représentatifs, avec une politique fixée avant leur évaluation. Des tickets presque identiques ou plusieurs exécutions du même ticket ne fournissent pas autant d'observations indépendantes.

La qualification des faux positifs impose un autre dénominateur. Le `β` de l'épisode précédent est la probabilité d'accepter une proposition **sachant qu'elle est incorrecte**. Pour l'estimer, il faut des propositions dont l'incorrection a été établie indépendamment, puis observer le verdict de l'oracle.

Prenons un objectif : l'oracle doit accepter au plus **0,5 % des propositions incorrectes**, soit cinq sur mille en moyenne. Pour le qualifier, nous lui soumettons des propositions dont nous savons déjà qu'elles sont mauvaises. La règle du test est simple : **il doit toutes les rejeter**.

Combien faut-il en tester ? Cela dépend de deux choix :

- `b`, la limite que l'on veut établir : ici **0,5 %**.
- `C`, le niveau de confiance choisi pour le test : ici **95 %**.

Le nombre minimal de propositions incorrectes à examiner, sans aucune fausse acceptation, est :

```text
n_min = arrondi au supérieur de [ ln(1 − C) / ln(1 − b) ]
```

Avec `b = 0,005` et `C = 0,95`, le calcul donne **598 propositions incorrectes**, soit environ 600.

Que signifie ici « 95 % » ? **Un oracle qui dépasse réellement la limite de 0,5 % a moins de 5 % de chances de réussir ce test par hasard.** Il pourrait donc être qualifié à tort. Pour réduire cette chance à moins de 1 %, choisir 99 % de confiance exige **919 propositions incorrectes**, toujours sans aucune fausse acceptation. Une certitude de 100 % n'est pas accessible avec un test fini.

Pour un dirigeant, l'enjeu est ce faux feu vert : un test trop indulgent peut autoriser la livraison automatique par un oracle qui laisse passer trop de mauvaises réponses. Le niveau de confiance détermine combien de preuves demander avant de prendre cette décision.

Cette règle suppose des propositions indépendantes et représentatives des usages prévus.

Le plan d'échantillonnage doit prévoir les volumes à chaque étage. Si l'escalade reçoit trop peu de cas, la conclusion honnête est « précision insuffisante ».

Même après un test réussi, limiter le déploiement initial et contrôler indépendamment les réponses livrées permet de détecter une qualification trop optimiste avant d'exposer tout le trafic.

## 7. Déployer en mode ombre, puis en canari

Passer en mode ombre lorsque le test réservé satisfait les critères de coût, de latence et de fiabilité fixés au départ, avec une précision suffisante pour décider.

En mode ombre, la politique candidate traite une fraction représentative du trafic sans piloter la réponse livrée. Les actions et leurs effets restent isolés. On compare les propositions, les verdicts, le coût et la latence à ceux du système actuel, avec une revue indépendante des cas sensibles.

Si les critères prévus sont satisfaits, un canari limité peut ensuite prendre en charge une petite part des cas éligibles. Le périmètre, les plafonds d'exposition, les seuils d'arrêt et le retour au système précédent doivent être opérationnels avant son lancement.

Au moindre changement du modèle, du prompt, du harness, des outils, de l'oracle ou des tâches traitées, reprendre ce processus depuis le début.

{{< callout variant="key" label="Le dossier de qualification à conserver" >}}
Conserver dans le dossier :

- La chaîne retenue et les versions de ses composants.
- L'origine des cas et leur répartition entre développement, validation et test.
- Les critères utilisés pour choisir la chaîne et autoriser son déploiement.
- Les verdicts de l'oracle et les résultats des vérifications indépendantes.
- Les résultats mesurés, le nombre de cas concernés et l'incertitude des estimations.
- Les conditions du mode ombre, du canari et du retour au système précédent.

Ce dossier permet à une autre personne de comprendre pourquoi la chaîne a été choisie et dans quelles conditions ses résultats restent valables.
{{< /callout >}}

{{< closing-question label="À retenir" >}}
Le benchmark suggère un portefeuille. La qualification doit établir **ce qu'il livre correctement, sur quels cas, à quel coût et avec quelle incertitude**.

Le protocole commence avant le choix du gagnant et continue après son premier déploiement.
{{< /closing-question >}}

---

## Sources

- Cawley et Talbot, [*On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation*](https://www.jmlr.org/papers/v11/cawley10a.html), JMLR, 2010.
- NIST/SEMATECH, [*Confidence intervals*](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm).
- scikit-learn, [*Cross-validation: evaluating estimator performance*](https://scikit-learn.org/stable/modules/cross_validation.html).
- Barr et al., [*The Oracle Problem in Software Testing: A Survey*](https://doi.org/10.1109/TSE.2014.2372785), IEEE Transactions on Software Engineering, 2015.
