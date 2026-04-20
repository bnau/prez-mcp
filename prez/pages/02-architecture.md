---
layout: section
number: "02"
title: Architecture
---


---
layout: default
section: "02"
sectionName: "Architecture"
slideName: "Client / Host / Server"
---

# Les trois acteurs

<div class="grid grid-cols-3 gap-4 mt-8">

<div>

### 🏠 Host
**Application**

* IDE / Interface de chat / Assistant de code...
* Accède à un LLM

</div>

<div v-click>

### 💻 Client

**Interagit avec le serveur**

- 1 client par serveur
- Maintient la connexion
- 1 ou plusieurs clients par host

</div>

<div v-click>

### 🔧 Serveur

**Fournit du contexte au client**

- Accède à des ressources externes (file system, bases de données, APIs...)

</div>

</div>
