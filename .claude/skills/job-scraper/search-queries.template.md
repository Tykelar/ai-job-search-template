# Search Queries for Job Scraper — Template

<!--
This is the TRACKED template. `/scrape` never reads this file directly — it reads
`search-queries.md` in this same directory, which is personal, gitignored, and not
committed. `/setup` (Section 9 of Path C, or the equivalent follow-up questions in
Path A) generates `search-queries.md` from this template by replacing every
[PLACEHOLDER] token with your actual search configuration. `/setup --section search`
regenerates it later as your priorities change.

If `search-queries.md` does not exist yet, copy this file to `search-queries.md` and
fill in the placeholders yourself, or just run `/setup --section search`.
-->

## Installed portal CLIs (primary for `/scrape`)

`/scrape` discovers every portal skill under `.agents/skills/*/SKILL.md` and runs its CLI first.

- **`linkedin-search`** (country-agnostic) — pass `--location` per target market.
- **`freehire-search`** (country-agnostic, tech-focused) — pass `--country` / `--region` facets; one call can span several countries.
- Any market-specific portals you add via `/add-portal` (e.g. a local job board) are auto-discovered the same way — list them here once added, with a one-line note on what each is best for.

The `site:` templates further down are the **WebSearch fallback** — for company career pages or when a CLI fails.

