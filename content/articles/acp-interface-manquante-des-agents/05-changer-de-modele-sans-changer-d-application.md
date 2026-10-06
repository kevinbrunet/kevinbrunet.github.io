---
title: "Changer de modèle sans changer d'application"
seo_title: "Changer de modèle IA sans remplacer l'application"
slug: "changer-modele-sans-changer-application"
date: 2026-09-28
description: "Découpler le client, le harness et le modèle facilite leur évolution indépendante sans promettre une interchangeabilité magique."
categories: ["Intelligence artificielle", "Architecture logicielle"]
tags: ["llmops-agentops", "agent-protocols"]
series: ["acp-interface-manquante-des-agents"]
series_order: 5
collection: "ARCHITECTURE"
cover: "/images/articles/acp-05-interface-agents.fr.png"
draft: false
---

{{< callout variant="scene" label="Deux scénarios fréquents" >}}
Un nouveau modèle vient de sortir. Il comprend mieux les documents longs, coute moins cher et obtient de meilleurs résultats sur les dossiers complexes.

Le mouvement inverse existe aussi. Un fournisseur met à jour le modèle utilisé en production et ses résultats se dégradent brutalement sur un usage métier précis. Le taux de réussite chute alors même que l'application, les prompts et les outils n'ont pas changé.

Dans le premier cas, l'entreprise veut adopter un modèle plus performant. Dans le second, elle doit pouvoir revenir en arrière ou basculer vers un autre modèle. Aucun de ces changements ne devrait obliger les collaborateurs à changer d'application.

Le commercial doit retrouver la même conversation dans son outil de vente. Le juriste doit conserver ses demandes de validation. L'historique, les sources et les règles du harness doivent rester disponibles. Le changement peut être important dans l'architecture tout en restant presque invisible pour l'utilisateur.
{{< /callout >}}

C'est l'une des conséquences les plus intéressantes de la séparation entre interface, harness et modèle.

## Le changement se produit derrière la conversation

Reprenons le harness qui prépare les réponses aux appels d'offres. Jusqu'ici, il utilise un modèle unique pour lire les documents, retrouver les exigences, rédiger les réponses et comparer les clauses.

L'équipe découvre qu'un nouveau modèle réussit mieux l'analyse juridique. Elle commence par lui confier uniquement cette étape. Le reste du workflow continue avec le modèle précédent.

Pour l'utilisateur, rien ne bouge. Il dépose les mêmes documents, suit le même plan et reçoit les demandes de validation dans la même interface. Le harness choisit le modèle au moment où il en a besoin, puis restitue le résultat dans la session en cours.

{{< zoomable-figure src="/images/articles/schema-routage-modeles-harness.png" alt="Schéma de routage : l'application habituelle communique par ACP avec le harness d'appel d'offres. Dans le harness, l'extraction est confiée à un modèle rapide, la rédaction à un modèle généraliste et l'analyse des clauses sensibles à un modèle spécialisé. Le harness reste relié aux outils métier." action="Agrandir" label="Voir le routage des tâches vers plusieurs modèles en grand" size="compact" >}}
Le même harness choisit un modèle différent pour l'extraction, la rédaction et l'analyse des clauses sensibles, sans changer l'application de l'utilisateur.
{{< /zoomable-figure >}}

Le modèle cesse ainsi d'être une destination choisie une fois pour toutes. Il devient une ressource que le harness peut affecter à une tâche.

## Un même dossier peut demander plusieurs expertises

Prenons un harness chargé d'analyser une demande d'investissement. Le collaborateur lui transmet le projet d'un fournisseur et choisit d'abord l'angle sous lequel il souhaite l'étudier : comptable, juridique ou synthèse.

Ces trois choix sont des routes préparées dans le harness. La route comptable extrait les montants, reconstruit les échéances, compare plusieurs scénarios et appelle les outils financiers de l'entreprise. La route juridique recherche les engagements, les responsabilités et les clauses de sortie. La route de synthèse rapproche les deux analyses pour préparer la décision.

Chaque route possède ses propres instructions, outils et contrôles. Le harness choisit également les modèles autorisés pour cette expertise. La route comptable peut ainsi privilégier des modèles fiables sur les calculs et les sorties structurées, tandis que la route juridique retient des modèles adaptés aux documents longs.

Un second choix règle la profondeur de l'analyse à l'intérieur de la route sélectionnée. Dans la route juridique, une première lecture peut utiliser un modèle rapide et économique pour repérer les clauses sensibles. Une analyse approfondie peut basculer vers un modèle plus couteux et plus capable pour produire un avis détaillé. L'utilisateur choisit un niveau de service, pas le nom du modèle.

