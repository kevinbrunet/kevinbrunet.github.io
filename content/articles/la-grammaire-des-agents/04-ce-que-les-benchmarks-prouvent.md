---
title: "Ce que les grammaires font vraiment gagner"
slug: "ce-que-les-benchmarks-prouvent"
date: 2026-11-05
description: "Mesurer le coût total d'une sortie exploitable et distinguer conformité du schéma et justesse métier."
categories: ["Intelligence artificielle", "Architecture logicielle"]
series: ["la-grammaire-des-agents"]
series_order: 4
collection: "ARCHITECTURE"
cover: "/images/articles/la-grammaire-des-agents/04-ce-que-les-benchmarks-prouvent.fr.png"
draft: false
---

Pour une seule recherche de Camille Martin, construire un générateur de contraintes serait excessif. L'équation change lorsque l'agent assiste toute l'équipe de Maya et répète le même workflow chaque jour.

Une grammaire dynamique demande un contrat, des tests, une stratégie de version et une validation à l'exécution. Son intérêt dépend donc du coût qu'elle ajoute et des échecs qu'elle évite.

## Le mauvais calcul : les tokens par seconde

La première tentation consiste à mesurer uniquement la vitesse du décodage. Puisque des tokens sont interdits, le modèle aurait moins de choix et devrait répondre plus vite.

Le moteur ne fonctionne pas ainsi. Le Transformer calcule encore les logits de son vocabulaire. La grammaire intervient ensuite pour déterminer les continuations compatibles avec le préfixe et masquer les autres. Elle ne rend donc pas le calcul principal du modèle plus petit. Elle ajoute même du travail entre deux tokens.

La documentation de [llama.cpp](https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md) avertit d'ailleurs que certaines constructions ont un coût élevé. Il faut donc benchmarker la combinaison exacte du modèle, du tokenizer, du moteur et du schéma.

Ce surcoût n'est pas nécessairement important. Le moteur [XGrammar](https://arxiv.org/abs/2411.15100) préanalyse une partie du vocabulaire, conserve des structures de parsing persistantes et peut faire travailler le contrôle grammatical en parallèle de l'inférence sur GPU. Ses auteurs annoncent jusqu'à cent fois moins de coût que certains moteurs de contraintes antérieurs et un surcoût de bout en bout proche de zéro dans leurs configurations. La contrainte peut donc devenir presque gratuite, sans pour autant accélérer le modèle par rapport à une génération libre.

Le retour sur investissement se mesure plus loin dans la chaîne.

