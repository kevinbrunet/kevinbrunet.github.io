---
title: "À la fin, l'agent ne possède plus un rôle. Il construit une preuve d'autorité."
seo_title: "Architecture de sécurité des agents IA : prouver l'autorité"
slug: "architecture-preuve-autorite"
date: 2026-09-03
description: "Identité, intersection des politiques, capacités et preuves signées composent une autorité progressive, vérifiable et révocable."
categories: ["Intelligence artificielle", "Sécurité", "Architecture logicielle"]
tags: ["ai-security", "software-architecture"]
series: ["qui-donne-le-droit-d-agir-a-votre-agent-ia"]
series_order: 10
collection: "ARCHITECTURE"
cover: "/images/articles/10-architecture-preuve-autorite.fr.png"
draft: false
---
Nous sommes partis du montage le plus simple :

```text
Alice donne son JWT à AgentSynthèse
```

Nous arrivons à une architecture très différente :

```text
l'agent possède sa propre identité
la tâche reçoit un mandat étroit
chaque délégation réduit l'autorité
les API ajoutent des faits signés à leurs réponses
l'étape suivante exige la preuve de la précédente
une action sensible exige une approbation exacte
certaines API refusent toujours les agents
```

Cette progression ne raconte pas l'évolution d'un token. Elle raconte le
passage d'un contrôle d'accès statique à un protocole d'autorité.

## Avant : posséder le bon rôle

Le modèle classique demande :

```text
Alice a-t-elle le rôle qui permet patient.read ?
```

L'agent hérite ensuite du token ou d'un compte de service. Ses droits sont
connus avant la tâche et restent globalement stables pendant son exécution.

Ce modèle convient à des parcours écrits à l'avance. Il devient fragile lorsque
le logiciel choisit lui-même ses outils, crée des sous-tâches et découvre les
ressources dont il a besoin en avançant.

## Après : présenter les preuves qui rendent cet appel légitime

Lorsque l'API reçoit une requête, elle peut vérifier :

```text
Alice est-elle autorisée sur cette ressource ?
AgentSynthèse est-il admis pour cette opération ?
Alice a-t-elle réellement délégué cette tâche ?
la ressource provient-elle d'une étape légitime ?
les restrictions des sous-tâches sont-elles toutes respectées ?
la bonne version a-t-elle été revue ?
l'approbation humaine porte-t-elle sur cet effet exact ?
la politique locale accepte-t-elle encore l'ensemble ?
```

L'autorité n'est plus contenue dans une seule case `scope`. Elle résulte de
l'intersection de plusieurs politiques et de plusieurs preuves.

## Deux mécanismes se rejoignent

Un premier courant prolonge OAuth et JWT. Le serveur d'autorisation connait
l'utilisateur, l'agent, le consentement et la politique. Il calcule une portée
réduite et réémet un token.

