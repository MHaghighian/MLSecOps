# خلاصهٔ کامل راهنمای MLSecOps Practical Reference Guide (v1.0.0)

> **نسخه:** v1.0.0 · **خواندن:** [README](README.md) · [Getting Started](GETTING-STARTED.md) · فصول: `chapters-en/`

---

## ۱. موضوع و جایگاه راهنما

**MLSecOps** گسترش اصول **DevSecOps** به سیستم‌های AI/ML در **کل چرخهٔ عمر**: داده → آموزش/پیکربندی → ارزیابی → اعتبارسنجی امنیتی → انتشار → اجرا → مانیتورینگ → SOC/IR → حاکمیت.

### چهار ادعای اختصاصی (نسبت به OWASP / OpenSSF / NIST)

| # | ادعا | محل در راهنما |
|---|------|----------------|
| 1 | مدل **۱۰ Control Point** یکپارچه برای lifecycle | فصل ۶ |
| 2 | تفکیک **تولید Evidence** از **Release Decision** (۴، ۷، ۸) و **Integrity** (۹) | فصل ۶ |
| 3 | **Evidence Pack** به‌عنوان خروجی قابل ممیزی هر انتشار | فصل ۱۱ |
| 4 | رشتهٔ واحد threat → runtime → SOC → governance | فصل‌های ۲، ۶، ۷، ۸، ۱۰، ۱۱ |

### دامنه و محدودیت

- **پوشش:** ML کلاسیک، LLM، RAG، managed AI (Azure/Bedrock/Vertex)، Agent، MCP، Shadow AI، multi-tenant، الگوهای K8s  
- **خارج از scope v1.0:** ترجمهٔ محلی؛ تفسیر حقوقی کامل؛ TEE/confidential GPU؛ کاتالوگ محصولات؛ **بدون YAML/CI/CD آماده در repo**

### مخاطبان

| نقش | تمرکز |
|-----|--------|
| Executive / risk | فصل ۱، ۲، ۱۴ |
| Security engineer | فصل ۲، ۳، ۶، ۱۰، ۱۲ |
| ML / MLOps | فصل ۴، ۵، ۶، ۹ |
| LLM / RAG builder | فصل ۷، ۸ |
| Platform / K8s | فصل ۱۶، ۷ (MCP) |
| Governance / compliance | فصل ۱۱، ۱۵ |
| پیاده‌سازی production | **Appendix E** + فصل ۶ |

---

## ۲. نمای کلی ساختار

```
فصل ۱–۲ (مقدمه و دامنه)
  → فصل ۳ (تهدیدهای خودمختار)
  → فصل ۴–۵ (داده و زنجیرهٔ تأمین)
  → فصل ۶ (مدل lifecycle — محور راهنما)
  → فصل ۷–۸ (LLM/RAG/Agent/MCP)
  → فصل ۹ (anti-pattern)
  → فصل ۱۰–۱۱ (SOC و governance)
  → فصل ۱۲ (نقشهٔ threat-control-tool)
  → فصل ۱۳ (case study)
  → فصل ۱۴ (بلوغ)
  → فصل ۱۵ (جمع‌بندی و پیوست‌ها)
  → فصل ۱۶ (K8s)
  → Appendix E (Implementation Reference)
```

---

## ۳. فصل ۱ — چکیده و مقدمه (`01-intro.md`)

| بخش | خلاصه |
|-----|--------|
| **Abstract** | تعریف MLSecOps؛ مشکل ناکافی بودن DevSecOps برای AI؛ روش ترکیب چارچوب‌ها و الگوهای عملیاتی؛ محدودیت‌ها و کلمات کلیدی |
| **Introduction** | چرا AI نیاز به مدل امنیتی متفاوت دارد |
| **What this guide adds beyond OWASP, OpenSSF, and NIST** | چهار ادعای اختصاصی راهنما؛ لینک به Appendix E |
| **How to use this guide** | جدول مسیر مطالعه بر اساس نقش (اجرایی، امنیت، MLOps، LLM، K8s، managed API، production) |
| **Why DevSecOps Is Insufficient** | رفتار probabilistic؛ سطح حملهٔ گسترده؛ وابستگی به داده و drift |
| **AI Threat Surface (Executive Overview)** | لایه‌های داده، مدل، اپلیکیشن، governance، زیرساخت، runtime |
| **MLSecOps Principles** | شش اصل: evidence قبل از deploy، release decision صریح، validation مداوم runtime، supply chain traceable، threat-modeled controls، فرآیند قابل ممیزی |
| **Relationship between MLSecOps and DevSecOps** | جدول مقایسهٔ دارایی، تست، monitoring، evidence |
| **AI supply chain evidence (AI-BOM)** | گسترش SBOM برای artifactهای AI |
| **Lifecycle Overview** | نمای ۸مرحله‌ای اجرایی و mapping به ۱۰ control point فصل ۶ |
| **Relationship to OWASP projects** | نقش مکمل LLM Top 10، LLMSVS، MCP Top 10، Agentic Security، ML Top 10 |
| **Focus and distinction from AISecOps** | MLSecOps = امنیت AI؛ AISecOps = استفاده از AI در SOC |

