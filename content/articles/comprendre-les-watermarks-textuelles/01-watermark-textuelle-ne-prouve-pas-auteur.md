---
title: "Ce qu'une watermark textuelle ne prouve pas"
slug: "watermark-textuelle-ne-prouve-pas-auteur"
date: 2026-08-12
description: "Une watermark peut signaler le passage d'un texte par une IA sans prouver qui en est l'auteur, son intention ou le travail réellement fourni."
categories: ["Intelligence artificielle", "Société"]
series: ["comprendre-les-watermarks-textuelles"]
series_order: 1
collection: "SYSTÈMES"
cover: "/images/articles/watermark-textuelle-consequences.fr.png"
draft: false
---

**Un texte peut porter la marque d'une IA sans avoir été écrit par elle. Et cette nuance pourrait décider d'une note, d'un recrutement ou d'une accusation de fraude.**

*Anthropic vient d'annoncer la généralisation progressive de marques lisibles par machine dans les contenus produits par Claude. Les nouveaux modèles lancés dans l'Union européenne à partir du 2 août 2026 doivent notamment intégrer une watermark aux textes qu'ils génèrent, quel que soit le produit depuis lequel ils sont utilisés. À la suite de cette annonce, il me semblait important de revenir sur ce que les watermarks textuelles permettent réellement d'établir et surtout sur les conclusions qu'elles ne permettent pas de tirer.*

{{< callout variant="scene" label="Cas concret" >}}
**Vous écrivez une lettre de motivation.**

Les idées sont les vôtres. Les exemples viennent de votre parcours. Vous avez choisi chaque argument. Avant de l'envoyer, vous demandez simplement à une intelligence artificielle de corriger les fautes et d'alléger une phrase maladroite.
{{< /callout >}}

Quelques jours plus tard, un recruteur passe cette lettre dans un détecteur. Une watermark est repérée. **Sa conclusion tombe : "texte généré par une IA".**

Le détecteur a peut-être correctement identifié quelque chose. Mais le recruteur en a déduit beaucoup trop.

{{< thesis >}}
Le texte est bien passé par une IA.  
**Cela ne signifie pas que l'IA en est l'auteur.**
{{< /thesis >}}

C'est toute l'ambiguïté des watermarks textuelles : elles peuvent fournir un indice sur le parcours d'un texte, puis être utilisées comme une preuve sur l'identité de son auteur, la quantité de travail qu'il a fournie ou son intention de tromper.

Or elles ne prouvent rien de tout cela.

## Une marque cachée dans les choix de mots

Une watermark textuelle n'est généralement ni un caractère invisible ni une étiquette attachée au fichier.

Lorsqu'un modèle écrit, il choisit chaque nouveau fragment de texte parmi plusieurs suites possibles. Après "cette solution est", il pourrait par exemple continuer avec "efficace", "pertinente", "adaptée" ou "intéressante".

Pour créer une watermark, le système favorise très légèrement certains choix selon une règle secrète. Aucun mot n'est suspect à lui seul. Mais, sur un texte assez long, certains choix apparaissent un peu plus souvent que ne le voudrait le hasard.

Le détecteur cherche ensuite cette corrélation statistique.

Il ne retrouve donc pas une signature comparable à un nom au bas d'un contrat. Il mesure la probabilité qu'une suite de mots porte le motif attendu.

Cette distinction compte pour deux raisons.

D'abord, **un texte humain peut parfois ressembler par hasard au motif recherché**. Ensuite, une réécriture importante, une traduction ou plusieurs paraphrases peuvent affaiblir la marque d'un texte réellement produit par une IA. Google DeepMind reconnait ainsi que SynthID fonctionne mieux sur des textes longs et variés, et que son niveau de confiance peut fortement diminuer après une réécriture complète ou une traduction.

{{< callout variant="alert" label="Limite essentielle" >}}
Un résultat positif n'est pas une certitude absolue.

Un résultat négatif n'est pas davantage un certificat d'origine humaine.
{{< /callout >}}

## Le problème le plus grave n'est pas le faux positif

On parle souvent du risque qu'un texte entièrement humain soit marqué par erreur. Ce risque existe. À grande échelle, même un faible taux d'erreur finit par produire beaucoup de personnes injustement suspectées.

Mais un cas plus subtil pose un problème encore plus difficile : **le vrai positif mal interprété.**

Reprenons la lettre de motivation. Si le correcteur IA a régénéré certaines phrases, la watermark peut réellement être présente. Le détecteur ne s'est pas trompé en la repérant.

{{< pullquote >}}
Ce qui est faux, c'est la conclusion ajoutée ensuite :  
**« cette personne n'a pas écrit son texte ».**
{{< /pullquote >}}

La marque ne connait pas le brouillon initial. Elle ne voit pas les heures de travail précédentes. Elle ignore le prompt envoyé au modèle. Elle ne sait pas si l'outil a inventé l'argumentation, traduit un texte existant, simplifié du jargon ou corrigé trois accords.

Elle répond imparfaitement à une question étroite : "ce passage présente-t-il le motif statistique associé à ce système ?"

Elle ne répond pas à la question qui intéresse réellement le professeur, le recruteur ou l'éditeur : "qui a produit les idées et fait le travail intellectuel ?"

Passer de la première question à la seconde demande une enquête sur le processus. Aucun motif caché dans les tokens ne peut la remplacer.

## Les usages les plus légitimes deviennent les plus visibles

Cette confusion ne pénaliserait pas tout le monde de la même manière.

Une personne parfaitement à l'aise à l'écrit peut rendre son texte sans assistance, mais :

