# فصل ۱۵: جمع‌بندی و پیوست‌ها

<div dir="rtl">

## جمع‌بندی

`MLSecOps` پاسخی به این واقعیت است که سامانه‌های هوش مصنوعی فقط نرم‌افزار کلاسیک نیستند. آن‌ها با داده، مدل، `Artifact`، پرامپت، `RAG`، حافظه، ابزار، عامل و رفتار احتمالاتی کار می‌کنند. بنابراین امنیت آن‌ها نیز باید در تمام چرخه حیات توزیع شود.

در این مقاله، امنیت از سطح داده آغاز شد، به مدل و زنجیره تأمین رسید، در پایپ‌لاین با gateهای قابل اجرا کنترل شد، در `Runtime` با guardrail و telemetry ادامه پیدا کرد و در نهایت با `Evidence Pack` و حاکمیت قابل ممیزی شد.

## اصول کلیدی

| اصل | توضیح |
|---|---|
| امنیت پیوسته است | یک تست قبل از انتشار کافی نیست. |
| داده دارایی امنیتی است | داده آلوده یا حساس می‌تواند مدل را ناامن کند. |
| مدل باید قابل ردیابی باشد | بدون provenance و امضا، مدل قابل اعتماد نیست. |
| Runtime حیاتی است | بسیاری از حملات LLM و Agent در زمان اجرا رخ می‌دهند. |
| شواهد باید خودکار باشند | audit دستی بعد از رخداد قابل اتکا نیست. |

> این راهنما بر اساس چارچوب‌ها و دانش منتشرشده تا پایان سال ۲۰۲۵ تدوین شده است. با توجه به سرعت تحول در حوزه LLM و Agentic AI، خواننده باید نسخه‌های جدید `OWASP LLM Top 10`، `MITRE ATLAS` و استانداردهای CycloneDX را به‌صورت دوره‌ای بررسی کند.

## چک‌لیست فشرده

| حوزه | سؤال |
|---|---|
| داده | آیا منشأ، نسخه، مالک و حساسیت داده مشخص است؟ |
| مدل | آیا مدل اسکن، تست و امضا شده است؟ |
| زنجیره تأمین | آیا `SBOM/AI-BOM` تولید شده است؟ |
| پایپ‌لاین | آیا gateها در صورت شکست واقعاً انتشار را متوقف می‌کنند؟ |
| RAG | آیا ACL در زمان retrieval اعمال می‌شود؟ |
| Agent | آیا هر tool call از `Intent Gate` عبور می‌کند؟ |
| Runtime | آیا prompt، response، retrieval و tool call لاگ می‌شوند؟ |
| SOC | آیا رخدادهای AI وارد SIEM می‌شوند؟ |
| حاکمیت | آیا evidence pack قابل audit وجود دارد؟ |

## چک‌لیست عملیاتی Production

این چک‌لیست تکمیل baseline حداقلی و عملیات `Day-2` است. اگر زمان کم است، ابتدا کنترل‌های `MUST` در پایپ‌لاین و `Runtime/SOC` بسته شوند. هر کنترل باید owner، تناوب و evidence مشخص داشته باشد.

### RACI حداقلی

| فعالیت | R مسئول اجرا | A پاسخگو نهایی | C مشاور | I مطلع |
|---|---|---|---|---|
| Threat Model | Product Security | CISO / Head of AI | Legal، Data Governance | Engineering Lead |
| Policy Gate / Pipeline | MLOps | Platform Engineering Manager | Security | Model Owner |
| Runtime Guardrails | Platform / AppSec | Model Owner | SOC | Privacy |
| SOC Alert / IR | SOC Analyst | SOC Manager | Security، MLOps | Legal در صورت نشت |
| Evidence Pack / Audit | MLOps | Compliance | Security | Internal Audit |

### داده و حریم خصوصی

| کنترل | Owner | تناوب | Evidence |
|---|---|---|---|
| `Data Contract` و `Schema Validation` | Data Engineer | هر dataset جدید | گزارش validation در `MLflow/DVC` |
| `PII Detection & Masking` | Data Governance | هر ingest | لاگ mask و نمونه audit |
| ارزیابی `Membership Inference` | Security + ML | سالانه یا پس از مدل پرریسک | گزارش تست privacy |
| ممیزی `Differential Privacy` | Privacy Officer | سالانه | سند تنظیمات DP |

