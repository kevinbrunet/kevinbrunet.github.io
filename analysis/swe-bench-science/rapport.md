# Complémentarité de Qwen3.8-27B sur SWE-bench Science

Analyse du 5 octobre 2026, calculée exclusivement sur les résultats binaires individuels. **DeepSeek-V4-Pro (max), sous Claude Code, récupère 23 des 84 échecs de Qwen**. Le classement porte sur les configurations dont les résultats par tâche sont publiés et vérifiables, pas sur tous les modèles du leaderboard.

## Référence exacte

- Modèle : `Qwen3.8-27B`, effort `xhigh` ; identifiant matrice `qwen-3-8-27b`.
- Harness : `Claude Code` ; identifiant de sélection/traces `qwen3-8-27b-xhigh`.
- 119 tâches `001`–`119`, 35 succès, 84 échecs, 29.41 %.
- Traces datées du 18 août 2026 à 13:00:51 UTC au 20 août 2026 à 09:06:26 UTC.
- Identifiants publiés individuels : `qwen3-8-27b-xhigh-001` … `qwen3-8-27b-xhigh-119`. Ils sont créés par l'exporteur ; les identifiants originaux des essais, versions de harness et révisions exactes des checkpoints ne sont pas exposés.

## Sources et fidélité

Le [dépôt officiel OpenMOSS](https://github.com/OpenMOSS/SWE-bench-Science/tree/08cea5a2ff7f56252de8658a75a4144c18a6c946) décrit les sorties `summary.csv`, `reward.json` et `ctrf.json`, mais son snapshot main ne publie pas les runs correspondants. Le dataset Hugging Face contient les tâches et les outils, pas cette collection de résultats de modèles.

Les résultats sont publiés dans le [dépôt du site officiel](https://github.com/swescience/swescience.github.io/tree/be2a34e53c8b201931bbc8a8d241292d3beccb03), lié depuis OpenMOSS. J'utilise ses fichiers de données et ses évaluations JSON, sans extraction des scores HTML :

- `data/task-matrix.json` : 119 × 7 résultats audités, chacun avec `reward`, tests publics/privés et indication de source.
- `public/traces/*/index.json` et les 833 `task-*.json` individuels : 7 sélections de 119 tâches. **Tous les rewards des indexes et fichiers individuels concordent avec la matrice**, sans divergence. Les fichiers individuels contiennent les résultats du vérificateur et ses logs.
- `data/hard70-model-results.json` : malgré son nom, contient des listes **exhaustives de succès sur les 119 tâches**, avec `taskCount: 119`, pour Nex N2, DeepSeek-V4-flash max et Intern-S2. Les autres IDs du périmètre sont des échecs pour ces sélections. Niveau de preuve inférieur aux traces complètes : pas de logs individuels publiés pour ces trois configurations.
- `data/benchmark.json` sert à identifier les configurations et à contrôler les comptes calculés. Aucun pourcentage n'est utilisé pour déduire les intersections.
- Scripts de construction officiels conservés dans `source/upstream-scripts/` : provenance des audits et du remappage historique `120 → 001`. Les IDs `002`–`119` restent inchangés.

Ce sont des **résultats sélectionnés et audités publiés**, pas une archive exhaustive de tous les rollouts originaux. Les fichiers d'audit privés et `reward.json`/`ctrf.json` originaux mentionnés par les scripts de construction ne sont pas accessibles dans ces snapshots. Les matrices et listes de succès ont des hashes SHA-256 dans le résultat ; les 833 traces ont leurs hashes dans `source-provenance.json`.

Le README officiel du site indique que les audits/reruns font autorité sur les traces pour les agrégats ; son validateur marque les métriques publiques/privées de Kimi comme remplacées. Les **rewards binaires de Kimi concordent néanmoins pour les 119 tâches**, ce qui suffit pour les intersections calculées ici.

## Classement par nombre d'échecs de Qwen récupérés

Même périmètre de 119 tâches pour chaque ligne. `Gain = Complement = |Succès(X) − Succès(Qwen)|` ; `Union = 35 + Gain`.

| Modèle / effort | Harness | Open-weight | Succès seul | Échecs Qwen récupérés | Qwen ∪ modèle | Gain |
|---|---|---|---:|---:|---:|---:|
| DeepSeek-V4-Pro (max) | Claude Code | oui | 50 | 23 | 58 | +23 |
| GLM-5.2 (max) | Codex | oui | 38 | 15 | 50 | +15 |
| Kimi-K3 (max) | Kimi Code | oui | 42 | 14 | 49 | +14 |
| Nex N2 (default) | Codex | oui | 29 | 9 | 44 | +9 |
| DeepSeek-V4-flash (max) | Claude Code | oui | 28 | 6 | 41 | +6 |
| Intern-S2-Preview-397B (max) | Claude Code | oui | 25 | 5 | 40 | +5 |
| GPT-6 Astra (max) | Codex | non | 60 | 33 | 68 | +33 |
| Claude-Opus-5 (max) | Claude Code | non | 57 | 28 | 63 | +28 |
| GPT-5.6-sol (max) | Codex | non | 48 | 21 | 56 | +21 |

GLM récupère 15 tâches et Kimi 14 : le modèle au score global inférieur est ici le meilleur complément des deux. Le recouvrement Qwen/DeepSeek comprend 27 succès communs, 8 succès propres à Qwen et 23 succès propres à DeepSeek.

## Meilleur complément open-weight

- **DeepSeek-V4-Pro (max) / Claude Code**.
- Qwen seul : 35/119 (29.41 %).
- DeepSeek seul : 50/119 (42.02 %).
- Tâches supplémentaires : **23**, soit 27.38 % des échecs de Qwen.
- Union : **58/119 (48.74 %)**.
- Gain absolu : **+23 tâches** ; **+19.33 points de pourcentage**.

IDs exacts publiés :

```text
002, 009, 010, 014, 017, 019, 020, 022, 024, 032, 051, 054, 058, 064, 079, 087, 098, 103, 104, 105, 106, 108, 118
```

DeepSeek publie les [poids de V4-Pro sous MIT](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro), avec 1,6 billion de paramètres totaux et 49 milliards actifs. C'est auto-hébergeable, mais nécessite une infrastructure très différente d'un 27B : les paramètres actifs ne représentent pas la mémoire totale des poids. Aucune performance de quantification locale n'est mesurée ici. Le nom du modèle du run n'établit pas l'identité exacte avec une révision des poids téléchargeables ; cette révision n'est pas publiée.

Autres vérifications open-weight : [GLM-5.2](https://huggingface.co/zai-org/GLM-5.2), [Kimi-K3](https://huggingface.co/moonshotai/Kimi-K3), [DeepSeek-V4-Flash](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash), [Intern-S2](https://huggingface.co/internlm/Intern-S2-Preview-397B), [Nex-N2](https://github.com/nex-agi/Nex-N2). Le label Nex N2 est conservé : le site mentionne le run historique Nex-N2-Pro, mais ne donne pas sa révision précise.

## Quatre exécutions : couverture mesurable et limites

Il n'existe qu'une sélection publiée par configuration dans ces données. Les sept indexes et la matrice représentent les **mêmes** sélections, pas deux passes. Il n'est pas possible de calculer pass 2, 3, 4, `Qwen × 4`, ni `Qwen + Qwen + DeepSeek + GLM`. Répéter quatre fois la colonne Qwen produirait une union de 35 ; ce ne serait pas une mesure de quatre rollouts.

Recherche exhaustive de toutes les combinaisons de quatre configurations disponibles, sans répétition artificielle : 35 combinaisons parmi les 7 open-weight et 210 parmi les 10 configurations totales.

| Stratégie | Couverture rétrospective | Gain sur Qwen seul |
|---|---:|---:|
| Qwen × 4 rollouts indépendants | Non calculable : trois rollouts manquants | — |
| Qwen + DeepSeek-V4-Pro + GLM-5.2 + Kimi-K3 | **65/119 (54,62 %)** | **+30 tâches ; +25,21 points** |
| DeepSeek-V4-Pro + GLM-5.2 + Kimi-K3 + Intern-S2 | 65/119 (54,62 %) | +30 tâches ; +25,21 points |
| Qwen + DeepSeek-V4-Pro + Claude-Opus-5 + GPT-6 Astra | 83/119 (69,75 %) | +48 tâches ; +40,34 points |

Les deux combinaisons open-weight à 65 sont les seuls optimums parmi les 35 combinaisons mesurables. La première est l'optimum unique sous contrainte d'inclure Qwen. La référence à 83 utilise deux modèles propriétaires et reste hors classement principal. Tous les optimums, y compris ceux sans Qwen, sont enregistrés dans `results/analysis.json`.

Ces valeurs sont une **union oracle rétrospective** : une tâche est couverte dès qu'une exécution publiée la réussit. Elles ne mesurent ni le choix automatique d'un patch correct, ni le coût constant, ni la performance attendue d'un portefeuille sur de nouvelles tâches. Le réglage du portefeuille sur ces mêmes 119 tâches introduit un biais de sélection.

## Effet harness et configurations absentes

Qwen et DeepSeek utilisent tous deux Claude Code : la comparaison du gagnant n'introduit pas de différence de *nom* de harness, sans pour autant garantir les mêmes versions, budgets et paramètres. GLM utilise Codex et Kimi utilise Kimi Code : leurs complémentarités mêlent modèle + harness + paramètres d'exécution.

Harness observés dans les résultats analysables : **Claude Code, Codex, Kimi Code**. Aucun résultat exploitable sous DSH Standard, DSH PTC, Pi, Qwen Code ou mini-SWE-agent. Pier est le runner de la distribution actuelle, pas une configuration "Pi" évaluée. La présence de profils pour mini-SWE-agent dans OpenMOSS ne constitue pas un résultat publié. Aucun même modèle n'a deux harness distincts dans le périmètre disponible.

Configurations publiées avec agrégat mais sans résultats individuels exploitables dans ces snapshots : DeepSeek-V4-flash high, Qwen3.5-397B, Qwen3.5-9B max, Qwen3.6-35B-A3B max, Agents-A1 max, BigBang-v1 max, Nex-N2-mini max. Elles sont explicitement exclues ; aucun échec n'est inventé pour combler leur absence. Mistral est absent. Le classement ne peut donc pas établir que DeepSeek-V4-Pro est le meilleur complément parmi **tous** les modèles existants, ni identifier un meilleur complément de taille comparable à Qwen27B.

## Reproduction

Voir `README.md` pour les commandes et l'import de CSV/JSON/résultats Pier. Le script conserve chaque passe séparément, refuse les doublons et périmètres incomplets, calcule les échecs, recouvrements et optimums. Sept tests de garde-fous passent ; les 833 traces individuelles ont été contrôlées. Aucune modification d'article, de shortcode ou de configuration Hugo n'est nécessaire pour cette analyse.
