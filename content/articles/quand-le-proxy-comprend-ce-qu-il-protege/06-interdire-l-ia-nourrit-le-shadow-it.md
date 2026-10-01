---
title: "Interdire l’IA nourrit le shadow IT"
slug: "proxy-ia-shadow-it-chemin-officiel"
date: 2026-10-01
description: "Un chemin officiel utile et explicable aide à limiter les contournements. Le proxy d’API ne couvre toutefois que les usages qui le traversent."
categories: ["Intelligence artificielle", "Cybersécurité", "Architecture logicielle"]
series: ["quand-le-proxy-comprend-ce-qu-il-protege"]
series_order: 6
collection: "SYSTÈMES"
cover: "/images/articles/shieldstral/06.png"
draft: false
---

{{< callout variant="scene" label="Point de départ" >}}
Nora veut résumer un dossier avant sa réunion. L’outil officiel bloque le modèle qu’elle avait choisi et affiche seulement : « Cette requête enfreint la politique de sécurité. »
{{< /callout >}}

Elle peut renoncer. Elle peut aussi ouvrir un service grand public depuis son navigateur personnel et y déposer le document, ou le photographier avec son smartphone avant d'envoyer l'image depuis un compte personnel.

Le second trajet est beaucoup plus dangereux que le premier. Pourtant, c’est parfois l’interdiction elle-même qui l’a rendu probable.

Une politique de sécurité qui ignore le besoin de travailler ne supprime pas ce besoin. Elle le déplace vers le shadow IT.

## Le shadow IT vient rarement d’une intention malveillante

