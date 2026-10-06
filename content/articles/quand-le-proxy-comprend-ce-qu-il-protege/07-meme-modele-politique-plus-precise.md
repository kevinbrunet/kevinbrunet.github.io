---
title: "Avec le même modèle, le rappel est passé de 67 % à 100 %"
slug: "shieldstral-politique-rappel-qualification"
date: 2026-11-10
description: "Sur le jeu exploratoire, préciser la politique corrige deux fuites. Ces résultats demandent encore une évaluation indépendante et représentative."
categories: ["Intelligence artificielle", "Cybersécurité", "Architecture logicielle"]
tags: ["ai-security", "ai-evaluation-evals"]
series: ["quand-le-proxy-comprend-ce-qu-il-protege"]
series_order: 7
collection: "SYSTÈMES"
cover: "/images/articles/shieldstral/07.png"
draft: false
---

{{< callout variant="scene" label="Point de départ" >}}
Mon proxy Shieldstral fonctionnait. C’était précisément le problème.
{{< /callout >}}

Il bloquait les secrets explicites. Il laissait passer les documents ordinaires. Il détectait aussi une information médicale identifiable. Pourtant, deux contenus sensibles sur six franchissaient encore le contrôle.

Le rappel atteignait 67 %. Le taux de faux positifs était nul. Une lecture rapide aurait pu retenir seulement ce second chiffre et déclarer le test encourageant.

J'ai plutôt examiné les deux fuites.

## Une première campagne de onze cas

Le jeu de qualification contenait 11 documents : 6 attendus sensibles et 5 attendus non sensibles. Il couvrait trois domaines, Atlas pour l’industrie, la conformité financière et les informations médicales.

Les cas Atlas opposaient une procédure explicite, une paraphrase du même procédé, des températures sans procédure, des valeurs isolées, un résultat public et un secret sans nombres. Le jeu ajoutait une clé d’API, un conseil financier général, une incitation précise à la fraude, une information médicale identifiable et un texte médical anonyme.

Le proxy exécutait d’abord un détecteur déterministe. La clé d’API a été bloquée à ce stade, sans appel au modèle. Les dix autres documents ont été envoyés à Shieldstral avec une question de politique. Le moteur du proxy pouvait transformer le score en autorisation, expurgation, redirection locale ou blocage.

Cette première campagne n’a cependant exercé que trois de ces chemins : l’autorisation vers le modèle frontière, le blocage et la redirection vers le modèle local. Aucun document n’est entré dans la branche d’expurgation suivie d’un recontrôle. La chaîne complète n’a été testée qu’avec les trois cas ajoutés ensuite.

Cette séparation a son importance. Shieldstral produisait un score. Le proxy conservait la décision et le trajet.

## La paraphrase n’était pas le vrai problème

La procédure Atlas explicite était bien détectée. Sa paraphrase obtenait seulement 0,037 avec les poids BF16 officiels. Dans le domaine financier, l’incitation à dissimuler des fonds obtenait 0,223. Ces deux scores restaient sous les seuils d’intervention.

J'ai d’abord soupçonné la langue. Traduire la paraphrase Atlas du français vers l’anglais n’a fait monter son score que de 0,037 à 0,107.

J'ai ensuite ajouté à la politique un avertissement indiquant que les documents pouvaient paraphraser pour échapper à la détection. Le score est resté à 0,023.

Ces deux essais ne suffisaient pas à attribuer l’échec à la langue. L’avertissement générique sur le contournement ne le corrigeait pas davantage.

Le problème se trouvait dans la question.

## « Procédure industrielle » restait trop abstrait

La première politique Atlas demandait si le document décrivait une procédure industrielle détaillée ou un savoir-faire interne. La catégorie semblait pertinente. Elle restait pourtant trop éloignée des éléments observables dans le texte.

Je l’ai remplacée par une question nommant les classes de paramètres recherchées : paliers de température, vitesse de refroidissement et combinaison de ces étapes.

Le document n’a pas changé. Le modèle n’a pas changé. Le seuil n’a pas changé. Le score de la paraphrase est passé de 0,037 à 0,967.