### مدل و زنجیره تأمین

| کنترل | Owner | تناوب | Evidence |
|---|---|---|---|
| `ModelScan` در load | MLOps | هر build | گزارش ModelScan |
| `SBOM/AI-BOM` | MLOps | هر build | فایل `CycloneDX` یا معادل آن |
| signing و verify | MLOps | هر deploy | `Cosign Attestation` |
| `ART / Adversarial Test` و ASR acceptance | Security | هر مدل جدید | گزارش ART و ASR نسبت به baseline |
| secret در `Vault/KMS` | Platform | هر چرخه کلید | audit log دسترسی |

### Pipeline، CT، RAG و Agent

| کنترل | Owner | تناوب | Evidence |
|---|---|---|---|
| Threat Model نسخه‌دار | Product Security | هر سرویس AI جدید و سالانه | سند threat model |
| Policy Gate بدون استثنا | MLOps | هر build | لاگ `OPA/Conftest` |
| Gate ۷ برای LLM | Security | هر build LLM | گزارش red team و متریک نسبت به baseline |
| CT با canary و regression امنیتی | MLOps | هر retrain | لاگ canary و مقایسه baseline |
| RAG allowlist و reindex playbook | ML Engineer | هر منبع جدید | hash index و تست regression |
| Agent intent gate، HITL و kill switch | AppSec | هر agent release | تست policy و runbook |
| tool output gate | AppSec | هر agent release | تست JSON/Markdown مخرب |
| multi-agent depth و PEP per hop | Architect | هر graph جدید | diagram و تست escalation |

### Runtime، Cloud-native و SOC

| کنترل | Owner | تناوب | Evidence |
|---|---|---|---|
| `Inference Gateway` و guardrails | Platform | مداوم | متریک block/allow |
| `K8s RBAC` و `NetworkPolicy` | Platform | هر تغییر cluster | manifest در Git |
| `Service Mesh mTLS/AuthZ` | Platform | هر تغییر سرویس | policyهای mesh |
| isolation چندمشتری | Architect | هر tenant جدید | diagram و تست نفوذ |
| telemetry به SIEM و ruleهای ATLAS | SOC | مداوم | نمونه alert و playbook |
| playbook جدا برای data drift و adversarial drift | SOC | فصلی | runbook به‌روز |
| tune rule و FP review | SOC | ماهانه | گزارش false positive rate |
| SLA رخداد P1/P2 | SOC Manager | هر incident | ticket با زمان acknowledge و contain |

### حاکمیت و Evidence Pack

| کنترل | Owner | تناوب | Evidence |
|---|---|---|---|
| evidence pack کامل برای هر deploy | MLOps | هر deploy | bundle امضاشده |
| security suite در Git و regression score | Product Security | هر تغییر gate/guardrail | hash suite و score نسبت به baseline |
| tamper-evident storage | Security | audit فصلی | object lock و verify امضا |
| prompt trace و snapshot در رخداد | SOC | هر incident | ticket و artifact |
| postmortem اجباری برای severity بالا | Engineering Manager | هر incident | سند postmortem |

## واژه‌نامه کوتاه

اصطلاحات پرتکرار در این مقاله:

| اصطلاح | معنی |
|---|---|
| `MLSecOps` | اعمال امنیت در چرخه حیات سامانه‌های ML و AI |
| `RAG` | بازیابی سند مرتبط و تزریق آن به context مدل |
| `Prompt Injection` | تلاش برای تغییر رفتار مدل از طریق دستور مخرب |
| `Artifact` | خروجی قابل ذخیره مانند مدل، dataset، image یا manifest |
| `Provenance` | منشأ و مسیر ساخت یک دارایی؛ شامل داده، کد، وابستگی و فرآیند build |
| `Evidence Pack` | مجموعه شواهد قابل ممیزی درباره ساخت، تست، انتشار و runtime مدل |
| `Guardrail` | کنترل ورودی، خروجی یا رفتار مدل در runtime |
| `Intent Gate` | کنترل مجوزدهی پیش از اقدام عامل یا فراخوانی ابزار |
| `Output Gate` | بررسی و اعتبارسنجی خروجی مدل یا ابزار پیش از تحویل به downstream |
| `Tool Abuse` / `Tool Misuse` | یک مفهوم با دو نام؛ در `OWASP ASI` با شناسه `ASI02` شناخته می‌شود |
| `ASR` | `Attack Success Rate` — نرخ موفقیت حمله adversarial نسبت به baseline |
| `Security Gate` / `Quality Gate` | نقطه توقف در pipeline؛ در صورت شکست، انتشار متوقف می‌شود |
| `Fail-closed` | اگر کنترل یا gate نامشخص یا خطادار باشد، سیستم به‌جای عبور، مسدود می‌کند |
| `Baseline` | نسخه یا متریک مرجع امضاشده برای مقایسه مدل‌ها و تست‌های regression |
| `Attestation` | سند دیجیتال که ثابت می‌کند artifact با فرآیند و سیاست مشخص ساخته شده |
| `SBOM` | فهرست اجزای نرم‌افزاری (پکیج، نسخه، وابستگی) |
| `AI-BOM` / `ML-BOM` | فهرست اجزای AI شامل داده، مدل پایه، متریک‌ها و شواهد آموزش |
| `Policy-as-Code` | تبدیل سیاست امنیتی به قاعده قابل اجرا در pipeline یا runtime |
| `Tamper-evident` | ذخیره‌سازی یا امضایی که هر تغییر غیرمجاز قابل تشخیص باشد |
| `HITL` | `Human-in-the-Loop` — تأیید انسانی برای اقدامات پرریسک |
| `Canary Deployment` | انتشار تدریجی مدل جدید روی بخش کوچکی از ترافیک واقعی |
| `Data Drift` | تغییر توزیع داده یا embedding نسبت به baseline آموزش |
| `Adversarial Drift` | تغییر رفتار حمله‌ای در runtime؛ معمولاً همراه با الگوی مشکوک prompt یا tool call |
| `Schema Validation` | بررسی ساختار JSON یا typed fields و allowlist کلیدها |
| `Content-policy Enforcement` | اعمال allow/block/redact روی prompt یا خروجی |
| `Content Safety Check` | تشخیص دستورالعمل مخرب در متن، مثل ignore previous |
| `Action-policy Verification` | تطابق tool planned با policy engine مانند `OPA/Cedar` |
| `Constrained Decoding` | محدودیت خروجی در سطح tokenizer، مانند JSON mode یا grammar |
| `Semantic Consistency Check` | تطابق پاسخ با retrieved context در RAG |

## پیوست الف: Reference Card تهدید، کنترل و ابزار

این کارت، نسخه تجمیع‌شده و کامل جدول فصل ۱۲ است و برای استفاده به‌عنوان مرجع سریع مستقل در اینجا تکرار شده است. شرح تفصیلی هر کنترل و نگاشت لایه‌ای ابزارها در فصل ۱۲ آمده است.

