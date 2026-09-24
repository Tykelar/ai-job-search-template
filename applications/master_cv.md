<!--
  CURATED MASTER CV CONTENT BANK — the Markdown twin of applications/main_example.tex.

  WHAT THIS FILE IS
  A WORKING EXAMPLE of a filled master bank, not just a blank form:

  1. [Bracketed] fields are PLACEHOLDERS for /setup (or you) to replace:
     name, contact line, employers, institutions, dates, links, referees,
     languages. Nothing personal is committed here.

  2. The bullet, competency, skill, and project content is EXAMPLE CONTENT
     based on a real filled master CV. It shows the expected style,
     specificity, metrics, and density - what "well written" looks like.
     Replace it with your own facts, keeping the shape. Never send example
     claims as your own; the examples are scaffolding, not your history.

  Delete any block that does not apply to you.

  PROVENANCE
  - This file and applications/main_example.tex are the same content: the full
    master bank, rendered once in Markdown and once in the compact LaTeX style.
    They must stay line-for-line identical (modulo LaTeX escaping). If they
    diverge, fix both together; if you maintain a source corpus, fix the source
    and regenerate. Do not hand-edit one twin only.

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
-->

# [YOUR_NAME]

<!-- Professional headline variants, role-tailoring map, and keyword banks, if you
     keep them, live here. /apply selects a headline or framing; it never invents one. -->

---

## About Me
<!-- EXAMPLE. Voice/quality baseline for the generative About Me paragraph. Adapt
     per role; never paste verbatim into a tailored CV. Ends with the portfolio
     sentence - delete it if you have no portfolio. -->

Computer Engineering MSc and Software Engineer who re-engineers delivery infrastructure, improves engineering velocity, and integrates AI into engineering workflows. In my most recent role I led a Lean-driven re-engineering of the delivery pipeline, from diagnosing accumulated technical debt through to measurable gains in delivery speed and reliability, formalized in a master's thesis on Lean CI/CD and AI-ready infrastructure. Alongside this I founded and ran a cooperative through its full operational lifecycle, and bring a systems-level perspective spanning applied AI, immersive technologies, and cybersecurity. Get to know me better [here](https://your-portfolio.example.com)!

---

## Education
<!-- PLACEHOLDERS for degree, institution, and dates. Keep the one-line-per-degree
     shape and the thesis/final-project sub-line. Full project write-ups belong in
     Selected Projects. -->

| Degree | Period | Institution | Key Topics |
|--------|--------|-------------|------------|
| [Primary Degree] | Sep 20XX - Jul 20XX | [Institution] | Thesis: "[Thesis title]" ([grade]) |
| [Second Degree] | Sep 20XX - Jul 20XX | [Institution] | Final project: [Final-project title] ([grade]) |
| [Optional Earlier Degree or Transfer] | Sep 20XX - Jul 20XX | [Institution] | [Key topics] |

---

## Work Experience
<!-- PLACEHOLDERS for job title, company, and dates; the bullets are EXAMPLES
     showing the expected style - action verb first, concrete tool or method,
     measured outcome. On a tailored CV: 5-6 bullets from the most recent role,
     3-4 from the second, 2-3 from earlier roles. -->

### [Most Recent Job Title], [Company] | Mon 20XX - Mon 20XX
[One-line company or product context - what the company does, for whom, and at what scale.]
- Built AI agent skills deployed in internal engineering repositories, enabling automated assistance for complex engineering and process workflows.
- Led a Lean-driven re-engineering of delivery infrastructure and processes, resolving accumulated technical debt and cutting total pipeline job time by more than 50%.
- Redesigned delivery and engineering workflows, contributing to up to 20% more features deployed per sprint.
- Restructured task distribution and handovers, reducing time consumption by around 30% and eliminating duplicated work.
- Contributed to the architecture and testing of an embedded AI chatbot that helps users navigate the platform.
- Contributed to the architecture and testing of a RAG system letting users query their own uploaded documents.
- Drove integration of AI agents and services into product and engineering workflows.
- Collaborated on an in-house image-recognition application built on object detection: labeled and curated the training dataset, helped define detection classes, and ran and evaluated training and optimization tests.
- Designed and implemented a test framework in Playwright, including reusable helpers and utilities for scalable coverage.
- Integrated the automated test battery into GitLab CI pipeline jobs, enabling fully automated execution as part of the workflow.
- Led the Cypress to Playwright migration, including trade-off evaluation, implementation, and documentation.
- Standardized test naming and data conventions and introduced seed-driven data setup to reduce coupling and instability.
- Scripted reproducible local and virtual test environments (seed, rebuild, reinitialize services) in Shell/Bash to improve developer experience.
- Maintained and extended an existing automated test battery; analyzed reports and failure patterns to prioritize fixes.

