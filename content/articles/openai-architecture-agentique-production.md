---
title: "OpenAI dévoile l’architecture agentique derrière les publicités de ChatGPT"
seo_title: "OpenAI : une architecture agentique en production"
slug: "openai-architecture-agentique-production"
date: 2026-11-03
description: "Un LLM orchestre, des outils conservent leurs responsabilités, les traces alimentent l’amélioration. Le système publicitaire de ChatGPT offre un cas concret d’architecture agentique."
categories: ["Intelligence artificielle", "Architecture logicielle"]
tags: ["ai-systems-harness-engineering", "ai-observability"]
collection: "ARCHITECTURE"
cover: "/images/articles/openai-architecture-agentique-production.fr.png"
draft: false
---

Un modèle interprète une conversation, appelle des outils, cherche des candidats et évalue leur pertinence. Pourtant, il ne décide pas seul du résultat. Certains candidats sont écartés par les règles métier. Un mécanisme d’enchères conserve la sélection finale. Et si le système arrive trop tard, il ne produit rien.

Cette architecture fonctionne dans ChatGPT. Elle sert à sélectionner des publicités.

Le 21 octobre 2026, OpenAI en a publié une [description technique signée Ritendra Datta et Karthik Gopalratnam](https://openai.com/index/building-chatgpt-ad-stack/). Son intérêt dépasse le domaine publicitaire : elle donne à examiner un système agentique effectivement exploité, avec ses dépendances, ses contrôles et sa boucle d’amélioration.

{{< thesis >}}
La fiabilité n’est pas nécessairement une propriété du composant. Elle peut être une propriété du système qui l’encadre.
{{< /thesis >}}

Cette publication permet de donner un contenu concret à cette idée. Elle invite aussi à préciser ce que nous entendons par un système qui apprend de son fonctionnement.

## Un orchestrateur avec des responsabilités délimitées

Le système décrit repose sur un LLM spécialisé qui interprète le contexte conversationnel et appelle des outils de recherche, de filtrage et d’évaluation. Il propose des candidats au mécanisme d’enchères, qui conserve le calcul du prix et la sélection finale. Des contrôles subsistent ensuite, dont un possible rejet contextuel par l’orchestrateur.

La chaîne se lit ainsi :

```text
Contexte conversationnel
          ↓
LLM orchestrateur et appels d’outils
          ↓
Requêtes → recherche sémantique
          ↓
Éligibilité → évaluation de pertinence
          ↓
Enchères → contrôles finaux
          ↓
Livraison éventuelle
```

Ce schéma résume les responsabilités. L’orchestrateur peut appeler les outils à plusieurs reprises.

**L’orchestrateur dispose d’une capacité d’interprétation, sans absorber toutes les autorités du système.**

J’y vois une règle de conception transposable. Un modèle peut comprendre qu’une demande appelle un remboursement. Le service de paiement doit encore vérifier le montant autorisé, l’état de la commande et les droits de l’appelant. La pertinence de la proposition et l’autorisation de l’exécuter sont deux questions différentes.

Cette séparation doit exister dans les interfaces et dans le code. Une consigne demandant au modèle de respecter un plafond ne remplace pas le composant qui refuse effectivement son dépassement.

Il faut toutefois examiner chaque frontière : un outil appelé par un LLM n’est pas nécessairement déterministe. Un score de pertinence peut lui-même provenir d’un modèle. La question utile devient : **quel composant possède quelle décision, avec quelle garantie ?**

## L’agent peut s’abstenir sans faire échouer le produit

OpenAI décrit un service publicitaire séparé de la génération des réponses. Sa lenteur ou son indisponibilité ne doit pas bloquer ChatGPT. L’absence de publicité est un résultat acceptable.

Ces deux choix se renforcent. Une dépendance facultative peut réellement le rester si le produit sait fonctionner sans son résultat.

Dans nos propres architectures, nous ajoutons souvent une étape agentique à un parcours existant : suggérer une action, enrichir un dossier, préparer une recommandation. Il faut alors décider si cette étape peut interrompre le service principal.

{{< callout variant="scene" label="Exemple de transposition" >}}
Un portail de support utilise un agent pour suggérer une documentation au moment où le client ouvre un incident. La recherche peut ne rien trouver, dépasser son délai ou proposer un document trop incertain.

Le ticket doit-il attendre ? Si la suggestion est facultative, le portail peut enregistrer l’incident immédiatement et renoncer à l’enrichissement pour ce parcours.
{{< /callout >}}

Cette décision demande plus qu’un timeout. Elle définit ce qui constitue le succès du produit, puis ce que l’agent peut y ajouter.

Il faut également distinguer les raisons de l’abstention. « Aucune suggestion utile » et « service indisponible » peuvent conduire au même écran, mais appellent des interventions différentes. Le premier résultat peut être correct. Le second révèle une dégradation technique.

## Observer les étapes métier pour savoir quoi améliorer

Les événements décrits par OpenAI distinguent notamment l’absence d’opportunité, l’absence de recherche, une recherche sans candidats, des rejets d’éligibilité et les interactions après livraison.

Cette granularité change la question posée aux traces. On peut chercher **où le parcours s’arrête et pour quelle raison**, au lieu de compter seulement les erreurs d’appels.

Transposons cette idée à l’agent de support. Un indicateur global « suggestion affichée » ne permet pas de distinguer plusieurs situations :

| Situation observée | Question à examiner |
|---|---|
| L’agent n’a pas lancé de recherche | A-t-il correctement reconnu le besoin ? |
| La recherche n’a rien renvoyé | Le contenu existe-t-il et est-il retrouvable ? |
| Les documents ont été rejetés | Sont-ils périmés, hors périmètre ou mal classés ? |
| Une suggestion a été préparée trop tard | Le budget de temps est-il adapté au parcours ? |
| Le client a écarté la suggestion | Était-elle utile dans ce contexte ? |

Ce tableau constitue une proposition pour notre exemple, pas une description supplémentaire du système d’OpenAI.

Chaque ligne suggère une amélioration différente. Enrichir la base documentaire ne résoudra pas nécessairement une mauvaise reconnaissance du besoin. Accélérer la recherche ne corrigera pas des documents systématiquement inadaptés.

**Une trace devient exploitable lorsqu’elle permet de départager les hypothèses sur le problème.**

Cela demande de conserver le lien entre l’étape, ses entrées pertinentes, son résultat et la version du composant concerné. Un total d’échecs sans cette attribution risque de conduire à modifier la mauvaise partie du système.

## Les traces deviennent une matière première d’amélioration

OpenAI décrit une boucle combinant événements de production, modèles évaluateurs puissants, amélioration de modèles plus petits et retours humains. La publication mentionne aussi Codex dans le développement, avec des garde-fous de livraison et des outils d’analyse des données.

```text
Exécution → événements structurés → évaluation
                                      ↓
                      Modèles évaluateurs + retours humains
                                      ↓
                         Amélioration des composants
                                      ↓
                              Exécutions suivantes
```

Ce passage m’intéresse particulièrement pour la **cristallisation** : la transformation d’une expérience en capacité durable, qu’il s’agisse d’un comportement appris, d’une procédure ou d’un contrôle.

Les traces de production peuvent servir à davantage qu’au diagnostic d’un incident. Une fois qualifiées et sélectionnées, elles peuvent aider à construire des évaluations, identifier des cas difficiles ou préparer l’amélioration d’un composant probabiliste.

Mais une trace ne porte pas automatiquement sa propre leçon. Une recommandation ignorée peut être mauvaise, arriver trop tard ou répondre à un besoin déjà résolu. Un clic prouve une interaction. Pour établir la satisfaction ou la qualité de la décision, il faut d’autres éléments.

Le retour humain apporte une autre perspective, à condition de préciser ce qu’il mesure. Une enquête, une correction explicite et un comportement observé ne répondent pas exactement à la même question.

{{< pullquote >}}
Les traces peuvent alimenter l’apprentissage. Elles ne décident pas, à elles seules, de ce qui mérite d’être appris.
{{< /pullquote >}}

## Améliorer les modèles ne démontre pas l’évolution autonome du harness

La publication décrit une boucle d’amélioration du système et de ses modèles. Elle ne démontre pas un mécanisme autonome qui modifierait puis promouvrait l’ensemble du *harness*, l’environnement logiciel qui organise les instructions, les outils et les contrôles du modèle.

Cette distinction est essentielle pour notre réflexion.

Améliorer un modèle de pertinence, changer une instruction et déplacer un contrôle d’autorisation ne présentent pas les mêmes risques. Un gain mesuré sur le premier ne valide pas les deux autres.

Pour aller vers une cristallisation plus large, je demanderais donc une chaîne de preuves explicite : quelles expériences ont motivé le changement, quel composant a été modifié, quels cas indépendants ont servi à l’évaluer et quelle décision a autorisé son activation ?

La version actuelle doit pouvoir rester préférable. Une proposition d’amélioration doit pouvoir être rejetée. Et si une modification dégrade le fonctionnement réel, il faut pouvoir revenir à l’état précédent.

Ce sont ici des exigences d’architecture que je propose, pas des mécanismes que cette publication suffirait à attester.

## Concevoir les frontières avant d’élargir l’autonomie

Mon interprétation de ce cas tient en trois décisions : délimiter ce que le modèle peut décider, prévoir les situations où le système peut s’abstenir et organiser les preuves qui guideront les améliorations.

Ces décisions donnent une forme opérationnelle à la fiabilité. Elles permettent d’exploiter la capacité d’interprétation du modèle tout en conservant des responsabilités vérifiables autour de lui.

La boucle d’amélioration ajoute une exigence : les contrôles doivent encadrer aussi les changements apportés au système. Une architecture fiable pendant l’exécution peut perdre ses garanties si son mécanisme d’évolution les contourne.

{{< closing-question label="La question d’architecture" >}}
Votre système sait produire des traces et proposer des améliorations. Quelle preuve exige-t-il avant de transformer une expérience en comportement durable ?
{{< /closing-question >}}

## Sources

- Ritendra Datta et Karthik Gopalratnam, OpenAI Engineering, [*How we built ChatGPT’s novel ad stack for user trust and relevance*](https://openai.com/index/building-chatgpt-ad-stack/), 21 octobre 2026.
