---
title: "Un harness d'entreprise, plusieurs portes d'entrée"
seo_title: "Un agent d'entreprise accessible depuis plusieurs interfaces"
slug: "harness-entreprise-plusieurs-interfaces"
date: 2026-09-28
description: "ACP permet d'envisager un même harness métier accessible depuis plusieurs clients sans reconstruire chaque expérience."
categories: ["Intelligence artificielle", "Architecture logicielle"]
tags: ["agent-protocols", "ai-systems-harness-engineering"]
series: ["acp-interface-manquante-des-agents"]
series_order: 4
collection: "ARCHITECTURE"
cover: "/images/articles/acp-04-interface-agents.fr.png"
draft: false
---

{{< callout variant="scene" label="Principe de départ" >}}
Un harness d'entreprise ne devrait pas devenir une nouvelle application que chacun doit apprendre à utiliser.

Il devrait rejoindre les collaborateurs là où leur travail existe déjà.

Le même agent peut être utile dans une application commerciale, une base de connaissances, une messagerie ou un client spécialisé. Sa présentation change selon le contexte. Ses règles, ses outils et ses contrôles restent les mêmes.

ACP rend cette idée beaucoup plus concrète : le harness peut devenir une capacité accessible par plusieurs conversations plutôt qu'un produit enfermé dans une seule fenêtre.
{{< /callout >}}

## Un même besoin depuis deux logiciels différents

Prenons une demande d'avis réglementaire sur la situation d'un client.

Dans Jira, un collaborateur ouvre une conversation avec le harness depuis le ticket qui décrit la situation. Le client ACP ajoute automatiquement le contenu du ticket au prompt. Le harness dispose ainsi du contexte nécessaire pour analyser la demande et retrouver les textes applicables.

Dans le CRM, une autre collaboratrice demande le même type d'avis depuis la fiche du client concerné. Cette fois, l'intégration ajoute les informations de la fiche au prompt envoyé au harness.

Un troisième utilisateur interroge enfin le même harness depuis une messagerie. Comme cette interface ne possède pas le contexte client, le harness identifie le dossier concerné puis va chercher les informations nécessaires dans le CRM au moyen de MCP.

Le besoin et la méthode restent identiques : comprendre la situation, retrouver les règles applicables, produire un avis et citer ses sources. Ce qui change, c'est la manière dont le contexte parvient au harness. Il est fourni par Jira dans le premier cas, par le CRM dans le deuxième et recherché par le harness dans le troisième.

ACP fournit le contrat de conversation commun aux trois interfaces. L'ajout automatique du ticket ou de la fiche client relève de l'intégration réalisée dans chaque logiciel. MCP permet au harness d'aller chercher lui-même les données lorsqu'elles ne sont pas déjà fournies avec la demande.

## L'écosystème ACP montre déjà la diversité des portes

Cette pluralité ne relève plus seulement d'un diagramme prospectif. La [liste officielle des clients ACP](https://agentclientprotocol.com/get-started/clients) rassemble des éditeurs et IDE, mais aussi Obsidian, des applications web et desktop, des clients mobiles, des notebooks et des passerelles de messagerie.

OpenACP relie par exemple des agents compatibles à Telegram, Discord et Slack. D'autres projets proposent des clients mobiles ou font entrer ACP dans Jupyter et Obsidian. Tous ne présentent pas la même expérience et ne couvrent pas les mêmes primitives, mais ils montrent qu'un agent peut déjà être rejoint depuis des environnements très différents.

