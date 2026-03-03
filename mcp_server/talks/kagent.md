# KAgent + KServe: Le combo parfait pour industrialiser ses propres agents IA

Exécuter son propre agent en local, facile : Internet regorge de ressources pour apprendre. Mais dès qu'il s'agit d'industrialiser, les choses se compliquent, surtout si on souhaite s'affranchir de services managés ! Dans ce talk, je vous présenterai deux outils présents dans le paysage CNCF qui répondent à cette problématique: KAgent et KServe.

KAgent permet de développer et déployer des agents IA avec une approche déclarative. Il suffit d’écrire quelques spécifications (system prompts, modèle d'inférence et tools supplémentaires) pour obtenir un agent fonctionnel. La magie s’opère en exploitant deux protocoles répandus: MCP et A2A.

KServe est utile pour héberger des modèles d’inférence sur son propre cluster Kubernetes. En plus de déployer des modèles, il propose des features intéressantes comme de l’auto-scaling, du contrôle d’accès ou une intégration native avec les APIs d’OpenAI.

Nous utiliserons ensemble les deux outils pour déployer et exécuter des agents IA avec une approche Cloud Native en partant d'un simple cluster Kubernetes. Vous repartirez avec une solution complète pour développer et déployer facilement vos propres agents, sans même avoir besoin d’être un expert en IA générative.

## Références

Le talk aura la structure suivante:

* Exécution d'un mini agent en local et présentation de la problématique. Ça permettra d'introduire MCP et A2A
* Présentation de KAgent. Déploiement du même agent sur un cluster k8s avec KAgent.
* Présentation de KServe. Passage d'une inférence managée vers une inférence on premise avec Kserve.

Le mini-projet consistera à consulter les CFP ouverts des confs techs selon des critères fournis dans le prompt.