# Élicitation MCP avec Confirmation Utilisateur

## Vue d'ensemble

L'élicitation MCP permet au **serveur** de demander une confirmation ou une information à l'utilisateur via le **client**. C'est l'inverse du sampling : au lieu que le client demande au serveur d'analyser des données avec l'IA, c'est le serveur qui demande une réponse à l'utilisateur.

Dans notre implémentation, l'élicitation est **intégrée dans le tool `search_conferences`** : après avoir matché les CFPs avec les conférences via sampling, le serveur demande à l'utilisateur s'il veut postuler à chaque conférence matchée.

## Pourquoi l'Élicitation ?

Quand le serveur MCP utilise `ctx.elicit()`, il peut :
- ✅ **Demander confirmation** à l'utilisateur avant une action
- ✅ **Obtenir une réponse** yes/no, texte libre, ou données structurées
- ✅ **Rendre les outils interactifs** sans logique côté client
- ✅ **Valider des choix** avant de les exécuter

## Architecture

```
Client → call_tool("search_conferences", match_cfps=True) → Serveur
                                                              ↓
                                                        Filtrage + ctx.sample (matching)
                                                              ↓
                                                        Pour chaque match:
                                                          ctx.elicit("Voulez-vous postuler ?")
                                                              ↓
Client ← Question ← Serveur
   ↓
elicitation_handler (affiche + demande réponse y/n)
   ↓
Client → Réponse (true/false) → Serveur
                                   ↓
                              Ajoute "application_status" au match
                                   ↓
Client ← Résultats avec statuts ← Serveur
```

## Workflow Complet

1. **Filtrage** : Le serveur filtre les conférences selon les critères (pays, CFP ouvert, dates...)
2. **Lecture CFPs** : Le serveur lit tous les fichiers CFP disponibles
3. **Sampling** : Pour chaque CFP, le serveur utilise `ctx.sample()` pour matcher avec les conférences
4. **Élicitation** : Pour chaque match trouvé, le serveur utilise `ctx.elicit()` pour demander confirmation
5. **Réponse utilisateur** : L'utilisateur répond y/n via le handler d'élicitation côté client
6. **Enrichissement** : Le serveur ajoute `user_wants_to_apply` et `application_status` à chaque match
7. **Retour** : Le client reçoit les résultats avec les statuts de candidature

## Implémentation Serveur

### Outil avec Élicitation Intégrée

```python
@mcp.tool(name="search_conferences", ...)
async def search_conferences(
    ctx: Context,
    ...,
    match_cfps: bool = False,
    min_score: int = 30,
) -> list[Any] | dict[str, Any]:
    # ... filtrage et sampling pour matcher les CFPs ...

    if match_cfps:
        for cfp_file in CFP_SUBJECTS_DIR.glob("*.md"):
            # ... lecture du CFP ...

            # Sampling pour trouver les matches
            result = await ctx.sample(messages=sampling_prompt, ...)

            # Pour chaque match, demander confirmation
            for match in scored_results:
                conf_name = match.get("name", "Unknown")
                match_score = match.get("match_score", 0)

                # Utiliser l'élicitation
                prompt = (
                    f"Voulez-vous postuler au CFP de la conférence '{conf_name}' "
                    f"avec votre sujet '{cfp_title}' (score: {match_score}/100) ?"
                )

                elicit_result = await ctx.elicit(prompt, response_type=bool)

                # Ajouter le résultat au match
                if elicit_result.action == "accept":
                    match["user_wants_to_apply"] = elicit_result.data
                    if elicit_result.data:
                        match["application_status"] = f"✅ Vous allez postuler à '{conf_name}'"
                    else:
                        match["application_status"] = f"❌ Vous ne postulerez pas à '{conf_name}'"
                elif elicit_result.action == "decline":
                    match["user_wants_to_apply"] = None
                    match["application_status"] = "ℹ️ Vous avez décliné de répondre"
                else:
                    match["user_wants_to_apply"] = None
                    match["application_status"] = "⚠️ Opération annulée"

            # Stocker les matches avec les statuts
            cfp_matches[cfp_name] = {
                "cfp_title": cfp_title,
                "matches": scored_results,
            }

        return cfp_matches

    return results
```

### Types de Réponses Supportés

L'élicitation supporte plusieurs types de réponses :

