---
layout: section
number: "06"
title: Features client
---


---
layout: section-with-header
title: Sampling
subtitle: Le serveur demande au client d'utiliser son API d'inférence
section: "06"
sectionName: "Features client"
slideName: "Sampling"
---


---
layout: default
section: "06"
sectionName: "Features client"
slideName: "Sampling - Flux"
---

# Sampling - Flux d'exécution

<div style="position: relative; height: 400px; display: flex; align-items: center; justify-content: center;">

<div v-click.hide style="position: absolute; width: 100%; text-align: center;">

```mermaid
%%{init: {'themeVariables': { 'edgeLabelBackground': 'white'}, 'flowchart': {'rankSpacing': 80, 'nodeSpacing': 120}}}%%
graph LR
    Server[🔧 Serveur]
    Client[💻 Host / Client]
    User[👤 User]
    LLM[🤖 LLM]

    Server -.-> Client
    Client -.-> User
    Client -.-> LLM

    Server -->|1. Demande de prompting| Client
    Client -.->|2. Demande d'approbation| User
    User -.->|3. Approuve| Client
    Client -->|4. Envoie prompt| LLM
    LLM -->|5. Génère réponse| Client
    Client -->|6. Retourne résultat| Server

    style Server fill:#e8f5e9
    style Client fill:#fff4e6
    style User fill:#e1f5ff
    style LLM fill:#f3e5f5

    linkStyle 0 stroke:none
    linkStyle 1 stroke:none
    linkStyle 2 stroke:none
    linkStyle 3 stroke:white,color:white
    linkStyle 4 stroke:white,color:white
    linkStyle 5 stroke:white,color:white
    linkStyle 6 stroke:white,color:white
    linkStyle 7 stroke:white,color:white
    linkStyle 8 stroke:white,color:white
```

</div>

<div v-click="[1,2]" style="position: absolute; width: 100%; text-align: center;">

```mermaid
%%{init: {'themeVariables': { 'edgeLabelBackground': 'white'}, 'flowchart': {'rankSpacing': 80, 'nodeSpacing': 120}}}%%
graph LR
    Server[🔧 Serveur]
    Client[💻 Host / Client]
    User[👤 User]
    LLM[🤖 LLM]

    Server -.-> Client
    Client -.-> User
    Client -.-> LLM

    Server -->|1. Demande de prompting| Client
    Client -.->|2. Demande d'approbation| User
    User -.->|3. Approuve| Client
    Client -->|4. Envoie prompt| LLM
    LLM -->|5. Génère réponse| Client
    Client -->|6. Retourne résultat| Server

    style Server fill:#e8f5e9
    style Client fill:#fff4e6
    style User fill:#e1f5ff
    style LLM fill:#f3e5f5

    linkStyle 0 stroke:none
    linkStyle 1 stroke:none
    linkStyle 2 stroke:none
    linkStyle 4 stroke:white,color:white
    linkStyle 5 stroke:white,color:white
    linkStyle 6 stroke:white,color:white
    linkStyle 7 stroke:white,color:white
    linkStyle 8 stroke:white,color:white
```

</div>

<div v-click="[2,3]" style="position: absolute; width: 100%; text-align: center;">

```mermaid
%%{init: {'themeVariables': { 'edgeLabelBackground': 'white'}, 'flowchart': {'rankSpacing': 80, 'nodeSpacing': 120}}}%%
graph LR
    Server[🔧 Serveur]
    Client[💻 Host / Client]
    User[👤 User]
    LLM[🤖 LLM]

    Server -.-> Client
    Client -.-> User
    Client -.-> LLM

    Server -->|1. Demande de prompting| Client
    Client -.->|2. Demande d'approbation| User
    User -.->|3. Approuve| Client
    Client -->|4. Envoie prompt| LLM
    LLM -->|5. Génère réponse| Client
    Client -->|6. Retourne résultat| Server

    style Server fill:#e8f5e9
    style Client fill:#fff4e6
    style User fill:#e1f5ff
    style LLM fill:#f3e5f5

    linkStyle 0 stroke:none
    linkStyle 1 stroke:none
    linkStyle 2 stroke:none
    linkStyle 5 stroke:white,color:white
    linkStyle 6 stroke:white,color:white
    linkStyle 7 stroke:white,color:white
    linkStyle 8 stroke:white,color:white
```

</div>

<div v-click="[3,4]" style="position: absolute; width: 100%; text-align: center;">

