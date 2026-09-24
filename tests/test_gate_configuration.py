"""The four hard gates: one set of values, one execution point.

Before this was pinned, gate values were restated in CLAUDE.md, the profile file
and the framework file (which also shipped a "requires relocation: FAIL" rule
contradicting a profile that authorizes relocation), and the gates themselves ran
in two places with different memberships - `/rank` ran three, `/apply` ran two,
and the Eligibility Gate ran nowhere at all. These tests hold the collapsed
design: every value lives in config/gates.md, and Step 2a of `/rank` is the only
place a gate executes.
"""

import re
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
GATES = REPO / "config" / "gates.md"
RANK = REPO / ".claude" / "commands" / "rank.md"
APPLY = REPO / ".claude" / "commands" / "apply.md"
SCRAPER = REPO / ".claude" / "skills" / "job-scraper" / "SKILL.md"
ASSISTANT = REPO / ".claude" / "skills" / "job-application-assistant" / "SKILL.md"
FRAMEWORK = REPO / ".claude" / "skills" / "job-application-assistant" / "04-job-evaluation.md"
CLAUDEMD = REPO / "CLAUDE.md"

GATE_NAMES = ("eligibility", "language", "experience", "location")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def in_template_state(text: str) -> bool:
    """The stock template ships all four gate blocks unfilled and says so; /setup
    removes the marker. A file that keeps the marker while some blocks are filled
    is half-configured, which the filled-state checks below still reject."""
    return "[PLACEHOLDER]" in text


class GateConfigurationFile(unittest.TestCase):
    def test_config_file_exists_outside_the_skills_tree(self):
        self.assertTrue(
            GATES.is_file(),
            "config/gates.md must exist: it is the single source of truth /rank Step 1.6 reads",
        )

    def test_all_four_gates_are_configured(self):
        text = read(GATES).lower()
        for gate in GATE_NAMES:
            self.assertIn(
                gate,
                text,
                f"config/gates.md must configure the {gate} gate",
            )

    def test_config_holds_the_experience_ceiling_as_a_number(self):
        text = read(GATES)
        if in_template_state(text):
            self.assertIn(
                "**[N]**",
                text,
                "the unfilled template must keep the documented [N] ceiling placeholder",
            )
            return
        self.assertRegex(
            text,
            r"Ceiling \(years\)\s*\|\s*\*\*\d+\*\*",
            "the ceiling must be a single configured number, not prose",
        )

    def test_config_carries_no_unfilled_placeholders(self):
        """An unfilled gate degrades to a silent PASS - /rank Step 1a stops on this."""
        text = read(GATES)
        if in_template_state(text):
            # Template state is legitimate only while every gate block is unfilled.
            for token in (
                "[YOUR_CITIZENSHIP_AND_WORK_AUTHORIZATION]",
                "[LANGUAGE_1]",
                "**[N]**",
                "[RELOCATION_COUNTRIES]",
            ):
                self.assertIn(
                    token,
                    text,
                    "template state must leave every gate block unfilled",
                )
            return
        leftovers = re.findall(r"\[[A-Z_]{4,}\]", text)
        self.assertEqual([], leftovers, f"unfilled placeholder tokens in config/gates.md: {leftovers}")

    def test_config_states_where_the_gates_run(self):
        text = read(GATES)
        self.assertIn(
            "Where the gates run",
            text,
            "config/gates.md must state which command executes the gates",
        )


class SingleSourceOfTruth(unittest.TestCase):
    def test_framework_defines_mechanisms_and_defers_values(self):
        text = read(FRAMEWORK)
        self.assertIn(
            "config/gates.md",
            text,
            "04-job-evaluation.md must read its gate values from config/gates.md",
        )

    def test_framework_does_not_hardcode_the_relocation_verdict(self):
        """The old dimension-4 rule failed every relocation posting, contradicting
        a profile that authorizes relocation to a named list of countries."""
        self.assertNotIn(
            "Requires relocation: FAIL",
            read(FRAMEWORK),
            "relocation is FAIL only outside the authorized-countries list in config/gates.md",
        )

    def test_claude_md_does_not_restate_gate_values(self):
        text = read(CLAUDEMD)
        self.assertNotRegex(
            text,
            r"stated minimum required experience is \*\*\d+\+ years\*\*",
            "the ceiling number must live only in config/gates.md",
        )
        self.assertIn(
            "config/gates.md",
            text,
            "CLAUDE.md must point at the gate configuration instead of restating it",
        )


