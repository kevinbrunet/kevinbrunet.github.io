---
title: "Expurger un secret sans format : le proxy protège-t-il encore la tâche ?"
slug: "shieldstral-expurgation-secret-metier"
date: 2026-11-10
description: "Le prototype localise les zones sensibles par tronçons et les recontrôle après expurgation, mais retire encore presque tout le document."
categories: ["Intelligence artificielle", "Cybersécurité", "Architecture logicielle"]
tags: ["ai-security"]
series: ["quand-le-proxy-comprend-ce-qu-il-protege"]
series_order: 4
collection: "SYSTÈMES"
cover: "/images/articles/shieldstral/04.png"
draft: false
---

{{< callout variant="scene" label="Point de départ" >}}
Shieldstral indique que le dossier de Nora contient un savoir-faire industriel. Le proxy peut maintenant aller plus loin qu'un blocage global : chercher les zones concernées, les remplacer puis évaluer si la version transformée peut être autorisée vers une destination externe. Le prototype ne démontre pas encore que cette version reste exploitable.
{{< /callout >}}

Pour un IBAN, un moteur spécialisé renvoie directement une position précise. Pour une procédure métier, le caractère sensible vient d’une combinaison de phrases. Il faut donc construire une carte du document autour du signal fourni par Shieldstral.

Cette étape transforme une détection sémantique en zone transformable. Encore faut-il vérifier que la transformation conserve assez de document pour rester utile.

## La pseudonymisation conserve un document exploitable

Un identifiant reconnaissable peut être remplacé sans retirer le reste de la phrase :

```text
Original : Envoyer le règlement à Jean sur FR76 3000 6000 0112 3456 7890 189
Externe  : Envoyer le règlement à <PERSON_1> sur <IBAN_1>
```

Le proxy conserve localement la table de correspondance. Si le modèle reprend `<PERSON_1>` ou `<IBAN_1>` dans sa réponse, la valeur peut être restaurée avant l’affichage à Nora. Certaines passerelles proposent directement ce mécanisme. LiteLLM, par exemple, expose l’option `output_parse_pii` avec son intégration Presidio.

Cette pseudonymisation est possible parce que le détecteur sait où commence et où finit chaque entité. Le modèle externe conserve assez de contexte pour réaliser la tâche sans connaître la valeur originale.

Le même principe peut être étendu à un savoir-faire industriel, à condition de travailler à l'échelle des passages plutôt qu'à celle d'un motif isolé.

## Le document est découpé en segments qui conservent leur position

Le proxy peut découper le texte en paragraphes ou en fenêtres de tokens. Chaque segment conserve ses offsets dans le document original. Shieldstral reçoit ensuite la même politique métier avec chaque morceau.

```text
document original avec positions
        ↓
segments chevauchants
        ↓
question de politique + segment
        ↓
score Shieldstral par segment
        ↓
fusion des zones sensibles
        ↓
remplacement par <SECRET_METIER_1>
```

Lorsqu’un segment dépasse le seuil, le composant de pseudonymisation connaît la zone correspondante. Il peut la remplacer par un pseudonyme avant l’appel externe.

Shieldstral pilote ainsi la pseudonymisation sémantique sans l’exécuter seul. Le classifieur produit le signal. Le découpage fournit les positions. Le proxy applique la transformation.

Le résultat associe ainsi trois fonctions distinctes : Shieldstral détecte le sens protégé, le découpage fournit les positions et le proxy applique la transformation. Aucun de ces composants n'a besoin d'assumer seul toute la tâche.

## Le POC exerce désormais toute la chaîne

La première campagne comptait 11 documents. Elle validait les décisions d'autorisation, de blocage et de redirection locale, mais aucun cas ne parcourait réellement la branche de pseudonymisation sémantique.

J'ai ajouté trois documents sensibles calibrés pour atteindre la bande intermédiaire de la politique : une description partielle de fractionnement financier, un réglage Atlas inclus dans un rapport et un dossier médical reconnaissable par ses initiales et son contexte.

Sur ces trois cas, le proxy a exécuté la chaîne complète :

```text
score d'un ou plusieurs tronçons
        ↓
zone sensible localisée
        ↓
remplacement par [PASSAGE EXPURGÉ]
        ↓
recontrôle Shieldstral
        ↓
autorisation de transmission au modèle frontière
```

Le score moyen est passé de 46 % avant transformation à 3 % après recontrôle. Aucun des trois recontrôles n'a échoué. Le POC exécute la localisation, l’expurgation et le recontrôle. Il retourne une décision de destination ; il n’appelle pas le modèle frontière pour accomplir la tâche.

Il faut toutefois appeler précisément ce que démontre le prototype. Il remplace actuellement les tronçons par un marqueur de suppression ; il ne conserve pas une table permettant de restaurer un secret métier dans la réponse. C'est une expurgation sémantique qui valide le mécanisme nécessaire à une future pseudonymisation réversible.

## Le chevauchement réduit les effets des frontières artificielles

Une procédure peut être répartie sur plusieurs phrases. Le premier paragraphe nomme la machine. Le suivant donne la température. Le troisième explique que l’ordre des étapes réduit les défauts.

Si chaque phrase est évaluée isolément, aucune ne contient forcément assez de contexte pour apparaître sensible. Mais évaluer uniquement le document complet crée le problème inverse : le signal peut être dilué dans un texte majoritairement neutre.