---

## ۴. فصل ۲ — دامنه، مخاطب و Threat Model (`02-scope-risk-threat-model.md`)

| بخش | خلاصه |
|-----|--------|
| **Scope of the article** | سازمان‌هایی که ML/AI در production دارند؛ کنترل‌ها threat-based |
| **Scenarios covered** | جدول سناریو: ML کلاسیک، LLM/RAG، managed AI، Agent، MCP، Shadow AI، enterprise، Edge/IoT/CPS |
| **Managed AI service scope** | shared responsibility؛ evidence جایگزین امضای وزن |
| **Managed AI services security reference** | پشتهٔ کنترل مشتری؛ evidence وقتی وزن را کنترل نمی‌کنید؛ baseline حداقلی managed API |
| **Customer control stack** | identity، data boundary، configuration، RAG، runtime، agent |
| **Evidence when you cannot sign model weights** | deployment ID، region، config snapshot به‌جای signature |
| **Minimum baseline for managed AI** | gateway، DLP، logging، control points ۷–۹ |
| **Primary audiences** | security، ML/MLOps، platform، governance، legal |
| **Selecting controls based on threat model** | کنترل اجباری vs اختیاری بر اساس معماری |
| **Risk management** | NIST AI RMF، ISO 42001، EU AI Act در سطح risk؛ threat modeling در سطح فنی |
| **Attack surface matrix** | سطح حمله → تهدید نمونه → کنترل (داده، مدل، managed API، supply chain، RAG، agent، MCP، Shadow AI، K8s، runtime) |
| **Expected output of threat modeling** | دارایی بحرانی، تهدید معنادار، کنترل اجباری، معیار block release، evidence مورد نیاز |

---

## ۵. فصل ۳ — تهدیدهای خودمختار AI (`03-threat-landscape.md`)

| بخش | خلاصه |
|-----|--------|
| **Reading priority** | اول demonstrated؛ بعد emerging؛ اخلاق و مجوز red team |
| **Overview** | تفاوت حملهٔ سنتی vs autonomous AI (مشاهده → استدلال → عمل → تطبیق) |
| **Agent Tool Abuse** | Tool Abuse/Injection، دستور خطرناک، API abuse — الگوی فعال |
| **Memory Poisoning** | مسمومیت حافظهٔ بلندمدت agent — الگوی فعال |
| **AI-driven Reconnaissance** | شناسایی خودکار محیط و دارایی |
| **AI-driven Lateral Movement** | حرکت جانبی با agent و ابزار |
| **AI Compute Hijacking** | سوءاستفاده از GPU/منابع inference |
| **Autonomous Data Exfiltration** | استخراج داده از طریق ابزار و پاسخ مدل |
| **Runtime Behavioral Threats** | الگوهای رفتاری مشکوک؛ نیاز به baseline نه فقط signature |
| **Emerging threats (summary)** | AI worm، malware/evasion تحقیقاتی — اولویت پایین‌تر |
| **MLSecOps Threat Modeling Considerations** | نگاشت به control point و SOC |
| **Relationship to Existing Frameworks** | OWASP، ATLAS، agentic frameworks |
| **Chapter Summary** | جمع‌بندی اولویت سرمایه‌گذاری کنترل |

---

## ۶. فصل ۴ — امنیت داده و حریم خصوصی (`04-data-security-privacy.md`)

