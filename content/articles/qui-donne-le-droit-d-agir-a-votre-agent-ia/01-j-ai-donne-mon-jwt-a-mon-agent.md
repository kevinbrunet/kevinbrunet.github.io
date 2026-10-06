---
title: "J'ai donné mon JWT à mon agent. J'ai aussi effacé l'agent."
seo_title: "JWT et agent IA : pourquoi partager le token est dangereux"
slug: "jwt-agent-efface-agent"
date: 2026-09-03
description: "Transmettre le JWT d'un utilisateur à un agent lui donne une identité trop large et rend l'acteur réel invisible dans les journaux."
categories: ["Intelligence artificielle", "Sécurité", "Architecture logicielle"]
tags: ["ai-security"]
series: ["qui-donne-le-droit-d-agir-a-votre-agent-ia"]
series_order: 1
collection: "ARCHITECTURE"
cover: "/images/articles/01-j-ai-donne-mon-jwt-a-mon-agent.fr.png"
draft: false
---
Alice est clinicienne. Elle ouvre son application métier et s'authentifie. Son
navigateur possède un JWT qui lui permet de consulter les dossiers patients
auxquels elle a accès.

Elle demande maintenant à un agent :

> Prépare la synthèse des patients de ma consultation de cet après-midi.

La première intégration est presque évidente. L'application transmet le token
d'Alice à l'agent. Celui-ci peut alors appeler les mêmes API que l'écran.

```text
Alice se connecte
        ↓
l'application reçoit son JWT
        ↓
elle remet ce JWT à l'agent
        ↓
l'agent appelle les API comme Alice
```

Tout fonctionne. C'est précisément pour cela que le problème risque de passer
en production.

## Une mission étroite reçoit une identité large

La tâche confiée à l'agent est limitée. Elle concerne une consultation, une
liste de patients et une préparation de synthèses.

Le token d'Alice ne connait rien de tout cela. Il a été conçu pour une session
interactive complète :

```json
{
  "sub": "alice",
  "aud": "patient-api",
  "scope": "patient.read summary.write"
}
```

Il exprime ce qu'Alice peut faire dans l'application. Il n'exprime pas ce que
cette tâche doit faire.

Si Alice peut consulter mille dossiers dans le cadre de son activité, l'agent
dispose potentiellement du même périmètre. Une mauvaise sélection d'outil, un
paramètre halluciné ou une instruction hostile dissimulée dans un document
peut exploiter toute cette latitude.

Le JWT peut pourtant être irréprochable. Sa signature est valide. Son audience
est correcte. Il n'est pas expiré.

La cryptographie répond bien à la question posée. C'est la question qui était
trop pauvre :

```text
Alice peut-elle appeler cette API ?
```

La question utile était :

```text
cet agent peut-il effectuer cette opération
pour la tâche précise qu'Alice vient de lui confier ?
```

## Dans les journaux, Alice fait tout

Supposons que l'agent lise le bon dossier, prépare la synthèse, puis la publie
avant la revue attendue.

L'API reçoit à chaque fois :

```text
sub = alice
```

Ses journaux racontent donc :

```text
14:02 Alice a consulté le dossier P-184
14:04 Alice a créé la synthèse
14:05 Alice a publié la synthèse
```

La dernière ligne est techniquement exacte et opérationnellement trompeuse.
Alice a demandé une préparation. Elle n'a pas choisi l'outil de publication,
ses paramètres ni le moment de l'appel. Ces décisions ont été prises par
l'agent.

Après un incident, le journal ne permet plus de distinguer quatre scénarios :
Alice a publié elle-même, l'agent a mal interprété la demande, un document a
détourné le raisonnement, ou un autre composant a réutilisé le Bearer token.

La [RFC 6750](https://www.rfc-editor.org/rfc/rfc6750) rappelle la propriété
fondamentale d'un Bearer token : le composant qui le possède peut l'utiliser.
Le token ne prouve pas que la main qui déclenche l'appel est encore celle
d'Alice.

En transmettant son JWT à l'agent, nous n'avons donc pas seulement transmis ses
permissions. Nous avons fait disparaitre le logiciel qui les exerce.

## Le problème ne se limite pas à l'audit

Si l'agent et Alice portent la même identité, il devient difficile de leur
appliquer des politiques différentes.

On peut vouloir autoriser Alice à valider une synthèse, mais limiter son agent à
la préparation. On peut vouloir révoquer AgentSynthèse sans fermer la session
d'Alice. On peut vouloir plafonner le nombre de dossiers lus par une tâche
automatisée sans limiter l'usage normal de l'application.

Avec `sub = alice` partout, ces distinctions arrivent trop tard. Pour l'API, il
n'existe qu'un seul acteur.

Cette confusion est souvent décrite comme un problème de traçabilité. Elle est
plus profonde. Un système ne peut pas appliquer une règle à une entité qu'il
est incapable de nommer.

## Première règle : ne jamais confondre le mandant et le mandataire

Le montage doit conserver deux réponses :

```text
pour qui le travail est-il réalisé ?  Alice
qui exécute réellement les appels ?   AgentSynthèse
```

Cela ne nous dit pas encore ce qu'AgentSynthèse peut faire. Nous n'avons résolu
ni la granularité des droits, ni l'ordre du workflow, ni l'approbation humaine.
Mais nous avons découvert le premier invariant :

> Aucun agent ne devrait recevoir le token nu de son utilisateur.

Il faut une délégation qui garde Alice comme origine du mandat et
AgentSynthèse comme acteur réel.

Avant de construire cette délégation, un autre défaut du montage initial mérite
d'être observé. En donnant à l'agent les API de l'application, nous lui avons
aussi donné une liberté que l'utilisateur n'avait jamais eue : celle d'appeler
les bonnes actions dans n'importe quel ordre.

C'est le sujet de l'article suivant.

## Sources

- IETF, [RFC 6750 : OAuth 2.0 Bearer Token Usage](https://www.rfc-editor.org/rfc/rfc6750)
- IETF, [RFC 7519 : JSON Web Token](https://www.rfc-editor.org/rfc/rfc7519)
