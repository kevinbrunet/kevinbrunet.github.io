---
title: "Comment contraindre un modèle frontière"
slug: "les-modeles-frontieres-contraignent-les-tools"
date: 2026-11-05
description: "Comparer sorties structurées, tools stricts et grammaires personnalisées dans les API des modèles frontières."
categories: ["Intelligence artificielle", "Architecture logicielle"]
tags: ["ai-systems-harness-engineering", "ai-reliability"]
series: ["la-grammaire-des-agents"]
series_order: 6
collection: "ARCHITECTURE"
cover: "/images/articles/la-grammaire-des-agents/06-les-modeles-frontieres-contraignent-les-tools.fr.png"
draft: false
---

Maya demande à l'agent du support de retrouver Camille Martin dans le secteur correspondant au code postal `69003`. L'application possède déjà une opération stable pour ce besoin : rechercher des clients par nom et par code postal.

Jusqu'ici, nous avons construit une grammaire dynamique autour du SQL, puis envisagé les samplers comme une chaîne de middlewares. Une objection arrive vite : en entreprise, beaucoup d'agents utilisent un modèle frontière par API. L'équipe n'a accès ni aux logits ni au sampler. Elle ne peut donc pas personnaliser cette chaîne token par token.

Elle n'en a pas forcément besoin. Mais les trois architectures vues dans l'article 2 ne sont pas supportées de la même façon.

## Premier mode : contraindre directement la réponse

Le modèle peut produire une réponse structurée conforme à un JSON Schema. Pour rechercher Camille Martin, on peut lui demander ce résultat :

```json
{
  "operation": "search_customers",
  "name": "Camille Martin",
  "postalCode": "69003",
  "maxResults": 5
}
```

