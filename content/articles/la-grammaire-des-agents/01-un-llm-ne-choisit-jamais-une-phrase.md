---
title: "Un conseil s'oublie. Une grammaire interdit."
slug: "un-llm-ne-choisit-jamais-une-phrase"
date: 2026-11-05
description: "Une grammaire retire les tokens interdits avant leur choix et évite les relances liées aux sorties invalides."
categories: ["Intelligence artificielle", "Architecture logicielle"]
tags: ["ai-systems-harness-engineering", "ai-reliability"]
series: ["la-grammaire-des-agents"]
series_order: 1
collection: "ARCHITECTURE"
cover: "/images/articles/la-grammaire-des-agents/01-un-llm-ne-choisit-jamais-une-phrase.fr.png"
draft: false
---

Maya travaille au support client. Elle demande à son nouvel agent de retrouver le dossier de Camille Martin à Lyon. L'application attend un objet JSON contenant le texte de recherche et le nombre maximal de résultats.

L'équipe contrôle cette sortie comme elle contrôle encore beaucoup d'agents : avec des conseils. Le prompt demande de répondre uniquement en JSON. Un skill précise que `maxResults` doit être un entier. Un fichier de règles interdit les propriétés supplémentaires.

Puis nous espérons que le modèle s'en souviendra au bon moment.

## Un conseil peut être ignoré

Le modèle reçoit une demande, des règles, du contexte et parfois plusieurs outils. Il doit décider ce qui compte, résoudre les contradictions et produire une réponse. La consigne est présente dans son contexte, mais elle n'est pas une barrière.

Il peut donc ajouter une phrase avant le JSON. Il peut écrire `maxResults` sous forme de texte. Il peut oublier une propriété obligatoire ou en inventer une qui semble utile.

Le comportement habituel consiste à vérifier sa réponse après coup.

Le parseur refuse le JSON. Le validateur signale que `maxResults` doit être un entier ou qu'une propriété n'existe pas. Le harnais transforme cette erreur en nouveau message : « Ta réponse est invalide pour telle raison. Recommence en respectant la consigne. »

L'agent génère une seconde réponse. Parfois une troisième.

```text
prompt + règles + skill
          ↓
       génération
          ↓
       validation
          ↓
         erreur
          ↓
   nouveau prompt avec l'erreur
          ↓
    nouvelle génération
```

Cette boucle fonctionne. Elle coûte aussi une fortune lorsqu'on la multiplie par le nombre de tâches, d'agents et d'étapes d'un workflow.

Chaque échec consomme une génération complète. Il augmente la latence. Il occupe le modèle avec une correction qui n'apporte rien au besoin métier. Il oblige enfin le système à prévoir des stratégies de relance, des limites de tentatives et des cas d'abandon.

Nous payons le modèle pour produire une erreur, puis pour comprendre l'erreur qu'il vient de produire, puis pour essayer de ne pas la reproduire.

## Empêcher plutôt que rappeler

Une grammaire intervient avant l'erreur.

Son but n'est pas de mieux expliquer la règle au modèle. Son but est de l'empêcher de prononcer un token incompatible avec la sortie attendue.

Prenons un [JSON Schema](https://json-schema.org/understanding-json-schema/reference/numeric#integer) simplifié :

```json
{
  "type": "object",
  "properties": {
    "maxResults": {
      "type": "integer"
    }
  },
  "required": ["maxResults"]
}
```

Une fois que la génération a produit :

```json
{"maxResults":
```

le moteur sait qu'il attend un entier. Le modèle calcule toujours une probabilité pour les tokens de son vocabulaire. Mais le décodeur applique un masque avant le choix final.

Les tokens qui peuvent poursuivre un entier restent disponibles. Ceux qui commenceraient une chaîne de caractères, un objet ou le mot `bonjour` reçoivent une probabilité effective de zéro.

Le modèle ne peut plus choisir parmi tout son vocabulaire. Il doit choisir parmi les suites encore compatibles avec un entier.

L'exemple est souvent résumé par « seuls les chiffres de 0 à 9 restent possibles ». Dans une implémentation réelle, le moteur doit aussi gérer le signe, les espaces autorisés, la fin du nombre et le fait qu'un token peut contenir plusieurs caractères. Le principe reste le même : toute continuation qui rendrait le document incompatible avec la grammaire est retirée avant l'échantillonnage.

## Le modèle continue de choisir

La grammaire ne décide pas que Maya veut cinq résultats.

Elle définit uniquement la forme des réponses admissibles. Parmi les nombres encore possibles, le modèle conserve ses probabilités et choisit celui qui correspond le mieux au contexte.

C'est la distinction essentielle. La grammaire ne remplace pas l'intelligence du modèle. Elle réduit l'espace dans lequel cette intelligence peut s'exprimer.

La [documentation de llama.cpp](https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md) décrit ce fonctionnement avec le format GBNF et permet aussi de convertir une partie de JSON Schema en grammaire. [vLLM](https://docs.vllm.ai/en/latest/features/structured_outputs/) propose plusieurs contraintes de sortie : un choix fermé, une expression régulière, un JSON Schema ou une grammaire.

## Ce que nous ne payons plus

Avec une grammaire adaptée, le JSON mal formé ne sort jamais. Une propriété interdite ne sort jamais. Une valeur située hors d'un choix fermé ne sort jamais.

Nous n'avons donc plus besoin de détecter ces erreurs, de les expliquer au modèle et de relancer toute la génération. Le gain ne vient pas nécessairement d'un décodage token par token plus rapide. Le calcul de la contrainte possède lui-même un coût.

Le gain vient surtout des boucles qui disparaissent.

Le validateur reste utile, mais il ne traite plus les erreurs que le décodeur pouvait rendre impossibles. Il peut se concentrer sur les contraintes que la grammaire ne sait pas exprimer : cet âge est-il crédible, cette personne existe-t-elle, cet utilisateur peut-il modifier son dossier ?

## La syntaxe n'est que le début

Un schéma statique peut garantir que `maxResults` est un entier. Mais le système connaît souvent beaucoup plus de choses.

Il connaît les tables réellement disponibles. Il connaît les méthodes accessibles dans un projet. Il connaît les commandes compatibles avec l'état du dossier de Camille. Il connaît les droits de Maya et les capacités accordées à l'agent.

Cette connaissance peut servir à fabriquer la grammaire au moment de la requête.

Le modèle ne serait plus seulement empêché de produire un JSON invalide. Il pourrait être empêché de proposer une opération qui n'existe pas dans le contexte actuel.

Avant d'aller jusque-là, il faut toutefois résoudre un problème : une grammaire destinée à la réponse finale ne doit pas empêcher le modèle de raisonner librement avant de répondre.

C'est le sujet du prochain article.

---

## Sources

- [llama.cpp, GBNF Guide, fonctionnement des grammaires, conversion JSON Schema et limites de performance](https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md)
- [vLLM, Structured Outputs, contraintes par choix, regex, JSON Schema et grammaire](https://docs.vllm.ai/en/latest/features/structured_outputs/)
- [JSON Schema, documentation du type `integer`](https://json-schema.org/understanding-json-schema/reference/numeric#integer)
