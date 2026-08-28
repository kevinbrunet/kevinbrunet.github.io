---
title: "Le modèle n'est pas l'agent"
seo_title: "Modèle, agent et harness : comprendre la différence"
slug: "modele-n-est-pas-agent"
date: 2026-09-28
description: "Le modèle n'est qu'un composant : la valeur durable d'un agent d'entreprise réside dans le harness qui l'entoure."
categories: ["Intelligence artificielle", "Architecture logicielle"]
series: ["acp-interface-manquante-des-agents"]
series_order: 2
collection: "ARCHITECTURE"
cover: "/images/articles/acp-02-interface-agents.fr.png"
draft: false
---

{{< callout variant="scene" label="Point de départ" >}}
Remplacer le modèle d'un agent ne devrait pas faire disparaitre tout ce que l'entreprise lui a appris.

Ses règles métier, ses accès, ses contrôles et ses preuves ne sont pas des propriétés du modèle. Ils appartiennent au système construit autour de lui. C'est ce système que le secteur appelle le harness.

Cette distinction change la manière d'investir dans l'IA. Si l'entreprise confond son agent avec le modèle qui l'alimente, chaque progrès du marché ressemble à une migration. Si elle possède son harness, un nouveau modèle devient un composant à évaluer.
{{< /callout >}}

## Une réponse ne révèle pas le système qui l'a produite

Imaginons deux assistants qui rédigent une réponse au même appel d'offres. Ils utilisent le même modèle et reçoivent la même question.

Le premier génère un texte depuis son contexte général. Le second commence par identifier le client et le secteur concerné. Il recherche uniquement les références commerciales encore autorisées. Il vérifie les clauses auprès de la base juridique. Il marque les affirmations qui exigent une preuve, demande une validation avant d'intégrer un document confidentiel et conserve les sources utilisées.

Le résultat du second assistant inspire davantage confiance. Pourtant, ce gain ne vient pas nécessairement d'un meilleur modèle. Il vient du harness qui organise le travail autour de lui.

