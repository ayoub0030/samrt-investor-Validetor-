import asyncio
from openai import AsyncOpenAI
import httpx
from .base import BaseAgent

class MarketingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            model="gpt-4o-mini",
            system_prompt="""أنت خبير تسويق ومحتوى إبداعي متخصص في إنشاء مواد ترويجية للاستثمارات و المشاريع الناشئة. مهمتك هي تحليل الفكرة الاستثمارية والتقرير النهائي، ثم إنشاء محتوى تسويقي جذاب ومقنع.

مطلوب منك تقديم 3 أنواع من المحتوى التسويقي:

1. **وصف صورة الفلاير (Flyer Image Description)**:
   - وصف مفصل للتصميم البصري للفلاير
   - الألوان المناسبة والخطوط والتخطيط
   - العناصر البصرية التي يجب تضمينها
   - الرسالة الرئيسية التي يجب أن ينقلها الفلاير

2. **وصف الإعلان الفيديو (Video Ad Description)**:
   - سيناريو الفيديو بالتفصيل
   - المشاهد الافتتاحية والوسطية والختامية
   - النصوص والحوار والمؤثرات الصوتية
   - مدة الفيديو المقترحة والجمهور المستهدف

3. **وصف المنتج للعرض التقديمي (Product Presentation Description)**:
   - محتوى العرض التقديمي للمستثمرين
   - النقاط الرئيسية التي يجب التركيز عليها
   - هيكل العرض (مقدمة، جوهر، خاتمة)
   - العناصر المقنعة والمزايا التنافسية

ركز على:
- الجاذبية البصرية والنصية
- الوضوح والإقناع
- التميز عن المنافسين
- إبراز القيمة الاستثمارية
- سهولة الفهم والتأثير

قدم ردك منسق بشكل احترافي مع عناوين واضحة لكل قسم."""
        )

    async def analyze(self, idea: str, final_report: str, api_key: str) -> str:
        # Create httpx client without proxies to avoid the error
        http_client = httpx.AsyncClient()
        
        try:
            client = AsyncOpenAI(
                api_key=api_key,
                http_client=http_client
            )
            
            user_message = f"""الفكرة الاستثمارية الأصلية:
{idea}

---

التقرير النهائي من لجنة الاستثمار:
{final_report}

---

بناءً على الفكرة الاستثمارية والتقرير النهائي، قم بإنشاء محتوى تسويقي شامل يتضمن وصف الفلاير، وصف الإعلان الفيديو، ووصف العرض التقديمي."""

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
