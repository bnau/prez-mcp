# Sampling Handler avec Confirmation Utilisateur

## Vue d'ensemble

Le client MCP peut implémenter un **sampling handler** personnalisé pour contrôler les demandes d'échantillonnage LLM du serveur. Notre handler demande une confirmation à l'utilisateur et, si accepté, appelle le LLM pour obtenir la réponse JSON.

## Pourquoi un Sampling Handler ?

Quand le serveur MCP utilise `ctx.sample()` pour faire des analyses IA (comme le matching CFP ↔ Conférences), il demande au client de fournir une réponse LLM. Notre handler personnalisé permet de :

- ✅ **Contrôler** les appels LLM (autoriser/refuser)
- ✅ **Visualiser** ce que le serveur demande à l'IA
- ✅ **Déboguer** les prompts de sampling
- ✅ **Appeler le LLM** uniquement après confirmation

## Implémentation

### Handler de Confirmation + Appel LLM

```python
from fastmcp.client.sampling import RequestContext, SamplingMessage, SamplingParams
import httpx

async def user_confirmation_sampling_handler(
    messages: list[SamplingMessage],
    params: SamplingParams,
    context: RequestContext,
) -> str:
    """
    Sampling handler qui demande une confirmation y/n à l'utilisateur.
    Si accepté, appelle le LLM et retourne sa réponse JSON.
    """
    # Afficher les informations sur la demande de sampling
    print("🤖 Le serveur MCP demande un échantillonnage LLM")

    # Afficher le system prompt
    if params.systemPrompt:
        print(f"📋 System Prompt: {params.systemPrompt[:500]}...")

    # Afficher les messages
    for message in messages:
        print(f"{message.role}: {message.content.text[:300]}...")

    # Afficher les paramètres
    print(f"⚙️  Temperature: {params.temperature}")
    print(f"⚙️  Max tokens: {params.maxTokens}")

    # Demander confirmation
    response = input("❓ Autoriser cet échantillonnage LLM ? (y/n): ")

    if response.lower() in ["y", "yes", "o", "oui"]:
        print("✅ Échantillonnage autorisé")
        print("🔄 Appel du LLM...\n")

        # Construire les messages pour l'API OpenAI
        llm_messages = []

        # Ajouter le system prompt si présent
        if params.systemPrompt:
            llm_messages.append({"role": "system", "content": params.systemPrompt})

        # Ajouter les messages du sampling
        for message in messages:
            content_text = message.content.text if hasattr(message.content, "text") else str(message.content)
            llm_messages.append({"role": message.role, "content": content_text})

        # Appeler le LLM
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "http://localhost:4141/v1/chat/completions",
                json={
                    "model": "gpt-4o-mini",
                    "messages": llm_messages,
                    "temperature": params.temperature if params.temperature else 0.3,
                    "max_tokens": params.maxTokens if params.maxTokens else 4000,
                },
            )

            result = response.json()
            llm_response = result["choices"][0]["message"]["content"]

            print(f"✅ Réponse du LLM reçue ({len(llm_response)} caractères)")
            return llm_response
    else:
        print("❌ Échantillonnage refusé")
        return '{"error": "Sampling denied by user"}'
```

### Enregistrement du Handler

Pour utiliser ce handler, passez-le au constructeur du client :

```python
from fastmcp.client import Client

client = Client(
    "http://127.0.0.1:8000/mcp",
    sampling_handler=user_confirmation_sampling_handler
)

async with client:
    # Les appels à ctx.sample() du serveur utiliseront ce handler
    result = await client.call_tool(
        "search_conferences",
        {
            "cfp_open": True,
            "country": "France",
            "match_cfps": True,  # Déclenchera des sampling
        }
    )
```

## Test

### Fichier de test : `test_sampling_with_handler.py`

```bash
# Terminal 1 : Démarrer le serveur
uv run python mcp_server/server.py

# Terminal 2 : Tester avec le handler
uv run python test_sampling_with_handler.py
```

### Workflow

1. Le client appelle `search_conferences` avec `match_cfps=True`
2. Le serveur lit les CFPs et pour chaque CFP appelle `ctx.sample()`
3. Le client reçoit la demande de sampling via le handler
4. **L'utilisateur voit** :
   - Le system prompt du sampling
   - Les messages envoyés au LLM
   - Les paramètres (temperature, max_tokens)
5. **L'utilisateur décide** :
   - `y` → Le handler appelle le LLM et retourne sa réponse JSON
   - `n` → Le handler retourne une erreur JSON
6. Le serveur reçoit la réponse et continue le traitement

## Exemple de Sortie

