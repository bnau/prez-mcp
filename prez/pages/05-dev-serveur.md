---
layout: section
number: "05"
title: Démo
subtitle: "Développement d'un serveur MCP"
---

---
layout: iframe

# the web page source
url: https://developers.events/#/2026/list?country=France
---
layout: default
section: "05"
sectionName: "Démo"
slideName: "Fausse idée"
---
layout: default
section: "05"
sectionName: "Démo"
slideName: "MCP Inspector"
hideFooter: true
---
<SlidevVideo controls>
  <source src="/public/videos/inspector.webm" type="video/webm">
</SlidevVideo>
---
layout: default
section: "05"
sectionName: "Démo"
slideName: "VS Code as Host"
hideFooter: true
---
<SlidevVideo controls>
  <source src="/public/videos/vscode.webm" type="video/webm">
</SlidevVideo>
---
layout: default
section: "05"
sectionName: "Démo"
slideName: "Fausse idée"
---

# Fausse idée

<div style="position: relative; height: 400px; display: flex; align-items: center; justify-content: center;">

<div v-click.hide style="position: absolute; width: 100%; text-align: center;">

```mermaid
%%{init: {'themeVariables': { 'edgeLabelBackground': 'white'}}}%%
graph LR
    User[👤 User] -->|1. Prompt| Client[💻 Host / Client]
    Client -->|2. Transmet| LLM[🤖 LLM]
    LLM -->|3. Déclenche| Tools[🔧 Serveur / Tools]

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
    User[👤 User] -->|1. Prompt| Client[💻 Host / Client]
    Client -->|2. Transmet| LLM[🤖 LLM]
    LLM -->|3. Déclenche| Tools[🔧 Serveur / Tools]

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
    User[👤 User] -->|1. Prompt| Client[💻 Host / Client]
    Client -->|2. Transmet| LLM[🤖 LLM]
    LLM -->|3. Déclenche| Tools[🔧 Serveur / Tools]

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
    User[👤 User] -->|1. Prompt| Client[💻 Host / Client]
    Client -->|2. Transmet| LLM[🤖 LLM]
    LLM -->|3. Déclenche| Tools[🔧 Serveur / Tools]

    style User fill:#e1f5ff
    style Client fill:#fff4e6
    style LLM fill:#f3e5f5
    style Tools fill:#e8f5e9
```

</div>

</div>

---
layout: default
section: "05"
sectionName: "Démo"
slideName: "La réalité"
---

# La réalité

<div style="position: relative; height: 400px; display: flex; align-items: center; justify-content: center;">

<div v-click.hide style="position: absolute; width: 100%; text-align: center;">

```mermaid
%%{init: {'themeVariables': { 'edgeLabelBackground': 'white'}, 'flowchart': {'rankSpacing': 120, 'nodeSpacing': 180}}}%%
graph LR
    User[👤 User]
    Client[💻 Host / Client]
    Tool[🔧 Serveur / Tools]
    LLM[🤖 LLM]

    User -.-> Client
    Client -.-> Tool
    Client -.-> LLM

    User -->|1. Prompt| Client
    Client --->|2. Liste les tools| Tool
    Tool --->|3. Signature des tools| Client
    Client --->|4. Prompt système + signatures| LLM
    LLM --->|5. Réponse structurée| Client
    Client --->|6. Déclenche| Tool
    Tool --->|7. Réponse MCP| Client
    Client --->|8. Prompt utilisateur + réponse MCP| LLM
    LLM --->|9. Réponse définitive| Client

    style User fill:#e1f5ff
    style Client fill:#fff4e6
    style Tool fill:#e8f5e9
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
    linkStyle 9 stroke:white,color:white
    linkStyle 10 stroke:white,color:white
    linkStyle 11 stroke:white,color:white
```

</div>

<div v-click="[1,2]" style="position: absolute; width: 100%; text-align: center;">