ACP permet déjà de présenter ces deux choix. Les [Session Config Options](https://agentclientprotocol.com/announcements/session-config-options-stabilized), stabilisées en février 2026, permettent à un agent d'exposer au client des sélecteurs propres à une session. Le harness peut ainsi proposer un sélecteur d'expertise et un sélecteur de profondeur d'analyse.

Le client affiche les options proposées par le harness. Dans la même conversation, l'utilisateur peut passer de l'analyse comptable à la lecture juridique du dossier, puis demander une analyse plus ou moins approfondie.

Le point de contact demeure stable. L'interface présente les choix. Le harness traduit l'expertise demandée en route métier, puis la profondeur en niveau de traitement et en modèle adapté.

## L'entreprise peut changer à son propre rythme

Quand le modèle et l'interface sont fusionnés, leur calendrier l'est aussi. Adopter une nouvelle capacité suppose de déployer un nouveau produit, reformer les utilisateurs, revoir les accès et reconstruire les intégrations.

Une architecture séparée permet plusieurs rythmes.

L'équipe chargée de l'expérience peut améliorer l'affichage des sources ou des permissions sans toucher au modèle. L'équipe qui maintient le harness peut modifier les règles et les outils sans imposer une nouvelle application. L'équipe IA peut comparer plusieurs modèles derrière le même workflow.

Cette liberté possède aussi une valeur de négociation. Si la qualité d'un fournisseur baisse, si son prix augmente ou si une nouvelle contrainte de localisation apparait, l'entreprise dispose d'un chemin de substitution. Elle ne part pas de zéro, car les utilisateurs, les outils métier et les règles restent organisés autour du harness.

Le changement peut même être progressif. Un nouveau modèle traite d'abord une faible part des dossiers. Il est ensuite utilisé sur une catégorie précise, puis étendu lorsque les résultats deviennent suffisants. Le modèle précédent reste disponible pendant la transition.

## Les évaluations deviennent le mécanisme de portabilité

Cette architecture transforme la question "Peut-on changer de modèle ?" en une série de mesures.

Le harness rejoue un ensemble de dossiers représentatifs. Il vérifie si les exigences ont été correctement extraites, si les sources citées existent, si les outils appropriés ont été appelés et si les validations ont été demandées au bon moment. Il mesure aussi le cout, la latence et le nombre de reprises nécessaires.

Anthropic recommande dans son [guide consacré aux évaluations d'agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) d'exécuter des évaluations automatisées lors de chaque changement d'agent ou de modèle. Le guide distingue notamment les évaluations de capacité, qui cherchent ce que le système sait désormais accomplir, et les tests de régression, qui vérifient qu'il n'a pas perdu les comportements déjà acquis.

Le [guide OpenAI sur la construction d'agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/) propose une démarche proche : établir une référence avec un modèle capable, puis essayer des modèles plus petits pour optimiser le cout et la latence tant que la qualité reste acceptable.

{{< thesis >}}
Les évaluations permettent de remplacer une fidélité supposée par une compatibilité démontrée.
{{< /thesis >}}

## La portabilité est une discipline, pas un bouton

{{< callout variant="alert" label="La portabilité n'est jamais automatique" >}}
Deux modèles ne suivent pas toujours les instructions de la même manière. Ils peuvent choisir des outils différents, demander plus de contexte ou produire des formats légèrement distincts. Un fournisseur peut aussi proposer une fonction difficile à remplacer, par exemple une analyse native des PDF qui conserve les tableaux, les images et les références de page. Si cette capacité améliore nettement les avis juridiques, l'entreprise peut accepter de l'utiliser uniquement dans cette route tout en gardant le reste du harness portable.
{{< /callout >}}

La séparation ne promet pas un échange instantané. Elle donne l'endroit où organiser le changement, les tests qui permettent de le décider et la possibilité de conserver l'ancienne solution pendant la transition.

{{< pullquote >}}
Le résultat recherché n'est pas que tous les modèles se valent. C'est que leur valeur soit évaluée à l'intérieur du système de l'entreprise.
{{< /pullquote >}}

{{< closing-question label="La question stratégique" >}}
Si le modèle et l'interface peuvent changer, quel est l'actif que l'entreprise doit réellement posséder ?
{{< /closing-question >}}

---

## Sources

- Agent Client Protocol, [Session Config Options stabilized](https://agentclientprotocol.com/announcements/session-config-options-stabilized), exposition de sélecteurs de modèle, de mode et de niveau de raisonnement
- Anthropic, [*Demystifying evals for AI agents*](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) (janvier 2026), évaluations lors des changements de modèle
- OpenAI, [*A practical guide to building agents*](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/), établissement d'une référence puis substitution de modèles selon les objectifs de qualité, de coût et de latence