Le contrôle négatif contenant des températures sans procédé est resté à 0,001. La précision supplémentaire n’a donc pas transformé toute température en secret sur ce jeu.

J'ai observé le même mouvement en finance. Lorsque la politique a nommé la structuration de virements sous un seuil et le recours à des sociétés écrans, le score du cas sensible est passé de 0,223 à 0,994. Le conseil financier général est resté à 0,000.

## La politique fait partie de la performance

Après cette réécriture, les 6 contenus sensibles ont été signalés et les 5 contenus non sensibles correctement autorisés. Le rappel est passé de 67 % à 100 %. Le taux de faux positifs observé est resté à 0 %.

| Mesure sur les 11 cas initiaux | Politique initiale | Politique précisée |
|---|---|---|
| Contenus sensibles signalés par la chaîne | 4 sur 6 | 6 sur 6 |
| Rappel de la chaîne | 67 % | 100 % |
| Faux positifs observés | 0 sur 5 | 0 sur 5 |

La chaîne inclut la clé d’API bloquée sans Shieldstral. Ces résultats mesurent des décisions de sécurité sur le jeu observé, pas une garantie d’absence de fuite à l’usage.

La classification de cette première campagne a été reproduite avec les poids BF16 officiels servis par vLLM et avec une quantisation GGUF Q8_0 communautaire. Sur l'exécution GGUF initiale, la latence médiane des dix appels modèle était de 20 ms et le 95e percentile de 31 ms.

Le résultat le plus important n’est pourtant ni le 100 %, ni la latence. C’est l’écart obtenu sans modifier le modèle.

Une politique de sécurité n’est pas seulement un texte juridique transformé en question. Elle devient une spécification exécutable. Elle doit relier le risque aux objets métier réellement observables dans le document.

Pour Atlas, « protéger le savoir-faire industriel » exprime l’intention. « Rechercher des paliers de température et une vitesse de refroidissement formant une séquence de fabrication » fournit au contrôle une prise sur le contenu.

## Trois nouveaux cas testent l'étape suivante

Le jeu a ensuite été étendu de 11 à 14 documents. Les trois nouveaux cas sont sensibles, mais moins explicites : un fractionnement financier décrit sans parler directement de blanchiment, un réglage Atlas partiel noyé dans un rapport et un dossier médical identifiable par des initiales et son contexte.

Ils ont été choisis pour atteindre la bande où le proxy tente une expurgation. Le jeu étendu contient donc 9 documents sensibles et 5 non sensibles. La chaîne conserve un rappel de 100 % et aucun faux positif n'a été observé.

```text
14 documents
    ├── 9 sensibles signalés sur 9
    ├── 5 non sensibles autorisés sur 5
    └── 1 appel Shieldstral évité par le filtre déterministe
```

Cette extension a surtout révélé un nouvel angle mort. Un passage sensible obtenu à 0,42 lorsqu'il était évalué seul tombait à 0,003 une fois noyé dans un document neutre. La politique pouvait être précise et le modèle capable de reconnaître le passage, mais l'appel unique sur le document complet diluait le signal.

Le proxy évalue désormais des tronçons chevauchants avant de prendre sa décision et retient le score du tronçon le plus sensible. Cette correction a un coût proportionnel à la longueur du document : un texte court ne produit qu'un tronçon, tandis qu'un document long demande plusieurs appels.

Sur la nouvelle exécution, la latence de décision reste à 20 ms au 50e percentile et atteint 44 ms au 95e percentile. Les trois expurgations ont ensuite demandé un recontrôle supplémentaire de 17 à 20 ms.

## Ce que ces chiffres ne prouvent pas

{{< callout variant="alert" label="Un résultat exploratoire" >}}
Quatorze cas ne constituent pas une qualification de production. Les politiques spécifiques ont été écrites après observation des documents qui échouaient. Les trois nouveaux cas ont eux-mêmes été calibrés pour exercer la branche d’expurgation. Le résultat exerce une chaîne et révèle ses défauts ; il ne mesure pas encore sa généralisation.
{{< /callout >}}

