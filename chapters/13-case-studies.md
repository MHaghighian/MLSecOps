# فصل ۱۳: مطالعات موردی و درس‌آموخته‌ها

<div dir="rtl">

## هدف فصل

مطالعات موردی نشان می‌دهند ریسک‌های `MLSecOps` فقط نظری نیستند. بسیاری از رخدادها از ترکیب داده، مدل، زنجیره تأمین، دسترسی و runtime ایجاد شده‌اند.

> توجه به منابع: تاریخ‌ها و شناسه‌های `CVE` ذکرشده در این فصل بر اساس گزارش‌های عمومی منتشرشده‌اند (از جمله Trail of Bits، HiddenLayer، ReversingLabs و OWASP). برای استناد رسمی، نگاشت کامل ادعا به منبع در پیوست «Claims & Evidence» فصل ۱۵ آمده است؛ توصیه می‌شود پیش از انتشار، لینک مستقیم گزارش هر مورد افزوده شود.

## LeftoverLocals (CVE-2023-4969)

`Trail of Bits` در ژانویه ۲۰۲۴ آسیب‌پذیری `LeftoverLocals` را گزارش کرد: باقی‌مانده پاسخ LLM در حافظه GPU بین processها قابل خواندن بود و منجر به cross-application data leakage می‌شد (GPUهای Apple، Qualcomm، AMD و Imagination).

درس‌آموخته:

- به‌روزرسانی driver GPU
- sanitization حافظه پس از inference
- isolation process در محیط multi-tenant GPU

## MLflow و آسیب‌پذیری‌های پلتفرم MLOps

آسیب‌پذیری‌های `MLflow` (از جمله path traversal و دسترسی به credential) نشان می‌دهد registry و experiment tracking بدون hardening می‌تواند کل حساب cloud را در معرض خطا قرار دهد.

درس‌آموخته:

- patch منظم پلتفرم MLOps
- authentication و network segmentation
- عدم expose کردن MLflow به اینترنت بدون auth

## ClearML و Confused Learning

تحقیقات `HiddenLayer` روی پلتفرم `ClearML` نشان داد که مهاجم با compromise کردن agent یا دستکاری metadata می‌تواند کل pipeline آموزش را مسموم کند (حمله‌ای معروف به `Confused Learning`).

درس‌آموخته:

- hardening کردن agentهای MLOps
- استفاده از allowlist برای artifactها
- جداسازی محیط‌های آموزش از هم

## SILENT SABOTAGE (HuggingFace Conversion Bot)

در یک حمله زنجیره تأمین واقعی، مهاجمان از یک bot عمومی در HuggingFace که وظیفه تبدیل مدل‌های `pickle` به `safetensors` را داشت سوءاستفاده کردند تا کد مخرب خود را در artifactهای ظاهراً امن جاسازی کنند.

درس‌آموخته:

- صرفِ تغییر فرمت به `safetensors` امنیت را تضمین نمی‌کند.
- ابزارهای تبدیل و botها خودشان سطح حمله هستند.
- اسکن artifact باید حتی روی فرمت‌های امن هم انجام شود.

## BentoML، LangChain و RCE

آسیب‌پذیری‌های deserialization در `BentoML` و `LangChain` منجر به `RCE` در سرور inference شده است. الگوی مشترک: load ناامن artifact یا pickle بدون sandbox.

درس‌آموخته:

- disable unsafe deserialization
- sandbox برای model serving
- به‌روزرسانی فوری پس از CVE

## HuggingFace: بیش از ۳۳۰۰ مدل ناامن

`ModelScan` و تحقیقات ReversingLabs (فوریه ۲۰۲۵) بیش از ۳۳۰۰ مدل ناامن در HuggingFace شناسایی کردند — عمدتاً pickle-based RCE.

درس‌آموخته:

- اسکن اجباری قبل از load
- ترجیح `safetensors` بر pickle
- allowlist منبع مدل

## LangSmith و افشای API Key (۲۰۲۵)

در برخی سناریوهای agent، API key از طریق prompt injection یا tool chain استخراج شده است.

درس‌آموخته:

- proxy gateway برای کلید API (agent هرگز کلید واقعی نبیند)
- چرخش فوری کلید پس از incident
- isolation credential از context مدل

## Pickle-based RCE در مخازن مدل

برخی مدل‌های منتشرشده با فرمت‌های ناامن مانند `pickle` می‌توانند هنگام load شدن کد اجرا کنند. اگر تیم بدون اسکن و ایزوله‌سازی، مدل را از مخزن عمومی بارگذاری کند، امکان اجرای کد مخرب در محیط آموزش یا inference وجود دارد. (جزئیات فنی فرمت‌های ناامن و کنترل‌ها در فصل ۵ آمده است.)

