---
framework_version: 2.4.0
---

# CV Template and Tailoring Guide (compact style, verbatim-first selection)

## The model: select and order; reword bullets only within bounds

CVs are built by **verbatim-first selection** from a curated master:

- **Master CV (LaTeX):** `applications/main_example.tex` — the FULL curated content bank
  rendered in the compact style. It is simultaneously the LaTeX skeleton and the verbatim
  content source. It compiles to several pages by design; only tailored CVs have the 2-page rule.
- **Master content bank (Markdown):** `applications/master_cv.md` — the same content in
  Markdown. The `.tex` master must always match it line for line; if they diverge, the
  Markdown bank wins. (If you maintain a source corpus, fix the wording there and regenerate
  both; otherwise fix them together by hand.)
- A tailored CV is `main_example.tex` **copied, then reduced**: keep the blocks relevant to
  the role, delete the rest, reorder within sections. Projects, education
  lines, and work headers stay **character-for-character identical** to the master.
- **Experience bullets are verbatim-first**: keep the master's wording unless a light
  rephrase genuinely improves role fit (tightening, aligning to the posting's
  terminology). A rephrased bullet must trace to one specific master bullet and keep its
  facts, metrics, and scope exact — no new claims, no escalated numbers, no merged
  achievements. Verbatim remains the default when rephrasing adds nothing.
- Structurally wrong wording is a master problem: fix it in the master (and in its source,
  if you keep one), regenerate — never patch the tailored copy.
- **Two surfaces are composed per role, never copied:** the **About Me paragraph** (fully
  generative) and the **Core Competencies** section (5-7 bullets written for the posting,
  from master material — see below). Core Competencies **replaces** the master's Skills
  section; a tailored CV never prints both. The CV header carries no headline — name +
  fixed contact line only.

**Output file:** `applications/<NN>_<company>_<role>/CV_<CVNameSlug>_<company>_<role>.tex`
(`<CVNameSlug>` is the `CV filename slug` set in your CLAUDE.md Identity section.)

## Template: compact single-column (Carlito)

The visual style is a hyper-optimized compact layout: Carlito (Calibri-metric) body, 20pt
blue name, ALL-CAPS blue section headings with a thin full-width rule, one-line
work/education headers, dense bullets. Single column — ATS-safe by construction, and the
contact line prints the email as literal text.

