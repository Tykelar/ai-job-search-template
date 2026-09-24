---
framework_version: 1.3.0
---

# Job Evaluation Framework

<!-- SETUP: Skill match areas and career goals are personalized by running /setup -->

## The four hard gates: mechanism here, values in `config/gates.md`

This file defines **how** to read a posting and classify it against each gate. It states
**no** thresholds, country lists, or language levels of its own: every value the four gates
below compare against lives in `config/gates.md`, the single source of truth. Never copy a
value out of that file into this one, and never hardcode one in a command.

**The gates execute once per posting, in `/rank` Step 2a**, in the order eligibility →
language → experience → location, on the fetched posting text, before any dimension is
scored. `/scrape` runs none of them (it collects postings and applies collection-stage
filters); `/apply` re-runs none of them (a job it builds was gated in `/rank`, and a cold
posting handed straight to it is reported as ungated at its Step 1c gate). A gate defined
here but executed nowhere is a silent PASS, and a gate executed twice is redundancy - the
single execution point is what keeps both from happening.

A `FAIL` on any gate is a hard stop: **do not score, do not draft.** Quote the exact
requirement line back to the user. A `FLAG` is not a fail - it proceeds, visibly, and the
human is the tiebreaker.

## Eligibility Gate — run before scoring

Reads the **work authorization** block of `config/gates.md` (Gate 1): the candidate's
citizenship and the countries it covers, any permit-timing constraint, and which countries
would require sponsorship. It is a hard filter, not a scoring dimension, and it is separate
from work-permit *timing*: timing asks "can they work the required hours yet?", eligibility
asks "are they permitted to hold this job at all?". A candidate can pass timing and still be
categorically excluded.

Read the posting's eligibility / work rights / "who can apply" section **verbatim** and classify:

| Posting wording | Verdict |
|-----------------|---------|
| Names a **citizenship or permanent-residency requirement** ("must be a citizen of X", "permanent resident", "PR required", "full working rights" where the employer means citizen/PR) | **FAIL — hard stop.** Do not score, do not draft. Quote the exact wording back to the user. |
| Requires a **security clearance** at any level | **FAIL** in most countries, since clearance is normally gated on citizenship. Verify the specific scheme rather than assuming. |
| **Explicitly names** the candidate's permit class, or says "international applicants welcome", "visa holders considered", "we sponsor" | **PASS** — verified acceptance. Worth noting as a positive in the application. |
| **Silent** on citizenship or residency | **PROCEED, but mark unverified.** Check the employer's own careers or international-applicant page before drafting. |

**Two rules that are easy to get wrong:**

1. **Silence is not permission.** Large graduate programs frequently gate eligibility on their own website rather than in the job ad. Highest-risk categories: professional-services firms, government and defence, banking, telecommunications, and anything touching critical infrastructure.
2. **A company-wide "we accept international applicants" statement is not role-level permission.** The common pattern is a general welcome followed by a *named list* of the specific programs or service lines it covers. Confirm the **specific posting or stream** appears on that list before drafting.

**Report an eligibility failure to the user with the quoted source** rather than silently dropping the role. They may know something about their own status that the profile does not record.

If the candidate's permit also constrains *hours* or *start date* (a student visa with a term-time cap, a permit that begins on graduation), record that as a second gate under this section during `/setup`, with the specific dates. Do not merge it with the eligibility question above — they fail for different reasons and need different answers.

A role that fails this gate is not scored and not drafted. Everything below applies only to roles that pass it.

## Language Gate — run before scoring

Checks a posting's stated language requirements against what the candidate actually speaks. It is a hard filter, not one of the Scoring Dimensions below, and it is structured the same way as the Eligibility Gate above: read the posting, classify against the declared table, and treat a hard mismatch as FAIL before scoring. `/rank` runs it in Step 2a and persists its result on the ranked entry (`language_gate`, plus `language_note` when it FLAGs), so the verdict outlives the run that produced it.

