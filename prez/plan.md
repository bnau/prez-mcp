# MCP 
## Introduction 
* Un peu d'histoire
* Philosophie: protocôle universel. Une interface graphique qu'on peut étendre à l'infini.
## Architecture: Client / host / server
* Schéma mental de l'architecture (user -> client -> LLM -> tools) alors qu'en réalité c'est plus complexe (user -> client -> server -> client -> LLM -> client -> tools)
* Client <-> Host <-> Server
## Lifecycle, transports, API
* JSON-RPC
* Transports (stdio, Streamable HTTP, SSE)
* Présentation très très rapide des primitives
* Lifecycle (initialisation avec payload, refresh)
## features serveur (Prompts/Resources/Tools)
* Tools
* Resources
* Prompts
## Développement d'un serveur MCP
* Présentation du use case CFP
* Développement des trois features
* On utilise l'injecteur, Dev tools navigateur avec trames HTTP
## Utilisation d'un client existant (Claude Desktop)
* Claude Desktop
* Je montre les logs Ollama
## Point sur les features client (Roots/Sampling/Elicitation)
* Elicitation
* Sampling
* Roots (vite fait)
## Développement d'un client
* Présentation du use case
* Développement d'un client
## MCP registry & awesome MCP, Point sur la roadmap
* Registry, repos awesome
* Serveurs que je préconise
* Tasks
## Authentification / sécurité
* Authentification avec Oauth 
* Parenthèse, les serveurs pensés stdio ne proposent pas d'authentification, ne pas les déployer sur de l'http
* À creuser !!! [](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices)
## Final thoughts
* Bonne pratiques
* Comparatif avec les assistants de code / quelle place pour MCP