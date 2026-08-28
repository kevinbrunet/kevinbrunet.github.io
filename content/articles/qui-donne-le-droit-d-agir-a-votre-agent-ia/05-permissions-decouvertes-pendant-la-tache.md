---
title: "On ne connaît pas toujours les bonnes permissions au début de la tâche"
seo_title: "Permissions dynamiques d'un agent IA : éviter le passe-partout"
slug: "permissions-decouvertes-pendant-tache"
date: 2026-09-03
description: "Une tâche découvre parfois son périmètre en cours d'exécution : l'autorité doit pouvoir évoluer sans devenir un passe-partout."
categories: ["Intelligence artificielle", "Sécurité", "Architecture logicielle"]
series: ["qui-donne-le-droit-d-agir-a-votre-agent-ia"]
series_order: 5
collection: "ARCHITECTURE"
cover: "/images/articles/05-permissions-decouvertes-pendant-la-tache.fr.png"
draft: false
---
Alice demande :

> Prépare les synthèses de ma consultation de cet après-midi.

À cet instant, l'agent ne connait aucun identifiant patient. Il doit commencer
par appeler :

```text
list_patients(consultation = "2026-07-25-pm")
```

La réponse contient :

```text
P-184
P-207
P-311
```

Ces trois identifiants changent la tâche. Avant la réponse, l'agent avait le
droit de rechercher la consultation. Après la réponse, il doit pouvoir lire
trois dossiers précis.

L'autorité nécessaire vient d'évoluer.

## Le dilemme du token initial

Nous pouvons remettre au départ un token très large :

```text
patient.read
```

L'agent trouvera toujours les dossiers dont il a besoin. Il pourra aussi tenter
d'en lire beaucoup d'autres.

Nous pouvons au contraire créer une autorisation limitée aux identifiants
connus. Mais il n'y en a encore aucun.

Le problème ne vient pas d'un manque de précision dans le prompt. Il apparait
dans toutes les tâches où une première étape découvre les ressources des
suivantes :

```text
rechercher des patients, puis ouvrir leurs dossiers
lister les factures en anomalie, puis télécharger leurs pièces
trouver les incidents d'un service, puis consulter leurs journaux
identifier les dépôts concernés, puis préparer des modifications
```

Une autorisation entièrement statique oblige à choisir entre deux défauts :
trop de pouvoir au départ ou un aller-retour vers un serveur central après
chaque découverte.

## La réponse doit pouvoir modifier le futur

L'idée intéressante consiste à ne plus considérer la réponse d'API comme de
simples données.

Le service de consultation est précisément celui qui sait quels patients
appartiennent à la consultation demandée. Sa réponse peut donc fournir deux
choses :

```text
les identifiants utiles au modèle
+ une preuve exploitable par les API suivantes
```

Conceptuellement :

```json
{
  "patients": ["P-184", "P-207", "P-311"],
  "authorization_evidence": "<preuve signée>"
}
```

Le modèle lit la liste. La couche d'autorisation utilise la preuve.

Le service des dossiers peut alors accepter P-184, P-207 et P-311, mais refuser
P-999. L'agent n'a pas reçu un scope `patient.read` général. Il a reçu la suite
autorisée d'une étape précise.

## Est-ce vraiment "ajouter des droits" ?

Oui du point de vue de la tâche : avant l'appel, elle ne pouvait pas ouvrir
P-184 ; après la réponse, elle le peut.

Mais il faut éviter une formulation dangereuse. L'agent ne s'accorde pas de
nouveaux droits. Un service déjà reconnu comme autorité produit un fait signé,
et un autre service a décidé à l'avance de faire confiance à ce type de fait.

L'autorité nouvelle vient donc de la rencontre entre :

```text
le mandat initial d'Alice
∩ la politique d'AgentSynthèse
∩ le résultat signé du service de consultation
∩ la politique locale du service des dossiers
```

On retrouve l'intersection. Une nouvelle preuve ne remplace pas les limites
précédentes. Elle complète une condition qui manquait.

## Un JWT pourrait porter cette preuve

Cette architecture n'exige pas nécessairement Biscuit. Le service peut demander
au serveur d'autorisation de réémettre un JWT limité aux trois patients. Il peut
émettre des capacités séparées par patient. Il peut conserver la liste dans une
session serveur et retourner seulement un identifiant opaque.

Ces options sont valables. Elles ont un point commun : un composant central ou
le service métier doit reconstruire un nouveau credential après chaque étape.

Le défi augmente lorsque la tâche se ramifie :

```text
un agent trouve les patients
un autre extrait les documents
un troisième prépare les synthèses
un quatrième vérifie les incohérences
```

Chaque sous-agent doit recevoir moins que le précédent, tout en profitant des
faits légitimes découverts par les services.

## Ce que nous cherchons maintenant

Il nous faut un objet qui sache porter :

```text
le mandat initial
les restrictions accumulées
les ressources découvertes
l'origine de chaque fait
les preuves signées par des services différents
```

Et il faut empêcher l'agent d'ajouter lui-même :

```text
patient_accessible("P-999")
```

comme si cette affirmation venait du service de consultation.

Cette distinction entre "un bloc ajouté par le détenteur" et "un bloc signé
par une autorité reconnue" est au coeur de Biscuit.

L'article suivant présente le mécanisme sans encore parler de workflow. Nous
verrons d'abord comment un token peut transporter une politique, tout en
garantissant qu'un détenteur ordinaire ne sait que la réduire.

## Sources

- IETF, [RFC 9396 : OAuth 2.0 Rich Authorization Requests](https://www.rfc-editor.org/rfc/rfc9396), utilisé ici pour situer les demandes d'autorisation structurées
- Eclipse Biscuit, [Specifications](https://doc.biscuitsec.org/reference/specifications), source du mécanisme de blocs et de signatures tierces introduit dans l'article suivant