| تهدید | Framework | Surface | Lifecycle | Phase | ریسک | کنترل اصلی | ابزار/مرحله |
|---|---|---|---|---|---|---|---|
| `Prompt Injection` | `LLM01` | Prompt | Deploy/Monitor | Execution | Critical | gateway و sanitization | Runtime |
| `Sensitive Data Leak` | `LLM02` | Prompt/Model | Monitor | Execution | High | output moderation | Gateway |
| `Supply Chain Attack` | `LLM03` | Model/Infra | Train/Deploy | Staging | Critical | sign و scan | Load |
| `Data Poisoning` | `ML02` | Data | Train | Staging | High | dataset validation | Data gate |
| `Model Poisoning / Backdoor` | `ML10` | Model | Train | Staging | Critical | backdoor test | `ART` |
| `Adversarial Evasion` | `ML01` | Model | Deploy | Execution | High | robustness و ASR gate | Gate ۷ |
| `Model Artifact RCE` | — | Model/Infra | Deploy | Staging | Critical | `ModelScan` | Load |
| `Retrieval Poisoning` | `LLM08` | Data/Prompt | Deploy | Execution | High | allowlist ingest | RAG |
| `Embedding Poisoning` | `LLM08` | Data | Train/Deploy | Staging | High | source hygiene | RAG |
| `Cross-tenant Leakage` | Arch/Infra (مرتبط با `LLM08`) | Infra | Deploy | Execution | Critical | physical isolation | Multi-tenant |
| `System Prompt Leakage` | `LLM07` | Prompt | Deploy/Monitor | Execution | Critical | output gate | Gateway |
| `Unbounded Consumption` | `LLM10` | API | Monitor | Execution | Medium | rate limit | Gateway |
| `Gradient Leakage` | — | Data | Train | Staging | High | secure aggregation | Federated |
| `Tool Misuse` | `ASI02` | Tool | Monitor | Execution | High | `Intent Gate` | Agent |
| `Model Collapse` | — | Model | Train | Staging | Medium | diversity evaluation | Gate ۷ |
| `Overrefusal` | LLM | Prompt | Monitor | Execution | Medium | threshold tuning | Gateway |
| `Agent Memory Poisoning` | ASI | Tool/Prompt | Monitor | Execution | High | sanitize و TTL | Memory |
| `Tool Output Injection` | `ASI/LLM01` | Tool | Monitor | Execution | High | `Output Gate` | Agent |
| `Multi-Agent Escalation` | ASI | Tool | Monitor | Execution | High | PEP per hop | Multi-agent |

## پیوست ب: نگاشت MITRE ATLAS

نگاشت تفصیلی‌تر `MITRE ATLAS` برای تحلیل SOC در فصل ۱۰ و نگاشت کنترل‌محور در فصل ۱۲ آمده است؛ این جدول خلاصه مرجع است.

| تهدید | تکنیک | شناسه |
|---|---|---|
| `Prompt Injection` | `LLM Prompt Injection` | `AML.T0051` |
| `Data Poisoning` | `Poison Training Data` | `AML.T0020` |
| `Model Extraction` | `Exfiltration via Inference API` | `AML.T0044` |
| `Adversarial Evasion` | `Evade ML Model` | `AML.T0015` |
| `Supply Chain` | `Publish Poisoned Models` | `AML.T0058` |
| `RAG Poisoning` | `Poison Web Index` | `AML.T0066` |

## منابع و مراجع

> توجه: این بخش به‌صورت فهرست منابع کاری ارائه شده است. برای انتشار رسمی، توصیه می‌شود هر مرجع با نویسنده، سال، ناشر و در صورت وجود `DOI`/`URL` به قالب کتاب‌نامه استاندارد (مثلاً `IEEE` یا `APA`) تبدیل شود.

### چارچوب‌ها و استانداردها

- OpenSSF (2025). *Visualizing Secure MLOps (MLSecOps) Whitepaper*. OpenSSF AI/ML Security Working Group.
- NIST (2023). *AI Risk Management Framework (AI RMF 1.0)*.
- NIST (2024). *Generative AI Profile (NIST-AI-600-1)*.
- ISO/IEC 42001:2023. *Artificial Intelligence — Management System*.
- ISO/IEC 23894:2023. *Artificial Intelligence — Guidance on Risk Management*.
- European Union (2024). *EU AI Act*.
- Cloud Security Alliance (2025). *MAESTRO — Multi-Agent Environment Security Framework*.

### تهدیدشناسی و راهنماهای امنیتی

- OWASP (2025). *Top 10 for LLM Applications (2025)*.
- OWASP. *Top 10 for Agentic Applications* / *Agentic Security Initiative*.
- OWASP. *Machine Learning Security Top 10* (وضعیت `draft`).
- OWASP. *LLM Verification Standard (LLMSVS)*.
- MITRE. *ATLAS — Adversarial Threat Landscape for AI Systems*. atlas.mitre.org
- *AI Vulnerability Database (AVID)*. avidml.org
- *AI Incident Database*. incidentdatabase.ai

### ابزارها و پروژه‌های متن‌باز

