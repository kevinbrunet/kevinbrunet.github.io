# Calculs de la série « L'oracle »

Les résultats sont calculés tâche par tâche à partir des données publiques DeepSWE v1.1 consultées le 6 octobre 2026. Les fichiers d'entrée sont conservés, compressés sans perte, dans `inputs/` ; `manifest.json` donne leur provenance et l'empreinte SHA-256 des fichiers décompressés.

Depuis la racine du dépôt, avec Python 3 et sa bibliothèque standard :

```powershell
python scripts/analyze-deepswe-oracle.py --trials analysis/deepswe-oracle/inputs/trials.json.gz --tasks analysis/deepswe-oracle/inputs/tasks.json.gz --epoch analysis/deepswe-oracle/inputs/epoch.html.gz
```

Le script accepte également les mêmes fichiers non compressés. Il produit `analysis.json` et `luna-failures-epoch.csv`.

## Convention de calcul

- Cohorte : 113 tâches, source `deep-swe`, périmètre `full`, 70 configurations et harness `mini-swe-agent`.
- Couverture : une tâche compte si au moins une tentative publiée a `passed=true`, sans déduire les recouvrements des scores globaux.
- Jusqu'à quatre tentatives disponibles : les absences ne sont pas remplacées par des échecs fictifs. Une récompense absente ne prouve pas que la proposition était incorrecte.
- Rejeu avec arrêt anticipé : pour chaque configuration et tâche, trier par `started_at`, puis `trial_name`. Simuler chaque étage sur les tâches sans succès au précédent. Aucune transmission de diagnostic entre exécutions n'est simulée.
- Les coûts sont estimés, pas facturés. La consommation des traces est conservée. Pour reproduire les ajustements proportionnels de tarifs dans l'interface officielle à cette date, les coûts bruts de Luna sont multipliés par 0,2 et ceux de GLM-5.3 Flash par 0,5. Astra et GLM-5.2 conservent leurs coûts bruts. Le budget de quatre essais de l'article 1 est calculé avant arrondi.
- La frontière économique incluse dans le JSON utilise cette revalorisation partielle : elle ne représente pas une comparaison de tous les tarifs actuels du marché.
- Les 23 tâches signalées par Epoch sont identifiées séparément. Le calcul qui les exclut constitue une analyse de sensibilité ; il ne valide pas les 90 tâches restantes et ne corrige pas les verdicts individuels.
- Les tests appariés exploratoires contenus dans le JSON ne corrigent ni les erreurs du grader ni la sélection a posteriori des configurations.

## Résultats utilisés dans les articles

- Luna `[max]` : 102/113 tâches avec au moins une acceptation.
- Astra `[xhigh]` : 91/113.
- GLM-5.3 Flash `[max]` : 96/113 seul ; 10 des 11 échecs de Luna récupérés ; union 112/113.
- Progression Flash sur les échecs de Luna, dans l'ordre chronologique retenu : 3, puis 7, puis 0, puis 0 nouvelles tâches.
- Flash → Luna → GLM-5.2 : 239 tentatives, coût estimé 76,46 $ ; ordre inverse : 209 tentatives, 119,31 $ ; économie relative d'environ 36 %.

La version antérieure du tableau utilisait un ordre par identifiant de tentative. Cet ordre change les succès intermédiaires et les coûts de l'arrêt anticipé. Il ne change pas les unions finales. La convention retenue ici utilise les dates de démarrage pour pouvoir reproduire une progression temporelle publiée.

Les acceptations sont les verdicts du grader. Ces résultats ne constituent pas une revalidation indépendante des propositions ni une mesure prospective de la chaîne.