Le POC a mesuré cet angle mort. Une phrase sensible obtenait un score de 0,42 seule, puis seulement 0,003 lorsqu'elle était entourée de texte neutre. Le localisateur évalue donc tous les tronçons avant la décision et retient le score le plus élevé. Les segments se chevauchent afin que la fin d’une fenêtre réapparaisse au début de la suivante.

Le chevauchement réduit les effets des frontières artificielles. Il ne garantit pas la détection d’un secret dont la compréhension exige plusieurs fenêtres. Cette méthode a aussi un coût : un document court tient dans un seul tronçon, mais un document long demande un appel Shieldstral par tronçon, y compris s'il est finalement autorisé.

## Le résultat doit être contrôlé une seconde fois

Après remplacement, le proxy réassemble le document et le soumet à un nouveau contrôle. Cette passe recherche un signal sensible dans le texte réassemblé. Elle ne prouve pas que toute reconstruction du secret est impossible. Dans le POC, elle ajoute de 17 à 20 ms aux trois cas concernés.

L’analyse par segment sert à localiser ; le contrôle final porte sur le texte dont l’envoi serait autorisé. Le même classifieur peut reproduire la même erreur : il faut aussi mesurer les fuites résiduelles avec une évaluation indépendante.

Le système doit également conserver les pseudonymes de manière cohérente. Si le même client apparaît cinq fois, `<CLIENT_1>` doit désigner la même entité partout. Cette stabilité permet au modèle de raisonner sur les relations sans connaître l’identité originale.

## Le mécanisme fonctionne, mais il supprime encore la tâche

L'objectif reste de transmettre une grande partie du document sans exposer le procédé protégé. Pour un résumé général, remplacer quelques passages par `<SECRET_METIER_1>` pourrait préserver assez de contexte pour obtenir un résultat utile.

{{< callout variant="alert" label="La limite mesurée" >}}
Le résultat actuel n'atteint pas encore cet objectif. Sur les trois nouveaux documents, le localisateur a supprimé entre 99 et 100 % du texte. Les trois recontrôles sont passés, mais essentiellement parce qu'il ne restait presque plus rien à évaluer. Le rapport les classe donc tous comme des expurgations possiblement excessives.
{{< /callout >}}

Cette limite vient en partie du jeu : les documents sont courts et le localisateur travaille à la granularité du tronçon, pas du passage exact à l'intérieur. Les trois versions expurgées passent le recontrôle du prototype. Ce résultat ne démontre ni l’absence de toute fuite résiduelle, ni l’utilité du document, ni son envoi réel à un modèle de destination. Pour mesurer cette dernière, il faudra ajouter des documents longs avec les positions sensibles attendues et vérifier que le contexte non sensible reste réellement exploitable.

La détection reste utile même lorsque l'expurgation automatique est trop large. Le proxy peut signaler à Nora la nature et la zone du problème, puis lui rendre la main pour qu'elle reformule elle-même le document. Elle connaît souvent mieux que le système les informations qui peuvent être retirées sans dénaturer sa demande. La nouvelle version repasse ensuite par Shieldstral avant tout envoi vers le modèle frontière.

Ce trajet transforme donc déjà le signal sémantique en aide à la décision, sans laisser le proxy réécrire silencieusement le contenu. Il reste à le tester dans le POC et à définir le niveau de détail que l'explication peut fournir sans révéler davantage le secret.

Une limite subsiste : le passage retiré peut être indispensable à la tâche. Si Nora demande de comparer les paramètres de deux procédures, le modèle frontière ne peut pas produire une analyse complète à partir de `<SECRET_METIER_1>`. Restaurer le passage dans la réponse ne réparera pas un raisonnement effectué sans lui.

Dans ce cas, le modèle local devient une meilleure solution que la pseudonymisation. Dans d’autres cas, le passage est accessoire et la version transformée suffit.

Le proxy ne connaît pas toujours l’intention de Nora assez précisément pour choisir entre ces deux traitements. Décider seul reviendrait à modifier silencieusement sa tâche.

L'avancée est néanmoins concrète : le proxy sait désormais détecter, localiser par tronçon, expurger puis recontrôler un secret qui n'a ni préfixe, ni format fixe, ni expression régulière évidente. La prochaine amélioration n'est plus de construire la chaîne, mais de rendre sa localisation assez fine pour préserver la tâche. En attendant, lorsque la transformation retire trop de contexte, l'utilisateur doit pouvoir choisir entre traiter localement ou annuler.

Le prochain article montre comment le proxy peut poser cette question dans l'interface existante en répondant lui-même, sans appeler le modèle demandé.

---

{{< closing-question label="À retenir" >}}
Détecter, localiser et transformer sont trois responsabilités distinctes. Une expurgation réussie au recontrôle doit encore préserver un travail utile.
{{< /closing-question >}}

## Sources

- [Rapport de qualification Shieldstral — 2 septembre 2026](/documents/shieldstral-qualification-2026-09-02.md)
- [LiteLLM — Types de l’intégration Presidio](https://github.com/BerriAI/litellm/blob/litellm_internal_staging/litellm/types/guardrails.py)
- [Mistral AI — Shieldstral](https://arxiv.org/abs/2607.25857)

**Pour continuer :** [Le proxy peut répondre sans appeler le modèle](/articles/proxy-ia-reponse-synthetique-choix-utilisateur/).
