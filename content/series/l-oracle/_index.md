---
title: "L'oracle"
seo_title: "Oracles et routage des modèles pour les agents IA"
description: "Quatre articles sur les tentatives vérifiées, la complémentarité des modèles, la fiabilité de l'oracle et la méthode de qualification d'un routage agentique."
weight: 5
---

Cette série montre comment un oracle transforme la génération en boucle de recherche, puis permet de router les échecs vers les modèles qui les récupèrent le mieux dans les résultats observés.

Le premier article étudie la valeur des tentatives vérifiées. Le second montre pourquoi le meilleur modèle d'un classement n'est pas forcément celui qui complète le mieux le précédent. Le troisième examine la fiabilité de l'oracle : bugs du grader, faux positifs et budget d'essais acceptable.

Le quatrième donne une méthode de mise en œuvre : définir les conditions de livraison, constituer les cas, construire l'oracle, mesurer la complémentarité des modèles, qualifier la chaîne et la déployer progressivement.
