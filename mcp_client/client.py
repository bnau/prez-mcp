#region Imports
import asyncio
import json

import httpx
from fastmcp.client import Client
from fastmcp.client.elicitation import ElicitResult
from fastmcp.client.sampling import RequestContext, SamplingMessage, SamplingParams
#endregion

#region Sampling Handler
async def sampling_handler(
    messages: list[SamplingMessage],
    params: SamplingParams,
    context: RequestContext,
):
    #region Affichage du prompt envoyé par le serveur
    content_text = messages[0].content.text

    print()
    print()
    print("📢 New sampling request from server")
    print("🤖 Server requests an LLM call:")
    print("-" * 80)
    if len(content_text) > 400:
        print(content_text[:400] + "...")
    else:
        print(content_text)
    print("-" * 80)
    #endregion

    #region Demande de confirmation à l'utilisateur
    response = input("Allow? (y/n): ").strip().lower()

    if response in ["n", "no", "non"]:
        return '{"error": "Sampling denied by user"}'

    if response not in ["y", "yes", "o", "oui"]:
        print("⚠️  Invalid response. Use 'y' or 'n'.")
        return '{"error": "Invalid user response"}'
    #endregion

    #region Appel au LLM
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "http://localhost:4141/v1/chat/completions",
                json={
                    "model": "gpt-4o-mini",
                    "messages": [{"role": message.role, "content": message.content.text} for message in messages],
                    "temperature": params.temperature,
                    "max_tokens": params.maxTokens,
                },
            )

            result = response.json()
            return result["choices"][0]["message"]["content"]

    except Exception as e:
        return f'{{"error": "{str(e)}"}}'
    #endregion
#endregion

#region Elicitation Handler
async def elicitation_handler(prompt: str, response_type: type | None, params, context):
    print()
    print()
    print("📢 New elicitation request from server")
    print(prompt)
    answer = input("Answer (y/n or 'cancel' to abort): ").strip().lower()

    if answer == "cancel":
        print("⚠️  Operation cancelled\n")
        return ElicitResult(action="cancel")

    if answer in ["y", "yes", "o", "oui"]:
            print("✅ Answer: Yes\n")
            return ElicitResult(action="accept")

    if answer in ["n", "no", "non"]:
            print("❌ Answer: No\n")
            return ElicitResult(action="decline")

    print("⚠️  Invalid response. Use 'y' for yes, 'n' for no.")
#endregion

async def main():
    mcp_client = Client(
        "http://127.0.0.1:8001/mcp",
        sampling_handler=sampling_handler,
        elicitation_handler=elicitation_handler,
    )

    async with mcp_client:
        #region Récupération des outils MCP disponibles
        tools_list = await mcp_client.list_tools()

        openai_tools = [{
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema,
            }
        } for tool in tools_list]
        #endregion

        #region Appel au LLM avec tool calling
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "http://localhost:4141/v1/chat/completions",
                json={
                    "model": "gpt-4o-mini",
                    "messages": [{"role": "user",
                                  "content": "Je voudrais candidater aux conférences en France en mai 2026 pour parler de MCP"}],
                    "tools": openai_tools,
                    "tool_choice": "auto",
                },
            )

            result = response.json()
            message = result["choices"][0]["message"]

            print(f"🤖 LLM: {message.get('content', '(calling tool)')}")
        #endregion

        #region Exécution de l'appel d'outil si demandé
        result = None
        if message.get("tool_calls"):
            tool_call = message["tool_calls"][0]
            function_name = tool_call["function"]["name"]
            function_args = json.loads(tool_call["function"]["arguments"])

            print(f"\n🔧 Tool call: {function_name}")
            print(f"📋 Arguments: {json.dumps(function_args, indent=2)}")

            result = await mcp_client.call_tool(function_name, function_args)
        #endregion

        #region Affichage des résultats
        print("\n✅ Result:")
        for content in result.content:
            if hasattr(content, "text"):
                data = json.loads(content.text)
                print("You applied to:")
                for conf in data['applied_confs']:
                    print(f"  - {conf}")
        #endregion


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Error: {e}")