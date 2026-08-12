---
title: "Comment cacher une watermark dans un texte généré par une IA"
slug: "comment-cacher-watermark-texte-ia"
date: 2026-08-13
description: "Une watermark textuelle se cache dans une succession de choix statistiques orientés, pas dans un caractère invisible. Voici comment ce signal fonctionne."
categories: ["Intelligence artificielle", "Ingénierie logicielle"]
series: ["comprendre-les-watermarks-textuelles"]
series_order: 2
collection: "ARCHITECTURE"
cover: "/images/articles/watermark-textuelle-technique.fr.png"
draft: false
---

**Il n'y a généralement aucun caractère invisible à retrouver. La marque se cache dans une succession de choix statistiquement orientés.**

*Anthropic vient d'annoncer que les nouveaux modèles Claude lancés dans l'Union européenne à partir du 2 août 2026 intégreront des marques lisibles par machine, dont une watermark directement incorporée aux textes générés. L'entreprise ne publie pas encore le détail de son algorithme. Mais cette annonce rend le sujet très concret : il me semblait important de revenir sur la mécanique générale qui permet de cacher une telle marque dans une succession de mots.*

{{< callout variant="scene" label="Point de départ" >}}
Prenez cette phrase inachevée :

**« Cette méthode est particulièrement… »**
{{< /callout >}}

Un modèle de langage pourrait la poursuivre avec "efficace", "utile", "adaptée", "pertinente" ou des dizaines d'autres fragments.

Pour produire la suite, il attribue une probabilité à chaque possibilité. Il peut estimer, par exemple, que "efficace" a 23 % de chances d'être un bon choix, "pertinente" 18 %, "utile" 15 % et "adaptée" 12 %.

Une watermark textuelle intervient dans cet espace de choix.

Elle n'ajoute pas nécessairement une information au fichier. Elle ne glisse pas non plus un alphabet secret dans le texte. Elle modifie légèrement la manière dont le modèle sélectionne ses prochains tokens afin de faire apparaitre, sur une séquence assez longue, un motif que seul un détecteur correctement configuré sait mesurer.

## Un modèle ne choisit pas directement des mots

Un modèle de langage découpe le texte en unités appelées *tokens*. Un token peut correspondre à un mot entier, à une partie de mot, à un signe de ponctuation ou parfois à un espace associé au fragment suivant.

À chaque étape, le modèle calcule une distribution de probabilités sur les tokens susceptibles de continuer la séquence. Il en sélectionne un, l'ajoute au texte, puis recommence à partir de la nouvelle séquence.

La génération ressemble donc à cette boucle :

1. lire les tokens déjà présents ;
2. calculer les continuations possibles ;
3. choisir le prochain token ;
4. l'ajouter au contexte ;
5. recommencer.

La watermark agit à la troisième étape.

Elle utilise une clé secrète pour orienter légèrement certains choix. Selon le contexte, le système peut considérer une partie des tokens comme momentanément favorisés. Le modèle conserve des phrases naturelles parce qu'il ne choisit pas n'importe quel token : il augmente seulement les chances de certaines continuations qui étaient déjà plausibles.

Le mot "efficace" n'est donc jamais une preuve en lui-même. Dans un autre contexte, ou après une autre suite de tokens, il pourrait ne pas être favorisé du tout.

{{< thesis >}}
Ce qui constitue la marque,  
**c'est l'accumulation des choix.**
{{< /thesis >}}

{{< zoomable-figure src="/images/articles/schema-selection-token-watermark.fr.png" alt="Processus de sélection d'un token pour créer une watermark textuelle" action="Agrandir" label="Voir le schéma de sélection d'un token en grand" >}}
La clé secrète n'impose pas un mot arbitraire : elle oriente légèrement le choix parmi des tokens déjà plausibles. Répétée sur un texte assez long, cette préférence fait émerger un motif statistique détectable.
{{< /zoomable-figure >}}

## Le signal apparait dans la répétition

Imaginons, pour simplifier, que la moitié des tokens possibles soient favorisés à chaque position.

Un texte non marqué devrait tomber dans ce groupe environ une fois sur deux. Un modèle marqué pourrait y tomber un peu plus souvent : 55 %, 60 % ou davantage selon le réglage retenu.

Sur dix tokens, cet écart ne signifie presque rien. Le hasard produit facilement six ou sept correspondances.

Sur plusieurs centaines de tokens, une préférence répétée devient plus difficile à expliquer par le hasard. Le détecteur reprend alors le texte, reconstitue à chaque position les choix que la clé aurait favorisés et compte les correspondances.

