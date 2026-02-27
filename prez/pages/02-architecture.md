---
layout: section
number: "02"
title: Architecture
---


---
layout: default
section: "02"
sectionName: "Architecture"
slideName: "Schéma mental vs réalité"
---

# Ce qu'on imagine

<div style="position: relative; height: 400px; display: flex; align-items: center; justify-content: center;">

<div v-click.hide style="position: absolute; width: 100%; text-align: center;">

```mermaid
%%{init: {'themeVariables': { 'edgeLabelBackground': 'white'}}}%%
graph LR
    User[👤 User] -->|1. Requête| Client[💻 Client]
    Client -->|2. Demande| LLM[🤖 LLM]
    LLM -->|3. Réponse| Tools[🔧 Tools]

    style User fill:#e1f5ff
    style Client fill:#fff4e6
    style LLM fill:#f3e5f5
    style Tools fill:#e8f5e9

    linkStyle 0 stroke:white,color:white
    linkStyle 1 stroke:white,color:white
    linkStyle 2 stroke:white,color:white
```

</div>

<div v-click="[1,2]" style="position: absolute; width: 100%; text-align: center;">

```mermaid
%%{init: {'themeVariables': { 'edgeLabelBackground': 'white'}}}%%
graph LR
    User[👤 User] -->|1. Requête| Client[💻 Client]
    Client -->|2. Demande| LLM[🤖 LLM]
    LLM -->|3. Réponse| Tools[🔧 Tools]

    style User fill:#e1f5ff
    style Client fill:#fff4e6
    style LLM fill:#f3e5f5
    style Tools fill:#e8f5e9

    linkStyle 1 stroke:white,color:white
    linkStyle 2 stroke:white,color:white
```

</div>

<div v-click="[2,3]" style="position: absolute; width: 100%; text-align: center;">

```mermaid
%%{init: {'themeVariables': { 'edgeLabelBackground': 'white'}}}%%
graph LR
    User[👤 User] -->|1. Requête| Client[💻 Client]
    Client -->|2. Demande| LLM[🤖 LLM]
    LLM -->|3. Réponse| Tools[🔧 Tools]

    style User fill:#e1f5ff
    style Client fill:#fff4e6
    style LLM fill:#f3e5f5
    style Tools fill:#e8f5e9

    linkStyle 2 stroke:white,color:white
```

</div>

<div v-click=3 style="position: absolute; width: 100%; text-align: center;">

```mermaid
%%{init: {'themeVariables': { 'edgeLabelBackground': 'white'}}}%%
graph LR
    User[👤 User] -->|1. Requête| Client[💻 Client]
    Client -->|2. Demande| LLM[🤖 LLM]
    LLM -->|3. Réponse| Tools[🔧 Tools]

    style User fill:#e1f5ff
    style Client fill:#fff4e6
    style LLM fill:#f3e5f5
    style Tools fill:#e8f5e9
```

</div>

</div>

---
layout: default
section: "02"
sectionName: "Architecture"
slideName: "La réalité"
---

# Ce qui se passe vraiment

<div style="position: relative; height: 400px; display: flex; align-items: center; justify-content: center;">

<div v-click.hide style="position: absolute; width: 100%; text-align: center;">

```mermaid
%%{init: {'themeVariables': { 'edgeLabelBackground': 'white'}}}%%
graph LR
    User[👤 User] -->|1. Requête| Client[💻 Client]
    Client -->|2. Appel tool| Tool[🔧 Tool]
    Tool -->|3. Résultat| Client
    Client -->|4. Contexte| LLM[🤖 LLM]
    LLM -->|5. Réponse| Client
    Client -->|6. Autre tool| Tool

    style User fill:#e1f5ff
    style Client fill:#fff4e6
    style Tool fill:#e8f5e9
    style LLM fill:#f3e5f5

    linkStyle 0 stroke:white,color:white
    linkStyle 1 stroke:white,color:white
    linkStyle 2 stroke:white,color:white
    linkStyle 3 stroke:white,color:white
    linkStyle 4 stroke:white,color:white
    linkStyle 5 stroke:white,color:white
```

</div>

<div v-click="[1,2]" style="position: absolute; width: 100%; text-align: center;">

```mermaid
%%{init: {'themeVariables': { 'edgeLabelBackground': 'white'}}}%%
graph LR
    User[👤 User] -->|1. Requête| Client[💻 Client]
    Client -->|2. Appel tool| Tool[🔧 Tool]
    Tool -->|3. Résultat| Client
    Client -->|4. Contexte| LLM[🤖 LLM]
    LLM -->|5. Réponse| Client
    Client -->|6. Autre tool| Tool

    style User fill:#e1f5ff
    style Client fill:#fff4e6
    style Tool fill:#e8f5e9
    style LLM fill:#f3e5f5

    linkStyle 1 stroke:white,color:white
    linkStyle 2 stroke:white,color:white
    linkStyle 3 stroke:white,color:white
    linkStyle 4 stroke:white,color:white
    linkStyle 5 stroke:white,color:white
```

