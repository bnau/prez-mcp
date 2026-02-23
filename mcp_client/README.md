# Client MCP Intelligent

Ce client utilise l'intelligence artificielle pour matcher automatiquement des propositions de CFP (Call for Papers) avec des conférences techniques ayant un CFP ouvert.

## Fonctionnalités

Le client effectue les opérations suivantes :

1. **Recherche de conférences** : Interroge le serveur MCP pour trouver toutes les conférences avec CFP ouvert
2. **Lecture des CFPs** : Charge tous les CFPs disponibles via les ressources MCP
3. **Analyse IA** : Utilise un modèle d'IA pour analyser la correspondance entre chaque CFP et chaque conférence
4. **Rapport détaillé** : Affiche les résultats avec scores de pertinence et explications

## Prérequis

### 1. API d'inférence

Le client nécessite une API compatible OpenAI disponible sur `http://localhost:4141`.

Vous pouvez utiliser :
- **GitHub Copilot CLI** avec accès API
- **Ollama** avec un modèle compatible
- **LM Studio** en mode serveur
- Tout autre serveur compatible avec l'API OpenAI

### 2. Serveur MCP

Le serveur MCP doit être démarré sur `http://127.0.0.1:8000/mcp`.

```bash
# Terminal 1 : Démarrer le serveur MCP
uv run python mcp_server/server.py
```

## Utilisation

```bash
# Terminal 2 : Exécuter le client intelligent
uv run python mcp_client/client.py
```

## Exemple de sortie

```
====================================================================================================
🔍 RECHERCHE DES CONFÉRENCES AVEC CFP OUVERT
====================================================================================================

📊 42 conférences trouvées avec CFP ouvert

====================================================================================================
📚 LECTURE DES CFPs DISPONIBLES
====================================================================================================

✅ CFP 'ide' chargé
   📝 Titre: Copilot, Cursor & cie : Explorons le vaste monde des assistants de code boostés par IA
   📊 Taille: 1823 caractères
✅ CFP 'kagent' chargé
   📝 Titre: KAgent + KServe: Le combo parfait pour industrialiser ses propres agents IA
   📊 Taille: 1735 caractères
✅ CFP 'mcp' chargé
   📝 Titre: MCP en pratique : une application pour tout comprendre
   📊 Taille: 1808 caractères

====================================================================================================
🎯 MATCHING CFPs <-> CONFÉRENCES (analyse IA en cours...)
====================================================================================================

🔄 Analyse du CFP 'ide' (42 conférences à évaluer)...
   ✅ 8 match(s) trouvé(s)

🔄 Analyse du CFP 'kagent' (42 conférences à évaluer)...
   ✅ 12 match(s) trouvé(s)

🔄 Analyse du CFP 'mcp' (42 conférences à évaluer)...
   ✅ 15 match(s) trouvé(s)

====================================================================================================
📋 RÉSULTATS DÉTAILLÉS
====================================================================================================

====================================================================================================
📝 CFP: IDE
   Copilot, Cursor & cie : Explorons le vaste monde des assistants de code boostés par IA
====================================================================================================

🎉 8 conférence(s) correspondante(s) trouvée(s):

  1. 🌟 DevOps World 2026
     📅 Date: 2026-05-15 → 2026-05-17
     📍 Lieu: San Francisco, USA
     🏷️  Tags: devops, ai, tools
     📊 Score de pertinence: 85/100
     💡 Analyse IA: Le tag 'ai' et 'tools' correspondent au thème des assistants de code IA
     ⏰ Deadline CFP: 2026-03-15
     🔗 Site: https://devopsworld.example.com
     📝 Lien CFP: https://devopsworld.example.com/cfp
```

## Architecture

### Classe `AIMatcherClient`

Gère les interactions avec l'API d'inférence :
- Envoie des prompts structurés pour analyser la correspondance
- Parse les réponses JSON de l'IA
- Gère les erreurs et les timeouts

### Fonction `run_intelligent_client()`

Orchestration du workflow :
1. Connexion au serveur MCP
2. Récupération des conférences et CFPs
3. Analyse IA pour chaque paire CFP/conférence
4. Affichage des résultats triés par score

## Personnalisation

### Changer le modèle d'IA

Dans `client.py`, ligne 62, modifiez le paramètre `model` :

```python
"model": "gpt-4o-mini",  # Ou "gpt-4o", "claude-sonnet-4", etc.
```

### Modifier le seuil de matching

Dans `client.py`, ligne 180, ajustez le score minimum :

```python
if match_result["match"] and match_result["score"] >= 30:  # Seuil minimum
```

### Changer l'URL de l'API

Passez l'URL au constructeur :

```python
ai_matcher = AIMatcherClient(base_url="http://votre-api:8080")
```

## Dépannage

### Erreur : "Erreur de connexion au serveur MCP"

- Vérifiez que le serveur MCP est démarré : `curl http://127.0.0.1:8000/mcp/sse`
- Redémarrez le serveur : `uv run python mcp_server/server.py`

### Erreur : "Erreur API: 404" ou "Connection refused" pour l'IA

- Vérifiez que votre API d'inférence est disponible : `curl http://localhost:4141/v1/models`
- Vérifiez que le modèle `gpt-4o-mini` est disponible dans la liste

### Résultats vides ou peu de matches

- Vérifiez qu'il y a bien des conférences avec CFP ouvert
- Ajustez le seuil de score (ligne 180)
- Vérifiez que les CFPs sont bien chargés (section "LECTURE DES CFPs")

## Développement futur

Idées d'amélioration :
- Cache des résultats d'analyse pour éviter de réanalyser les mêmes conférences
- Export des résultats en JSON/CSV
- Interface web pour visualiser les matches
- Notification automatique quand de nouvelles conférences matchent
- Analyse sémantique plus profonde du contenu des CFPs
