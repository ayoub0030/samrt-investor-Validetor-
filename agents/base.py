import asyncio
from openai import AsyncOpenAI
import httpx


class BaseAgent:
    def __init__(self, model: str, system_prompt: str):
        self.model = model
        self.system_prompt = system_prompt
    
    async def analyze(self, idea: str, api_key: str) -> str:
        # Create httpx client without proxies to avoid the error
        http_client = httpx.AsyncClient()
        
        try:
            client = AsyncOpenAI(
                api_key=api_key,
                http_client=http_client
            )
            
            response = await client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": idea}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
        finally:
            await http_client.aclose()
