---
layout: section
number: "03"
title: Lifecycle, Transports, API
---



---
layout: default
section: "03"
sectionName: "Lifecycle"
slideName: "JSON-RPC"
---

# Data layer

Basé sur **JSON-RPC 2.0**

<div class="grid grid-cols-2 gap-4">

<div>

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "my_method",
  "params": {
    "id": "123",
    ...
  }
}
```

<p class="text-sm italic">Requête</p>

</div>

<div>

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": [
    "Whatever",
    "valid",
    "JSON"
  ]
}
```

<p class="text-sm italic">Réponse</p>

</div>

</div>



---
layout: default
section: "03"
sectionName: "Lifecycle"
slideName: "Les transports"
---

# Transport layer

Trois modes de communication possibles entre client et serveur

| Transport | Usage                        |
| --------- |------------------------------|
| **stdio** | Processus locaux             |
| **Streamable HTTP** | Serveurs distants            |
| **SSE** | _Déprecié_ |



---
layout: default
section: "03"
sectionName: "Lifecycle"
slideName: "Cycle de vie"
---

# Cycle de vie MCP

MCP est un **protocole stateful**

Les trois types d'échanges entre client et serveur sont :

1. **Initialisation** - _Client → Serveur_ - Handshake et négociation des fonctionnalités supportées
2. **Utilisation** - _Client ↔ Serveur_ - Découverte et manipulation de primitives (tools, elicitation, sampling...)
3. **Notification** - _Serveur → Client_ - Mise à jour dynamique des primitives disponibles

_Une **primitive** est une fonctionnalité supportée par MCP exposée par le client ou le serveur_

---
layout: default
section: "03"
sectionName: "Lifecycle"
slideName: "Initialisation"
---

# 1. Initialisation

Handshake avec négociation des capabilities

<div class="grid grid-cols-2 gap-4">

<div>

```json {all|7-10}
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-06-18",
    "capabilities": {
      "elicitation": {},
      "sampling": {}
    },
    "clientInfo": {
      "name": "example-client",
      "version": "1.0.0"
    }
  }
}
```

<p class="text-sm italic">Requête</p>

</div>

<div>

```json {all|6-10}
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2025-06-18",
    "capabilities": {
      "tools": {
        "listChanged": true
      }
    },
    "serverInfo": {
      "name": "example-server",
      "version": "1.0.0"
    }
  }
}
```

<p class="text-sm italic">Réponse</p>

</div>

</div>

---
layout: default
section: "03"
sectionName: "Lifecycle"
slideName: "Utilisation"
---

# 2. Utilisation

Appels de tools/resources/prompts

<div class="grid grid-cols-2 gap-4">

<div>

```json {all|4}
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list"
}
```

<p class="text-sm italic">Requête</p>

</div>

<div>

```json {all|6-12}
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      {
        "name": "example_tool",
        "description": "This is an example tool",
        "inputSchema": {
          ... JSON Schema...
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
section: "03"
sectionName: "Lifecycle"
slideName: "Refresh"
---

# 3. Refresh

Mise à jour des capabilities

<div class="grid grid-cols-2 gap-4">

<div>

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/tools/list_changed"
}
```

<p class="text-sm italic">Notification (envoyée par le serveur)</p>

</div>

<div>

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/list"
}
```

<p class="text-sm italic">Requête de refresh (envoyée par le client)</p>

</div>

</div>