Des brouillons IETF consacrés aux agents explorent aujourd'hui la délégation
multi-sauts, les capacités structurées et la réduction monotone. Le projet
[*Cross-Domain AuthZ Information Sharing for Agents*](https://datatracker.ietf.org/doc/draft-diaconu-agents-authz-info-sharing/)
écrit explicitement une formule d'intersection entre la portée délégable du
parent, la portée intrinsèque du destinataire, la délégation explicite et la
politique du domaine receveur.

Un second courant est celui des capacités atténuables. Avec Biscuit, le
détenteur peut ajouter des restrictions hors ligne, mais ne peut pas retirer
celles qui existent. Des services reconnus peuvent également signer des blocs
tiers dont les faits seront acceptés par certaines policies.

Les deux peuvent être combinés :

```text
OAuth / JWT
    identité de l'utilisateur
    identité de l'agent
    consentement et frontière organisationnelle
                  ↓
émission d'une capacité Biscuit initiale
                  ↓
Biscuit
    restrictions de la tâche
    atténuation vers les sous-agents
    preuves signées par les API
    préconditions du workflow
                  ↓
authorizer local
    faits frais
    policy de la ressource
    allow ou deny final
```

JWT explique qui agit pour qui. Biscuit peut transporter ce que cette tâche a
encore le droit de faire et ce qu'elle a légitimement accompli.

## Le token devient un historique utile, pas un journal complet

Il serait tentant d'ajouter chaque observation au Biscuit. Ce serait une erreur.

Le token doit porter les faits nécessaires aux décisions suivantes, pas toute
la conversation. Une liste de milliers de patients, des contenus cliniques ou
des traces détaillées n'ont rien à faire dans un Bearer token qui circulera
entre services.

On peut transporter :

```text
un identifiant de résultat
un hash de version
une attestation courte
une échéance
une référence de délégation
```

Et conserver les données volumineuses ou sensibles derrière les API.

## Les cinq points où l'architecture peut encore échouer

Le premier est le contournement. Si une API secondaire accepte toujours le JWT
général d'Alice, toutes les policies sophistiquées du chemin principal deviennent
facultatives.

Le deuxième est la fraicheur. Une preuve signée peut rester cryptographiquement
valide après une révocation métier. Les faits volatils exigent des tokens
courts, une introspection, une liste de révocation ou un contrôle en ligne.

Le troisième est la confiance entre clés. Une policy qui fait confiance à trop
de services recrée une autorité globale. Chaque type de fait doit avoir un
émetteur légitime et une audience claire.

Le quatrième est la complexité. Les règles ont besoin de tests, de versions,
d'outils d'explication et d'une gouvernance. Déplacer une règle du code vers un
langage de policy ne la rend pas automatiquement correcte.

Le cinquième est la donnée produite. Une autorisation parfaite sur chaque
lecture ne garantit pas qu'une synthèse ne révèle pas une information sensible
par combinaison. L'autorisation borne les opérations. Elle ne valide pas toutes
les inférences du modèle.

## Ce que cette architecture change malgré tout

Elle déplace la sécurité hors du raisonnement probabiliste de l'agent.

Le modèle peut choisir un mauvais outil. L'API refuse s'il manque la preuve.

Le modèle peut tenter de sauter la revue. La publication exige le bloc signé du
service de revue.

Le modèle peut inventer un identifiant patient. Le service n'accepte que les
patients attestés dans cette tâche.

Le modèle peut demander une action interdite. La réponse l'oriente vers un
humain, ou la policy ferme définitivement cette voie aux acteurs agentiques.

Nous ne demandons plus à l'IA d'être la gardienne de sa propre liberté.

## La vraie unité d'autorisation devient la tâche

Le point de départ de cette série était un utilisateur avec un rôle.

Le point d'arrivée est une tâche qui accumule des preuves :

```text
mandat d'Alice
∩ identité d'AgentSynthèse
∩ restrictions de délégation
∩ patients effectivement listés
∩ versions effectivement lues
∩ étapes effectivement réalisées
∩ approbation éventuellement obtenue
∩ politique actuelle de l'API
```

Une telle architecture ne supprime pas l'identité, OAuth ou les rôles. Elle les
replace dans un calcul plus riche.

Le changement profond tient en une phrase :

> Un agent ne devrait pas arriver devant une API avec la permission générale
> de son utilisateur. Il devrait arriver avec la preuve que cet appel est la
> suite autorisée de cette tâche.

## Sources

- IETF, [RFC 8693 : OAuth 2.0 Token Exchange](https://www.rfc-editor.org/rfc/rfc8693)
- IETF Internet-Draft, [Cross-Domain AuthZ Information Sharing for Agents](https://datatracker.ietf.org/doc/draft-diaconu-agents-authz-info-sharing/), document de travail et non standard établi
- Eclipse Foundation, [Eclipse Biscuit project](https://projects.eclipse.org/projects/technology.biscuit)
- Eclipse Biscuit, [Specifications](https://doc.biscuitsec.org/reference/specifications)
- Eclipse Biscuit, [Authorization Policies](https://doc.biscuitsec.org/getting-started/authorization-policies)