درس‌آموخته:

- بارگذاری مدل باید در sandbox انجام شود.
- فرمت‌های ناامن باید محدود یا ممنوع شوند.
- `ModelScan` و کنترل artifact باید قبل از load اجرا شوند.

## PoisonGPT و زنجیره تأمین AI

در سناریوهایی مانند `PoisonGPT`، مهاجم مدل یا artifact آلوده را با نام مشابه مدل معتبر منتشر می‌کند. توسعه‌دهنده ممکن است مدل اشتباه را دانلود و وارد pipeline کند.

درس‌آموخته:

- استفاده از allowlist برای منابع مدل
- بررسی امضا و provenance
- ثبت hash مدل پایه
- کنترل نام‌های مشابه و typosquatting

## Prompt Injection در سامانه‌های عمومی

رخدادهای مربوط به `Prompt Injection` نشان داده‌اند که مدل‌های زبانی ممکن است دستورالعمل‌های سیستمی را نادیده بگیرند، محدودیت‌ها را دور بزنند یا اطلاعاتی را افشا کنند که نباید در خروجی بیاید.

درس‌آموخته:

- امنیت LLM فقط با prompt حل نمی‌شود.
- `Gateway` و `Output Gate` ضروری‌اند.
- تست red team باید به‌صورت مداوم انجام شود.

## نشت داده از استفاده سازمانی از LLM عمومی

در برخی سازمان‌ها، کارکنان کد منبع، لاگ، داده مشتری یا اسناد داخلی را در ابزارهای LLM عمومی وارد کرده‌اند. این کار داده را از مرز کنترل سازمان خارج می‌کند.

درس‌آموخته:

- سیاست روشن برای استفاده از LLM عمومی لازم است.
- داده production نباید وارد سرویس عمومی شود.
- gateway سازمانی و `DLP` خروجی باید فعال باشد.

## Indirect Prompt Injection در Copilot و RAG

در حمله غیرمستقیم، دستور مخرب داخل ایمیل، سند، صفحه وب یا ticket قرار می‌گیرد. سامانه `RAG` یا copilot آن سند را بازیابی می‌کند و مدل دستور مخفی را به‌عنوان context می‌پذیرد.

درس‌آموخته:

- منبع خارجی باید untrusted فرض شود.
- خروجی retrieval باید sanitize شود.
- context نباید بدون کنترل وارد مدل شود.

## ابزارهای AI داخل DevOps

ادغام AI در گردش کار توسعه، مانند پیشنهاد کد یا chat روی repository، سطح حمله را به کد، secret و مجوزهای repository گسترش می‌دهد. نمونه‌هایی مانند `GitLab Duo` نشان می‌دهند که threat model برای AI داخل IDE/CI باید جداگانه تعریف شود.

درس‌آموخته:

- دسترسی مدل به repository باید بر اساس permission واقعی کاربر محدود شود.
- context ارسالی به مدل نباید شامل secret یا داده حساس باشد.
- secret scanning همچنان کنترل اجباری `DevSecOps` و `MLSecOps` است.

## RAG در Knowledge Base سازمانی

وقتی کل دانش سازمانی بدون پالایش وارد `Vector DB` شود، chat داخلی می‌تواند به مسیر افشای اسناد تبدیل شود. اگر ACL در زمان retrieval اعمال نشود، کاربر ممکن است پاسخ‌هایی بر اساس اسنادی بگیرد که اجازه دیدن آن‌ها را ندارد.

درس‌آموخته:

- ACL باید در query time اعمال شود.
- index مشترک برای tenantها خطرناک است.
- تست retrieval leakage باید بخشی از pipeline باشد.

## جمع‌بندی درس‌ها

| الگوی شکست | کنترل کلیدی |
|---|---|
| مدل آلوده از مخزن عمومی | امضا، allowlist، scan |
| prompt injection | gateway، guardrail، red team |
| نشت داده به LLM عمومی | policy، DLP، آموزش کارکنان |
| RAG بدون ACL | authorization در retrieval |
| Agent با دسترسی زیاد | scoped tool access و intent gate |

## اصل عملی

در بیشتر رخدادها، شکست فقط از خود مدل نیست. شکست از اعتماد بیش از حد به داده، ابزار، زنجیره تأمین، context یا کاربر ایجاد می‌شود.

</div>
