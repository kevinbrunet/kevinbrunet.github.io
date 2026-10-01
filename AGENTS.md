# Instructions pour les articles Hugo

- Le HTML brut Markdown est volontairement désactivé pour limiter les injections.
- Ne jamais réactiver `markup.goldmark.renderer.unsafe` pour mettre en forme un article.
- Utiliser les shortcodes documentés dans `README.md`, section « Composants éditoriaux sécurisés ».
- Les composants disponibles sont `callout`, `thesis`, `pullquote`, `closing-question` et `zoomable-figure`.
- `callout` accepte uniquement les variantes `scene`, `alert` et `key`.
- Si un nouveau rendu est nécessaire, créer un shortcode à paramètres fermés dans `layouts/shortcodes/` et laisser l'échappement Hugo actif pour tous les paramètres.
- Après toute modification de contenu ou de shortcode, lancer `./.tools/hugo/hugo.exe --buildFuture` et vérifier qu'aucun avertissement `raw HTML omitted` n'apparaît.
- Une CSP est définie très tôt dans `layouts/_default/baseof.html`. Toute nouvelle ressource (script, style, image, police, média ou appel réseau) doit rester locale ou faire l'objet d'une révision explicite et minimale de cette politique ; ne jamais ajouter globalement `'unsafe-inline'` ou `'unsafe-eval'`.

## Contrôle obligatoire de chaque série

Avant de déclarer une série terminée, appliquer toute cette liste :

1. Comparer au dossier source : aucun épisode absent, ajouté involontairement ou dupliqué ; ordre continu de 1 à N.
2. Livrer les N articles français, les N traductions anglaises et les deux pages de série. Vérifier la fidélité des traductions, notamment les chiffres, exemples et liens.
3. Vérifier les métadonnées : même identifiant de série, même ordre dans les deux langues, slugs uniques, dates et statut de publication conformes à la demande.
4. Utiliser les couvertures finales françaises et anglaises correspondantes, avec leurs titres. Ne pas utiliser les images `.base.png` comme couvertures. Contrôler visuellement la correspondance entre image, langue et épisode.
5. Les listes « Sources » contiennent uniquement des références identifiables avec leurs liens. Supprimer les annotations de travail, symboles de validation, réserves, commentaires d'audit et auto-attributions ; ne pas les déplacer ailleurs dans l'article.
6. Compiler avec `./.tools/hugo/hugo.exe --buildFuture`. Aucun avertissement `raw HTML omitted`, aucune erreur d'encodage et aucun caractère de remplacement `�` dans le rendu.
7. Servir l'aperçu avec `--disableFastRender --renderToMemory`. Après des ajouts ou changements groupés, vérifier son état complet ; redémarrer si les pages servies diffèrent de la compilation. Ne pas laisser le serveur et la compilation écrire dans le même dossier.
8. Vérifier la page de série dans chaque langue : N liens, dans l'ordre 01 à N, tous accessibles. Sur chacun des 2N articles, vérifier que « Continuer la série » présente les N épisodes de la langue courante, sans omission.
9. Vérifier tous les liens internes, les images et le sélecteur FR/EN dans les deux sens, ainsi que les liens de traduction des pages de série. Vérifier les libellés d'interface dans la bonne langue.
10. Exécuter `./scripts/check-series.ps1 -Series "identifiant-de-serie" -ExpectedCount N`, puis contrôler le rendu dans le navigateur : début d'article, couverture, sources, citation et navigation de fin. Ne pas conclure sur la seule présence des fichiers ou la seule réussite de Hugo. Corriger chaque échec avant de livrer.
