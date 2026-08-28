---
title: "Le véritable actif est le harness, pas la fenêtre de chat"
seo_title: "Agent IA : le harness est l'actif stratégique de l'entreprise"
slug: "harness-actif-pas-fenetre-chat"
date: 2026-09-28
description: "L'actif durable d'une stratégie agentique est le harness d'entreprise et ses contrats ouverts, pas l'interface d'un fournisseur."
categories: ["Intelligence artificielle", "Architecture logicielle"]
series: ["acp-interface-manquante-des-agents"]
series_order: 6
collection: "ARCHITECTURE"
cover: "/images/articles/acp-06-interface-agents.fr.png"
draft: false
---

{{< callout variant="scene" label="Ce qui doit survivre" >}}
Une fenêtre de chat peut disparaitre en quelques mois. La manière dont une entreprise sait instruire un appel d'offres, analyser un investissement ou gérer un incident doit lui survivre.

Cette capacité ne réside pas dans la couleur d'un bouton. Elle ne réside pas non plus dans le nom du modèle affiché en haut de la conversation.

Elle réside dans le harness : comment une demande devient une tâche, quels outils peuvent être appelés, quelles règles s'appliquent, qui doit autoriser une action et quelles preuves doivent être conservées.

Les contrats avec l'interface, les modèles et les outils rendent ce harness portable. Ils en sont une propriété, pas la totalité.
{{< /callout >}}

## Une conversation peut cacher deux formes de dépendance

Lorsqu'une entreprise adopte un assistant, elle commence souvent par regarder le modèle. Le fournisseur peut-il traiter ses documents ? Sa qualité est-elle suffisante ? Où les données sont-elles hébergées ?

Une seconde dépendance s'installe plus discrètement. L'interface apprend à afficher les événements propres à l'agent. Elle connait ses sessions, ses permissions, ses appels d'outils et ses formats de réponse. Les workflows métier sont ensuite configurés dans ce même produit.

Le jour où l'entreprise souhaite changer, elle ne doit plus seulement retrouver un modèle performant. Elle doit reconstruire l'expérience des utilisateurs, reconnecter les systèmes, traduire les règles et déplacer l'historique du travail.

La dépendance n'était donc pas seulement dans le modèle. Elle était dans les contrats restés privés entre toutes les couches.

## Posséder le harness signifie posséder la manière de travailler

{{< thesis >}}
Un harness d'entreprise rassemble les instructions, les outils, les politiques d'autorisation, les contrôles, les jeux d'évaluation, les traces et les mécanismes d'escalade qui transforment un modèle en capacité métier.
{{< /thesis >}}

Pour un appel d'offres, il sait quelles références sont encore publiables. Pour une demande d'investissement, il distingue l'analyse comptable de l'analyse juridique. Pour un incident, il détermine quelles actions peuvent être automatisées et lesquelles exigent une validation.

Ces éléments doivent pouvoir évoluer dans les dépôts, les systèmes de configuration et les processus de gouvernance de l'entreprise. Ils doivent être versionnés, testés et attribués à des responsables identifiés.

Le modèle peut alors progresser sans emporter cette connaissance avec lui. L'interface peut s'améliorer sans redéfinir les règles. Le harness devient le lieu où l'entreprise accumule réellement son apprentissage.

## Le harness se connecte aux outils. ACP le connecte aux interfaces

Pour agir, le harness peut appeler ses outils directement ou passer par le [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro). MCP standardise l'accès aux outils et aux ressources, ainsi que l'exposition de prompts réutilisables.

Ce choix se fait outil par outil. Un appel direct à une fonction, une bibliothèque ou une API peut être plus simple et moins couteux pour une capacité locale ou très sollicitée. MCP ajoute de la découverte et de l'interopérabilité, mais aussi des descriptions dans le contexte, de la sérialisation et parfois un transport ou un processus supplémentaire. Le harness utilise cette couche lorsque sa capacité à partager et gouverner l'accès compense ce cout.

L'[Agent Client Protocol](https://agentclientprotocol.com/get-started/introduction) traite l'autre frontière. Il standardise la relation entre le client et l'agent : demandes, progression, permissions, sessions et capacités négociées.

{{< zoomable-figure src="/images/articles/schema-harness-actif-entreprise.png" alt="Schéma d'architecture ouverte : les interfaces choisies par les utilisateurs communiquent par ACP avec un harness possédé par l'entreprise. Ce harness utilise des modèles évalués et remplaçables, et accède par appels directs ou MCP aux outils et aux données gouvernés par le système d'information." action="Agrandir" label="Voir l'architecture où le harness constitue l'actif de l'entreprise en grand" size="compact" >}}
Le harness possédé par l'entreprise relie les interfaces choisies par les utilisateurs à des modèles remplaçables et aux outils gouvernés par le système d'information.
{{< /zoomable-figure >}}

MCP évite que chaque agent exige son propre connecteur vers les outils qui gagnent à être partagés. Les appels directs restent disponibles lorsque la proximité ou la performance priment. ACP évite que chaque interface exige son propre contrat avec chaque agent. Entre les deux, le harness conserve la logique métier et choisit le niveau de standardisation adapté.

