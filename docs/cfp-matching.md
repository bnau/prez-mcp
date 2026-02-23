# CFP Matching avec Sampling MCP

## Vue d'ensemble

Le serveur MCP fournit un outil `search_conferences` enrichi qui peut automatiquement matcher des CFPs (Call for Papers) avec des conférences pertinentes en utilisant le **sampling MCP côté serveur**.

Avec le paramètre `match_cfps=True`, le serveur :
1. Lit automatiquement tous les fichiers CFP disponibles
2. Analyse chaque CFP avec l'IA pour trouver les conférences correspondantes
3. Retourne les résultats groupés par CFP avec scores et raisonnements

## Architecture

### Avant (API d'inférence externe)
```
Client → API Inférence → Analyse → Client
  ↓
Serveur MCP (données uniquement)
```

### Après (Sampling MCP intégré)
```
Client → search_conferences(match_cfps=True) → Serveur MCP
                                                    ↓
                                               Lecture CFPs
                                               ctx.sample (IA)
                                               Matching
                                                    ↓
                                           Résultats groupés → Client
```

## Avantages

1. **🔒 Sécurité** : Pas besoin d'exposer une API d'inférence externe
2. **⚡ Simplicité extrême** : Un seul appel avec un booléen
3. **📦 Tout côté serveur** : Le serveur gère la lecture des CFPs et le matching
4. **🎨 Réutilisabilité** : Aucune logique métier côté client
5. **🤖 Automatique** : Plus besoin de lire manuellement les CFPs

## Utilisation

### 1. Appel simple avec matching automatique (recommandé)

```python
from fastmcp.client import Client

client = Client("http://127.0.0.1:8000/mcp")

async with client:
    # Un seul appel pour tout faire !
    result = await client.call_tool(
        "search_conferences",
        {
            "cfp_open": True,
            "country": "France",
            "match_cfps": True,  # Active le matching automatique
            "min_score": 30,
        },
    )

    # Le résultat est un dictionnaire groupé par CFP
    # {
    #   "cfp_name_1": {
    #     "cfp_title": "...",
    #     "matches": [...]
    #   },
    #   "cfp_name_2": {...}
    # }
```

### 2. Pattern avec orchestration LLM

```python
async with client:
    # 1. Récupérer le prompt du serveur
    prompt_result = await client.get_prompt(
        "find_conferences_for_open_cfps",
        {"country": "France"}
    )

    # 2. Lister les outils disponibles
    tools = await client.list_tools()

    # 3. Envoyer le prompt + outils à votre LLM
    # Le LLM va appeler search_conferences avec match_cfps=True
    # et formater les résultats
```

### 3. Résultat avec scores de matching

Quand `match_cfps=True`, le résultat est un dictionnaire :

```json
{
  "mcp": {
    "cfp_title": "Model Context Protocol et agents IA",
    "matches": [
      {
        "name": "Devoxx France 2026",
        "date": {"beginning": "2026-04-15", "end": "2026-04-17"},
        "tags": ["java", "development", "cloud"],
        "match_score": 85,
        "match_reasoning": "Conférence généraliste développement avec track AI/ML très pertinent",
        "cfp": {
          "link": "https://...",
          "untilDate": "2026-01-15"
        }
      }
    ]
  },
  "cloud_native": {
    "cfp_title": "Architecture Cloud Native et Kubernetes",
    "matches": [...]
  }
}
```

## Test rapide

```bash
# Terminal 1 : Démarrer le serveur
uv run python mcp_server/server.py

# Terminal 2 : Tester le matching
uv run python test_sampling.py

# Ou tester le workflow complet avec orchestration LLM
uv run python mcp_client/client.py
```

## Implémentation côté serveur

```python
@mcp.tool()
async def search_conferences(
    ctx: Context,  # Context pour accéder au sampling
    cfp_open: bool = False,
    country: Optional[str] = None,
    match_cfps: bool = False,  # Booléen pour activer le matching
    min_score: int = 30,
    ...
) -> list[Any] | dict[str, Any]:
    # Filtrer les conférences
    results = [...conferences filtrées...]

    # Si match_cfps est True, lire tous les CFPs et matcher
    if match_cfps:
        cfp_matches = {}

        # Lire tous les fichiers CFP du répertoire
        for cfp_file in CFP_SUBJECTS_DIR.glob("*.md"):
            cfp_content = cfp_file.read_text(encoding="utf-8")

            # Utiliser ctx.sample pour matcher
            result = await ctx.sample(
                messages=prompt_de_matching,
                temperature=0.3,
                max_tokens=4000,
            )

            # Enrichir et grouper les résultats
            cfp_matches[cfp_name] = {
                "cfp_title": title,
                "matches": [...]
            }

        return cfp_matches

    return results
```

## Comment ça marche

1. **Filtrage classique** : Le serveur filtre d'abord les conférences selon les critères (pays, CFP ouvert, dates...)

2. **Lecture automatique des CFPs** : Si `match_cfps=True` :
   - Le serveur liste tous les fichiers `.md` dans `CFP_SUBJECTS_DIR`
   - Lit le contenu de chaque CFP

3. **Sampling MCP pour chaque CFP** :
   - Extraction du titre et extrait du CFP
   - Préparation d'un prompt avec les conférences filtrées
   - Appel à `ctx.sample()` pour analyser les correspondances
   - Le LLM retourne un JSON avec scores et raisonnements

4. **Groupement des résultats** :
   - Les résultats sont groupés par CFP
   - Chaque CFP contient : `cfp_title` et `matches`
   - Chaque match inclut : `match_score` (0-100) et `match_reasoning`
   - Les matches sont triés par score décroissant

## Comparaison avec l'ancienne approche

### Avant
- Client liste les ressources MCP
- Client lit chaque CFP via `read_resource`
- Client appelle une API d'inférence externe pour chaque CFP
- Client fait le matching et l'enrichissement
- Code de matching complexe côté client (étapes 4, 5, 6)

### Après (avec match_cfps)
- Client appelle `search_conferences` avec `match_cfps=True`
- **Le serveur fait tout automatiquement** :
  - Lecture des CFPs depuis le filesystem
  - Sampling MCP pour chaque CFP
  - Matching et enrichissement
  - Groupement des résultats
- Code client minimal : **un seul appel**
- Plus besoin de `list_resources` ni `read_resource`

## Paramètres de l'outil

| Paramètre | Type | Optionnel | Description |
|-----------|------|-----------|-------------|
| `ctx` | Context | Non | Context FastMCP (injecté automatiquement) |
| `min_date` | date | Oui | Date minimale de conférence |
| `max_date` | date | Oui | Date maximale de conférence |
| `country` | str | Oui | Pays pour filtrer |
| `tags` | str | Oui | Tags séparés par virgules |
| `cfp_open` | bool | Oui | Filtrer sur CFP ouverts uniquement |
| `match_cfps` | bool | Oui | **Active le matching automatique des CFPs** |
| `min_score` | int | Oui | Score minimum (défaut: 30) |

## Format du résultat

### Sans matching (`match_cfps=False`)
Retourne une liste de conférences :
```json
[
  {"name": "Conf 1", "date": {...}, ...},
  {"name": "Conf 2", "date": {...}, ...}
]
```

### Avec matching (`match_cfps=True`)
Retourne un dictionnaire groupé par CFP :
```json
{
  "cfp_name": {
    "cfp_title": "Titre du CFP",
    "matches": [
      {
        "name": "Conf 1",
        "match_score": 85,
        "match_reasoning": "...",
        ...
      }
    ]
  }
}
```