Il transforme ce comptage en score statistique. Plus le score s'éloigne du comportement attendu pour un texte non marqué, plus la présence de la watermark est jugée probable.

{{< callout variant="alert" label="La question du détecteur" >}}
Il ne demande pas : « Cette phrase contient-elle le code secret ? »

Il demande : « Cette longue suite de choix est-elle anormalement compatible avec les préférences produites par cette clé ? »
{{< /callout >}}

## Pourquoi la clé dépend du contexte

Une méthode naïve favoriserait toujours la même liste de tokens. Elle créerait des biais faciles à observer et peut-être à exploiter.

Les méthodes modernes font varier les préférences en fonction du contexte déjà généré. Une fonction pseudo-aléatoire combine la clé secrète et certains tokens précédents pour produire de nouveaux scores à chaque position.

Deux occurrences du même mot ne reçoivent donc pas nécessairement le même traitement. Après une séquence donnée, "pertinente" peut être avantagée. Trois lignes plus loin, dans un autre contexte, elle ne le sera pas.

Cette variation permet de répartir la marque dans toute la génération sans transformer quelques mots précis en signature permanente.

Elle produit aussi une propriété importante : lorsqu'un token est modifié, le calcul des positions suivantes peut changer, puisqu'il repose désormais sur un contexte différent.

## SynthID fait concourir plusieurs candidats

La méthode SynthID-Text publiée par Google DeepMind ne se contente pas d'ajouter un bonus fixe à une liste de tokens.

Le modèle tire plusieurs candidats selon sa distribution normale. Ces candidats participent ensuite à un tournoi pseudo-aléatoire déterminé par la clé. À chaque tour, les candidats sont comparés par paires et l'un des deux est retenu. Le dernier survivant devient le token produit.

Avec trois tours, huit candidats initiaux sont réduits successivement à quatre, puis deux, puis un.

Ce mécanisme permet d'influencer le choix final tout en partant de candidats réellement proposés par le modèle. Il peut être configuré pour préserver, en moyenne, la distribution originale : sur de nombreuses générations, un token ne devient pas globalement plus fréquent simplement parce qu'il appartient à une liste fixe.

Le détecteur qui connait la clé peut cependant recalculer les résultats pseudo-aléatoires associés aux tokens observés. En agrégeant leurs scores, il recherche la corrélation introduite par les tournois successifs.

La subtilité est là : la distribution générale peut sembler normale, alors que les choix individuels restent corrélés à une information secrète.

## Certains textes offrent plus d'espace que d'autres

{{< pullquote >}}
Une watermark a besoin de choix.
{{< /pullquote >}}

Dans un récit, un courriel ou une explication développée, plusieurs formulations peuvent généralement poursuivre chaque phrase sans en dégrader le sens. Le système dispose alors d'une certaine liberté pour orienter la sélection.

Dans une réponse très contrainte, cette liberté disparait. À la question "Quelle est la capitale de la France ?", la réponse utile contient nécessairement "Paris". Pour une citation exacte, une formule mathématique, du code très rigide ou une liste de faits précis, modifier les tokens peut altérer la justesse du résultat.

Si un seul token est réellement acceptable, aucune technique de sélection ne peut y cacher beaucoup d'information.

C'est pourquoi Google DeepMind indique que SynthID fonctionne mieux sur des réponses longues et variées que sur des réponses factuelles ou très courtes.

## Copier conserve la marque, réécrire la fragilise

La watermark appartient à la séquence des tokens, pas au fichier qui les contient.

Un copier-coller conserve donc le signal. Changer la police, convertir un document ou publier le texte sur une autre plateforme ne modifie généralement pas les tokens analysés.

Quelques corrections ponctuelles peuvent aussi laisser assez de choix marqués pour permettre une détection.

Une réécriture profonde pose un autre problème. Considérez ces deux phrases :

> Cette méthode réduit considérablement le temps nécessaire.

> Cette approche permet d'accomplir la tâche beaucoup plus rapidement.

Le sens reste proche, mais presque toute la séquence de tokens a changé. Une traduction ou une paraphrase complète peut ainsi effacer une grande partie de la corrélation recherchée.

Lorsque le calcul dépend de plusieurs tokens précédents, une seule modification peut également perturber les scores des positions qui suivent. Le système peut ensuite se resynchroniser si la séquence redevient identique, mais des changements régulièrement répartis brouillent une part importante du signal.

