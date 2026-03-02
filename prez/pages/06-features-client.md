---
layout: section
number: "06"
title: Features client
---


---
layout: default
section: "06"
sectionName: "Features client"
slideName: "Primitives client"
---

# Les trois primitives client

<v-clicks>

| Primitive       | Usage                                                         | Exemples                                           |
|-----------------|---------------------------------------------------------------|----------------------------------------------------|
| **Sampling**    | Le serveur demande au client d'utiliser son API d'inférence   | Génération de texte, complétion de code            |
| **Elicitation** | Le serveur demande au client des informations à l'utilisateur | Confirmer une action, renseigner des paramètres    |
| **Root**        | Le client indique un dossier de travail au serveur            | Pour un assistant de code, le chemin du workspace. |

</v-clicks>


---
layout: default
section: "06"
sectionName: "Features client"
slideName: "Sampling - Requête"
---

# Sampling - Requête

Le serveur demande au client d'utiliser son LLM

<div class="grid grid-cols-2 gap-4">

<div>

```json {all|4-16}
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "sampling/createMessage",
  "params": {
    "messages": [
      {
        "role": "user",
        "content": {
          "type": "text",
          "text": "Summarize this data"
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

```json {all|5-16}
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "role": "assistant",
    "content": {
      "type": "text",
      "text": "Here's a summary..."
    },
    "model": "claude-3-5-sonnet",
    "stopReason": "endTurn"
  }
}
```

<p class="text-sm italic">Réponse (client → serveur)</p>

</div>

</div>


---
layout: default
section: "06"
sectionName: "Features client"
slideName: "Elicitation - Requête"
---

# Elicitation - Requête

Le serveur demande des informations à l'utilisateur

<div class="grid grid-cols-2 gap-4">

<div>

```json {all|4-14}
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "elicitation/createMessage",
  "params": {
    "messages": [
      {
        "role": "user",
        "content": {
          "type": "text",
          "text": "Do you want to delete file.txt?"
        }
      }
    ]
  }
}
```

<p class="text-sm italic">Requête (serveur → client)</p>

</div>

<div>

```json {all|5-11}
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "role": "user",
    "content": {
      "type": "text",
      "text": "Yes, proceed"
    }
  }
}
```

<p class="text-sm italic">Réponse (client → serveur)</p>

</div>

</div>



---
layout: default
section: "06"
sectionName: "Features client"
slideName: "Roots - Liste"
---

# Roots - Liste

Le client déclare ses dossiers de travail

<div class="grid grid-cols-2 gap-4">

<div>

```json {all|4}
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "roots/list"
}
```

<p class="text-sm italic">Requête (serveur → client)</p>

</div>

<div>

```json {all|5-13}
{
  "jsonrpc": "2.0",
  "id": 3,
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

