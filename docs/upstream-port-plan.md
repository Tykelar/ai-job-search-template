# Upstream Port Plan

Status: **active**
Owner: Tykelar fork (`personal` branch)
Upstream: `MadsLorentzen/ai-job-search` @ `upstream/master` (`120f476`, v1.7.1 + Unreleased)
Fork root commit: `3c0c028` "chore: initial sanitized template state" (histories are **unrelated**)

## Objective

Port the upstream features, fixes and hardening that this fork lacks, in small,
independently verifiable work packages. Each part is executed **in its own fresh
session**, ends green, updates the Progress ledger below, and produces a
`/handoff` for the next session.

## Scope / non-goals

- **In scope:** upstream commits from ~v1.4.0 → `master` that are absent here.
- **Out of scope:** rewriting the fork's own work (gate refactor, USI sync,
  `config/gates.md`, CV methodology 2.4.0). Those are preserved, never replaced.
- **Not a rebase.** Do not merge `upstream/master` wholesale; do not let upstream
  versions of fork-rewritten files overwrite the fork's content.

## Porting methods

Choose per file, using the classification in [Appendix B](#appendix-b-file-classification).

| Method | When | Command |
|---|---|---|
| **A — whole-file checkout** | File is an untouched *older copy* of upstream (all of `.agents/skills/**`, `salary_lookup.py`, `tools/convert_salary_excel.py`, `tools/verify_pdf.py`, `.claude/settings.json`, `gmail-sync.md`, `html-report.md`, `reset.md`, `expand.md`, `09-web-research.md`, `CONTRIBUTING.md`) | `git checkout upstream/master -- <path>` |
| **B — cherry-pick** | Self-contained commit whose files are close to upstream | `git cherry-pick -x <sha>` (fallback: `git show <sha> \| git apply --3way`) |
| **C — manual reconcile** | File the fork rewrote (see Appendix B "CUSTOM") | `git show <sha> -- <path>`, integrate by hand; never overwrite fork sections |

**Rule of thumb:** verify first, then port.
```bash
git diff --stat HEAD upstream/master -- <path>
```
If the diff is only upstream additions (fork is the older copy) → **A**. If the fork
has its own lines → **B** or **C**.

## Global conventions

- **Branch per part:** `port/part-NN-<slug>` cut from `personal`. Merge back to
  `personal` only when the part's verification is green.
- **One commit per upstream change**, using `-x` when cherry-picked, so a future
  upstream-triage pass can match by patch-id once history converges. Never rewrite
  the fork's own commits.
- **Never commit personal data.** `applications/**`, `documents/applications/**`,
  `documents/usi/**`, `config/gates.md` values, `job_scraper/seen_jobs.json` and the
  tracker are personal; keep them out of port commits.
- **CHANGELOG:** add a short `### Upstream port` block to `[Unreleased]` per part,
  referencing the upstream PR/SHA. Do not copy upstream's CHANGELOG wholesale.
- **Framework version markers:** if a port changes a `framework_version`-marked file,
  bump it and note it (upstream's marker values diverge from this fork's; never copy
  upstream's number blindly).
- **Skill roots are not one namespace.** `.claude/skills/` (fork methodology and
  workflow specs) and `.agents/skills/` (upstream's portable portal skills) are read
  by different runtimes; never install the same skill `name` in both. Keep
  `.agents/skills/` an upstream-only mirror so `git checkout upstream/master --
  .agents/skills/` and future merges stay clean.

## Verification (run every part)

```bash
# Python
python -m unittest discover -s tests -t . -v
# Lint / guards
python tools/lint_skills.py
python tools/security_guards.py
# A single portal CLI
cd .agents/skills/<portal>-search/cli && bun install && bun run typecheck && bun test
# All portal CLIs
for d in .agents/skills/*/cli; do (cd "$d" && bun run typecheck && bun test) || exit 1; done
```

Baseline note: record the initial state of each command in Part 0. Any pre-existing
failure must be recorded as a baseline, not "fixed" by a port (unless the port is the
fix).

## Session close-out (every part) — this is the `/handoff`

1. Commit code on `port/part-NN-<slug>`; merge to `personal` when green.
2. Update the **Progress ledger** (status, commit SHA, deviation notes).
3. Commit the ledger update.
4. Produce a handoff document per the `handoff` skill contract:
   - Write to the OS temp dir (`%TEMP%` / `$TMPDIR`), not the workspace.
   - Name: `handoff-port-part-NN-<YYYYMMDD-HHMM>.md`.
   - Sections: **Part**, **Status**, **What changed** (files + commit SHAs),
     **Upstream refs used**, **Deviations & why**, **Verification evidence**
     (commands + result), **Next part**, **Blockers/open questions**,
     **Suggested skills**.
   - Reference artifacts by path/SHA; do not duplicate them; redact PII.
   - If `/handoff` is unavailable in the session, do the above manually from the
     copied skill at `.claude/skills/handoff/SKILL.md` (installed in Part 0).

## Progress ledger

| Part | Title | Status | Branch / commit | Notes |
|---|---|---|---|---|
| 0 | Preflight & handoff setup | ☑ done | merge `4b89ad6` into `personal` (part branch `port/part-00-preflight` @ `cfbc5fd`) | Baseline all-green (no pre-existing failures); `handoff` skill installed; no upstream code ported. |
| 1 | Portal CLIs — wholesale refresh | ☑ done | merge `889f407` into `personal` (part branch `port/part-01-portal-clis` @ `9e12980`) | Method A take of `.agents/skills/`: 64 files, 6/6 CLIs green (312 tests, no network). Also ported `cffacfd` (#288) frontmatter — the four Danish portals now ship `enabled: false` (correct for this fork's PT market). `cffacfd`'s `setup.md` half deferred to Part 11 (now in its table). |
| 2 | Cross-portal contract, settings, CI discovery | ☑ done | merge `4a91964` into `personal` (part branch `port/part-02-contract-settings-ci` @ `d696a88`) | Contract test (`db8312948`) green against all six CLIs; `.claude/settings.json` scoped (A) with `security_guards.py` mirroring the allowlist; `discover-clis` added to CI (`f658bb6f9`), fork `applications/` paths and Tykelar placeholder condition preserved. Also took `f658bb6f9`'s `add-portal.md` note (same commit; no other part covered it). |
| 3 | Salary tooling (+ UTF-8 stdout) | ☑ done | merge `2aef346` into `personal` (part branch `port/part-03-salary-tooling` @ `4cd5c16`) | Method A take of the salary files (untouched `v1.4.0` copies): `salary_lookup.py`, `tools/convert_salary_excel.py`, three test files, + new `tests/test_convert_salary_excel_integration.py`. 112 salary tests green; full suite 271 (skipped=1). UTF-8 guards self-contained in both tools (salary files portion of `ba4f2397a`). |
| 4 | PDF tooling & ATS verification stack | ☑ done | merge `95ea9ee` into `personal` (part branch `port/part-04-pdf-tooling` @ `2a80e9e`) | Method A take of `tools/verify_pdf.py`, `tests/test_verify_pdf.py`, `tests/test_latex_guidance.py`, + new `tools/verify_layout.py`/`tests/test_verify_layout.py`. 51 Part-4 tests green; full suite 313 (skipped=3). Deviations: `verify_layout` docstring escape; `verify_pdf` tolerates a missing `pdfinfo` on text-only checks (`--pages` still fails); `test_gate_configuration` also guards `verify_pdf.py`; `test_latex_guidance` ignores a `\item [` example that sits in a `%%` comment (the template example documents the pitfall). `tests/test_tools_utf8_output.py` deferred to Part 7/13 per the Part 3 handoff. |
| 5 | Deadline persistence end-to-end | ☐ todo | | |
| 6 | seen_jobs provenance & scrape behavior | ☐ todo | | |
| 7 | `/rank` refactor & hardening | ☐ todo | | |
| 8 | `/outcome` stale sweep & CSV-safe notes | ☐ todo | | |
| 9 | Company-research cache | ☐ todo | | |
| 10 | `/apply` source-host verification | ☐ todo | | |
| 11 | Workflow spec fixes | ☐ todo | | |
| 12 | `documents/projects` & `/expand` GitHub | ☐ todo | | |
| 13 | CI, guards, tests & repo infra | ☐ todo | | |
| 14 | `08-application-forms` + final integration | ☐ todo | | |

Legend: ☐ todo · ◐ in progress · ☑ done · ⚠ blocked

---

## Part 0 — Preflight & handoff setup

**Goal:** establish a verified baseline and make the per-session workflow real.

**Steps**
1. `git fetch upstream --tags` and confirm `upstream/master` = `120f476`.
2. Record the baseline of every verification command (Python tests, lint, guards,
   all six CLI `typecheck`/`test`) as run today. Save output under
   `docs/port-logs/part-00-baseline.txt`.
3. Confirm the `handoff` skill is available in this workspace. If not, copy it from
   a sibling project (same shape in each):
   - `C:/Users/josep/Desktop/Dev/DevPractice/.claude/skills/handoff/SKILL.md`
   - `C:/Users/josep/Desktop/Dev/Support_Ticket_assistant/.claude/skills/handoff/SKILL.md`
   Install to `.claude/skills/handoff/SKILL.md` **only** — one canonical copy. Do
   not duplicate it under `.agents/skills/`: the two roots are read by different
   runtimes, so a second real copy collides wherever both roots are enumerated and
   the two copies drift. Keep `.agents/skills/` an upstream-only mirror. Commit as
   fork tooling.
4. Create `personal` from its current tip; confirm clean tree.

**Verify:** baseline recorded; `handoff` skill loads; `git log --oneline -1`.

**DoD:** ledger present (this file committed); baseline file committed; no code ported.

**Handoff:** next part = 1; note any baseline failures.

---

## Part 1 — Portal CLIs: wholesale upstream refresh

**Goal:** bring all six portal CLIs to upstream's current state (dozens of bug fixes,
contract fields, crash guards, retry/backoff, URL normalization, closed-posting
detection). All 47 CLI files are exact *older copies* of upstream (Appendix B), so
this is a safe, mechanical replacement.

**Upstream refs**
`3bfd525cc` (unknown flags), `fa8db56a9` (single-dash flags), `c42806674` /
`79cd383e5` (fractional flags), `6ef295bf7` (trailing-slash URLs), `3d296448b`
(linkedin `isActive`), `a30691213` (drop `applyUrl`), `c85640e30` (jobindex detail
rewrite), `b067928da` (ASAP→null), `c7bd494f1` (non-jobindex detail URLs),
`2edf8c41f` (linkedin/jobindex fixtures), `56f679e5c` (jobdanmark pay­load trim),
`17bc69869` / `04186b9a3` / `df7919cdf` (contract fields), `7aba0b4a9` (postcode
comma), `c844359ed` (autocomplete null text), `dab215073` (jobdanmark detail
fallback), `c2cd71dde` (429/5xx backoff), `f8c606fb3` (jobnet 404 fallback),
`bcba687fb` (jobnet sentinel), `ba9b1d837` (null publicationDate), `0883958d4`
(bad pubDate), `48965960d` (deadline ISO), `71674d022` (detail URL inputs),
`dd02c8248` (freehire `--no-description`).

**Method:** A
```bash
git checkout upstream/master -- .agents/skills/
```
This brings `src/`, `tests/`, `README.md`, `package.json`, `bun.lock`, and each
portal `SKILL.md`. It does **not** touch `.claude/skills/job-scraper/SKILL.md`
(handled in Part 6) — upstream `3d296448b` also edits that file; its CLI half lands
here, its spec half in Part 6.

**Fork adaptation:** the CLI `src/`/`tests/` had no fork changes, so they are an exact
upstream take. One non-CLI divergence surfaced during the take: the six `SKILL.md`
frontmatter blocks were a *pre-`cffacfd` older copy* (the four Danish portals were
`enabled: true`). Upstream `cffacfd` (#288) ships them `enabled: false` so a non-Danish
user's `/scrape` does not spend tokens on irrelevant boards. The fork's candidate market
is Portugal, so the upstream value is the correct one — accepted, no fork override.
`cffacfd` also edits `.claude/commands/setup.md`, which is CUSTOM; that half is listed
in Part 11 and must not be lost. `package.json` dependency versions were already at
upstream's, so `bun.lock` is unchanged.

**Verify**
```bash
for d in .agents/skills/*/cli; do (cd "$d" && bun install && bun run typecheck && bun test) || exit 1; done
```
Spot-check the reported high-severity bugs are gone: unknown flag now exits 1 with
`UNKNOWN_FLAG`; `jobindex detail` returns real fields; `jobbank search` emits `date`.

**DoD:** all six CLIs typecheck and pass their fixture tests; `bun.lock` committed;
no personal files touched.

**Handoff:** next = 2; note any CLI test that needed network (must be none).

---

## Part 2 — Cross-portal contract pin, settings, CI portal discovery

**Goal:** lock the `/scrape` search-output contract across portals, narrow the
pre-approved `bun run` permission, and make CI discover portal CLIs dynamically.

**Upstream refs:** `db8312948` (contract test), `2d636c50b` (`bun run` scoping),
`f658bb6f9` (discover-clis).

**Target files / method**
- `tests/test_scrape_contract.py` — new; take upstream (A):
  `git checkout upstream/master -- tests/test_scrape_contract.py`.
  *Note:* `8c81edc33` later extends this test for job keys; that extension belongs
  to Part 6/7 — take only the `db8312948` version here if the later hunk depends on
  `tools/job_key.py` (check `git show 8c81edc33 -- tests/test_scrape_contract.py`).
- `.claude/settings.json` — A (`git checkout upstream/master -- .claude/settings.json`).
  Confirmed to be an untouched older copy; the upstream version already contains the
  per-CLI `bun run` entries and the new tool permissions.
- `.github/workflows/ci.yml` — **C**. Add upstream's `discover-clis` job (see
  `git show f658bb6f9 -- .github/workflows/ci.yml`) while preserving fork-specific
  lines (the `Tykelar/ai-job-search-template` placeholder condition, the fork's
  `applications/` compile commands). Do not reintroduce upstream's
  `MadsLorentzen`-only guards.
- `tools/security_guards.py` — **C**. Add the scoped `bun run` entries and new tool
  paths from `2d636c50b` while keeping the fork's extra `REQUIRED_IGNORE_RULES`
  (`search-queries.md`, `applications/**` CV/CL patterns, `!applications/OpenFonts`,
  the example PDFs). Coordinate the file's final allowlist with Part 13.

**Verify:** `python tools/security_guards.py`;
`python -m unittest tests.test_scrape_contract -v`;
`git check-ignore -v` on the fork's extra rules still returns a match.

**DoD:** contract test green; `bun run` no longer wildcarded; `discover-clis` present;
fork ignore rules intact.

**Handoff:** next = 3.

---

## Part 3 — Salary tooling (+ UTF-8 stdout)

**Goal:** port the salary lookup/converter fixes and the Windows UTF-8 stdout guard.

**Upstream refs:** `7d00ec792` (A.M.B.A.), `9833a5dcb` (null metadata/categories),
`7f709eda5` (header corroboration), `621ce5ab3` (dot thousands), `1c19f6c45`
(locale by last separator + compound headers), `968fb1bd7` (count/index pair),
`b91c6125e` (privacy footnote), `362ef6a52` (Excel integration tests), `ba4f2397a`
(UTF-8 stdout — salary files portion).

**Method:** A (both files are untouched older copies; upstream versions already carry
the UTF-8 guard).
```bash
git checkout upstream/master -- salary_lookup.py tools/convert_salary_excel.py \
  tests/test_salary_lookup.py tests/test_convert_salary_excel.py \
  tests/test_convert_salary_excel_integration.py
```
The integration test needs optional `openpyxl`; it must skip (not fail) when absent.

**Verify:** `python -m unittest tests.test_salary_lookup tests.test_convert_salary_excel tests.test_convert_salary_excel_integration -v`.

**DoD:** all salary tests green; `salary_lookup.py` normalizes `A.M.B.A.`; US/UK and
Danish number forms parse; missing `openpyxl` skips the two integration cases.

**Handoff:** next = 4. Carried forward: upstream's `tests/test_tools_utf8_output.py`
spans all six tools (`rank_state.py`, `job_key.py`, `verify_pdf.py`,
`verify_layout.py`, plus the two salary tools); take it in the last part that
completes those tools (Part 7 for `rank_state`/`job_key`, Part 4 for
`verify_pdf`/`verify_layout`) or in Part 13.

---

## Part 4 — PDF tooling & ATS verification stack

**Goal:** mechanical PDF layout checking, pypdf text-layer fallback, deterministic
encoding, and LaTeX escape guidance.

**Upstream refs:** `cbd8a991a` + `1b65f7198` (`verify_layout.py`), `dea8140db`
(pypdf), `75c15eeec` (verify_pdf fixup), `73d52e099` (typographic folding + T1
fontenc), `b2545d512` (braced bullets, escapes, `pdftotext -enc UTF-8`),
`c696b60b7` (moderncv `\namefont`), `07cec1f22` (placeholder sentinels),
`ba4f2397a` (UTF-8 portion).

**Target files / method**
- `tools/verify_pdf.py` — A.
- `tools/verify_layout.py`, `tests/test_verify_layout.py` — new, take upstream (A).
- `tests/test_verify_pdf.py`, `tests/test_latex_guidance.py` — take upstream (A).
- `.claude/skills/job-application-assistant/05-cv-templates.md` — **C** (fork is
  2.4.0). Integrate: braced `\item {[text]}` bullets, the LaTeX special-character
  table, `pdftotext -layout -enc UTF-8`, and the pypdf-before-Poppler order.
- `.claude/commands/apply.md` — **C**; wire Step 5d to pypdf-first and the
  `verify_layout.py` invocation (do not restructure the fork's gate Stey 1).
- `CLAUDE.md`, `README.md`, `SETUP.md` — **C**; add the pypdf/`-enc UTF-8` notes only.
- `.github/workflows/ci.yml` — **C**; add the bookworm LaTeX leg and the
  `Achievement`-survives-`pdftotext` assertion, keeping fork-specific jobs.
- `applications/main_example.tex` and the fork's compiled-CV toolchain: check for the
  moderncv `\firstnamestyle` bug (fork currently has no match; if it uses a banking
  template, apply `\namefont`).

**Verify:** `python -m unittest tests.test_verify_pdf tests.test_verify_layout tests.test_latex_guidance -v`;
`python tools/verify_layout.py <a compiled pdf>` (skips gracefully without Poppler).

**DoD:** layout tool present; `verify_pdf` prefers pypdf; `-enc UTF-8` documented;
tests green.

**Deviations (fork adaptations to the A takes, recorded in the ledger and the
commit message):** `tools/verify_layout.py` escapes `\hypersetup` in its docstring
(Python 3.12 SyntaxWarning); `tools/verify_pdf.py` lets a text-only check survive a
missing `pdfinfo` when the `pdftotext` on PATH is the Git-for-Windows xpdf build
(`--pages` still fails loudly, with two regression tests);
`tests/test_gate_configuration.py` also asserts `verify_pdf.py`; and
`tests/test_latex_guidance.py` strips `%` comments from `.tex` lines before
matching, because the template example documents the `\item [text]` pitfall
inside a `%%` comment. The two tool files are therefore no longer byte-identical
to upstream - reconcile by hand if upstream changes them. `tests/test_tools_utf8_output.py` is deferred to Part 7/13.

**Handoff:** next = 5.

---

## Part 5 — Deadline persistence end-to-end

**Goal:** store the application `deadline` wherever the framework provably holds it,
so urgency and expiry survive across runs, and expose it in the tracker/dashboard.

**Upstream refs:** `c855e11d2` (#319/#324, end-to-end), `762d3218e` (#325,
html-report column), `57e82d2b5` (non-ISO deadlines defensive).

**Fork adaptation (all C):** this is the fork's own data model, and the fork's
`rank.md`/`apply.md`/`outcome.md`/`SKILL.md` are gate-refactored. Reconcile manually:
- `.claude/skills/job-scraper/SKILL.md` — add `deadline` to the seen_jobs schema
  (`null` vs missing distinguished, never guessed).
- `.claude/skills/job-application-assistant/SKILL.md` — bump `framework_version`;
  write the deadline on application.
- `.claude/commands/rank.md` — re-derive urgency from the stored deadline (no
  re-fetch) and sweep past-deadline entries to `expired`; keep the fork's
  four-gate Step 2a untouched.
- `.claude/commands/apply.md` — Step 0 extracts the deadline; Step 6b writes it.
- `.claude/commands/outcome.md`, `gmail-sync.md`, `notion-sync.md`,
  `html-report.md` — surface/preserve the new column.
  (`gmail-sync.md` and `html-report.md` are older copies → can take upstream A, then
  layer the fork's tracker-status-vocabulary references if needed.)
- `job_search_tracker.csv` — header-line-only migration: append `deadline` as the
  14th column. **This is personal data**: run the migration locally, do not commit
  tracker rows.

**Verify:** `python -m unittest tests.test_rank_command tests.test_apply_records_application tests.test_html_report_command tests.test_upskill_skill -v`;
manual: a ranked entry with a past deadline moves to `expired` on the next run.

**DoD:** `deadline` round-trips scrape → rank → apply → tracker → report; fork gates
unchanged.

**Handoff:** next = 6; flag any tracker migration performed.

---

## Part 6 — seen_jobs provenance & scrape behavior

**Goal:** record posting provenance and harden `/scrape` collection.

**Upstream refs:** `f136b534d` (seen_jobs `source`: `cli` vs `websearch`),
`ea2f25b39` (posted_date — verify already present; port any remainder),
`9a6930974` (client-side recency fallback for flagless portals), `3d296448b`
(spec half: consume linkedin `isActive` → `expired`), `d4e0c64c3`
(`location` → `location_verdict`), `2ff108525` (archive path as one component),
`ab5732138` (`$SCRATCHPAD` fail-loud).

**Fork adaptation (C):** integrate into the fork's `job-scraper/SKILL.md` and
`rank.md` without disturbing the gate-refactor or `config/gates.md` references:
- Add the `source` field + Step 1c tagging + Step 5 summary line.
- Add the recency fallback text (fork may already scope by date; verify).
- Wire `isActive: false` → `status: "expired"` (marked, not dropped).
- Rename the persisted rank verdict to `location_verdict` with legacy read-compat.
- Apply the `<company>_<role>` single-component rule via `documents/README.md`
  (CUSTOM) and cite it from `apply.md`/`outcome.md`/`interview.md`.
- `09-web-research.md` is an older copy → A for the `$SCRATCHPAD` fix.

**Verify:** `python -m unittest tests.test_scrape_provenance tests.test_scrape_contract tests.test_rank_command tests.test_security_guards -v`.

**DoD:** new jobs carry `source`; a closed linkedin posting becomes `expired`;
`location_verdict` written and legacy read; archive paths single-component.

**Handoff:** next = 7.

---

## Part 7 — `/rank` refactor & hardening

**Goal:** move seen_jobs read/write into a tool, bound batches, validate scores, and
flag stale postings.

**Upstream refs:** `3bf41149e` (`tools/rank_state.py`: `candidates`/`sweep`/`apply`),
`8c81edc33` (`tools/job_key.py` deterministic keys), `120f476a0` (Unicode tracker
matching), `2e8600d69` (score-dimension validation), `6a308c5cc` (UTF-8 BOM tracker
header), `456f2bfdb` (non-Latin fallback keys), `fd89eac17` (`--limit`),
`284dc4c2d` (stale `posted_date` ⚠ flag), `ba4f2397a` (UTF-8 in these tools).

**Target files / method**
- `tools/rank_state.py`, `tools/job_key.py`, `tests/test_rank_state.py`,
  `tests/test_job_key.py` — new; take upstream (A). They already include the UTF-8
  guard.
- `.claude/commands/rank.md` — **C**. Replace the inline `python -c` block (Step 1)
  and Step 4 write-back with the documented `rank_state.py` calls; add `--limit`,
  the stale-posting flag (`⚠ posted <date>, N months ago`, FLAG not veto), and keep
  the fork's four-gate Step 2a, `--rescan-vetoed`, and `config/gates.md` inputs.
- `.claude/settings.json` — already carries the rank_state/job_key permissions from
  Part 2; verify.
- `tools/security_guards.py` — ensure the tool paths are allowed (final check in
  Part 13).

**Verify:** `python -m unittest tests.test_rank_state tests.test_job_key tests.test_rank_command -v`.

**DoD:** `/rank` reads/writes via the tool; batch capped at 10 with `--limit`;
invalid scores rejected per job; Unicode companies/roles match; stale flag shown.

**Handoff:** next = 8.

---

## Part 8 — `/outcome` stale sweep & CSV-safe notes

**Goal:** batch-resolve quiet applications and stop free-form notes corrupting the CSV.

**Upstream refs:** `6176e6aac` (`/outcome stale [N]`), `c93609cd2` (tracker-notes CSV
escaping), `c776e3f2b` (glob the full `<company>_<role>` stem).

**Fork adaptation (C):** `outcome.md` and `interview.md` are fork-rewritten.
Integrate the new `stale`/`sweep` branch (numbered list → `all`/`select`/`skip` →
resolve to `no_response` → log dated notes → calibrate at 3+), the note-escaping
rule at every write path, and the stem-glob fix. Keep the fork's tracker-status
vocabulary references.

**Verify:** `python -m unittest tests.test_outcome_stale tests.test_tracker_notes_csv_safe tests.test_outcome_followup tests.test_tracker_status_vocab -v`.

**DoD:** `/outcome stale` resolves confirmed rows; notes with commas/quotes/newlines
survive a round-trip; no tracker row is silently dropped.

**Handoff:** next = 9.

---

## Part 9 — Company-research cache

**Goal:** cache the Company Research Checklist so `/apply` and `/interview` don't
repeat it.

**Upstream refs:** `becdc5dfd` (#349), `eee739ed7` (follow-up).

**Fork adaptation (C):** add `company_research/<normalized>.json` (30-day TTL) to
`.claude/skills/job-application-assistant/04-job-evaluation.md`, and reference the
cache from `apply.md` Step 2 and `interview.md` Step 2. Preserve the fork's
gate-refactored 04 (keep the gate *mechanisms*, add the cache section). Add the
ignore rule + guard entry:
- `.gitignore` — **C**; add `company_research/*.json` (rooted, not `**/`).
- `tools/security_guards.py` — **C**; add the matching `REQUIRED_IGNORE_RULES` entry
  while preserving fork rules.
- `company_research/.gitkeep` — take upstream.

**Verify:** `python -m unittest tests.test_company_research_cache tests.test_security_guards -v`;
`git check-ignore company_research/foo.json` matches.

**DoD:** cache read/write documented; cache never treated as verified fact; ignore
rule enforced by the guard.

**Handoff:** next = 10.

---

## Part 10 — `/apply` source-host verification

**Goal:** verify a posting URL's provenance before spending drafting tokens.

**Upstream refs:** `88d1b6104` (#431/#467).

**Fork adaptation (C):** add the Step 1 host check to `apply.md` — compare the
posting host against installed portal boards and the six ATS apexes
(`greenhouse.io`, `lever.co`, `myworkdayjobs.com`/`workday.com`, `ashbyhq.com`,
`smartrecruiters.com`, `workable.com`), fail closed on look-alike spoofing, and print
`⚠ Unverified source host: <hostname>` when unrecognised. This must sit **before**
the fork's cold-posting "Ungated" shortlist gate at Step 1c, not replace it.

**Verify:** `python -m unittest tests.test_apply_host_check tests.test_apply_records_application -v`.

**DoD:** spoofed prefix/suffix hosts fail; unknown hosts flagged; gate flow intact.

**Handoff:** next = 11.

---

## Part 11 — Workflow spec fixes

**Goal:** the remaining small command-level correctness fixes.

**Upstream refs / targets**
| Fix | Ref | File | Method |
|---|---|---|---|
| gmail-sync `in:inbox` → `-in:sent -in:drafts` | `4ed5fee22` | `gmail-sync.md` | A |
| html-report funnel + rejection rate | `2c3d2d855` | `html-report.md` | A (then verify tracker columns from Part 5) |
| `/reset profile` clears `04-job-evaluation.md`; documents covers `documents/postings/` | `d82df2fe5`, `2036b9704` | `reset.md` | A (older copy) — then **add the fork-only sweep targets**: `config/gates.md` gate table and the generated `search-queries.md` (template stays) |
| `/setup` fills `05`/`06` contact blocks (Step 3.5/3.6) | `e6f6f4e32` | `setup.md` | C |
| function-based (not title-based) matching | `5c423b406` | `setup.md`, `04-job-evaluation.md` | C |
| Danish demo portals ship disabled; `/setup` enables them for Danish-market users | `cffacfd` | `setup.md` | C — **the SKILL.md half was already taken in Part 1**; reconcile `setup.md` to match (do not re-enable the four Danish portals for this PT fork) |
| `/upskill` blank `fit_rating` fallback | `0e054f16e` | `.claude/skills/upskill/SKILL.md` | C |
| `$SCRATCHPAD` fail-loud | `ab5732138` | `09-web-research.md` | A |
| invited-PR reservation | `2ea29b09b` | `CONTRIBUTING.md` | A |

**Fork adaptation:** for `setup.md`/`04-job-evaluation.md`/`upskill/SKILL.md`, keep
the fork's USI/gate references and add only the upstream behaviour. `reset.md` is an
older copy but its file list may name fork files (`config/gates.md`,
`search-queries.template.md`) — reconcile after the wholesale take.

**Verify:** `python -m unittest tests.test_gmail_sync_command tests.test_html_report_command tests.test_reset_command tests.test_setup_command tests.test_upskill_skill tests.test_robots_check -v`.

**DoD:** each listed fix present and tested; no fork feature regressed.

**Handoff:** next = 12.

---

## Part 12 — `documents/projects` & `/expand` GitHub

**Goal:** independent-project ingestion and GitHub repo extraction.

**Upstream refs:** `e92f7d906` (`documents/projects/` Path A), `6b07b13bd`
(`/expand` GitHub).

**Target files / method**
- `documents/projects/.gitkeep` — new (A).
- `documents/README.md` — **C**; add the `projects/` section.
- `.gitignore` — **C**; add `documents/projects/**` (fork already ignores
  `documents/usi/**`; keep both).
- `tools/security_guards.py` — **C**; add the matching guard rule.
- `.claude/commands/setup.md` — **C**; add Path A project ingestion while keeping the
  USI flow and gate config writes.
- `.claude/commands/reset.md` — reconcile the added scope.
- `.claude/commands/expand.md` — A (older copy) for the GitHub extraction, then check
  the fork has no `/expand` customisation (it appears close to upstream).
- `tests/test_setup_command.py`, `tests/test_expand_command.py` — take upstream (A).

**Verify:** `python -m unittest tests.test_setup_command tests.test_expand_command tests.test_security_guards -v`;
`git check-ignore documents/projects/foo.md` matches.

**DoD:** projects ingest into `## Independent Projects`; GitHub repos extract
idempotently; ignore/guard rules present.

**Handoff:** next = 13.

---

## Part 13 — CI, guards, tests & repo infra

**Goal:** the CI/security/onboarding hardening batch.

**Upstream refs:** `23dc1936b` (Python 3.10–3.14 matrix), `ff3e2d00b` (bookworm — if
not done in Part 4), `6f0178a8a` + `9484a6183` (placeholder/pristine skips on forks),
`07cec1f22` (sentinel co-location), `1a116b3c6` + `e6f6f4e32` (CHANGELOG structure
guard), `65fbe8b8a` (framework-version tests), `9a074b262` (lint-skills tests),
`c20458d76` (robots tests), `730dcfb07` (ISSUE_TEMPLATE + `gh repo set-default`),
`34b8b3f91` (public-fork warning), `27eb57ae9` (README paid plan), `8d2786118` (docs).

**Method:** mostly **C** for `.github/workflows/ci.yml`, `tools/security_guards.py`,
`README.md`, `SETUP.md`; **A** for the new `tests/*` and
`.github/ISSUE_TEMPLATE/**`.

**Fork adaptation:** keep the fork's `Tykelar/ai-job-search-template` conditions in
`ci.yml` and the `upstream-watch.yml` workflow. Add tests that upstream added; skip
any that assume upstream's `cv/main_example.tex` path (fork uses
`applications/main_example.tex`) — adapt or mark fork-specific.

**Verify:** `python -m unittest discover -s tests -t . -v`;
`python tools/lint_skills.py`; `python tools/security_guards.py`;
`actionlint` if available.

**DoD:** CI matrix green locally equivalent; new guards tests pass; issue template
present; onboarding warning in place.

**Handoff:** next = 14.

---

## Part 14 — `08-application-forms` + final integration

**Goal:** decide on the missing skill file and close out the port.

**Steps**
1. Evaluate `.claude/skills/job-application-assistant/08-application-forms.md`
   (upstream, `framework_version 1.0.0`). If the fork wants the form-handling
   workflow, port it and reference it from `SKILL.md`; otherwise record the decision
   in `.github/upstream-wontport.txt` (add the relevant upstream SHAs) so triage stops
   re-surfacing it.
2. Confirm `tools/upstream_triage.py` / `check_upstream_updates.py` behave sensibly
   after the port; if the squashed history still makes them noisy, add a note to
   `SETUP.md` §8 documenting that the fork rebased history and how to review upstream
   manually.
3. Full verification sweep (all commands in **Verification**), plus every portal CLI.
4. Update `CHANGELOG.md` `[Unreleased]` with a consolidated `### Upstream port` block
   listing the PR/SHAs ported.
5. Remove `docs/port-logs/` baseline logs if they contain machine-specific noise, or
   keep them intentionally.
6. Tag/announce per the fork's convention.

**Verify:** full suite green; `git status` clean; no personal data staged.

**DoD:** plan ledger fully ☑; changelog records the port; handoff produced (final).

---

## Appendix A — Upstream commit inventory (v1.4.0 → master, 117 non-merge)

Full list with per-commit classification is reproducible from this repo:

```bash
git log --no-merges --format='%h %s' v1.4.0..upstream/master
```

Key groups by part are listed inline above. Commits **already effectively present**
in the fork (verified by content) include the changelog-only commits and the
fork's own ports; do not port them again:
`e09d3eb37` (tracker status vocab), `0e1a895c4` (job posting archive),
`3efc52ebd` (hooks allowlist), `cfd9a9fba` (upskill gitignore), `670d30ae7`
(upstream triage), plus the `1.5.0`–`1.7.0` release/changelog commits.

## Appendix B — File classification

Determined by matching each fork blob against upstream history.
**OLDER** = untouched older upstream copy → Method A. **CUSTOM** = fork diverged →
Method B/C.

**OLDER (safe wholesale):**
`.agents/skills/**` (47/47 files), `salary_lookup.py`, `tools/convert_salary_excel.py`,
`tools/verify_pdf.py`, `.claude/settings.json`, `.claude/commands/gmail-sync.md`,
`.claude/commands/html-report.md`, `.claude/commands/reset.md`,
`.claude/commands/expand.md`, `.claude/skills/job-application-assistant/09-web-research.md`,
`CONTRIBUTING.md`.

**CUSTOM (manual reconcile):**
`tools/security_guards.py`, `.gitignore`, `README.md`, `SETUP.md`, `CLAUDE.md`,
`.claude/commands/{apply,rank,outcome,interview,setup,notion-sync,add-portal,add-template}.md`,
`.claude/skills/job-scraper/SKILL.md`,
`.claude/skills/job-application-assistant/{04-job-evaluation,05-cv-templates,06-cover-letter-templates,SKILL}.md`,
`.claude/skills/upskill/SKILL.md`, `documents/README.md`, `.github/workflows/ci.yml`.

**Fork-only (never overwrite):**
`config/gates.md`, `.claude/skills/sync-usi/SKILL.md`, `tools/sync_usi.py`,
`documents/usi/**`, `.claude/skills/job-scraper/search-queries.template.md`,
`applications/**`, `.github/upstream-wontport.txt`, `tools/upstream_triage.py` +
its test, `tests/test_gate_configuration.py`.