| Type | Description | Exemple |
|------|-------------|---------|
| `bool` | Oui/Non | `ctx.elicit(prompt, response_type=bool)` |
| `str` | Texte libre | `ctx.elicit(prompt, response_type=str)` |
| `int` | Nombre entier | `ctx.elicit(prompt, response_type=int)` |
| `None` | Juste une confirmation | `ctx.elicit(prompt, response_type=None)` |
| Dataclass/Pydantic | Données structurées | `ctx.elicit(prompt, response_type=MyDataClass)` |

### Actions de Résultat

Le résultat de `ctx.elicit()` contient :
- `action` : `"accept"`, `"decline"`, ou `"cancel"`
- `data` : Les données de la réponse (si `action == "accept"`)

## Implémentation Client

### Handler d'Élicitation

```python
from fastmcp.client import Client
from fastmcp.client.elicitation import ElicitResult


async def elicitation_handler(prompt: str, response_type: type | None, params, context):
    """
    Handler d'élicitation qui demande une réponse y/n à l'utilisateur.

    Args:
        prompt: Le texte de la question posée par le serveur
        response_type: Le type de réponse attendu (bool dans notre cas)
        params: Paramètres d'élicitation
        context: Contexte de la requête
    """
    print(f"\n❓ {prompt}\n")

    # Boucle pour obtenir une réponse valide
    while True:
        answer = input("Répondez (y/n ou 'cancel' pour annuler): ").strip().lower()

        # Annuler l'opération
        if answer == "cancel":
            print("⚠️  Opération annulée\n")
            return ElicitResult(action="cancel")

        # Décliner de répondre
        if answer == "decline":
            print("ℹ️  Vous avez décliné de répondre\n")
            return ElicitResult(action="decline")

        # Réponse oui/non
        if answer in ["y", "yes", "o", "oui"]:
            print("✅ Réponse: Oui\n")
            return ElicitResult(action="accept", content=True)

        if answer in ["n", "no", "non"]:
            print("❌ Réponse: Non\n")
            return ElicitResult(action="accept", content=False)

        # Réponse invalide
        print("⚠️  Réponse invalide. Utilisez 'y' pour oui, 'n' pour non.")
```

### Enregistrement du Handler

Le handler d'élicitation peut être enregistré de deux façons :

#### Option 1 : Client de test dédié

```python
from fastmcp.client import Client

client = Client(
    "http://127.0.0.1:8000/mcp",
    elicitation_handler=elicitation_handler
)

async with client:
    result = await client.call_tool(
        "ask_to_apply",
        {
            "conference_name": "Devoxx France 2026",
            "cfp_title": "Model Context Protocol et agents IA",
            "match_score": 85,
        },
    )
```

#### Option 2 : Client intelligent avec sampling + élicitation

Le client principal (`mcp_client/client.py`) supporte à la fois le sampling et l'élicitation :

```python
from fastmcp.client import Client

mcp_client = Client(
    mcp_url,
    sampling_handler=user_confirmation_sampling_handler,
    elicitation_handler=elicitation_handler,
)
```

Cela permet d'avoir un client complet qui gère :
- **Sampling** : Le serveur demande une analyse IA au client
- **Élicitation** : Le serveur demande une confirmation utilisateur au client

## Test

### Fichier de test : `test_elicitation.py`

```bash
# Terminal 1 : Démarrer le serveur
uv run python mcp_server/server.py

# Terminal 2 : Tester le matching avec élicitation
uv run python test_elicitation.py
```

### Workflow

1. Le client appelle `search_conferences` avec `match_cfps=True`
2. Le serveur filtre les conférences et lit les CFPs
3. Pour chaque CFP, le serveur utilise `ctx.sample()` pour trouver les matches
4. Pour chaque match trouvé, le serveur appelle `ctx.elicit()` pour demander confirmation
5. Le client reçoit la demande d'élicitation via le handler
6. **L'utilisateur voit** la question du serveur pour chaque match
7. **L'utilisateur répond** pour chaque match :
   - `y` → Le handler retourne `ElicitResult(action="accept", content=True)`
   - `n` → Le handler retourne `ElicitResult(action="accept", content=False)`
   - `cancel` → Le handler retourne `ElicitResult(action="cancel")`
   - `decline` → Le handler retourne `ElicitResult(action="decline")`
8. Le serveur enrichit chaque match avec `user_wants_to_apply` et `application_status`
9. Le client reçoit les résultats finaux avec les statuts de candidature

## Exemple de Sortie