| بخش | خلاصه |
|-----|--------|
| **Importance of data security** | داده به‌عنوان دارایی امنیتی و رفتار مدل |
| **Basic data controls** | دسترسی، lineage، versioning، PII masking، quality |
| **Privacy** | ریسک PII در training و operational data |
| **Sensitive data classification for scanning** | سطوح حساسیت برای اسکن خودکار |
| **Differential Privacy** | کاهش وابستگی مدل به رکورد فردی |
| **Information leakage from Embedding** | بازسازی اطلاعات از بردارها |
| **Privacy audit tools** | PrivacyRaven، ML Privacy Meter (informative) |
| **Experimentation environment security** | جداسازی آزمایش از production |
| **Supplementary controls for experimental environments** | محدودیت دسترسی و دادهٔ synthetic |
| **Data security in RAG** | ACL ingest، حساسیت سند، tenant isolation |
| **Feature Store security** | lineage، ACL، PII در feature |
| **Training data licensing and copyright** | ریسک حقوقی دادهٔ آموزشی |
| **Prompt and telemetry logging vs privacy** | GDPR/CCPA در لاگ prompt |
| **Practical principle** | دادهٔ مسموم یا ناشناس‌نشده نباید وارد pipeline شود |

---

## ۷. فصل ۵ — امنیت مدل، Artifact و Supply Chain (`05-model-artifact-supply-chain.md`)

| بخش | خلاصه |
|-----|--------|
| **Model as a security asset** | وزن‌ها و فرمت‌ها قابل حمله‌اند |
| **Model security controls** | scan، test، sign، access control |
| **Minimum Adversarial Robustness** | حداقل تست بر اساس modality |
| **Defining threat model before testing** | بدون threat model، تست معنا ندارد |
| **Minimum security tests** | backdoor، extraction، evasion (با توجه به نوع مدل) |
| **Risk of unsafe formats** | pickle، deserialization — RCE |
| **AI supply chain** | HuggingFace، registry، conversion pipeline |
| **MLOps infrastructure vulnerabilities** | MLflow، Ray، notebook servers |
| **Infrastructure-as-Code security for ML** | Terraform/Helm برای ML stack |
| **SBOM and AI-BOM** | CycloneDX ML-BOM؛ component مدل و dataset |
| **Security acceptance criteria** | آستانه‌های نمونه (قابل تنظیم در threat model) |
| **Provenance and signing** | Sigstore model-signing، Rekor |
| **Security evaluation output** | گزارش برای Evidence Pack |
| **Federated Learning** | aggregation امن، DP |
| **Key and secret management** | Vault، KMS، چرخش کلید API |
| **Practical principle** | هیچ artifact بدون scan و provenance promote نشود |

---

## ۸. فصل ۶ — مدل کنترل چرخهٔ عمر MLSecOps (`06-pipeline.md`)

> **توجه:** این فصل lifecycle control model است — **نه** پیاده‌سازی CI/CD آماده.

| بخش | خلاصه |
|-----|--------|
| **Control model objective** | تصمیم و evidence در هر مرحله؛ بدون artifact بدون کنترل |
| **Control model overview** | پیش‌نیاز planning + ۱۰ نقطهٔ کنترل |
| **Prerequisite: Planning and Threat Modeling** | scope، OWASP/ATLAS، کنترل اجباری، threat model در Evidence Pack |
| **Lifecycle control points** | جدول ۱۰ مرحله (زیر) |
| **Practical notes for each control point** | نکتهٔ عملی هر مرحله |
| **Release decision model** | تفکیک evidence-producing vs blocking (۴، ۷، ۸)؛ integrity در ۹ |
| **Continuous Training cycle** | CT بدون میان‌بر؛ canary/rollback |
| **CT cycle risks** | drift، poison در دادهٔ جدید |
| **Control points in CT cycle** | کدام مراحل در CT اجباری‌اند |
| **Secure deployment methods for retrained models** | canary، shadow، blue-green |
| **Difference between Data Drift and Adversarial Drift** | playbook جدا |
| **Alignment with MLOps lifecycle and OpenSSF** | mapping مکمل OpenSSF whitepaper |
| **Common implementation challenges** | silo، manual gate، managed API |
| **Minimum security baseline** | Level 1 vs Level 2+ |
| **Lifecycle control prioritization** | MUST / SHOULD |
| **Stage 7 test acceptance conditions** | آستانه‌های نمونه red team |
| **Red Team program and security test cadence** | برنامهٔ تست نسخه‌دار |
| **Implementation note** | بدون CI/CD مرجع؛ نیاز به evidence ساختاریافته |
| **Golden rule** | بدون integrity + Evidence Pack → no production |
| **Operational summary** | چهار قانون عملیاتی |

### ده Control Point (فصل ۶)

