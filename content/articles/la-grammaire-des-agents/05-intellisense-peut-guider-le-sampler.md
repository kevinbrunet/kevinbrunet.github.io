---
title: "IntelliSense peut-il guider le modèle ?"
slug: "intellisense-peut-guider-le-sampler"
date: 2026-10-01
description: "Combiner contraintes syntaxiques, informations du compilateur et choix du sampler pour mieux générer du code."
categories: ["Intelligence artificielle", "Architecture logicielle"]
series: ["la-grammaire-des-agents"]
series_order: 5
collection: "ARCHITECTURE"
cover: "/images/articles/la-grammaire-des-agents/05-intellisense-peut-guider-le-sampler.fr.png"
draft: false
---

Une grammaire C# peut empêcher une parenthèse mal placée ou un mot-clé impossible. Elle ne sait pas que `customer.GetBalance()` n'existe pas, que `Close()` est inaccessible ou que le projet utilise une autre version du framework.

Pour aider le modèle à produire du code, il faut donc dépasser la syntaxe générale du langage. Il faut tenir compte des types, des méthodes réellement disponibles et de la position exacte dans le fichier.

Un outil fait déjà une partie de ce travail pour les développeurs : IntelliSense.

## IntelliSense connaît le programme

Lorsque le développeur écrit `customer.`, IntelliSense ne propose pas tous les mots du C#. Il cherche les membres accessibles sur le type de `customer`, dans ce projet et à cette position.

