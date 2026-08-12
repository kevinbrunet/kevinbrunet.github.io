# Blog Hugo — Kévin Brunet

Blog statique Hugo organisé par **séries** et **catégories**, prêt pour GitHub Pages.

## Développement local

Installer Hugo Extended, puis lancer :

```powershell
hugo server -D -F -E
```

Cette commande affiche localement tous les articles : brouillons (`-D`),
publications futures (`-F`) et contenus expirés (`-E`). Ces options ne sont pas
utilisées par le déploiement GitHub Pages.

## Ajouter un article

Créer un fichier dans `content/articles/` avec ce front matter :

```yaml
---
title: "Titre"
date: 2026-07-31
description: "Résumé court."
categories: ["Architecture logicielle"]
series: ["Nom de la série"] # facultatif
series_order: 1             # requis dans une série
collection: "ARCHITECTURE" # ou SYSTÈMES
draft: false
---
```

Le déploiement est automatique à chaque push sur `main`. Dans GitHub, sélectionner **GitHub Actions** comme source dans Settings → Pages.

Le site est également reconstruit automatiquement chaque jour à 08:00, heure de
Paris. Pour programmer un article, indiquer simplement sa date et conserver
`draft: false` :

```yaml
date: 2026-08-12
draft: false
```

Hugo masque l'article avant cette date. Il devient visible lors du déploiement de
08:00 le jour programmé.

## Composants éditoriaux sécurisés

Le HTML brut est désactivé dans Markdown. Ne pas ajouter directement de balises
HTML dans `content/` : utiliser les shortcodes contrôlés ci-dessous. Leur contenu
accepte la syntaxe Markdown habituelle.

```markdown
{{< callout variant="scene" label="Cas concret" >}}
Texte de l'encadré avec du **gras**.
{{< /callout >}}

{{< thesis >}}
Première ligne.  
**Conclusion mise en avant.**
{{< /thesis >}}

{{< pullquote >}}
Citation mise en avant.
{{< /pullquote >}}

{{< closing-question label="À retenir" >}}
Texte de conclusion.
{{< /closing-question >}}

{{< zoomable-figure src="/images/articles/schema.png" alt="Description de l'image" action="Agrandir" label="Voir le schéma en grand" >}}
Légende de l'image.
{{< /zoomable-figure >}}
```

Les seules variantes acceptées par `callout` sont `scene`, `alert` et `key`.
Ajouter un nouveau composant visuel nécessite de créer ou d'étendre un shortcode
dans `layouts/shortcodes/`, sans réactiver `markup.goldmark.renderer.unsafe`.

## Publier en anglais

Le français reste disponible aux URL historiques et l'anglais est publié sous `/en/`.
Pour traduire une page, ajouter un fichier portant le même nom et le suffixe `.en.md` :

```text
content/articles/mon-article.md
content/articles/mon-article.en.md
```

Les deux fichiers sont alors reliés par le sélecteur de langue et par les balises
SEO `hreflang`. Un article peut rester uniquement en français tant que sa traduction
n'est pas prête ; il ne sera pas affiché dans la liste anglaise.
