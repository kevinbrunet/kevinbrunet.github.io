---
title: "Dix documents sur onze passent le filtre par motifs"
slug: "proxy-ia-limites-filtre-motifs"
date: 2026-11-10
description: "Sur les onze cas initiaux du prototype, le filtre déterministe bloque une clé API et laisse cinq autres contenus sensibles à analyser."
categories: ["Intelligence artificielle", "Cybersécurité", "Architecture logicielle"]
series: ["quand-le-proxy-comprend-ce-qu-il-protege"]
series_order: 2
collection: "SYSTÈMES"
cover: "/images/articles/shieldstral/02.png"
draft: false
---

{{< callout variant="scene" label="Point de départ" >}}
Le proxy LiteLLM de Nora connait son projet, le modèle demandé et la destination de la requête. Il peut maintenant exécuter un premier contrôle avant tout appel externe : rechercher les secrets qui possèdent une forme reconnaissable.
{{< /callout >}}

Une clé API possède souvent un préfixe caractéristique. Un IBAN suit une structure. Une adresse électronique ou un numéro de téléphone peut être localisé dans le texte. Ces cas ne demandent pas de comprendre le métier de Nora.

## La première couche cherche des formes

Pour mesurer ce qu'elle protège réellement, j'ai préparé 11 documents : six contenaient une information sensible et cinq pouvaient être transmis. Je les ai d'abord soumis à un contrôle déterministe recherchant des motifs connus.

Ce contrôle a reconnu et bloqué une clé d'API. Les dix autres documents ont franchi le filtre. Parmi eux se trouvaient pourtant cinq documents sensibles : deux descriptions du procédé Atlas, un secret métier sans nombres, une incitation à la fraude financière et un dossier médical identifiable.

```text
11 documents
    ↓ contrôle par motifs
1 clé d'API bloquée
10 documents transmis à l'étape suivante
    ├── 5 autorisés
    └── 5 sensibles
```

{{< callout variant="key" label="Périmètre de la mesure" >}}
Ces chiffres décrivent le détecteur limité du prototype. Ils ne mesurent pas les performances de l’ensemble des moteurs DLP ni celles de Presidio, qui combine plusieurs méthodes, dont des modèles de reconnaissance d’entités.
{{< /callout >}}

Le filtre a donc pris une décision certaine dans un cas sur onze. Utilisé seul, il n'aurait pas empêché cinq contenus sensibles d'atteindre un fournisseur externe.

Cette campagne initiale explique le titre de l'article. Le POC a ensuite été étendu à 14 documents pour tester l’expurgation sémantique et le recontrôle. Le constat de cette première étape ne change pas : la clé d'API est toujours le seul cas arrêté sans appel à Shieldstral ; les 13 autres atteignent l'analyse sémantique.

## Ce qui est localisable peut être pseudonymisé

Un moteur comme Presidio peut reconnaitre certaines entités et les remplacer par des pseudonymes :

```text
Original : Le compte de Nora est FR76 3000 6000 0112 3456 7890 189
Externe  : Le compte de <PERSON_1> est <IBAN_1>
```

Le modèle frontière reçoit une phrase encore exploitable sans voir les valeurs originales. Le proxy conserve localement la correspondance et peut, si l'architecture le prévoit, restaurer les pseudonymes dans la réponse rendue à l'utilisateur autorisé.

Cette protection reste indispensable. Lorsqu’un motif suffit à appliquer la règle, il est préférable de conserver ce contrôle déterministe. Reconnaître une entité ne suffit toutefois pas toujours à décider si sa transmission est autorisée. Mais la majorité des cas sensibles du jeu de test ne possédaient pas cette propriété.

## Un document peut être sensible sans contenir de motif remarquable

Le dossier de Nora appartient au projet fictif Atlas. Il décrit une séquence industrielle, plusieurs températures et une vitesse de refroidissement. Aucun élément isolé n'est secret. Les mêmes nombres pourraient apparaitre dans un bulletin météo ou un tableau de maintenance.

Ce qui est protégé est leur combinaison dans une procédure précise. La politique de l'entreprise interdit de transmettre ce savoir-faire à un système externe.

Le proxy peut extraire les nombres. Il peut savoir que la destination est un fournisseur extérieur. Il ne sait pas relier automatiquement ce passage à la notion de savoir-faire industriel définie par l'entreprise.

Ajouter les mots « confidentiel », « procédé » ou « interne » à une liste ne résout pas le problème. Le document peut les éviter. La même liste peut aussi bloquer des textes ordinaires qui utilisent ces mots sans révéler de secret.

## La protection suivante doit comprendre le sens

La configuration du prototype possède le bon emplacement, mais il lui manque encore une capacité : comparer le sens du document à une politique métier.

C'est à ce moment que Shieldstral entre dans l'architecture. L'entreprise décrit en langage naturel ce qu'elle cherche à protéger, puis le modèle évalue cette question sur les dix documents que le premier filtre n'a pas pu trancher.

Le prochain article montre ce que Shieldstral ajoute réellement, comment la politique devient une question posée au document et pourquoi cette nouvelle couche ne remplace pas les contrôles déterministes.

---

{{< closing-question label="À retenir" >}}
Les motifs protègent les secrets reconnaissables par leur forme. Les secrets métier demandent aussi une évaluation du contenu.
{{< /closing-question >}}

## Sources

- [Rapport de qualification Shieldstral — 2 septembre 2026](/documents/shieldstral-qualification-2026-09-02.md)
- [Microsoft — Presidio](https://microsoft.github.io/presidio/)

**Pour continuer :** [Shieldstral ajoute un classifieur local piloté par la politique métier](/articles/shieldstral-classifieur-local-politique-metier/).
