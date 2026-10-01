---
title: "Le proxy peut répondre sans appeler le modèle"
slug: "proxy-ia-reponse-synthetique-choix-utilisateur"
date: 2026-10-01
description: "Une réponse synthétique peut expliquer une décision et proposer les chemins autorisés. Son intégration dépend du protocole du client."
categories: ["Intelligence artificielle", "Cybersécurité", "Architecture logicielle"]
series: ["quand-le-proxy-comprend-ce-qu-il-protege"]
series_order: 5
collection: "SYSTÈMES"
cover: "/images/articles/shieldstral/05.png"
draft: false
---

{{< callout variant="scene" label="Point de départ" >}}
Nora demande à Claude Code de résumer un dossier avec un modèle frontière. LiteLLM intercepte la requête et Shieldstral détecte un procédé industriel confidentiel.
{{< /callout >}}

L'entreprise peut traiter cette situation de deux façons. Elle peut conserver Claude Code et demander au proxy de répondre à la place du modèle. Elle peut aussi fournir, avec le proxy, un agent compatible avec l'Agent Client Protocol. Un client ACP peut alors afficher les explications, les options et les demandes de permission dans une interface prévue pour cela.

L'agent ACP offre l'intégration la plus riche, mais oblige Nora à utiliser un client compatible. La réponse synthétique vise une interface existante et constitue le premier chemin à intégrer puis à tester.

Le proxy pourrait se contenter de bloquer l'appel avec une erreur. Nora saurait que sa demande a échoué, mais pas comment continuer. Il peut faire mieux : ne contacter aucun fournisseur et renvoyer lui-même une réponse au format attendu par Claude Code.

> Je n'ai pas envoyé ce document au modèle demandé, car il contient un procédé confidentiel. Vous pouvez me demander de pseudonymiser les passages sensibles, d'utiliser le modèle local ou d'annuler.

Pour Nora, ce texte apparaît comme une réponse ordinaire de l'assistant. En réalité, aucun modèle généraliste ne l'a produit.

## LiteLLM sait produire une réponse sans appeler le fournisseur

LiteLLM permet d'exécuter un hook juste avant l'appel au modèle. Pour les appels de type Chat Completions, ce hook peut retourner une chaîne à la place de la requête modifiée. LiteLLM construit alors une réponse d'assistant dans le format de l'endpoint, y compris pour un flux en streaming.

LiteLLM permet aussi d'enregistrer un fournisseur personnalisé. Ce composant reçoit la requête et peut soit appeler le modèle autorisé, soit retourner directement un `ModelResponse`. La documentation montre également la transformation de cette réponse vers l'endpoint Anthropic `/v1/messages`, utilisé par Claude Code lorsqu'il passe par une passerelle.

Le mécanisme nécessaire existe donc, mais il demande du code dans ou autour de LiteLLM. Shieldstral calcule la décision ; un hook ou un fournisseur personnalisé construit la réponse de sécurité.

```text
Claude Code
    ↓
LiteLLM + contrôle Shieldstral
    ├── autorisé → appel du modèle
    └── choix requis → réponse synthétique, sans appel du modèle
```

## La question reste textuelle

Claude Code affiche cette réponse, mais il ne transforme pas automatiquement les options en boutons. Nora répond dans le message suivant :

> Utilise le modèle local.

ou :

> Pseudonymise les passages sensibles puis continue.

Le proxy doit reconnaître cette reprise. Il ne peut pas se contenter de chercher les mots « modèle local » dans le texte : un document transmis par Nora pourrait contenir la même expression.

La réponse synthétique doit donc être associée à une décision temporaire conservée côté serveur :

```text
identifiant de décision
empreinte du document
clé ou identité de Nora
modèle initialement demandé
options autorisées
date d'expiration
```

Lors du message suivant, le proxy vérifie que le choix correspond à cette décision, que le document n'a pas changé et que l'autorisation n'a pas expiré.

## Le choix ne contourne jamais la politique

Le proxy ne propose que des chemins déjà autorisés. Si le modèle frontière ne peut pas recevoir le document complet, Nora ne voit jamais l'option « envoyer quand même ».