Les guides publiés par les fournisseurs décrivent eux-mêmes cette composition. Le [guide OpenAI consacré à la construction d'agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/) distingue le modèle, les outils et les instructions, puis ajoute l'orchestration et les guardrails. De son côté, [Anthropic décrit](https://www.anthropic.com/engineering/building-effective-agents) le bloc élémentaire d'un système agentique comme un LLM augmenté par la recherche, les outils et la mémoire. J'examine plus en détail ce qui rend ce système fiable, mais aussi ses limites, dans ma série [« Aucun harnais n'est parfait »](https://kevinbrunet.github.io/series/aucun-harnais-n-est-parfait/).

Le modèle raisonne. Le système décide avec quoi, dans quelles limites et pour produire quelles preuves.

## Le harness contient la connaissance exécutable de l'entreprise

Dans notre exemple, le harness ne se résume pas à un prompt soigneusement écrit. Il assemble plusieurs composants.

Les instructions traduisent la méthode de réponse aux appels d'offres. Les outils donnent accès au CRM, au catalogue de références, à la base documentaire et au workflow de validation. Les règles d'autorisation déterminent qui peut consulter ou transmettre chaque information. Les contrôles vérifient la présence des sources, le respect du plan et les affirmations sensibles. Les traces permettent enfin de comprendre quel document et quelle décision ont produit chaque partie du résultat.

Cette architecture transforme une compétence diffuse en capacité réutilisable. Le savoir du juriste ne reste plus seulement dans ses corrections. La méthode du commercial ne dépend plus uniquement de sa mémoire. Les règles de sécurité ne sont plus rappelées à la fin du processus. Elles participent à son exécution.

Le modèle demeure essentiel, car il interprète la demande, relie les éléments et produit le texte. Mais il travaille à l'intérieur d'un environnement préparé par l'entreprise.

{{< zoomable-figure src="/images/articles/schema-harness-acp-modele-mcp.png" alt="Schéma d'architecture : l'interface utilisateur communique par ACP avec le harness, qui regroupe les instructions, le contexte, les outils, les permissions, les contrôles et les traces. Le harness échange séparément avec le modèle et, par MCP, avec les systèmes et les données d'entreprise." action="Agrandir" label="Voir l'architecture séparant l'interface, le harness, le modèle et les systèmes d'entreprise en grand" size="compact" >}}
Le harness concentre les règles et les moyens d'action, tout en gardant des connexions distinctes avec l'interface, le modèle et les systèmes d'entreprise.
{{< /zoomable-figure >}}

Ce schéma représente un choix d'architecture, pas une organisation imposée par ACP ou MCP. Il isole dans le harness les règles, les outils, les contrôles et les traces que l'entreprise veut conserver lorsqu'elle change d'interface ou de modèle.

## Le modèle peut alors devenir une décision locale

Toutes les étapes d'un appel d'offres ne demandent pas les mêmes capacités. Extraire les dates et les montants d'un document peut être confié à un modèle rapide et économique. Comparer une clause inhabituelle aux politiques de l'entreprise peut justifier un modèle plus puissant. Un document très sensible peut être orienté vers un modèle exécuté dans un environnement contrôlé.

Le [guide OpenAI](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/) recommande d'ailleurs d'établir une référence avec un modèle capable, puis de tester des modèles plus petits afin d'optimiser le coût et la latence lorsque leur qualité reste suffisante.

Dans une architecture où le harness est séparé, cette décision peut être prise tâche par tâche. L'entreprise ne remplace pas son agent chaque fois qu'elle change un modèle. Elle conserve son processus, ses outils et ses garanties, puis choisit le moteur adapté à l'étape.

La même séparation permet de tester une nouvelle génération de modèles sans déplacer immédiatement tous les utilisateurs. Un échantillon de dossiers peut être rejoué. Les résultats peuvent être comparés sur les critères du métier. Le nouveau modèle est promu seulement s'il respecte les seuils attendus.

## Ce que l'entreprise accumule vraiment

Au fil du temps, le modèle initial peut disparaitre du marché. Les règles de réponse, les connecteurs, les jeux d'évaluation, les décisions d'autorisation et les traces restent utiles.

C'est là que se trouve l'effet cumulatif. Chaque correction d'un expert peut améliorer une instruction ou un test. Chaque incident peut ajouter un contrôle. Chaque nouveau système peut enrichir les outils disponibles. Le harness accumule ainsi une connaissance exécutable de l'entreprise, sans que le modèle ait besoin d'être entrainé sur ses données.

Cette propriété prépare aussi l'ouverture apportée par ACP. Si le harness possède son propre contrat avec l'interface, il peut être appelé depuis plusieurs clients. S'il possède également ses connexions aux outils, il peut faire évoluer son modèle sans reconstruire le reste du système.

## Remplaçable ne veut pas dire identique

Changer de modèle demandera toujours des évaluations. Deux modèles peuvent interpréter différemment une instruction, choisir d'autres outils ou produire des réponses de qualité inégale. Certains fournissent aussi des fonctions propriétaires que le harness peut décider d'utiliser.

{{< callout variant="alert" label="Distinction essentielle" >}}
L'objectif n'est pas de rendre les modèles indistinguables. Il consiste à rendre leur différence mesurable et leur remplacement possible, au lieu de laisser toute la capacité métier fusionner silencieusement avec l'un d'eux.
{{< /callout >}}

{{< pullquote >}}
Le modèle apporte une intelligence disponible sur le marché. Le harness transforme cette intelligence en manière de travailler propre à l'entreprise.
{{< /pullquote >}}

{{< closing-question label="La question suivante" >}}
Même avec un harness séparé du modèle, un agent reste captif si une seule application sait comprendre ses plans, ses permissions et ses sessions.
{{< /closing-question >}}

---

## Sources

- OpenAI, [*A practical guide to building agents*](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/), composition d'un agent autour du modèle, des outils et des instructions
- Anthropic, [*Building Effective AI Agents*](https://www.anthropic.com/engineering/building-effective-agents), modèle augmenté par la recherche, les outils et la mémoire