**Language scope:** write every query category in the languages you work in professionally (see the `Languages:` line in CLAUDE.md's Identity section). Translate each category's keywords rather than machine-translating word-for-word. Two *separate* language checks then apply to what comes back — the **Language Filter** below (scrape-time, on the language a posting is *written* in) and `04-job-evaluation.md`'s **Language Gate** (on the languages the role *requires*). See the Language Filter section for how they differ.

## Target Profile (drives keywords)

- **Primary roles:** [YOUR_PRIMARY_ROLE_TYPE] — 2-4 job titles you'd search for first, e.g. "Data Scientist", "ML Engineer".
- **Secondary roles:** [YOUR_SECONDARY_ROLE_TYPE] — adjacent roles worth a wider net.
- **Seniority:** [YOUR_SENIORITY] — e.g. "junior / graduate / trainee" or "mid / senior", based on your actual years of experience. State it plainly so query breadth (Priority 4, `broad` mode) matches your real level.

## Geography (open to relocation)

- **Home market:** [YOUR_HOME_MARKET] — your base city/region and realistic commute radius, or "remote-first" if you have no commute constraint.
- **Relocation-OK countries:** must match the authorized list in `config/gates.md` Gate 4 (the single source of truth). [YOUR_RELOCATION_COUNTRIES] — comma-separated list, or "none" if you're not open to relocating.
- **Remote:** [YOUR_REMOTE_SCOPE] — e.g. "any EU-remote role regardless of country", or "remote within [region] only".

### LinkedIn `--location` strings per market
[YOUR_LINKEDIN_LOCATION_STRINGS] — one string per market from the list above, e.g. `Portugal` · `Remote`. City-level strings are useful too (e.g. `Lisbon, Portugal`).

### freehire facets per market
`--country [YOUR_COUNTRY_CODES]` (comma = OR, ISO-2 codes). Add `--region eu,none` (or your region's equivalent) to sweep remote roles that never resolved a geography. Discover live facet values at `/api/v1/jobs/facets?q=<role>` — never invent them.

## Search Matrix (pinned — do not improvise)

Run exactly the query × market × pass combinations you define here, and report the call count in `/scrape` Step 5. Leaving breadth to run-time judgement makes yields incomparable across runs — pin the matrix instead of re-deciding it each time.

- **Core markets** — [YOUR_CORE_MARKETS] — the markets that get every priority category and the deepest breadth pass.
- **Extended markets** (optional) — [YOUR_EXTENDED_MARKETS] — markets that only get the recency pass on your top-priority category.

| Priority | Recency pass (page 1) | Breadth pass | Breadth pages |
|---|---|---|---|
| 1 — [your top priority category] | Core + Extended | Core | 2 |
| 2 — [second priority category] | Core | Core | 1 |
| 3 — [third priority category] | Core | Core | 1 |
| 4 — [wider-net category, `broad` only] | Core | Core | 1 |

Priority 1 gets the deepest sweep because it is your primary target. Estimate and record the **expected call count** for a default run here once you've run it once or twice, the same way the framework tracks it — this makes a thin run visible instead of looking like a quiet market.

**Language variants are scoped, not multiplied** — only run a query category in more than one language where you actually expect postings in that language for that market; running every language across every market multiplies the matrix for little return.

## Query Categories

Queries are grouped by priority. Substitute `<market>` from the **Search Matrix** above — never pick markets ad hoc. The `--jobage` values are the **breadth-pass** windows; the recency pass overrides them per `SKILL.md` Step 1b.

### Priority 1: [Your top priority category]
```
linkedin  -q "[YOUR_PRIMARY_JOB_TITLE]"       -l <market> --jobage 14
linkedin  -q "[YOUR_KEY_SKILL]"                -l <market> --jobage 14
freehire  -q "[YOUR_DOMAIN_KEYWORD_1]"  --country <codes> --jobage 21
```

### Priority 2: [Your second priority category]
```
linkedin  -q "[YOUR_SECONDARY_JOB_TITLE]"     -l <market> --jobage 14
freehire  --category [YOUR_FREEHIRE_CATEGORY]  --country <codes> --jobage 21
```

### Priority 3: [Your third priority category]
```
linkedin  -q "[YOUR_ADJACENT_JOB_TITLE]"      -l <market> --jobage 14
```

### Priority 4: [Wider-net category] (`broad` only)
```
linkedin  -q "[YOUR_BROADER_JOB_TITLE]"       -l <market> --jobage 30
```

## Location Filter

[YOUR_HOME_MARKET] roles: verify commute feasibility or remote/hybrid fit. Relocation-OK countries: accept onsite/hybrid (relocation expected). Reject markets outside your configured list (unless fully remote and in scope).

## Language Filter

The candidate's declared languages come from the **Languages table in `config/gates.md`** (Gate 2) - the single source of truth. Read it at run time rather than trusting a level copied into this file.

This filter is **not** the Language Gate: it reads what language the ad is *written in* and drops the listing before anything is scored, while the gate reads what the *role requires* and runs once, in `/rank` Step 2a.

A posting **written in** a language outside that set is a strong proxy for the job requiring that language day to day. Filter on the language of the **posting body**, not the employer's country:

| Posting body language | Action |
|---|---|
| [languages you work in at a working level] | **Include.** Working proficiency. |
| [a language you have only basic/limited proficiency in, if any] | **Include but mark ⚠.** State honestly why (e.g. below working proficiency); the user decides. |
| Any language outside your declared set | **Exclude.** Record in `seen_jobs.json` with `"status": "skipped"` and `"skip_reason": "language"`, and count it in the Step 5 summary. |

Rules that keep this honest:

- **Filter on the posting body, not the employer.** A local company posting in a language you work in is **in scope** even if the employer's home market speaks something else.
- **A stated working-language line overrides the body language.** If a posting is written in a language outside your set but explicitly states the working language is one you have, include it.
- **Never silently drop.** Excluded postings are counted in the Step 5 output so you can see what the filter cost you, and they stay in `seen_jobs.json` so dedup still works.
- **Mixed-language postings** count by whichever language carries the actual requirements section.

### Two separate checks, both applied

The table above is a **scrape-time** screen on the language a posting is *written in* — your explicit policy. It is distinct from `04-job-evaluation.md`'s **Language Gate**, which runs later (at `/scrape` Step 3 and in `/rank`) and reads the languages a posting requires **for the role**: a required language not declared at all is a hard FAIL, while a declared language at a stated bar above your declared level is a FLAG for you to judge, never a silent exclusion. Both checks run, and neither is silent.

## Date Filter

Two windows, one per pass (flags in `SKILL.md` Step 1b):

- **Recency pass:** last ~48 hours.
- **Breadth pass:** last 14 days by default; widen to 30 for thinner categories.

If a posting date can't be determined, include it, store `posted_date: null`, and flag it "date unknown" in the Step 5 table — never substitute today's date.

## WebSearch fallback (`site:` templates)

Use only for portals without a CLI or company career pages:
```
site:linkedin.com/jobs "[YOUR_PRIMARY_JOB_TITLE]" ([YOUR_CORE_MARKETS] OR remote)
site:boards.greenhouse.io "[YOUR_PRIMARY_JOB_TITLE]" [YOUR_REGION]
site:jobs.lever.co "[YOUR_SECONDARY_JOB_TITLE]" [YOUR_REGION]
```