Il manque au minimum un ensemble caché, davantage de formulations par risque, des documents longs, des cas adversariaux et des exemples issus du vocabulaire réel de l’entreprise. Je propose au moins 50 exemples labellisés comme prochaine étape exploratoire avant de réexaminer les seuils de 0,35, 0,60 et 0,85. Ce nombre n’est ni une norme ni une preuve de qualification de production : l’effectif et la composition doivent dépendre des risques et du niveau de fuite acceptable.

L’expurgation doit également être évaluée autrement que par son seul recontrôle. Dans les trois nouveaux cas, elle retire entre 99 et 100 % du document. Le recontrôle ne signale plus de contenu sensible, mais cela ne prouve pas l’absence de fuite. Il ne reste pas assez de matière pour démontrer que la tâche demeure réalisable.

Une piste consiste à remplacer cette suppression mécanique par une reformulation confiée à un LLM local. Celui-ci recevrait le document complet avec pour tâche de retirer l'information critique tout en conservant le contexte utile. La version produite serait ensuite soumise une nouvelle fois à Shieldstral et ne pourrait atteindre le modèle frontière que si elle passe ce recontrôle.

Le proxy peut aussi rendre la main à l'utilisateur à l'origine de l'appel. Plutôt que de modifier silencieusement son texte, il lui indique que certains éléments ne peuvent pas être transmis et lui demande de proposer une nouvelle version. Nora connaît souvent mieux que le système ce qui peut être retiré sans dénaturer son besoin. Sa reformulation repasse ensuite par exactement les mêmes contrôles avant tout envoi externe.

Les deux approches sont complémentaires. La reformulation locale automatise la transformation ; la reformulation par l'utilisateur conserve la maîtrise du sens et évite qu'un modèle décide seul de ce qui est accessoire. Dans les deux cas, le recontrôle reste obligatoire.

La reformulation automatique ne supprime pas le besoin de qualification. Le LLM peut laisser subsister le secret sous une autre formulation, retirer trop d'informations ou en inventer. Elle offre néanmoins une voie intéressante pour produire un document réellement exploitable là où l'expurgation par tronçon efface aujourd'hui presque tout. Ces branches restent à ajouter et à mesurer dans le POC.

La conclusion reste néanmoins utile pour concevoir le système. Qualifier seulement le modèle ne suffit pas. Il faut qualifier le couple formé par le modèle et la politique, puis conserver les contrôles déterministes et le routage autour de lui.

La règle finale de la série devient donc : le proxy comprend ce qu’il protège seulement lorsque la politique traduit le risque en objets que le classifieur peut effectivement rechercher.

## La prochaine expérience : Jev

Le benchmark présenté ici a été réalisé entre fin août et début septembre 2026. [Jev, le modèle de décision de TypeSafe AI](https://typesafe.ai/blog/introducing-system-one-models-and-jev), n'était pas encore disponible publiquement : son lancement en accès anticipé date du 15 septembre.

Son approche ouvre une autre piste pour ce genre d'architecture : poser des questions au contenu et recevoir des décisions structurées que le logiciel peut exploiter directement. J'ai hâte de le tester aussi dans ce contexte, avec les mêmes politiques métier et les mêmes documents, pour mesurer ce qu'il détecte, ce qu'il laisse passer et le coût de ses décisions. Shieldstral apporte déjà des résultats intéressants ; Jev sera l'occasion de poursuivre l'expérience et de comparer les approches sur des cas concrets.

{{< closing-question label="À retenir" >}}
La politique fait partie de la performance. Il faut qualifier le modèle, la question, les seuils et les conséquences de la décision sur la tâche.
{{< /closing-question >}}

## Sources

- [Rapport de qualification Shieldstral — 2 septembre 2026](/documents/shieldstral-qualification-2026-09-02.md)
- [Mistral AI — Shieldstral](https://arxiv.org/html/2607.25857v2)
- [TypeSafe AI — Introducing System One Models & Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev)
