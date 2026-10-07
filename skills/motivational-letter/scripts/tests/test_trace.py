"""Check synthetic CV traces through the command-line interface."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "check.py"


def entry(unit, category, citations=()):
    lines = [
        "## Entry",
        f"- Unit: {json.dumps(unit)}",
        f"- Category: {json.dumps(category)}",
    ]
    for source, excerpt in citations:
        lines.extend((
            f"- Source: {json.dumps(source)}",
            f"- Excerpt: {json.dumps(excerpt)}",
        ))
    return "\n".join(lines)


class CvTraceCliTests(unittest.TestCase):
    def run_trace(self, document, trace, profile="# Profile\n", *, extra_args=()):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            document_path = root / "cv.txt"
            trace_path = root / "trace.md"
            profile_path = root / "profile.md"
            if document is not None:
                document_path.write_text(document, encoding="utf-8")
            if trace is not None:
                trace_path.write_text(trace, encoding="utf-8")
            if profile is not None:
                profile_path.write_text(profile, encoding="utf-8")
            return subprocess.run(
                [
                    sys.executable, "-X", "utf8", str(SCRIPT), "trace",
                    str(document_path), "--document-type", "cv",
                    "--trace", str(trace_path), "--profile", str(profile_path),
                    *extra_args,
                ],
                cwd=folder, capture_output=True, text=True, encoding="utf-8",
            )

    def test_reports_each_non_empty_document_line_missing_from_the_trace(self):
        result = self.run_trace("Skills\n\nPython\n", entry("Skills", "heading"))

        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("Untraced units:", result.stdout)
        self.assertIn('document line 3: "Python"', result.stdout)
        self.assertNotIn('document line 2:', result.stdout)
        self.assertEqual(result.stderr, "")

    def test_reports_a_fact_entry_with_no_excerpt(self):
        result = self.run_trace("Built a release tool.\n", entry("Built a release tool.", "fact"))

        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("Facts with no excerpts:", result.stdout)
        self.assertIn('trace line 2: "Built a release tool."', result.stdout)
        self.assertNotIn("Untraced units:", result.stdout)

    def test_an_empty_excerpt_does_not_satisfy_a_fact_entry(self):
        trace = entry("Built a release tool.", "fact", (("profile.md", ""),))
        result = self.run_trace("Built a release tool.\n", trace)

        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("Facts with no excerpts:", result.stdout)
        self.assertNotIn("Excerpts not found:", result.stdout)

    def test_reports_an_excerpt_not_found_in_the_profile(self):
        trace = entry(
            "Built a release tool.", "fact",
            (("profile.md", "Built a deployment tool."),),
        )
        result = self.run_trace(
            "Built a release tool.\n", trace,
            "# Profile\nBuilt a release tool for one team.\n",
        )

        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("Excerpts not found:", result.stdout)
        self.assertIn('trace line 5: "Built a deployment tool."', result.stdout)
        self.assertNotIn("Facts with no excerpts:", result.stdout)

    def test_accepts_a_profile_excerpt_after_whitespace_normalisation(self):
        trace = entry(
            "Built a release tool.", "fact",
            (("profile.md", "Built a release tool for one team."),),
        )
        result = self.run_trace(
            "Built a release tool.\n", trace,
            "# Profile\nBuilt a release\n\ttool   for one team.\n",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Clean: every CV unit has a valid trace citation.", result.stdout)

    def test_accepts_heading_and_contact_entries_without_excerpts(self):
        trace = "\n\n".join((
            entry("Skills", "heading"),
            entry("candidate@example.test", "contact"),
        ))
        result = self.run_trace("Skills\ncandidate@example.test\n", trace)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("Facts with no excerpts:", result.stdout)

    def test_rejects_excerpts_from_each_forbidden_profile_region(self):
        profile = (
            "# Profile\n"
            "## Positions\nBuilt a release tool.\n"
            "## Voice profile\nWrites short sentences.\n"
            "## Never claim\nNever say led the migration.\n"
            "## Stories\nOutcome: [NEEDED] Ask for a measurable result.\n"
        )
        cases = (
            ("Writes short sentences.", "Excerpts from Voice profile:"),
            ("Never say led the migration.", "Excerpts from Never claim:"),
            ("Ask for a measurable result.", "Excerpts from [NEEDED] lines:"),
        )
        for excerpt, heading in cases:
            with self.subTest(excerpt=excerpt):
                trace = entry("Claim.", "fact", (("profile.md", excerpt),))
                result = self.run_trace("Claim.\n", trace, profile)

                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn(heading, result.stdout)
                self.assertIn(f'trace line 5: {json.dumps(excerpt)}', result.stdout)
                self.assertNotIn("Excerpts not found:", result.stdout)

    def test_reports_profile_history_and_other_disallowed_sources_separately(self):
        trace = "\n\n".join((
            entry(
                "Former claim.", "fact",
                (("profile-history.md", "Superseded claim."),),
            ),
            entry(
                "Company claim.", "fact",
                (("company.md", "Company statement."),),
            ),
        ))
        result = self.run_trace("Former claim.\nCompany claim.\n", trace)

        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("Profile history citations:", result.stdout)
        self.assertIn('trace line 4: "profile-history.md"', result.stdout)
        self.assertIn("Sources not allowed for cv:", result.stdout)
        self.assertIn('trace line 10: "company.md"', result.stdout)

    def test_reports_duplicate_and_stale_entries_separately(self):
        trace = "\n\n".join((
            entry("Skills", "heading"),
            entry("Skills", "heading"),
            entry("Old section", "heading"),
        ))
        result = self.run_trace("Skills\n", trace)

        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("Duplicate entries:", result.stdout)
        self.assertIn('trace line 6: "Skills"', result.stdout)
        self.assertIn("Stale entries:", result.stdout)
        self.assertIn('trace line 10: "Old section"', result.stdout)

    def test_missing_profile_source_is_an_explicit_input_error(self):
        result = self.run_trace("Skills\n", entry("Skills", "heading"), None)

        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("error: cannot read source profile.md", result.stderr)
        self.assertIn("profile.md", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_trace_help_states_that_citations_do_not_prove_accuracy(self):
        result = subprocess.run(
            [sys.executable, "-X", "utf8", str(SCRIPT), "trace", "--help"],
            capture_output=True, text=True, encoding="utf-8",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(
            "verifies that a citation exists, not that the document line is accurate",
            " ".join(result.stdout.split()),
        )


if __name__ == "__main__":
    unittest.main()