Cette architecture permet aux trois couches de suivre des calendriers différents. Les équipes peuvent ajouter un client, promouvoir un modèle ou modifier une règle sans devoir remplacer tout le système au même moment.

## Être présent partout sans renoncer aux garanties

Cette architecture apporte deux bénéfices distincts.

Le premier concerne l'accès. Une même capacité peut rejoindre le collaborateur dans son outil de prédilection ou l'accompagner sur plusieurs canaux. Un harness chargé de produire un avis réglementaire peut être appelé depuis un CRM, un outil de ticketing, une base documentaire ou une messagerie. ACP fournit le contrat de conversation commun à ces clients.

Depuis l'une de ces interfaces, le collaborateur peut mobiliser plusieurs logiciels de l'entreprise sans passer manuellement de l'un à l'autre. Le harness orchestre les systèmes autorisés au moyen d'appels directs, d'API ou de MCP : retrouver une fiche client, consulter un document, ouvrir un ticket ou déclencher une validation.

Le second bénéfice concerne la confiance. Le harness s'intercale entre la demande et le modèle. Avant l'exécution, il vérifie le contexte disponible, les droits de l'utilisateur et les informations manquantes. Pendant la tâche, il limite les outils accessibles et demande les validations nécessaires. Après la génération, il contrôle le résultat, exige les sources attendues et conserve la trace des actions.

Ces garde-fous s'adaptent à l'enjeu. Une recherche d'information peut seulement exiger des références vérifiables. Une analyse sensible peut ajouter des contrôles indépendants et un seuil de qualité. Une action dans le SI peut imposer une validation humaine et la conservation d'une preuve.

L'entreprise peut alors constituer un catalogue de capacités transverses, chacune définie par les tâches qu'elle accepte, les systèmes qu'elle peut utiliser et le degré d'assurance qu'elle doit fournir. La question n'est plus seulement "Dans quelle application installer un assistant ?", mais "Quelle capacité rendre accessible, depuis quels outils et avec quelles garanties ?"

## L'ouverture devient une capacité d'entreprise

Cette architecture permet de conserver le même harness lorsque l'interface ou le modèle change, de proposer une capacité dans plusieurs outils et de faire évoluer chaque couche à son propre rythme. Elle facilite aussi un déploiement progressif : un nouveau client, un nouveau modèle ou une nouvelle capacité peuvent d'abord être testés sur un périmètre limité avant d'être généralisés.

Pour concrétiser ces avantages, plusieurs points demandent une expertise particulière. L'identité et les autorisations déterminent qui peut appeler chaque capacité et au nom de qui elle agit. L'isolation protège les données et les environnements d'exécution. Les évaluations vérifient la qualité lors d'un changement de modèle ou de règle. L'observabilité relie enfin la conversation, les appels d'outils, les validations et les écritures dans le SI.

La négociation des capacités ACP, le transport des agents distants et le versionnement des clients et des harness complètent ce socle. L'entreprise peut commencer avec un client administré, une équipe pilote et un jeu d'évaluations, puis élargir progressivement les capacités et les interfaces disponibles.

Elle obtient ainsi une ouverture maitrisée : davantage de choix pour les utilisateurs et les équipes techniques, avec des responsabilités clairement attribuées pour la sécurité, la qualité et les preuves.

## Construire ce qui doit rester

Les modèles continueront de changer. Les interfaces aussi. Certains fournisseurs disparaitront, d'autres proposeront des capacités qu'il serait absurde d'ignorer.

{{< callout variant="key" label="Choix d'architecture" >}}
La réponse n'est pas de chercher une architecture sans dépendance. Elle consiste à décider où ces dépendances sont acceptables et où l'entreprise doit conserver la maitrise.
{{< /callout >}}

{{< pullquote >}}
Le modèle fournit une intelligence. L'interface fournit un lieu de collaboration. Le harness porte la manière de travailler.
{{< /pullquote >}}

{{< closing-question label="À retenir" >}}
Le véritable actif n'est pas la fenêtre dans laquelle le collaborateur écrit sa demande. C'est le harness qui porte la capacité d'entreprise, agit avec ses règles et continue d'exister lorsque cette fenêtre change.
{{< /closing-question >}}

---

## Sources

- Model Context Protocol, [Introduction](https://modelcontextprotocol.io/docs/getting-started/intro), outils, ressources, prompts et architecture d'intégration
- Agent Client Protocol, [Introduction](https://agentclientprotocol.com/get-started/introduction), interopérabilité entre clients et agents et analogie avec le Language Server Protocol
- Agent Client Protocol, [Architecture](https://agentclientprotocol.com/get-started/architecture), communication bidirectionnelle, compatibilité avec MCP et négociation de capacités
- Agent Client Protocol, [Clients](https://agentclientprotocol.com/get-started/clients), liste officielle des clients documentaires, web, mobiles et de messagerie
