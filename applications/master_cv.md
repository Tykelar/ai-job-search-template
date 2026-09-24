<!--
  CURATED MASTER CV CONTENT BANK — the Markdown twin of applications/main_example.tex.

  PROVENANCE
  - This file and applications/main_example.tex are the same content: the full
    master bank, rendered once in Markdown and once in the compact LaTeX style.
    They must stay line-for-line identical (modulo LaTeX escaping). If they
    diverge, fix both together; if you maintain a source corpus, fix the source
    and regenerate. Do not hand-edit one twin only.
  - The content below is a REALISTIC EXAMPLE built to mirror a filled master bank
    in shape and density. Every bracketed token is a placeholder: /setup replaces
    the identity and history, and you expand the rest with your own facts and
    metrics. Delete any block that does not apply.

  PROJECT ENTRY FORMAT (mandatory)
  - Every project is THREE lines: **Title**, then *Tech stack: a · b · c*, then the
    description.
  - The stack line must fit ONE rendered line (~95 chars incl. the "Tech stack: " label).
    Trim items rather than wrap.
  - Titles and descriptions must NOT repeat the stack: no "(Python + Ollama)" title
    suffix, no "built with X, Y, Z" prose. Description = what it is + what came of it.

  LATEX TWIN PITFALL
  - In applications/main_example.tex, no bullet may start with a bare "[" -
    LaTeX parses \item [text] as \item's optional label and the text clips into
    the left margin. Keep the two twins aligned on word-initial bullets.

  ROLE UNDER THE /apply WORKFLOW
  - This file IS the verbatim-selection master: every tailored-CV line except the two
    composed surfaces must be an exact copy of a line in here. /apply picks and
    orders; it never rewords.
  - THE TWO COMPOSED SURFACES: the About Me paragraph (fully generative) and the
    CORE COMPETENCIES section (5-7 bullets written for each posting). Core
    Competencies REPLACES the Skills section on a tailored CV - the Skills bank
    below is never printed, it is the evidence pool the competency bullets are
    composed from. Every tool, method, and metric a competency bullet names must
    trace to this bank or to the candidate profile.
  - The Projects section prints as SELECTED PROJECTS on a tailored CV and closes
    with a mandatory one-line "Also built:" catch-all naming the projects cut.
  - applications/main_example.tex is this same content in the compact LaTeX
    template (the copy-base for tailored CVs).
-->

# [YOUR_NAME]

<!-- Professional headline variants, role-tailoring map, and keyword banks, if you
     keep them, live here. /apply selects a headline or framing; it never invents one. -->

---

## About Me
<!-- Voice/quality baseline for the generative About Me paragraph. Adapt per role;
     never paste verbatim into a tailored CV. Ends with the portfolio sentence. -->