```mermaid
%%{init: {'themeVariables': { 'edgeLabelBackground': 'white'}, 'flowchart': {'rankSpacing': 80, 'nodeSpacing': 120}}}%%
graph LR
    Server[🔧 Serveur]
    Client[💻 Host / Client]
    User[👤 User]
    LLM[🤖 LLM]

    Server -.-> Client
    Client -.-> User
    Client -.-> LLM

    Server -->|1. Demande de prompting| Client
    Client -.->|2. Demande d'approbation| User
    User -.->|3. Approuve| Client
    Client -->|4. Envoie prompt| LLM
    LLM -->|5. Génère réponse| Client
    Client -->|6. Retourne résultat| Server

    style Server fill:#e8f5e9
    style Client fill:#fff4e6
    style User fill:#e1f5ff
    style LLM fill:#f3e5f5

    linkStyle 0 stroke:none
    linkStyle 1 stroke:none
    linkStyle 2 stroke:none
    linkStyle 6 stroke:white,color:white
    linkStyle 7 stroke:white,color:white
    linkStyle 8 stroke:white,color:white
```

</div>

<div v-click="[4,5]" style="position: absolute; width: 100%; text-align: center;">

```mermaid
%%{init: {'themeVariables': { 'edgeLabelBackground': 'white'}, 'flowchart': {'rankSpacing': 80, 'nodeSpacing': 120}}}%%
graph LR
    Server[🔧 Serveur]
    Client[💻 Host / Client]
    User[👤 User]
    LLM[🤖 LLM]

    Server -.-> Client
    Client -.-> User
    Client -.-> LLM

    Server -->|1. Demande de prompting| Client
    Client -.->|2. Demande d'approbation| User
    User -.->|3. Approuve| Client
    Client -->|4. Envoie prompt| LLM
    LLM -->|5. Génère réponse| Client
    Client -->|6. Retourne résultat| Server

    style Server fill:#e8f5e9
    style Client fill:#fff4e6
    style User fill:#e1f5ff
    style LLM fill:#f3e5f5

    linkStyle 0 stroke:none
    linkStyle 1 stroke:none
    linkStyle 2 stroke:none
    linkStyle 7 stroke:white,color:white
    linkStyle 8 stroke:white,color:white
```

</div>

<div v-click="[5,6]" style="position: absolute; width: 100%; text-align: center;">

```mermaid
%%{init: {'themeVariables': { 'edgeLabelBackground': 'white'}, 'flowchart': {'rankSpacing': 80, 'nodeSpacing': 120}}}%%
graph LR
    Server[🔧 Serveur]
    Client[💻 Host / Client]
    User[👤 User]
    LLM[🤖 LLM]

    Server -.-> Client
    Client -.-> User
    Client -.-> LLM

    Server -->|1. Demande de prompting| Client
    Client -.->|2. Demande d'approbation| User
    User -.->|3. Approuve| Client
    Client -->|4. Envoie prompt| LLM
    LLM -->|5. Génère réponse| Client
    Client -->|6. Retourne résultat| Server

    style Server fill:#e8f5e9
    style Client fill:#fff4e6
    style User fill:#e1f5ff
    style LLM fill:#f3e5f5

    linkStyle 0 stroke:none
    linkStyle 1 stroke:none
    linkStyle 2 stroke:none
    linkStyle 8 stroke:white,color:white
```

</div>

<div v-click=6 style="position: absolute; width: 100%; text-align: center;">

```mermaid
%%{init: {'themeVariables': { 'edgeLabelBackground': 'white'}, 'flowchart': {'rankSpacing': 80, 'nodeSpacing': 120}}}%%
graph LR
    Server[🔧 Serveur]
    Client[💻 Host / Client]
    User[👤 User]
    LLM[🤖 LLM]

    Server -.-> Client
    Client -.-> User
    Client -.-> LLM

    Server -->|1. Demande de prompting| Client
    Client -.->|2. Demande d'approbation| User
    User -.->|3. Approuve| Client
    Client -->|4. Envoie prompt| LLM
    LLM -->|5. Génère réponse| Client
    Client -->|6. Retourne résultat| Server

    style Server fill:#e8f5e9
    style Client fill:#fff4e6
    style User fill:#e1f5ff
    style LLM fill:#f3e5f5

    linkStyle 0 stroke:none
    linkStyle 1 stroke:none
    linkStyle 2 stroke:none
```

</div>

</div>


---
layout: default
section: "06"
sectionName: "Features client"
slideName: "Sampling - Requête"
---

# Sampling - Détails des payloads

Le serveur demande au client d'utiliser son LLM

<div class="grid grid-cols-2 gap-4">

<div>

```json {none|all}
{
  "method": "sampling/createMessage",
  "params": {
    "messages": [
      {
        "role": "user",
        "content": {
          "type": "text",
          "text": "Quelle est la meilleure conf ?"
        }
      }
    ],
    "maxTokens": 100
  }
}
```