Les choix peuvent être :

- pseudonymiser les passages localisés, puis appeler le modèle demandé ;
- utiliser un modèle local avec le document complet ;
- annuler.

Si Nora choisit la pseudonymisation, le contenu transformé est contrôlé une seconde fois avant son départ. Si elle choisit le modèle local, LiteLLM route la requête vers le déploiement autorisé. Si elle annule, aucun modèle n'est appelé.

## Cette solution ne fonctionne pas uniformément avec tous les clients

La documentation de LiteLLM établit le retour d'une réponse de rejet normale pour Chat Completions et montre comment un fournisseur personnalisé peut servir l'endpoint Anthropic `/v1/messages`. Ces mécanismes rendent l’intégration envisageable avec Claude Code. Ils ne démontrent pas à eux seuls la reprise interactive de cette série : il faut tester le client, l’endpoint, le streaming et l’état de décision ensemble.

Codex utilise désormais Responses API pour ses fournisseurs personnalisés. Le raccourci du hook qui retourne une chaîne n'est pas documenté pour cet endpoint. Pour offrir la même expérience dans Codex, il faut ajouter une couche capable de produire une réponse Responses API valide et de gérer le streaming. Il ne faut pas présenter cette compatibilité comme acquise sans la tester sur la version déployée.

Cette différence ne change pas le principe architectural : le point de contrôle peut répondre à la place du modèle. Elle impose seulement d'adapter la réponse au protocole réellement utilisé par le client.

## Un agent ACP peut offrir une intégration plus riche

L'entreprise peut également distribuer un agent ACP qui appelle LiteLLM pour le compte de l'utilisateur. Lorsque le proxy exige un choix, cet agent peut adapter la décision au mécanisme `session/request_permission`, après vérification que les options et leur portée correspondent à ce contrat. Un client ACP peut alors présenter des options structurées, recevoir la sélection de Nora et reprendre la tâche.

```text
client ACP
    ↓
agent ACP fourni avec le proxy
    ↓
LiteLLM + Shieldstral
```

Cette architecture ne transforme pas LiteLLM en proxy ACP. Elle ajoute un agent au-dessus de la passerelle. LiteLLM conserve l'application de la politique ; l'agent adapte ses décisions au protocole d'interaction du client.

Ce second chemin convient à une entreprise qui contrôle l'outil distribué à ses utilisateurs. Il demande davantage de développement, mais permet de remplacer la question textuelle par une interaction explicite. Pour les autres clients, la réponse synthétique reste une voie à intégrer et à qualifier séparément.

## Bloquer sans abandonner l'utilisateur

Une sécurité utile ne dit pas seulement non. Elle explique ce qui n'a pas été envoyé et indique les chemins encore possibles.

Ici, le proxy reste le verrou : il contrôle le contenu, décide des options et vérifie la reprise. La réponse synthétique lui permet simplement de rendre cette décision visible dans une interface qui ne possède pas de mécanisme spécialisé pour l'afficher.

Cette transparence réduit aussi l'envie de contourner l'outil officiel. Le prochain article examine précisément ce lien entre blocage opaque et shadow IT.

---

{{< closing-question label="À retenir" >}}
Le choix de l’utilisateur porte sur des chemins autorisés. Il ne peut jamais lever une interdiction de transmission.
{{< /closing-question >}}

## Sources

- [LiteLLM — Modify / Reject Incoming Requests](https://docs.litellm.ai/docs/proxy/call_hooks)
- [LiteLLM — Custom API Server](https://docs.litellm.ai/docs/providers/custom_llm_server)
- [Anthropic — Claude Code, LLM gateway](https://docs.anthropic.com/en/docs/claude-code/llm-gateway)
- [OpenAI — Codex, référence de configuration](https://developers.openai.com/codex/config-reference)
- [Agent Client Protocol — Architecture](https://agentclientprotocol.com/get-started/architecture)

**Pour continuer :** [Interdire l’IA nourrit le shadow IT](/articles/proxy-ia-shadow-it-chemin-officiel/).
