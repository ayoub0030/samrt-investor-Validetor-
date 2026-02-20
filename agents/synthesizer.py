import asyncio
from openai import AsyncOpenAI
import httpx

SYSTEM_PROMPT = """أنت الشريك العام وصانع القرار الاستثماري النهائي.

دورك: استلام تحليلات ثلاثة محللين متخصصين (منطق السوق، الاستدامة المالية، المتانة التنافسية) ودمجها في حكم نهائي شامل.

عند اتخاذ القرار:
1. وازن بين الحجج المتناقضة من المحللين الثلاثة
2. حدد أوجه التوافق والاختلاف بين التحليلات
3. قيّم المخاطر الإجمالية مقابل الفرص
4. أصدر حكماً استثمارياً واضحاً

هيكل ردك يجب أن يكون:
## ملخص التحليلات
(ملخص موجز لما قاله كل محلل)

## نقاط التوافق
(أين اتفق المحللون)

## نقاط الاختلاف
(أين اختلفت الآراء وكيف توازن بينها)

## الحكم الاستثماري النهائي
اختر واحداً: [استثمر بقوة | استثمر بحذر | راقب وانتظر | لا تستثمر]

## التقييم الإجمالي
(من 1-10 مع تبرير)

## الاستشارة الاستراتيجية
(نصائح عملية للمستثمر)"""


class SynthesizerAgent:
    def __init__(self):
        self.model = "gpt-4o"
        self.system_prompt = SYSTEM_PROMPT
    
    async def synthesize(
        self,
        idea: str,
        market_analysis: str,
        financial_analysis: str,
        competitive_analysis: str,
        api_key: str
    ) -> str:
        # Create httpx client without proxies to avoid the error
        http_client = httpx.AsyncClient()
        
        try:
            client = AsyncOpenAI(
                api_key=api_key,
                http_client=http_client
            )
            
            user_message = f"""الفكرة الاستثمارية:
{idea}

---

تحليل منطق السوق:
{market_analysis}

---

تحليل الاستدامة المالية:
{financial_analysis}

---

تحليل المتانة التنافسية:
{competitive_analysis}

---

بناءً على التحليلات الثلاثة أعلاه، قدم حكمك الاستثماري النهائي والاستشارة الاستراتيجية."""

            response = await client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.5,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
        finally:
            await http_client.aclose()
