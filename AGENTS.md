# Instructions pour les articles Hugo

- Le HTML brut Markdown est volontairement désactivé pour limiter les injections.
- Ne jamais réactiver `markup.goldmark.renderer.unsafe` pour mettre en forme un article.
- Utiliser les shortcodes documentés dans `README.md`, section « Composants éditoriaux sécurisés ».
- Les composants disponibles sont `callout`, `thesis`, `pullquote`, `closing-question` et `zoomable-figure`.
- `callout` accepte uniquement les variantes `scene`, `alert` et `key`.
- Si un nouveau rendu est nécessaire, créer un shortcode à paramètres fermés dans `layouts/shortcodes/` et laisser l'échappement Hugo actif pour tous les paramètres.
- Après toute modification de contenu ou de shortcode, lancer `./.tools/hugo/hugo.exe --buildFuture` et vérifier qu'aucun avertissement `raw HTML omitted` n'apparaît.
- Une CSP est définie très tôt dans `layouts/_default/baseof.html`. Toute nouvelle ressource (script, style, image, police, média ou appel réseau) doit rester locale ou faire l'objet d'une révision explicite et minimale de cette politique ; ne jamais ajouter globalement `'unsafe-inline'` ou `'unsafe-eval'`.
