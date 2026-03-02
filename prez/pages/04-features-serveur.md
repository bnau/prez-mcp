---
layout: section
number: "04"
title: Features serveur
---


---
layout: default
section: "04"
sectionName: "Features serveur"
slideName: "Primitives serveur"
---

# Les trois primitives serveur

<v-clicks>

| Primitive    | Usage                                                      | Exemples                                          |
|--------------|------------------------------------------------------------|---------------------------------------------------|
| **Tool**     | Fonction que le LLM peut décider d'appeler                 | Rechercher dans une base de données               |
| **Resource** | Source de données en lecture seule fournissant du contexte | Fichiers, schémas DB, documentation...            |
| **Prompt**   | Messge prédéfini qu'on envoie au LLM                       | Liste d'opération à exécuter dans un ordre précis |

</v-clicks>


---
layout: default
section: "04"
sectionName: "Features serveur"
slideName: "Tools - Découverte"
---

# Tools - Découverte

Lister les tools disponibles

<div class="grid grid-cols-2 gap-4">

<div>

```json {all|4}
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list"
}
```

<p class="text-sm italic">Requête</p>

</div>

<div>

```json {all|5-15}
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {
        "name": "search_conferences",
        "description": "Search for tech conferences",
        "inputSchema": {
          "type": "object",
          "properties": {
            "query": { "type": "string" }
          }
        }
      }
    ]
  }
}
```

<p class="text-sm italic">Réponse</p>

</div>

</div>


---
layout: default
section: "04"
sectionName: "Features serveur"
slideName: "Tools - Appel"
---

# Tools - Appel

Exécuter un tool avec ses arguments

<div class="grid grid-cols-2 gap-4">

<div>

```json {all|4-10}
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "search_conferences",
    "arguments": {
      "query": "React"
    }
  }
}
```

<p class="text-sm italic">Requête</p>

</div>

<div>

```json {all|5-12}
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Found 3 React conferences:\n- React Summit\n- React Advanced\n- React Day Berlin"
      }
    ],
    "isError": false
  }
}
```

<p class="text-sm italic">Réponse</p>

</div>

</div>


---
layout: default
section: "04"
sectionName: "Features serveur"
slideName: "Resources - Découverte"
---

# Resources - Découverte

Lister les resources disponibles

<div class="grid grid-cols-2 gap-4">

<div>

```json {all|4}
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "resources/list"
}
```

<p class="text-sm italic">Requête</p>

</div>

<div>

```json {all|5-14}
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "resources": [
      {
        "uri": "file:///docs/api.md",
        "name": "API Documentation",
        "mimeType": "text/markdown",
        "description": "Complete API reference"
      }
    ]
  }
}
```

<p class="text-sm italic">Réponse</p>

</div>

</div>


---
layout: default
section: "04"
sectionName: "Features serveur"
slideName: "Resources - Lecture"
---

# Resources - Lecture

Lire le contenu d'une resource

<div class="grid grid-cols-2 gap-4">

<div>

```json {all|4-8}
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "resources/read",
  "params": {
    "uri": "file:///docs/api.md"
  }
}
```

<p class="text-sm italic">Requête</p>

</div>

<div>

```json {all|5-11}
{
  "jsonrpc": "2.0",
  "id": 4,
  "result": {
    "contents": [
      {
        "uri": "file:///docs/api.md",
        "mimeType": "text/markdown",
        "text": "# API Reference\n\n..."
      }
    ]
  }
}
```

<p class="text-sm italic">Réponse</p>

</div>

</div>


---
layout: default
section: "04"
sectionName: "Features serveur"
slideName: "Prompts - Découverte"
---

# Prompts - Découverte

Lister les prompts disponibles

<div class="grid grid-cols-2 gap-4">

<div>

```json {all|4}
{
  "jsonrpc": "2.0",
  "id": 5,
  "method": "prompts/list"
}
```

<p class="text-sm italic">Requête</p>

</div>

<div>

```json {all|5-18}
{
  "jsonrpc": "2.0",
  "id": 5,
  "result": {
    "prompts": [
      {
        "name": "code_review",
        "description": "Review code for quality",
        "arguments": [
          {
            "name": "file",
            "description": "File to review",
            "required": true
          }
        ]
      }
    ]
  }
}
```

<p class="text-sm italic">Réponse</p>

</div>

</div>


---
layout: default
section: "04"
sectionName: "Features serveur"
slideName: "Prompts - Récupération"
---

# Prompts - Récupération

Obtenir un prompt avec ses arguments

<div class="grid grid-cols-2 gap-4">

<div>

```json {all|4-10}
{
  "jsonrpc": "2.0",
  "id": 6,
  "method": "prompts/get",
  "params": {
    "name": "code_review",
    "arguments": {
      "file": "app.py"
    }
  }
}
```

<p class="text-sm italic">Requête</p>

</div>

<div>

```json {all|5-13}
{
  "jsonrpc": "2.0",
  "id": 6,
  "result": {
    "messages": [
      {
        "role": "user",
        "content": {
          "type": "text",
          "text": "Review app.py for:\n- Code quality\n- Security\n- Performance"
        }
      }
    ]
  }
}
```

<p class="text-sm italic">Réponse</p>

</div>

</div>