| # | نام | هدف |
|---|-----|-----|
| 1 | Initiate Change | شروع مجاز تغییر |
| 2 | Load Artifacts | بارگذاری امن + manifest/hash |
| 3 | Security & Quality Review | اسکن کد، notebook، container، IaC |
| 4 | **Data / Artifact Decision** | **Release decision** — block/escalate |
| 5 | Train or Configure | آموزش/fine-tune/RAG/agent config |
| 6 | Evaluate Model | عملکرد، fairness، baseline |
| 7 | **Security Validation** | **Release decision** (L2+) — red team، injection |
| 8 | **Release Decision** | **Release decision** — compliance، business |
| 9 | Integrity and Provenance | امضا یا config snapshot |
| 10 | Store & Monitor | registry + telemetry + Evidence Pack |

---

## ۹. فصل ۷ — امنیت LLM و RAG (`07-llm-rag-security.md`)

| بخش | خلاصه |
|-----|--------|
| **How LLM security differs from classic ML** | runtime، prompt، probabilistic |
| **Primary LLM threats** | جدول OWASP LLM01–10 کاربردی |
| **Security controls for LLM** | gateway، authZ، moderation، anomaly |
| **Secure architecture for RAG** | User → Gateway → Retriever → LLM → Output Gate |
| **Ingest security in RAG** | allowlist، scan، hash سند |
| **Three-layer controls in RAG** | ingest، retrieval، generation |
| **Retrieval Poisoning** | سند مخرب در corpus |
| **Embedding Poisoning** | دستکاری بردار |
| **Reindex Playbook** | مراحل پاکسازی و re-index |
| **Cloud Native and Multi-Tenant deployment** | isolation، quota |
| **Advanced Multi-Tenant hardening** | cache leakage، tenant boundary |
| **Fine-tuning risks** | behavioral drift، overfitting به دادهٔ حساس |
| **System Prompt Leakage (LLM07)** | system prompt کنترل امنیتی نیست |
| **Advanced Prompt Injection techniques** | token smuggling، ASCII art، many-shot |
| **Direct and indirect Prompt Injection** | sequence diagram حملهٔ غیرمستقیم via RAG |
| **Guardrails** | pre/post model |
| **Guardrail limitations** | bypass، false positive — defense in depth |
| **LoRA, PEFT, and adapter supply chain** | adapter = artifact امنیتی |
| **Model Context Protocol (MCP) security** | بخش جامع MCP |
| → Architecture and trust boundaries | Host → Client → Gateway → Servers |
| → OWASP MCP Top 10 mapping | کنترل برای MCP01–MCP10 |
| → MCP gateway pattern | production pattern |
| → MCP server hardening checklist | حداقل bar |
| → MCP scanning and tooling | mcps-audit، mcp-scan، MCP Guardian |
| → MCP on Kubernetes | استقرار امن server |
| → MCP and Shadow AI overlap (MCP09) | shadow MCP در IDE |
| → Evidence Pack — MCP fields | فیلدهای ممیزی MCP |
| **If only three LLM/RAG controls** | gateway، ACL retrieval، output gate |
| **LLM and RAG control prioritization** | MUST / SHOULD |
| **LLM verification approach** | مکمل OWASP LLMSVS |
| → Verification scope by system type | chatbot vs RAG vs agent |
| → Acceptance criteria | تعریف در threat model |
| **Practical principle / summary** | جمع‌بندی اجرایی |

---

## ۱۰. فصل ۸ — امنیت Agentic AI (`08-agentic-ai-security.md`)

