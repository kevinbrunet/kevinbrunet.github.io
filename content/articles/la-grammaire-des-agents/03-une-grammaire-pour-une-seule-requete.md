---
title: "Une grammaire fabriquée pour une seule requête"
slug: "une-grammaire-pour-une-seule-requete"
date: 2026-10-01
description: "Produire le contexte et la contrainte depuis le schéma réel, les droits et les capacités disponibles."
categories: ["Intelligence artificielle", "Architecture logicielle"]
series: ["la-grammaire-des-agents"]
series_order: 3
collection: "ARCHITECTURE"
cover: "/images/articles/la-grammaire-des-agents/03-une-grammaire-pour-une-seule-requete.fr.png"
draft: false
---

La grammaire SQL de l'agent garantit maintenant que sa réponse commence par `SELECT`. Pourtant, en cherchant Camille Martin, il demande une table `customer_addresses` qui n'existe pas. La base utilise deux tables séparées, `customers` et `addresses`.

La requête est syntaxiquement valide. Elle reste inexécutable, car la grammaire décrit SQL en général et non cette base précise.

Le saut architectural consiste à fabriquer la contrainte depuis le schéma réel au moment de la demande, puis à la jeter après usage.

## Du langage général au contexte réel

Une grammaire statique peut utilement limiter la sortie à `SELECT`, mais le modèle peut encore inventer une table, utiliser une colonne masquée ou joindre deux entités sans relation pertinente.

Au moment de la requête, l'application connaît pourtant beaucoup plus de choses : le catalogue de la base, les vues exposées, le rôle de l'utilisateur, le tenant courant, les limites de volume et les fonctions admises. Elle peut calculer un contrat qui ne contient que ce sous-ensemble.

Le modèle ne reçoit plus « le SQL ». Il reçoit le SQL possible ici et maintenant.

## La grammaire ne renseigne pas le modèle

Il faut ici distinguer deux flux.

La grammaire est utilisée par le moteur de décodage. Elle lui permet de supprimer les tokens incompatibles avec les tables et les colonnes autorisées. Mais elle ne fait pas nécessairement partie du prompt. Le modèle ne la lit donc pas comme une description de la base.

La [documentation de llama.cpp](https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md) le précise pour JSON Schema : le schéma fourni pour contraindre la sortie n'est pas injecté dans le prompt. Le modèle n'en connaît pas la structure, sauf si l'application la lui présente aussi dans ses instructions. Les définitions d'outils constituent un cas différent, car leurs schémas sont généralement ajoutés au contexte du modèle.

Si nous fournissons seulement la grammaire SQL dynamique, la requête obtenue restera valide, mais la prédiction peut être médiocre. Le modèle calcule les probabilités sans connaître la signification des tables disponibles. Le décodeur masque ensuite les tokens interdits et choisit parmi ceux qui restent.

Le token retenu est donc le meilleur choix autorisé, mais il pouvait avoir une probabilité très faible dans la distribution initiale. La grammaire garantit la conformité de la sortie. Elle ne donne pas au modèle la connaissance nécessaire pour faire un choix pertinent.

Pour obtenir une bonne décision, le système doit donc produire deux artefacts depuis la même source :

```text
schéma réel de la base
        ↓
contexte pour le modèle
tables, colonnes, relations, descriptions
        +
contrainte pour le décodeur
tokens et structures autorisés
```

Le prompt guide la probabilité vers la bonne requête. La grammaire empêche les requêtes impossibles de sortir.

Les deux mécanismes ne se remplacent pas. Une description sans contrainte reste un conseil que le modèle peut ignorer. Une contrainte sans description ferme des portes sans lui indiquer laquelle mène au résultat attendu.

Le même principe s'applique à une API. Un document OpenAPI décrit toutes les opérations publiques. L'agent chargé du support n'a peut-être accès qu'à la lecture d'un dossier et à l'ajout d'une note. Le générateur transforme ces deux capacités en appels structurés. Une opération d'annulation absente du contrat ne peut pas être choisie.

## Une intersection de contributeurs

La grammaire dynamique n'a pas besoin d'être produite par un composant omniscient. Elle peut résulter de plusieurs ensembles qui se réduisent mutuellement :

```text
capacités du produit
∩ données visibles
∩ droits de l'utilisateur
∩ mandat de l'agent
∩ état courant
= décisions exprimables
```

Chaque contributeur reste propriétaire de sa connaissance. Le catalogue sait quelles colonnes existent. Le moteur d'autorisation sait lesquelles sont visibles. Le workflow sait quelles transitions partent de l'état courant. La configuration de l'agent sait quelles opérations lui ont été confiées.