[Primary degree] and [profession] who [throughline - the change you make or the thing you build]. At [most recent employer] I [most relevant achievement, ideally measurable], formalized in [thesis or flagship project]. Alongside this I [second thread of experience - founding, operations, research], and bring a [systems-level, cross-functional] perspective spanning [area 1], [area 2], and [area 3]. Get to know me better [here](https://your-portfolio.example.com)!

---

## Education

| Degree | Period | Institution | Key Topics |
|--------|--------|-------------|------------|
| [Primary Degree] | Sep 20XX - Jul 20XX | [Institution] | Thesis: "[Thesis title]" ([grade]) |
| [Second Degree] | Sep 20XX - Jul 20XX | [Institution] | Final project: [Final-project title] ([grade]) |
| [Optional Earlier Degree or Transfer] | Sep 20XX - Jul 20XX | [Institution] | [Key topics] |

---

## Work Experience

### [Most Recent Job Title], [Company] | Mon 20XX - Mon 20XX
[One-line company or product context - what the company does, for whom, and at what scale.]
- Built [tool, automation, or system] deployed in [context], enabling [measurable benefit] on [workflow].
- Led a [methodology]-driven re-engineering of [system or process], resolving [accumulated problem] and cutting [primary metric] by more than [X]%.
- Redesigned [workflow or process], contributing to [X]% [improvement in the outcome that matters most to the role].
- Restructured [task distribution or handovers], reducing [time or effort] by around [X]% and eliminating duplicated work.
- Contributed to the architecture and testing of [product feature], helping users [outcome the feature delivers].
- Contributed to the architecture and testing of [second system], letting users [outcome it enables].
- Drove integration of [technology or practice] into [product, team, or engineering workflow].
- Collaborated on [specialist system or model]: [data, evaluation, or training work you did] and [what it achieved].
- Designed and implemented [framework or system], including reusable [components], for scalable and maintainable [capability].
- Integrated [automation or test suite] into [pipeline or delivery workflow], enabling fully automated [execution or verification].
- Led the [old tool] to [new tool] migration, including trade-off evaluation, implementation, and documentation.
- Standardized [naming, data, or process] conventions and introduced [approach], reducing [coupling, instability, or rework].
- Scripted reproducible [local or virtual environments] ([setup, rebuild, and reset]) in [scripting language] to improve developer experience.
- Maintained and extended [existing system]; analyzed [reports or failure patterns] to prioritize fixes.

### [Previous Job Title], [Company] | Mon 20XX - Mon 20XX
[One-line company or initiative context.]
- Founded [organization or initiative]: legal incorporation, administrative setup, governance structure, and ongoing compliance.
- Owned the full [entrepreneurial or operational] process from idea to execution with no prior institutional support.
- Coordinated partnerships with public and private institutions to fund and support [programmes or projects].
- Led [activities], [workshops], and [initiatives] for [community or audience].
- Organized and monitored internal procedures for consistent operational execution.
- Managed the full physical setup and operational launch of [space or operation].

### [Earlier Job Title], [Company] | Mon 20XX - Mon 20XX
- Organized inventory, materials, and [logistics or storage] flows.
- Optimized [procedures], improving [metric] by up to [X]%.
- Supported the full [operational cycle] ([picking, dispatch, transport, retrieval]); handled [specialized operational task].
- Performed [technical or assembly] support, including [task].

### [Earliest Job Title], [Company], [Country] | Mon 20XX - Mon 20XX
- Built [databases or reports] from publicly available information for [purpose].
- Conducted [outreach] for partnership opportunities.
- Produced documentation linking [stakeholders or partners].

---

## Languages

[Language]: [Level] · [Language]: [Level] · [Language]: [Level] · [Language]: [Level]

---

## Skills
<!-- MASTER-ONLY evidence bank: Core Competencies is composed from these rows, and a
     tailored CV never prints this section. -->

- **[Process, Operations & Continuous Improvement]:** [Process analysis and mapping] · [Workflow re-engineering] · [Operational efficiency] · [Waste identification and prioritization] · [Procedure standardization] · [Task ownership and handover design] · [KPI design and tracking] · [Lean Software Development] · [Technical debt diagnosis and remediation] · [Continuous improvement (PDCA / Kaizen)] · [Process automation (RPA)] · [Structured business-case analysis]
- **[Quality, Testing & Reliability]:** [Software QA (manual and automated)] · [End-to-end test framework design] · [Reusable test helpers and utilities] · [API integration testing] · [Component-level unit testing] · [Test pyramid design and coverage rebalancing] · [Flaky test mitigation] · [Seed-driven test data] · [Failure-pattern and log analysis] · [Shift-left quality] · [Eval and benchmark harness design (golden sets, controlled A/B)]
- **[CI/CD, DevOps & Delivery]:** [CI/CD foundations and practical application] · [Pipeline optimization and feedback-loop reduction] · [Build and test resource efficiency] · [CI job integration for test batteries] · [Test parallelization] · [Workflow governance] · [Local environment automation scripting] · [Environment reproducibility] · [Containerization and deployment (Docker, Docker Compose)] · [Tooling and migration assessment]
- **[Applied AI & Machine Learning]:** [CNNs and image classification] · [Object detection] · [Sequence models] · [Transfer Learning] · [Hyperparameter optimization] · [LLM integration and AI agents] · [RAG system design, testing, and evaluation (recall@k benchmarking)] · [Vector databases] · [LangChain] · [Chatbot and embedded AI chat] · [Local LLM deployment] · [Prompt engineering] · [Deep-learning training practice] · [LLM guardrails and grounding enforcement] · [Agent harness engineering] · [Tool and function-calling design] · [Multi-agent orchestration] · [LLM observability and production monitoring]
- **[Security & Defensive Engineering]:** [Offensive security] · [OSINT and footprinting] · [Vulnerability assessment and reporting] · [SIEM implementation and log centralization] · [Threat detection and alerting] · [Host-based intrusion detection] · [File integrity monitoring] · [Wazuh and Elastic Stack (ELK)] · [Data privacy and PII redaction pipeline design] · [Penetration testing methodology] · [Detection rule authoring and alert tuning]
- **[Immersive Tech, 3D & Visualization]:** [Virtual and Augmented Reality] · [Digital Twins] · [3D modelling and printing] · [VTK 2D/3D/VR visualization] · [Unity (C#)] · [Godot] · [Blender] · [VRChat SDK] · [Additive manufacturing and rapid prototyping]
- **[Data, Analysis & Reporting]:** [Excel database creation and maintenance] · [Data structuring and reporting] · [SQL data handling] · [SPSS statistics] · [KPI and operational metric tracking] · [Analytical reasoning]
- **[Engineering Foundations]:** [Physics and Mathematics] · [Scientific computing and simulation (MATLAB)] · [Engineering drawings] · [Systems and computer hardware architecture] · [Elementary electrical circuits]
- **[Programming Languages]:** [Language 1] · [Language 2] · [Language 3] · [SQL] · [MATLAB] · [Shell / Bash] · [Full-stack web architecture]
- **[Tools & Platforms]:** [Tool 1] · [Tool 2] · [Tool 3] · [Framework 1] · [Framework 2] · [Database 1] · [Cloud platform] · [Container and orchestration tooling] · [CI platform] · [Microsoft 365]
- **[Soft Skills]:** [Initiative and autonomy] · [Problem-solving (root-cause-first)] · [Fast learning and resilience] · [Leadership and team dynamics] · [Communication with technical and non-technical stakeholders] · [Adaptability]

---

## Selected Projects

<!-- Three-line format: **Title**, *Tech stack: ...*, then description. Keep stacks
     under ~95 chars. Select 4-6 per role; close with the mandatory "Also built:" line. -->

**[Project Title 1]**
*Tech stack: [Tech item] · [Tech item] · [Tech item]*
[What the project is and what came of it - outcome, scale, or validation. Keep the stack out of this line.]

**[Project Title 2]**
*Tech stack: [Tech item] · [Tech item] · [Tech item]*
[What the project is and what came of it.]

**[Project Title 3]**
*Tech stack: [Tech item] · [Tech item] · [Tech item]*
[What the project is and what came of it.]

**[Project Title 4]**
*Tech stack: [Tech item] · [Tech item] · [Tech item]*
[What the project is and what came of it.]

**[Project Title 5]**
*Tech stack: [Tech item] · [Tech item] · [Tech item]*
[What the project is and what came of it.]

**[Project Title 6]**
*Tech stack: [Tech item] · [Tech item] · [Tech item]*
[What the project is and what came of it.]

**[Project Title 7]**
*Tech stack: [Tech item] · [Tech item] · [Tech item]*
[What the project is and what came of it.]

**[Project Title 8]**
*Tech stack: [Tech item] · [Tech item] · [Tech item]*
[What the project is and what came of it.]

**[Project Title 9]**
*Tech stack: [Tech item] · [Tech item] · [Tech item]*
[What the project is and what came of it.]

**[Project Title 10]**
*Tech stack: [Tech item] · [Tech item] · [Tech item]*
[What the project is and what came of it.]

**[Project Title 11]**
*Tech stack: [Tech item] · [Tech item] · [Tech item]*
[What the project is and what came of it.]

**[Project Title 12]**
*Tech stack: [Tech item] · [Tech item] · [Tech item]*
[What the project is and what came of it.]

**[Project Title 13]**
*Tech stack: [Tech item] · [Tech item] · [Tech item]*
[What the project is and what came of it.]

**[Project Title 14]**
*Tech stack: [Tech item] · [Tech item] · [Tech item]*
[What the project is and what came of it.]

**[Project Title 15]**
*Tech stack: [Tech item] · [Tech item] · [Tech item]*
[What the project is and what came of it.]

**[Project Title 16]**
*Tech stack: [Tech item] · [Tech item] · [Tech item]*
[What the project is and what came of it.]

**[Project Title 17]**
*Tech stack: [Tech item] · [Tech item] · [Tech item]*
[What the project is and what came of it.]

**[Project Title 18]**
*Tech stack: [Tech item] · [Tech item] · [Tech item]*
[What the project is and what came of it.]

**Also built:** [a cut project], [a second cut project], and [a third cut project]. More at [your-portfolio.example.com](https://your-portfolio.example.com).

---

## Other Relevant Information
<!-- Closes the CV. The references bullet is MANDATORY and always leads the section;
     select 2-4 of the optional bullets. Referee names and contact details are never
     printed. -->

- Recommendation letter from [Reference Name, Title at Organization], available on request; additional references on request.
- International exposure: [travel, training courses, or time living abroad - keep only what adds signal].
- Award: [what it was for and what came of it].
- Volunteering: [community involvement, scope, and years].
- Certification: [qualification relevant to the posting].
- Writing: [blogs, publications, or documentation you maintain].
- Personal interest in [domain relevant to the posting]: [what you actually do with it] (surface only for adjacent roles).
- Personal maker practice: [building, prototyping, or craft] for iterative problem-solving.