| بخش | خلاصه |
|-----|--------|
| **Why Agentic AI poses a different risk** | action risk؛ OWASP Agentic / ASI02 |
| **Chatbot vs AI agent** | جدول تفکیک scope امنیتی |
| **Agent reference architecture** | orchestrator، LLM، memory، data، tools، actions |
| **Agent think–act cycle** | Observe → Reason → Plan → Act → Learn + کنترل هر مرحله |
| **MAESTRO framework (CSA)** | threat modeling multi-agent |
| **Agent attack surface** | overview |
| → Six attack domains | prompt، tool، memory، data، multi-agent، supply chain |
| → Internal components | جدول component → boundary |
| **Tool trust boundary** | همهٔ ورودی downstream غیرقابل اعتماد |
| **Intent Gate** | تأیید سیاست قبل از act |
| **Intent Gate implementation components** | policy engine، context، risk score |
| **OPA vs Cedar comparison** | انتخاب policy engine |
| **Tool Output Injection** | خروجی ابزار = ورودی مخرب به agent |
| → Chain exploitation scenario | زنجیرهٔ exploit چندمرحله‌ای |
| **Memory Poisoning** | مسمومیت STM/LTM |
| → Memory contamination path | مسیر آلودگی |
| → Real-world context poisoning example | سناریوی workflow |
| → Vendor and payment approval poisoning | سناریوی مالی |
| → Conversation manipulation | دستکاری چندنوبتی |
| **Data exfiltration model** | چهار مرحلهٔ exfiltration |
| **Multi-Agent** | delegation و trust |
| **Multi-Agent principles** | جلوگیری از privilege escalation بین agent |
| **Agent defense layers** | لایه‌های دفاع depth |
| **Secure agent lifecycle** | design → deploy → monitor |
| **Runtime controls for Agent** | telemetry، sandbox، egress |
| **Three critical controls** | Intent Gate، Output Gate، scoped tools |
| **Agent control prioritization** | MUST / SHOULD |
| **Agent security metrics** | KPIهای agent |
| **Agent security DO's and DON'Ts** | چک‌لیست design review |
| **MCP tool connections** | لینک به فصل ۷ |
| **Practical principle** | هیچ tool/memory/output مورد اعتماد کامل نیست |

---

## ۱۱. فصل ۹ — Anti-patternهای MLSecOps (`09-anti-patterns.md`)

| بخش | خلاصه |
|-----|--------|
| **Why anti-patterns matter** | شبیه امنیت بدون audit واقعی |
| **Common anti-patterns** | فهرست کلی |
| **Model without provenance** | deploy بدون hash/sign |
| **RAG without security boundary** | کل سازمان در vector DB |
| **Agent without tool control** | دسترسی نامحدود ابزار |
| **One-time security testing** | تست یک‌بار قبل از production |
| **Practical principle** | ابزار بدون release decision = anti-pattern |

---

## ۱۲. فصل ۱۰ — مانیتورینگ، SOC و IR (`10-monitoring-soc-ir.md`)

| بخش | خلاصه |
|-----|--------|
| **Monitoring in AI systems** | چرا log کلاسیک کافی نیست |
| **Data required for telemetry** | prompt، response، tool call، model version، session/trace ID |
| **SOC integration** | feed به SIEM؛ correlation |
| **Detection Engineering** | rule برای رفتار AI |
| **Threat analysis with MITRE ATLAS** | mapping alert → technique |
| **Sample SIEM scenarios** | injection، leakage، Shadow AI، tool abuse |
| **Sample attack chain** | recon → access → exfiltration |
| **Incident response** | rollback مدل، re-index، disable tool |
| **False positive management** | baseline، segmentation، feedback |
| **Incident response SLA** | P1–P4 با زمان acknowledge/containment |
| **Evidence required for incident analysis** | Prompt Trace، Tool Logs، Evidence Pack |
| **First 30 minutes of an incident** | snapshot → contain → verify → rollback → timeline |
| **Day-2 operations** | rotation، permission review، embedding cleanup |
| **Security metrics** | injection rate، block rate، drift |
| **SOC control prioritization** | MUST / SHOULD |
| **If only three SOC/Runtime controls** | logging، detection rule، playbook |
| **Practical principle / summary** | SOC بخش اجباری MLSecOps |

---

## ۱۳. فصل ۱۱ — حاکمیت، Compliance و Evidence Pack (`11-governance-evidence.md`)