- `Adversarial Robustness Toolbox (ART)` — تست adversarial مدل کلاسیک
- `Microsoft PyRIT` — red team چندمرحله‌ای LLM
- `ModelScan` (Protect AI) — اسکن artifact مدل
- `Garak` (NVIDIA) — اسکنر آسیب‌پذیری LLM
- `Vigil`، `Promptfoo`، `Giskard` — تست و red team LLM/RAG
- `NeMo Guardrails`، `Lakera Guard`، `Patronus AI` — guardrail و gateway
- `lintML` (NVIDIA)، `NB Defense` (Protect AI) — linter و اسکن notebook/کد ML
- `Gitleaks`، `Trivy`، `Syft`، `Grype` — secret/SCA/SBOM
- `Checkov`، `tfsec`، `OPA`/`Conftest`، `Kyverno` — IaC و policy-as-code
- `Sigstore / Cosign / Rekor`، `sigstore/model-transparency` (`model-signing`)، `SLSA` — امضا و provenance مدل
- `CycloneDX 1.7 (ECMA-424)`، `cdxgen` (`aibom`)، `OWASP AIBOM Generator` — SBOM و ML-BOM/AI-BOM
- `AI-exploits` (Protect AI)، `AI-Infra-Guard` (Tencent)، `Agentic Security`، `PurpleLlama` (Meta)، `Mindgard CLI` — تست زیرساخت MLOps و عامل
- `PrivacyRaven` (Trail of Bits)، `ML Privacy Meter`، `TensorFlow Privacy`، `OpenDP` — ممیزی حریم خصوصی و differential privacy
- `huntr.com` — پلتفرم bug bounty اختصاصی AI/ML
- `awesome-MLSecOps`، `Awesome-LM-SSP`، `awesome-llm-security`، `awesome-llm-supply-chain-security` — فهرست‌های مرجع MLSecOps

### مقالات و گزارش‌های مرجع

- Shumailov, I. et al. (2023). *The Curse of Recursion: Training on Generated Data Makes Models Forget* (Model Collapse).
- Greshake, K. et al. (2023). *Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection*.
- Zou, W. et al. (2024). *PoisonedRAG: Knowledge Poisoning Attacks to RAG*.
- Goodfellow, I. et al. (2015). *Explaining and Harnessing Adversarial Examples* (FGSM).
- Carlini, N. & Wagner, D. (2017). *Towards Evaluating the Robustness of Neural Networks*.
- Trail of Bits (2024). *LeftoverLocals (CVE-2023-4969)*.
- HiddenLayer. *SILENT SABOTAGE* — سوءاستفاده از bot تبدیل Pickle به SafeTensors.
- HiddenLayer. *NOT SO CLEAR: How MLOps Solutions Can Muddy the Waters of Your Supply Chain* (ClearML).
- Sigstore Blog (2025). *Practical Model Signing with Sigstore — model-transparency v1.0*.
- Cohen, S. et al. (2024). *Here Comes the AI Worm (Morris II): Zero-click Worms Targeting GenAI-Powered Applications*.
- Spracklen, J. et al. (2024). *We Have a Package for You: Package Hallucinations by Code-Generating LLMs (Slopsquatting)*.
- ZJU-SEC. *TensorAbuse — Transforming AI Models into Malware by Abusing TensorFlow APIs*.
- Li, Y. et al. (2024). *BadEdit: Backdooring Large Language Models by Model Editing*.
- Xiang, Z. et al. (2024). *BadChain: Backdoor Chain-of-Thought Prompting for LLMs*.
- Morris, J. X. et al. (2023). *Text Embeddings Reveal (Almost) As Much As Text* (Embedding Inversion).
- Rando, J. & Tramèr, F. (2024). *Universal Jailbreak Backdoors from Poisoned Human Feedback*.

> یادداشت درباره AISecOps: اصطلاح `AISecOps` (مثلاً در NSFOCUS (2023), *AISecOps Whitepaper*) به «به‌کارگیری AI در عملیات امنیتی/SOC» اشاره دارد و حوزه‌ای جدا از موضوع این راهنماست؛ این منبع صرفاً برای تفکیک مفهومی در فصل ۱ ذکر شده است.

## پیوست: Claims & Evidence

این پیوست ادعاهای کلیدی مقاله را به مرجع قابل بررسی نگاشت می‌دهد:

