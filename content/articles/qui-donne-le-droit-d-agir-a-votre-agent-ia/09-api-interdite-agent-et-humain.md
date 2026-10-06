---
title: "Parfois, la bonne politique est : « cet agent ne peut pas appeler cette API »"
seo_title: "Sécurité API : interdire certains endpoints aux agents IA"
slug: "api-interdite-agent-humain"
date: 2026-09-03
description: "Approbation humaine déléguée et endpoint strictement humain constituent deux frontières de sécurité différentes."
categories: ["Intelligence artificielle", "Sécurité", "Architecture logicielle"]
tags: ["ai-security", "ai-risk-governance"]
series: ["qui-donne-le-droit-d-agir-a-votre-agent-ia"]
series_order: 9
collection: "ARCHITECTURE"
cover: "/images/articles/09-api-interdite-agent-et-humain.fr.png"
draft: false
---
AgentSynthèse a préparé un brouillon. Il a respecté l'ordre du workflow. Les
données proviennent des bons dossiers et chaque étape possède sa preuve.

Il reste l'action qui engage réellement le système.

Devons-nous permettre à l'agent de l'exécuter après une approbation humaine, ou
exiger que l'humain appelle lui-même l'API finale ?

Ces deux solutions sont souvent mélangées sous l'expression
*human in the loop*. Elles ne fournissent pas la même garantie.

## Premier régime : l'humain autorise, l'agent exécute

L'agent prépare une action exacte :

```json
{
  "action": "publish_summary",
  "patient": "P-184",
  "draft": "draft:991",
  "version": 3,
  "content_hash": "sha256:..."
}
```

Le service d'approbation présente ce contenu à Alice. Après sa décision, il
produit un bloc signé :

```datalog
approved(
  "alice",
  "publish_summary",
  "draft:991",
  3,
  "sha256:..."
);
```

La policy de publication fait confiance à la clé du service d'approbation.
AgentSynthèse peut ensuite appeler l'API, mais uniquement pour l'action, la
version et le contenu réellement approuvés.

Si l'agent modifie le texte après le clic, le hash ne correspond plus. S'il
change de patient, la preuve ne correspond plus. S'il attend trop longtemps,
l'attestation peut expirer.

Dans ce régime, l'humain prend la décision et l'agent effectue l'appel
technique.

## Deuxième régime : l'API est humain-only

Pour certaines actions, l'organisation peut vouloir une frontière plus dure :

```text
acteur direct = agent  → refus
acteur direct = humain authentifié → évaluation de la policy
```

L'agent peut préparer les informations, expliquer le choix et ouvrir le bon
écran. Il ne reçoit jamais la capacité d'exécuter l'acte final.

La policy pourrait exprimer :

```datalog
deny if
  operation("finalize_clinical_decision"),
  actor_type("agent");

allow if
  operation("finalize_clinical_decision"),
  actor_type("human"),
  recent_user_verification(true);
```

Ici, aucune attestation d'approbation ne transforme AgentSynthèse en humain.
Alice doit effectuer un nouvel acte authentifié.

Cette distinction évite un tour de passe-passe fréquent : conserver l'agent
comme acteur réel tout en écrivant dans le journal que "l'humain a validé".

## Une policy manquante n'est pas un refus définitif

Quand l'agent tente une action soumise à approbation, le service peut répondre :

```json
{
  "error": "human_approval_required",
  "action_hash": "sha256:...",
  "approval_service": "/human-approvals",
  "required_approver_role": "clinician",
  "expires_in": 300
}
```

Le refus guide l'agent vers le seul chemin capable de produire la preuve
manquante.

Le service d'approbation ne lui remet pas une permission générale
`summary.publish`. Il fournit une attestation étroite sur une action figée.

On retrouve encore le principe de la réponse qui ouvre l'étape suivante :

```text
API finale refuse
        ↓
l'agent sollicite le service humain
        ↓
l'humain examine une action exacte
        ↓
le service rend une preuve signée
        ↓
la même action devient autorisable
```

## Le clic humain n'est pas une preuve magique

Une session déjà ouverte peut être pilotée par un agent. Un bouton "Valider"
cliqué systématiquement ne constitue pas une supervision effective.

Pour une action sensible, le service peut exiger une authentification récente,
une vérification de l'utilisateur ou une preuve de présence. Le standard
[WebAuthn du W3C](https://www.w3.org/TR/webauthn-3/) distingue notamment les
notions de présence et de vérification de l'utilisateur. Leur utilisation ne
prouve pas que la décision humaine était pertinente, mais elle renforce
l'attribution de l'acte.

La conception de l'écran compte aussi. L'humain doit voir l'effet exact,
l'origine des données, les modifications proposées et les incertitudes utiles.
Une approbation générique sur une tâche encore modifiable ne protège rien.

## La réglementation ne choisit pas votre protocole

L'[article 14 du règlement européen sur l'IA](https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX%3A32024R1689)
exige, pour les systèmes à haut risque auxquels il s'applique, des mesures
permettant une supervision effective par des personnes physiques,
proportionnées aux risques, au niveau d'autonomie et au contexte.

Un bloc Biscuit, une passkey ou un endpoint humain-only ne suffisent pas à
établir cette conformité. Ces mécanismes peuvent toutefois matérialiser une
frontière décidée par l'organisation et produire des traces plus solides qu'une
simple consigne : "l'IA prépare, l'humain valide".

Dans un contexte médical, la politique doit aussi s'inscrire dans le cadre
applicable au dispositif, à son usage prévu et au processus clinique. La
technique ne décide pas à la place de l'analyse de risques.

## Trois régimes plutôt qu'un interrupteur

Toutes les API n'ont pas besoin de la même frontière.

```text
1. humain ou agent
   lectures et calculs à faible impact

2. agent sous délégation et éventuellement sous approbation
   écritures réversibles ou actions précisément bornées

3. humain uniquement
   décision ou acte que l'organisation refuse de déléguer
```

Ce classement n'est pas un simple attribut de l'agent. Il appartient à chaque
opération.

Le même AgentSynthèse peut lire un document, enregistrer un brouillon après
intersection des policies, publier une version après approbation, et être
formellement refusé sur une décision clinique finale.

Nous sommes loin du JWT d'Alice donné au modèle. L'article final assemblera le
trajet complet et montrera ce que cette architecture résout réellement, ainsi
que ce qu'elle laisse intact.

## Sources

- Union européenne, [Règlement (UE) 2024/1689, article 14 : contrôle humain](https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX%3A32024R1689)
- W3C, [Web Authentication: An API for accessing Public Key Credentials, Level 3](https://www.w3.org/TR/webauthn-3/), utilisé pour les notions de présence et de vérification de l'utilisateur
- Eclipse Biscuit, [Specifications : third-party blocks](https://doc.biscuitsec.org/reference/specifications)
