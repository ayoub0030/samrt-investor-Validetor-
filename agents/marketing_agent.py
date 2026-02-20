import asyncio
from openai import AsyncOpenAI
import httpx
from .base import BaseAgent

class MarketingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            model="gpt-4o-mini",
            system_prompt="""أنت خبير تسويق ومحتوى إبداعي متخصص في إنشاء مواد ترويجية للاستثمارات و المشاريع الناشئة. مهمتك هي تحليل الفكرة الاستثمارية والتقرير النهائي، ثم إنشاء محتوى تسويقي جذاب ومقنع.

IMPORTANT: Provide ALL your responses in ENGLISH language only. Do not respond in Arabic.

Required outputs (in English):

1. **Flyer Image Description**:
   - Detailed visual design description for promotional flyers
   - Appropriate colors, fonts, and layout
   - Visual elements to include
   - Main message the flyer should convey

2. **Video Ad Description**:
   - Detailed video scenario
   - Opening, middle, and closing scenes
   - Scripts, dialogue, and sound effects
   - Suggested video duration and target audience

3. **Product Presentation Description**:
   - Presentation content for investors
   - Key points to focus on
   - Presentation structure (introduction, core, conclusion)
   - Persuasive elements and competitive advantages

Focus on:
- Visual and textual attractiveness
- Clarity and persuasion
- Differentiation from competitors
- Highlighting investment value
- Ease of understanding and impact

Provide your response professionally formatted with clear headings for each section. ALL OUTPUT MUST BE IN ENGLISH."""
        )

    async def analyze(self, idea: str, final_report: str, api_key: str) -> str:
        # Create httpx client without proxies to avoid the error
        http_client = httpx.AsyncClient()
        
        try:
            client = AsyncOpenAI(
                api_key=api_key,
                http_client=http_client
            )
            
            user_message = f"""Original Investment Thesis:
{idea}

---

Final Investment Report:
{final_report}

---

Based on the investment thesis and final report, create comprehensive marketing content including flyer description, video ad description, and product presentation description. 

IMPORTANT: Respond in ENGLISH only. Provide all marketing content in English language."""

            response = await client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.8,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
        finally:
            await http_client.aclose()