Le [National Cyber Security Centre britannique](https://www.ncsc.gov.uk/guidance/shadow-it) définit le shadow IT comme l’ensemble des actifs utilisés professionnellement sans être connus ni alignés avec les processus de l’organisation. Sa définition inclut explicitement les technologies d’IA utilisées sans autorisation, souvent appelées shadow AI.

Le NCSC insiste sur un point essentiel : ces usages résultent rarement d’une volonté de contourner la sécurité pour nuire. Les salariés essaient généralement de terminer leur travail avec des outils officiels trop lents, incomplets ou inadaptés. Ils peuvent également ne pas comprendre le risque créé par un service personnel.

Le cas de Nora correspond exactement à ce mécanisme. Elle ne cherche pas à exfiltrer une procédure industrielle. Elle cherche un résumé avant une réunion. Si l’entreprise lui donne seulement une interdiction, un besoin légitime reste sans solution.

Bloquer l’accès à quelques domaines ne règle pas durablement le problème. Les services changent, les modèles s’intègrent dans les logiciels existants et un téléphone personnel suffit parfois à contourner le système d’information.

## Le proxy doit conserver un chemin praticable

L’architecture décrite dans cette série protège la frontière sans réduire chaque incident à un refus.

Le proxy IA centralise les destinations. Un moteur spécialisé pseudonymise les données reconnaissables. Shieldstral compare le sens du contenu à la politique métier. Le découpage aide à isoler les passages sensibles. Une réponse synthétique permet enfin de présenter à Nora les chemins encore autorisés sans appeler le modèle demandé.

Le message devient :

> Ce document contient une procédure industrielle interne. Le modèle externe demandé ne peut pas recevoir sa version complète. Vous pouvez pseudonymiser les passages concernés, utiliser le modèle local ou annuler.

Le POC étendu a signalé les 9 contenus sensibles et autorisé les 5 contenus non sensibles. Il a produit une décision de destination locale pour un secret sans forme déterministe et expurgé trois cas avant recontrôle. La décision médiane prenait 20 ms, avec un 95e percentile à 44 ms ; le recontrôle ajoutait de 17 à 20 ms. Ces mesures sur des documents courts ne couvrent ni la génération d’un résumé ni la boucle interactive décrite ici.

La sécurité demeure ferme sur la destination interdite. Elle devient souple sur la manière de réaliser le travail.

Cette différence est décisive. Nora ne doit pas connaître la localisation des datacenters, les clauses contractuelles de chaque fournisseur ou la taxonomie de Shieldstral. Le système traduit ces contraintes en options compréhensibles et utilisables.

## Le proxy d’API protège les usages qui le traversent

Une requête envoyée depuis un compte personnel ou un autre chemin échappe à ce point de contrôle. La protection des usages web demande des mesures complémentaires et un accompagnement des utilisateurs.

Un routage local ne constitue pas non plus un consentement utilisateur. LiteLLM propose déjà un routage des données sensibles fondé sur des motifs ; Shieldstral ajoute ici le signal sémantique étudié. Après un tour local, l’historique peut encore contenir le secret. Les tours suivants doivent être recontrôlés et la destination autorisée conservée tant que ce contexte subsiste.

## Une explication vaut mieux qu’un code d’erreur

Chaque intervention du proxy peut devenir un moment de sensibilisation. Nora apprend qu’un IBAN est pseudonymisé, qu’une procédure métier ne se détecte pas comme un numéro de carte et qu’un modèle local peut recevoir un document refusé par une destination externe.

Elle voit aussi les conséquences de son choix. La pseudonymisation peut dégrader un résumé si le passage remplacé était nécessaire. Le modèle local protège davantage le document, mais peut fournir une expérience différente. L’annulation reste possible.

Cette pédagogie ne doit pas prendre la forme d’un cours obligatoire à chaque requête. Une explication courte, placée au moment de la décision, relie directement le risque à l’action. Elle donne à l’utilisateur un modèle mental qu’il pourra réutiliser la fois suivante.

Le proxy ne se contente plus d’appliquer la politique. Il la rend visible et intelligible.

## Les blocages deviennent une source d’amélioration

Les choix de Nora produisent également une information précieuse pour l’entreprise. Si de nombreux utilisateurs redirigent la même tâche vers le modèle local, l’outil externe n’est peut-être pas adapté à ce métier. Si tous refusent une pseudonymisation proposée, la segmentation retire peut-être trop de contexte. Si une équipe rencontre sans cesse la même règle, la politique est peut-être mal expliquée ou trop large.

Ces traces doivent être agrégées sans transformer la sécurité en surveillance individuelle. Elles permettent d’améliorer les modèles locaux, de préciser les politiques et d’ajouter des chemins officiels là où les besoins réels apparaissent.

Le NCSC recommande justement d’éviter les verrouillages inutiles, de traiter rapidement les demandes des utilisateurs et de développer une culture dans laquelle les problèmes peuvent être remontés sans crainte de sanction. Une mauvaise culture rend le shadow IT moins visible, donc plus difficile à sécuriser.

## L’utilisateur éclairé est une ligne de défense

Dire que la meilleure sécurité repose sur un utilisateur formé ne signifie pas lui transférer toute la responsabilité. Nora ne remplacera jamais les contrôles d’accès, le chiffrement, le proxy ou les interdictions structurelles. Même un utilisateur expérimenté peut se tromper sous pression.

La bonne architecture associe les deux formes de protection. Les contrôles techniques empêchent les trajets interdits. L’explication aide l’utilisateur à comprendre le risque et à choisir correctement parmi les trajets permis.

Cette combinaison fait évoluer les mentalités. La cybersécurité cesse d’apparaître comme le service qui empêche de travailler. Elle devient le système qui permet de travailler avec l’IA sans abandonner la maîtrise des données.

La conclusion de la série tient dans cette idée : pour combattre le shadow AI, l’entreprise doit offrir mieux qu’une interdiction. Elle doit proposer un chemin sûr, expliquer ses décisions et écouter les besoins que les contournements révèlent.

Un utilisateur éclairé constitue alors une défense supplémentaire. Pas parce qu’on lui fait aveuglément confiance, mais parce qu’on lui donne les informations, les outils et les choix nécessaires pour agir en connaissance de cause.

Cette expérience repose cependant sur une décision invisible pour Nora : la manière dont la politique a été écrite. Lors de ma première exécution, deux contenus sensibles sur six n’ont pas été signalés. Le dernier article ouvre le POC pour comprendre comment le même modèle est passé de 67 % à 100 % de rappel sans augmenter les faux positifs observés.

---

{{< closing-question label="À retenir" >}}
Un contrôle utile protège la frontière et conserve un chemin de travail. L’explication renforce les protections techniques.
{{< /closing-question >}}

## Sources

- [Rapport de qualification Shieldstral — 2 septembre 2026](/documents/shieldstral-qualification-2026-09-02.md)
- [NCSC — Shadow IT](https://www.ncsc.gov.uk/guidance/shadow-it)
- [NCSC — Using SaaS securely](https://www.ncsc.gov.uk/collection/cloud/using-cloud-services-securely/using-saas-securely)
- [ANSSI — Recommandations de sécurité pour un système d’IA générative](https://messervices.cyber.gouv.fr/guides/recommandations-de-securite-pour-un-systeme-dia-generative)
- [LiteLLM — Sensitive Data Routing](https://docs.litellm.ai/docs/proxy/guardrails/sensitive_data_routing)

**Pour continuer :** [Avec le même modèle, le rappel est passé de 67 % à 100 %](/articles/shieldstral-politique-rappel-qualification/).