Two different language checks exist in this pipeline and they are not the same thing. **This gate** reads what the *role* requires of the person; `/scrape`'s collection-stage Language Filter reads what *language the ad is written in* and drops the posting before anything is scored. A posting written in a language you don't work in, for a role that only needs languages you do work in on the job, passes this gate fine.

Read the posting's language requirements as stated for **the role itself** — not the language the ad happens to be written in. Only an explicit job-condition requirement ("fluent X required," "must communicate with the Y team in Z") triggers this check. For each language the posting requires as a job condition, compare it against the declared **Languages table in `config/gates.md`** (Gate 2) — the single source of truth for which languages are declared and at what level:

| Posting requirement vs. the declared Languages table | Verdict |
|---|---|
| Requires a language **not on the declared table at all** (e.g. "fluent Polish required," "must communicate with the Warsaw team in Russian," and you list no Polish/Russian row) | **FAIL — hard stop.** Do not score, do not draft. Quote the exact requirement line. |
| Requires a language the table **does** list, but the posting's stated bar (as written — "fluent," "native," "C1+," "business-level") reads as plausibly **higher** than your declared level | **FLAG, then proceed.** Not a fail. Score and draft normally, but surface the gap explicitly in your report to the user (quote both the posting's requirement and your declared level) so they can judge it themselves — bars like "fluent" vary a lot by company and geography, and a recruiter may be flexible. Never silently drop the posting and never silently treat it as a clean pass. |
| Requires a language the table lists, at or below the declared level (or the posting doesn't specify a level at all — just names the language) | **PASS.** No note needed. |

Judge the level comparison the same way you judge everything else in this framework: read both sides as written and reason about it, don't force either into a rigid scale — CEFR letters, LinkedIn-style buckets ("professional working proficiency"), and plain-English words ("conversational," "fluent," "native") all appear in the wild and don't map onto each other precisely. When genuinely unsure whether a stated bar exceeds the candidate's level, prefer FLAG over a silent PASS — the human is meant to be the tiebreaker, not the gate.

**Worked example** (illustrative levels, not this candidate's): a table listing Spanish (Native) and English (B1/B2). A posting requiring "fluent Russian" → **FAIL**, Russian isn't declared at all. A posting requiring "fluent English" → **FLAG**, English is declared but "fluent" plausibly exceeds B1/B2 — score and draft the application, but tell the candidate this posting's bar may be a stretch and let them decide. A posting requiring "conversational English" or unspecified English → **PASS**, B1/B2 clears a "conversational" bar cleanly.

## Experience Gate — run before scoring

The ceiling itself is **not** set here - it is a single configurable value in `config/gates.md` (Gate 3). This section only defines the mechanism, so the number changes in one place without touching this logic. Distinct from the **Experience Match** scoring dimension below: this gate is a hard pass/fail on the posting's *stated minimum requirement*, independent of how well the candidate's actual background matches the role - a posting can pass this gate and still score low on Experience Match, or vice versa.

Read the posting's stated experience requirement **as written**, and identify the **minimum required** years for the role being evaluated - not a "nice to have," not an aspirational range's upper bound, and not a figure that belongs to a different seniority tier the same posting also lists (e.g., a posting with separate Junior/Mid tracks: gate only the track actually being evaluated).

| Posting's stated minimum required experience vs. the configured ceiling | Verdict |
|---|---|
| At or above the ceiling, stated as a requirement (e.g. ceiling = 3: "3+ years", "minimum 3 years", "3-5 years") | **FAIL — hard stop.** Do not score, do not draft. Quote the exact requirement line. |
| Below the ceiling (e.g. ceiling = 3: "1-2 years", "2+ years") | **PASS.** |
| Mentioned only as "preferred," "a plus," "nice to have," or not stated as a hard requirement at all | **PASS.** Never infer a requirement the posting doesn't actually state as required. |

**Worked example** (ceiling = 3): a posting requiring "3+ years of relevant experience" → **FAIL**. A posting requiring "2-4 years" → **PASS** - the *stated minimum* is 2, below the ceiling, even though the range's upper bound exceeds it; the posting does not require 3+. A posting saying "3+ years preferred, but we'll consider strong junior candidates" → **PASS**, since the hard requirement is waived - note the stretch under Gaps instead. A posting silent on years of experience → **PASS**.

When the requirement is genuinely ambiguous (e.g., a vague "experienced professional" with no number), don't guess a number - treat it as silent and **PASS**, then let the Experience Match dimension below do the qualitative judgment.

## Scoring Dimensions

Evaluate each posting that cleared all four gates against the dimensions below: **four scored dimensions** (1, 2, 3, 5) that carry the weights, **one pass/fail gate** (4, Location - the fourth hard gate, listed here because it is where the location rules are read), and **one optional benchmark** (6, Salary - unweighted, skipped when the lookup tool is not configured).

### 1. Technical Skills Match (0-100)
How well do the required/preferred skills align with the candidate's capabilities?

| Score | Meaning |
|-------|---------|
| 80-100 | Core requirements are primary skills |
| 60-79 | Most requirements match, 1-2 gaps that are learnable |
| 40-59 | Partial match, significant upskilling needed |
| 0-39 | Fundamental mismatch |

**Strong match areas:** [YOUR_PRIMARY_SKILLS]

**Moderate match areas:** [YOUR_SECONDARY_SKILLS]

**Weak match areas:** [SKILLS_YOU_LACK]

### 2. Experience Match (0-100)
Does work history align with what they're looking for?

| Score | Meaning |
|-------|---------|
| 80-100 | Direct experience in the same domain and role type |
| 60-79 | Related experience, transferable skills clear |
| 40-59 | Adjacent experience, would need to make the case |
| 0-39 | Unrelated experience |

**Strong:** [YOUR_DIRECT_EXPERIENCE_DOMAINS]

**Moderate:** [YOUR_ADJACENT_EXPERIENCE]

**Entry-level:** [ROLES_WITH_LIMITED_EXPERIENCE]

### 3. Behavioral/Culture Fit (0-100)
Does the role and company culture match the behavioral profile?

| Score | Meaning |
|-------|---------|
| 80-100 | Culture strongly matches behavioral preferences |
| 60-79 | Mixed signals but mostly compatible |
| 40-59 | Some friction areas |
| 0-39 | Significant culture mismatch |

**Red flags to research:** Department disorganization, work dominated by maintenance over development, poor chemistry with leadership, culture mismatches. Check reviews, media coverage, LinkedIn connections, and network contacts for insider perspective.

### 4. Location & Logistics (Pass/Fail + Notes)

This is the fourth hard gate, not a weighted dimension, and it reads the **authorized
countries** block of `config/gates.md` (Gate 4) - base location, commutable cities, the
authorized-relocation list, and the remote scope. Relocation is **not** categorically a
deal-breaker: whether it fails depends entirely on whether the posting's country is on that
list.

- Commutable from the configured base: PASS
- Remote within the configured remote scope: PASS
- On-site or hybrid in a country on the authorized-relocation list: PASS
- On-site or hybrid in a country **not** on that list and not commutable: FAIL (deal-breaker)
- Frequent international travel: FLAG (discuss with user)

### 5. Career Alignment & Motivation (0-100)
Does this role advance career goals and contain tasks that energize?

| Score | Meaning |
|-------|---------|
| 80-100 | Strongly aligned with career direction, clear growth path |
| 60-79 | Good role but only partially aligned with long-term goals |
| 40-59 | Decent job but doesn't build toward career goals |
| 0-39 | Dead end or backwards step |

**Career goals:**
- [YOUR_CAREER_GOAL_1]
- [YOUR_CAREER_GOAL_2]
- [YOUR_CAREER_GOAL_3]

**Motivation filter:** Evaluate not just whether you *can* do the tasks, but whether the tasks will *energize* you. Consider:
- Tasks that energize: [YOUR_ENERGIZING_TASKS]
- Tasks that drain: [YOUR_DRAINING_TASKS]
- Non-task factors: leadership style, department culture, company values, degree of autonomy

**Life situation alignment:** Consider personal constraints:
- **Security**: [YOUR_FINANCIAL_SITUATION_CONTEXT]
- **Flexibility**: [YOUR_SCHEDULE_CONSTRAINTS]
- **Professional development**: [YOUR_GROWTH_PRIORITIES]

### 6. Salary Benchmark (Optional)

If the salary lookup tool is configured (`salary_data.json` exists), look up the company:
```
python salary_lookup.py "<Company Name>" --json
```

If a city is known from the posting, add `--city "<City>"` to narrow results.

Present findings as:
```
### Salary Benchmark
| Metric | Value |
|--------|-------|
| [Category] index | XX.X (+/-X.X% vs baseline) |
| Overall index | XX.X (+/-X.X% vs baseline) |
```

Interpret results relative to the baseline defined in the data file's metadata. For index-based data, higher typically means above-market compensation.

If the salary tool is not configured, skip this section.

## Output Format

Present the evaluation as:

```
## Job Fit Evaluation: [Role] at [Company]

| Dimension | Score | Notes |
|-----------|-------|-------|
| Technical Skills | XX/100 | [brief note] |
| Experience Match | XX/100 | [brief note] |
| Behavioral Fit | XX/100 | [brief note] |
| Location | PASS/FAIL | [brief note] |
| Career Alignment | XX/100 | [brief note] |

**Overall Score: XX/100** (weighted average of scored dimensions)

### Verdict: [Strong Fit / Good Fit / Moderate Fit / Weak Fit / Poor Fit]

### Key Strengths for This Role
- [bullet points]

### Gaps to Address
- [bullet points]

### Recommendation
[1-2 sentences: apply/skip/apply with caveats]

### Company Research Checklist
- [ ] Checked company website (mission, values, recent news)
- [ ] Checked review sites (Glassdoor, Jobindex, etc.)
- [ ] Checked LinkedIn for team size, recent hires, connections
- [ ] Checked media for restructuring, growth, or workplace issues
- [ ] Identified network contacts who may know the team/manager
```

## Weighting
- Technical Skills: 30%
- Experience Match: 25%
- Behavioral Fit: 15%
- Career Alignment: 30%

(Location is pass/fail, not weighted)

## Thresholds
- **Strong Fit** (75+): Definitely apply, tailor everything
- **Good Fit** (60-74): Apply, address gaps in cover letter
- **Moderate Fit** (45-59): Consider carefully, discuss with user
- **Weak Fit** (30-44): Probably skip unless strategic reasons
- **Poor Fit** (<30): Skip

## Pre-Application: Call the Employer (Best Practice)

Before writing the application, consider whether the candidate should call the contact person listed in the posting. **Only call if there are substantive questions** - never call just to "be remembered."

### When to Suggest Calling
- The posting has unclear or ambiguous requirements
- It's unclear which competencies are essential vs. nice-to-have
- The role description is vague about day-to-day tasks
- There's a named contact person who invites questions

### Good Questions to Ask
- "What are the primary challenges in this role?"
- "How is time typically divided across the listed responsibilities?"
- "Which competencies are most critical for success in this position?"
- "What does success look like in the first 6-12 months?"

### Rules for the Call
- Prepare a 30-second "elevator pitch" about your background in case they ask
- The call's purpose is **gathering information**, not delivering a pitch
- Take notes - use what you learn to tailor the application
- Reference the conversation naturally in the cover letter ("After speaking with [name], I was especially drawn to...")