### [Previous Job Title], [Company] | Mon 20XX - Mon 20XX
[One-line company or initiative context.]
- Founded a non-profit cooperative: legal incorporation, administrative setup, governance structure, and ongoing compliance.
- Owned the full entrepreneurial process from idea to operational execution with no prior institutional support.
- Coordinated partnerships with public and private institutions to fund and support community programmes.
- Led educational activities, community workshops, and public-space renovation initiatives.
- Organized and monitored internal procedures for consistent operational execution.
- Managed the full physical setup and operational launch of a café/restaurant space and a nursing-school space.

### [Earlier Job Title], [Company] | Mon 20XX - Mon 20XX
- Organized inventory, materials, and warehouse and storage flows.
- Optimized storage and transport procedures, improving handling and distribution time by up to 20%.
- Supported the full logistics cycle (picking, dispatch, transport, retrieval); drove forklift for load handling.
- Performed technical assembly support, including ventilation conduit assembly.

### [Earliest Job Title], [Company], [Country] | Mon 20XX - Mon 20XX
- Built Excel databases from publicly available company information for business outreach.
- Conducted company and individual outreach for partnership opportunities.
- Produced documentation linking travel agencies and hospitality brands.

---

## Languages
<!-- PLACEHOLDERS - one line. Values must match the Languages table in config/gates.md. -->

[Language]: [Level] · [Language]: [Level] · [Language]: [Level] · [Language]: [Level]

---

## Skills
<!-- EXAMPLES - the source pool Core Competencies is composed from. A tailored CV
     DELETES this whole section; it is never printed alongside Core Competencies.
     Replace the items with your own; keep the category · item · item shape. -->