[XGrammar-2](https://arxiv.org/abs/2601.04426) prolonge ce travail pour les agents dont les contrats varient entre les requêtes et pendant une génération. Ses auteurs rapportent une compilation plus de six fois plus rapide que les moteurs comparés et un surcoût de bout en bout proche de zéro dans leurs configurations. La réutilisation de sous-structures entre grammaires permet de préparer un nouveau contrat sans recommencer tout le travail.

Un autre cas mérite un moteur spécialisé : choisir parmi des milliers de valeurs autorisées. Le préprint [*Trie Automata for Constrained Decoding over Large Finite Sets*](https://arxiv.org/abs/2608.12574), publié le 12 août 2026, exploite les préfixes communs de ces chaînes pour préparer les masques de tokens. Il rapporte des gains de compilation et de débit face à XGrammar dans ses configurations. Ces résultats concernent les ensembles finis et leur intégration au serveur ; ils ne prouvent pas qu'une grammaire SQL générale accélère la génération libre.

## Les reprises qui disparaissent

Sans contrainte, chaque réponse ouvre une série de cas : texte avant le JSON, propriété manquante, nom approximatif, valeur hors liste, SQL mélangé à une explication ou appel d'outil impossible à parser. Le code client ajoute des extracteurs, des réparateurs, des relances et des fallbacks.

Ces couches consomment des tokens, du temps de calcul et surtout du temps d'ingénierie. Elles compliquent aussi l'observabilité, car un résultat réparé n'est plus exactement celui que le modèle avait proposé.

Une sortie garantie supprime les réparations de forme. Un contrat généré depuis le système réduit aussi les erreurs de vocabulaire. Le gain cumulé vient de ces chemins d'échec qui disparaissent.

## Mesurer séparément la forme et la justesse

Un [préprint du 20 septembre 2026](https://arxiv.org/abs/2609.23742) évalue cinq petits modèles, de 0,6 à 4 milliards de paramètres, sur quatorze tâches structurées. Dans ce protocole, Outlines et XGrammar permettent d'atteindre 100 % de conformité au schéma, contre 78,6 à 92,9 % sans ces contraintes. Des erreurs de contenu persistent cependant, notamment dans les tâches demandant plusieurs appels de fonctions.

L'agent peut donc produire un JSON parfaitement conforme tout en recherchant Camille dans le mauvais arrondissement. Il n'y a plus d'erreur de parsing, mais le besoin de Maya reste insatisfait.

Il faut mesurer les deux résultats : la proportion de sorties conformes et la proportion de décisions correctes. Le coût d'une sortie exploitable inclut les validations et les reprises encore nécessaires pour obtenir le bon résultat métier. Le benchmark renforce cette distinction ; ses taux ne constituent pas une garantie pour tous les modèles et tous les workflows.

## Pourquoi ce n'est pas déjà utilisé partout

Les sorties JSON contraintes et les appels d'outils sont courants. Les grammaires personnalisées et dynamiques le sont moins, car elles déplacent le travail du prompt vers l'infrastructure.

Il faut construire le contrat depuis une source fiable, le convertir dans le dialecte du moteur et tester les fonctionnalités supportées. Tous les backends n'implémentent pas le même sous-ensemble de JSON Schema.

La taille compte aussi. Une grammaire JSON avec quelques propriétés est facile à compiler. Une grammaire contenant toute l'API d'un framework, des milliers de symboles ou de nombreux paramètres optionnels peut être coûteuse à construire et à parcourir. Il faut souvent la découper par tâche ou combiner une partie stable mise en cache avec une petite partie dynamique.

Enfin, une grammaire garantit une forme, pas une bonne décision. Beaucoup d'équipes restent donc au prompt et à la validation après coup, plus simples à prototyper. Le coût des relances apparaît surtout lorsque l'usage augmente.

## Les cas où il ne faut pas le faire

La génération contrainte n'est pas adaptée à toute production. Un article, une synthèse ou une exploration créative ont besoin d'un grand espace de formulation. Une grammaire métier trop étroite peut empêcher le modèle d'exprimer une action nouvelle que le système devrait apprendre à prendre en charge.

Une contrainte peut également donner une fausse impression de sécurité. Un JSON valide peut contenir un montant absurde. Une commande autorisée lors de la génération peut ne plus l'être au moment de l'exécution. Un backend peut ne supporter qu'une partie du schéma. La validation du domaine, l'autorisation et les tests restent indispensables.

## Ce que nous avons réellement déplacé

Sans grammaire, le modèle génère d'abord sa réponse. Le logiciel vérifie ensuite sa forme et relance le modèle lorsqu'elle est inutilisable.

Avec une grammaire, le logiciel décrit la forme acceptable avant la génération. Le décodeur empêche alors le modèle de produire un champ inconnu, un type incorrect ou un token situé hors du langage autorisé.

Ce déplacement ne donne pas au modèle une meilleure compréhension du métier. Il ne décide pas si Maya possède le droit de fermer un dossier ni si l'action reste valide au moment de l'exécution. Ces contrôles restent dans l'application.

Le bénéfice établi est plus précis : lorsque la sortie attendue possède une structure ou un vocabulaire fermé, la grammaire évite certaines réponses impossibles avant qu'elles soient formulées. Elle réduit ainsi les réparations et les relances liées à la forme.

Elle peut aussi réduire le rayon d'action. Une grammaire SQL limitée à `SELECT` empêche `DELETE`, `UPDATE` ou `DROP`. Pour un tool `grep`, le contrat peut limiter les chemins à un répertoire et refuser `..` ou les chemins absolus.

Cette restriction reste active face à une injection de prompt demandant de supprimer une table ou de sortir de la sandbox. L'injection peut détourner le choix parmi les actions autorisées, mais pas réintroduire les tokens interdits. La grammaire limite ainsi le champ d'action de l'attaque.

C'est toute la force de la grammaire : la sortie dangereuse n'est pas rejetée après coup, elle n'existe jamais. Le modèle ne peut tout simplement pas la produire.

Jusqu'ici, la grammaire garantit surtout une syntaxe et un vocabulaire fermé. Pour produire du code, cela ne suffit pas. Une méthode peut être correctement écrite sans exister, un appel peut viser la mauvaise version d'un framework et deux types valides peuvent rester incompatibles.

Peut-on renforcer la grammaire avec les informations du compilateur pour aider le modèle à produire du code qui utilise réellement les bonnes API ?

C'est la piste explorée dans l'article suivant.

---

## Sources

- [llama.cpp, GBNF Guide, fonctionnement, limites de conversion JSON Schema et pièges de performance](https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md)
- [Dong et al., XGrammar: Flexible and Efficient Structured Generation Engine for Large Language Models (2024), optimisations et benchmarks du moteur](https://arxiv.org/abs/2411.15100)
- [Li et al., XGrammar-2: Dynamic and Efficient Structured Generation Engine for Agentic LLMs (2026), compilation et génération de structures dynamiques](https://arxiv.org/abs/2601.04426)
- [Xu et Bouyarmane, Trie Automata for Constrained Decoding over Large Finite Sets (préprint, août 2026), optimisations pour les grandes listes de chaînes autorisées](https://arxiv.org/abs/2608.12574)
- [Chavan, Constrained Decoding Eliminates Structural Failures in Small LLMs but Reveals a Scale-Dependent Semantic Gap (préprint, septembre 2026), conformité et exactitude évaluées séparément](https://arxiv.org/abs/2609.23742)
