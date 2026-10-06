---
title: "MCP donne des outils à l'agent. ACP donne l'agent à l'utilisateur."
seo_title: "ACP et MCP : deux interfaces complémentaires pour les agents IA"
slug: "mcp-outils-acp-agent-utilisateur"
date: 2026-09-28
description: "MCP relie l'agent aux outils ; ACP relie l'agent à son utilisateur et permet de conserver la même interface quand l'agent change."
categories: ["Intelligence artificielle", "Architecture logicielle"]
tags: ["agent-protocols"]
series: ["acp-interface-manquante-des-agents"]
series_order: 1
collection: "ARCHITECTURE"
cover: "/images/articles/acp-01-interface-agents.fr.png"
draft: false
---

{{< callout variant="scene" label="Point de départ" >}}
Choisir un agent ne devrait pas obliger à choisir sa fenêtre.

C'est pourtant ainsi que fonctionne encore une grande partie du marché. Un agent arrive avec son interface, ses sessions, sa manière d'afficher les actions et ses boites de dialogue. Pour utiliser un autre agent, il faut souvent changer d'environnement ou construire une intégration dédiée.

ACP propose déjà une autre expérience. Dans un client compatible, l'utilisateur peut lancer différents agents, leur envoyer une demande, suivre leur progression, voir leurs appels d'outils, autoriser une action et reprendre une session. L'interface reste familière. C'est l'agent derrière elle qui change.
{{< /callout >}}

## Aujourd'hui, ACP permet de choisir son agent dans son éditeur

Le premier usage concret d'ACP se trouve dans le développement logiciel. Des éditeurs comme [Zed et JetBrains](https://agentclientprotocol.com/get-started/clients) peuvent accueillir plusieurs agents compatibles. Le développeur reste dans son éditeur, ouvre une conversation et choisit l'agent auquel il veut confier la tâche.

Il peut lui demander de comprendre un projet, chercher l'origine d'un bug ou modifier plusieurs fichiers. L'agent explore le dépôt, annonce sa progression, présente ses appels d'outils et affiche les changements dans l'interface. Lorsqu'une commande demande une autorisation, l'éditeur montre les choix à l'utilisateur et transmet sa décision à l'agent.

L'[Agent Client Protocol](https://agentclientprotocol.com/get-started/architecture) rend cette expérience commune. Le client envoie la demande avec `session/prompt`. L'agent diffuse sa progression avec `session/update` et sollicite une autorisation avec `session/request_permission`. Le client peut interrompre la tâche avec `session/cancel`, puis l'utilisateur peut retrouver ou reprendre ses sessions.

Le développeur peut ainsi essayer un autre agent sans abandonner son éditeur, ses raccourcis, ses fichiers ouverts et sa manière de suivre le travail. Inversement, l'agent compatible peut rejoindre un nouvel éditeur sans que son équipe reconstruise toute l'intégration.

{{< thesis >}}
ACP ne transporte pas uniquement une réponse. Il porte la durée de la tâche, les actions, les décisions intermédiaires et le contrôle rendu à l'utilisateur.
{{< /thesis >}}

## Le harness se connecte aux outils. ACP le connecte à l'utilisateur

Pour agir, un harness peut appeler ses outils directement ou passer par le [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro). MCP devient surtout utile lorsque ces accès doivent être standardisés et partagés entre plusieurs agents ou environnements.

ACP ouvre l'autre côté. Il permet à plusieurs interfaces de dialoguer avec l'agent selon un contrat partagé.

La différence peut se résumer ainsi :

{{< zoomable-figure src="/images/articles/schema-acp-client-agent.png" alt="Schéma vertical : l'utilisateur transmet sa demande à un client, le client communique avec l'agent par ACP, puis l'agent accède aux outils et au contexte par des appels directs ou par MCP." action="Agrandir" label="Voir le schéma des rôles respectifs d'ACP et de MCP en grand" size="compact" >}}
ACP relie le client à l'agent ; les appels directs ou MCP relient ensuite l'agent aux outils et au contexte.
{{< /zoomable-figure >}}

Le harness choisit comment donner à l'agent les moyens d'agir. MCP standardise cette connexion lorsqu'elle doit être partagée. ACP donne à l'utilisateur les moyens de piloter l'agent. Ensemble, ils rendent possible une architecture ouverte des deux côtés sans imposer le même niveau de standardisation à chaque outil.

## Le même protocole sert déjà à écrire, pas seulement à coder

Obsidian fournit un exemple intéressant de ce déplacement. Ce logiciel sert d'abord à écrire, organiser et relier des notes en Markdown. Ce n'est pas un IDE, même si certains utilisateurs s'en servent aussi pour documenter leurs projets techniques.

