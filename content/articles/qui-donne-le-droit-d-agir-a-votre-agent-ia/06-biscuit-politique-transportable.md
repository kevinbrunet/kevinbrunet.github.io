---
title: "Biscuit transforme un token en politique transportable"
slug: "biscuit-politique-transportable"
date: 2026-10-08
description: "Les tokens Biscuit transportent faits, règles et restrictions avec la tâche, tout en laissant à chaque API le dernier mot."
categories: ["Intelligence artificielle", "Sécurité", "Architecture logicielle"]
series: ["qui-donne-le-droit-d-agir-a-votre-agent-ia"]
series_order: 6
collection: "ARCHITECTURE"
cover: "/images/articles/06-biscuit-politique-transportable.fr.png"
draft: false
---
Un JWT transporte généralement des claims :

```text
sub = alice
act = agent-synthese
scope = patient.read
```

Biscuit peut transporter des faits et des restrictions interprétés par un
langage logique :

```datalog
user("alice");
agent("agent-synthese");
right("consultation:2026-07-25-pm", "list_patients");
```

Ce n'est pas seulement une différence de syntaxe. Le token peut évoluer pendant
sa circulation, et chaque origine possède un niveau de confiance distinct.

## Un token fait de blocs

Un Biscuit commence par un bloc d'autorité signé par l'émetteur. Ce bloc définit
les faits et les règles de base.

Le détenteur peut ensuite ajouter un bloc :

```datalog
check if operation("list_patients");
check if consultation("2026-07-25-pm");
check if time($t), $t < 2026-07-25T18:00:00Z;
```

Ces vérifications réduisent l'usage du token. Pour qu'un appel soit accepté,
tous les checks accumulés doivent réussir.

La liste des blocs est protégée par une chaine de signatures. Retirer ou
modifier un bloc invalide la preuve. Le détenteur peut donc fabriquer un token
dérivé plus étroit sans posséder la clé privée racine.

