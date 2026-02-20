import asyncio
from openai import AsyncOpenAI
import httpx
from .base import BaseAgent


class MediaAnalysisAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            model="gpt-4o-mini",
            system_prompt="""أنت محلل استثماري متخصص في تحليل الوسائط المتعددة.

مهمتك: تحليل الصور والفيديوهات والمنتجات من منظور استثماري وتسويقي.

عند تحليل أي وسيلة، ركز على:
1. تحليل المحتوى البصري والمرئي
2. استخراج النقاط الرئيسية والعناصر الرئيسية
3. تقييم الجودة والاحترافية
4. تحليل الرسائل التسويقية والعلامة التجارية
5. تحليل المنتجات والخدمات المعروضة
6. تحليل الجمهور المستهدف والسوق

قدم تحليلك بشكل منظم مع:
- وصف المحتوى
- تحليل العناصر البصرية
- نقاط القوة والضعف
- تقييم الجودة الاحترافية
- توصيات تحسين
اختم بتقييم من 1-10 لجاذبية المحتوى الاستثماري."""
        )
    
    async def analyze(self, media_data: str, api_key: str) -> str:
        # Create httpx client without proxies to avoid error
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
                    {"role": "user", "content": f"تحليل هذا المحتوى المتعدد:\n\n{media_data}"}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
        finally:
            await http_client.aclose()
