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

# Sampling

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
layout: default
section: "06"
sectionName: "Features client"
slideName: "Elicitation - Requête"
---

# Elicitation

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
layout: default
section: "06"
sectionName: "Features client"
slideName: "Roots - Liste"
---

# Roots

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

