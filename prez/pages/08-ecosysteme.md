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
* **Awesome MCP** : liste communautaire antérieure au registry


---
layout: default
section: "08"
sectionName: "Écosystème"
slideName: "Serveurs recommandés"
---

# Mes recommandations

* Context7
* Playwright
* TaskMaster
* Brave Search

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
* Possibilité d'étendre le protocole

# À venir

* **Tasks** : exécution asynchrone
* Protocole stateless
* URLs .well-known pour découvrir les possibilités d'un serveur
* Extensions officielles

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

## Failles de sécurité spécifiques

* Tool poisoning
>  _Injection d'un prompt malveillant dans la description d'un tool_

* Rug pulling
>  _Le serveur modifie la description d'un tool après validation du client_
* Tool shadowing
>  _Le serveur propose un tool avec une description similaire à un tool légitime_

<!--
https://semgrep.dev/blog/2025/a-security-engineers-guide-to-mcp/#concepts-(control-flow)
-->