# Hard Gates - User Configuration

**This file is the single source of truth for every hard gate in the job-search
pipeline.** No other file states these values. The framework files
(`.claude/skills/job-application-assistant/04-job-evaluation.md`) define the gate
*mechanisms* - how to read a posting and classify it - and read every threshold,
list, and level from here.

**Executed once, in `/rank`.** `/rank` Step 1.6 reads this file and forwards these
values verbatim into every scoring agent's prompt; Step 2a runs the gates on the
fetched posting before any scoring. `/scrape` runs no gates (it collects postings),
and `/apply` re-runs none (a job it builds has already been gated). See *Where the
gates run* below.

**Editing.** Change a value here and every consumer picks it up on the next run;
never copy a value out of this file into a skill, a command, or CLAUDE.md. Candidate
facts originate in your profile files under
`.claude/skills/job-application-assistant/` - update those first, then this file.
The one exception is the work-authorization line in Gate 1, which no profile file
records.

**This file ships unfilled.** `/setup` writes all four blocks on every path, and
`/rank` refuses to run while any block below still holds a `[PLACEHOLDER]`.

---

## Gate 1: Eligibility (work authorization)

Runs first. Asks whether the candidate is *permitted to hold the job at all* -
separate from whether a permit's timing works out.

| Field | Value |
|---|---|
| Citizenship / work authorization | [YOUR_CITIZENSHIP_AND_WORK_AUTHORIZATION] |
| Permit timing constraints | [NONE_OR_DESCRIBE] |
| Countries requiring sponsorship or a visa | [COUNTRIES_WHERE_YOU_WOULD_NEED_SPONSORSHIP] |

**Verdicts.** A posting demanding citizenship or permanent residency of a country
outside the authorization above, or a security clearance, is a **FAIL**. A posting in
a sponsorship-required country is a **FAIL** unless it states that it sponsors. A
posting silent on work rights inside the authorized region is a **PASS**.

> This is the one gate input no profile file records. Ask the user directly during
> `/setup` rather than inferring it from their CV.

## Gate 2: Languages

The declared table the Language Gate compares a posting's **job-condition** language
requirements against (not the language the ad happens to be written in).

| Language | Declared level |
|---|---|
| [LANGUAGE_1] | [LEVEL_1] |
| [LANGUAGE_2] | [LEVEL_2] |

**Verdicts.** A language required as a job condition that is **absent from this
table** is a **FAIL**. A language **on** this table whose stated bar reads higher
than the declared level is a **FLAG** for the candidate to judge, never a fail. At or
below the declared level, or a language named with no level, is a **PASS**.

This same table is the source for `/scrape`'s collection-stage language filter, which
drops postings whose **body** is written in a language outside it. That filter is not
a gate: it never scores, never vetoes, and carries no `skip_note`.

## Gate 3: Experience ceiling

| Field | Value |
|---|---|
| Ceiling (years) | **[N]** |

**Verdicts.** A posting whose **stated minimum required** experience is at or above
the ceiling is a **FAIL**. Below it, silent on it, or naming it only as
preferred/nice-to-have is a **PASS**. Never infer a requirement the posting does not
state.

Raise or lower the search's seniority band by changing that one number. It is
independent of the Experience Match scoring dimension, which judges how well the
actual background fits.

## Gate 4: Authorized countries (location)

| Field | Value |
|---|---|
| Base location | [YOUR_CITY, YOUR_COUNTRY] |
| Commutable from base | [COMMUTABLE_CITIES] |
| Authorized for relocation | **[RELOCATION_COUNTRIES]** |
| Remote scope | [REMOTE_SCOPE, e.g. "Any EU-remote role" or "Any remote role in <region>"] |
| Hybrid | In scope when the office is commutable from base, or in an authorized-relocation country |

**Verdicts.** On-site or hybrid in an **authorized** country is a **PASS** -
relocation is not a deal-breaker here, so never fail a posting merely for requiring
it. On-site or hybrid in a country that is **not** on the authorized list and not
commutable from base is a **FAIL**. Remote within the declared scope is a **PASS**.
Frequent international travel is a **FLAG**.

Relocation willingness may be stated directly in cover letters for postings in the
authorized list.

---

## Where the gates run

| Command | Role | Gates |
|---|---|---|
| `/scrape` | Collect and deduplicate postings | **None.** Collection-stage filters only (posting-body language, geographic search scope), which drop a listing before anything is scored |
| `/rank` | Triage: gate, then score | **All four**, once per posting, in Step 2a, in the order eligibility → language → experience → location. First FAIL wins and stops that job |
| `/apply` | Build the application | **None.** A job carried from `/rank` was gated there. A cold posting handed straight to `/apply` is reported as **ungated** at the Step 1c shortlist gate, for the user to judge |

A `FAIL` is never scored and never drafted; `/rank` Step 4 records it as
`"status": "skipped"` with a `skip_reason` (`eligibility`/`language`/`experience`/`location`)
and a `skip_note` quoting the posting. A `FLAG` proceeds and stays visible.

A gate whose input is missing must never degrade to a silent PASS. If any table above
is empty or still holds a placeholder, `/rank` stops and says so rather than ranking
against a gate it cannot evaluate.