- une personne dyslexique peut avoir besoin d'un correcteur ;
- un étudiant étranger peut maitriser son sujet sans encore maitriser toutes les nuances du français ;
- une personne en situation de handicap peut utiliser un outil de reformulation comme technologie d'assistance ;
- un technicien compétent peut vouloir rendre son explication compréhensible sans déléguer son raisonnement.

{{< callout variant="key" label="Distinction clé" >}}
L'IA intervient sur la **forme** sans être nécessairement à l'origine du **fond**.
{{< /callout >}}

Si la simple présence d'une watermark devient un indice de triche, l'institution ne sanctionne plus seulement la délégation d'un travail. **Elle risque de sanctionner l'outil qui permet à certaines personnes d'exprimer leur propre travail dans une forme attendue.**

OpenAI a elle-même cité ce danger dans ses recherches sur le watermarking textuel : cette technique pourrait stigmatiser l'usage de l'IA comme outil d'écriture par les personnes qui rédigent dans une langue qui n'est pas la leur.

Le paradoxe est sévère : les utilisateurs qui cherchent délibérément à tromper peuvent tenter de supprimer la marque par des réécritures ou une traduction. Les utilisateurs honnêtes, eux, rendent souvent directement le texte corrigé. Le dispositif devient alors plus contraignant pour ceux qui déclarent ou assument leur assistance que pour ceux qui organisent son contournement.

## Une marque peut voyager sans son auteur

Même lorsqu'une watermark est correctement détectée, elle ne prouve pas qui a demandé la génération.

Un passage marqué peut être cité dans un mémoire, copié dans un courriel, intégré à un document collectif ou envoyé par un collègue. Quelqu'un peut aussi faire reformuler par une IA le texte écrit par une autre personne. La marque suit les mots ; elle n'établit pas l'identité ni l'intention de celui qui les remet.

Elle peut donc révéler un traitement technique sans reconstituer la chaine de responsabilité.

C'est la différence entre provenance et paternité. La provenance décrit les outils rencontrés par un contenu. La paternité cherche à savoir qui a conçu, décidé et formulé l'essentiel. Les deux informations peuvent se recouper, mais elles ne sont pas interchangeables.

## Le bon objet de contrôle est le processus

Si une école interdit toute aide extérieure lors d'un examen, le passage par un modèle peut suffire à constater une violation de cette règle précise. Mais, dans la plupart des situations réelles, les usages ne sont pas aussi binaires.

Corriger l'orthographe, traduire, chercher des idées, rédiger un plan, produire un premier jet ou écrire l'intégralité d'un devoir ne représentent pas le même niveau de délégation.

Une politique sérieuse doit donc définir ce qu'elle évalue avant de choisir son détecteur.

Cherche-t-on à mesurer la maitrise de l'orthographe ? La capacité à argumenter ? La connaissance d'un sujet ? La qualité d'une candidature ? Le respect d'une consigne interdisant explicitement tout outil ?

Sans cette clarification, la watermark fournit une réponse technique à une question que personne n'a correctement posée.

Son usage devrait au minimum respecter quelques principes :

1. Ne jamais transformer une détection en preuve autonome de fraude.
2. Afficher un niveau de confiance, pas un verdict présenté comme certain.
3. Refuser de conclure lorsque le texte est trop court ou le signal trop faible.
4. Permettre à la personne concernée de présenter ses brouillons et d'expliquer sa méthode.
5. Distinguer explicitement l'assistance linguistique de la délégation du raisonnement.
6. Prévoir une contestation humaine avant toute décision ayant des conséquences.
7. Tester les taux d'erreur dans la langue, le type de texte et la population réellement concernés.

Ces précautions ne rendent pas la watermark inutile. Elles la remettent simplement à sa place.

## Un indice de parcours, pas un détecteur de vérité

Les watermarks textuelles peuvent aider à étudier la diffusion de contenus générés, à signaler le passage probable par un service ou à compléter d'autres indices de provenance.

Elles ne peuvent pas raconter à elles seules l'histoire complète d'un texte.

Un résultat positif ne prouve ni que l'IA est l'auteur principal ni que son utilisateur a voulu tromper. Un résultat négatif ne prouve pas que le texte est humain : le modèle pouvait ne pas apposer de marque, le passage pouvait être trop court ou la marque pouvait avoir été altérée.

La question décisive n'est donc pas : "une IA a-t-elle touché ce texte ?"

Dans un monde où les correcteurs, les traducteurs et les outils d'accessibilité intégreront de plus en plus de modèles génératifs, presque tous les textes pourront un jour avoir été "touchés" par une IA.

{{< closing-question label="La bonne question" >}}
« Qu'a fait l'outil, qu'a fait la personne, et quelle capacité cherchons-nous réellement à évaluer ? »
{{< /closing-question >}}

Une watermark peut contribuer à cette enquête. Elle ne peut pas en prononcer le verdict.

## Sources

- Google DeepMind, [*Watermarking AI-generated text and video with SynthID*](https://deepmind.google/blog/watermarking-ai-generated-text-and-video-with-synthid/), 14 mai 2024.
- Dathathri et al., [*Scalable watermarking for identifying large language model outputs*](https://www.nature.com/articles/s41586-024-08025-4), *Nature*, 2024.
- OpenAI, [*Understanding the source of what we see and hear online*](https://openai.com/index/understanding-the-source-of-what-we-see-and-hear-online/), mise à jour du 4 août 2024.
- Anthropic, [*How Claude marks AI-generated content*](https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content), août 2026.
