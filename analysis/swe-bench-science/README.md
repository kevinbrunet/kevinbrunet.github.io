# Analyse reproductible de SWE-bench Science

Résultat : **DeepSeek-V4-Pro max / Claude Code récupère 23 échecs de Qwen3.8-27B xhigh / Claude Code**. Union : **58/119**. Meilleure union de quatre configurations open-weight publiées incluant Qwen : **65/119**, avec DeepSeek-V4-Pro, GLM-5.2 et Kimi-K3.

Lire [rapport.md](rapport.md) pour les résultats, IDs exacts, provenance et limites. La référence homogène Qwen × 4 est **non calculable** : une seule sélection de résultats de Qwen est publiée.

## Recalcul hors réseau

Depuis la racine de ce dépôt, avec Python 3.10 ou supérieur ; aucune dépendance pandas requise :

```powershell
python scripts/analyze-swe-science.py --official-dir analysis/swe-bench-science/source
python scripts/test-analyze-swe-science.py
```

Les entrées publiées sont conservées telles quelles dans `source/`. Les classifications open-weight, avec sources, sont explicites dans `model-classifications.json`. Le statut inconnu ne peut pas gagner le classement principal.

Sorties dans `results/` :

- `task-model-matrix.csv` : 119 tâches × 10 configurations, rewards binaires.
- `complementarity.csv` : classement par nombre d'échecs de la référence récupérés.
- `reference-failures.csv` : les 84 échecs de Qwen.
- `recovered-tasks.csv` : toutes les tâches récupérées, par complément.
- `analysis.json` : métriques, métadonnées, passes disponibles, combinaisons optimales, configurations exclues et hashes SHA-256 des entrées.

Un CSV avec les IDs comme `001` doit être importé comme texte dans les tableurs ; le script conserve les zéros initiaux. Le remappage historique `120 → 001` est **déjà appliqué** aux données officielles conservées. Ne pas l'appliquer une seconde fois.

## Recontrôler les 833 traces individuelles originales

Le dépôt principal OpenMOSS n'héberge pas les runs publiés. Le dépôt du site officiel, lié depuis OpenMOSS, publie leur matrice et leurs évaluations JSON. Les clones téléchargés pour cette analyse sont dans `.analysis-cache/`, exclu de Git. Les trajectoires complètes occupent beaucoup plus d'espace que les données nécessaires au calcul.

Pour recréer ce cache depuis les révisions vérifiées :

```powershell
git clone https://github.com/swescience/swescience.github.io.git .analysis-cache/swescience
git -C .analysis-cache/swescience checkout --detach be2a34e53c8b201931bbc8a8d241292d3beccb03
python scripts/analyze-swe-science.py --official-dir analysis/swe-bench-science/source --traces-root .analysis-cache/swescience/public/traces
```

Si le clone existe, utiliser uniquement la commande d'analyse. Les hashes des 833 fichiers individuels vérifiés lors de cette livraison se trouvent dans `source-provenance.json`. Le contrôle compare les IDs, modèles/harness et rewards de chaque fichier à son index puis à la matrice ; les pourcentages ne sont qu'un contrôle de cohérence.

Les noms publiés de runs sont parfois des identifiants synthétiques de l'exporteur. La sélection d'audit, le checkpoint exact, les versions de harness et tous les essais non sélectionnés ne sont pas entièrement publiés. Ne pas interpréter les données comme un échantillon exhaustif de rollouts indépendants.

## Réutiliser sur un autre modèle/harness

```powershell
python scripts/analyze-swe-science.py --official-dir analysis/swe-bench-science/source --reference glm --output tmp/science-glm
```

Les noms `qwen_recovered` et `reference-failures.csv` désignent les échecs de la **référence choisie** ; les calculs sont génériques. Un passage de référence supplémentaire ou un autre harness est une colonne distincte.

## Ajouter de vrais rollouts bruts

Créer un manifeste JSON explicite. Tous les chemins sont relatifs à son dossier. Chaque entrée correspond à **une seule passe complète** ; ne pas mettre plusieurs trials d'une tâche dans une seule entrée.

```json
{
  "runs": [
    {
      "run_id": "qwen-cc-pass2",
      "model": "Qwen3.8-27B",
      "harness": "Claude Code",
      "effort": "xhigh",
      "pass": 2,
      "open_weight": true,
      "format": "csv",
      "path": "qwen-cc-pass2/summary.csv"
    },
    {
      "run_id": "qwen-pi-pass1",
      "model": "Qwen3.8-27B",
      "harness": "Pi",
      "effort": "xhigh",
      "pass": 1,
      "open_weight": true,
      "format": "pier",
      "path": "jobs/qwen-pi-pass1"
    }
  ]
}
```

Cet exemple décrit des futurs imports, **pas des runs présents dans les données**.

Formats :

- `csv` : colonnes `task_id,reward`. `task_column` et `reward_column` permettent d'adapter leurs noms. Compatible avec le `summary.csv` du dépôt OpenMOSS, à condition de séparer les passes.
- `json` : liste de lignes ou objet contenant `rows`, avec les mêmes champs.
- `pier` : parcourt les `reward.json` sous le dossier d'un run ; reconnaît `task_001__trial/verifier/reward.json` et `task_001/reward.json`.
- `ctrf` : accepte les fichiers `ctrf.json` seulement avec `scoring_test_names`, liste explicite des tests qui définissent le succès. Le simple total de tests passés n'établit pas la récompense : la frontière public/privé doit être connue. Si les noms diffèrent par tâche, convertir les rewards avec un adaptateur explicite en CSV avant import.

```powershell
python scripts/analyze-swe-science.py --official-dir analysis/swe-bench-science/source --runs-manifest chemin/manifest.json
# Ou une analyse exclusivement sur vos runs :
python scripts/analyze-swe-science.py --runs-manifest chemin/manifest.json --reference qwen-cc-pass2 --output tmp/science-local
```

Les périmètres doivent être identiques : tâches absentes, rewards manquants/non binaires, doublons et collisions d'IDs de runs provoquent une erreur. Aucun échec n'est inventé. Les rewards indiquant une erreur d'infrastructure restent les résultats publiés si le reward vaut 0 ; leur exclusion exige un périmètre explicitement reconstruit et identique pour toutes les passes.

Les passes sont conservées sous des `run_id` distincts. Le script groupe les résultats par modèle/harness/effort et calcule la meilleure union de quatre passes réellement disponibles, y compris Qwen homogène lorsque quatre passes existent. La recherche du portefeuille compare exhaustivement les unions des combinaisons de quatre exécutions distinctes. Elle représente une couverture oracle rétrospective, sans supposer la capacité de choisir automatiquement le bon patch.

Sept tests vérifient notamment le classement indépendant des scores globaux, le refus des valeurs absentes et doublons, la conservation de quatre passes distinctes, les ex æquo et l'exclusion des modèles propriétaires de l'optimum open-weight.
