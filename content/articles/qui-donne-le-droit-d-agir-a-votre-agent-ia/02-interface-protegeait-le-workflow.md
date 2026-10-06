---
title: "L'interface faisait respecter un workflow sans le dire"
seo_title: "Agent IA et API : l'interface cachait les règles du workflow"
slug: "interface-protegeait-workflow"
date: 2026-09-03
description: "En appelant directement les API, un agent peut contourner l'ordre des actions que l'interface imposait silencieusement à l'utilisateur."
categories: ["Intelligence artificielle", "Sécurité", "Architecture logicielle"]
tags: ["ai-security", "software-architecture"]
series: ["qui-donne-le-droit-d-agir-a-votre-agent-ia"]
series_order: 2
collection: "ARCHITECTURE"
cover: "/images/articles/02-interface-protegeait-le-workflow.fr.png"
draft: false
---
Dans l'application d'Alice, la préparation d'une synthèse suivait un parcours
simple :

```text
ouvrir la consultation
        ↓
afficher la liste des patients
        ↓
ouvrir un dossier
        ↓
préparer un brouillon
        ↓
faire relire
        ↓
publier
```

Personne n'appelait cela une politique de sécurité. C'était "le fonctionnement
de l'écran".

Pourtant, l'interface imposait des contraintes. Le bouton Publier n'apparaissait
pas avant la revue. Le dossier devait provenir de la consultation ouverte. Le
brouillon devait exister avant sa validation.

Puis nous avons exposé les mêmes actions à l'agent :

```text
list_patients
read_patient
create_draft
request_review
publish_summary
```

Pour le modèle, ce ne sont plus les étapes d'un parcours. Ce sont cinq outils
indépendants.

## Les mêmes actions, dans le mauvais ordre

L'agent peut appeler `publish_summary` avant `request_review`. Il peut conserver
l'identifiant d'un patient obtenu dans une ancienne conversation. Il peut
réessayer une opération avec un autre paramètre après un refus.

Chaque appel peut sembler valide pris isolément :

```text
Alice a le droit de lire des dossiers
Alice a le droit de créer des brouillons
Alice a le droit de publier
```

Et pourtant la séquence complète est invalide.

Le problème apparait parce que l'autorisation classique regarde souvent une
requête à la fois :

```text
acteur + action + ressource → permit ou deny
```

Le workflow ajoute une autre dimension :

```text
acteur + action + ressource + état atteint → permit ou deny
```

`publish_summary` n'est pas une action interdite. C'est une action interdite
maintenant, tant qu'une revue valide n'existe pas.

## L'interface n'était pas la règle

On pourrait demander à l'agent de suivre le manuel :

> Toujours lister les patients avant d'ouvrir un dossier. Toujours demander une
> revue avant de publier.

Cette instruction est utile pour guider le modèle. Elle ne constitue pas la
garantie.

Un prompt peut être oublié, contredit ou mal interprété. Un autre agent peut
appeler directement l'API. Une nouvelle interface peut ignorer la convention.
Un attaquant n'utilisera probablement pas l'écran.

L'OWASP consacre une catégorie de son classement API aux
[flux métier sensibles insuffisamment protégés](https://owasp.org/API-Security/editions/2023/en/0xa6-unrestricted-access-to-sensitive-business-flows/).
Le point important dépasse la fraude automatisée décrite dans ces exemples :
une opération légitime n'est pas nécessairement légitime à n'importe quel
moment du processus.

Si l'ordre est important, la règle doit vivre derrière l'interface, à la
frontière qui produit l'effet.

Nous sommes d'accord que les règles de bonnes pratiques imposent ce genre de précautions mais bien souvent dans ma carrière j'ai pu observer des APIs qui ne satisfaisaient pas cette contrainte. Suffisamment pour me sembler essentiel de revenir sur le sujet dans cet article car un agent lâché sur des APIs mal conçu peut faire des ravages dans une entreprise.

## Le refus doit enseigner l'étape suivante

Déplacer la règle dans l'API ne signifie pas répondre par un opaque
`403 Forbidden`.

Un agent a besoin d'une erreur exploitable :

```json
{
  "error": "workflow_order_violation",
  "current_state": "draft_created",
  "required_state": "review_approved",
  "allowed_next_action": "request_review",
  "rule": "A summary must be reviewed before publication."
}
```

L'API refuse et décrit la marche autorisée. La même règle sert alors à la
sécurité, à l'orchestration et à l'explication.

Cela rejoint une transformation plus large : la règle métier ne devrait plus
être seulement écrite dans un wiki que le modèle est censé avoir lu. Elle peut
être compilée dans le service et apparaître au moment exact où une tentative la
viole. Nous reviendrons sur cette idée dans une autre série.

## Une machine à états ne suffit pas encore

Nous pourrions stocker côté serveur :

```text
task-7841 = review_approved
```

Puis vérifier cet état avant la publication. C'est une solution parfaitement
valable. Elle devient toutefois plus complexe lorsque le parcours traverse
plusieurs services, plusieurs organisations ou plusieurs sous-agents.

Qui possède l'état ? Comment le service B sait-il que le service A a bien
réalisé l'étape précédente ? Comment éviter qu'un identifiant de tâche soit
réutilisé dans un autre contexte ? Comment transmettre la preuve sans donner à
tous les services un accès direct à la même base centrale ?

Nous n'allons pas répondre tout de suite. Il nous manque d'abord une information
plus élémentaire.

Dans les exemples précédents, toutes les API voient encore seulement Alice.
Même une excellente machine à états ne peut pas distinguer une publication
directe d'Alice d'une publication choisie par son agent.

La prochaine étape consiste donc à faire apparaitre le mandataire : l'agent ne
doit plus agir comme Alice, mais pour Alice.

## Sources

- OWASP, [API6:2023 : Unrestricted Access to Sensitive Business Flows](https://owasp.org/API-Security/editions/2023/en/0xa6-unrestricted-access-to-sensitive-business-flows/)
