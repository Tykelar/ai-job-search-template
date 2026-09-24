# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Releases are vetted checkpoints of `master`. If you maintain a personalized fork,
prefer updating to a tagged release over pulling raw `master` (see
[SETUP.md, section 8](SETUP.md#8-pulling-upstream-updates-into-your-fork)). The
`framework_version` markers on methodology files tell you which of your customized
files a release touched; `python3 tools/check_upstream_updates.py` lists them with
per-file diff commands.

## [Unreleased]

### Added

- **`config/gates.md`** - user configuration holding every hard-gate value in one
  readable file outside the skills tree: work authorization, the Languages table with
  levels, the experience ceiling, and the authorized-relocation countries with base
  location and remote scope. It is now the single source of truth those gates read.
  `/setup` writes it on all three onboarding paths and `/sync-usi` keeps it in sync
  with the USI corpus.
- **`/rank` personalization check (Step 1a)** - the run stops when
  `04-job-evaluation.md` still holds placeholder tokens or a gate table in
  `config/gates.md` is unfilled. An unpersonalized framework used to score silently:
  placeholder skill areas and career goals produce plausible-looking numbers across
  60% of the weighting, and an empty gate table degrades that gate to a PASS on every
  posting.

### Changed

- **The four hard gates now execute exactly once, in `/rank` Step 2a.** Previously
  `/rank` ran three gates, `/apply` ran two, and the Eligibility Gate ran nowhere at
  all. `/scrape` runs none (its geography and body-language filters are collection
  filters, not gates) and `/apply` re-runs none - a cold posting handed straight to it
  is reported as **Ungated** at its Step 1c shortlist gate rather than being treated as
  gate-cleared. Gate order is fixed: eligibility, language, experience, location, with
  the first FAIL winning.
- **`04-job-evaluation.md` holds gate mechanisms only, no values.** Thresholds, country
  lists, and language levels moved to `config/gates.md`; CLAUDE.md,
  `01-candidate-profile.md`, and `search-queries.md` now point at it instead of
  restating it. Location dimension 4 is documented as the fourth hard gate, and its
  blanket relocation-is-a-deal-breaker rule - which contradicted a profile that
  authorizes relocation to named countries - is now authorized-list logic.
- **`/rank` hands off to `/apply` without asking it to re-evaluate.** The two specs
  contradicted each other: `/rank` told `/apply` to re-run its full Step 1 evaluation
  while `/apply` Step 1 forbade re-scoring a job `/rank` had scored. The triage verdict
  is now carried forward unchanged, and the depth `/apply` adds is company research
  after approval.
- **`/scrape` produces no applications.** Its route into the job-application-assistant
  drafting workflow is removed; a run ends at `/rank`, or at `/apply` for one named
  job. That path skipped the numbered application folder, `POSTING.md`, `/apply`'s
  validation gate, the reviewer pass, and the mandatory PDF/ATS verification. The
  skill's own drafting steps now use `applications/<NN>_<company>_<role>/` and the
  profile's CV filename slug, per CLAUDE.md's hard naming rules.
- **`/scrape` records geographic exclusions.** The geography skip reason was documented
  in the schema but written by no step; the geographic filter now writes it and Step 5
  reports the count, alongside the language-exclusion line.

### Fixed

- Language Gate documentation asserted that nothing in the framework tracked language
  requirements, which had been false since `/rank` began persisting its language-gate
  verdict. It now also separates the two different language checks: what the *role
  requires* (the gate) versus what language the *ad is written in* (`/scrape`'s
  collection filter).
- An `archived` status was named as a `seen_jobs.json` exit status in two prune rules
  but was absent from the schema enum and written by nothing; `evaluated` was in the
  enum and produced by nothing. Both removed.
- `04-job-evaluation.md` announced five scoring dimensions over a list of six.

### Upstream port

- **Part 0 - preflight & handoff setup** (fork tooling, no upstream code ported).
  Recorded a green baseline of every verification command in
  `docs/port-logs/part-00-baseline.txt` and installed the `handoff` skill
  (`.claude/skills/handoff`) so each part of the upstream port can close out with a
  handoff document. Installed once, not duplicated across skill roots — see the
  port plan's "skill roots are not one namespace" convention. See `docs/upstream-port-plan.md`.
- **Part 1 - portal CLIs: wholesale upstream refresh** (commit `9e12980`). All six
  portal CLIs (`freehire`, `jobbank`, `jobdanmark`, `jobindex`, `jobnet`, `linkedin`)
  replaced with `upstream/master` under `.agents/skills/` (Method A). Brings flag
  validation (unknown/single-dash/fractional flags now exit 1 with `UNKNOWN_FLAG` /
  `BAD_ARG` instead of being silently dropped), 429/5xx retry with backoff, request
  timeouts, detail/posted-date URL normalization, closed-posting detection, detail
  fallbacks, and the added `/scrape` contract fields, with their fixture tests
  (139 -> 312 CLI tests). Upstream refs: `3bfd525cc`, `fa8db56a9`, `c42806674`,
  `79cd383e5`, `6ef295bf7`, `3d296448b` (CLI half), `a30691213` (drops `applyUrl`),
  `c85640e30`, `b067928da`, `c7bd494f1`, `2edf8c41f`, `56f679e5c`, `17bc69869`,
  `04186b9a3`, `df7919cdf`, `7aba0b4a9`, `c844359ed`, `dab215073`, `c2cd71dde`,
  `f8c606fb3`, `bcba687fb`, `ba9b1d837`, `0883958d4`, `48965960d`, `71674d022`,
  `dd02c8248`. The take also carries `cffacfd` (#288) for the portal `SKILL.md`
  frontmatter: the four Danish demo portals now ship `enabled: false`, which matches
  this fork's Portuguese market (`linkedin`/`freehire` stay enabled). The `setup.md`
  half of `cffacfd` is a CUSTOM reconcile and lands in Part 11.
- **Part 2 — cross-portal contract, scoped `bun run`, CI CLI discovery** (commit
  `d696a88`). Adds `tests/test_scrape_contract.py`, which derives the `/scrape`
  Step 2 search-output contract (title, company, location, date, url) from
  `job-scraper/SKILL.md` and fails if any `.agents/skills/*-search` CLI stops
  emitting a field. `.claude/settings.json` now scopes the pre-approved
  `Bash(bun run:*)` to the six shipped portal CLIs and adds the
  `rank_state`/`job_key`/`verify_pdf`/`verify_layout` tool permissions;
  `tools/security_guards.py`'s allowlist mirrors it. CI gains a `discover-clis`
  job, so `cli-checks` derives its matrix from
  `.agents/skills/*/cli/package.json` and a portal added by `/add-portal` is
  typechecked and tested with no workflow edit. Upstream refs: `db8312948`
  (#344), `2d636c50b` (#396), `f658bb6f9` (#310).
- **Part 3 — salary tooling & UTF-8 stdout** (commit `4cd5c16`). Method A take of
  `salary_lookup.py`, `tools/convert_salary_excel.py`, and their three test files
  (all untouched `v1.4.0` copies), plus the new
  `tests/test_convert_salary_excel_integration.py`. Fixes `A.M.B.A.` dotted legal
  suffix normalization, null metadata/categories handling, count/index header
  corroboration across cells, dot-thousands and US/UK + Danish number forms
  (locale chosen by the last separator), compound count/index headers, the
  count/index pair fallback, and the privacy-suppression footnote. Both tools now
  reconfigure stdout/stderr to UTF-8 on entry, so non-Latin company names no
  longer crash a piped Windows run. Upstream refs: `7d00ec792`, `9833a5dcb`,
  `7f709eda5`, `621ce5ab3`, `1c19f6c45`, `968fb1bd7`, `b91c6125e`, `362ef6a52`,
  `ba4f2397a` (salary files portion; the remaining tools of that commit land in
  Parts 4 and 7, with the full `tests/test_tools_utf8_output.py` once all six
  tools exist).
- **Part 4 — PDF tooling & ATS verification stack** (commit `2a80e9e`). Method A
  take of `tools/verify_pdf.py`, `tests/test_verify_pdf.py` and
  `tests/test_latex_guidance.py`, plus the new `tools/verify_layout.py` and
  `tests/test_verify_layout.py`. `verify_pdf.py` now tries pypdf first (BSD,
  optional) and falls back to Poppler `pdftotext -layout -enc UTF-8`; it folds
  NFC and LaTeX's typographic substitutions (curly apostrophes, en/em dashes,
  no-break spaces) on both sides of `--contains`, and writes the raw text layer
  with `--dump-text`. `verify_layout.py` measures page geometry (mid-page holes,
  early page ends, footer collisions, orphaned/split entries) from Poppler
  `-bbox` and exits 2 with `skipped:` when the extractor cannot supply boxes.
  `/apply` Step 5b/5d, the 05/06 template guides, `CLAUDE.md`, `README.md`,
  `SETUP.md` and the CI LaTeX job were reconciled by hand (C): the new bookworm
  leg compiles on apt TeX Live 2022, and the text-layer guard asserts a
  template-mechanical token (`Tech stack:`, `Dear`). Fork deviations from the
  upstream A files: the `verify_layout.py` docstring escapes `\hypersetup` (no
  SyntaxWarning), a missing `pdfinfo` no longer fails a text-only check on the
  Git-for-Windows xpdf `pdftotext` path (`--pages` still fails loudly),
  `tests/test_gate_configuration.py` also asserts `verify_pdf.py`, and
  `tests/test_latex_guidance.py` strips `%` comments before matching (the
  template example documents the pitfall in a comment). Upstream
  refs: `cbd8a991a`, `1b65f7198`, `dea8140db`, `75c15eeec`, `73d52e099`,
  `b2545d512`, `c696b60b7`, `ba4f2397a` (the `07cec1f22` sentinel half is
  Part 13).

## [1.0.0] - 2026-07-22

First tagged release. This marks the framework as stable and gives forks a described
checkpoint to update against instead of a moving `master`. It is a baseline of what
already exists rather than a set of new changes; subsequent releases will document
what changed since the previous tag.

At this baseline the framework provides:

- **Application workflow** - a drafter/reviewer `/apply` pipeline (CV + cover letter),
  plus `/setup`, `/scrape`, `/rank`, `/interview`, `/outcome`, `/upskill`,
  `/expand`, `/html-report`, `/gmail-sync`, `/notion-sync`, `/add-portal`,
  `/add-template`, and `/reset`.
- **Portal search skills** - country-agnostic job-board CLIs (LinkedIn, freehire, and
  the Danish boards) in the portable Agent Skills format under `.agents/skills/`,
  discovered and orchestrated by `/scrape`, with an `enabled:` toggle for skipping
  portals.
- **Framework versioning** - `framework_version` markers on methodology files plus
  `tools/check_framework_version.py` (CI guard) and `tools/check_upstream_updates.py`
  (fork-side update preview).
- **Privacy and safety guards** - `.gitignore` protection for personal data, the
  `tools/security_guards.py` allowlist for `.gitignore` negations, and a CI policy of
  making no live portal requests.
- **Cross-runtime support** - a root `AGENTS.md` pointer so Codex and Antigravity can
  discover the portable portal skills, with Claude Code as the reference runtime.

[Unreleased]: https://github.com/MadsLorentzen/ai-job-search/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/MadsLorentzen/ai-job-search/releases/tag/v1.0.0
