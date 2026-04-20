---
layout: section
number: "08"
title: Good to know
---


---
layout: default
section: "08"
sectionName: "Good to know"
slideName: "MCP Registry"
---

# Écosystème

* **MCP Registry** : registre officiel de serveurs
  * Support de paquets PyPI, npm, Docker/OCI...
  * https://registry.modelcontextprotocol.io/
  * ⚠️ Géré par la communauté - vérifier la pertinence avant installation

* **Awesome MCP** : liste communautaire antérieure au registry

<v-click>

# Quelques serveurs intéressants

* Context7
* Playwright
* Brave Search
</v-click>

---
layout: default
section: "08"
sectionName: "Good to know"
slideName: "Roadmap"
---

# Good to know

* Quelques fonctionnalités supplémentaires: Completion, Logging, Pagination
* Possibilité d'ajouter des extensions
  * MCP Apps
  * Extensions d'Authorisation
<v-click>

# À venir

* **Tasks** : exécution asynchrone

* Protocole stateless

* URLs .well-known
</v-click>

---
layout: two-cols
section: "08"
sectionName: "Good to know"
slideName: "Bonnes pratiques et sécurité"
---

## Bonnes pratiques

* Descriptions des tools claires et précises
* Limiter le nombre de tools exposés
* Un tool par intention, pas par endpoint REST
* ⚠️ Les données sensibles ne doivent pas être exposées

::right::

<v-click>

## Failles de sécurité

* Tool poisoning
>  _Injection d'un prompt malveillant dans la description d'un tool_

* Rug pulling
>  _Le serveur modifie la description d'un tool après validation du client_

* Tool shadowing
>  _Le serveur propose un tool avec une description similaire à un tool légitime_
</v-click>

## Solutions

---
layout: image
section: "08"
sectionName: "Good to know"
slideName: "Comparatif"
image: /images/mcp-claude-code.png
backgroundSize: contain
---