Le [registre ACP](https://agentclientprotocol.com/get-started/registry), stabilisé en mars 2026, complète cette dynamique. Il donne aux clients une manière commune de découvrir, installer et configurer des agents compatibles. Une interface peut ainsi ouvrir l'accès à un catalogue d'agents sans développer une intégration particulière pour chacun.

Pour l'entreprise, cette logique ouvre deux possibilités. Un même harness interne peut être distribué dans plusieurs clients compatibles. L'entreprise peut aussi proposer un catalogue de harness approuvés, par exemple pour produire un avis réglementaire, préparer un appel d'offres ou analyser un incident, auquel les collaborateurs accèdent depuis leur interface habituelle. ACP fournit le contrat commun avec les clients ; la sélection, les droits d'accès et la gouvernance de ce catalogue restent à construire par l'entreprise.

## Le client adapte l'expérience, le harness conserve la décision

Une demande de validation juridique peut prendre plusieurs formes. Dans l'application commerciale, elle devient une carte qui résume la clause et propose trois choix. Dans la base documentaire, elle apparait à côté du passage concerné. Dans une messagerie, elle devient une réponse structurée accompagnée d'un lien vers le dossier complet.

La décision métier ne doit pourtant pas être recalculée dans chaque interface.

Le harness détermine pourquoi une validation est nécessaire, qui peut la donner et quelles options sont autorisées. Il lie la réponse au dossier concerné et conserve la preuve du choix. ACP transporte la demande, les options et le résultat. Le client choisit la meilleure manière de les présenter.

{{< zoomable-figure src="/images/articles/schema-clients-acp-harness-entreprise.png" alt="Schéma montrant quatre interfaces — application commerciale, espace documentaire, messagerie et client spécialisé — réunies par ACP vers un même harness d'entreprise, lequel échange avec les outils, les API et les données par MCP ou par des appels directs." action="Agrandir" label="Voir le schéma du harness d'entreprise accessible depuis plusieurs clients en grand" size="compact" >}}
Plusieurs interfaces peuvent accéder au même harness par ACP, tandis que celui-ci conserve ses connexions aux outils et aux données.
{{< /zoomable-figure >}}

Cette répartition évite de disperser la politique. Ajouter une nouvelle porte d'entrée ne signifie pas copier les règles d'autorisation, la logique du workflow et les connecteurs métier dans une nouvelle application.

## La conversation devient un mode de distribution

Une entreprise distribue habituellement une capacité logicielle sous la forme d'une application. Il faut concevoir ses écrans, organiser sa navigation, gérer son déploiement et apprendre aux utilisateurs où trouver chaque fonction.

Une interface conversationnelle déjà présente change ce coût d'accès. Le collaborateur décrit son objectif dans le client qu'il utilise. Le harness transforme cette demande en workflow, sollicite les informations manquantes, rend ses actions visibles et demande les validations nécessaires.

L'entreprise peut alors constituer un catalogue de capacités conversationnelles : préparer un appel d'offres, analyser un incident, vérifier un contrat, instruire une demande d'achat ou accompagner une mise en production.

{{< thesis >}}
Chaque nouveau harness n'exige plus nécessairement une nouvelle interface complète. Il doit surtout posséder un contrat clair avec les clients, des outils fiables, une politique d'autorisation et une manière de prouver ce qu'il a fait.
{{< /thesis >}}

## On peut commencer avant que tout soit stabilisé

{{< callout variant="alert" label="Commencer avec un périmètre maitrisé" >}}
ACP est aujourd'hui surtout stabilisé autour des agents de code, et le transport distant reste en cours de standardisation. Cela n'empêche pas une entreprise de commencer. Cela lui demande de choisir un premier périmètre et de compléter le protocole avec les briques de sécurité qu'elle possède déjà.
{{< /callout >}}

Elle peut d'abord déployer un harness auprès d'une équipe pilote, depuis un client administré et sur des dossiers non critiques. ACP porte la conversation, les sessions et les permissions. Une passerelle conserve l'authentification, applique les politiques et n'expose que les agents autorisés.

L'identité peut être reliée à l'annuaire par OIDC ou OAuth, puis transmise au harness avec un jeton délégué et limité à la tâche. Un environnement éphémère par session peut isoler l'exécution. Un registre interne peut fixer les versions des agents, leurs configurations et les clients admis.

Pour l'observabilité, un identifiant de corrélation peut relier la session ACP, les appels de modèles, les outils MCP et les écritures dans le SI.

Pour les agents distants, une passerelle peut encapsuler les échanges dans un transport sécurisé déjà approuvé. Cette couche évoluera lorsque les transports HTTP et WebSocket d'ACP seront stabilisés, sans modifier le harness ni les interfaces.

{{< pullquote >}}
La stratégie consiste à confier à ACP le contrat client-agent, puis à laisser l'identité, l'isolation, les politiques et les preuves aux systèmes conçus pour cela.
{{< /pullquote >}}

L'entreprise peut ainsi apprendre sur un cas réel et élargir progressivement les usages. Avant de financer une interface agentique pour chaque métier, elle peut déjà construire un premier harness accessible depuis celles qui existent.

{{< closing-question label="La question suivante" >}}
Comment changer de modèle sans imposer aux utilisateurs de changer d'interface ni perdre leur manière de travailler ?
{{< /closing-question >}}

---

## Sources

- Agent Client Protocol, [Clients](https://agentclientprotocol.com/get-started/clients), liste officielle incluant éditeurs, Obsidian, clients desktop, web, mobiles, notebooks et passerelles de messagerie
- Agent Client Protocol, [Registry](https://agentclientprotocol.com/get-started/registry), découverte, installation et configuration d'agents compatibles
- Agent Client Protocol, [Introduction](https://agentclientprotocol.com/get-started/introduction), scénarios locaux et distants et état du support distant
- Agent Client Protocol, [Transports working group](https://agentclientprotocol.com/announcements/transports-working-group), création du groupe de travail HTTP et WebSocket en avril 2026