| بخش | خلاصه |
|-----|--------|
| **Governance in MLSecOps** | تصمیم قابل توضیح و ممیزی |
| **Shadow AI governance** | برنامهٔ کامل Shadow AI |
| → Why shadow AI matters | دادهٔ prod در ChatGPT مصرفی |
| → Shadow AI vs sanctioned path | مسیر مجاز vs غیرمجاز |
| → Five-layer detection stack | CASB، DLP، egress، training |
| → AI-AUP minimum contents | محتوای سیاست استفاده |
| → 30-day shadow AI rollout | برنامهٔ عملیاتی ۳۰ روز |
| → Technical controls | mapping به MLSecOps |
| → Open-source gateway references | مسیر sanctioned |
| → Evidence Pack fields for shadow AI | فیلدهای برنامه |
| → Anti-patterns | paste prod data، personal API key |
| **OpenSSF MLSecOps Mapping (2025)** | جدول stage OpenSSF → فصل راهنما |
| **Optional assurance tiering** | سطح‌بندی illustrative |
| **STRIDE and FMEA applied to ML assets** | threat modeling ساختاریافته |
| **Reference frameworks** | NIST، ISO، EU AI Act |
| **What is an Evidence Pack?** | بستهٔ evidence قابل ممیزی (الگو، نه استاندارد OWASP) |
| **Recommended Evidence Pack contents** | data، model، security، supply chain، policy، deploy، runtime |
| **Evidence Pack components** | identity، integrity، testing، policy، runtime |
| **Relationship to compliance** | NIST، EU AI Act، ISO 23894 |
| → EU AI Act → controls | mapping high-risk |
| → EU AI Act → Evidence Pack | فیلدهای مستندسازی |
| **Policy-as-Code** | OPA/Conftest/Kyverno |
| **Responsibilities** | نقش‌ها |
| **Personas and shared responsibility** | RACI مفهومی |
| **Tamper-evident storage** | object lock، signature |
| **Security validation and assurance** | assurance program |
| **Assurance metrics** | متریک‌های governance |
| **Optional regression scoring pattern** | فرمول illustrative (غیر استاندارد) |
| **Governance Benchmark Suite** | مجموعهٔ ارزیابی |
| **Verification vs. validation** | تفکیت مفاهیم |
| **Vulnerability disclosure** | منابع intelligence |
| **Practical principle** | governance بدون Evidence Pack ناقص است |

---

## ۱۴. فصل ۱۲ — نقشهٔ Threat، Control و Tool (`12-threat-control-tools-map.md`)

| بخش | خلاصه |
|-----|--------|
| **Purpose of Mapping** | threat → control → capability؛ ابزار informative |
| **Primary Mapping** | جدول بزرگ تهدیدها (poisoning، injection، MCP، agent، …) |
| **Tool Layers** | L1–L7 diagram |
| **Capabilities by lifecycle area** | ingest، model، release، runtime، SOC |
| **Layered Tool Architecture** | L1 Data → L7 Observability |
| **Appendix: Informative tool command reference** | CLI اختیاری — **نه بخش اصلی** |
| → Design principle | observe → decision → evidence |
| → L2 ModelScan، Gitleaks، Trivy، NB Defense، ART | artifact و code scan |
| → L2 Garak، Promptfoo، PyRIT | LLM red team |
| → L2 mcps-audit، mcp-scan، MCP-Shield | MCP scan |
| → L3 Syft، CycloneDX/cdxgen، Sigstore | SBOM/AI-BOM/sign |
| → L4 OPA/Conftest | policy-as-code |
| → L6 NeMo Guardrails | runtime guard |
| → L2 AI-exploits، AI-Infra-Guard، Agentic Security | infra/agent test |
| → L2 PrivacyRaven، ML Privacy Meter | privacy audit |
| → Summary table | tool → exit code → decision |
| **OWASP ML Top 10 Mapping to MLOps Stages** | ML01–ML10 → stage |
| **Threat, Control, and Tool Reference Card** | کارت فشرده |
| **MITRE ATLAS Mapping** | technique → control |
| **Commercial Tool Market Map** | بازار ابزار (غیرتأییدشده) |
| **Tool Selection Criteria** | معیار انتخاب |
| **Emerging AI-native Threats** | تهدیدهای در حال ظهور |
| **Practical Principle** | mapping برای architecture review |

---

## ۱۵. فصل ۱۳ — مطالعات موردی (`13-case-studies.md`)

| بخش | نوع | درس کلیدی |
|-----|-----|-----------|
| **Chapter objective** | — | incident واقعی vs الگوی illustrative |
| **LeftoverLocals (CVE-2023-4969)** | Documented | نشت GPU memory |
| **MLflow vulnerabilities** | Documented | پلتفرم MLOps باز و بدون auth |
| **ClearML Confused Learning** | Documented | امنیت pipeline آزمایش |
| **SILENT SABOTAGE (HF Conversion Bot)** | Documented | supply chain تبدیل مدل |
| **BentoML / LangChain RCE** | Documented | deserialization |
| **HuggingFace unsafe models** | Documented | scale مدل‌های ناامن |
| **Agent API key exposure** | Illustrative | کلید در trace agent |
| **Pickle-based RCE** | Pattern class | pickle در registry |
| **PoisonGPT** | Research demo | مدل مخرب در HF |
| **Prompt injection (public)** | Incident class | injection در سیستم‌های عمومی |
| **Shadow LLM (Samsung)** | Documented | دادهٔ prod در ChatGPT |
| **Indirect injection Copilot/RAG** | Research | سند خارجی مخرب |
| **AI tools inside DevOps** | Illustrative | AI در CI بدون کنترل |
| **RAG in org knowledge base** | Illustrative | مرز دسترسی RAG |
| **MCP red team lab** | Illustrative | آزمایش MCP09 و tool poison |
| **Summary of lessons** | — | الگوهای مشترک |
| **Practical principle** | — | case study → control point |