```mermaid
%%{init: {'themeVariables': { 'edgeLabelBackground': 'white'}, 'flowchart': {'rankSpacing': 120, 'nodeSpacing': 180}}}%%
graph LR
    User[👤 User]
    Client[💻 Host / Client]
    Tool[🔧 Serveur / Tools]
    LLM[🤖 LLM]

    User -.-> Client
    Client -.-> Tool
    Client -.-> LLM

    User -->|1. Prompt| Client
    Client --->|2. Liste les tools| Tool
    Tool --->|3. Signature des tools| Client
    Client --->|4. Prompt système + signatures| LLM
    LLM --->|5. Réponse structurée| Client
    Client --->|6. Déclenche| Tool
    Tool --->|7. Réponse MCP| Client
    Client --->|8. Prompt utilisateur + réponse MCP| LLM
    LLM --->|9. Réponse définitive| Client

    style User fill:#e1f5ff
    style Client fill:#fff4e6
    style Tool fill:#e8f5e9
    style LLM fill:#f3e5f5

    linkStyle 0 stroke:none
    linkStyle 1 stroke:none
    linkStyle 2 stroke:none
    linkStyle 4 stroke:white,color:white
    linkStyle 5 stroke:white,color:white
    linkStyle 6 stroke:white,color:white
    linkStyle 7 stroke:white,color:white
    linkStyle 8 stroke:white,color:white
    linkStyle 9 stroke:white,color:white
    linkStyle 10 stroke:white,color:white
    linkStyle 11 stroke:white,color:white
```

</div>

<div v-click="[2,3]" style="position: absolute; width: 100%; text-align: center;">

```mermaid
%%{init: {'themeVariables': { 'edgeLabelBackground': 'white'}, 'flowchart': {'rankSpacing': 120, 'nodeSpacing': 180}}}%%
graph LR
    User[👤 User]
    Client[💻 Host / Client]
    Tool[🔧 Serveur / Tools]
    LLM[🤖 LLM]

    User -.-> Client
    Client -.-> Tool
    Client -.-> LLM

    User -->|1. Prompt| Client
    Client --->|2. Liste les tools| Tool
    Tool --->|3. Signature des tools| Client
    Client --->|4. Prompt système + signatures| LLM
    LLM --->|5. Réponse structurée| Client
    Client --->|6. Déclenche| Tool
    Tool --->|7. Réponse MCP| Client
    Client --->|8. Prompt utilisateur + réponse MCP| LLM
    LLM --->|9. Réponse définitive| Client

    style User fill:#e1f5ff
    style Client fill:#fff4e6
    style Tool fill:#e8f5e9
    style LLM fill:#f3e5f5

    linkStyle 0 stroke:none
    linkStyle 1 stroke:none
    linkStyle 2 stroke:none
    linkStyle 5 stroke:white,color:white
    linkStyle 6 stroke:white,color:white
    linkStyle 7 stroke:white,color:white
    linkStyle 8 stroke:white,color:white
    linkStyle 9 stroke:white,color:white
    linkStyle 10 stroke:white,color:white
    linkStyle 11 stroke:white,color:white
```

</div>

<div v-click="[3,4]" style="position: absolute; width: 100%; text-align: center;">

```mermaid
%%{init: {'themeVariables': { 'edgeLabelBackground': 'white'}, 'flowchart': {'rankSpacing': 120, 'nodeSpacing': 180}}}%%
graph LR
    User[👤 User]
    Client[💻 Host / Client]
    Tool[🔧 Serveur / Tools]
    LLM[🤖 LLM]

    User -.-> Client
    Client -.-> Tool
    Client -.-> LLM

    User -->|1. Prompt| Client
    Client --->|2. Liste les tools| Tool
    Tool --->|3. Signature des tools| Client
    Client --->|4. Prompt système + signatures| LLM
    LLM --->|5. Réponse structurée| Client
    Client --->|6. Déclenche| Tool
    Tool --->|7. Réponse MCP| Client
    Client --->|8. Prompt utilisateur + réponse MCP| LLM
    LLM --->|9. Réponse définitive| Client

    style User fill:#e1f5ff
    style Client fill:#fff4e6
    style Tool fill:#e8f5e9
    style LLM fill:#f3e5f5

    linkStyle 0 stroke:none
    linkStyle 1 stroke:none
    linkStyle 2 stroke:none
    linkStyle 6 stroke:white,color:white
    linkStyle 7 stroke:white,color:white
    linkStyle 8 stroke:white,color:white
    linkStyle 9 stroke:white,color:white
    linkStyle 10 stroke:white,color:white
    linkStyle 11 stroke:white,color:white
```