class SingleExecutionPoint(unittest.TestCase):
    def test_rank_runs_all_four_gates_in_a_fixed_order(self):
        text = read(RANK)
        self.assertIn(
            "eligibility → language → experience → location",
            text,
            "/rank must fix the order the four gates run in, so the first FAIL is deterministic",
        )
        for gate in GATE_NAMES:
            self.assertIn(
                f'"{gate}"',
                text,
                f"/rank's vetoed shape and skip_reason vocabulary must cover {gate}",
            )

    def test_rank_reads_gate_inputs_from_the_config_file(self):
        text = read(RANK)
        self.assertIn("config/gates.md", text, "/rank Step 1 must read the gate configuration")
        self.assertIn(
            "four gate inputs",
            text,
            "/rank must forward all four gate inputs into every scoring agent's prompt",
        )

    def test_apply_runs_no_gates_and_reports_cold_jobs_as_ungated(self):
        text = read(APPLY)
        self.assertIn(
            "`/apply` runs no hard gates.",
            text,
            "/apply must not re-run gates that /rank already executed",
        )
        self.assertIn(
            "Ungated",
            text,
            "a cold posting has never been gated; /apply must say so at its Step 1c gate",
        )

    def test_apply_does_not_rescore_ranked_jobs(self):
        self.assertIn(
            "do not re-gate a job `/rank` already handled",
            read(APPLY),
            "/apply must carry the triage verdict rather than re-deriving it",
        )

    def test_rank_hands_off_without_asking_apply_to_re_evaluate(self):
        """/rank used to tell /apply to re-run the full Step 1 evaluation while
        /apply's own Step 1 forbade exactly that."""
        text = read(RANK)
        self.assertNotIn(
            "re-running the full Step 1 evaluation",
            text,
            "the handoff must not contradict /apply Step 1's no-re-scoring rule",
        )
        self.assertIn(
            "does not re-score and does not re-gate",
            text,
            "/rank must state that /apply carries its verdict forward unchanged",
        )

    def test_scrape_runs_no_gates(self):
        text = read(SCRAPER)
        self.assertIn(
            "runs **no hard gates**",
            text,
            "/scrape collects postings; gating from a search snippet is not gating",
        )


class ScrapeProducesNoApplications(unittest.TestCase):
    def test_scrape_routes_to_rank_not_into_the_drafting_workflow(self):
        text = read(SCRAPER)
        self.assertIn(
            "never route into the **job-application-assistant** drafting workflow from here",
            text,
            "that path skips the numbered folder, POSTING.md, the 1c gate, the reviewer and PDF verification",
        )
        self.assertIn(
            "It never produces an application",
            text,
            "/scrape's scope boundary must be stated where the run ends",
        )

    def test_assistant_skill_uses_the_numbered_folder_and_slug(self):
        """The skill's drafting steps wrote applications/<company>_<role>/ with a
        hardcoded name slug, violating CLAUDE.md's hard numbering rule."""
        text = read(ASSISTANT)
        self.assertNotIn(
            "applications/<company>_<role>/CV_<CVNameSlug>_",
            text,
            "drafting must use applications/<NN>_<company>_<role>/ and the profile's CV filename slug",
        )
        self.assertIn(
            "applications/<NN>_<company>_<role>/CV_<CVNameSlug>_<company>_<role>.tex",
            text,
            "the skill must name the same paths /apply Step 1b produces",
        )