---

## ۱۶. فصل ۱۴ — نقشهٔ بلوغ MLSecOps (`14-maturity-roadmap.md`)

| بخش | خلاصه |
|-----|--------|
| **Why Phased Maturity Matters** | پیاده‌سازی تدریجی |
| **Maturity Levels** | سه سطح |
| **Level 1: Foundational** | baseline حداقلی؛ decision در ۴ و ۸؛ stage ۷ record |
| **Level 2: Operational** | blocking در ۴، ۷، ۸؛ CT کامل؛ signing |
| **Level 3: Mature** | assurance پیشرفته؛ red team مستمر؛ metrics |
| **Minimum Starting Controls** | شروع سریع |
| **Recommended 90-Day Path** | برنامهٔ ۹۰ روز |
| **Maturity Metrics** | سنجش پیشرفت |
| **Common Mistakes on the Maturity Path** | اشتباهات رایج |
| **Practical Principle** | بلوغ process-based است نه «صفر incident» |

---

## ۱۷. فصل ۱۵ — جمع‌بندی و پیوست‌ها (`15-conclusion-appendix.md`)

| بخش | خلاصه |
|-----|--------|
| **Conclusion** | امنیت AI در کل lifecycle |
| **Key Principles** | پنج اصل جمع‌بندی |
| **Compact Checklist** | سوالات سریع دامنه‌ای |
| **Production Operational Checklist** | چک‌لیست production |
| → Minimum RACI | نقش‌ها |
| → Data and Privacy | کنترل داده |
| → Model and Supply Chain | artifact و sign |
| → Lifecycle Controls, CT, RAG, Agent | control pointها |
| → Runtime, Cloud-native, and SOC | telemetry و IR |
| → Governance and Evidence Pack | حاکمیت |
| **Short Glossary** | واژه‌نامهٔ اصطلاحات |
| **Appendix A: Threat/Control/Tool Reference Card** | کارت مرجع فشرده |
| **Appendix B: MITRE ATLAS Mapping** | mapping تکنیک‌ها |
| **Appendix D: Managed AI Services Security Reference** | چک‌لیست managed API |
| → Shared responsibility | جدول provider vs customer |
| → Pre-production checklist | قبل از prod |
| → Evidence Pack fields (managed API) | فیلدهای deployment |
| → OWASP v1 publication readiness | چک‌لیست انتشار community guide |
| **References** | منابع |
| → Frameworks and Standards | NIST، ISO، EU AI Act، … |
| → Threat Taxonomy and Security Guides | OWASP، ATLAS، … |
| → Open-Source Tools and Projects | ابزار OSS |
| → Reference Papers and Reports | مقالات |
| **Appendix: Claims & Evidence** | ردیابی ادعا → منبع |
| **Mermaid Diagram Guide** | رندر GitHub/Word |
| **GitHub Version** | نگهداری markdown |
| **Final Conclusion** | جمع‌بندی نهایی |
| → What this guide contributes | چهار ادعای اختصاصی + Appendix E |

---

## ۱۸. فصل ۱۶ — مرجع استقرار Kubernetes (`16-kubernetes-deployment-reference.md`)

| بخش | خلاصه |
|-----|--------|
| **Purpose** | الگوی معماری — **بدون manifest آماده در repo** |
| **Reference architecture** | Gateway → Inference → Registry + SOC |
| **Prerequisites** | cluster baseline |
| **Namespace isolation and RBAC** | جداسازی tenant/team |
| **Network policy — default deny** | egress کنترل‌شده |
| **Admission control — verify signed images** | Kyverno / ImageValidatingPolicy |
| **vLLM on Kubernetes** | الگوی امن Helm/API key |
| **KServe and generic model serving** | serving pattern |
| **GPU isolation and shared inference** | MIG، quota |
| **Runtime security on the cluster** | Falco/Tetragon |
| **Egress control for agentic workloads** | allowlist برای agent |
| **MCP servers on Kubernetes** | استقرار MCP امن |
| **Mapping to lifecycle control points** | K8s → control point ۳، ۹، ۱۰ |
| **Tool and reference index** | لینک upstream |
| **Minimum baseline checklist (Level 2)** | چک‌لیست production K8s |
| **Practical principle / summary** | test IaC در محیط خود |

