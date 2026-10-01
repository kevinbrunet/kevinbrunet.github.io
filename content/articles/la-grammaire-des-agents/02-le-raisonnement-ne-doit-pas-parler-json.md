---
title: "Le raisonnement ne doit pas parler JSON"
slug: "le-raisonnement-ne-doit-pas-parler-json"
date: 2026-11-05
description: "Laisser le raisonnement libre et contraindre uniquement le message que le logiciel doit consommer."
categories: ["Intelligence artificielle", "Architecture logicielle"]
series: ["la-grammaire-des-agents"]
series_order: 2
collection: "ARCHITECTURE"
cover: "/images/articles/la-grammaire-des-agents/02-le-raisonnement-ne-doit-pas-parler-json.fr.png"
draft: false
---

Dans l'article précédent, nous avons vu qu'une grammaire pouvait retirer les tokens interdits de la sortie d'un modèle. Lorsqu'un champ attend un entier, les continuations incompatibles reçoivent une probabilité effective de zéro.

Mais quelle sortie voulons-nous contraindre ?

La réponse dépend de l'architecture. Le modèle peut remettre directement la requête SQL. Il peut appeler un tool qui l'exécutera sur la base. Il peut aussi fonctionner sur une API qui ne propose pas le type d'appel structuré dont nous avons besoin.

Ces trois cas ne placent pas la grammaire au même endroit.

## Premier cas : le modèle fournit directement le résultat

Pour retrouver Camille Martin, l'agent de Maya peut produire lui-même une requête SQL. Avant de répondre, il doit examiner le schéma, relier les clients à leurs adresses et distinguer les homonymes.

Son raisonnement peut commencer ainsi : « Je dois filtrer le nom, puis utiliser la ville portée par l'adresse. » La réponse attendue, elle, doit commencer par `SELECT` et respecter la grammaire SQL autorisée.

```text
raisonnement libre
      ↓
fin du raisonnement
      ↓
requête SQL contrainte
```

Il ne faut pas l'activer dès le premier token. Le décodeur attendrait immédiatement `SELECT` et empêcherait le modèle d'analyser le problème.

Les modèles de raisonnement rendent cette frontière visible. La [documentation de Qwen](https://github.com/QwenLM/Qwen3/blob/main/docs/source/getting_started/concepts.md) décrit par exemple les balises `<think>` et `</think>`. L'[API Qwen](https://docs.qwencloud.com/developer-guides/text-generation/thinking) expose séparément `reasoning_content` et `content`.

Un moteur peut utiliser cette séparation pour laisser le premier canal libre et contraindre le second. [vLLM](https://docs.vllm.ai/en/latest/features/structured_outputs/) documente l'association d'un parseur de raisonnement et de structured outputs.

[XGrammar-2](https://arxiv.org/abs/2601.04426) traite aussi le changement de structure pendant une génération. Son mécanisme `TagDispatch` permet de sélectionner une structure à partir d'une balise. Cela fournit une brique pour alterner texte libre et régions contraintes ; l'application doit encore définir la frontière correspondant au protocole du modèle.

## Deuxième cas : le modèle appelle un tool

L'application peut aussi exposer un tool `execute_query`. Le modèle construit la même requête SQL, mais au lieu de la remettre comme réponse finale, il la place dans les arguments de l'appel :

```json
{
  "name": "execute_query",
  "arguments": {
    "sql": "SELECT ... FROM customers ..."
  }
}
```

Le nom doit correspondre à un tool disponible et les arguments doivent respecter son JSON Schema. Le serveur exécute la requête, puis renvoie les lignes obtenues au modèle.

La contrainte porte ici sur le tool call. Son périmètre exact dépend du modèle et du serveur utilisés. Certains contraignent seulement la structure JSON des arguments. D'autres acceptent des expressions régulières ou des grammaires plus précises. Chaque fournisseur possède ses limites, que nous examinerons dans l'article 6.

Une sortie conforme ne garantit évidemment pas que l'action est légitime. La requête peut viser une table inexistante, demander une donnée interdite ou dépasser les droits de Maya. Le serveur doit encore valider la requête avant son exécution.

Après l'exécution, la réponse principale reste libre. L'agent peut expliquer normalement à Maya quels dossiers correspondent à Camille Martin.

```text
raisonnement libre
      ↓
tool call contraint
      ↓
exécution par l'application
      ↓
réponse principale libre
```

Cette distinction est importante avec les modèles frontières. Le fournisseur peut garantir la structure de l'appel d'outil sans imposer le même format à la réponse destinée à l'utilisateur. L'article 6 reviendra sur les modes stricts et les grammaires qu'exposent leurs API.

## Troisième cas : le tool call nécessaire n'est pas disponible

Certains modèles ou certaines API ne proposent pas de tool calling. D'autres savent appeler des tools, mais ne permettent pas de combiner correctement le raisonnement choisi avec la contrainte attendue.

On peut alors séparer le travail en deux appels.

Le premier laisse le modèle analyser la demande et préparer la requête. Le second reçoit cette analyse, fonctionne sans raisonnement explicite et génère uniquement le SQL contraint.

```text
appel 1 : raisonnement libre
              ↓
         plan intermédiaire
              ↓
appel 2 : génération contrainte
              ↓
       SQL ou JSON valide
```

C'est une solution de repli. Elle ajoute une génération, de la latence et un artefact intermédiaire à transmettre. Elle reste utile lorsque l'API ne fournit pas de frontière exploitable entre le raisonnement, l'appel structuré et la réponse principale.

Certains modèles qui exposent leur raisonnement dans une zone dédiée permettent de désactiver ce fonctionnement. Qwen propose par exemple le paramètre `enable_thinking`. Pour une tâche simple, le modèle peut alors produire directement la sortie contrainte, sans canal de raisonnement à séparer.

## Contraindre le bon message

La règle n'est donc pas « appliquer la grammaire à toute la réponse du modèle ». Il faut identifier le message que le logiciel doit consommer.

Si le modèle remet directement du SQL, la grammaire protège le SQL final. S'il agit par un tool, elle protège le nom et les arguments de l'appel. Si cette interface n'existe pas, deux appels peuvent reconstruire la frontière au prix d'un surcoût.

Dans notre cas, nous savons désormais laisser l'agent raisonner librement puis contraindre sa requête SQL. Une limite subsiste : la grammaire connaît SQL en général, mais elle ignore encore les tables et les colonnes réellement présentes dans la base du support.

Le prochain article part de cette limite.

---

## Sources

- [Qwen, Qwen3 concepts, séparation du thinking par balises dédiées](https://github.com/QwenLM/Qwen3/blob/main/docs/source/getting_started/concepts.md)
- [Qwen, Thinking, séparation de `reasoning_content` et `content`, modes hybride et thinking-only](https://docs.qwencloud.com/developer-guides/text-generation/thinking)
- [vLLM, Structured Outputs, association des sorties structurées et des modèles de raisonnement](https://docs.vllm.ai/en/latest/features/structured_outputs/)
- [Li et al., XGrammar-2: Dynamic and Efficient Structured Generation Engine for Agentic LLMs (2026), changement de structure par `TagDispatch`](https://arxiv.org/abs/2601.04426)