| موضوع / ادعا | مرجع پیشنهادی |
|---|---|
| `Model Collapse` | Shumailov et al., *The Curse of Recursion* (2023) |
| `Indirect / Tool-mediated Injection` | Greshake et al., *Not what you've signed up for* (2023) |
| `RAG / Retrieval Poisoning` | Zou et al., *PoisonedRAG* (2024)؛ `OWASP LLM08` |
| `Adversarial Evasion` | Goodfellow et al. (2015)؛ Carlini & Wagner (2017)؛ `MITRE ATLAS AML.T0015` |
| `Overrefusal` | `OWASP LLM Top 10 (2025)` |
| `Agentic Threats` / `Tool Misuse` | `OWASP Top 10 for Agentic Applications`؛ CSA `MAESTRO` |
| `System Prompt Leakage` / `LLM07` | `OWASP Top 10 for LLM Applications (2025)` |
| `Vector & Embedding Weaknesses` / `LLM08` | `OWASP Top 10 for LLM Applications (2025)` |
| `LeftoverLocals` (نشت حافظه GPU) | Trail of Bits، `CVE-2023-4969` (۲۰۲۴) |
| مدل‌های ناامن HuggingFace (Pickle RCE) | ReversingLabs / Protect AI `ModelScan` (۲۰۲۵) |
| `AI Worm / Zero-click` | Cohen et al., *Here Comes the AI Worm (Morris II)* (2024) |
| `Models-as-Malware` | ZJU-SEC, *TensorAbuse* |
| `Package Hallucination` | Spracklen et al., *We Have a Package for You* (2024) |
| `Embedding Inversion` | Morris et al., *Text Embeddings Reveal (Almost) As Much As Text* (2023) |
| `Advanced Backdoors (RLHF/CoT/Edit)` | Rando & Tramèr (2024)، Xiang et al. (2024)، Li et al. (2024) |
| `SILENT SABOTAGE / ClearML` | HiddenLayer Research |
| ۲۲ کنترل امنیتی MLOps | OpenSSF *MLSecOps Whitepaper* (2025) |

## راهنمای دیاگرام‌های Mermaid

دیاگرام‌ها در GitHub، GitLab و Cursor Preview نمایش داده می‌شوند. برای خروجی PDF یا Word می‌توان از `Mermaid Live Editor` خروجی PNG یا SVG گرفت. بهتر است برچسب nodeها انگلیسی باشد و توضیح فارسی در caption یا متن زیر شکل بیاید.

فهرست شکل‌ها شامل نمای `DevSecOps/MLSecOps`، پایپ‌لاین، چرخه `CT`، `Tool Output Injection`، `Memory Contamination`، `Multi-Agent` و لایه‌های ابزار است.

## نسخه GitHub

این نسخه به‌صورت Markdown نوشته شده و برای نمایش در GitHub آماده است. برای کاهش مشکل متن فارسی و انگلیسی، هر فصل داخل `div` راست‌به‌چپ قرار گرفته و اصطلاحات انگلیسی با `inline code` نوشته شده‌اند.

## نتیجه نهایی

امنیت هوش مصنوعی با یک ابزار، یک prompt امن یا یک تست ساده حل نمی‌شود. امنیت زمانی قابل دفاع است که داده، مدل، زنجیره تأمین، پایپ‌لاین، runtime و عملیات امنیتی به‌صورت یک جریان واحد و قابل ممیزی دیده شوند.

با تفکیک `Risk Management` از `Threat Modeling`، پایپ‌لاین ۱۰ مرحله‌ای، assurance قابل اندازه‌گیری، کنترل‌های runtime و `Evidence Pack`، سازمان‌ها می‌توانند مدل‌ها را با امنیت و قابلیت دفاع ممیزی در production مستقر کنند.

`MLSecOps` شرط اطمینان‌پذیری سیستم‌های AI در محیط واقعی است. سازمانی که `MLSecOps` را جدی بگیرد، نه‌تنها ریسک را کاهش می‌دهد، بلکه سرعت استقرار امن را نیز بالا می‌برد؛ و این تفاوت بین «استفاده از AI» و «اعتماد به AI» است.

</div>
