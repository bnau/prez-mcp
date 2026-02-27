"""Test de l'élicitation intégrée dans search_conferences."""

import asyncio
import json

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

        # Réponse oui/non
        if answer in ["y", "yes", "o", "oui"]:
            print("✅ Réponse: Oui\n")
            return ElicitResult(action="accept", content=True)

        if answer in ["n", "no", "non"]:
            print("❌ Réponse: Non\n")
            return ElicitResult(action="accept", content=False)

        # Réponse invalide
        print("⚠️  Réponse invalide. Utilisez 'y' pour oui, 'n' pour non.")


async def test_elicitation_in_search():
    """Test du matching CFP avec élicitation intégrée."""
    mcp_url = "http://127.0.0.1:8000/mcp"
    client = Client(mcp_url, elicitation_handler=elicitation_handler)

    try:
        async with client:
            print("=" * 80)
            print("🔧 Test du matching CFP avec élicitation intégrée")
            print("=" * 80)
            print()
            print("ℹ️  Le serveur va matcher les CFPs avec les conférences")
            print("ℹ️  Pour chaque match, il vous demandera si vous voulez postuler")
            print()

            print("🌍 Paramètres:")
            print("   - Country: France")
            print("   - CFP open: True")
            print("   - Match CFPs: True")
            print("   - Min score: 30")
            print()

            # Appeler le tool qui déclenche le matching et l'élicitation
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
            print("✅ RÉSULTATS FINAUX")
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
                    for idx, conf in enumerate(matches, 1):
                        score = conf.get("match_score", 0)
                        reasoning = conf.get("match_reasoning", "")
                        app_status = conf.get("application_status", "N/A")
                        wants_to_apply = conf.get("user_wants_to_apply")

                        print(f"   {idx}. {conf.get('name', 'Unknown')} (Score: {score}/100)")
                        print(f"      💡 {reasoning}")
                        print(f"      📌 Statut: {app_status}")
                        if wants_to_apply is not None:
                            apply_icon = "✅" if wants_to_apply else "❌"
                            apply_text = "Oui" if wants_to_apply else "Non"
                            print(f"      {apply_icon} Postuler: {apply_text}")
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
    asyncio.run(test_elicitation_in_search())