- **Process, Operations & Continuous Improvement:** Process analysis and mapping · Workflow re-engineering · Operational efficiency · Waste identification and prioritization · Procedure standardization · Task ownership and handover design · KPI design and tracking · Lean Software Development · Technical debt diagnosis and remediation · Continuous improvement (PDCA / Kaizen) · Process automation (RPA, UiPath) · Structured business-case analysis
- **QA, Testing & Reliability:** Software QA (manual and automated) · End-to-end test framework design (Playwright) · Reusable test helpers and utilities · Cypress maintenance and extension · API integration testing · Component-level unit testing · Test pyramid design and coverage rebalancing · Flaky test mitigation · Seed-driven test data · Failure-pattern and log analysis · Shift-left quality · Eval and benchmark harness design (golden sets, controlled A/B)
- **CI/CD, DevOps & Delivery:** CI/CD foundations and practical application · Pipeline optimization and feedback-loop reduction · Build and test resource efficiency · CI job integration for test batteries · Test parallelization · Workflow governance · Local environment automation scripting · Environment reproducibility · Containerization and deployment (Docker, Docker Compose) · Tooling and migration assessment
- **Applied AI & Machine Learning:** CNNs and image classification · YOLO object detection · RNNs and sequence prediction · Transfer Learning · Hyperparameter optimization (Optuna) · LLM integration and AI agents · RAG system design, testing and evaluation (recall@k benchmarking) · Vector databases (Chroma) · LangChain · Chatbot and embedded AI chat · Local LLM deployment (Ollama, Gemma, Qwen) · Prompt engineering · Deep-learning training practice (dropout, batch normalization, augmentation, early stopping, class imbalance) · LLM guardrails and grounding enforcement · Agent harness engineering · Tool and function-calling design · Claude Code extensibility (hooks, slash commands, skills, subagents) · Multi-agent orchestration · AI system design · LLM observability and production monitoring
- **Cybersecurity & Defensive Engineering:** Offensive security · OSINT and footprinting · Vulnerability assessment and reporting · SIEM implementation and log centralization · Threat detection and alerting · Host-based intrusion detection (HIDS) · File integrity monitoring · Wazuh and Elastic Stack (ELK) · Data privacy and PII redaction pipeline design · Penetration testing methodology · Wireless network assessment and MITM · Social engineering and authorized phishing simulation · Web application attack techniques · Detection rule authoring and alert tuning (Wazuh) · Data-layer authorization (PostgreSQL Row-Level Security)
- **Immersive Tech, 3D & Visualization:** Virtual and Augmented Reality · Digital Twins · 3D modelling and printing · VTK 2D/3D/VR visualization · Unity (C#) · Godot · Blender · VRChat SDK · Additive manufacturing and rapid prototyping
- **Data, Analysis & Reporting:** Excel database creation and maintenance · Data structuring and reporting · SQL data handling · SPSS statistics · KPI and operational metric tracking · Analytical reasoning
- **Engineering Foundations:** Physics and Mathematics (classical and quantum mechanics) · Scientific computing and simulation (MATLAB) · Engineering drawings · Systems and computer hardware architecture · Elementary electrical circuits
- **Programming Languages:** Python · TypeScript · JavaScript · Java · C# (Unity) · React Native · SQL Server / SQL · MATLAB · Shell / Bash · Assembly · C · Full-stack web architecture
- **Tools & Platforms:** Playwright · Cypress · GitLab CI · Bash / Shell · Git · MS Project · Excel · SQL · SPSS · Unity · Godot · Blender · VRChat SDK · VTK · Ollama (Gemma, Qwen) · LangChain · ChromaDB · OpenClaw · Docker / Docker Compose · Cloudflare Tunnel · UiPath · Wazuh · Elastic Stack (ELK) · Microsoft 365 · Claude Code · Supabase · PostgreSQL · Drizzle ORM · Zod · pnpm workspaces · Vite · Vercel · Cloudflare R2 · Nmap · Wireshark · Metasploit · Aircrack-ng · Burp Suite · Postfix · Slack webhooks
- **Soft Skills:** Initiative and autonomy · Problem-solving (root-cause-first) · Fast learning and resilience · Leadership and team dynamics · Communication with technical and non-technical stakeholders · Adaptability

---

## Selected Projects
<!-- EXAMPLES - always include; select 4-6 per role in tailored CVs, then close
     with the mandatory "Also built:" line naming what was cut. Keep the three-line
     shape: title, one-line tech stack, then what it is and what came of it. -->

**Lean-Driven QA & CI/CD Re-Engineering Towards AI-Ready Infrastructures (Master's Thesis)**
*Tech stack: CI/CD architecture · QA architecture · Test-suite optimization · Research*
Research into engineering infrastructures that stay scalable, understandable, and ready for AI integration: CI/CD architecture, QA integration, shift-left quality, flakiness dynamics, and toolchain-migration criteria.

**Big Data Analysis & Representation: NO2 Air Pollution in VR (Bachelor's Final Project)**
*Tech stack: OpenXR · VTK · Unity · 3D*
A VR system for visualizing large-scale NO2 air-pollution data across an urban area, with a user study comparing VR and desktop interaction.

**Niche-Field SaaS Marketing & Admin Platform**
*Tech stack: TypeScript · React · Express · PostgreSQL · Drizzle · Zod · Playwright · Vercel*
A multi-tenant SaaS platform helping businesses in a niche field market themselves and manage the information central to their operations. Built solo end to end: architecture, data model, API, UI, auth, testing, and deploy.

**Shared Expense Tracker (Serverless PWA)**
*Tech stack: TypeScript · React · Supabase · PostgreSQL (RLS) · Google OAuth · Workbox*
A private, installable expense-tracking PWA for two people, deliberately built with no backend to maintain, with authorization enforced in the database rather than in the client. Delivered solo end to end.

**Production RAG Chatbot**
*Tech stack: Python · LangChain · ChromaDB · Ollama · Docker Compose · Cloudflare Tunnel*
A publicly deployed chatbot answering visitor questions over a structured personal knowledge corpus. Every retrieval change is gated by a golden evaluation set; controlled A/B testing exposed a silent embedding-tokenizer defect degrading every measurement, and fixing it raised recall@5 from 56% to 70%. Ships behind an audience-filtering and PII-redaction safety gate.

**Support Ticket Auto-Reply: Guardrailed Agentic Pipeline**
*Tech stack: Python · FastAPI · Pydantic · SQLite · pytest · Docker Compose · Ollama*
A service that answers support tickets automatically, or hands them to a human when it cannot answer safely. A bounded agentic tool-calling loop drafts replies grounded only in tool results, a post-hoc check verifies every number and identifier against those results, and every failure closes to a handoff with a full decision trace. Built test-first: 500+ automated tests and 15 ADRs.

**From-Scratch Local RAG Pipeline**
*Tech stack: Python · Ollama · nomic-embed-text · numpy*
A framework-free local RAG pipeline built to turn RAG theory into hands-on implementation. Built a recall@k evaluation harness, then caught the evaluation itself being too permissive: tightening the ground truth dropped apparent recall@1 from 71% to 14%, turning retrieval depth from an assumption into a measured choice.

**Structured Personal Knowledge Corpus**
*Tech stack: Python · YAML · Markdown*
A single-source-of-truth corpus holding identity, skills, projects, and experience as tagged Markdown blocks, ending the drift of maintaining the same facts across a CV, a portfolio site, and an assistant's context. Schema-level audience gating keeps each export to what is appropriate.

**Agent-Driven Application Pipeline**
*Tech stack: Python · LaTeX · TypeScript · Bun · Claude Code · Git*
An agent pipeline that turns a job posting into a fit evaluation, a tailored CV, and a cover letter, with a reviewer agent critiquing each draft. Its CV system tailors by verbatim selection from a verified master bank, making invented claims structurally impossible, and its profile syncs from the structured corpus above.

**SIEM Implementation: Security Monitoring & Detection**
*Tech stack: Wazuh · Elasticsearch · Kibana · HIDS · FIM*
Designed and deployed a working SIEM centralizing log collection, with detection rules, alerting, file integrity monitoring, and host-based intrusion detection, validated against simulated attacks.

**Cybersecurity Assessment & Footprinting (Client Project)**
*Tech stack: OSINT · Offensive security · Vulnerability assessment*
External attack-surface mapping for a small cooperative; delivered a prioritized vulnerability and remediation report and presented it to the client.

**Digital Twin & Animal Tracking App**
*Tech stack: Kotlin · React Native · Firebase · A-Frame*
A mobile system keeping a live digital twin of tracked animals across large-scale environments, with two-way communication and an AR layer mapping positions in real space.

**1:1 Architectural VR Walkthrough (Client Project)**
*Tech stack: Unity · 3D modelling · Desktop + headset*
Accurate 1:1-scale 3D building models navigable on desktop and in VR, used by clients to plan interior decoration in a spatially accurate representation of their space.

**Mobile Client-Management App**
*Tech stack: React Native · Firebase*
A mobile app letting a cooperative access and manage client information on the go, delivered end to end.

**Sign Language Recognition: Image-to-Text (Academic)**
*Tech stack: Python · Computer vision · ML*
A computer-vision system reading sign-language gestures from images and converting them to text at 98% classification accuracy.

**CNN Match Classification (Academic)**
*Tech stack: Python · CNNs · Transfer Learning · EfficientNetB0 · Optuna*
A multiclass-multilabel CNN over 4,100 spatial heatmap images predicting match outcome, player role, and duration; compared single-input, per-output, Transfer Learning, and Optuna-optimized architectures. Separate per-task models exposed interference in the shared base, and two-phase EfficientNetB0 fine-tuning gave the best win/loss accuracy.

**Further Academic ML & Computing**
*Tech stack: Python · YOLO · RNNs · MATLAB · SPSS*
YOLO multi-class object detection at scale; RNN sequence prediction; MATLAB physics and mathematics simulations; SPSS statistical analysis across research cases.

**Game Design & Development and Maker Practice**
*Tech stack: Unity · Godot · Blender · VRChat SDK · FDM printing*
Independent multi-engine game development with published content, plus an ongoing home 3D modelling and printing practice for rapid prototyping.

**Also built:** a SIEM implementation (Wazuh + ELK), a client cybersecurity assessment, a digital twin with an AR layer, 1:1 architectural VR walkthroughs, academic ML (sign-language recognition, CNN/YOLO), and independent game development. More at [your-portfolio.example.com](https://your-portfolio.example.com).

---

## Other Relevant Information
<!-- EXAMPLES - closes the CV. The references bullet is MANDATORY and always leads
     the section; select 2-4 of the optional bullets. Referee names and contact
     details are never printed. -->

- Recommendation letter from [Reference Name, Title at Organization], available on request; additional references on request.
- International exposure: travel across 20+ countries, training courses in multiple countries, and six months living abroad (Erasmus+).
- Founded a student-run radio station using governmental funds for school improvement; sourced and set up the equipment.
- 18+ years of Scouting across national and international activities, including World Scout Jamboree participation.
- Recurring food-bank volunteer and further volunteer work across forest conservation and animal welfare; community ambassador roles.
- Personal maker practice: home-based 3D modelling and printing for rapid prototyping and iterative problem-solving.
- Writing: two personal blogs on personal growth/psychology and creative writing.
- Personal interest in financial markets and portfolio management: equities and options trading, margin accounts, and risk/position sizing via a live brokerage account (surface only for finance-adjacent roles).
