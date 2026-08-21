---
title: "Vos tests passent. Le réel peut dévier quand même."
seo_title: "Harnais d'agent IA : les limites du happy path"
slug: "happy-path-validation"
date: 2026-09-08
description: "Un harnais ne teste que les erreurs transformées en contrôles et laisse hors champ les situations que personne n'a encore imaginées."
categories: ["Intelligence artificielle", "Ingénierie logicielle"]
series: ["aucun-harnais-n-est-parfait"]
series_order: 2
collection: "ARCHITECTURE"
cover: "/images/articles/02-le-happy-path-de-la-validation.fr.png"
draft: false
---

Un harness teste les erreurs que quelqu'un a pensé à transformer en contrôles.

Cette phrase ne condamne pas les tests. Elle rappelle seulement leur frontière.

Nous avons pris l'habitude d'opposer le code fragile à une validation rigoureuse. L'opposition rassure : si la production devient plus rapide grâce à l'IA, il suffirait de renforcer les contrôles pour conserver la maitrise. Pourtant, la validation possède son propre happy path.

## Le prévu face au réel

Un test est la formulation exécutable d'une attente. Il peut vérifier un résultat nominal, une entrée vide, une erreur connue, une limite de volume ou la non-régression d'un incident passé.

Pour écrire ce test, il a fallu imaginer le cas.

Le harness peut exécuter cette vérification mille fois sans fatigue. Il ne peut pas inventer, par cette seule répétition, la déviation qui n'existe dans aucun exemple, aucune règle et aucun jeu de données qu'on lui a fourni.

On retrouve ici le problème classique du happy path. Un système peut très bien couvrir la grande majorité des situations prises séparément et échouer sur une grande partie des parcours réels. Si dix étapes ont chacune 90 % de chances de rester dans leur cas nominal, la probabilité que les dix restent toutes dans ce cas n'est que de 0,9 puissance 10, soit environ 35 %.

Le parcours exceptionnel n'est donc pas forcément rare. Il peut être la combinaison ordinaire de petites exceptions banales.

## Le harness hérite du regard de son concepteur

Les contrôles les plus utiles naissent souvent de l'expérience. Une panne se produit, l'équipe en comprend le mécanisme puis ajoute un test qui empêchera son retour. Le harness devient progressivement la mémoire exécutable des problèmes rencontrés.

C'est une force considérable. C'est aussi la preuve qu'il ne précède pas toujours le réel.

Avant le premier incident, l'équipe ne savait pas nécessairement que cette classe de défaillance existait. Après l'incident, elle peut la nommer, la reproduire et l'ajouter à sa ligne de défense. Le harness apprend, mais une partie de son apprentissage est rétrospective.

La bonne question n'est donc pas : "Nos tests passent-ils ?" Elle est : "Qu'est-ce qui pourrait être faux tout en faisant passer nos tests ?"

Cette question change la revue. Elle ne cherche plus seulement les contrôles manquants autour d'un comportement connu. Elle recherche les hypothèses silencieuses sur lesquelles repose la définition même du succès.

## Plus de tests ne résout pas automatiquement le problème

L'IA permet de générer beaucoup de tests à faible coût. C'est utile pour élargir les combinaisons d'entrées, renforcer la non-régression et explorer des cas auxquels un développeur n'aurait pas consacré du temps.

Mais la quantité ne garantit pas l'indépendance du regard.

Si le même modèle lit la demande, écrit le code puis produit cent tests à partir de sa propre compréhension, ces cent tests peuvent explorer très largement un malentendu commun. La couverture augmente. La conformité au besoin, elle, n'a peut-être pas bougé.

Un millier de variations autour d'une hypothèse ne constitue pas une vérification de cette hypothèse.

Cette distinction permet de répartir les contrôles plus proprement. Les tests unitaires peuvent accompagner la production et aider l'agent à stabiliser son code. Les tests d'intégration et de qualification doivent davantage s'ancrer dans des références extérieures : données réelles anonymisées, exemples fournis par le métier, contrats d'API indépendants, propriétés définies par une autre personne ou résultats observables hors de la session du générateur.

## Un bon harness organise sa propre incomplétude

La réponse n'est pas de promettre une couverture parfaite. Cette promesse serait contradictoire : un harness parfait devrait contenir les tests correspondant à tout ce que ses concepteurs n'ont pas imaginé.

La réponse consiste à organiser l'apprentissage.

Il faut conserver les incidents, les divergences entre résultat attendu et résultat réel, les reprises humaines et les cas où un agent s'est déclaré très confiant avant d'avoir tort. Chaque surprise peut devenir un futur contrôle. Peu à peu, l'organisation construit une taxonomie empirique de ses angles morts.

Cette discipline rend le harness vivant. Elle empêche de le traiter comme un produit terminé que l'on installe une fois pour toutes.

Elle impose aussi une forme d'humilité opérationnelle. Un taux de réussite mesure ce qui a été testé, sur les distributions observées, avec les critères disponibles. Il ne mesure pas l'ensemble des manières dont le système pourrait se tromper.

Le premier piège du harness est donc de confondre la répétabilité de la validation avec son exhaustivité.

Le second est plus subtil. Puisque le générateur connait bien sa production, pourquoi ne pas lui demander de la relire lui-même ?
C'est ce que nous verrons dans le prochain article de cette série.

---

## Sources

- Calcul du parcours composé : 0,9¹⁰ ≈ 34,9 %
- Huang et al., *Large Language Models Cannot Self-Correct Reasoning Yet*, ICLR 2024, sur les limites de l'auto-correction sans signal externe · https://arxiv.org/abs/2310.01798
- Principe de taxonomie empirique des angles morts : développement original issu du manuscrit BYOAI, à valider expérimentalement ~