class SetupWritesTheGateConfigOnEveryPath(unittest.TestCase):
    """config/gates.md is written on all three onboarding paths.

    Path A reads a documents folder and Path B a single CV; neither carries work
    authorization or an experience ceiling, so both must ask. When only Path C
    collected the gate inputs, a Path A onboarding finished with two gate blocks
    empty and /rank refused to run.
    """

    SETUP = REPO / ".claude" / "commands" / "setup.md"

    def test_setup_generates_the_config_file(self):
        text = read(self.SETUP)
        self.assertIn(
            "config/gates.md",
            text,
            "/setup must write the gate configuration, not just the skill files",
        )

    def test_every_path_collects_all_four_gate_inputs(self):
        text = read(self.SETUP)
        for phrase in (
            "Work authorization",
            "Experience ceiling",
            "Authorized countries",
            "proficiency levels",
        ):
            self.assertIn(
                phrase,
                text,
                f"/setup must collect '{phrase}' - an unasked gate input leaves a block unfilled",
            )
        self.assertIn(
            "four hard-gate questions",
            text,
            "Path B must reuse Path A's gate questions rather than skipping them",
        )

    def test_setup_does_not_point_language_levels_at_the_framework_file(self):
        """The levels live in config/gates.md; 04-job-evaluation.md holds only the mechanism."""
        self.assertNotIn(
            "feeds the Language Gate in `04-job-evaluation.md`",
            read(self.SETUP),
            "a stale pointer here is where /setup writes the levels into the wrong file",
        )


class NoGhostStatuses(unittest.TestCase):
    """`archived` was named as an exit status in both prune rules but was absent
    from the schema enum and written by nothing."""

    def test_archived_is_not_referenced_as_a_status(self):
        for path in (RANK, SCRAPER):
            self.assertNotIn(
                "`archived`",
                read(path),
                f"{path.name} must not name a status nothing writes",
            )


class OneVerificationChecklist(unittest.TestCase):
    """CLAUDE.md owns the pass/fail criteria; /apply Step 5 owns procedure and fixes.

    The two used to carry overlapping checkbox lists - page count, widows, orphaned
    headers, (cid:) markers, reading order - while /apply Step 6 also said to report
    against CLAUDE.md's list. Nothing detected them diverging.
    """

    def test_apply_restates_no_pass_fail_criteria(self):
        checkboxes = [
            line for line in read(APPLY).splitlines() if line.startswith("- [ ]")
        ]
        self.assertEqual(
            [],
            checkboxes,
            "the criteria live in CLAUDE.md; /apply must reference them, not restate them",
        )

    def test_claude_md_still_holds_the_criteria(self):
        text = read(CLAUDEMD)
        self.assertIn("### Compiled PDF verification", text)
        self.assertIn("### ATS & keyword verification", text)
        self.assertGreater(
            len([l for l in text.splitlines() if l.startswith("- [ ]")]),
            30,
            "CLAUDE.md must remain the full checklist both paths report against",
        )

    def test_apply_points_at_both_criteria_sections(self):
        text = read(APPLY)
        for section in ("*Compiled PDF verification*", "*ATS & keyword verification*"):
            self.assertIn(
                section,
                text,
                f"/apply Step 5 must name CLAUDE.md's {section} section as its criteria",
            )

    def test_apply_keeps_the_procedure(self):
        """Deduplicating criteria must not strip the how-to: compile commands,
        extraction, and the keyword-coverage table stay in /apply."""
        text = read(APPLY)
        for fragment in ("verify_pdf.py", "pdftotext -layout", "lualatex", "xelatex", "Keyword coverage"):
            self.assertIn(fragment, text, f"/apply must retain the {fragment} procedure")


class PersonalizationCheck(unittest.TestCase):
    def test_rank_stops_when_the_framework_is_still_a_template(self):
        text = read(RANK)
        self.assertIn(
            "Personalization check",
            text,
            "/rank must verify the framework was personalized before scoring against it",
        )
        self.assertIn(
            "YOUR_PRIMARY_SKILLS",
            text,
            "the check must name the placeholder tokens it looks for",
        )
        self.assertIn(
            "Do not rank a partial pool",
            text,
            "an unpersonalized framework must stop the run, not degrade it silently",
        )


if __name__ == "__main__":
    unittest.main()