</div>

<div v-click="[2,3]" style="position: absolute; width: 100%; text-align: center;">

```mermaid
%%{init: {'themeVariables': { 'edgeLabelBackground': 'white'}}}%%
graph LR
    User[👤 User] -->|1. Requête| Client[💻 Client]
    Client -->|2. Appel tool| Tool[🔧 Tool]
    Tool -->|3. Résultat| Client
    Client -->|4. Contexte| LLM[🤖 LLM]
    LLM -->|5. Réponse| Client
    Client -->|6. Autre tool| Tool

    style User fill:#e1f5ff
    style Client fill:#fff4e6
    style Tool fill:#e8f5e9
    style LLM fill:#f3e5f5

    linkStyle 2 stroke:white,color:white
    linkStyle 3 stroke:white,color:white
    linkStyle 4 stroke:white,color:white
    linkStyle 5 stroke:white,color:white
```

</div>

<div v-click="[3,4]" style="position: absolute; width: 100%; text-align: center;">

```mermaid
%%{init: {'themeVariables': { 'edgeLabelBackground': 'white'}}}%%
graph LR
    User[👤 User] -->|1. Requête| Client[💻 Client]
    Client -->|2. Appel tool| Tool[🔧 Tool]
    Tool -->|3. Résultat| Client
    Client -->|4. Contexte| LLM[🤖 LLM]
    LLM -->|5. Réponse| Client
    Client -->|6. Autre tool| Tool

    style User fill:#e1f5ff
    style Client fill:#fff4e6
    style Tool fill:#e8f5e9
    style LLM fill:#f3e5f5

    linkStyle 3 stroke:white,color:white
    linkStyle 4 stroke:white,color:white
    linkStyle 5 stroke:white,color:white
```

</div>

<div v-click="[4,5]" style="position: absolute; width: 100%; text-align: center;">

```mermaid
%%{init: {'themeVariables': { 'edgeLabelBackground': 'white'}}}%%
graph LR
    User[👤 User] -->|1. Requête| Client[💻 Client]
    Client -->|2. Appel tool| Tool[🔧 Tool]
    Tool -->|3. Résultat| Client
    Client -->|4. Contexte| LLM[🤖 LLM]
    LLM -->|5. Réponse| Client
    Client -->|6. Autre tool| Tool

    style User fill:#e1f5ff
    style Client fill:#fff4e6
    style Tool fill:#e8f5e9
    style LLM fill:#f3e5f5

    linkStyle 4 stroke:white,color:white
    linkStyle 5 stroke:white,color:white
```

</div>

<div v-click="[5,6]" style="position: absolute; width: 100%; text-align: center;">

```mermaid
%%{init: {'themeVariables': { 'edgeLabelBackground': 'white'}}}%%
graph LR
    User[👤 User] -->|1. Requête| Client[💻 Client]
    Client -->|2. Appel tool| Tool[🔧 Tool]
    Tool -->|3. Résultat| Client
    Client -->|4. Contexte| LLM[🤖 LLM]
    LLM -->|5. Réponse| Client
    Client -->|6. Autre tool| Tool

    style User fill:#e1f5ff
    style Client fill:#fff4e6
    style Tool fill:#e8f5e9
    style LLM fill:#f3e5f5

    linkStyle 5 stroke:white,color:white
```

</div>

<div v-click=6 style="position: absolute; width: 100%; text-align: center;">

```mermaid
%%{init: {'themeVariables': { 'edgeLabelBackground': 'white'}}}%%
graph LR
    User[👤 User] -->|1. Requête| Client[💻 Client]
    Client -->|2. Appel tool| Tool[🔧 Tool]
    Tool -->|3. Résultat| Client
    Client -->|4. Contexte| LLM[🤖 LLM]
    LLM -->|5. Réponse| Client
    Client -->|6. Autre tool| Tool

    style User fill:#e1f5ff
    style Client fill:#fff4e6
    style Tool fill:#e8f5e9
    style LLM fill:#f3e5f5
```

</div>

</div>

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
**Unique composant d'interface**

* IDE / Interface de chat / Assistant de code...
* Accède à un LLM

</div>

<div>

### 💻 Client

**Interagit avec le serveur**

- 1 client par serveur
- Maintient la connexion
- 1 ou plusieurs clients par host

</div>

<div>

### 🔧 Serveur

**Fournit du contexte au client**

- Accède à des ressources externes (file system, bases de données, APIs...)

</div>

</div>

<div class="mt-8 text-sm text-gray-500">

**Exemple** : VS Code (Host) → instancie un Client → se connecte au Serveur filesystem

</div>
