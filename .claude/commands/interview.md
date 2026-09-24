# /interview - Prepare for an Interview on a Tracked Application

You are preparing the user for a real, scheduled interview on one of their applications. The frameworks for this already exist - `07-interview-prep.md` (STAR examples, tough questions, questions to ask, roleplay protocol) and the Company Research Checklist in `04-job-evaluation.md` - and the `/outcome` archive records which stage the user is at and what earlier stages surfaced. This command wires them together into a stage-specific prep pack and an optional mock interview.

`/apply` optimizes what the company reads; `/interview` optimizes what the company hears. The bridge between them is consistency: the interviewer has read the submitted CV and cover letter, so everything prepared here must match what those documents claim.

Follow these steps **in order**.

---

## Step 0: Parse Input

`$ARGUMENTS` may contain a company name (optionally with a role), e.g. `/interview acme`.

- **With an argument:** match against `job_search_tracker.csv` rows (case-insensitive on company, then role). One match → proceed. Several → list and ask. None → this application isn't tracked; suggest `/outcome <company>` to register it first, or accept the posting and role details directly if the user wants to prep anyway.
- **Without an argument:** list tracker rows whose status suggests a live process — an open status per the **Tracker status vocabulary** in `/outcome` (`interview`, `offer`, or recently `applied`; `drafted` is open but nothing was sent, so it never qualifies) — and ask which one. If the tracker is empty, ask for the company, role, and posting.

v1 preps for a **specific application**. Generic no-target practice is out of scope - if asked, prep against a real tracked application instead.

---

## Step 1: Load the Application Context

1. **The archive** (started by `/apply`, maintained by `/outcome`): `documents/applications/<company>_<role>/`
   - `job_posting.md` - the exact posting the user applied to
   - `cv_draft.tex` and `cover_letter.tex` - what was actually submitted. **These are what the interviewer read**; every talking point must be consistent with their claims.
   - `outcome.md` - the stage reached so far and any recorded feedback from earlier stages. Feedback from stage N is the highest-value input for stage N+1 prep.
2. **The application folder** (written by `/apply`): `applications/<NN>_<company>_<role>/`, or `applications/INTERVIEW_<NN>_<company>_<role>/` if a previous `/interview` run already flagged it. Locate it with a glob that tolerates both prefixes - `applications/*<company>*/` - and note the exact folder name; Step 3 writes the prep pack here and Step 3b renames the folder.
3. **Fallbacks** (the application may predate `/outcome`): posting via WebFetch on the tracker row's `source` URL, or ask the user to paste it; CV via `applications/*<company>*/CV_<CVNameSlug>_<company>*.tex` and cover letter via `applications/*<company>*/CL_<CVNameSlug>_<company>_*.tex`. State plainly which context is missing rather than guessing - and suggest `/outcome <company>` to build the archive for next time. If no application folder exists at all (application made outside `/apply`), fall back to saving the pack in `documents/applications/<company>_<role>/`, skip Step 3b, and say so.
4. **Ask the user what this interview is** (skip anything `outcome.md` already records): stage (phone screen / technical / case / final round), date, format (phone, video, onsite), and who is interviewing (names and titles, if known).
5. **Read the frameworks once** - do not re-read them in later steps:
   - `.claude/skills/job-application-assistant/07-interview-prep.md`
   - `.claude/skills/job-application-assistant/01-candidate-profile.md`
   - `.claude/skills/job-application-assistant/02-behavioral-profile.md`
   - `.claude/skills/job-application-assistant/04-job-evaluation.md`

---

## Step 2: Research the Company (Interview-Focused)

Execute the Company Research Checklist that `04-job-evaluation.md` defines: company website (mission, values, recent news), review sites, LinkedIn (team size, recent hires), and media coverage (growth, restructuring, workplace issues).

Additions for interview purposes:

- **Interviewer angle:** if interviewer names are known (from Step 1 or the tracker's `contact_person`), look up their public professional profile. A hiring manager probes team fit and motivation; a senior engineer probes technical depth; HR probes the CV timeline. Note the likely angle per interviewer - do not speculate beyond public information.
- **Conversation hooks:** 2-3 recent, verifiable company specifics (a product launch, a stated strategic priority) the user can reference naturally in answers and in the "why this company" moment.

**Verify before using:** every company claim that will appear in the prep pack must be independently confirmed via WebFetch/WebSearch - same rule the repo applies to cover-letter claims. An unverified "fact" delivered confidently in an interview is worse than no fact. On a 403, retry with browser headers per `.claude/skills/job-application-assistant/09-web-research.md` rather than dropping to search snippets; a snippet is a lead, not a source.

---

## Step 3: Build the Prep Pack

Assemble a stage-appropriate prep document with these sections:

### 1. Likely questions
Derive from four sources, in priority order:
1. **Recorded feedback from earlier stages** (`outcome.md`) - anything flagged, doubted, or left unresolved will come back
2. **The fit evaluation's gaps** - the requirements where the profile is weakest are the likeliest probes. For each, prepare an honest bridge answer per `07`'s "You don't have [X]" pattern: acknowledge, connect adjacent experience, show the learning path. **Never prepare an answer that invents experience.**
3. **The posting's stated requirements** - competency by competency
4. **The stage type** - phone screens get motivation and timeline questions; technical rounds get the posting's stack; final rounds get values, salary, and "any reservations" questions

### 2. STAR answer mapping
Match the ready-made STAR examples in `07-interview-prep.md` to the likely questions using their "Use for" tags. Then:
- For likely questions **no existing STAR example covers**, draft a new STAR answer grounded strictly in facts from `01-candidate-profile.md` - profile facts arranged into S/T/A/R, not embellished. Include these drafts in the prep pack; offer to append them to `07-interview-prep.md` only if the user explicitly approves.
- If `/setup` left incomplete STAR stubs relevant to this role, surface them: the user should fill in the details before the interview.

### 3. Consistency brief
A short list of the specific claims the submitted CV and cover letter make (achievements, numbers, skills emphasized) that the interviewer is most likely to probe. The rule stated plainly: **no claim in the room that isn't on the paper, and every claim on the paper must be defensible in depth.**

### 4. Tough questions, customized
The relevant entries from `07`'s tough-question list with per-application answers - "Why this company specifically?" must use the verified hooks from Step 2, never a generic line.

### 5. Questions to ask
Pick 4-6 from `07`'s categories, customized to the research and the stage: role and team questions at screens, tech and growth questions at technical rounds, culture and leadership questions by the final round (that is the last chance to detect a deal-breaker). Cut any question the research already answers publicly - asking it signals you didn't look.

### 6. Logistics
The phone/video tips from `07` when the format calls for them, plus date and interviewer names as a header.

Save the pack to the application folder found in Step 1, as `interview_prep_<stage>.md` - alongside the CV and cover letter that were actually submitted, so everything about this application lives in one place. One file per stage, so earlier packs remain as history. `applications/**/interview_*.md` is gitignored, so the pack stays personal even though the application folders themselves are not ignored wholesale. Present the pack in chat as well - the file is the artifact, the conversation is the delivery.

---

## Step 3b: Flag the Application Folder

Rename the application folder so the interviewing applications are identifiable at a glance in a directory listing:

```
applications/<NN>_<company>_<role>/  ->  applications/INTERVIEW_<NN>_<company>_<role>/
```

Rules:

- **The sequence number is preserved, never changed.** The `INTERVIEW_` prefix is added in front of the existing `<NN>_` prefix; the rest of the folder name is untouched. Creation-order numbering still holds - `/apply` computes the next number by reading the `<NN>_` prefix and ignoring any `INTERVIEW_` in front of it.
- **Idempotent.** If the folder is already prefixed (a second or third round on the same application), leave the name as it is - never stack a second `INTERVIEW_`.
- **Never renamed back.** The flag records that the application reached an interview stage; `/outcome` recording a rejection does not remove it.
- **The files inside are untouched.** `CV_<CVNameSlug>_<company>_<role>.tex/.pdf`, `CL_...`, and `POSTING.md` keep their names - nothing sent to an employer ever carries the flag or the number.
- Use `git mv` if any file in the folder is tracked (`applications/*/job_posting.md` can be), plain `mv` otherwise.
- **Fix the references the rename breaks:** update the `cv_file` and `cover_letter_file` columns of this application's `job_search_tracker.csv` row to the new path, and any folder path mentioned in that row's `notes`. Do the rename before writing the prep pack's header so the pack points at the new path too.
- If Step 1 found no application folder, skip this step and note it in the chat delivery.

---

## Step 4: Offer a Mock Interview

Ask if the user wants to practice. If yes, run the roleplay **in this conversation** following the Roleplay Guidelines in `07-interview-prep.md` exactly: warm-up first, then role-specific technical questions, 1-2 behavioral questions tied to the posting's competencies, and one tough question or curveball. After each answer, give brief feedback - what worked, what to sharpen, and which STAR example from the pack would have served better.

Calibrate feedback against `02-behavioral-profile.md`: coach toward the user's natural register, not a generic ideal - the same voice-consistency rule the `/apply` reviewer applies to cover letters.

---

## Step 5: Close the Loop

End with:

> Good luck. After the interview, run `/outcome <company>` to log the stage and any feedback - it sharpens the prep for the next round, and once the process resolves it feeds your fit-framework calibration via `/setup`.

If Step 3 drafted new STAR answers the user approved for keeps, remind them those were appended to `07-interview-prep.md` (or offer again if they deferred).

---

## Important Rules

1. **Consistency with the submitted documents.** The interviewer read the archived CV and cover letter; prep must never contradict them or coach claims beyond them.
2. **Honesty on gaps.** Weak matches get bridge answers (acknowledge → adjacent experience → learning path), never invented experience. Same rule as everywhere else in this repo.
3. **Verified research only.** Company specifics go in the pack only after independent confirmation. Interviewer notes stick to public professional information.
4. **Stage-appropriate prep.** A phone screen pack and a final-round pack are different documents; recorded feedback from earlier stages takes priority over generic question lists.
5. **Write only to the application folder.** The prep pack lands in `applications/INTERVIEW_<NN>_<company>_<role>/`, next to the submitted documents; the only other writes are this application's `job_search_tracker.csv` row (paths broken by the rename) and, on explicit request, user-approved STAR examples appended to `07-interview-prep.md`. Framework and profile files are otherwise never edited, and the `documents/applications/<company>_<role>/` archive is **read-only** here - `/outcome` owns it.