{{< callout variant="key" label="Limite structurelle" >}}
**Ce n'est pas seulement un défaut d'implémentation.**
{{< /callout >}}

Le langage permet de préserver approximativement une idée tout en transformant presque entièrement sa forme. Une watermark résistante à toutes les reformulations devrait reconnaitre l'idée elle-même plutôt que la séquence qui l'exprime. Elle ne serait alors plus vraiment une watermark : elle deviendrait un système de comparaison sémantique, avec d'autres incertitudes.

## Le seuil fabrique le compromis

Même sans watermark, un texte peut contenir par hasard beaucoup de tokens compatibles avec la clé. Le détecteur doit donc fixer un seuil au-delà duquel il considère le signal comme significatif.

Un seuil bas détecte davantage de textes marqués, mais produit plus de faux positifs. Un seuil élevé réduit les alertes injustifiées, mais laisse passer davantage de textes réellement marqués.

Ce compromis ne disparait pas grâce à un meilleur vocabulaire marketing.

La longueur du texte compte également. Sur un passage court, le détecteur dispose de peu d'observations. Quelques correspondances fortuites peuvent fortement faire varier le score. Une réponse responsable devrait alors être "signal insuffisant", plutôt que "humain" ou "IA".

Les tests multiples aggravent encore le problème. Si une organisation découpe un document en dizaines de passages, essaie les clés de nombreux fournisseurs et ne conserve que le score le plus élevé, elle multiplie les occasions de trouver une corrélation par hasard. Le seuil doit tenir compte de cette procédure globale, pas seulement de chaque test pris isolément.

## Watermark et métadonnées ne jouent pas le même rôle

Une provenance cryptographique, comme celle que peut porter un fichier selon le standard C2PA, fonctionne autrement.

Un service signe une déclaration indiquant l'origine ou les traitements appliqués au fichier. Lorsque la signature est valide, le vérificateur peut contrôler que cette déclaration n'a pas été modifiée. Il ne cherche pas une anomalie statistique dans le contenu.

Cette précision a un prix : les métadonnées peuvent être supprimées lors d'une conversion, d'un copier-coller ou d'un réenregistrement. Une watermark textuelle survit mieux à la séparation entre le contenu et son fichier, mais elle fournit un signal probabiliste et peut être affaiblie par la réécriture.

Les deux approches répondent donc à des problèmes différents :

- la signature dit précisément ce qu'un service atteste, tant que cette attestation accompagne encore le fichier ;
- la watermark recherche un motif incorporé au contenu, même après un copier-coller ;
- aucune des deux ne prouve à elle seule qui a conçu les idées ni pourquoi l'outil a été utilisé.

## Un canal statistique à faible débit

La manière la plus juste de comprendre une watermark textuelle est peut-être de la voir comme un petit canal de communication caché dans les choix du modèle.

Chaque token transporte très peu d'information. Le signal ne devient lisible qu'en accumulant de nombreuses décisions. Plus on cherche à renforcer ce signal, plus on risque de contraindre la génération ou d'en modifier la qualité. Plus on préserve la liberté normale du modèle, plus la détection demande un texte long et reste sensible aux transformations.

Une watermark textuelle n'est donc ni magique ni inutile.

C'est un compromis d'ingénierie entre quatre objectifs qui entrent partiellement en tension : rendre la marque invisible, préserver la qualité du texte, résister aux modifications et limiter les erreurs de détection.

Comprendre cette mécanique permet d'éviter deux excès symétriques : croire qu'une marque est une preuve cryptographique infaillible, ou penser qu'elle ne fournit aucune information.

{{< closing-question label="À retenir" >}}
Elle fournit un signal réel, dans certaines conditions, avec un niveau de confiance et des limites mesurables.

Tout commence à déraper lorsqu'on oublie la dernière partie.
{{< /closing-question >}}

---

## Sources

- Dathathri et al., [*Scalable watermarking for identifying large language model outputs*](https://www.nature.com/articles/s41586-024-08025-4), *Nature*, 2024.
- Google DeepMind, [*Watermarking AI-generated text and video with SynthID*](https://deepmind.google/blog/watermarking-ai-generated-text-and-video-with-synthid/), 14 mai 2024.
- Google DeepMind, [*SynthID: A tool to watermark and identify content generated through AI*](https://deepmind.google/models/synthid/).
- OpenAI, [*Understanding the source of what we see and hear online*](https://openai.com/index/understanding-the-source-of-what-we-see-and-hear-online/), mise à jour du 4 août 2024.
- Anthropic, [*How Claude marks AI-generated content*](https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content), août 2026.
