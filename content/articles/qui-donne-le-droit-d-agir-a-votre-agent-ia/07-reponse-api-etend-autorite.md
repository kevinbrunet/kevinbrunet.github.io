---
title: "Une réponse d'API peut ouvrir précisément l'étape suivante"
seo_title: "Autorisation d'un agent IA : étendre les droits via une API"
slug: "reponse-api-etend-autorite"
date: 2026-10-15
description: "Une API peut signer la preuve de son résultat afin d'autoriser exactement les ressources découvertes à l'étape suivante."
categories: ["Intelligence artificielle", "Sécurité", "Architecture logicielle"]
series: ["qui-donne-le-droit-d-agir-a-votre-agent-ia"]
series_order: 7
collection: "ARCHITECTURE"
cover: "/images/articles/07-reponse-api-etend-autorite.fr.png"
draft: false
---
AgentSynthèse possède au départ un droit étroit :

```text
lister les patients de la consultation de cet après-midi
```

Il ne possède aucun droit général de lecture sur les dossiers patients.

Le service de consultation répond :

```json
{
  "patients": ["P-184", "P-207", "P-311"],
  "authorization_block": "<bloc signé>"
}
```

Le premier champ est destiné au travail de l'agent. Le second est destiné aux
services suivants.

Cette réponse vient de changer ce que la tâche peut faire.

## Le service atteste ce qu'il vient de révéler

Le bloc signé peut contenir :

```datalog
listed_patient("task:7841", "P-184");
listed_patient("task:7841", "P-207");
listed_patient("task:7841", "P-311");
```

Le détenteur ajoute ce bloc au Biscuit. La spécification lie la signature du
tiers au token concerné grâce au contexte cryptographique de sa chaine. Le bloc
ne peut donc pas être déplacé librement vers n'importe quel autre Biscuit.

Lorsque l'agent appelle :

```text
GET /patients/P-184
```

le service des dossiers applique une règle équivalente à :

```datalog
allow if
  task("task:7841"),
  resource("patient:P-184"),
  listed_patient("task:7841", "P-184")
  trusting <clé-du-service-de-consultation>;
```

Le détail de syntaxe dépend de l'implémentation et du vocabulaire retenu. La
propriété importante est l'origine du fait : le service des dossiers accepte
`listed_patient` seulement lorsqu'il provient d'un bloc signé par le service de
consultation.

Si l'agent ajoute lui-même :

```datalog
listed_patient("task:7841", "P-999");
```

la policy ne lui fait pas confiance. P-999 reste inaccessible.

## Le droit ne vient pas de la donnée seule

Il serait dangereux de conclure :

> Puisque l'agent connait un identifiant patient, il peut ouvrir le dossier.

Un identifiant n'est pas une capacité. Il peut provenir d'un log, d'une ancienne
conversation ou d'une hallucination.

L'autorité apparait seulement lorsque plusieurs conditions se rencontrent :

```text
le mandat initial permet cette consultation
∩ AgentSynthèse est admis pour cette tâche
∩ le service de consultation a signé ce patient
∩ le token concerne toujours task:7841
∩ la politique du dossier accepte cette preuve
```

Nous ne remplaçons donc pas l'intersection par un "droit ajouté". Nous
ajoutons un fait de confiance à l'intersection existante.

## La réponse peut rendre un token complet ou un bloc

Deux formes d'implémentation sont possibles.

Le service peut rendre un nouveau Biscuit déjà enrichi. C'est simple pour le
client, mais le service doit recevoir et manipuler le token.

