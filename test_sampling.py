"""Quick test of search_conferences with match_cfps parameter (MCP sampling)."""

import asyncio
import json

from fastmcp.client import Client


async def test_cfp_matching():
    """Test the search_conferences tool with match_cfps parameter."""
    mcp_url = "http://127.0.0.1:8000/mcp"
    client = Client(mcp_url)

    try:
        async with client:
            print("🔧 Testing search_conferences with match_cfps=True (MCP sampling)\n")
            print("🌍 Country filter: France")
            print("📊 Min score: 30")
            print("🤖 The server will automatically read all CFP files and match them\n")

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

            # Parser et afficher - c'est maintenant un dict avec les CFPs comme clés
            cfp_matches = json.loads(result_text)

            print("✅ Results:")
            print(f"   - CFPs analyzed: {len(cfp_matches)}\n")

            for cfp_name, cfp_data in cfp_matches.items():
                cfp_title = cfp_data.get("cfp_title", "Unknown")
                matches = cfp_data.get("matches", [])
                error = cfp_data.get("error")

                print(f"\n📝 CFP: {cfp_name}")
                print(f"   Title: {cfp_title}")

                if error:
                    print(f"   ❌ Error: {error}")
                    continue

                if matches:
                    print(f"   🎯 Matches found: {len(matches)}\n")
                    for idx, conf in enumerate(matches[:3], 1):  # Show top 3
                        score = conf.get("match_score", 0)
                        reasoning = conf.get("match_reasoning", "")

                        print(f"   {idx}. {conf.get('name', 'Unknown')} (Score: {score}/100)")
                        print(f"      💡 {reasoning}")
                        print(f"      🏷️  Tags: {', '.join(conf.get('tags', []))}")
                        cfp_deadline = conf.get("cfp", {}).get("untilDate", "N/A")
                        print(f"      ⏰ CFP deadline: {cfp_deadline}")
                else:
                    print("   😔 No matches found")

    except ConnectionError:
        print("❌ Error: Cannot connect to MCP server")
        print("   Make sure the server is running:")
        print("   uv run python mcp_server/server.py")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_cfp_matching())
