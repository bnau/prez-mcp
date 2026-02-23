"""MCP Client intelligent utilisant le pattern Prompt -> LLM -> Tool Call."""

import asyncio
import json
from collections import defaultdict
from typing import Any

import httpx
from fastmcp.client import Client


class LLMOrchestrator:
    """Orchestrateur qui utilise un LLM pour décider quels outils MCP appeler."""

    def __init__(self, base_url: str = "http://localhost:4141"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=60.0)

    async def close(self):
        """Ferme le client HTTP."""
        await self.client.aclose()

    async def execute_prompt_with_tools(
        self, prompt_text: str, available_tools: list[dict], mcp_client: Client
    ) -> dict:
        """
        Envoie un prompt au LLM avec la liste des outils disponibles.
        Le LLM décide quels outils appeler et avec quels paramètres.

        Args:
            prompt_text: Le texte du prompt à exécuter
            available_tools: Liste des outils MCP disponibles
            mcp_client: Client MCP pour appeler les outils

        Returns:
            Dictionnaire avec les résultats
        """
        # Formater les outils pour l'API OpenAI
        tools_spec = []
        for tool in available_tools:
            tool_spec = {
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": tool["inputSchema"],
                },
            }
            tools_spec.append(tool_spec)

        # Première requête : le LLM décide quels outils appeler
        messages = [{"role": "user", "content": prompt_text}]

        print("🤖 Envoi du prompt au LLM pour qu'il décide des outils à appeler...")

        response = await self.client.post(
            f"{self.base_url}/v1/chat/completions",
            json={"model": "gpt-4o-mini", "messages": messages, "tools": tools_spec, "temperature": 0.3},
        )

        if response.status_code != 200:
            raise Exception(f"Erreur API LLM: {response.status_code} - {response.text}")

        result = response.json()
        assistant_message = result["choices"][0]["message"]

        # Si le LLM veut appeler des outils
        if "tool_calls" in assistant_message:
            print(f"🔧 Le LLM a décidé d'appeler {len(assistant_message['tool_calls'])} outil(s)\n")

            # Ajouter le message de l'assistant à l'historique
            messages.append(assistant_message)

            # Exécuter chaque tool call
            tool_results = {}
            for tool_call in assistant_message["tool_calls"]:
                function_name = tool_call["function"]["name"]
                function_args = json.loads(tool_call["function"]["arguments"])

                print(f"   📞 Appel de l'outil: {function_name}")
                print(f"   📋 Paramètres: {json.dumps(function_args, indent=6)}")

                # Appeler l'outil MCP
                try:
                    tool_result = await mcp_client.call_tool(function_name, function_args)

                    # Extraire le contenu textuel
                    result_content = ""
                    for content in tool_result.content:
                        if hasattr(content, "text"):
                            result_content += content.text

                    print(f"   ✅ Résultat reçu ({len(result_content)} caractères)\n")

                    # Stocker le résultat brut pour utilisation ultérieure
                    tool_results[function_name] = result_content

                    # Pour le LLM, envoyer juste un résumé si trop long
                    llm_content = result_content
                    if len(result_content) > 10000:
                        # Tronquer pour le LLM
                        llm_content = (
                            f"Résultat trop volumineux pour être inclus entièrement. "
                            f"Taille: {len(result_content)} caractères. "
                            f"Les données ont été stockées et seront traitées directement par le client."
                        )
                        print(
                            f"   ⚠️  Résultat trop volumineux, envoi d'un résumé au LLM au lieu du JSON complet\n"
                        )

                    # Ajouter le résultat à l'historique
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call["id"],
                            "name": function_name,
                            "content": llm_content,
                        }
                    )
                except Exception as e:
                    print(f"   ❌ Erreur lors de l'appel: {e}\n")
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call["id"],
                            "name": function_name,
                            "content": f"Erreur: {str(e)}",
                        }
                    )

            # Deuxième requête : le LLM traite les résultats des outils
            print("🤖 Le LLM analyse les résultats des outils...")
            response = await self.client.post(
                f"{self.base_url}/v1/chat/completions",
                json={"model": "gpt-4o-mini", "messages": messages, "temperature": 0.3},
            )

            if response.status_code != 200:
                error_detail = ""
                try:
                    error_detail = response.text
                except:
                    pass
                raise Exception(
                    f"Erreur API LLM (2ème requête): {response.status_code}\n{error_detail[:500]}"
                )

            result = response.json()
            final_response = result["choices"][0]["message"]["content"]

            return {
                "type": "tool_result",
                "content": final_response,
                "messages": messages,
                "raw_tool_results": tool_results,
            }

        else:
            # Le LLM a répondu directement sans appeler d'outils
            return {
                "type": "direct_response",
                "content": assistant_message.get("content", ""),
                "messages": messages,
            }

    async def analyze_cfp_match(
        self, cfp_name: str, cfp_content: str, conferences_json: str
    ) -> list[dict]:
        """
        Utilise le LLM pour analyser quelles conférences correspondent à un CFP.

        Args:
            cfp_name: Nom du CFP
            cfp_content: Contenu complet du CFP
            conferences_json: JSON des conférences disponibles

        Returns:
            Liste de matches avec scores et explications
        """
        # Extraire un résumé du CFP
        cfp_lines = cfp_content.split("\n")
        cfp_title = cfp_lines[0].replace("#", "").strip()
        cfp_summary = "\n".join(cfp_lines[:10])

        prompt = f"""Analyse quelles conférences de la liste correspondent à ce CFP.

CFP: {cfp_name}
Titre: {cfp_title}

Extrait du CFP:
{cfp_summary}

Conférences disponibles (JSON):
{conferences_json}

Pour chaque conférence, analyse si elle correspond au thème du CFP en te basant sur:
- Les tags de la conférence
- Le nom de la conférence
- Le contenu et le sujet du CFP

Réponds UNIQUEMENT avec un JSON valide (sans markdown) au format:
{{
  "matches": [
    {{
      "conference_name": "nom de la conférence",
      "match": true/false,
      "score": 0-100,
      "reasoning": "explication en français (1 phrase max)"
    }}
  ]
}}

Important:
- N'inclus dans les matches QUE les conférences qui ont un score >= 30
- Sois strict sur la pertinence des tags"""

        try:
            response = await self.client.post(
                f"{self.base_url}/v1/chat/completions",
                json={
                    "model": "gpt-4o-mini",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                },
            )

            if response.status_code != 200:
                return []

            result = response.json()
            content = result["choices"][0]["message"]["content"].strip()

            # Nettoyer la réponse si elle contient des markdown code blocks
            if content.startswith("```"):
                lines = content.split("\n")
                content = "\n".join(lines[1:-1]) if len(lines) > 2 else content

            data = json.loads(content)
            return data.get("matches", [])

        except Exception as e:
            print(f"      ⚠️ Erreur lors de l'analyse: {e}")
            return []