Le générateur assemble ces contraintes sous forme d'une grammaire. Selon le moteur utilisé, elle peut prendre la forme d'un JSON Schema, d'une liste de choix, d'une grammaire formelle ou d'une définition de tool.

## Une protection parmi d'autres

Comme nous l'avons vu dans la [série sur l'authentification et l'autorisation](/series/qui-donne-le-droit-d-agir-a-votre-agent-ia/), la protection d'un agent repose sur plusieurs mécanismes. Une grammaire ne remplace ni les droits, ni la validation métier, ni les contrôles du point d'exécution.

Elle contribue à obtenir immédiatement une réponse exploitable. Elle évite une partie des allers-retours entre le système et le modèle, puis réduit le travail de validation et de correction en fin de traitement.

## Plus la grammaire est précise, plus elle se périme vite

Ajouter les tables et les colonnes autorisées réduit les requêtes fausses. Ajouter l'état du dossier, les droits de Maya et les valeurs disponibles réduit encore l'espace de génération. Mais chaque détail rend aussi la grammaire plus vite périmée.

Si le système doit reconstruire une grammaire complète à chaque demande, le coût de préparation peut finir par annuler le gain obtenu sur les erreurs évitées. À l'inverse, une grammaire trop stable ignore une partie du contexte et laisse davantage de sorties incorrectes passer jusqu'à la validation.

Le compromis actuel consiste souvent à mettre en cache une base stable, par exemple la syntaxe SQL et le schéma général, puis à ne recalculer qu'une couche plus petite liée à la requête. [XGrammar-2](https://arxiv.org/abs/2601.04426) propose une réutilisation à l'échelle des sous-structures avec son `Cross-Grammar Cache`. Deux contrats différents peuvent ainsi partager une partie du travail de préparation.

Un [préprint de juillet 2026 sur les *decode-time grammars*](https://arxiv.org/abs/2607.18357) explore une autre dimension : des fragments instanciés pendant la génération depuis l'environnement courant. Les déclarations déjà produites peuvent enrichir cet environnement et déterminer les références autorisées ensuite. Cette direction reste encore expérimentale.

Pour le moment, il faut donc arbitrer entre deux coûts : celui des requêtes fausses que la grammaire laisse encore produire et celui du barrage qu'il faut reconstruire pour les empêcher.

## Limiter le rayon d'action avant la requête

La grammaire sécurise aussi le flux de sortie. Une grammaire SQL limitée à `SELECT` retire `DELETE`, `UPDATE` ou `DROP` de l'espace de génération. Le modèle ne reçoit pas simplement l'instruction de les éviter. Il ne peut pas formuler ces requêtes.

La contrainte peut également retirer les tables sensibles et limiter les colonnes accessibles. Le rayon d'action de l'agent est réduit avant que sa réponse atteigne la base.

Ce mécanisme ne remplace pas les droits ni la validation du serveur. Il constitue un rempart supplémentaire, particulièrement utile lorsqu'un agent IA peut agir sur un système réel. La confiance ne repose plus uniquement sur sa capacité à suivre une consigne. Une partie des actions dangereuses devient impossible à exprimer.

Il reste maintenant à vérifier si cette protection vaut son coût. Le modèle calcule toujours les logits de tout son vocabulaire, tandis que le moteur doit compiler la grammaire, suivre l'état du préfixe et filtrer les tokens à chaque étape.

La bonne question n'est donc pas seulement : « La sortie est-elle valide ? » Il faut mesurer le coût nécessaire pour obtenir une sortie exploitable, avec la compilation, le décodage, les validations, les réparations et les éventuelles relances.

C'est ce que nous examinerons dans le prochain article.

---

## Sources

- [llama.cpp, GBNF Guide, conversion à la requête de JSON Schema vers GBNF et limites de fonctionnalités](https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md)
- [vLLM, Structured Outputs, choix des backends et formes de contraintes supportées](https://docs.vllm.ai/en/latest/features/structured_outputs/)
- [Li et al., XGrammar-2: Dynamic and Efficient Structured Generation Engine for Agentic LLMs (2026), réutilisation de sous-structures entre grammaires](https://arxiv.org/abs/2601.04426)
- [Zhang et al., Decode-Time Grammars: Constrained LLM Generation over a Refinement Order of Grammar Fragments (préprint, juillet 2026)](https://arxiv.org/abs/2607.18357)
