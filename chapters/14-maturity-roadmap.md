# فصل ۱۴: نقشه راه بلوغ MLSecOps

<div dir="rtl">

## چرا بلوغ مرحله‌ای مهم است؟

پیاده‌سازی کامل `MLSecOps` در یک مرحله معمولاً عملی نیست. تیم‌ها باید بر اساس ریسک، ظرفیت و معماری خود حرکت کنند. نقشه راه بلوغ کمک می‌کند سازمان از کنترل‌های پایه شروع کند و به‌تدریج به معماری قابل ممیزی و عملیاتی برسد.

## سطح‌های بلوغ

| سطح | وضعیت | ویژگی‌ها |
|---|---|---|
| سطح ۰ | بدون کنترل منسجم | مدل‌ها دستی ساخته و منتشر می‌شوند، شواهد کم است. |
| سطح ۱ | پایه | threat model، data validation، artifact scan و آگاهی تیم برقرار است. |
| سطح ۲ | عملیاتی | gate خودکار، signing، تست امنیتی، runtime telemetry و SOC runbook وجود دارد. |
| سطح ۳ | بالغ | evidence خودکار، SOC پیشرفته، tamper-evident storage، multi-tenant hardening و regression score برقرار است. |

## سطح ۱: Foundational

هدف سطح ۱ جلوگیری از خطاهای بنیادین پیش از ورود به `Production` است. معیار ورود به این سطح، پیاده‌سازی baseline حداقلی است.

| قابلیت | معیار آمادگی |
|---|---|
| `Threat Model` و planning | سند `ATLAS/OWASP` پیش از اولین pipeline |
| `Data Validation` | schema و PII check پیش از train |
| اسکن artifact | `ModelScan` در مرحله load |
| awareness | تیم از `Prompt Injection` و supply chain آگاه است |

## سطح ۲: Operational

هدف سطح ۲ کنترل خودکار در pipeline و دفاع runtime است.

| قابلیت | معیار آمادگی |
|---|---|
| `Policy Gate` | هیچ استثنای دستی برای deploy وجود ندارد |
| signing | همه مدل‌های production امضا و verify می‌شوند |
| `Adversarial / LLM Test` | `ART` یا prompt suite با acceptance criteria در gate ۷ اجرا می‌شود |
| runtime | `Inference Gateway`، telemetry و tracking برای FN/bypass |
| SOC | runbook، SIEM rule و SLA رخداد |

شرط ارتقا به سطح ۳، حداقل ۶ ماه پایش production بدون رخداد critical، بدون نیاز به مداخله دستی gateها، و وجود evidence pack امضاشده و قابل verify برای آخرین deploy است.

## سطح ۳: Mature

هدف سطح ۳ ممیزی خودکار، انطباق سازمانی و بهبود مستمر است.

| قابلیت | معیار آمادگی |
|---|---|
| evidence pack خودکار | در هر build بدون مداخله دستی تولید شود |
| SOC پیشرفته | alertها به `MITRE ATLAS` نگاشت و correlation شوند |
| tamper-evident evidence | استفاده از `Rekor`، `WORM` یا object lock |
| multi-tenant / K8s | RBAC، service mesh و isolation چندمشتری |
| انطباق | trace از `NIST AI RMF`، `ISO 42001` و `EU AI Act` به کنترل‌ها |
| بهبود مستمر | red team دوره‌ای و regression score خودکار |

## حداقل کنترل‌های شروع

برای شروع عملی، این کنترل‌ها بیشترین ارزش را دارند:

- ثبت نسخه داده و مدل
- اسکن secret و وابستگی‌ها
- اسکن artifact مدل
- تعریف gateهای توقف واقعی
- امضای مدل پیش از انتشار
- ثبت evidence pack پایه
- مانیتورینگ prompt، response و tool call

## مسیر پیشنهادی ۹۰ روزه

| بازه | تمرکز | خروجی |
|---|---|---|
| روز ۱ تا ۳۰ | شناخت و پایه‌سازی | threat model، فهرست دارایی‌ها، کنترل داده |
| روز ۳۱ تا ۶۰ | پایپ‌لاین | security gate، scan، test و evidence pack |
| روز ۶۱ تا ۹۰ | runtime | gateway، telemetry، alert و rollback |

## معیارهای بلوغ

| معیار | نشانه بلوغ |
|---|---|
| بازتولیدپذیری | مدل با همان داده و کد قابل بازسازی است. |
| ممیزی | تمام تصمیم‌های انتشار شواهد دارند. |
| توقف خودکار | gateها واقعاً pipeline را fail می‌کنند. |
| امنیت runtime | prompt، response، retrieval و tool call پایش می‌شود. |
| پاسخ به رخداد | rollback و playbook مشخص وجود دارد. |

## خطاهای رایج در مسیر بلوغ

- شروع با ابزارهای زیاد بدون threat model
- نادیده گرفتن داده و تمرکز صرف روی مدل
- ایجاد gateهایی که فقط هشدار می‌دهند و توقف ندارند
- فراموش کردن runtime و SOC
- تولید دستی evidence بعد از رخداد

## اصل عملی

بلوغ `MLSecOps` با خرید ابزار شروع نمی‌شود. با شناخت دارایی، تعریف تهدید، اجرای کنترل‌های پایه و تولید شواهد قابل اتکا شروع می‌شود.

</div>
