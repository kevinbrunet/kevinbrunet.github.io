---
title: "Deux agents. Le même angle mort."
slug: "juge-et-partie-agents"
date: 2026-09-15
description: "Faire relire un agent par une copie du même système multiplie les avis sans nécessairement réduire leurs angles morts communs."
categories: ["Intelligence artificielle", "Ingénierie logicielle"]
series: ["aucun-harnais-n-est-parfait"]
series_order: 3
collection: "ARCHITECTURE"
cover: "/images/articles/03-juge-et-partie.fr.png"
draft: false
---

Demander à un agent de relire sa propre production donne un regard neuf. Cela ne donne pas un autre regard.

La nuance parait sémantique. Elle décide pourtant de la solidité de nombreuses architectures multi-agents.

Le scénario est devenu courant. Un premier agent produit une réponse ou une modification de code. Un second reçoit le rôle de reviewer. Il doit chercher les erreurs, critiquer les choix et proposer des corrections. Sur le diagramme, deux agents se font face. On en déduit facilement que deux points de vue ont été mobilisés.

Ce n'est pas nécessairement le cas.

## Un rôle différent ne crée pas un autre cerveau

Si les deux agents utilisent le même modèle, ils partagent l'essentiel : données d'entrainement, représentations, réflexes de raisonnement et catégories d'erreurs.

Le prompt de revue apporte une différence réelle. Il change l'objectif immédiat et attire l'attention sur certains défauts. C'est comparable au fait de reprendre son propre dossier après quelques semaines. On remarque des maladresses auxquelles on était devenu aveugle. On vérifie des détails que l'élan de la rédaction avait masqués.

Mais on revient aussi avec les mêmes convictions profondes. Le contresens produit parce que l'on comprend le problème d'une certaine manière reste difficile à voir, puisqu'on relit toujours depuis cette même compréhension.

Un rôle neuf améliore l'attention. Il ne garantit pas l'indépendance.

## Ce que dit l'auto-correction sans signal externe

La recherche sur l'auto-correction intrinsèque des grands modèles apporte un résultat moins confortable que les démonstrations habituelles. Dans leur étude présentée à l'ICLR 2024, [Huang et ses coauteurs](https://arxiv.org/abs/2310.01798) montrent que demander à un modèle de corriger son raisonnement sans lui apporter de retour extérieur n'améliore pas systématiquement le résultat et peut le dégrader.

Le mot important est "extérieur".

Un test qui échoue apporte une information nouvelle. Une erreur d'exécution apporte une information nouvelle. Un exemple métier qui contredit le résultat apporte une information nouvelle. Une simple consigne du type "vérifie encore" demande au modèle de rééchantillonner ce qu'il sait déjà.

Il peut trouver une erreur d'inattention. Il ne reçoit aucun moyen supplémentaire de reconnaitre comme faux ce qu'il considère déjà comme juste.

## La boucle élimine d'abord les erreurs faciles à voir

Cela ne signifie pas que les boucles de critique sont inutiles. Elles peuvent corriger beaucoup de défauts au début : oublis, incohérences locales, imports manquants, cas simples ou contradictions visibles.

Le rendement décroit ensuite.

Chaque tour supplémentaire explore la même distribution avec une variation de formulation et d'attention. Les premières passes retirent les erreurs que le modèle sait reconnaitre. À mesure que la production se stabilise, il reste davantage d'erreurs liées à ses angles morts. La boucle commence alors à polir une solution plutôt qu'à l'enrichir.

Le signe de ce plateau n'est pas un nombre universel de tours. Il dépend du modèle, de la tâche et des contrôles disponibles. On peut néanmoins l'observer : les corrections deviennent mineures, les verdicts convergent et aucun fait nouveau n'entre dans le système.

À ce stade, demander une onzième relecture achète surtout de la confiance.

## Le reviewer doit apporter une différence vérifiable

Avant d'ajouter un agent de revue, il faut donc demander ce qu'il ajoute.

Apporte-t-il un autre modèle ? Une spécification qu'il est seul à voir ? Des tests hors de portée du producteur ? Un jeu de données indépendant ? Un outil déterministe ? Une expertise ou une consigne construite par une autre équipe ?

Si la réponse est non, le reviewer peut rester utile comme contrôle de cohérence. Il ne faut simplement pas le présenter comme une source indépendante de vérité.

Cette distinction permet aussi d'éviter la multiplication décorative des agents. Un agent "sécurité", un agent "architecture" et un agent "qualité" ne constituent pas trois lignes de défense si tous appliquent les mêmes connaissances avec les mêmes accès sur la même production. Ils constituent trois focales d'un même dispositif.

Ce n'est pas rien. Ce n'est pas trois cerveaux.

## Chercher un signal, pas une approbation

Le meilleur usage d'une seconde revue n'est pas toujours d'obtenir un verdict final. Il peut être de produire un désaccord.

Si deux évaluateurs réellement différents aboutissent séparément à des conclusions incompatibles, nous ne savons pas encore lequel a raison. Nous savons en revanche où concentrer la revue humaine. Le désaccord devient un détecteur de zones fragiles.

Cette idée inverse le réflexe habituel. On ne demande plus au deuxième agent de rassurer le premier en signant sa copie. On lui demande de révéler les endroits où une confiance unique serait dangereuse.

Un agent peut donc relire sa production. Il faut simplement savoir ce que cette relecture prouve : une meilleure cohérence interne, parfois une correction utile, jamais à elle seule l'absence d'angle mort.

Dans le prochain article, la boucle rencontre un autre problème. Dès qu'on lui donne une mesure claire à optimiser, l'agent peut réussir le contrôle sans réussir la mission.

---

## Sources

- Huang et al., *Large Language Models Cannot Self-Correct Reasoning Yet*, ICLR 2024 · https://arxiv.org/abs/2310.01798
- Kamoi et al., *When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-Correction of LLMs*, TACL 2024 · https://aclanthology.org/2024.tacl-1.78/
- Tyen et al., *LLMs Cannot Find Reasoning Errors, but Can Correct Them Given the Error Location*, Findings of ACL 2024 · https://aclanthology.org/2024.findings-acl.826/
- Zhu et al., *Demystifying Multi-Agent Debate: The Role of Confidence and Diversity*, Findings of ACL 2026 · https://aclanthology.org/2026.findings-acl.1694/
