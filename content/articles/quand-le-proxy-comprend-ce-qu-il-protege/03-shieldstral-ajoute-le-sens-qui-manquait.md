---
title: "Shieldstral ajoute un classifieur local piloté par la politique métier"
slug: "shieldstral-classifieur-local-politique-metier"
date: 2026-11-10
description: "Un classifieur spécialisé de 3 milliards de paramètres évalue localement le contenu selon une question de sécurité définie par l’entreprise."
categories: ["Intelligence artificielle", "Cybersécurité", "Architecture logicielle"]
tags: ["ai-security"]
series: ["quand-le-proxy-comprend-ce-qu-il-protege"]
series_order: 3
collection: "SYSTÈMES"
cover: "/images/articles/shieldstral/03.png"
draft: false
---

{{< callout variant="scene" label="Point de départ" >}}
Le proxy de Nora sait qu’elle demande un modèle frontière. Il sait aussi reconnaître un IBAN, une adresse électronique et certaines clés d’API. Il ne sait toujours pas que trois paragraphes de son dossier décrivent un savoir-faire industriel interdit à cette destination.
{{< /callout >}}

Shieldstral ajoute précisément ce regard à la configuration étudiée ici.

Les passerelles peuvent déjà intégrer des contrôles sémantiques. LiteLLM propose notamment un juge LLM avec des critères personnalisés. Ce mécanisme permet de poser la question ; son efficacité dépend du modèle choisi et de sa qualification. La documentation de l'intégration ne fournit pas de benchmark comparatif sur les secrets métier du projet Atlas.

L'approche Shieldstral est intéressante parce que le modèle est entraîné spécifiquement à comparer un contenu à une question de sécurité. Le papier de Mistral rapporte un F1 moyen de 84,9 % sur les benchmarks textuels et de 91,3 % sur son évaluation d'adaptation aux politiques. Ce sont des résultats publiés en faveur de ce classifieur spécialisé de 3 milliards de paramètres, pas une preuve de supériorité sur tout juge généraliste possible.

Au lieu d’enfermer toutes les règles dans une taxonomie choisie avant l’entraînement, il reçoit une question de sécurité avec le contenu à examiner. La politique métier devient une entrée du modèle.

## La politique devient une question posée au document

Pour le projet fictif Atlas, l’entreprise peut formuler la règle suivante :

> Ce contenu décrit-il les paramètres protégés du procédé Atlas, notamment des paliers de température, une vitesse de refroidissement ou leur séquence, interdits à un fournisseur externe ?