</div>

<div v-click="[4,5]" style="position: absolute; width: 100%; text-align: center;">

```mermaid
%%{init: {'themeVariables': { 'edgeLabelBackground': 'white'}, 'flowchart': {'rankSpacing': 120, 'nodeSpacing': 180}}}%%
graph LR
    User[👤 User]
    Client[💻 Host / Client]
    Tool[🔧 Serveur / Tools]
    LLM[🤖 LLM]

    User -.-> Client
    Client -.-> Tool
    Client -.-> LLM

    User -->|1. Prompt| Client
    Client --->|2. Liste les tools| Tool
    Tool --->|3. Signature des tools| Client
    Client --->|4. Prompt système + signatures| LLM
    LLM --->|5. Réponse structurée| Client
    Client --->|6. Déclenche| Tool
    Tool --->|7. Réponse MCP| Client
    Client --->|8. Prompt utilisateur + réponse MCP| LLM
    LLM --->|9. Réponse définitive| Client

    style User fill:#e1f5ff
    style Client fill:#fff4e6
    style Tool fill:#e8f5e9
    style LLM fill:#f3e5f5

    linkStyle 0 stroke:none
    linkStyle 1 stroke:none
    linkStyle 2 stroke:none
    linkStyle 7 stroke:white,color:white
    linkStyle 8 stroke:white,color:white
    linkStyle 9 stroke:white,color:white
    linkStyle 10 stroke:white,color:white
    linkStyle 11 stroke:white,color:white
```

</div>

<div v-click="[5,6]" style="position: absolute; width: 100%; text-align: center;">

```mermaid
%%{init: {'themeVariables': { 'edgeLabelBackground': 'white'}, 'flowchart': {'rankSpacing': 120, 'nodeSpacing': 180}}}%%
graph LR
    User[👤 User]
    Client[💻 Host / Client]
    Tool[🔧 Serveur / Tools]
    LLM[🤖 LLM]

    User -.-> Client
    Client -.-> Tool
    Client -.-> LLM

    User -->|1. Prompt| Client
    Client --->|2. Liste les tools| Tool
    Tool --->|3. Signature des tools| Client
    Client --->|4. Prompt système + signatures| LLM
    LLM --->|5. Réponse structurée| Client
    Client --->|6. Déclenche| Tool
    Tool --->|7. Réponse MCP| Client
    Client --->|8. Prompt utilisateur + réponse MCP| LLM
    LLM --->|9. Réponse définitive| Client

    style User fill:#e1f5ff
    style Client fill:#fff4e6
    style Tool fill:#e8f5e9
    style LLM fill:#f3e5f5

    linkStyle 0 stroke:none
    linkStyle 1 stroke:none
    linkStyle 2 stroke:none
    linkStyle 8 stroke:white,color:white
    linkStyle 9 stroke:white,color:white
    linkStyle 10 stroke:white,color:white
    linkStyle 11 stroke:white,color:white
```

</div>

<div v-click="[6,7]" style="position: absolute; width: 100%; text-align: center;">

```mermaid
%%{init: {'themeVariables': { 'edgeLabelBackground': 'white'}, 'flowchart': {'rankSpacing': 120, 'nodeSpacing': 180}}}%%
graph LR
    User[👤 User]
    Client[💻 Host / Client]
    Tool[🔧 Serveur / Tools]
    LLM[🤖 LLM]

    User -.-> Client
    Client -.-> Tool
    Client -.-> LLM

    User -->|1. Prompt| Client
    Client --->|2. Liste les tools| Tool
    Tool --->|3. Signature des tools| Client
    Client --->|4. Prompt système + signatures| LLM
    LLM --->|5. Réponse structurée| Client
    Client --->|6. Déclenche| Tool
    Tool --->|7. Réponse MCP| Client
    Client --->|8. Prompt utilisateur + réponse MCP| LLM
    LLM --->|9. Réponse définitive| Client

    style User fill:#e1f5ff
    style Client fill:#fff4e6
    style Tool fill:#e8f5e9
    style LLM fill:#f3e5f5

    linkStyle 0 stroke:none
    linkStyle 1 stroke:none
    linkStyle 2 stroke:none
    linkStyle 9 stroke:white,color:white
    linkStyle 10 stroke:white,color:white
    linkStyle 11 stroke:white,color:white
```

