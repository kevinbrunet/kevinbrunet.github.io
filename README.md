# Blog Hugo — Kévin Brunet

Blog statique Hugo organisé par **séries** et **catégories**, prêt pour GitHub Pages.

## Développement local

Installer Hugo Extended, puis lancer :

```powershell
hugo server -D -F -E --disableFastRender --renderToMemory
```

Cette commande affiche localement tous les articles : brouillons (`-D`),
publications futures (`-F`) et contenus expirés (`-E`). Ces options ne sont pas
utilisées par le déploiement GitHub Pages.

L'aperçu est servi en mémoire avec une reconstruction complète. Il ne partage
ainsi pas les fichiers de sortie de `public/` avec les compilations de vérification.

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

{{< zoomable-figure src="/images/articles/schema-vertical.png" alt="Description du diagramme" action="Agrandir" label="Voir le diagramme en grand" size="compact" >}}
Légende d'un diagramme vertical affiché dans une largeur réduite.
{{< /zoomable-figure >}}

{{< scatter-chart
  dataset="deepswe-luna-cost-recovery"
  title="Coût et récupération"
  description="Chaque point représente une configuration."
  x-label="Tâches couvertes à quatre essais"
  y-label="Échecs récupérés"
  x-min="0" x-max="105"
  y-min="0" y-max="11"
  regression="none"
  frontier="upper-left"
  x-format="currency"
  x-scale="log"
  regression-exclude="configuration-de-reference"
  primary="configuration-principale"
  secondary="configuration-secondaire"
  reference="configuration-de-reference"
  regression-label="Tendance des configurations"
  count-label="configurations"
  x-total="113" y-total="11"
  tooltip-x="Couverture"
  tooltip-y="Échecs récupérés"
  tooltip-residual="Écart à la tendance"
  details-label="Voir les données"
>}}
Légende du graphique. Les données sont lues dans `data/charts/deepswe-luna-cost-recovery.json`.
{{< /scatter-chart >}}

{{< cost-comparison
  dataset="deepswe-routing-orders"
  title="Comparer deux scénarios"
  description="Les scénarios atteignent le même résultat avec des coûts différents."
  x-label="Coût estimé ($)"
  primary="glm-first"
  cost-label="Coût estimé"
  coverage-label="Verdicts positifs"
  attempts-label="Tentatives"
  scenario-label="Scénario"
  count-label="scénarios comparés"
  details-label="Voir les données"
>}}
Légende du graphique. Les données sont lues dans `data/charts/deepswe-routing-orders.json`.
{{< /cost-comparison >}}
```

Les seules variantes acceptées par `callout` sont `scene`, `alert` et `key`.
`zoomable-figure` accepte uniquement les tailles `wide` (par défaut) et `compact`.
`scatter-chart` accepte uniquement les jeux de données nommés stockés dans
`data/charts/`, les régressions `linear` ou `none`, les frontières `upper-left`
ou `none`, les formats d’axe `number` ou `currency` et les échelles horizontales
`linear` ou `log`. Les axes, domaines,
infobulles, points mis en avant et analyses sont configurés
depuis le Markdown. Le graphique conserve un tableau HTML accessible comme repli.
`cost-comparison` compare des scénarios nommés à partir d’un jeu de données local
contenant leur coût, leur couverture et leur nombre de tentatives. Le scénario
principal est le seul affiché en bleu et un tableau HTML reste disponible en repli.
Ajouter un nouveau composant visuel nécessite de créer ou d'étendre un shortcode
dans `layouts/shortcodes/`, sans réactiver `markup.goldmark.renderer.unsafe`.

## Classer un article par sujet

Les mots-clés de recrutement sont regroupés dans la taxonomie `tags`, accessible
depuis **Sujets** (`/sujets/`) et **Topics** (`/en/topics/`). Retenir un ou deux
sujets correspondant à la question principale et à la démonstration de l'article.
Une technologie citée, un exemple ou une conséquence secondaire ne justifie pas
un classement. Ne pas recopier les sujets d'une série sur tous ses épisodes et
ne pas ajouter un sujet général lorsque seul un sujet spécialisé est central.
Si aucun sujet ne correspond au cœur de l'article, utiliser `tags: []`.
Par exemple, pour un article consacré aux limites d'une méthode d'évaluation :

```yaml
tags: ["ai-evaluation-evals", "ai-reliability"]
```

Les identifiants autorisés sont `agentic-ai`, `ai-systems-harness-engineering`,
`ai-evaluation-evals`, `ai-reliability`, `ai-observability`, `llmops-agentops`,
`ai-platform-engineering`, `agent-protocols`, `ai-security`,
`ai-risk-governance` et `software-architecture`.

Conserver les mêmes identifiants sur l'article français et sa traduction anglaise.
Les titres, descriptions, URL et ordre des sujets sont définis dans
`content/tags/<identifiant>/_index.md` et `_index.en.md`. Les sujets sans article
publié ne sont pas affichés dans l'index. Les pages thématiques regroupent les
articles par série, de la série la plus récente à la plus ancienne, puis dans
l'ordre des épisodes. Seuls les épisodes portant le mot-clé sont inclus.
Les articles hors série sont classés par date dans le même parcours.

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