Il peut aussi rendre un *third-party block*. Le détenteur génère d'abord une
requête liée à son Biscuit. Le service signe le contenu sans avoir besoin de
connaitre tout le token, puis le détenteur ajoute le bloc reçu. C'est le flux
décrit dans la
[spécification Biscuit](https://doc.biscuitsec.org/reference/specifications).

Dans les deux cas, la réponse transporte une preuve exploitable par la suite.

## Une preuve n'accorde pas tous les droits

Le bloc signé atteste uniquement que P-184 figurait dans la consultation de cet après-midi. Cette preuve ne donne pas automatiquement accès à l'ensemble de son dossier.

Le token contient déjà un mandat précis :

```text
préparer la synthèse de la consultation de cet après-midi
```

Le service des dossiers vérifie alors que l'opération demandée reste dans les limites de ce mandat. Il peut, par exemple, accepter de renvoyer :

```text
l'identité du patient
et le résumé clinique nécessaire à la préparation de la consultation
```

mais refuser :

```text
l'historique médical complet
les documents administratifs
les données sans rapport avec cette consultation
```

L'autorisation résulte donc de la combinaison de plusieurs éléments :

```text
le token autorise la préparation de cette consultation
le service de consultation atteste que P-184 en fait partie
la demande porte sur les données prévues par ce mandat
le token est présenté au service autorisé à le recevoir
le token est encore valide
```

Les responsabilités restent séparées. Le service de consultation peut certifier quels patients sont concernés. En revanche, il ne peut pas élargir le mandat initial ni décider que l'agent peut lire tout leur dossier.

Le service des dossiers conserve la décision finale :

```text
la preuve affirme :
"P-184 fait partie de la consultation concernée"

le mandat précise :
"l'agent prépare la synthèse de cette consultation"

la policy en déduit :
"le résumé clinique de P-184 peut être renvoyé,
mais pas son dossier complet"
```

Cette séparation limite le risque de *confused deputy*. Une API disposant d'un accès étendu aux dossiers ne doit pas exercer tous ses pouvoirs à la demande de l'agent. Elle exécute uniquement l'opération permise à la fois par le mandat initial et par la preuve reçue.


## Les preuves doivent rester étroites

Une réponse de liste peut contenir beaucoup de patients. La recopier sans limite
dans un token pose des problèmes de taille, de confidentialité et de
révocation.

Imaginons que l'API renvoie une liste de 5 000 patients.
On pourrait inscrire les 5 000 identifiants dans le token, mais cela créerait trois problèmes :
- le token deviendrait très volumineux
- toute personne récupérant le token découvrirait ces identifiants
- une liste inscrite dans un token reste utilisable jusqu'à son expiration, même si elle devient incorrecte entre-temps


Selon le cas, on peut préférer :

```text
Une capacité séparée par patient : produire une autorisation distincte uniquement pour le patient que l'agent doit consulter.
Un identifiant signé de résultat matérialisé : conserver la liste côté serveur et mettre seulement dans le token un identifiant signé comme resultat:R-42.
Un prédicat sur une consultation : indiquer "patient participant à la consultation C-17", plutôt que recopier tous les patients. Le service vérifiera ensuite si P-184 appartient à C-17.
Un bloc très court avec une échéance : placer quelques identifiants dans la preuve, mais rendre celle-ci valable seulement quelques minutes.
Une référence opaque vérifiée en ligne : mettre dans le token une référence qui ne révèle rien, puis demander au serveur de vérifier cette référence au moment de l'accès.
```

Le token n'a pas vocation à devenir une base de données portable.

Il faut aussi lier la preuve à la tâche, à l'audience, à une durée et parfois au
hash exact de la requête.


Dans Biscuit, ces limites peuvent être exprimées par des faits et des checks portant, par exemple, sur le service destinataire, la ressource, l'opération et l'heure de la demande.

Le bloc signé par un tiers est également lié cryptographiquement au Biscuit pour lequel il a été produit. Il ne peut donc pas être transféré librement vers un autre token.

L'application peut ajouter deux protections distinctes.

La première consiste à réserver la preuve à un appel précis. Une empreinte est alors calculée à partir des éléments significatifs de la requête :

```text
méthode HTTP
+ service destinataire
+ route
+ paramètres
+ corps de la requête, s'il existe
```

Le service recalcule cette empreinte à la réception. Si la méthode, la route ou le contenu de la requête a changé, la preuve est refusée.

La seconde consiste à ne pas faire apparaitre l'identifiant du patient en clair dans la preuve. Le bloc peut contenir une empreinte de l'identifiant plutôt que sa valeur :

```text
patient_ref(<empreinte de "P-184">)
```

Au moment de l'accès, le service calcule l'empreinte de l'identifiant demandé et vérifie qu'elle correspond à celle contenue dans la preuve.

Si les identifiants sont courts ou prévisibles, un hash simple ne suffit pas à les dissimuler efficacement. Il est préférable d'utiliser une empreinte calculée avec une clé secrète, comme un HMAC, ou une référence opaque générée par le service.

Ces deux mécanismes sont des protections applicatives supplémentaires. Biscuit permet de transporter les faits et les checks nécessaires à leur vérification, mais ne calcule pas automatiquement ces empreintes.

## Une nouvelle manière de regarder les API

Jusqu'ici, une API recevait une autorisation et renvoyait des données.

Elle peut maintenant renvoyer :

```text
des données
+ la preuve de l'étape réalisée
+ l'autorité strictement nécessaire pour continuer
```

Cette idée permet en plus de l'accès aux ressources découvertes, d'enregistrer chaque étape passée.
Ainsi l'étape suivante attend la preuve fournit par la précédente.
Le workflow lui-même peut devenir vérifiable.

L'agent reste libre de raisonner et de choisir ses outils. Mais il ne peut plus
produire les effets dans un ordre que les services n'ont pas autorisé.

## Sources

- Eclipse Biscuit, [Specifications : third-party blocks et scopes de confiance](https://doc.biscuitsec.org/reference/specifications)
- Eclipse Biscuit, [Datalog reference : block scoping](https://doc.biscuitsec.org/reference/datalog.html)
