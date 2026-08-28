---
title: "Un agent ne doit pas agir comme Alice. Il doit agir pour Alice."
seo_title: "Délégation d'autorité à un agent IA : séparer les identités"
slug: "agent-agit-pour-alice"
date: 2026-09-03
description: "Une délégation sûre conserve des identités distinctes pour l'utilisateur qui mandate et l'agent qui exécute."
categories: ["Intelligence artificielle", "Sécurité", "Architecture logicielle"]
series: ["qui-donne-le-droit-d-agir-a-votre-agent-ia"]
series_order: 3
collection: "ARCHITECTURE"
cover: "/images/articles/03-agent-agit-pour-alice.fr.png"
draft: false
---
Le premier montage donnait le JWT d'Alice à AgentSynthèse. Les API ne voyaient
donc qu'Alice.

Nous devons maintenant conserver deux identités :

```text
Alice            = l'origine du mandat
AgentSynthèse    = le logiciel qui choisit et exécute les appels
```

Ce changement parait administratif. Il transforme pourtant les décisions que
le système peut prendre.

## "Comme Alice" et "pour Alice" décrivent deux architectures

Quand l'agent utilise directement le token d'Alice, il agit comme elle. On parle
d'impersonation. Du point de vue de l'API, Alice et son agent sont
interchangeables.

Dans une délégation, AgentSynthèse s'authentifie avec sa propre identité et
présente un mandat provenant d'Alice :

```text
Alice demande une tâche
        ↓
AgentSynthèse s'authentifie comme AgentSynthèse
        ↓
un token délégué indique qu'il agit pour Alice
```

La [RFC 8693 sur OAuth Token Exchange](https://www.rfc-editor.org/rfc/rfc8693)
fournit des briques utiles. Le `subject_token` représente le sujet au nom
duquel l'autorité est demandée. L'`actor_token` peut représenter l'acteur
délégué. Dans le token émis, le claim `act` peut conserver l'acteur courant :

```json
{
  "sub": "alice",
  "act": {
    "sub": "agent-synthese"
  },
  "aud": "patient-api",
  "scope": "patient.read"
}
```

L'API peut désormais poser une question qui n'existait pas auparavant :

> AgentSynthèse peut-il lire ce dossier pour Alice ?

## L'identité de l'agent devient une donnée de politique

Alice peut être autorisée à publier directement. AgentSynthèse peut être limité
à la préparation.

Un second agent peut recevoir un plafond différent. Un agent expérimental peut
être admis sur des données de test et refusé en production. Un agent spécialisé
en synthèse peut lire du texte, tandis qu'un agent de facturation n'accède
qu'aux actes codés.

La distinction améliore aussi l'exploitation :

```text
quelles actions Alice a-t-elle réalisées directement ?
quelles actions proviennent d'AgentSynthèse ?
quel agent faut-il révoquer après un incident ?
combien de dossiers une tâche automatisée a-t-elle parcourus ?
```

Rendre l'agent visible n'ajoute aucun droit. Cela donne au système une nouvelle
dimension sur laquelle appliquer ses règles.

## Le consentement doit lui aussi nommer l'agent

Les travaux récents autour de l'autorisation agentique rendent cette
distinction plus explicite.

Le brouillon IETF
[*On-Behalf-Of User Authorization for AI Agents*](https://www.ietf.org/archive/id/draft-oauth-ai-agents-on-behalf-of-user-00.html)
proposait qu'un utilisateur consente à une délégation vers un agent identifié
par `requested_agent`. L'agent possédait ses propres credentials et le token
final conservait la séparation entre utilisateur et acteur.

Ce brouillon a expiré. Ce n'est pas un standard sur lequel promettre une
interopérabilité. Il reste intéressant parce qu'il montre le déplacement du
problème : le consentement ne porte plus seulement sur une application et
quelques scopes. Il porte sur un agent nommé qui agira pour un utilisateur.

## Un nouveau token à chaque frontière

Imaginons le trajet :

```text
Alice
  ↓
AgentSynthèse
  ↓
Service de consultation
  ↓
API des dossiers patients
```

Transmettre le même token jusqu'au dernier service recrée un passe-partout. Un
token destiné au service de consultation ne devrait pas être accepté par l'API
des dossiers.

L'échange de tokens permet de changer d'audience à chaque frontière, de
raccourcir la durée de vie et de conserver la chaine de délégation. Chaque
service reçoit un credential destiné à son propre rôle dans la tâche.

Cette architecture améliore fortement l'attribution. Elle ne résout pourtant
pas la question centrale des permissions.

## Deux identités valides peuvent encore produire trop de pouvoir

Notre token délégué contient encore :

```text
scope = patient.read
```

Alice a le droit de lire le dossier. AgentSynthèse est correctement identifié.
La délégation est valide.

Mais AgentSynthèse est-il autorisé à lire tous les patients visibles par Alice,
ou seulement ceux de la consultation ? Alice a-t-elle réellement délégué la
publication, ou seulement la préparation ? La politique locale de l'API
accepte-t-elle cet agent sur ce type de dossier ?

La délégation répond à "qui agit pour qui ?". Elle ne calcule pas, à elle
seule, l'autorité effective.

La prochaine étape est l'idée qui commence à apparaitre dans plusieurs travaux
sur les agents : les droits ne doivent plus être hérités du dernier acteur. Ils
doivent être l'intersection de toutes les limites de la chaine.

## Sources

- IETF, [RFC 8693 : OAuth 2.0 Token Exchange](https://www.rfc-editor.org/rfc/rfc8693)
- IETF Internet-Draft, [On-Behalf-Of User Authorization for AI Agents](https://www.ietf.org/archive/id/draft-oauth-ai-agents-on-behalf-of-user-00.html), brouillon expiré cité comme direction de travail, pas comme standard