```
================================================================================
🤖 Le serveur MCP demande un échantillonnage LLM
================================================================================

📋 System Prompt:
--------------------------------------------------------------------------------
Analyze which conferences match this CFP topic: "Model Context Protocol"...
--------------------------------------------------------------------------------

💬 Messages:
--------------------------------------------------------------------------------
👤 Message 1 (user):
CFP excerpt:
# Model Context Protocol et agents IA

Ce talk présente le Model Context Protocol (MCP)...

Available conferences:
[
  {"name": "Devoxx France 2026", "tags": ["java", "development"]},
  ...
]
--------------------------------------------------------------------------------

⚙️  Paramètres de sampling:
   - Temperature: 0.3
   - Max tokens: 4000

================================================================================
❓ Voulez-vous autoriser cet échantillonnage LLM ? (y/n): y
✅ Échantillonnage autorisé
🔄 Appel du LLM...

✅ Réponse du LLM reçue (542 caractères)
```

Le serveur reçoit alors la réponse JSON du LLM et peut continuer le matching.

## Structure du Sampling Handler

### Signature

```python
async def handler(
    messages: list[SamplingMessage],
    params: SamplingParams,
    context: RequestContext,
) -> str:
```

### Paramètres

| Paramètre | Type | Description |
|-----------|------|-------------|
| `messages` | `list[SamplingMessage]` | Liste des messages (role + content) |
| `params` | `SamplingParams` | Paramètres du sampling (temperature, maxTokens, systemPrompt...) |
| `context` | `RequestContext` | Contexte de la requête MCP |

### Retour

Le handler doit retourner une `str` qui sera utilisée comme réponse du LLM par le serveur. Dans notre cas, c'est la réponse JSON du LLM.

### Messages

Chaque `SamplingMessage` contient :
- `role` : `"user"` ou `"assistant"`
- `content` : Objet avec attribut `text` pour le contenu textuel

### Params

`SamplingParams` contient :
- `systemPrompt` : Prompt système optionnel
- `temperature` : Température de sampling (0-1)
- `maxTokens` : Nombre maximum de tokens
- `modelPreferences` : Préférences de modèle
- `stopSequences` : Séquences d'arrêt
- `tools` : Liste des outils disponibles
- `toolChoice` : Choix d'utilisation des outils

## Handlers Prédéfinis

FastMCP fournit des handlers pour les APIs courantes :

### OpenAI

```python
from fastmcp.client.openai import OpenAISamplingHandler

handler = OpenAISamplingHandler(default_model="gpt-4o")
client = Client(url, sampling_handler=handler)
```

Installation : `pip install fastmcp[openai]`

### Anthropic

```python
from fastmcp.client.anthropic import AnthropicSamplingHandler

handler = AnthropicSamplingHandler(default_model="claude-sonnet-4-5")
client = Client(url, sampling_handler=handler)
```

Installation : `pip install fastmcp[anthropic]`

## Cas d'Usage

### 1. Développement et Débogage

Utiliser le handler de confirmation pour :
- Voir exactement ce que le serveur envoie au LLM
- Comprendre les prompts de sampling
- Contrôler chaque appel LLM

### 2. Contrôle des Coûts

Autoriser manuellement chaque appel LLM pour éviter :
- Les boucles infinies
- Les appels non souhaités
- Les coûts inattendus

### 3. Tests Automatisés

Créer un handler qui :
- Retourne des réponses prédéfinies
- Simule différents scénarios
- Teste sans vraie API LLM

```python
async def mock_sampling_handler(messages, params, context):
    # Retourner une réponse mockée
    return '{"matches": [{"conference_name": "Test Conf", "score": 100}]}'
```

### 4. Production avec Validation

En production, ajouter une validation avant d'appeler le vrai LLM :
```python
async def validated_sampling_handler(messages, params, context):
    # Vérifier que la demande est légitime
    if not is_valid_request(messages, params):
        return '{"error": "Invalid request"}'

    # Appeler le vrai LLM
    return await call_real_llm(messages, params)
```

## Configuration

### Client avec Handler de Confirmation (Développement)

```python
client = Client(url, sampling_handler=user_confirmation_sampling_handler)
```

### Client avec LLM Direct (Production)

```python
from fastmcp.client.openai import OpenAISamplingHandler

handler = OpenAISamplingHandler(
    default_model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)

client = Client(url, sampling_handler=handler)
```

### Sans Handler

Si aucun handler n'est fourni, le client ne supportera pas le sampling et les appels à `ctx.sample()` échoueront.

## Documentation FastMCP