Le plugin communautaire [Agent Client pour Obsidian](https://community.obsidian.md/plugins/agent-client) transforme un coffre de notes en client ACP. Depuis le panneau latéral, l'utilisateur choisit entre plusieurs agents compatibles. Il peut mentionner une note avec `@`, joindre une image, lancer plusieurs sessions et retrouver ses conversations dans Obsidian.

L'agent peut lire et modifier les notes par l'intermédiaire de l'API du coffre. Les demandes d'autorisation apparaissent dans l'interface, et les conversations peuvent être enregistrées sous forme de notes Markdown. Le même protocole qui sert à montrer un diff de code porte donc déjà une expérience d'écriture et de gestion de connaissances.

Le plugin n'a pas besoin d'une intégration différente pour chaque agent. Il implémente ACP comme client. Un agent compatible peut alors rejoindre l'environnement sans que toute l'interface soit réécrite pour lui.

Obsidian reste ainsi l'espace de travail. L'utilisateur conserve ses notes, ses habitudes et son interface. Claude Code, Codex ou Gemini CLI peuvent occuper tour à tour la place de l'agent. Le moteur de la conversation change, pas l'endroit où le travail est réalisé.

Obsidian prouve ainsi qu'ACP peut déjà transporter une expérience au-delà du code.

## Demain, un harness d'entreprise derrière plusieurs conversations

Prenons un harness d'entreprise conçu pour préparer les réponses aux appels d'offres. Il retrouve les références autorisées, applique les règles juridiques, produit un brouillon, demande une validation avant d'utiliser un document sensible et conserve la trace des sources utilisées.

Ce harness pourrait demain devenir un service conversationnel de l'entreprise plutôt que de rester enfermé dans un assistant.

Le commercial l'appellerait depuis son application de vente. Le juriste retrouverait la même session dans son environnement de travail. Un expert pourrait reprendre le dossier depuis un client spécialisé. Dans chaque interface, le harness présenterait son avancement, demanderait les permissions nécessaires et conserverait la même logique métier.

Ce découplage change aussi la diffusion des outils internes. Si l'entreprise possède déjà des clients conversationnels capables de parler à ses agents, elle peut distribuer un nouveau harness par la conversation. L'interface existe. La nouvelle valeur se concentre dans la capacité métier.

On peut alors imaginer un catalogue interne de harness : préparer un appel d'offres, analyser un incident, instruire une demande d'achat, vérifier un contrat ou accompagner une mise en production. Chaque équipe garde son interface préférée, tandis que l'entreprise fait évoluer les règles et les outils derrière le protocole.

## La séparation devient un choix stratégique

{{< callout variant="alert" label="Limite actuelle" >}}
ACP relie aujourd'hui principalement des éditeurs de code à des agents. Une version 2 est déjà en préparation, mais elle reste à l'état de brouillon. Utiliser le protocole dans d'autres métiers est déjà possible, mais pas encore sans intégration spécifique : il faut compléter ACP pour prendre en charge les interactions métier, la gestion fine des permissions, la propagation de l'identité de l'utilisateur et la traçabilité. Et parce qu'une interface commune ne rend pas tous les agents équivalents, chaque combinaison de harness et de modèle devra continuer d'être évaluée sur les tâches métier visées.
{{< /callout >}}

La direction, elle, est claire. Le client porte l'expérience utilisateur. Le harness porte les règles, le contexte, les outils, les contrôles et les preuves. Le modèle apporte ses capacités de raisonnement et de génération. MCP relie le harness aux données, aux outils et aux services du SI. ACP le relie aux interfaces.

Une entreprise peut ainsi améliorer son interface sans réécrire son agent, faire évoluer son harness sans obliger les collaborateurs à changer d'application et évaluer un autre modèle sans abandonner tout ce qui donne au système sa valeur métier.

{{< closing-question label="À retenir" >}}
Le modèle n'est qu'un composant. L'actif durable de l'entreprise est le harness construit autour de lui.
{{< /closing-question >}}

---

## Sources

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Agent Client Protocol](https://agentclientprotocol.com/)
- Agent Client Protocol, [aperçu officiel du protocole v1](https://github.com/agentclientprotocol/agent-client-protocol/blob/main/docs/protocol/v1/overview.mdx)
- Agent Client Protocol, listes officielles des [clients compatibles](https://agentclientprotocol.com/get-started/clients) et des [agents compatibles](https://agentclientprotocol.com/get-started/agents)
- Agent Client Protocol, [registre officiel](https://agentclientprotocol.com/get-started/registry) stabilisé en mars 2026 pour découvrir, installer et configurer des agents
- Agent Client pour Obsidian, [fiche officielle du plugin communautaire](https://community.obsidian.md/plugins/agent-client), agents pris en charge, accès aux notes, sessions, permissions et export Markdown
- Agent Client pour Obsidian, [dépôt source et documentation](https://github.com/RAIT-09/obsidian-agent-client) des fonctionnalités ACP