Semantic commands (defined in the master's preamble — a tailored CV never needs new ones):

```latex
\cvjob{Job Title, Company}{Sep 2025 - Jun 2026}   % one-line bold work header (has built-in \needspace)
\cvcontext{One-line italic context under a work header.}
\cvedu{Degree}{Institution}{Sep 2024 - Jul 2026}  % one bold education line
\cvedusub{Thesis: Title (grade)}                  % italic thesis/final-project line under a \cvedu
\cvskill{Category}{item · item · item}            % one row of the MASTER-ONLY skills bank
\cvcomp{Label}{Concrete items. What it buys.}     % one Core Competencies bullet (inside itemize)
\cvproject{Title}{Tech stack}{Description.}       % project entry - stack arg is MANDATORY, see below
\cvmoreprojects{short list. Portfolio link.}      % mandatory closing "Also built:" line
\cvrule                                           % bare separator rule (used above About Me, which has no heading)
```

### Bullets must never start with a bare `[`

`\item [text]` is parsed as `\item`'s **optional label**, so the text renders in the
left margin and clips off the page instead of appearing in the bullet. Start every
`\item` with a word or a command (`\textbf{...}`) - never with a bare `[`. This has
bitten the example master once; the compile-and-inspect loop below is what catches it
(a clipped bullet shows as a fragment in `pdftotext -layout` output, e.g. `onsibility
bullet.`).

### The mandatory project tech-stack line

`\cvproject` takes **three** arguments. Argument 2 renders as an italic one-line
`Tech stack: a · b · c` subtitle between the bold title and the description. Rules:

- **Never omit it.** Every project entry has one; a two-argument `\cvproject` is a
  template error, not a shorthand.
- **One line, always.** Keep the whole line under ~95 characters including the
  `Tech stack: ` label. If it would wrap, **drop items** (least role-relevant first) —
  never shrink the font, never let it run to two lines. Verify in the compiled PDF, not
  the `.tex`.
- **Items come from the master's stack line for that project**, trimmed and reordered for
  the role. Selecting a subset is expected; inventing a tool that isn't in the master is a
  fidelity violation.
- **Separator is ` · `** (the same middot used in skill rows), not commas.
- **Never repeat the stack in the title or description.** The stack line owns the tooling,
  so titles carry no `(Python + Ollama)` suffix and descriptions carry no "built with X,
  Y, and Z" prose. Descriptions say *what the thing is and what came of it*; the stack
  line says what it was built with.

### The four-project floor (hard)

**Selected Projects always carries at least four full `\cvproject` entries**, not counting
the `Also built:` line. A reader who only sees three detailed entries under-reads the
breadth. Consequences:

- **Four is a floor, not a target.** Five or six is better when the page holds them.
- **The `Also built:` line does not count toward the floor.** It is a catch-all, not a
  fourth entry.
- **A fourth project is never the fix for an overfull page 2.** Cut a competency bullet
  (down to five), trim a value clause, or drop an optional Other-Relevant-Information
  bullet first. Projects fall below four only if every one of those is exhausted — and a
  build that lands there should be re-checked, because it usually means the competency
  bullets ran to three lines each.
- Deselecting a project still moves it into the `Also built:` line rather than deleting it.

### The mandatory "Also built:" closing line

The section is titled **Selected Projects**, so it has to read as a selection rather than as
the whole inventory. `\cvmoreprojects` closes it with a one-line catch-all naming what was
left out. Rules:

- **Never omit it.** Every tailored CV has one, directly after the last `\cvproject`.
- **One rendered line** (two at the absolute limit). Compress each cut project to a short
  descriptor, not its full title: "a client cybersecurity assessment", not
  "Cybersecurity Assessment & Footprinting (Client Project)".
- **Only master projects.** Every item names a project that exists in
  `applications/master_cv.md` and was *not* selected above. Never a project the master does
  not carry, and never one already listed above it.
- **Order by role relevance**, highest first — the reader skims the first two items only.
- **Close with the portfolio link** (`More at \href{[YOUR_PORTFOLIO_URL]}{[YOUR_PORTFOLIO_SHORT_URL]}.`)
  so the reader has somewhere to go; delete the link if you have no portfolio.

**Compile with lualatex** (fontspec + system Carlito font; pdflatex cannot load it). Run
from `applications/` with `-output-directory` into the application folder:

```bash
cd applications && lualatex -interaction=nonstopmode -output-directory=<NN>_<company>_<role> <NN>_<company>_<role>/CV_<CVNameSlug>_<company>_<role>.tex
```

Expected output: `Output written on ... (2 pages, ...)`. Any other page count is a failure.

## Fixed 2-page structure

The master carries a `\newpage` before Core Competencies. Tailored CVs keep it, making the
page break deterministic:

- **Page 1:** Header (name + bold contact line, no headline) · About Me (separator rule,
  no heading) · Education · Work Experience · Languages
- **Page 2:** Core Competencies · Selected Projects · Other Relevant Information

There is **no standalone References section**. Its line —
`[YOUR_REFERENCES_LINE]`, e.g. `Formal recommendation letter from [REFERENCE_NAME], available on request; additional references on request.`
— is the mandatory first bullet of Other Relevant Information, so the CV closes on that
section and never prints referee names or contact details.

The master's `\section{Skills}` block is **deleted outright** in a tailored CV — it is the
evidence bank Core Competencies is composed from, not a section the CV prints.

Selection budgets (tune to fill both pages, never overfull):

| Section | Tailored budget |
|---|---|
| Most recent role bullets | 5-6, ordered for the role |
| Second role bullets | 3-4 |
| Earlier roles | 2-3 each |
| Education | one line per degree with its `\cvedusub` thesis/final-project lines; drop the optional or early rows unless the posting calls for them |
| Core Competencies | 5-7 `\cvcomp` bullets, composed for the posting, highest-relevance first (see below) |
| Skills bank | 0 rows — the section is deleted, never printed alongside Core Competencies |
| Selected Projects | **4 minimum**, 4-6 typical, highest-relevance first (the project entries carry the full descriptions; the Education sub-lines carry title + grade). Every entry needs its mandatory one-line `Tech stack:` subtitle, and the section closes with the mandatory `\cvmoreprojects` line, which does **not** count toward the four |
| Other Relevant Information | the mandatory references bullet first, then 2-4 optional bullets; always the last section |

Replacing 6-9 dense skill rows with 5-7 competency bullets frees roughly a third of page 2;
that budget goes to Selected Projects (4-6 rather than 3-5) and the `Also built:` line. The
compile loop is the arbiter, not the table — except for the four-project floor, which the
compile loop does not get to overrule.

### Measured starting selection (use this, not the middle of the ranges)

The ranges above are what is *allowed*; this is what actually **filled two pages** in a
calibrated build (lualatex/Carlito, standard geometry):

| Page | Selection that filled it |
|---|---|
| Page 1 | 3-sentence About Me · two education lines · **5-6** most-recent-role bullets · **3-4** second-role bullets · **2-3** earlier-role bullets · Languages |
| Page 2 | **5-6** competency bullets held to **2** rendered lines each · **4** project entries · a 1-line `Also built:` line · **4** Other Relevant Information bullets (references bullet + 3 optional) |

Start here and adjust by one line at a time. **Grow into an empty page; never plan to trim
an overfull one.** Restoring the best line you left out is a single compile, while cutting
an overfull page takes several rounds, because removing one line changes which line is now
the lowest-scoring. Calibration notes worth keeping:

- Seven competency bullets at three lines each pushed page 2 onto a third page on their
  own. Six is the practical ceiling, and only at two rendered lines each.
- A project entry costs about five rendered lines. Four of them fit **only** if the
  competency bullets are held to two lines each — so budget the competency bullets around
  the four projects, not the other way round. If page 2 is tight, the competency section
  gives way first: six two-line bullets, then five.
- "Two lines each" means two **full** lines. A bullet running one line plus a three-word
  stub costs the same vertical space as a two-line bullet while saying a third less, so the
  widow sweep in the compile loop is what makes these numbers hold in practice.
- These numbers assume the standard compact template. A custom template registered through
  `/add-template` needs its own calibration row.

**Structural rules:** fixed contact line; no headline; Education is one bold line per degree
plus its italic thesis/final-project sub-line; always include a Selected Projects section
carrying **at least four full `\cvproject` entries**, every entry with its mandatory
one-line `Tech stack:` subtitle and the section closing with `\cvmoreprojects` (which does
not count toward the four);
no "Internship" qualifier on a role title unless it was literally an internship;
date ranges use an **ASCII hyphen**, never an en-dash (see "Date fields must be ASCII
ranges" below); **no em-dashes anywhere**; the references bullet never prints referee names
or contact details — only the fixed available-on-request line.

## About Me (fully generative)

Write it fresh for the role, anchored in the master's paragraph as the voice/quality
baseline (adapt, don't invent a new story):

- Facts from the master/profile only; your voice as recorded in `03-writing-style.md`
  (typically direct, technical, grounded); no em-dashes; no keyword stuffing.
- One short paragraph, 2-3 sentences plus the mandatory closing sentence, kept verbatim:
  `Get to know me better \href{[YOUR_PORTFOLIO_URL]}{here}!` (delete the closing sentence
  if you have no portfolio).
- Lead with the most role-relevant point, then close with the broader profile
  (systems-level breadth) as context.
- **No widow line.** In the compiled PDF, the paragraph's last rendered line must not be a
  three-word stub. Because the mandatory closing sentence is fixed verbatim, trim the
  sentence before it until the paragraph closes on a full line.
- Match the role's lead content to whichever master material fits the posting's domain
  best; lead with the most recent role's relevant outcomes where they apply, name **Claude
  Code** (or your own agentic tooling) where agentic work is genuinely part of the story,
  and respect any framing-suppression rule you configured in `03-writing-style.md`.

## Core Competencies (the second composed surface)

This section replaces the raw Skills bank. It opens page 2, so it is the first thing a
reader sees after the experience — it has to answer "what is this person for?" in six lines.

**How to build it:**

- **Reorder and emphasize based on the role. Use bold category labels.**
- **List 5-7 key competencies in bullet format, tailored to the specific job.** For each
  competency, briefly explain how it adds value to the position.
- **Use the posting's own core term in the matching bullet's bold label when it truthfully
  applies** — ATS and skim-reading hiring managers match literally, and "MLOps" in a
  heading outperforms a paraphrase like "ML Deployment".

**How it renders here** (the compact-template adaptation):

```latex
\section{Core Competencies}

\begin{itemize}
\cvcomp{Label}{Concrete items, comma-separated. Then one clause on what it buys this role.}
...
\end{itemize}
```

- **Body = concrete first, value second.** Name specific skills, frameworks, tools, and
  metrics — the same items the Skills bank carries — then close with a short clause on what
  the competency does for *this* role. Abstract competency prose with no tool names in it
  is a failed bullet: it loses the ATS surface the Skills bank used to provide.
- **Two rendered lines per bullet** (three only where the content genuinely earns it),
  comma-separated (not the ` · ` middot, which belongs to skill rows and stack lines).
- **No widow lines.** A bullet whose last rendered line carries three words or fewer — or
  fills less than about a quarter of the text width — is spending a full line height on
  almost nothing. Page 2 typically holds five or six competency bullets, so two widows cost
  roughly a whole project entry. Fix by **cutting words from the value clause** until the
  bullet closes on the previous line: drop hedges ("which allows me to", "helping to"),
  collapse "X and Y" pairs to whichever is stronger, and cut the value clause to a single
  short phrase. Never fix a widow by padding the bullet out to fill the line, and never by
  deleting a concrete tool name — those carry the keywords, so the value clause is always
  what gives way. Widows are only visible in the compiled PDF; check every bullet there.
- **Cover the tooling.** Between them, the 5-7 bullets must carry the concrete tool and
  language names a parser looks for. With the Skills bank gone, these bullets are the CV's
  whole keyword surface, so check coverage here deliberately in step 5d rather than
  assuming it.
- **Every named tool, method, and metric must trace** to `applications/master_cv.md` /
  `applications/main_example.tex` or to `01-candidate-profile.md`. What is free is the
  composition: which items group under which label, how the label is worded, what the value
  clause says, and the ordering. What is not free is inventing a tool, escalating a metric,
  or claiming a depth of experience the master does not support.
- **No overlap with a selected experience bullet's own claim.** If a competency bullet and
  an experience bullet would say the same thing in the same words, the competency bullet is
  the one that changes — it abstracts, the experience bullet stays concrete evidence.
- **Respect your framing rules** in `03-writing-style.md` / CLAUDE.md: a suppressed framing
  never leads and never carries the suppressed words.
- The master's worked example (`applications/main_example.tex`) is **calibration, not
  content** — a tailored CV rewrites all of its bullets for its own posting.

## Experience bullet ordering (default / general)

By default lead with the bullets that carry the posting's domain and the largest measured
impacts, then demote implementation-detail bullets toward the bottom. For a role that
explicitly leads on one competency (e.g. a dedicated Test Automation role), reorder so that
competency leads — the order follows the role, but for general roles the impact bullets
never displace the most relevant domain evidence. Ordering is always a selection operation;
any wording change stays within the bounded-rephrasing rule.

## Keywords: matched by composition and selection

**Core Competencies is now the primary keyword surface**, since the dense Skills bank is no
longer printed. A posting term is covered by (a) putting it in a competency label where it
truthfully applies, (b) naming it among that bullet's concrete items — drawn from the
master's skill rows — or (c) surfacing the master experience bullet or project that already
carries it. A selected experience bullet may be lightly retermed to the posting's exact
vocabulary where truthfully equivalent (the posting's tool/method name for the master's
synonym — never a claim the master line does not make); project entries and headings stay
verbatim. The About Me and cover letter (generative) are where the posting's vocabulary can
be engaged directly, where truthfully applicable.
If the profile genuinely has a skill but no master line carries it, that is a
master-coverage gap: report it, add it to the master (and its source), then regenerate.

## Section headings must match the CV's language

Section names (`Education`, `Work Experience`, `Languages`, `Core Competencies`,
`Selected Projects`, `Other Relevant Information`) are literal text in the
template, as is the bold `Also built:` lead-in that `\cvmoreprojects` prints (About Me has
no printed heading). If the CV
language (see `CV language` in the candidate profile) were ever not English, translate all
of them, not just body prose — check explicitly during verification. (Skill-row and bullet
content is verbatim master content and only changes language if the master does.)

## Compile-and-inspect loop (MANDATORY)

1. Compile (command above); confirm exactly 2 pages.
2. Read the PDF via the Read tool and inspect both pages:
   - Page 1 ends with Languages; page 2 starts with Core Competencies and ends with
     Other Relevant Information, whose first bullet is the references line. The Skills
     bank and any standalone References section must be gone entirely.
   - No orphaned `\cvjob` header (built-in `\needspace` normally prevents it).
   - **Count the project entries: four or more.** Three is a failure even if the page
     otherwise looks right.
   - The `Also built:` line is present and renders on **one line** (two at the limit).
   - **Widow sweep on the composed surfaces.** Look at the last rendered line of every
     `\cvcomp` bullet and of the About Me paragraph: any that carries three words or fewer
     gets its value clause cut until the text closes on the previous line. Two widows on
     page 2 are about one project entry's worth of space. This is a per-build check, not an
     optional polish — a first draft usually produces two or three of them.
   - No overfull page (content pushed past the `\newpage` or onto page 3) and no page
     ending awkwardly early.
2a. If the count is wrong, prefer **growing** over shrinking. Starting from the measured
   selection above, a page that ends early is one compile away from correct; an overfull
   page needs the cut re-scored after every removal. When a line is borderline, leave it
   out of the first build and add it back if the page ends early.
3. Fix by **selection**: deselect whole lines (least relevant first) from an overfull
   page; restore the highest-relevance omitted line to a sparse page. Never fix layout by
   rewording to shrink, tightening spacing, or changing geometry.
   `\enlargethispage{2-3\baselineskip}` is allowed for a near-miss trailing spill on
   page 2. Core Competencies is the one exception to "never reword to fit": dropping a
   competency bullet from 7 to 6, or trimming its value clause, is a legitimate fit tool
   because the section is composed rather than selected — never below 5 bullets, and never
   by deleting the concrete tool names that carry the keywords.
   **Widow-trimming is confined to the two composed surfaces** (About Me, Core
   Competencies). Master-traced text — experience bullets, project titles and descriptions,
   education lines — is never reworded to kill a widow; a short trailing line there is
   fixed by selection or simply lived with, because fidelity outranks density. (The
   `Tech stack:` and `Also built:` lines have their own one-line rules above.)
   **Space reclaimed from widows is spent, not banked**: two recovered lines is most of a
   fifth project entry or an extra Other-Relevant-Information bullet. A page 2 that now
   ends early is a page 2 with room for more evidence.
   On an overfull page 2,
   **Core Competencies gives way before Selected Projects does**: trim value clauses, then
   drop to five bullets, then cut an optional Other-Relevant-Information bullet, and only
   then consider a project — which still may not take the section below four entries.
4. Selection scoring when cutting: keep lines that (a) hit THIS posting's keywords and
   responsibilities, (b) carry unique claims (the quantified impact bullets survive),
   (c) the cover letter depends on. Cut the lowest-scoring line first, regardless of
   section. When a claim appears in **both** a competency bullet and an experience
   bullet, cut the competency version — the experience bullet is the more concrete
   evidence.

## ATS parseability

After the layout passes, verify the text layer (`pdftotext -layout`; poppler is optional —
if missing, skip the mechanical check with a warning):

- **Contact details as literal text** — the template prints the email address as text (no
  icons); it must survive extraction.
- **No garbled output** — no `(cid:NNN)` or `�` characters (Carlito under lualatex embeds
  a clean Unicode mapping).
- **Reading order** — single-column, so extraction order matches visual order; verify
  section headings appear in sequence.
- **Keyword coverage** — match the posting's required/preferred terms against the
  extraction, in the posting's language. Coverage improves by composition and selection
  (see above); genuine gaps stay visible and are never stuffed. Check this **harder than
  before**: with the Skills bank no longer printed, a term the CV used to pick up for free
  from a 20-item skill row now only lands if a competency bullet names it.
- **Date ranges parse** — every `\cvjob` and `\cvedu` entry in the extraction shows a start
  *and* an end separated by an ASCII hyphen (see below).

### Date fields must be ASCII ranges (confirmed ATS import failure)

This one is worth knowing about because it fails **silently**. A CV that passes every other
check in this section — clean extraction, no `(cid:)` markers, contact details intact,
correct reading order — can still have its dates dropped on import. In a real Workday
resume import, a CV lost the end date of a short role and failed to import **any**
education entry, forcing manual re-entry. Nothing about the PDF or its text layer looked
wrong.

Two independent causes, both easy to avoid:

1. **An en-dash in a date field does not parse as a range.** Many parsers split date ranges
   only on an ASCII hyphen (U+002D); a literal `–` (U+2013), or the `--` ligature LaTeX
   renders as one, reaches the text layer as a character they do not split on, so they see
   no range at all. Write the date argument of `\cvjob` / `\cvedu` with a single hyphen:

   ```latex
   \cvjob{Job Title, Company}{Sep 2025 - Jun 2026}   % parses
   \cvjob{Job Title, Company}{Sep 2025 – Jun 2026}   % en-dash, may not
   ```

   This applies to the **date argument only**. Keep `--`/`–` everywhere it is
   typographically correct in prose, for example a numeric range like `EUR 600k--1M`.

2. **A bare single year gives the parser no end date.** A short role written as
   `{2020}` imports as a start date with nothing to close it. Use an explicit range, with
   months where the role ran under a year (`Jul 2020 - Sep 2020`). Where a genuine range
   exists, use it even when a single year would be factually accurate. Never invent a start
   date; a lone graduation year is fine, just expect it to be typed in by hand.
