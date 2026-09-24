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
