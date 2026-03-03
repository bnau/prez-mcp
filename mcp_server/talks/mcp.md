# MCP en pratique : une application pour tout comprendre

Model Context Protocol, le célèbre protocole développé par Anthropic, est sorti en 2024 et s’est rapidement imposé dans le monde des IA génératives. Conçu pour interconnecter des LLM et des systèmes externes, MCP ouvre la voie à des intégrations puissantes : appels d’API web, accès à des sources de connaissance privées, ou encore déclenchement d’autres IA !

La première utilisation de MCP est excessivement simple : on lance un serveur, on configure un client, et hop, ça marche ! Cependant, une mécanique riche se cache derrière cette simplicité apparente et il est essentiel de la comprendre pour l’intégrer dans ses projets.

Ce sera l’enjeu de ce talk. Je vous propose de plonger dans les entrailles de MCP. Nous développerons ensemble une petite application en Python, ce qui nous permettra de passer en revue les différentes fonctionnalités du protocole, d’observer les interactions entre les différentes briques et d’avoir une bonne connaissance de son écosystème.

À la fin de cette session, vous partirez avec toutes les clés pour intégrer MCP dans vos projets en production.

## Références

Le plan sera le suivant:

* Introduction rapide du sujet et de l'enjeu de MCP
* Architecture : Client / host / server
* Présentation du Lifecycle / les modes de transports / les APIs essentielles.
* Développement d'un serveur + MCP inspector
* Point sur les features serveur (Prompts/Resources/Tools)
* Utilisation d'un client existant (Claude Desktop)
* Développement d'un client
* Point sur les features client (Roots/Sampling/Elicitation)
* Authentification / sécurité
* MCP registry & awesome MCP, Point sur la roadmap