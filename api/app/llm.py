import httpx


OLLAMA_URL = "http://ollama:11434"


async def generate_chat(messages: list[dict]) -> str:
    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": "llama3.1",
                "messages": messages,
                "stream": False,
            },
        )

        response.raise_for_status()
        data = response.json()

        return data["message"]["content"]