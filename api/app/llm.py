import httpx
import json
from typing import AsyncGenerator, List, Dict
from app.core.config import settings


class LLMService:
    def __init__(self):
        self.base_url = settings.OLLAMA_URL
        self.model = settings.MODEL

    async def generate_chat(
        self,
        messages: list[dict]
    ) -> str:
        async with httpx.AsyncClient(timeout=120) as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                },
            ) as response:
                full = ""
                async for line in response.aiter_lines():
                    if not line:
                        continue
                    data = json.loads(line)
                    if "message" in data:
                        full += data["message"].get("content", "")
                return full
            
            
    async def stream_chat(
        self,
        messages: List[Dict[str, str]],
    ) -> AsyncGenerator[str, None]:

        async with httpx.AsyncClient(timeout=120) as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": True,
                },
            ) as response:

                async for chunk in response.aiter_bytes():
                    text = chunk.decode("utf-8")

                    for line in text.split("\n"):
                        if not line.startswith("{"):
                            continue

                        data = json.loads(line)

                        if "message" in data:
                            token = data["message"].get("content")
                            if token:
                                yield data["message"]["content"]

""" THIS IS A NON WORKING IMPLMENETATION, IM REVERTING TO EASIER MORE DIRECT GENERATION
    async def _call_ollama(self, messages, isStream: bool):
        async with httpx.AsyncClient(timeout=120) as client:
            return client.stream(
                "POST",
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": isStream,
                },
            )

    async def stream_chat(
        self,
        messages: List[Dict[str, str]],
    ) -> AsyncGenerator[str, None]:
   
        async with await self._call_ollama(messages, True) as response:
            async for line in response.aiter_lines():
                if not line:
                    continue

                data = json.loads(line)

                if "message" in data:
                    token = data["message"].get("content")
                    if token:
                        yield token

                if data.get("done"):
                    break

    async def generate_chat(
        self,
        messages: list[dict]
    ) -> str:
        full = ""
        async with await self._call_ollama(messages, False) as response:
            async for line in response.aiter_lines():
                if not line:
                    continue

                data = json.loads(line)

                if "message" in data:
                    full += data["message"].get("content", "")

        return full
"""