Pour plus d'informations :
- [FastMCP Sampling Clients](https://gofastmcp.com/clients/sampling)
- [FastMCP Client API](https://gofastmcp.com/clients/python)

### Enregistrement du Handler

Pour utiliser ce handler, passez-le au constructeur du client :

```python
from fastmcp.client import Client

client = Client(
    "http://127.0.0.1:8000/mcp",
    sampling_handler=user_confirmation_sampling_handler
)

async with client:
    # Les appels à ctx.sample() du serveur utiliseront ce handler
    result = await client.call_tool(
        "search_conferences",
        {
            "cfp_open": True,
            "country": "France",
            "match_cfps": True,  # Déclenchera des sampling
        }
    )
```

## Test

### Fichier de test : `test_sampling_with_handler.py`

```bash
# Terminal 1 : Démarrer le serveur
uv run python mcp_server/server.py

# Terminal 2 : Tester avec le handler
uv run python test_sampling_with_handler.py
```

### Workflow

1. Le client appelle `search_conferences` avec `match_cfps=True`
2. Le serveur lit les CFPs et pour chaque CFP appelle `ctx.sample()`
3. Le client reçoit la demande de sampling via le handler
4. **L'utilisateur voit** :
   - Le system prompt du sampling
   - Les messages envoyés au LLM
   - Les paramètres (temperature, max_tokens)
5. **L'utilisateur décide** :
   - `y` → Le handler retourne une réponse positive
   - `n` → Le handler retourne une réponse négative
6. Le serveur continue avec la réponse du handler

## Exemple de Sortie

```
================================================================================
🤖 Le serveur MCP demande un échantillonnage LLM
================================================================================

📋 System Prompt:
--------------------------------------------------------------------------------
Analyze which conferences match this CFP topic: "Model Context Protocol"...
--------------------------------------------------------------------------------

💬 Messages:
--------------------------------------------------------------------------------
👤 Message 1 (user):
CFP excerpt:
# Model Context Protocol et agents IA

Ce talk présente le Model Context Protocol (MCP)...

Available conferences:
[
  {"name": "Devoxx France 2026", "tags": ["java", "development"]},
  ...
]
--------------------------------------------------------------------------------

⚙️  Paramètres de sampling:
   - Temperature: 0.3
   - Max tokens: 4000

================================================================================
❓ Voulez-vous autoriser cet échantillonnage LLM ? (y/n): y
✅ Échantillonnage autorisé
```

## Structure du Sampling Handler

### Signature

```python
async def handler(
    messages: list[SamplingMessage],
    params: SamplingParams,
    context: RequestContext,
) -> str:
```

### Paramètres

| Paramètre | Type | Description |
|-----------|------|-------------|
| `messages` | `list[SamplingMessage]` | Liste des messages (role + content) |
| `params` | `SamplingParams` | Paramètres du sampling (temperature, maxTokens, systemPrompt...) |
| `context` | `RequestContext` | Contexte de la requête MCP |

### Retour

Le handler doit retourner une `str` qui sera utilisée comme réponse du LLM par le serveur.

### Messages

Chaque `SamplingMessage` contient :
- `role` : `"user"` ou `"assistant"`
- `content` : Objet avec attribut `text` pour le contenu textuel

### Params

`SamplingParams` contient :
- `systemPrompt` : Prompt système optionnel
- `temperature` : Température de sampling (0-1)
- `maxTokens` : Nombre maximum de tokens
- `modelPreferences` : Préférences de modèle
- `stopSequences` : Séquences d'arrêt
- `tools` : Liste des outils disponibles
- `toolChoice` : Choix d'utilisation des outils

## Handlers Prédéfinis

FastMCP fournit des handlers pour les APIs courantes :

### OpenAI

```python
from fastmcp.client.openai import OpenAISamplingHandler

handler = OpenAISamplingHandler(default_model="gpt-4o")
client = Client(url, sampling_handler=handler)
```

Installation : `pip install fastmcp[openai]`

### Anthropic

```python
from fastmcp.client.anthropic import AnthropicSamplingHandler

handler = AnthropicSamplingHandler(default_model="claude-sonnet-4-5")
client = Client(url, sampling_handler=handler)
```

Installation : `pip install fastmcp[anthropic]`

## Cas d'Usage

### 1. Développement et Débogage

Utiliser le handler de confirmation pour :
- Voir exactement ce que le serveur envoie au LLM
- Comprendre les prompts de sampling
- Tester sans consommer de crédits API

### 2. Contrôle des Coûts

Autoriser manuellement chaque appel LLM pour éviter :
- Les boucles infinies
- Les appels non souhaités
- Les coûts inattendus

### 3. Tests Automatisés

Créer un handler qui :
- Retourne des réponses prédéfinies
- Simule différents scénarios
- Teste sans vraie API LLM

```python
async def mock_sampling_handler(messages, params, context):
    # Retourner une réponse mockée
    return '{"matches": [{"conference_name": "Test Conf", "score": 100}]}'
```

### 4. Production avec Validation

En production, ajouter une validation avant d'appeler le vrai LLM :
```python
async def validated_sampling_handler(messages, params, context):
    # Vérifier que la demande est légitime
    if not is_valid_request(messages, params):
        return "Invalid request"

    # Appeler le vrai LLM
    return await call_real_llm(messages, params)
```

## Configuration

### Client Simple (Test)

```python
client = Client(url, sampling_handler=user_confirmation_sampling_handler)
```

### Client avec LLM (Production)

```python
from fastmcp.client.openai import OpenAISamplingHandler

handler = OpenAISamplingHandler(
    default_model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)

client = Client(url, sampling_handler=handler)
```

### Sans Handler

Si aucun handler n'est fourni, le client ne supportera pas le sampling et les appels à `ctx.sample()` échoueront.

## Documentation FastMCP

Pour plus d'informations :
- [FastMCP Sampling Clients](https://gofastmcp.com/clients/sampling)
- [FastMCP Client API](https://gofastmcp.com/clients/python)
