---
title: "Le workflow peut devenir une chaîne de preuves"
seo_title: "Sécurité d'un workflow agent IA : créer une chaîne de preuves"
slug: "workflow-chaine-de-preuves"
date: 2026-09-03
description: "Quand chaque appel exige la preuve du précédent, le système impose l'ordre du workflow sans dépendre de l'obéissance de l'agent."
categories: ["Intelligence artificielle", "Sécurité", "Architecture logicielle"]
series: ["qui-donne-le-droit-d-agir-a-votre-agent-ia"]
series_order: 8
collection: "ARCHITECTURE"
cover: "/images/articles/08-workflow-chaine-de-preuves.fr.png"
draft: false
---
Au début de cette série, l'interface imposait ce parcours :

```text
lister les patients
        ↓
ouvrir un dossier
        ↓
créer un brouillon
        ↓
obtenir une revue
        ↓
publier
```

Quand nous avons donné les API à l'agent, ces étapes sont devenues des outils
indépendants. Le modèle pouvait appeler les bonnes actions dans le mauvais
ordre.

Les réponses signées permettent maintenant de reconstruire la contrainte sans
revenir à une interface rigide.

## Chaque étape rend la preuve nécessaire à la suivante

Le service de consultation rend un bloc signé :

```datalog
patients_listed("task:7841", "result:42");
```

Le service des dossiers n'accepte une lecture que si ce résultat signé contient
le patient demandé. Après la lecture, il rend à son tour :

```datalog
record_read("task:7841", "P-184", "version:7");
```

Le service de brouillon exige cette preuve avant d'accepter
`create_draft`. Il signe ensuite :

```datalog
draft_created("task:7841", "draft:991", "input-version:7");
```

Le service de revue exige le brouillon. Le service de publication exige une
revue portant sur la même version.

```text
preuve de liste
      ↓
preuve de lecture
      ↓
preuve du brouillon
      ↓
preuve de revue
      ↓
autorisation de publier
```

L'agent peut toujours décider quand appeler les outils. Il ne peut plus
fabriquer l'état nécessaire à l'étape suivante.

## L'ordre ne vit plus dans le prompt

Nous pouvons continuer à écrire dans les instructions :

> Toujours faire relire une synthèse avant de la publier.

Cette phrase aide le modèle à planifier. La garantie se trouve ailleurs :

```datalog
allow if
  operation("publish"),
  resource("draft:991"),
  reviewed("draft:991", "version:3")
  trusting <clé-du-service-de-revue>;
```

Sans la preuve de revue, l'API refuse. Une injection de prompt peut persuader
l'agent que la revue est inutile. Elle ne peut pas signer à la place du service
de revue.

La politique devient une machine à états distribuée dont les transitions sont
prouvées.

## Le détail cryptographique qui rend l'ordre crédible

Un simple certificat "la revue a été faite" peut être copié dans une autre
tâche ou associé à un brouillon modifié.

La preuve doit donc lier :

```text
l'identifiant de tâche
la ressource exacte
sa version ou son hash
l'étape précédente
l'audience suivante
une échéance
```

Dans Biscuit, une demande de bloc tiers contient le contexte de la signature
précédente du token. D'après la
[spécification](https://doc.biscuitsec.org/reference/specifications), la
signature externe est ainsi attachée à un Biscuit précis. Pour construire une
chaine séquentielle, la demande adressée au service suivant est générée après
l'ajout du bloc précédent.

La structure append-only ne prouve pas à elle seule qu'un processus métier a été
correctement exécuté. Elle fournit le support permettant d'enchainer des
attestations que chaque service signe après avoir effectué sa propre
vérification.

## Le refus devient une transition proposée

Si AgentSynthèse tente de publier trop tôt, l'API peut répondre :

```json
{
  "error": "missing_authorization_evidence",
  "missing_fact": "reviewed(draft:991, version:3)",
  "allowed_next_action": "request_review",
  "approval_endpoint": "/reviews"
}
```

Cette erreur ne demande pas au modèle de mémoriser une documentation générale.
Elle lui présente la règle au moment de l'infraction et lui indique la
transition permise.

La policy ne sert donc plus seulement à fermer une porte. Elle expose le graphe
des prochains mouvements légitimes.

## Le workflow peut se ramifier

Une machine à états n'est pas obligée d'être linéaire.

Après la lecture d'un dossier, la policy peut autoriser :

```text
extraire les allergies
ou
préparer la synthèse
ou
demander un document manquant
```

Puis exiger que certaines preuves soient réunies avant la suite :

```datalog
allow if
  operation("request_review"),
  draft_created($draft, $version),
  allergies_checked($patient, $source_version),
  based_on($draft, $source_version);
```

La logique décrit des préconditions, pas un script unique. L'agent conserve de
la liberté à l'intérieur de l'espace autorisé.

C'est précisément ce que l'interface traditionnelle avait du mal à faire. Elle
imposait souvent un seul parcours parce qu'il était coûteux d'en représenter
plusieurs. Une politique déclarative peut autoriser plusieurs chemins, tout en
interdisant les raccourcis dangereux.

## Ce mécanisme ne supprime pas tout état

Certaines propriétés ne peuvent pas être garanties par un token autonome.

Si une preuve doit être consommée une seule fois, le service doit mémoriser son
usage. Si une revue est révoquée, les vérificateurs doivent apprendre cette
révocation. Si deux agents travaillent en parallèle sur la même version, il
faut gérer la concurrence. Si le dossier change après la revue, le hash ou le
numéro de version doit rendre la preuve précédente inutilisable.

Le workflow transporté par les preuves ne remplace donc pas les transactions,
l'idempotence ou le contrôle de concurrence. Il évite surtout que la
progression repose sur la bonne volonté du modèle.

## L'étape suivante n'est pas toujours automatique

Nous savons maintenant forcer :

```text
liste avant lecture
lecture avant brouillon
revue avant publication
```

Mais qui produit la preuve de revue ?

Dans certains cas, un autre service automatique suffit. Dans d'autres, la règle
exige une décision humaine.

Deux architectures sont alors possibles. L'humain peut signer une approbation
qui autorise l'agent à exécuter un effet précis. Ou l'API finale peut refuser
formellement tout acteur de nature agentique et exiger un appel humain direct.

Cette différence est le dernier saut de la série.

## Sources

- Eclipse Biscuit, [Specifications : signature chain et third-party blocks](https://doc.biscuitsec.org/reference/specifications)
- OWASP, [API6:2023 : Unrestricted Access to Sensitive Business Flows](https://owasp.org/API-Security/editions/2023/en/0xa6-unrestricted-access-to-sensitive-business-flows/)
