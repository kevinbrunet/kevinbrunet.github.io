---
title: "Les droits d'un agent sont une intersection, pas un rôle"
seo_title: "Permissions d'un agent IA : appliquer le moindre privilège"
slug: "droits-agent-intersection"
date: 2026-09-03
description: "Les permissions effectives d'un agent résultent de l'intersection entre utilisateur, agent, délégation, tâche et ressource."
categories: ["Intelligence artificielle", "Sécurité", "Architecture logicielle"]
tags: ["ai-security"]
series: ["qui-donne-le-droit-d-agir-a-votre-agent-ia"]
series_order: 4
collection: "ARCHITECTURE"
cover: "/images/articles/04-droits-agent-policy-intersection.fr.png"
draft: false
---
Nous savons maintenant qu'AgentSynthèse agit pour Alice. Les deux identités sont
visibles.

Il reste à calculer ce que cette chaîne a réellement le droit de faire.

Le réflexe RBAC consiste à chercher un rôle :

```text
Alice             → soignant
AgentSynthèse     → agent clinique
```

Puis à additionner ou à transmettre les permissions. Pour un agent délégué,
c'est précisément ce qu'il ne faut pas faire.

## Aucun acteur ne doit prêter ce qu'un autre n'a pas

Prenons quatre cas.

Alice peut consulter le patient P-184, mais AgentSynthèse n'est pas homologué
pour les données de santé. L'appel doit être refusé.

AgentSynthèse est autorisé à lire des dossiers, mais Alice ne peut pas consulter
P-184. L'appel doit être refusé.

Alice et l'agent possèdent le droit de lecture, mais Alice a seulement demandé
une synthèse de P-184. Une lecture de P-991 doit être refusée.

Enfin, la politique locale peut interdire cet usage sur un dossier placé sous
restriction particulière. L'appel doit encore être refusé.

L'autorité effective ressemble donc à ceci :

```text
droits_effectifs =
    droits_de_l_utilisateur
    ∩ plafond_de_l_agent
    ∩ délégation_expresse
    ∩ besoin_de_la_tâche
    ∩ politique_de_la_ressource
```

Chaque terme peut réduire le résultat. Aucun ne peut l'agrandir à lui seul.

C'est cette logique que plusieurs travaux récents commencent à formaliser sous
la forme d'une *policy intersection* : la permission finale n'appartient à
aucun acteur pris isolément. Elle existe seulement dans la partie commune de
leurs politiques.

## L'intersection commence à être écrite noir sur blanc

La [RFC 8693](https://www.rfc-editor.org/rfc/rfc8693) permet l'échange de tokens
et la représentation du sujet et de l'acteur. Elle ne définit pas un algorithme
universel d'intersection des droits. Le token produit dépend de la politique du
serveur d'autorisation.

Des travaux IETF plus récents rendent cette règle explicite. Le brouillon
[*Cross-Domain AuthZ Information Sharing for Agents*](https://datatracker.ietf.org/doc/draft-diaconu-agents-authz-info-sharing/)
publié en février 2026 propose de calculer les droits d'un agent destinataire
comme l'intersection de quatre ensembles :

```text
portée délégable de l'agent parent
∩ portée intrinsèque de l'agent destinataire
∩ délégation explicite pour cette invocation
∩ politique du domaine destinataire
```

Le texte exige aussi que la portée ne puisse que diminuer ou rester identique à
chaque délégation.

Il s'agit d'un Internet-Draft, donc d'un travail en cours et non d'un standard
établi. Mais il est intéressant de voir cette formule apparaître dans un
document consacré aux agents. Elle rejoint directement le principe des
capacités atténuables comme Macaroons et Biscuit, que le brouillon cite
d'ailleurs comme références conceptuelles.

Ce n'est pas une convergence sur un format. C'est une convergence sur un
invariant :

> Une délégation ne doit jamais créer de pouvoir par addition.

## Pourquoi le rôle de l'agent ne suffit pas

Un rôle décrit une autorité relativement stable. Une tâche est beaucoup plus
étroite et beaucoup plus courte.

Le rôle `agent-clinique` peut indiquer qu'AgentSynthèse est techniquement
autorisé à manipuler certaines données de santé. Il ne prouve pas qu'Alice lui
a demandé de lire P-184 aujourd'hui. Le droit d'Alice ne prouve pas davantage
que cet agent particulier est acceptable.

L'agent ne doit donc pas recevoir :

```text
les droits d'Alice
```

ni même :

```text
les droits du rôle agent-clinique
```

Il doit recevoir leur intersection, réduite par le mandat de la tâche et par la
politique de l'API.

## Le serveur d'autorisation peut calculer cette intersection

Dans une architecture OAuth, un composant central collecte les éléments
nécessaires et émet un token réduit :

```text
token d'Alice
+ identité d'AgentSynthèse
+ consentement
+ demande structurée
+ politique
        ↓
serveur d'autorisation
        ↓
token délégué limité
```

La [RFC 9396 sur les Rich Authorization Requests](https://www.rfc-editor.org/rfc/rfc9396)
permet d'exprimer une demande plus structurée qu'une simple chaîne de scopes :
type d'action, emplacement, montant ou autres détails propres au domaine.

Cela rapproche le token de la tâche. La sécurité dépend toutefois de la qualité
de la politique centrale et des données disponibles au moment de l'émission.

Si AgentSynthèse possède ailleurs un compte de service plus puissant, il peut
contourner le beau token réduit. Si un endpoint accepte encore le JWT général
d'Alice, le chemin faible subsiste. L'intersection doit être une propriété de
tous les chemins d'accès, pas seulement du parcours nominal.

## La limitation que l'intersection ne résout pas

Au moment où Alice lance la tâche, nous ne connaissons pas forcément les
patients concernés.

Elle demande :

> Prépare les synthèses de ma consultation de cet après-midi.

La liste exacte sera fournie par une première API. Faut-il donner dès le départ
à l'agent un droit sur tous les patients qu'Alice pourrait voir ? Ce serait trop
large. Faut-il n'en donner aucun ? La tâche ne peut pas commencer.

Le serveur d'autorisation sait calculer une intersection sur les faits qu'il
connaît. Le workflow agentique fait apparaître de nouveaux faits pendant son
exécution.

Voilà la limite suivante : l'autorité d'une tâche ne peut pas toujours être
entièrement calculée au départ. Elle doit parfois évoluer à partir des réponses
obtenues.

## Sources

- IETF, [RFC 8693 : OAuth 2.0 Token Exchange](https://www.rfc-editor.org/rfc/rfc8693)
- IETF Internet-Draft, [Cross-Domain AuthZ Information Sharing for Agents](https://datatracker.ietf.org/doc/draft-diaconu-agents-authz-info-sharing/), version de février 2026, proposition en cours et non standard établi
- IETF, [RFC 9396 : OAuth 2.0 Rich Authorization Requests](https://www.rfc-editor.org/rfc/rfc9396)