[Shieldstral](https://arxiv.org/abs/2607.25857) reçoit cette question avec le document. Il évalue les deux ensemble et produit une réponse binaire accompagnée d’un score continu dérivé des probabilités de `yes` et `no`.

Cette formulation change profondément le cycle de création d’une règle. L’entreprise n’a pas besoin de prévoir toutes les phrases qui pourraient exprimer une température, une cadence ou une séquence de fabrication. Elle doit toutefois nommer la classe d’information recherchée.

Dans le POC, les dix documents que le filtre par motifs n'avait pas pu trancher ont été soumis à cette question sémantique. Shieldstral leur attribue un score ; le proxy compare ensuite ce score aux seuils de la politique pour autoriser, transformer, rediriger ou bloquer la requête.

C'est l'avancée importante : la politique métier devient exécutable avant l'envoi du document. Le proxy ne cherche plus seulement une forme connue. Il peut vérifier qu'un texte décrit un savoir-faire précis, même si ce texte n'emploie ni le mot « secret » ni le vocabulaire attendu.

## Distinguer deux textes qui se ressemblent

Prenons deux documents contenant des températures et une vitesse :

```text
Document A : plusieurs paliers et une vitesse de refroidissement
             décrivent le procédé industriel Atlas.

Document B : plusieurs températures et une vitesse de vent
             décrivent les prévisions météorologiques.
```

Un filtre par motifs voit des nombres et des unités dans les deux textes. Une règle trop large bloque les deux. Une règle trop étroite laisse passer le procédé Atlas dès que sa formulation change.

Shieldstral évalue une autre question : le document décrit-il les paramètres protégés du procédé Atlas ? Le proxy peut alors traiter le document A comme un secret métier et laisser passer le document B.

Le gain du contrôle ajouté est là : parmi les dix documents que les motifs n'avaient pas pu trancher, le proxy dispose maintenant d'un signal lié à leur signification. Le moteur de décision peut autoriser un contenu ordinaire, demander sa transformation, désigner un modèle local ou bloquer l’envoi selon la politique de l’entreprise.

```text
avant : forme reconnue ou absence de décision
après : sens évalué par rapport à une règle métier
```

## Le résultat tient sur un jeu étendu à quatorze documents

La première campagne contenait 11 documents : six sensibles et cinq autorisés. Après le blocage déterministe de la clé d'API, Shieldstral avait évalué les dix documents restants.

Le jeu comprend désormais trois cas sensibles supplémentaires, conçus pour exercer la bande intermédiaire où le proxy tente une transformation plutôt qu'un blocage. Sur cette exécution étendue, la chaîne complète a signalé les neuf documents sensibles sur neuf et correctement autorisé les cinq documents non sensibles. Le rappel reste donc de 100 %, avec 0 % de faux positifs observés sur ce petit jeu. La latence de décision atteint 44 ms au 95e percentile.

```text
9 documents sensibles     → 9 signalés
5 documents non sensibles → 5 autorisés
14 cas                    → latence p95 : 44 ms
1 cas                     → Shieldstral non appelé
```

Ces chiffres décrivent les décisions de la chaîne complète, qui comprend le filtre déterministe ; ils ne sont pas un rappel de Shieldstral seul. Ils montrent le gain recherché : les contenus sensibles que les motifs ne reconnaissent pas peuvent désormais déclencher une décision de sécurité. Ils ne démontrent pas encore une qualification de production : quatorze cas restent un jeu exploratoire.

Une équipe juridique peut poser une question sur certaines clauses contractuelles. Une équipe de recherche peut protéger des résultats avant publication. Une autre politique peut dépendre de la destination : le document complet est autorisé vers un modèle local, mais interdit vers une API externe.

## Le contrôle reste du côté de l’entreprise

Shieldstral compte 3 milliards de paramètres selon le papier publié par Mistral. Cette taille permet d’envisager une exécution locale beaucoup plus facilement qu’avec un grand modèle frontière généraliste.

Le positionnement est essentiel :

```text
application de Nora
        ↓
proxy IA d’entreprise
        ↓
contrôles déterministes
        ↓
Shieldstral local + politique métier
        ↓
destination autorisée
```

Le document est évalué avant de quitter l’infrastructure. Le fournisseur externe n’est pas chargé de décider après réception si les données auraient dû lui être transmises. Le proxy de l’entreprise conserve la maîtrise de la question, du seuil et de la destination.

Le benchmark publié par Mistral contient une catégorie `Trade Secrets`. Shieldstral y obtient un score F1 de 92,1 % dans l’évaluation fine présentée par ses auteurs. Les secrets commerciaux font donc partie des risques pour lesquels le modèle a été explicitement évalué.

## Les règles déterministes ne disparaissent pas

Shieldstral ne remplace pas Presidio, les expressions régulières ou les étiquettes de classification. Un IBAN conserve une forme plus simple et plus fiable à détecter avec un outil spécialisé. Une destination structurellement interdite n’a pas besoin d’un score probabiliste.

Le proxy obtient deux regards complémentaires :

```text
motif connu : fait localisable
politique Shieldstral : relation sémantique
moteur de décision : action autorisée
```

Les contrôles déterministes interviennent d’abord. Shieldstral est appelé lorsque la forme ne suffit plus à appliquer la politique métier. Le moteur de décision transforme ensuite son score en autorisation, blocage ou demande de traitement différent.

Cette répartition évite de confier toute la sécurité à un modèle probabiliste. Elle limite également le coût et la latence en réservant l’analyse sémantique aux contenus et aux politiques qui en ont besoin.

## Détecter n’est pas pseudonymiser

Cette capacité fournit un signal de détection probabiliste ; elle ne résout pas toute la chaîne de traitement. Shieldstral peut conclure qu’un document contient un savoir-faire protégé, mais il ne fournit pas nécessairement la position exacte de chaque passage sensible dans le texte.

Cette différence est invisible dans une démonstration binaire :

```text
Question : le document contient-il les paramètres protégés du procédé Atlas ?
Réponse : oui, avec un score transmis au moteur de décision
```

Elle devient décisive lorsque Nora souhaite continuer avec le modèle frontière. Le proxy ne peut pas remplacer proprement le secret par un pseudonyme s’il ignore quels caractères ou quelles phrases le composent.

Pseudonymiser un IBAN est simple parce que le détecteur retourne ses limites. Pseudonymiser une procédure métier demande d’abord de l’isoler sans supprimer tout le document.

Shieldstral ne devient donc ni un pseudonymiseur, ni un routeur, ni le propriétaire de la politique. Il apporte un signal sémantique local. L’architecture qui l’entoure conserve les autres responsabilités.

## Le proxy gagne un contrôle qu’il n’avait pas

Dans notre configuration initiale, le proxy reconnaissait surtout des formats et des catégories prévues à l'avance. Avec Shieldstral, il peut rapprocher le sens d'un document d'une règle écrite par l'entreprise avant tout envoi externe. Une équipe peut faire évoluer cette règle en décrivant plus précisément ce qu'elle protège, sans reconstruire un classifieur pour chaque nouveau secret métier.

Ce mécanisme reste probabiliste : une question imprécise produit une frontière imprécise, et les seuils doivent être qualifiés sur des cas représentatifs. Le dernier article montrera comment les mesurer et améliorer la politique.

Cette capacité ouvre directement l’étape suivante : pour transformer ce signal en pseudonymisation, le proxy doit découper le texte, conserver les positions et demander à Shieldstral quels segments correspondent à la politique.

Cette localisation constitue la prochaine étape de l'architecture.

---

{{< closing-question label="À retenir" >}}
Shieldstral fournit un signal sémantique local. Le moteur de décision conserve la responsabilité de l’action et de la destination.
{{< /closing-question >}}

## Sources

- [Rapport de qualification Shieldstral — 2 septembre 2026](/documents/shieldstral-qualification-2026-09-02.md)
- [Mistral AI — Shieldstral](https://arxiv.org/abs/2607.25857)
- [Microsoft — Presidio](https://microsoft.github.io/presidio/)

**Pour continuer :** [Expurger un secret sans format : le proxy protège-t-il encore la tâche ?](/articles/shieldstral-expurgation-secret-metier/).
