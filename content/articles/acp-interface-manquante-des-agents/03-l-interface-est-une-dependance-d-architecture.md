---
title: "L'interface est une dépendance d'architecture"
seo_title: "Interface d'agent IA : une dépendance d'architecture cachée"
slug: "interface-dependance-architecture-agent"
date: 2026-09-28
description: "Plans, permissions, appels d'outils et sessions forment un contrat d'interface qui peut enfermer un agent chez un fournisseur."
categories: ["Intelligence artificielle", "Architecture logicielle"]
series: ["acp-interface-manquante-des-agents"]
series_order: 3
collection: "ARCHITECTURE"
cover: "/images/articles/acp-03-interface-agents.fr.png"
draft: false
---

{{< callout variant="scene" label="Derrière la conversation" >}}
Une interface d'agent ne se contente pas d'afficher du texte.

Elle montre qu'une tâche a commencé. Elle reçoit un plan, suit des appels d'outils, affiche les fichiers modifiés, demande une permission et permet d'interrompre le travail. Elle retrouve aussi les anciennes sessions et sait comment en reprendre une.

Toutes ces interactions forment déjà un contrat entre le client et l'agent. Lorsqu'il reste privé, changer l'un oblige souvent à adapter l'autre. ACP donne un nom et une forme commune à ce contrat.
{{< /callout >}}

## Derrière une conversation se cache une machine à états

Prenons une demande simple dans un éditeur : "Ajoute l'export PDF à ce rapport."

L'agent ne répond pas immédiatement avec un paragraphe. Il inspecte le projet, annonce un plan, recherche les composants concernés, propose des modifications et lance les tests. Certaines actions sont seulement informatives. D'autres attendent une décision de l'utilisateur. La fin de la tâche peut signifier que le travail est terminé, que l'agent a été interrompu ou qu'il a atteint une erreur.

Le client doit comprendre chacun de ces états pour les présenter correctement.

{{< zoomable-figure src="/images/articles/schema-progression-permission-resultat.png" alt="Schéma du cycle d'une tâche agentique : la demande envoyée mène à la progression et au plan, puis à un appel d'outil ; une permission peut être demandée et soumise au choix de l'utilisateur ; le flux se termine par un résultat, une interruption ou une erreur." action="Agrandir" label="Voir le cycle de progression et de permission d'une tâche ACP en grand" size="compact" >}}
Le client suit les états successifs de la tâche, présente la demande de permission et transmet le choix de l'utilisateur.
{{< /zoomable-figure >}}

Sans protocole partagé, chaque agent invente ses événements et chaque interface écrit un adaptateur. Le bouton "Annuler" d'un éditeur doit savoir quel message envoyer. La carte qui montre une commande doit comprendre comment son état évolue. La vue des conversations passées doit connaitre les identifiants et les métadonnées produits par l'agent.

Ce travail est rarement visible dans une démonstration. Il devient pourtant une dépendance d'architecture dès que plusieurs agents ou plusieurs interfaces doivent coexister.

## ACP transforme ces comportements en primitives

