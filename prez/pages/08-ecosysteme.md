---
layout: section
number: "08"
title: Écosystème MCP
---


---
layout: default
section: "08"
sectionName: "Écosystème"
slideName: "MCP Registry"
---

# Découvrir des serveurs

* **MCP Registry** : registre officiel de serveurs
  * Support de paquets PyPI, npm, Docker/OCI, NuGet et MCPB
  * Installation de paquets par la host
  * ⚠️ Modération légère - vérifier la source avant installation

<v-click>

* **Awesome MCP** : liste communautaire antérieure au registry
</v-click>

<v-click>

# Mes recommandations

* Context7
* Playwright
* TaskMaster
* Brave Search
</v-click>

---
layout: default
section: "08"
sectionName: "Écosystème"
slideName: "Roadmap"
---

# Good to know

* Quelques fonctionnalités serveur
  * Completion
  * Logging
  * Pagination

<v-click>

* Possibilité d'étendre le protocole
</v-click>

<v-click>

# À venir
</v-click>

<v-click>

* **Tasks** : exécution asynchrone
</v-click>
<v-click>

* Protocole stateless
</v-click>
<v-click>

* URLs .well-known pour découvrir les possibilités d'un serveur
</v-click>

---
layout: default
section: "08"
sectionName: "Écosystème"
slideName: "Sécurité"
---

## Authentification et configurations réseau

* Implémenter l'authentification OAuth2
* Utiliser les pratiques de sécurité standard pour les API (HTTPS, validation de jetons, etc.)
* Utiliser des SDKs officiels ou reconnus

<v-click>

## Failles de sécurité spécifiques

* Tool poisoning
>  _Injection d'un prompt malveillant dans la description d'un tool_

</v-click>
<v-click>

* Rug pulling
>  _Le serveur modifie la description d'un tool après validation du client_
</v-click>
<v-click>

* Tool shadowing
>  _Le serveur propose un tool avec une description similaire à un tool légitime_
</v-click>

<!--
https://semgrep.dev/blog/2025/a-security-engineers-guide-to-mcp/#concepts-(control-flow)
-->

---
layout: image
section: "08"
sectionName: "Écosystème"
slideName: "Comparatif"
image: /images/mcp-claude-code.png
backgroundSize: contain
---