<p class="text-sm italic">Requête (serveur → client)</p>

</div>

<div>

```json {none|all}
{
  "result": {
    "role": "assistant",
    "content": {
      "type": "text",
      "text": "Devoxx France bien sûr !!!"
    },
    "model": "claude-3-sonnet",
    "stopReason": "endTurn"
  }
}
```

<p class="text-sm italic">Réponse (client → serveur)</p>

</div>

</div>


---
layout: section-with-header
title: Elicitation
subtitle: Le serveur demande au client des informations à l'utilisateur
section: "06"
sectionName: "Features client"
slideName: "Elicitation"
---


---
layout: default
section: "06"
sectionName: "Features client"
slideName: "Elicitation - Flux"
---

# Elicitation - Flux d'exécution

<div style="position: relative; height: 400px; display: flex; align-items: center; justify-content: center;">

<div v-click.hide style="position: absolute; width: 100%; text-align: center;">

```mermaid
%%{init: {'themeVariables': { 'edgeLabelBackground': 'white'}, 'flowchart': {'rankSpacing': 100, 'nodeSpacing': 150}}}%%
graph LR
    Server[🔧 Serveur]
    Client[💻 Host / Client]
    User[👤 User]

    Server -.-> Client
    Client -.-> User

    Server -->|1. Demande d'informations| Client
    Client -->|2. Affiche formulaire| User
    User -->|3. Saisit données| Client
    Client -->|4. Transmet données| Server

    style Server fill:#e8f5e9
    style Client fill:#fff4e6
    style User fill:#e1f5ff

    linkStyle 0 stroke:none
    linkStyle 1 stroke:none
    linkStyle 2 stroke:white,color:white
    linkStyle 3 stroke:white,color:white
    linkStyle 4 stroke:white,color:white
    linkStyle 5 stroke:white,color:white
```

</div>

<div v-click="[1,2]" style="position: absolute; width: 100%; text-align: center;">

```mermaid
%%{init: {'themeVariables': { 'edgeLabelBackground': 'white'}, 'flowchart': {'rankSpacing': 100, 'nodeSpacing': 150}}}%%
graph LR
    Server[🔧 Serveur]
    Client[💻 Host / Client]
    User[👤 User]

    Server -.-> Client
    Client -.-> User

    Server -->|1. Demande d'informations| Client
    Client -->|2. Affiche formulaire| User
    User -->|3. Saisit données| Client
    Client -->|4. Transmet données| Server

    style Server fill:#e8f5e9
    style Client fill:#fff4e6
    style User fill:#e1f5ff

    linkStyle 0 stroke:none
    linkStyle 1 stroke:none
    linkStyle 3 stroke:white,color:white
    linkStyle 4 stroke:white,color:white
    linkStyle 5 stroke:white,color:white
```

</div>

<div v-click="[2,3]" style="position: absolute; width: 100%; text-align: center;">

```mermaid
%%{init: {'themeVariables': { 'edgeLabelBackground': 'white'}, 'flowchart': {'rankSpacing': 100, 'nodeSpacing': 150}}}%%
graph LR
    Server[🔧 Serveur]
    Client[💻 Host / Client]
    User[👤 User]

    Server -.-> Client
    Client -.-> User

    Server -->|1. Demande d'informations| Client
    Client -->|2. Affiche formulaire| User
    User -->|3. Saisit données| Client
    Client -->|4. Transmet données| Server

    style Server fill:#e8f5e9
    style Client fill:#fff4e6
    style User fill:#e1f5ff

    linkStyle 0 stroke:none
    linkStyle 1 stroke:none
    linkStyle 4 stroke:white,color:white
    linkStyle 5 stroke:white,color:white
```

</div>

<div v-click="[3,4]" style="position: absolute; width: 100%; text-align: center;">

```mermaid
%%{init: {'themeVariables': { 'edgeLabelBackground': 'white'}, 'flowchart': {'rankSpacing': 100, 'nodeSpacing': 150}}}%%
graph LR
    Server[🔧 Serveur]
    Client[💻 Host / Client]
    User[👤 User]

    Server -.-> Client
    Client -.-> User

    Server -->|1. Demande d'informations| Client
    Client -->|2. Affiche formulaire| User
    User -->|3. Saisit données| Client
    Client -->|4. Transmet données| Server

    style Server fill:#e8f5e9
    style Client fill:#fff4e6
    style User fill:#e1f5ff

    linkStyle 0 stroke:none
    linkStyle 1 stroke:none
    linkStyle 5 stroke:white,color:white
```