</div>

<div v-click="[7,8]" style="position: absolute; width: 100%; text-align: center;">

```mermaid
%%{init: {'themeVariables': { 'edgeLabelBackground': 'white'}, 'flowchart': {'rankSpacing': 120, 'nodeSpacing': 180}}}%%
graph LR
    User[👤 User]
    Client[💻 Host / Client]
    Tool[🔧 Serveur / Tools]
    LLM[🤖 LLM]

    User -.-> Client
    Client -.-> Tool
    Client -.-> LLM

    User -->|1. Prompt| Client
    Client --->|2. Liste les tools| Tool
    Tool --->|3. Signature des tools| Client
    Client --->|4. Prompt système + signatures| LLM
    LLM --->|5. Réponse structurée| Client
    Client --->|6. Déclenche| Tool
    Tool --->|7. Réponse MCP| Client
    Client --->|8. Prompt utilisateur + réponse MCP| LLM
    LLM --->|9. Réponse définitive| Client

    style User fill:#e1f5ff
    style Client fill:#fff4e6
    style Tool fill:#e8f5e9
    style LLM fill:#f3e5f5

    linkStyle 0 stroke:none
    linkStyle 1 stroke:none
    linkStyle 2 stroke:none
    linkStyle 10 stroke:white,color:white
    linkStyle 11 stroke:white,color:white
```

</div>

<div v-click="[8,9]" style="position: absolute; width: 100%; text-align: center;">

```mermaid
%%{init: {'themeVariables': { 'edgeLabelBackground': 'white'}, 'flowchart': {'rankSpacing': 120, 'nodeSpacing': 180}}}%%
graph LR
    User[👤 User]
    Client[💻 Host / Client]
    Tool[🔧 Serveur / Tools]
    LLM[🤖 LLM]

    User -.-> Client
    Client -.-> Tool
    Client -.-> LLM

    User -->|1. Prompt| Client
    Client --->|2. Liste les tools| Tool
    Tool --->|3. Signature des tools| Client
    Client --->|4. Prompt système + signatures| LLM
    LLM --->|5. Réponse structurée| Client
    Client --->|6. Déclenche| Tool
    Tool --->|7. Réponse MCP| Client
    Client --->|8. Prompt utilisateur + réponse MCP| LLM
    LLM --->|9. Réponse définitive| Client

    style User fill:#e1f5ff
    style Client fill:#fff4e6
    style Tool fill:#e8f5e9
    style LLM fill:#f3e5f5

    linkStyle 0 stroke:none
    linkStyle 1 stroke:none
    linkStyle 2 stroke:none
    linkStyle 11 stroke:white,color:white
```

</div>

<div v-click=9 style="position: absolute; width: 100%; text-align: center;">

```mermaid
%%{init: {'themeVariables': { 'edgeLabelBackground': 'white'}, 'flowchart': {'rankSpacing': 120, 'nodeSpacing': 180}}}%%
graph LR
    User[👤 User]
    Client[💻 Host / Client]
    Tool[🔧 Serveur / Tools]
    LLM[🤖 LLM]

    User -.-> Client
    Client -.-> Tool
    Client -.-> LLM

    User -->|1. Prompt| Client
    Client --->|2. Liste les tools| Tool
    Tool --->|3. Signature des tools| Client
    Client --->|4. Prompt système + signatures| LLM
    LLM --->|5. Réponse structurée| Client
    Client --->|6. Déclenche| Tool
    Tool --->|7. Réponse MCP| Client
    Client --->|8. Prompt utilisateur + réponse MCP| LLM
    LLM --->|9. Réponse définitive| Client

    style User fill:#e1f5ff
    style Client fill:#fff4e6
    style Tool fill:#e8f5e9
    style LLM fill:#f3e5f5

    linkStyle 0 stroke:none
    linkStyle 1 stroke:none
    linkStyle 2 stroke:none
```

</div>

</div>
