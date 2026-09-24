---
name: job-application-assistant
description: >
  Assists with job applications: evaluating job postings, tailoring CVs, writing cover letters,
  and preparing for interviews. Triggers on keywords like: job posting, job application, CV,
  cover letter, resume, interview prep, job fit, career, application, apply, ansøgning, stilling
allowed-tools: Read, Glob, Grep, WebFetch, WebSearch, Bash, Edit, Write, AskUserQuestion
framework_version: 1.4.0
---

# Job Application Assistant

---

## Workflow

**`/apply` is the canonical path for a complete application.** It owns the numbered
application folder, the `POSTING.md`, the shortlist validation gate, the reviewer pass, and
the mandatory PDF/ATS verification. Use the workflow below only for the **individual
requests** in *Quick Commands* - one CV, one cover letter, one evaluation, interview prep -
where the user explicitly wants a single artifact rather than an application. `/scrape` no
longer routes here: it collects postings, and drafting happens through `/rank` → `/apply`.

**This workflow runs no hard gates.** The four gates (eligibility, language, experience,
location) execute once per posting, in `/rank` Step 2a, against the values in
`config/gates.md`. Step 1 below scores fit; it does not veto.

When the user provides a job posting (URL or text), follow this workflow:

### Step 1: Research & Evaluate Fit
- Fetch the job posting content (use WebFetch for URLs). **A 403 is not a dead end** - follow the escalation order in `09-web-research.md` before concluding a page is unavailable, and prefer the employer's own careers posting over an aggregator listing
- Keep the **full posting text verbatim** for Step 3b to archive - never a summary
- Analyze the posting for required competencies, keywords, and priorities
- Research the company (website, LinkedIn, mission, recent news), per `09-web-research.md`
- Score the posting against the candidate's profile using the framework in `04-job-evaluation.md`
- Present the evaluation table and verdict
- Suggest whether the candidate should call the employer before applying (see `04-job-evaluation.md` for guidance)
- Ask the user if they want to proceed with an application

### Step 2: Tailor CV
- Read the most relevant existing CV variant from `applications/*/` as a starting point
- Follow the guidelines in `05-cv-templates.md`
- Create `applications/<NN>_<company>_<role>/CV_<CVNameSlug>_<company>_<role>.tex` with tailored
  content. **The folder naming is not optional:** `<NN>` is the next two-digit sequence number in
  creation order (highest existing prefix + 1, `INTERVIEW_` flags stripped when reading them) and
  `<CVNameSlug>` is the `CV filename slug:` line from CLAUDE.md's Identity section - the same
  rules `/apply` Step 1b applies, stated in CLAUDE.md's Repo Structure as hard rules
- Adjust: profile statement, skills section, experience bullet emphasis, section order
- **Compile and verify before presenting**, per `/apply` Step 5: lualatex for the CV, exactly two
  pages, at least four `\cvproject` entries, no orphaned headers, and the ATS text-layer check.
  A `.tex` that was never compiled is not a finished CV

### Step 3: Write Cover Letter
- Follow the writing style rules in `03-writing-style.md` (critical: no em-dashes, no cliches)
- Follow the template structure in `06-cover-letter-templates.md`
- Create `applications/<NN>_<company>_<role>/CL_<CVNameSlug>_<company>_<role>.tex`, in the folder
  Step 2 created and under the same naming rules
- Ensure the letter connects specific experience to the role requirements
- **Compile with xelatex and verify** it is exactly one page with the signature block intact, per
  `/apply` Step 5

### Step 3b: Record the Application
- Run this once both documents exist. A CV or cover letter drafted alone is not yet an application.
- Follow **`/apply` Step 6b** (`.claude/commands/apply.md`) exactly: same header, same match-then-update rule, same `drafted` row, same posting archive, same prohibition on touching `job_scraper/seen_jobs.json`. It is stated there once so the two paths cannot drift. Three of its values are named in `/apply`'s own terms: `cv_file`/`cover_letter_file` are the paths written in Steps 2 and 3 here, `source` is the posting URL from Step 1, and the posting text item 7 archives is the one Step 1 read.
- This step exists for the direct-request path (a user who asked for both documents in conversation). Without it, that path writes two documents and records nothing. When a full application is what the user wants, prefer `/apply`, which does this and the verification automatically.

### Step 4: Interview Preparation
- Follow the framework in `07-interview-prep.md`
- Prepare STAR-format answers for likely questions
- Identify role-specific talking points
- Draft questions the candidate should ask the interviewer

---

## Reference Files

| File | Purpose |
|------|---------|
| `01-candidate-profile.md` | Education, experience, skills, publications, awards |
| `02-behavioral-profile.md` | Behavioral assessment, strengths, ideal environments |
| `03-writing-style.md` | Tone, structure, do's and don'ts |
| `04-job-evaluation.md` | Scoring framework for job fit |
| `05-cv-templates.md` | LaTeX CV structure and tailoring rules |
| `06-cover-letter-templates.md` | LaTeX cover letter structure and tailoring rules |
| `07-interview-prep.md` | STAR examples, tough questions, roleplay guidelines |
| `09-web-research.md` | Fetching postings and company pages: trust boundary, the WebFetch 403 fallback, escalation order, claim verification |

---

## Quick Commands

The user may also ask for individual steps without the full workflow:
- "Evaluate this job posting" - Step 1 only
- "Write a CV for [company]" - Step 2 only
- "Write a cover letter for [role] at [company]" - Step 3 only
- "Help me prepare for an interview at [company]" - Step 4 only
- "What jobs should I look for?" - Career strategy discussion using profile + evaluation framework