</div>

<div v-click=4 style="position: absolute; width: 100%; text-align: center;">

```mermaid
%%{init: {'themeVariables': { 'edgeLabelBackground': 'white'}, 'flowchart': {'rankSpacing': 100, 'nodeSpacing': 150}}}%%
graph LR
    Server[🔧 Serveur]
    Client[💻 Host / Client]
    User[👤 User]

    Server -.-> Client
    Client -.-> User

    Server -->|1. Demande d'informations| Client
    Client -->|2. Affiche formulaire| User
    User -->|3. Saisit données| Client
    Client -->|4. Transmet données| Server

    style Server fill:#e8f5e9
    style Client fill:#fff4e6
    style User fill:#e1f5ff

    linkStyle 0 stroke:none
    linkStyle 1 stroke:none
```

</div>

</div>


---
layout: default
section: "06"
sectionName: "Features client"
slideName: "Elicitation - Requête"
---

# Elicitation - Détails des payloads

Le serveur demande des informations à l'utilisateur

<div class="grid grid-cols-2 gap-4">

<div>

```json {all|5-15}
{
  "method": "elicitation/create",
  "params": {
    "mode": "form",
    "message": "Quel a été ton talk préféré ?",
    "requestedSchema": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string"
        }
      },
      "required": [
        "name"
      ]
    }
  }
}
```

<p class="text-sm italic">Requête (serveur → client)</p>

</div>

<div>

```json {none|all}
{
  "result": {
    "action": "accept",
    "content": {
      "name": "Je te dirai ça vendredi."
    }
  }
}
```

<p class="text-sm italic">Réponse (client → serveur)</p>

</div>

</div>



---
layout: section-with-header
title: Roots
subtitle: Le client indique un dossier de travail au serveur
section: "06"
sectionName: "Features client"
slideName: "Roots"
---


---
layout: default
section: "06"
sectionName: "Features client"
slideName: "Roots - Flux"
---

# Roots - Flux d'exécution

<div style="position: relative; height: 400px; display: flex; align-items: center; justify-content: center;">

<div v-click.hide style="position: absolute; width: 100%; text-align: center;">

```mermaid
%%{init: {'themeVariables': { 'edgeLabelBackground': 'white'}, 'flowchart': {'rankSpacing': 100, 'nodeSpacing': 150}}}%%
graph LR
    Server[🔧 Serveur]
    Client[💻 Host / Client]

    Server -.-> Client

    Server -->|1. Liste Roots| Client
    Client -->|2. Retourne URIs| Server

    style Server fill:#e8f5e9
    style Client fill:#fff4e6

    linkStyle 0 stroke:none
    linkStyle 1 stroke:white,color:white
    linkStyle 2 stroke:white,color:white
```

</div>

<div v-click="[1,2]" style="position: absolute; width: 100%; text-align: center;">

```mermaid
%%{init: {'themeVariables': { 'edgeLabelBackground': 'white'}, 'flowchart': {'rankSpacing': 100, 'nodeSpacing': 150}}}%%
graph LR
    Server[🔧 Serveur]
    Client[💻 Host / Client]

    Server -.-> Client

    Server -->|1. Liste Roots| Client
    Client -->|2. Retourne URIs| Server

    style Server fill:#e8f5e9
    style Client fill:#fff4e6

    linkStyle 0 stroke:none
    linkStyle 2 stroke:white,color:white
```

</div>

<div v-click=2 style="position: absolute; width: 100%; text-align: center;">

```mermaid
%%{init: {'themeVariables': { 'edgeLabelBackground': 'white'}, 'flowchart': {'rankSpacing': 100, 'nodeSpacing': 150}}}%%
graph LR
    Server[🔧 Serveur]
    Client[💻 Host / Client]

    Server -.-> Client

    Server -->|1. Liste Roots| Client
    Client -->|2. Retourne URIs| Server

    style Server fill:#e8f5e9
    style Client fill:#fff4e6

    linkStyle 0 stroke:none
```

</div>

</div>


---
layout: default
section: "06"
sectionName: "Features client"
slideName: "Roots - Liste"
---

# Roots - Détails des payloads

Le client déclare ses dossiers de travail

<div class="grid grid-cols-2 gap-4">

<div>

```json
{
  "method": "roots/list"
}
```

<p class="text-sm italic">Requête (serveur → client)</p>

</div>

<div>

```json {none|all}
{
  "result": {
    "roots": [
      {
        "uri": "file:///home/user/project",
        "name": "My Project"
      }
    ]
  }
}
```

<p class="text-sm italic">Réponse (client → serveur)</p>

</div>

</div>

