"""Test du sampling handler avec confirmation utilisateur."""

import asyncio
import json

from fastmcp.client import Client
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
                import httpx

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


async def test_cfp_matching_with_handler():
    """Test du matching avec handler de confirmation utilisateur."""
    mcp_url = "http://127.0.0.1:8000/mcp"
    client = Client(mcp_url, sampling_handler=user_confirmation_sampling_handler)

    try:
        async with client:
            print("=" * 80)
            print("🔧 Test du matching CFP avec sampling handler")
            print("=" * 80)
            print()
            print("ℹ️  Le serveur va demander votre autorisation avant chaque échantillonnage LLM")
            print("ℹ️  Répondez 'y' pour autoriser ou 'n' pour refuser")
            print()

            print("🌍 Paramètres:")
            print("   - Country: France")
            print("   - CFP open: True")
            print("   - Match CFPs: True")
            print("   - Min score: 30")
            print()

            result = await client.call_tool(
                "search_conferences",
                {
                    "cfp_open": True,
                    "country": "France",
                    "match_cfps": True,
                    "min_score": 30,
                },
            )

            # Extraire le résultat
            result_text = ""
            for content_item in result.content:
                if hasattr(content_item, "text"):
                    result_text += content_item.text

            # Parser et afficher
            cfp_matches = json.loads(result_text)

            print("\n" + "=" * 80)
            print("✅ RÉSULTATS")
            print("=" * 80)
            print(f"\n📊 CFPs analysés: {len(cfp_matches)}\n")

            for cfp_name, cfp_data in cfp_matches.items():
                cfp_title = cfp_data.get("cfp_title", "Unknown")
                matches = cfp_data.get("matches", [])
                error = cfp_data.get("error")

                print(f"\n📝 CFP: {cfp_name}")
                print(f"   Titre: {cfp_title}")

                if error:
                    print(f"   ❌ Erreur: {error}")
                    continue

                if matches:
                    print(f"   🎯 Matches trouvés: {len(matches)}\n")
                    for idx, conf in enumerate(matches[:3], 1):
                        score = conf.get("match_score", 0)
                        reasoning = conf.get("match_reasoning", "")

                        print(f"   {idx}. {conf.get('name', 'Unknown')} (Score: {score}/100)")
                        print(f"      💡 {reasoning}")
                        print(f"      🏷️  Tags: {', '.join(conf.get('tags', []))}")
                        cfp_deadline = conf.get("cfp", {}).get("untilDate", "N/A")
                        print(f"      ⏰ CFP deadline: {cfp_deadline}")
                else:
                    print("   😔 Aucun match trouvé")

    except ConnectionError:
        print("❌ Erreur: Impossible de se connecter au serveur MCP")
        print("   Assurez-vous que le serveur tourne:")
        print("   uv run python mcp_server/server.py")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_cfp_matching_with_handler())