[OpenAI](https://developers.openai.com/api/docs/guides/structured-outputs), [Anthropic](https://platform.claude.com/docs/en/build-with-claude/structured-outputs), [Gemini](https://ai.google.dev/gemini-api/docs/generate-content/structured-output) et [Mistral](https://docs.mistral.ai/studio-api/conversations/structured-output/custom) proposent tous une forme de sortie JSON structurée. C'est suffisant lorsque le logiciel attend un objet. Cela ne permet pas forcément de contraindre directement une chaîne SQL, du Markdown ou un langage métier.

OpenAI accepte `pattern`, les formats, les bornes numériques et celles des tableaux. Anthropic garantit également ses sorties structurées et accepte des expressions régulières simples dans `pattern`, mais exclut notamment les lookarounds et les références à des groupes capturés. Gemini documente notamment `enum`, `minimum`, `maximum`, `minItems` et `maxItems`. Mistral accepte un schéma décrit en JSON Schema, Pydantic ou Zod.

Le noyau portable reste donc limité : objets, propriétés obligatoires, types simples, tableaux et `enum`. Pour rester multi-fournisseur, mieux vaut produire le petit arbre JSON ci-dessus, puis laisser un compilateur déterministe fabriquer le SQL.

## Deuxième mode : contraindre le tool call

L'application peut exposer directement `search_customers`. Le modèle choisit le tool et produit ses arguments ; sa réponse principale reste libre après l'exécution.

OpenAI et Anthropic disposent d'un mode `strict: true` pour garantir les arguments dans leur sous-ensemble de JSON Schema. [Gemini](https://ai.google.dev/gemini-api/docs/function-calling) documente aussi un mode `validated` assurant le respect du schéma de fonction. Mistral accepte des déclarations de fonctions par schéma. Il faut donc vérifier la garantie et le mode d'activation propres au modèle et à l'API utilisés.

OpenAI va plus loin : un custom tool peut recevoir une grammaire `regex` ou `lark`. On peut donc contraindre une entrée textuelle comme du SQL. La regex suit toutefois la syntaxe Rust sans lookarounds, et le dialecte Lark reste partiel. Anthropic compile lui-même le schéma en grammaire, mais ne permet pas d'envoyer la sienne. Gemini et Mistral n'exposent pas non plus de grammaire générale comparable dans leurs API documentées.

Notre regex `^[0-9]{5}$` entre ainsi dans les motifs simples documentés par OpenAI et Anthropic. Pour notre code postal, les deux peuvent contraindre le champ `postalCode` avec `pattern`. La différence apparaît lorsque nous voulons fournir une grammaire textuelle complète pour la requête SQL : OpenAI expose ce point d'entrée sur ses custom tools, tandis qu'Anthropic reçoit un JSON Schema. Dans les deux cas, le serveur doit encore vérifier que la recherche et son périmètre sont autorisés.

## Troisième mode : séparer raisonnement et formalisation

Si l'API ne sait contraindre ni le langage final ni le tool comme nécessaire, on retrouve le double appel de l'article 2.

Le modèle frontière réalise le raisonnement. Un second appel transforme son résultat en sortie structurée. Ce second appel peut utiliser un petit modèle local équipé d'un décodeur contraint.

Cette dernière solution est moins satisfaisante qu'elle n'en a l'air. Si le petit modèle choisit le tool et reformule ses arguments, il reprend une partie de la décision. Une mauvaise traduction peut dégrader un bon raisonnement du modèle frontière.

Un [benchmark de septembre 2026 sur les petits modèles](https://arxiv.org/abs/2609.23742) confirme l'importance de séparer conformité et justesse : les contraintes éliminent les erreurs de schéma dans ses tâches, mais des erreurs de contenu subsistent. Le second appel doit donc être évalué sur sa fidélité à la décision du premier modèle, en plus de la validité du JSON ou du SQL.

Le double appel ne supprime donc pas les allers-retours. Il remplace une boucle imprévisible de validation, d'erreur et de relance par deux générations prévues dès le départ. Le premier modèle raisonne librement. Le second reçoit ce raisonnement et produit directement le SQL sous contrainte.

Le prix reste élevé : une génération supplémentaire, plus de latence et un passage entre deux modèles. C'est un mode de repli lorsque le modèle frontière ne sait contraindre ni sa réponse SQL ni l'appel de tool. Ce n'est pas l'architecture à privilégier lorsqu'un des deux premiers modes est disponible.

## Une couverture encore très inégale

| Fournisseur | Réponse JSON contrainte | Tool strict | Grammaire personnalisée |
| --- | --- | --- | --- |
| OpenAI | Oui | Oui | `regex` ou `lark` sur un custom tool |
| Anthropic | Oui | Oui | Non exposée |
| Gemini | Oui | Respect du schéma en mode `validated`, selon l'API | Non exposée |
| Mistral | Oui | Schéma de fonction | Non exposée |
| Qwen via Model Studio | JSON mode ; JSON Schema strict sur les modèles compatibles | Schéma de fonction | Non exposée par l'API hébergée |
| Kimi via Moonshot | Non documentée comme stricte | Tool calling | Non exposée par l'API hébergée |

Le cas des modèles chinois ajoute une distinction importante. [Qwen via Model Studio](https://help.aliyun.com/en/model-studio/qwen-structured-output) distingue désormais deux modes. `json_object` demande du JSON valide sans garantir sa conformité à notre contrat. `json_schema` avec `strict: true` contraint la structure sur les modèles compatibles. La disponibilité dépend du modèle et du mode d'entrée ; la documentation signale notamment un repli vers `json_object` pour les entrées multimodales. Il faut vérifier le support effectif avant de compter sur cette garantie.

[Kimi K2](https://github.com/MoonshotAI/Kimi-K2) et Kimi K2.5 savent appeler des tools, mais Moonshot ne documente pas de mode strict ni de grammaire personnalisée comparable à celle d'OpenAI. Leur API hébergée n'offre donc pas nécessairement plus de contrôle que les plateformes occidentales.

Qwen et Kimi ont toutefois un autre avantage : plusieurs de leurs modèles sont disponibles avec leurs poids. En les servant avec [vLLM](https://docs.vllm.ai/en/latest/features/structured_outputs/), l'équipe choisit elle-même le moteur de structured outputs et peut appliquer un JSON Schema, une regex ou une grammaire indépendamment des limites de l'API du créateur. La capacité vient alors du serveur d'inférence autant que du modèle.

## L'intelligence du modèle reste notre principal correctif

À l'heure actuelle, beaucoup d'équipes limitent les erreurs en choisissant un modèle plus intelligent. Si cela ne suffit pas, elles valident la réponse, renvoient l'erreur au modèle et paient un nouveau tour. Dans les deux cas, la fiabilité augmente avec la facture : soit le token coûte plus cher, soit il faut en consommer davantage.

La grammaire suit la logique inverse. Elle retire les sorties interdites avant leur génération et réduit les tokens consacrés aux erreurs, aux explications et aux nouvelles tentatives. Un modèle moins coûteux peut alors suffire pour certaines étapes de formalisation.

Ce mécanisme n'est donc pas naturellement aligné avec le modèle économique d'une API facturée au token. Un fournisseur peut vendre un modèle plus puissant ou plusieurs échanges pour atteindre le résultat. Exposer une contrainte qui permet d'y parvenir du premier coup réduit précisément cette consommation.

La grammaire est donc particulièrement utile avec un modèle auto-hébergé. L'équipe contrôle le moteur d'inférence et choisit elle-même où appliquer un JSON Schema, une regex ou une grammaire complète. La capacité ne dépend plus du bon vouloir d'une API distante.

Avec un modèle frontière, l'intégration devient plus compliquée. Il faut composer avec le sous-ensemble de JSON Schema, les modes de raisonnement et les endpoints proposés par chaque fournisseur. OpenAI se distingue ici par un point d'extension précis : ses custom tools acceptent directement une regex ou une grammaire Lark, là où les autres plateformes comparées exposent surtout du JSON structuré et du function calling.

La série se termine donc sur cette limite. En auto-hébergement, les grammaires, les samplers et les logits processors peuvent former une chaîne personnalisée. Avec un modèle frontière, cette chaîne reste derrière l'API. Le développeur ne peut utiliser que les points d'extension que le fournisseur décide d'exposer.

Le modèle frontière apporte davantage de capacité de raisonnement. Il retire en échange une partie du contrôle sur la manière dont ses logits deviennent une action. C'est pourquoi la génération contrainte est aujourd'hui plus puissante en auto-hébergement, même si OpenAI réduit nettement l'écart.

---

## Sources

- [OpenAI, Function calling, function tools stricts et custom tools avec grammaire `regex` ou `lark`](https://developers.openai.com/api/docs/guides/function-calling)
- [OpenAI, Structured Outputs, propriétés JSON Schema supportées et exclusions](https://developers.openai.com/api/docs/guides/structured-outputs)
- [Anthropic, Strict tool use, compilation du `input_schema` en grammaire contrainte](https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use)
- [Anthropic, Structured outputs, réponse JSON conforme à un schéma](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
- [Anthropic, Troubleshooting tool use, support des motifs simples et limites de `pattern` dans les tools stricts](https://platform.claude.com/docs/en/agents-and-tools/tool-use/troubleshooting-tool-use)
- [Google, Structured outputs, sous-ensemble JSON Schema supporté par Gemini](https://ai.google.dev/gemini-api/docs/generate-content/structured-output)
- [Google, Function calling, mode `validated` et respect du schéma de fonction](https://ai.google.dev/gemini-api/docs/function-calling)
- [Mistral, Custom Structured Outputs, schémas Pydantic, Zod et JSON Schema](https://docs.mistral.ai/studio-api/conversations/structured-output/custom)
- [Alibaba Cloud Model Studio, Qwen Structured Output, distinction entre JSON mode et JSON Schema strict, limites de compatibilité](https://help.aliyun.com/en/model-studio/qwen-structured-output)
- [Moonshot AI, Kimi K2, tool calling et déploiement sur ses propres moteurs](https://github.com/MoonshotAI/Kimi-K2)
- [vLLM, Structured Outputs, contraintes par JSON Schema, regex et grammaire](https://docs.vllm.ai/en/latest/features/structured_outputs/)
- [Chavan, Constrained Decoding Eliminates Structural Failures in Small LLMs but Reveals a Scale-Dependent Semantic Gap (préprint, septembre 2026), conformité et justesse des petits modèles](https://arxiv.org/abs/2609.23742)
