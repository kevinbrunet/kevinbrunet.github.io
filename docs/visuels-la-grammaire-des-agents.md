# Couvertures — La grammaire des agents

Collection : **ARCHITECTURE**. Format final : **1920 × 1080 px**.

Les six couvertures françaises fournies dans le dossier source sont conservées. Les versions anglaises ont été produites avec l’outil ImageGen intégré, à partir de nouvelles images maîtresses sans texte inspirées de ces couvertures. Aucun texte n’a été ajouté par un script ; le traitement local se limite à la normalisation des dimensions.

Les 18 fichiers sont conservés dans `static/images/articles/la-grammaire-des-agents/` : six images maîtresses `.base.png`, six couvertures `.fr.png` et six couvertures `.en.png`. La couverture anglaise retenue pour le sixième épisode porte le suffixe `-v2.en.png`.

| Épisode | Hook français fourni | Hook anglais retenu | Métaphore |
| --- | --- | --- | --- |
| 01 | LE PROMPT CONSEILLE. LA GRAMMAIRE INTERDIT. | PROMPTS ADVISE. GRAMMARS FORBID. | Une porte filtre les tokens sur un pont avant leur sortie. |
| 02 | LE RAISONNEMENT NE DOIT PAS PARLER JSON | REASONING SHOULD NOT SPEAK JSON | Un parcours libre dans un labyrinthe mène à une sortie structurée. |
| 03 | UNE GRAMMAIRE POUR CETTE BASE. PAS UNE AUTRE. | A GRAMMAR FOR THIS DATABASE. NO OTHER. | Le schéma réel façonne la porte qui filtre les éléments admissibles. |
| 04 | LA SORTIE DANGEREUSE N’EXISTE JAMAIS. | DANGEROUS OUTPUT NEVER GETS GENERATED. | Une porte conserve le chemin admissible et bloque celui qui nécessiterait une reprise. |
| 05 | INTELLISENSE PEUT-IL GUIDER LE MODÈLE ? | CAN INTELLISENSE GUIDE THE MODEL? | Deux branches distinguent classement contextuel et filtrage syntaxique. |
| 06 | LES MODÈLES FRONTIÈRES CACHENT LE SAMPLER. | FRONTIER MODELS HIDE THE SAMPLER. | Les ports visibles d’une machine donnent accès à un mécanisme interne fermé. |

## Prompts des images maîtresses

Pour chaque épisode, fournir sa couverture française comme référence et employer cette spécification, avec la métaphore de la ligne correspondante :

```text
Create a text-free master illustration inspired by the supplied editorial
cover. Preserve the episode's central metaphor and architectural cutaway,
navy blueprint grid, cream engraving, cobalt accents and one continuous
coral thread. Reserve quiet space at the left for editorial typography.
Remove all titles, labels, signatures, words, numbers, letters and
pseudo-text. Use abstract line rectangles instead of lettering on cards.
No words anywhere. Landscape 16:9, 1920 × 1080.
```

Les métaphores demandées, dans l’ordre :

1. Gate on a bridge filtering blue geometric tokens, rejected coral shapes.
2. Cream architectural maze and free coral path leading through a gate into a structured output chamber.
3. Schema blueprint panel and custom gate filtering cobalt permitted objects.
4. Gate, valid cobalt route, blocked coral path and avoided retry loop.
5. Branching completion cards, contextual ranking weights and syntax gate mask.
6. Closed inference machine with three ports and a cutaway internal mechanism, human engineer at lower left.

## Prompts des couvertures anglaises

Pour chaque épisode, fournir **son image maîtresse sans texte** comme référence, reprendre sa métaphore et insérer son hook anglais exact :

```text
Use the supplied text-free master as reference for a finished English
editorial cover, landscape 16:9, 1920 × 1080. Preserve the central metaphor,
navy blueprint, cream engraving, cobalt accents and continuous coral
thread. Integrate tall condensed sans-serif editorial typography on the
quiet left side; maximum three lines for the hook. Strong hierarchy,
generous safe margins, readable on mobile.
Text verbatim:
Top label: "THE GRAMMAR OF AGENTS · NN"
Main hook: "[exact English hook from the table]"
Signature: "KÉVIN BRUNET"
No other text, no pseudo-text, no duplicated words.
```

Pour la correction retenue de l’épisode 06, préciser :

```text
Typography must be tall condensed sans serif, like DIN Condensed or Bebas
Neue: absolutely no serifs, no Times, no classical Roman lettering.
Exact label: "THE GRAMMAR OF AGENTS · 06"
Exact hook: "FRONTIER MODELS HIDE THE SAMPLER."
Exact signature: "KÉVIN BRUNET"
Cream main letters, optional cobalt pivot. No coral-colored typography.
Preserve the closed machine, three ports, internal cutaway, engineer and
coral thread from the text-free master reference.
```

Les couvertures françaises étant fournies, elles n’ont pas fait l’objet d’une nouvelle génération.