---

## ۱۹. Appendix E — Implementation Reference (`17-appendix-e-implementation-reference.md`)

| بخش | خلاصه |
|-----|--------|
| **E.1 Architecture Cards** | کارت معماری per سناریو + دیاگرام Mermaid |
| → E.1.1 Enterprise RAG | gateway، ingest ACL، output gate |
| → E.1.2 Managed AI API | Azure/Bedrock/Vertex؛ config snapshot |
| → E.1.3 Self-hosted LLM (vLLM/KServe) | sign، admission، NetworkPolicy |
| → E.1.4 Agent + MCP | Intent Gate، tool allowlist |
| → E.1.5 Multi-agent | delegation، trace |
| → E.1.6 Classic ML | data + adversarial + sign |
| **E.2 Decision Matrix** | اگر معماری X → کنترل‌های اجباری + reference flow |
| **E.3 Threat Model Template** | جدول Asset/Threat/Control/Risk/Evidence + release blockers |
| **E.4 Evidence Pack Template** | YAML نمونهٔ فیلدها |
| **E.5 Operational Playbooks** | runbook کوتاه |
| → E.5.1 Runtime prompt injection | detect → contain → eradicate → lessons |
| → E.5.2 RAG contamination | reindex playbook |
| → E.5.3 Agent tool abuse | disable tool، policy review |
| **E.6 Master Control Matrix** | Threat → Prevent/Detect/Respond → control point → evidence |
| **Practical summary** | ۵ گام پیاده‌سازی |

---

## ۲۰. مسیرهای مطالعهٔ پیشنهادی

| هدف | مسیر |
|-----|------|
| نمای اجرایی | ۱ → ۲ → ۱۴ |
| درک تهدید | ۳ → ۲ → ۱۳ |
| پیاده‌سازی lifecycle | ۶ → ۱۲ → ۱۵ |
| LLM / RAG / Agent | ۷ → ۸ → ۹ |
| Managed API فقط | ۲ → ۷ → Appendix D |
| Shadow AI / governance | ۲ → ۱۱ → ۱۳ → ۹ |
| MCP | ۷ → ۸ → ۱۲ → ۱۳ |
| SOC / operations | ۱۰ → ۱۱ |
| Kubernetes | ۱۶ |
| **Production rollout** | **Appendix E** → ۶ → ۱۲ |

---

## ۲۱. مفاهیم کلیدی

| اصطلاح | معنی |
|--------|------|
| Control point | نقطهٔ کنترل lifecycle (۱–۱۰) |
| Release decision | تصمیم blocking در ۴، ۷، ۸ |
| Integrity and Provenance | control point ۹ — امضا یا config snapshot |
| Evidence Pack | بستهٔ ممیزی هر انتشار |
| Intent Gate | تأیید سیاست قبل از اجرای tool |
| Output Gate | بازبینی خروجی/خروجی tool |
| Shadow AI | LLM غیرمجاز سازمانی |
| MCP09 | Shadow MCP server |
| AI-BOM / ML-BOM | فهرست اجزای AI supply chain |
| CT cycle | Continuous Training با همان control pointها |
| Data Drift vs Adversarial Drift | drift آماری vs رفتار حمله‌ای |

---

## ۲۲. فرمت، خروجی و ابزار

| قالب | توضیح |
|------|--------|
| Markdown | `chapters-en/*.md` — ۱۸ فایل محتوا |
| Word | `MLSecOps-Guide-v1.0.docx` — ساخته‌شده در workspace محلی (خارج از این ریپو) |
| Mermaid | ۲۶ دیاگرام (GitHub native + PNG در Word) |
| `_docx_assets/mermaid/` | PNGهای میانی export |

---

## ۲۳. یادآوری

- راهنما **community reference** است — جایگزین مشاورهٔ حقوقی یا certification نیست.  
- ابزارها و اعداد **informative** هستند؛ در threat model سازمان تنظیم شوند.  
- Appendix E و چک‌لیست‌ها **الگو** هستند — در GRC/IaC خود validate کنید.