```
================================================================================
🔧 Test du matching CFP avec élicitation intégrée
================================================================================

ℹ️  Le serveur va matcher les CFPs avec les conférences
ℹ️  Pour chaque match, il vous demandera si vous voulez postuler

🌍 Paramètres:
   - Country: France
   - CFP open: True
   - Match CFPs: True
   - Min score: 30

[Le serveur utilise ctx.sample() pour matcher les CFPs...]

================================================================================
❓ Le serveur demande une confirmation
================================================================================

Voulez-vous postuler au CFP de la conférence 'Devoxx France 2026' avec votre sujet 'Model Context Protocol et agents IA' (score de match: 85/100) ?

Répondez (y/n ou 'cancel' pour annuler): y
✅ Réponse: Oui

[Élicitations suivantes pour les autres matches...]

================================================================================
✅ RÉSULTATS FINAUX
================================================================================

📊 CFPs analysés: 2

📝 CFP: mcp
   Titre: Model Context Protocol et agents IA
   🎯 Matches trouvés: 3

   1. Devoxx France 2026 (Score: 85/100)
      💡 Conférence généraliste développement avec track AI/ML très pertinent
      📌 Statut: ✅ Vous allez postuler à 'Devoxx France 2026'
      ✅ Postuler: Oui
      🏷️  Tags: java, development, cloud
      ⏰ CFP deadline: 2026-01-15

   2. Paris Web 2026 (Score: 60/100)
      💡 Conférence web avec session sur les nouveaux protocoles
      📌 Statut: ❌ Vous ne postulerez pas à 'Paris Web 2026'
      ❌ Postuler: Non
      🏷️  Tags: web, frontend, accessibility
      ⏰ CFP deadline: 2026-02-28
```

## Différence avec le Sampling

| Aspect | Sampling | Élicitation |
|--------|----------|-------------|
| **Direction** | Client → Serveur (demande analyse IA) | Serveur → Client (demande info utilisateur) |
| **Initiateur** | Serveur appelle `ctx.sample()` | Serveur appelle `ctx.elicit()` |
| **Handler** | `sampling_handler` côté client | `elicitation_handler` côté client |
| **Réponse** | LLM génère du texte | Utilisateur fournit des données |
| **Cas d'usage** | Analyse, matching, génération | Confirmation, validation, input |

## Cas d'Usage

### 1. Confirmation d'Actions

Demander confirmation avant une action importante :
```python
result = await ctx.elicit(
    "Êtes-vous sûr de vouloir supprimer cette ressource ?",
    response_type=bool
)
```

### 2. Validation de Choix

Valider un choix parmi plusieurs options :
```python
result = await ctx.elicit(
    "Quelle conférence préférez-vous : Devoxx France ou Paris Web ?",
    response_type=str
)
```

### 3. Collecte d'Informations

Demander des informations supplémentaires :
```python
result = await ctx.elicit(
    "Quel est votre budget maximum pour les frais de déplacement ?",
    response_type=int
)
```

### 4. Workflow Interactif

Créer un workflow interactif avec plusieurs étapes :
```python
# Étape 1 : Choisir une conférence
conf_result = await ctx.elicit("Quelle conférence ?", response_type=str)

# Étape 2 : Confirmer la soumission
if conf_result.action == "accept":
    confirm = await ctx.elicit(
        f"Confirmer la soumission à {conf_result.data} ?",
        response_type=bool
    )
```

## Configuration

### Client avec Handler d'Élicitation

```python
client = Client(url, elicitation_handler=elicitation_handler)
```

### Sans Handler

Si aucun handler n'est fourni, le client ne supportera pas l'élicitation et les appels à `ctx.elicit()` échoueront.

## Documentation FastMCP

Pour plus d'informations :
- [FastMCP Elicitation Servers](https://gofastmcp.com/servers/elicitation)
- [FastMCP Elicitation Clients](https://gofastmcp.com/clients/elicitation)

## Combinaison Sampling + Élicitation

Vous pouvez combiner sampling et élicitation dans le même outil :

```python
@mcp.tool()
async def smart_cfp_submission(ctx: Context, cfp_title: str) -> str:
    # 1. Utiliser le sampling pour trouver les meilleures conférences
    analysis = await ctx.sample(
        messages=f"Trouve les meilleures conférences pour le sujet: {cfp_title}",
        temperature=0.3,
    )

    # 2. Utiliser l'élicitation pour demander confirmation
    result = await ctx.elicit(
        f"Voulez-vous postuler aux conférences suggérées ?",
        response_type=bool
    )

    if result.action == "accept" and result.data:
        return "✅ Soumission confirmée !"
    else:
        return "❌ Soumission annulée."
```

Cela permet de créer des outils puissants qui :
1. Analysent les données avec l'IA (sampling)
2. Demandent confirmation à l'utilisateur (élicitation)
3. Exécutent l'action validée