La [documentation d'Eclipse Biscuit](https://doc.biscuitsec.org/getting-started/introduction)
appelle cette propriété l'atténuation hors ligne.

## Le service conserve le dernier mot

Le token ne décide pas seul.

Lors d'un appel, l'API ajoute des faits qu'elle connait :

```datalog
resource("consultation:2026-07-25-pm");
operation("list_patients");
time(2026-07-25T13:58:00Z);
```

Puis son *authorizer* applique les règles locales :

```datalog
allow if
  resource($r),
  operation($op),
  right($r, $op);

deny if true;
```

Les checks contenus dans le token sont cumulatifs. Les policies `allow` et
`deny` restent du côté de l'application. Selon la
[documentation sur les politiques Biscuit](https://doc.biscuitsec.org/getting-started/authorization-policies),
un token peut ajouter des restrictions, mais seule l'application définit la
politique qui l'approuve finalement.

Cette séparation est essentielle. L'agent transporte une capacité. L'API reste
souveraine sur ses ressources.

## Un bloc peut contenir des faits, des règles et des checks

Ajouter un bloc ne signifie pas nécessairement ajouter une permission. Biscuit distingue plusieurs types d'instructions.

Un **fait** affirme qu'une information est vraie :

```datalog
right("consultation:2026-07-25-pm", "list_patients");
document_type("clinical_note");
```

Une **règle** permet de déduire de nouveaux faits à partir de faits existants :

```datalog
can_read($document) <-
  assigned_document($document),
  document_type($document, "clinical_note");
```

Un **check** n'affirme rien. Il impose une condition à l'utilisation du token :

```datalog
check if operation("read_document");
check if time($t), $t < 2026-07-25T14:30:00Z;
```

Tous les checks accumulés dans les différents blocs doivent réussir. Ajouter un check ne crée donc pas le droit `read_document`. Cela signifie seulement que le token ne pourra être utilisé que pour cette opération, à condition qu'un droit correspondant existe déjà.

Biscuit examine ensuite l'origine des instructions. Chaque fait et chaque règle reste associé au bloc qui l'a introduit. L'authorizer peut alors décider quelles origines il accepte pour prendre sa décision :

- le bloc d'autorité signé par l'émetteur
- les faits fournis par l'authorizer lui-même
- un bloc signé par un tiers reconnu
- ou, si la politique le prévoit explicitement, d'autres blocs.

Cette distinction entre **nature** et **origine** est essentielle :

```text
la syntaxe indique ce que fait l'instruction
la provenance indique si l'authorizer peut lui faire confiance.
```

Un détenteur peut ainsi écrire un nouveau fait dans un bloc ordinaire. Mais il ne peut pas obliger l'authorizer à utiliser ce fait pour lui accorder un droit.

À l'inverse, un check ajouté par le détenteur est toujours une condition supplémentaire. Il peut rendre le token moins puissant ou même inutilisable, mais jamais lui donner davantage d'autorité.


## Pourquoi l'agent ne peut pas écrire ses propres droits

La chaine de signatures garantit l'intégrité et l'ordre des blocs.

Les règles de confiance et de portée déterminent ensuite quelles origines l'authorizer accepte pour chaque décision.

Un détenteur peut donc ajouter :

```datalog
right("patient:P-999", "read");
```

Ce fait sera bien présent dans le token et protégé par la chaine cryptographique. Mais son origine reste un bloc ajouté par l'agent.

Si la politique d'autorisation ne fait confiance qu'au bloc d'autorité et aux faits fournis par l'API, elle ne prendra pas ce nouveau droit en compte.

L'agent peut écrire une affirmation, il ne peut pas décider que l'API doit la croire.

Biscuit associe les faits à leur bloc d'origine. Par défaut, les politiques de l'authorizer font confiance aux faits du bloc d'autorité et à ceux fournis par l'authorizer lui-même. Elles ne font pas confiance aux faits arbitraires ajoutés dans un bloc ordinaire sans que l'on l'autorise spécifiquement.

Le bloc frauduleux peut être cryptographiquement valide et logiquement inutile.

Par contre, les "check if" ajoutés dans un bloc ordinaire sont des conditions supplémentaires que le token impose à son propre usage. Ils ne peuvent alterer la liste des règles déjà émises.

## L'atténuation convient aux sous-agents

Avec ce principe de bloc additif uniquement, l'AgentSynthèse peut recevoir une capacité portant sur la consultation. Avant de la transmettre à AgentExtracteur, il ajoute ou fait ajouter par un authorizer sépifique :

```datalog
check if operation("read_document");
check if document_type("clinical_note");
check if time($t), $t < 2026-07-25T14:30:00Z;
```

AgentExtracteur ne reçoit que le dérivé. Il ne peut pas retirer ces conditions.

S'il crée lui-même une sous-tâche, il peut encore ajouter une restriction. L'architecture supporte ainsi des chemins qui n'étaient pas connus au moment où le token racine a été émis.

Chaque maillon sait transmettre moins sans devoir recontacter l'émetteur.

## Biscuit réalise une intersection dans l'objet

Dans l'architecture OAuth présentée plus tôt, un serveur calcule l'intersection
et réémet un token.

Avec Biscuit, une partie de l'intersection se matérialise dans la chaine :

```text
autorité initiale
∩ check ajouté par l'orchestrateur
∩ check ajouté par le sous-agent
∩ faits de la requête
∩ politique locale de l'API
```

Les deux approches ne sont pas ennemies. OAuth peut établir qui agit pour qui et
émettre la capacité initiale. Biscuit peut transporter les restrictions propres
à la tâche et à ses sous-tâches.

## La propriété moins connue : les blocs signés par un tiers

Jusqu'ici, chaque bloc ajouté ne pouvait que restreindre.

La spécification prévoit aussi des *third-party blocks*. Un service externe
peut signer un bloc destiné à un token précis. L'authorizer peut choisir de
faire confiance aux faits issus de cette clé publique.

C'est ce mécanisme qui permet de revenir au problème de la liste des patients.
Le service de consultation peut attester :

```datalog
listed_patient("task:7841", "P-184");
listed_patient("task:7841", "P-207");
listed_patient("task:7841", "P-311");
```

Ces faits ne viennent ni de l'agent ni de l'émetteur initial. Ils viennent d'une
API reconnue, après une étape réelle du workflow.

L'article suivant montre comment une réponse d'API peut ainsi ouvrir une
autorité nouvelle, sans transformer le token en permission auto-signée.

## Sources

- Eclipse Foundation, [Eclipse Biscuit project](https://projects.eclipse.org/projects/technology.biscuit), projet au statut Incubating
- Eclipse Biscuit, [Introduction](https://doc.biscuitsec.org/getting-started/introduction)
- Eclipse Biscuit, [Authorization Policies](https://doc.biscuitsec.org/getting-started/authorization-policies)
- Eclipse Biscuit, [Specifications](https://doc.biscuitsec.org/reference/specifications)