async def run_intelligent_client():
    """Client qui utilise le pattern Prompt -> LLM -> Tool Call."""
    mcp_url = "http://127.0.0.1:8000/mcp"
    mcp_client = Client(mcp_url)
    orchestrator = LLMOrchestrator()

    try:
        async with mcp_client:
            print("=" * 100)
            print("🎯 CLIENT MCP INTELLIGENT - Pattern Prompt → LLM → Tool Call")
            print("=" * 100)
            print()

            # Étape 1 : Récupérer le prompt du serveur MCP
            print("=" * 100)
            print("📋 ÉTAPE 1 : Récupération du prompt depuis le serveur MCP")
            print("=" * 100)
            print()

            # Demander le prompt pour les conférences en France
            prompt_result = await mcp_client.get_prompt(
                "find_conferences_for_open_cfps", {"country": "France"}
            )
            prompt_text = ""
            if hasattr(prompt_result, "messages"):
                for message in prompt_result.messages:
                    if hasattr(message.content, "text"):
                        prompt_text = message.content.text
                    else:
                        prompt_text = str(message.content)

            print("📝 Prompt reçu du serveur:")
            print("-" * 100)
            print(prompt_text)
            print("-" * 100)
            print()

            # Étape 2 : Récupérer la liste des outils disponibles
            print("=" * 100)
            print("🔧 ÉTAPE 2 : Récupération des outils MCP disponibles")
            print("=" * 100)
            print()

            tools_list = await mcp_client.list_tools()
            tools_for_llm = []
            for tool in tools_list:
                tools_for_llm.append(
                    {
                        "name": tool.name,
                        "description": tool.description,
                        "inputSchema": tool.inputSchema,
                    }
                )
                print(f"   🔧 {tool.name}: {tool.description[:80]}...")

            print()

            # Étape 3 : Envoyer le prompt au LLM avec les outils
            print("=" * 100)
            print("🤖 ÉTAPE 3 : Le LLM analyse le prompt et décide des actions")
            print("=" * 100)
            print()

            llm_result = await orchestrator.execute_prompt_with_tools(
                prompt_text, tools_for_llm, mcp_client
            )

            print("\n💬 Réponse du LLM:")
            print("-" * 100)
            print(llm_result["content"][:500] + "..." if len(llm_result["content"]) > 500 else llm_result["content"])
            print("-" * 100)
            print()

            # Étape 4 : Parser les conférences du résultat
            print("=" * 100)
            print("📊 ÉTAPE 4 : Extraction des conférences depuis les résultats des outils")
            print("=" * 100)
            print()

            # Chercher les résultats bruts des outils d'abord
            conferences = []
            if "raw_tool_results" in llm_result and "search_conferences" in llm_result["raw_tool_results"]:
                # Utiliser les résultats bruts des tool calls
                result_json = llm_result["raw_tool_results"]["search_conferences"]
                try:
                    conferences = json.loads(result_json)
                    print(f"✅ Données extraites des résultats d'outils MCP\n")
                except json.JSONDecodeError as e:
                    print(f"⚠️  Erreur de parsing JSON: {e}")

            # Fallback: chercher dans la réponse du LLM
            if not conferences:
                content = llm_result["content"]
                # Le LLM devrait avoir retourné du JSON ou une description
                try:
                    # Essayer de parser directement
                    if content.strip().startswith("[") or content.strip().startswith("{"):
                        conferences = json.loads(content)
                    else:
                        # Chercher un bloc JSON dans la réponse
                        import re

                        json_match = re.search(r"```json\s*(.*?)\s*```", content, re.DOTALL)
                        if json_match:
                            conferences = json.loads(json_match.group(1))
                        else:
                            # Chercher juste un tableau JSON
                            json_match = re.search(r"(\[.*\])", content, re.DOTALL)
                            if json_match:
                                conferences = json.loads(json_match.group(1))
                except json.JSONDecodeError:
                    print("⚠️  Aucun JSON valide trouvé, appel direct de l'outil...")

            # Fallback final : appeler directement l'outil
            if not conferences:
                result = await mcp_client.call_tool("search_conferences", {"cfp_open": True})
                for content_item in result.content:
                    if hasattr(content_item, "text"):
                        conferences = json.loads(content_item.text)

            print(f"✅ {len(conferences)} conférences avec CFP ouvert trouvées\n")

            # Étape 5 : Lire les CFPs disponibles
            print("=" * 100)
            print("📚 ÉTAPE 5 : Lecture des CFPs disponibles via ressources MCP")
            print("=" * 100)
            print()

            cfp_contents = {}
            resources_list = await mcp_client.list_resources()

            # Filtrer les ressources de CFP (fichiers .md dans sujets_cfp)
            for resource in resources_list:
                uri_str = str(resource.uri)
                # Les CFPs sont des fichiers .md
                if "sujets_cfp" in uri_str and uri_str.endswith(".md"):
                    cfp_name = resource.name  # Utiliser le nom de la ressource
                    try:
                        resource_result = await mcp_client.read_resource(uri_str)
                        content_text = ""
                        for content_item in resource_result:
                            if hasattr(content_item, "text"):
                                content_text += content_item.text
                        cfp_contents[cfp_name] = content_text
                        first_line = content_text.split("\n")[0].replace("#", "").strip()
                        print(f"   ✅ CFP '{cfp_name}' chargé")
                        print(f"      📝 {first_line}")
                    except Exception as e:
                        print(f"   ❌ Erreur lecture de {cfp_name}: {e}")

            print()

            # Étape 6 : Matching IA entre CFPs et conférences
            print("=" * 100)
            print("🎯 ÉTAPE 6 : Matching IA entre CFPs et conférences")
            print("=" * 100)
            print()

            conferences_json = json.dumps(conferences, ensure_ascii=False)
            cfp_matches = defaultdict(list)

            for cfp_name, cfp_content in cfp_contents.items():
                print(f"🔄 Analyse du CFP '{cfp_name}'...")

                matches = await orchestrator.analyze_cfp_match(
                    cfp_name, cfp_content, conferences_json
                )

                for match_data in matches:
                    if match_data.get("match") and match_data.get("score", 0) >= 30:
                        # Trouver la conférence correspondante
                        conf_name = match_data["conference_name"]
                        conf = next((c for c in conferences if c["name"] == conf_name), None)

                        if conf:
                            cfp_matches[cfp_name].append(
                                {
                                    "conference": conf,
                                    "match_score": match_data["score"],
                                    "reasoning": match_data["reasoning"],
                                }
                            )

                print(f"   ✅ {len(cfp_matches[cfp_name])} match(s) trouvé(s)\n")

            # Étape 7 : Affichage des résultats
            print("=" * 100)
            print("📋 RÉSULTATS FINAUX - Matches CFP ↔ Conférences")
            print("=" * 100)
            print()

            for cfp_name in sorted(cfp_contents.keys()):
                cfp_content = cfp_contents[cfp_name]
                cfp_title = cfp_content.split("\n")[0].replace("#", "").strip()

                print(f"\n{'=' * 100}")
                print(f"📝 CFP: {cfp_name.upper()}")
                print(f"   {cfp_title}")
                print(f"{'=' * 100}\n")

                matches = cfp_matches[cfp_name]
                if matches:
                    matches.sort(key=lambda x: x["match_score"], reverse=True)
                    print(f"🎉 {len(matches)} conférence(s) correspondante(s):\n")

                    for idx, match in enumerate(matches, 1):
                        conf = match["conference"]
                        score = match["match_score"]
                        reasoning = match["reasoning"]

                        date_info = conf.get("date", {})
                        date_str = "Date non disponible"
                        if date_info:
                            start = date_info.get("beginning", "")
                            end = date_info.get("end", "")
                            if start and end:
                                date_str = f"{start} → {end}"
                            elif start:
                                date_str = start

                        cfp_info = conf.get("cfp", {})
                        cfp_deadline = cfp_info.get("untilDate", "N/A")

                        location_parts = []
                        if conf.get("city"):
                            location_parts.append(conf["city"])
                        if conf.get("country"):
                            location_parts.append(conf["country"])
                        location = ", ".join(location_parts) if location_parts else "En ligne"

                        score_emoji = "🌟" if score >= 80 else "🎯" if score >= 60 else "✨"

                        print(f"  {idx}. {score_emoji} {conf['name']}")
                        print(f"     📅 Date: {date_str}")
                        print(f"     📍 Lieu: {location}")
                        print(f"     🏷️  Tags: {', '.join(conf.get('tags', []))}")
                        print(f"     📊 Score: {score}/100")
                        print(f"     💡 {reasoning}")
                        print(f"     ⏰ Deadline CFP: {cfp_deadline}")
                        if conf.get("hyperlink"):
                            print(f"     🔗 {conf['hyperlink']}")
                        if cfp_info.get("link"):
                            print(f"     📝 CFP: {cfp_info['link']}")
                        print()
                else:
                    print("😔 Aucune conférence correspondante\n")

            # Statistiques
            print("\n" + "=" * 100)
            print("📊 STATISTIQUES FINALES")
            print("=" * 100)
            print(f"\n✅ CFPs analysés: {len(cfp_contents)}")
            print(f"✅ Conférences avec CFP ouvert: {len(conferences)}")
            total_matches = sum(len(matches) for matches in cfp_matches.values())
            print(f"✅ Matches trouvés: {total_matches}")

            print("\n🏆 MEILLEUR MATCH PAR CFP:")
            for cfp_name in sorted(cfp_contents.keys()):
                matches = cfp_matches[cfp_name]
                if matches:
                    best = max(matches, key=lambda x: x["match_score"])
                    print(f"   • {cfp_name}: {best['conference']['name']} ({best['match_score']}/100)")
            print()

    finally:
        await orchestrator.close()


async def main():
    """Point d'entrée principal."""
    try:
        await run_intelligent_client()
    except ConnectionError as e:
        print("❌ Erreur de connexion")
        print("   Serveur MCP: http://127.0.0.1:8000/mcp")
        print("   API d'inférence: http://localhost:4141")
        print(f"   Détails: {e}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
