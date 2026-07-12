# ISO/IEC 42001:2023 — مرجع سرفصل‌ها و ساختار

> **خلاصه:** اولین استاندارد بین‌المللی برای **سیستم مدیریت هوش مصنوعی (AIMS — Artificial Intelligence Management System)**.  
> منتشرکننده: ISO/IEC JTC 1/SC 42 · تاریخ انتشار: **دسامبر ۲۰۲۳**  
> ساختار: **High-Level Structure (HLS)** مشابه ISO 27001، ISO 9001، ISO 14001 (Plan–Do–Check–Act)

**توجه:** این سند یک **خلاصه مرجعی** است، نه جایگزین متن رسمی استاندارد. برای audit، certification و استناد حقوقی باید نسخه رسمی ISO/IEC 42001:2023 را از [iso.org](https://www.iso.org/standard/81230.html) تهیه کنید.

---

## 1. نمای کلی

| مورد | توضیح |
|------|--------|
| **عنوان کامل** | Information technology — Artificial intelligence — Management system |
| **مخاطب** | هر سازمانی که AI system **توسعه می‌دهد، ارائه می‌کند یا استفاده می‌کند** |
| **هدف** | establish, implement, maintain, continually improve یک AIMS در بستر سازمان |
| **رویکرد** | risk-based + **AI system impact assessment** (اثر بر افراد، گروه‌ها و جامعه) |
| **کنترل‌های مرجع** | **۳۸ control** در Annex A (۹ control objective: A.2 تا A.10) |
| **Statement of Applicability (SoA)** | سازمان کنترل‌های قابل‌اعمال را بر اساس risk/impact انتخاب و توجیه می‌کند |

### تفاوت کلیدی با ISO 27001

| ISO/IEC 27001 | ISO/IEC 42001 |
|---------------|---------------|
| ریسک **امنیت اطلاعات** برای سازمان | ریسک **AI** برای سازمان **+ impact** AI بر افراد/جامعه |
| 93 control در Annex A | 38 control در Annex A |
| ISMS | AIMS |
| بدون impact assessment اجباری مشابه | **AI system impact assessment** (Clause 6.1.4 / 8.4) |

---

## 2. فهرست مطالب رسمی (Table of Contents)

### بخش اصلی (Clauses 1–10)

| Clause | عنوان | ماهیت |
|--------|--------|--------|
| **Foreword** | مقدمه ISO/IEC | — |
| **Introduction** | مفاهیم AI، نقش سازمان، trustworthiness | راهنما |
| **1** | Scope | توصیفی |
| **2** | Normative references | ISO/IEC 22989 (اصطلاحات AI) |
| **3** | Terms and definitions | تعاریف (AIMS، AI system impact assessment، SoA، data quality، …) |
| **4** | Context of the organization | **الزام** |
| **5** | Leadership | **الزام** |
| **6** | Planning | **الزام** |
| **7** | Support | **الزام** |
| **8** | Operation | **الزام** |
| **9** | Performance evaluation | **الزام** |
| **10** | Improvement | **الزام** |

### پیوست‌ها (Annexes)

| Annex | عنوان | ماهیت |
|-------|--------|--------|
| **A** | Reference control objectives and controls | **Normative** (مرجع کنترل) |
| **B** | Implementation guidance for AI controls | **Normative** (راهنمای پیاده‌سازی برای Annex A) |
| **C** | Potential AI-related organizational objectives and risk sources | Informative |
| **D** | Use of the AI management system across domains or sectors | Informative |
| **Bibliography** | استانداردها و منابع مرتبط | Informative |

---

## 3. Clause 4 — Context of the organization

| زیربند | عنوان |
|--------|--------|
| 4.1 | Understanding the organization and its context |
| 4.2 | Understanding the needs and expectations of interested parties |
| 4.3 | Determining the scope of the AI management system |
| 4.4 | AI management system |

**نکات مهم (4.1):** سازمان باید نقش خود را نسبت به AI system تعیین کند، از جمله:

- AI provider / platform / product-service provider  
- AI producer (developer, designer, operator, tester, deployer, impact assessor, …)  
- AI customer / user  
- AI partner (integrator, data provider)  
- AI subject (data subject و سایر subjects)  
- relevant authorities (regulator, policymaker)

---

## 4. Clause 5 — Leadership

| زیربند | عنوان |
|--------|--------|
| 5.1 | Leadership and commitment |
| 5.2 | AI policy |
| 5.3 | Roles, responsibilities and authorities |

---

## 5. Clause 6 — Planning

| زیربند | عنوان |
|--------|--------|
| 6.1 | Actions to address risks and opportunities |
| 6.1.1 | General |
| 6.1.2 | **AI risk assessment** |
| 6.1.3 | **AI risk treatment** |
| 6.1.4 | **AI system impact assessment** |
| 6.2 | AI objectives and planning to achieve them |
| 6.3 | Planning of changes |

> **6.1.4** یکی از تمایزهای اصلی 42001 نسبت به MSSهای کلاسیک است: ارزیابی formal تأثیر AI بر **individuals, groups, societies**.

---

## 6. Clause 7 — Support

| زیربند | عنوان |
|--------|--------|
| 7.1 | Resources |
| 7.2 | Competence |
| 7.3 | Awareness |
| 7.4 | Communication |
| 7.5 | Documented information |
| 7.5.1 | General |
| 7.5.2 | Creating and updating documented information |
| 7.5.3 | Control of documented information |

---

## 7. Clause 8 — Operation

| زیربند | عنوان |
|--------|--------|
| 8.1 | Operational planning and control |
| 8.2 | AI risk assessment (operational) |
| 8.3 | AI risk treatment (operational) |
| 8.4 | AI system impact assessment (operational) |

**عملیات:** این clause جایی است که Annex A controls در practice operationalize می‌شوند.

---

## 8. Clause 9 — Performance evaluation

| زیربند | عنوان |
|--------|--------|
| 9.1 | Monitoring, measurement, analysis and evaluation |
| 9.2 | Internal audit |
| 9.2.1 | General |
| 9.2.2 | Internal audit programme |
| 9.3 | Management review |
| 9.3.1 | General |
| 9.3.2 | Management review inputs |
| 9.3.3 | Management review results |

---

## 9. Clause 10 — Improvement

| زیربند | عنوان |
|--------|--------|
| 10.1 | Continual improvement |
| 10.2 | Nonconformity and corrective action |

---

## 10. Annex A — 38 Reference Controls (A.2 تا A.10)

کنترل‌ها **principle-based** هستند؛ سازمان در SoA مشخص می‌کند کدام‌ها apply می‌شوند.

### A.2 — Policies related to AI (3 controls)

| Control | عنوان |
|---------|--------|
| A.2.2 | AI policy |
| A.2.3 | Alignment with other organisational policies |
| A.2.4 | Review of the AI policy |

### A.3 — Internal organisation (2 controls)

| Control | عنوان |
|---------|--------|
| A.3.2 | AI roles and responsibilities |
| A.3.3 | Reporting of concerns |

### A.4 — Resources for AI systems (5 controls)

| Control | عنوان |
|---------|--------|
| A.4.2 | Resource documentation |
| A.4.3 | Data resources |
| A.4.4 | Tooling resources |
| A.4.5 | System and computing resources |
| A.4.6 | Human resources |

### A.5 — Assessing impacts of AI systems (4 controls)

| Control | عنوان |
|---------|--------|
| A.5.2 | AI system impact assessment process |
| A.5.3 | Documentation of AI system impact assessments |
| A.5.4 | Assessing AI system impact on individuals or groups of individuals |
| A.5.5 | Assessing societal impacts of AI systems |

### A.6 — AI system life cycle (9 controls)

| Control | عنوان |
|---------|--------|
| A.6.1.2 | Objectives for responsible development of AI system |
| A.6.1.3 | Processes for responsible design and development of AI systems |
| A.6.2.2 | AI system requirements and specification |
| A.6.2.3 | Documentation of AI system design and development |
| A.6.2.4 | AI system verification and validation |
| A.6.2.5 | AI system deployment |
| A.6.2.6 | AI system operation and monitoring |
| A.6.2.7 | AI system technical documentation |
| A.6.2.8 | AI system recording of event logs |

**A.6.2.6** صراحتاً تهدیدهای امنیتی AI-specific را mention می‌کند (مثل data poisoning، model stealing، model inversion).

### A.7 — Data for AI systems (5 controls)

| Control | عنوان |
|---------|--------|
| A.7.2 | Data for development and enhancement of AI system |
| A.7.3 | Acquisition of data |
| A.7.4 | Quality of data for AI systems |
| A.7.5 | Data provenance |
| A.7.6 | Data preparation |

### A.8 — Information for interested parties of AI systems (4 controls)

| Control | عنوان |
|---------|--------|
| A.8.2 | System documentation and information for users |
| A.8.3 | External reporting |
| A.8.4 | Communication of incidents |
| A.8.5 | Information for interested parties |

### A.9 — Use of AI systems (3 controls)

| Control | عنوان |
|---------|--------|
| A.9.2 | Processes for responsible use of AI systems |
| A.9.3 | Objectives for responsible use of AI system |
| A.9.4 | Intended use of the AI system |

### A.10 — Third-party and customer relationships (3 controls)

| Control | عنوان |
|---------|--------|
| A.10.2 | Allocation of responsibilities |
| A.10.3 | Suppliers |
| A.10.4 | Customers |

---

## 11. Annex B — Implementation guidance (normative)

راهنمای پیاده‌سازی **برای هر control در Annex A** (جزئیات operational، مثال‌ها، considerations).  
در audit معمولاً **Annex A + Clauses 4–10** محور هستند؛ تیم implementation باید Annex B را برای هر control applicable بخواند.

---

## 12. Annex C — Objectives and risk sources (informative)

### اهداف سازمانی مرتبط با AI (نمونه)

Accountability · AI expertise · Data quality · Environmental impact · Fairness · Maintainability · Privacy · Robustness · Safety · Security · Transparency and explainability · Adherence to AI ethical principles

### منابع ریسک AI (نمونه)

Complexity of environment · Lack of transparency/explainability · Level of automation · ML-related risks · System hardware issues · System lifecycle issues · Technology readiness · Unclear responsibility for AI risks

> برای risk assessment عمیق‌تر، استاندارد مکمل **ISO/IEC 23894** (AI risk management guidance) پیشنهاد می‌شود.

---

## 13. Annex D — Domains and sectors (informative)

راهنما برای:

- اعمال AIMS در **چند business unit** یا **چند نوع AI system**  
- تطبیق با **context بخش/صنعت** (healthcare، finance، public sector، …)  
- **یکپارچگی** با سایر MSSها (27001، 27701، 9001)  
- مدل «program + systems»: لایه governance پایدار + execution سطح هر AI system

---

## 14. تعاریف کلیدی (Clause 3 — انتخابی)

| Term | معنی کوتاه |
|------|------------|
| **AIMS** | AI Management System |
| **AI system impact assessment** | فرایند documented برای شناسایی/ارزیابی/رسیدگی به impacts بر individuals, groups, societies |
| **Statement of Applicability (SoA)** | مستندسازی همه controls لازم + justification برای include/exclude |
| **Data quality** | ویژگی داده که requirements سازمان را در context مشخص برآورده کند |
| **Control** | measure که risk را maintain/modify می‌کند |

مرجع اصطلاحات AI: **ISO/IEC 22989:2022**.

---

## 15. استانداردها و فریم‌ورک‌های مرتبط

| استاندارد / فریم‌ورک | نقش |
|---------------------|-----|
| **ISO/IEC 22989** | Concepts and terminology (مرجع normative در Clause 2) |
| **ISO/IEC 23894** | AI risk management — guidance برای risk assessment |
| **ISO/IEC 27001** | Information security MSS — overlap در supplier, documentation, incident |
| **ISO/IEC 27701** | Privacy extension — وقتی AI با PII کار می‌کند |
| **ISO/IEC 23053** | AI/ML framework and lifecycle |
| **NIST AI RMF** | Govern / Map / Measure / Manage — مکمل غیر-certifiable |
| **EU AI Act** | Regulation — بسیاری از الزامات high-risk با Clauses و Annex A هم‌راستا هستند |

### نگاشت تقریبی NIST AI RMF ↔ ISO 42001

| NIST AI RMF | ISO/IEC 42001 |
|-------------|---------------|
| **Govern** | Clauses 4–5، A.2–A.3 |
| **Map** | A.4، A.7 |
| **Measure** | A.5، A.6.2.4 |
| **Manage** | A.6.2.5–A.6.2.8، A.8–A.10 |

---

## 16. Plan–Do–Check–Act (PDCA)

| فاز | محتوا |
|-----|--------|
| **Plan** | Clauses 4–7: context, policy, roles, risk/impact assessment, objectives |
| **Do** | Clause 8 + Annex A: اجرای controls و lifecycle |
| **Check** | Clause 9: monitoring, internal audit, management review |
| **Act** | Clause 10: corrective action, continual improvement |

---

## 17. ارتباط با MLSecOps Practical Reference Guide

راهنمای MLSecOps **جایگزین ISO 42001 نیست**؛ operational reference برای lifecycle، release gates و Evidence Pack است.  
ISO 42001 در AIMS/s governance layer؛ MLSecOps در **MLSecOps lifecycle control points** و evidence عملیاتی.

| موضوع ISO 42001 | فصل/بخش مرتبط در MLSecOps Guide |
|-----------------|----------------------------------|
| A.5 Impact assessment | Ch.2 (risk/threat model)، Ch.11 (governance) |
| A.6 Lifecycle | Ch.6 (pipeline / control points) |
| A.7 Data | Ch.4 (data security & privacy) |
| A.6.2.6 Operation & monitoring | Ch.10 (SOC/IR) |
| A.10 Suppliers / third-party | Ch.5 (supply chain)، Ch.12 (tools map) |
| Documented information / evidence | Ch.11، Appendix E (Evidence Pack) |

---

## 18. منابع جستجو (2026)

- [ISO.org — ISO/IEC 42001:2023](https://www.iso.org/standard/81230.html)  
- Preview فهرست مطالب: IEC webstore / standards preview  
- [Mindset Cyber — Annex A controls list](https://mindsetcyber.com.au/iso-42001-controls-list/)  
- [Control Stack — ISO 42001 framework guide](https://controlstack.au/frameworks/iso-iec-42001/)  
- [Modulos — Annexes A–D summary](https://docs.modulos.ai/frameworks/iso-42001/annexes-a-d)  
- [Grecta — Standard structure overview](https://grecta.com/iso-iec-42001/)

---

*آخرین به‌روزرسانی این مرجع: 2026-07-12 · بر اساس ISO/IEC 42001:2023 (First edition, 2023-12)*