[Roslyn](https://github.com/dotnet/roslyn/blob/main/docs/wiki/Roslyn-Overview.md) représente la solution, ses projets, leurs références et les documents ouverts. Son [`SemanticModel`](https://learn.microsoft.com/en-us/dotnet/api/microsoft.codeanalysis.semanticmodel?view=roslyn-dotnet-4.14.0) relie le texte aux symboles et aux types issus de la compilation.

Il peut donc savoir que `customer` est un `SupportCustomer`, que `AddNote()` est public, que `Deactivate()` est interne et que `GetOutstandingAmountAsync()` renvoie un `Task<decimal>`.

Cette connaissance serait précieuse pour un modèle. Elle vient du code réellement compilé, pas d'une liste de méthodes recopiée dans un prompt et potentiellement périmée.

## Une liste de complétion n'est pas une grammaire

La tentation serait d'utiliser directement les propositions d'IntelliSense comme liste des tokens autorisés. Cela ne fonctionne pas.

IntelliSense propose ce qui semble utile à une position. Il ne décrit pas toutes les suites de caractères pouvant conduire à un programme valide. Après `customer.`, le développeur peut appeler un membre, mais ailleurs il peut introduire une variable, commencer une lambda, écrire une constante ou créer un nouvel identifiant.

Le découpage diffère également. Roslyn raisonne sur des caractères et des unités syntaxiques C#. Le modèle génère les tokens de son propre vocabulaire. `GetOutstandingAmountAsync` peut être découpé en plusieurs fragments. Après le premier fragment, le code est incomplet sans être condamné.

Enfin, IntelliSense travaille sur un document momentanément invalide et recalcule ses propositions lorsque le développeur avance. Transformer chaque token généré en modification du document, nouvelle compilation et nouvelle liste de complétion produirait une boucle coûteuse.

IntelliSense ne peut donc pas être branché tel quel comme une grammaire.

## Aider plutôt qu'interdire

Cette limite ne rend pas ses informations inutiles. Elle change la manière de les employer.

Une grammaire applique une contrainte dure. Si un token ne peut conduire à aucune sortie valide, sa probabilité effective devient nulle. Le modèle doit choisir parmi les continuations restantes.

IntelliSense pourrait fournir un signal plus souple. Une méthode accessible et adaptée au type attendu reçoit un bonus. Une API obsolète reçoit une pénalité. Un membre provenant de la bonne version du framework est favorisé. Les autres possibilités restent disponibles lorsque le modèle doit introduire du code nouveau.

Nous ne demandons plus à IntelliSense de définir tout le langage possible. Nous lui demandons d'aider le modèle à choisir parmi plusieurs continuations syntaxiquement valides.

## Le sampler devient le point d'extension

Le modèle produit un score pour chaque prochain token. Un sampler transforme ensuite cette distribution avant d'en sélectionner un.

[`llama-server`](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md) permet déjà d'ordonner plusieurs samplers comme Top-K, Top-P, Min-P ou la température. [vLLM](https://docs.vllm.ai/en/stable/design/logits_processors/) expose de son côté des `LogitsProcessor` personnalisés capables de modifier le tenseur de logits avant le softmax.

On peut les voir comme une chaîne de middlewares :

```text
modèle
  ↓
logits
  ↓
grammaire C# : interdit l'impossible
  ↓
signal IntelliSense : favorise le pertinent
  ↓
politique de répétition
  ↓
température
  ↓
token choisi
```

La grammaire et IntelliSense ne jouent alors plus le même rôle. La première ferme des chemins. Le second aide à classer ceux qui restent ouverts.

Un [préprint de septembre 2026, CLAMP](https://arxiv.org/abs/2609.08602), expérimente cette combinaison dans la planification d'actions à partir d'une scène visuelle. Les objets observés et un modèle symbolique des actions fournissent les contraintes. Un masque retire les candidats invalides, puis un mécanisme tenant compte de l'état et de l'objectif ajuste les probabilités des candidats restants. Cela fournit un exemple de combinaison entre contrainte dure et classement contextuel. Ce résultat ne démontre pas encore le gain d'une intégration IntelliSense pour le code.

Cette architecture mérite une série à part entière : il faudra examiner l'ordre des processors, leur état, le tokenizer, le coût de Roslyn et la manière de convertir une complétion en biais de logits.

## IntelliSense peut aussi proposer la suite

Une autre intégration se rapproche encore davantage de l'autocomplétion humaine. Après `customer.`, IntelliSense pourrait proposer plusieurs tokens correspondant à `GetOutstandingAmountAsync()` au lieu de modifier leurs probabilités un par un.

Le modèle principal reçoit cette suite comme un brouillon. Il vérifie plusieurs tokens en un seul passage, accepte le préfixe compatible avec sa propre distribution et reprend la génération au premier désaccord. C'est le principe du décodage spéculatif.

[vLLM](https://docs.vllm.ai/en/v0.22.0/features/speculative_decoding/) expose actuellement un `custom proposer` expérimental. Une classe personnalisée implémente une méthode `propose` et fournit les tokens candidats. IntelliSense pourrait donc devenir le moteur de proposition pour les fragments de code qu'il sait compléter.

[llama.cpp](https://github.com/ggml-org/llama.cpp/blob/master/docs/speculative.md) prend également en charge le décodage spéculatif. Les brouillons peuvent venir d'un petit modèle, d'un cache de n-grams ou de motifs retrouvés dans le texte déjà produit. Il ne documente pas la même interface générique de proposer personnalisé, mais le point d'intégration est de même nature.

Cette voie ne remplace pas le sampler. Le logits processor aide le modèle à préférer une continuation. Le proposer tente de deviner plusieurs tokens à l'avance pour accélérer leur validation. IntelliSense pourrait servir aux deux, avec deux effets différents : orienter le choix ou anticiper la suite.

## Le compilateur peut aussi intervenir pendant la génération

L'accès au sampler n'est pas la seule piste pour exploiter la connaissance du compilateur. Le préprint [*Generative Compilation*](https://arxiv.org/abs/2607.13921), publié en juillet 2026, propose de vérifier du code Rust avant que le programme soit terminé.

Son mécanisme transforme un programme partiel en une forme que le compilateur peut diagnostiquer. Il cherche à détecter les erreurs déjà inévitables sans rejeter un préfixe qui pourrait encore être complété correctement. Les auteurs évaluent cette approche avec des modèles à poids ouverts et des modèles frontières accessibles en boîte noire.

Cette voie permet au compilateur de participer au processus de génération même lorsque l'application ne peut pas modifier les logits. Elle fournit des diagnostics intermédiaires ; elle ne donne pas accès au sampler et ne remplace pas le proposer IntelliSense envisagé ici.

## Le contrôle du sampler reste une limite

Cette chaîne suppose que nous contrôlions l'inférence. Avec llama.cpp ou vLLM, nous pouvons choisir la grammaire, ajouter un logits processor et décider de leur ordre.

Mais beaucoup d'équipes utilisent un modèle frontière derrière une API. Elles ne voient ni les logits ni le sampler. Elles ne peuvent pas y brancher IntelliSense ou leur propre politique de génération.

Avant d'explorer les samplers en détail, il faut donc répondre à une question plus immédiate : jusqu'où les modèles frontières permettent-ils réellement de contraindre leur sortie ?

C'est le sujet du dernier article.

---

## Sources

- [.NET Roslyn, Roslyn Overview, Workspace, syntaxe, compilation et modèle sémantique](https://github.com/dotnet/roslyn/blob/main/docs/wiki/Roslyn-Overview.md)
- [Microsoft Learn, API `SemanticModel`, accès aux symboles et aux informations sémantiques](https://learn.microsoft.com/en-us/dotnet/api/microsoft.codeanalysis.semanticmodel?view=roslyn-dotnet-4.14.0)
- [llama.cpp, documentation de `llama-server`, ordre configurable des samplers](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)
- [vLLM, conception des logits processors personnalisés et état par batch](https://docs.vllm.ai/en/stable/design/logits_processors/)
- [vLLM, décodage spéculatif et `custom proposer` expérimental](https://docs.vllm.ai/en/v0.22.0/features/speculative_decoding/)
- [llama.cpp, décodage spéculatif par modèle de brouillon et stratégies n-gram](https://github.com/ggml-org/llama.cpp/blob/master/docs/speculative.md)
- [Ma et Kordjamshidi, CLAMP: Constrained Decoding for Vision-Language Embodied Planning (préprint, septembre 2026), masques et classement selon le contexte d'action](https://arxiv.org/abs/2609.08602)
- [Mündler-Sasahara et al., Generative Compilation: On-the-Fly Compiler Feedback as AI Generates Code (préprint, juillet 2026), diagnostics sur des programmes Rust partiels](https://arxiv.org/abs/2607.13921)