La [vue d'ensemble du protocole ACP](https://github.com/agentclientprotocol/agent-client-protocol/blob/main/docs/protocol/v1/overview.mdx) décrit une conversation bidirectionnelle fondée sur JSON-RPC.

Le client ouvre une session puis envoie la demande avec `session/prompt`. L'agent publie des notifications `session/update` pour faire progresser l'interface au rythme de son travail. Ces mises à jour peuvent porter les fragments de messages, le raisonnement rendu visible, les appels d'outils, le plan ou les changements de mode.

Dans l'autre sens, l'agent peut appeler `session/request_permission`. Le client présente alors les options à l'utilisateur et retourne son choix. Si la personne interrompt la tâche, `session/cancel` transmet cette décision à l'agent.

Les sessions possèdent elles aussi un contrat. `session/list` permet au client de découvrir les conversations connues de l'agent. `session/resume`, stabilisé en avril 2026, permet de se reconnecter à une session sans rejouer tout son historique. Le protocole prévoit également la fermeture et la libération des ressources liées à une session.

L'effet est concret : une nouvelle interface n'a plus besoin de deviner comment l'agent représente sa progression, ses permissions et son cycle de vie. Elle implémente les primitives qu'elle souhaite prendre en charge.

## L'interface peut alors innover de son côté

Une permission ACP peut devenir une boite de dialogue dans un éditeur, une carte dans une application web ou un choix structuré dans une conversation. Le sens reste le même, tandis que la présentation s'adapte au contexte.

Le client peut aussi choisir la quantité d'information qu'il expose. Un développeur voudra voir la commande exécutée, sa sortie et le diff associé. Un responsable métier préférera peut-être voir l'étape du processus, la raison de la demande et les conséquences de son choix. Le protocole transporte l'événement. L'interface décide comment le rendre compréhensible.

Cette séparation rappelle le rôle qu'a joué le Language Server Protocol pour les éditeurs. La [documentation d'introduction d'ACP](https://agentclientprotocol.com/get-started/introduction) revendique elle-même cette filiation. Un éditeur n'a plus besoin d'intégrer séparément chaque serveur de langage. Il parle un protocole commun, puis conserve la liberté de construire sa propre expérience autour des informations reçues.

Avec ACP, le même principe commence à s'appliquer aux agents. Le client et l'agent peuvent progresser sans attendre une version coordonnée de chaque combinaison possible.

## Un contrat d'interface devient un actif d'entreprise

Revenons au harness qui prépare une réponse à un appel d'offres. Il doit signaler les documents consultés, montrer l'avancement de la réponse, demander une validation juridique et permettre à un expert de reprendre le dossier.

Si ces interactions sont codées uniquement dans l'application commerciale, le harness dépend de cette application. Si elles sont définies uniquement par l'agent d'un fournisseur, l'application dépend de cet agent.

Un contrat partagé permet de placer la logique métier au bon endroit. Le harness décide qu'une validation est nécessaire, calcule les choix autorisés et conserve la preuve. Le client affiche la demande dans le langage et le format adaptés à l'utilisateur. ACP transporte l'interaction entre les deux.

L'entreprise peut alors améliorer l'expérience sans déplacer ses règles. Elle peut proposer une interface spécialisée aux juristes, une autre aux commerciaux et une troisième dans un client conversationnel général. Toutes comprennent les mêmes événements émis par le harness.

## Standardiser le dialogue ne standardise pas l'expérience

{{< callout variant="alert" label="Ce que le standard ne garantit pas" >}}
Les capacités ACP sont négociées. Tous les agents ne prennent donc pas en charge toutes les primitives, et tous les clients ne les présentent pas avec la même richesse. Une session reprise ne garantit pas non plus que deux interfaces reconstruisent exactement le même affichage.
{{< /callout >}}

C'est une propriété utile du protocole. Le contrat définit un socle d'interopérabilité sans imposer une interface unique. Il permet aux expériences de se différencier tout en évitant de réinventer le sens de chaque échange.

{{< thesis >}}
La dépendance d'interface ne disparait pas. Elle devient explicite, observable et remplaçable.
{{< /thesis >}}

{{< closing-question label="À retenir" >}}
Lorsqu'un harness possède un contrat de dialogue commun, il peut devenir accessible par plusieurs portes d'entrée sans être réécrit pour chacune.
{{< /closing-question >}}

---

## Sources

- Agent Client Protocol, [Introduction](https://agentclientprotocol.com/get-started/introduction), problème des intégrations agent-éditeur et analogie avec le Language Server Protocol
- Agent Client Protocol, [Architecture](https://agentclientprotocol.com/get-started/architecture), communication bidirectionnelle, notifications en temps réel et demandes de permission
- Agent Client Protocol, [Protocol v1 overview](https://github.com/agentclientprotocol/agent-client-protocol/blob/main/docs/protocol/v1/overview.mdx), vue d'ensemble et primitives de session
- Agent Client Protocol, [Session list stabilized](https://agentclientprotocol.com/announcements/session-list-stabilized), stabilisation de `session/list` en mars 2026
- Agent Client Protocol, [Session resume stabilized](https://agentclientprotocol.com/announcements/session-resume-stabilized), stabilisation de `session/resume` en avril 2026
