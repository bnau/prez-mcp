"""MCP Client intelligent utilisant le pattern Prompt -> LLM -> Tool Call."""

import asyncio
import json

import httpx
from fastmcp.client import Client
from fastmcp.client.elicitation import ElicitResult
from fastmcp.client.sampling import RequestContext, SamplingMessage, SamplingParams


async def user_confirmation_sampling_handler(
    messages: list[SamplingMessage],
    params: SamplingParams,
    context: RequestContext,
) -> str:
    """
    Sampling handler qui demande une confirmation y/n à l'utilisateur.

    Ce handler est appelé par le serveur MCP quand il a besoin d'un échantillonnage LLM.
    Si l'utilisateur accepte, on appelle le LLM et on retourne sa réponse JSON.
    """
    print("\n" + "=" * 80)
    print("🤖 Le serveur MCP demande un échantillonnage LLM")
    print("=" * 80)

    # Afficher le system prompt si présent
    if params.systemPrompt:
        print("\n📋 System Prompt:")
        print("-" * 80)
        print(params.systemPrompt[:500])
        if len(params.systemPrompt) > 500:
            print("... (tronqué)")
        print("-" * 80)

    # Afficher les messages
    print("\n💬 Messages:")
    print("-" * 80)
    for i, message in enumerate(messages, 1):
        role_emoji = "👤" if message.role == "user" else "🤖"
        print(f"{role_emoji} Message {i} ({message.role}):")

        # Extraire le contenu
        content_text = ""
        if hasattr(message.content, "text"):
            content_text = message.content.text
        else:
            content_text = str(message.content)

        # Afficher un extrait
        if len(content_text) > 300:
            print(content_text[:300] + "... (tronqué)")
        else:
            print(content_text)
        print()

    print("-" * 80)

    # Afficher les paramètres de sampling
    print("\n⚙️  Paramètres de sampling:")
    if params.temperature is not None:
        print(f"   - Temperature: {params.temperature}")
    if params.maxTokens is not None:
        print(f"   - Max tokens: {params.maxTokens}")
    if params.modelPreferences:
        print(f"   - Model preferences: {params.modelPreferences}")

    # Demander confirmation à l'utilisateur
    print("\n" + "=" * 80)
    while True:
        prompt_msg = "❓ Voulez-vous autoriser cet échantillonnage LLM ? (y/n): "
        response = input(prompt_msg).strip().lower()
        if response in ["y", "yes", "o", "oui"]:
            print("✅ Échantillonnage autorisé")
            print("🔄 Appel du LLM...\n")

            # Construire les messages pour l'API OpenAI
            llm_messages = []

            # Ajouter le system prompt si présent
            if params.systemPrompt:
                llm_messages.append({"role": "system", "content": params.systemPrompt})

            # Ajouter les messages du sampling
            for message in messages:
                content_text = ""
                if hasattr(message.content, "text"):
                    content_text = message.content.text
                else:
                    content_text = str(message.content)

                llm_messages.append({"role": message.role, "content": content_text})

            # Appeler le LLM
            try:
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

                    if response.status_code != 200:
                        error_msg = f"Erreur API LLM: {response.status_code}"
                        print(f"❌ {error_msg}")
                        return f'{{"error": "{error_msg}"}}'

                    result = response.json()
                    llm_response = result["choices"][0]["message"]["content"]

                    print(f"✅ Réponse du LLM reçue ({len(llm_response)} caractères)")
                    return llm_response

            except Exception as e:
                error_msg = f"Erreur lors de l'appel LLM: {str(e)}"
                print(f"❌ {error_msg}")
                return f'{{"error": "{error_msg}"}}'

        elif response in ["n", "no", "non"]:
            print("❌ Échantillonnage refusé\n")
            # Retourner une réponse négative
            return '{"error": "Sampling denied by user"}'
        else:
            print("⚠️  Réponse invalide. Utilisez 'y' ou 'n'.")


async def elicitation_handler(prompt: str, response_type: type | None, params, context):
    """
    Handler d'élicitation qui demande une réponse y/n à l'utilisateur.

    Ce handler est appelé par le serveur MCP quand il a besoin d'une confirmation
    ou d'une information de la part de l'utilisateur.

    Args:
        prompt: Le texte de la question posée par le serveur
        response_type: Le type de réponse attendu (bool, str, int, None, ou dataclass)
        params: Paramètres d'élicitation
        context: Contexte de la requête
    """
    print("\n" + "=" * 80)
    print("❓ Le serveur demande une confirmation")
    print("=" * 80)
    print(f"\n{prompt}\n")

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

        # Réponse oui/non pour type bool
        if answer in ["y", "yes", "o", "oui"]:
                print("✅ Réponse: Oui\n")
                return ElicitResult(action="accept", content=True)

        if answer in ["n", "no", "non"]:
                print("❌ Réponse: Non\n")
                return ElicitResult(action="accept", content=False)

        # Pour d'autres types, accepter directement la réponse
        elif response_type is str:
            print(f"✅ Réponse: {answer}\n")
            return ElicitResult(action="accept", content=answer)

        # Réponse invalide
        print("⚠️  Réponse invalide. Utilisez 'y' pour oui, 'n' pour non.")


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
            json={
                "model": "gpt-4o-mini",
                "messages": messages,
                "tools": tools_spec,
                "temperature": 0.3,
            },
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
                            "Résultat trop volumineux pour être inclus entièrement. "
                            f"Taille: {len(result_content)} caractères. "
                            "Les données ont été stockées et seront traitées "
                            "directement par le client."
                        )
                        print(
                            "   ⚠️  Résultat trop volumineux, envoi d'un résumé "
                            "au LLM au lieu du JSON complet\n"
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
                except Exception:
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


async def run_intelligent_client():
    """Client qui utilise le pattern Prompt -> LLM -> Tool Call."""
    mcp_url = "http://127.0.0.1:8000/mcp"
    mcp_client = Client(
        mcp_url,
        sampling_handler=user_confirmation_sampling_handler,
        elicitation_handler=elicitation_handler,
    )
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

            print("\n💬 Réponse finale du LLM:")
            print("=" * 100)
            content = llm_result["content"]
            print(content)
            print("=" * 100)
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
