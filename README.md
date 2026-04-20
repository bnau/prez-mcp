# MCP en pratique : une application pour tout comprendre

## Merci !!

Au projet [Developers Events](https://developers.events/) sur lequel la démo repose et à [Aurélie](https://github.com/scraly) pour tout le travail qu'elle y fait.

> **Note** : Ce code est volontairement pensé pour être le plus simple possible, compréhensible rapidement et éviter les effets démo. Certaines parties non présentées pendant la présentation ont été écrites le plus vite possible pour que je puisse me concentrer sur le code qui sera montré.

---

## Prérequis

Vous avez besoin de :
- **Python** et **uv**
- **mise** ([installation](https://mise.jdx.dev/getting-started.html))
- Un **abonnement GitHub Copilot** (pour le LLM proxy utilisé dans les démos)

---

## Installation

```bash
# Installer les dépendances et outils
mise install

# Synchroniser les dépendances Python
uv sync --dev
```

---

## Lancer les slides

```bash
mise run slides
```

Ouvrez ensuite votre navigateur à l'adresse affichée (généralement http://localhost:3000).

---

## Lancer les démos

### Démo 1 : Les bases de MCP

```bash
# Lancer le serveur MCP (port 8000)
mise run server_demo1

# Dans un autre terminal : inspecter le serveur avec MCP Inspector
mise run inspect_demo1
```

### Démo 2 : Fonctionnalités avancées (Context, Sampling, Elicitation)

```bash
# Lancer le serveur MCP (port 8001)
mise run server_demo2

# Dans un autre terminal : inspecter le serveur avec MCP Inspector
mise run inspect_demo2
```

### Client de test

```bash
# Lancer le client Python pour tester les serveurs
mise run run_client
```

---

## Structure du projet

```
mcp_server/
├── server_demo1.py    # Démo 1 : Tools, Prompts, Resources
├── server_demo2.py    # Démo 2 : Context, Sampling, Elicitation
└── talks/             # Talks exposés comme resources

mcp_client/
└── client.py          # Client de test

prez/
└── slides.md          # Slides de la conférence
```

---

**Merci d'avoir assisté à la conférence ! 🎉**
