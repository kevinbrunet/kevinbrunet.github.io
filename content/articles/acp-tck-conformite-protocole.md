---
title: "Avec son TCK, ACP se donne les moyens de devenir fiable"
seo_title: "ACP TCK : un pas vers des implémentations fiables, comme A2A"
slug: "acp-tck-conformite-protocole"
date: 2026-11-09
description: "Comme A2A, ACP se dote d'un kit de tests de conformité. Une étape pour fiabiliser les implémentations et rendre sa promesse d'interopérabilité plus solide."
categories: ["Intelligence artificielle", "Architecture logicielle"]
tags: ["agent-protocols", "ai-evaluation-evals"]
collection: "ARCHITECTURE"
cover: "/images/articles/acp-tck-conformite.fr.png"
draft: false
---

{{< callout variant="scene" label="Point de départ" >}}
ACP se dote d'un [Test Compatibility Kit](https://github.com/agentclientprotocol/acp-tck), une suite de tests pour vérifier les implémentations du protocole. [A2A dispose déjà d'un outil de ce type](https://github.com/a2aproject/a2a-tck). C'est une étape importante pour un écosystème qui promet de faire fonctionner ensemble des composants développés par des équipes différentes.
{{< /callout >}}

Dans la série [ACP, l'interface manquante des agents]({{< relref "/series/acp-interface-manquante-des-agents" >}}), nous avons exploré cette promesse : conserver son interface tout en changeant l'agent qui travaille derrière elle. Avec un outil commun pour tester le respect du contrat, ACP se donne davantage de moyens de la tenir.

{{< thesis >}}
La confiance dans un protocole se construit aussi dans les outils qui permettent de vérifier ses implémentations.
{{< /thesis >}}

## Un contrat commun doit produire des comportements communs

Deux équipes peuvent lire la même spécification et en tirer des comportements différents. Tant que l'utilisateur envoie une demande simple, tout fonctionne. Les écarts apparaissent lorsqu'il faut interrompre une tâche, reprendre une session ou gérer une erreur.

Pour l'utilisateur, ces écarts deviennent une interface qui reste bloquée ou une conversation impossible à reprendre. Pour l'entreprise, ils deviennent des intégrations à corriger et des changements de composants plus risqués que prévu.

Une spécification décrit les règles. Un kit de conformité permet de confronter une implémentation à des scénarios partagés. Les équipes disposent ainsi d'un moyen commun de repérer les écarts et de prévenir leur retour lors des mises à jour.

## Comme A2A, ACP outille sa promesse d'interopérabilité

A2A possède son *Technology Compatibility Kit* pour tester les implémentations de son protocole. ACP adopte la même démarche sur une autre frontière : la relation entre le client et l'agent.

Son TCK lance un agent et exerce des échanges comme l'initialisation, les sessions, les demandes, l'annulation et la gestion des erreurs. Il produit un rapport qui distingue les exigences réussies, échouées ou non vérifiées.

L'apport dépasse le diagnostic d'un bug. Un développeur peut vérifier son agent avant une livraison. Une équipe d'intégration peut demander des résultats de tests plutôt que se contenter d'une déclaration de compatibilité. Une régression peut être détectée avant d'atteindre les utilisateurs.

C'est ainsi qu'un protocole gagne en crédibilité : chaque implémentation peut être confrontée à des attentes communes, au lieu de dépendre uniquement des essais réalisés avec quelques partenaires.

## Une raison supplémentaire de miser sur ACP

Pour une entreprise, l'intérêt d'ACP tient au choix qu'il ouvre. L'interface et l'agent peuvent évoluer séparément. Une équipe peut améliorer son harness, essayer un autre agent ou proposer une nouvelle interface sans reconstruire systématiquement toute l'intégration.

Le TCK renforce les conditions de cette liberté. Plus les écarts sont détectés tôt, plus il devient réaliste de remplacer un composant en conservant le reste du système.

Le kit est encore expérimental, mais il apporte déjà une base commune pour vérifier les implémentations et détecter les régressions. C'est une étape de maturité pour l'écosystème ACP.

{{< closing-question label="À retenir" >}}
Avec son TCK, ACP franchit une étape vers un protocole sur lequel on pourra compter. Sa promesse d'ouverture s'accompagne désormais d'un outil pour en vérifier la mise en œuvre.
{{< /closing-question >}}

---

## Sources

- Agent Client Protocol, [ACP TCK : kit de tests de conformité](https://github.com/agentclientprotocol/acp-tck).
- Agent2Agent Project, [A2A Technology Compatibility Kit](https://github.com/a2aproject/a2a-tck).
