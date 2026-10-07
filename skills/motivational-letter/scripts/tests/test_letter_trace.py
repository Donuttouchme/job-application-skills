"""Check synthetic letter traces through the command-line interface."""
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


class LetterTraceCliTests(unittest.TestCase):
    def run_trace(self, document, trace, *, sources=None):
        source_contents = {
            "profile.md": "# Profile\n",
            "company.md": "# Company\n",
            "motivation.md": "# Motivation\n",
            "search.md": "# Search constraints\n",
        }
        if sources:
            source_contents.update(sources)
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            document_path = root / "letter.txt"
            trace_path = root / "letter-trace.md"
            document_path.write_text(document, encoding="utf-8")
            trace_path.write_text(trace, encoding="utf-8")
            command = [
                sys.executable, "-X", "utf8", str(SCRIPT), "trace",
                str(document_path), "--document-type", "letter",
                "--trace", str(trace_path),
            ]
            for source_name, contents in source_contents.items():
                source_path = root / source_name
                if contents is not None:
                    source_path.write_text(contents, encoding="utf-8")
                command.extend((f"--{source_name.removesuffix('.md')}", str(source_path)))
            return subprocess.run(
                command, cwd=folder, capture_output=True, text=True, encoding="utf-8",
            )

    def test_dr_abbreviation_does_not_end_a_letter_sentence(self):
        sentence = "I spoke with Dr. Example about the role."
        result = self.run_trace(sentence, entry(sentence, "motivation"))

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Clean: every letter unit has a valid trace citation.", result.stdout)

    def test_common_german_and_english_abbreviations_do_not_end_sentences(self):
        for abbreviation in ("z. B.", "z. H.", "d. h.", "u. a.", "ca.", "Nr.",
                             "e.g.", "i.e.", "etc."):
            with self.subTest(abbreviation=abbreviation):
                first = f"The detail {abbreviation} remains part of this sentence."
                second = "This is the next sentence."
                trace = "\n\n".join((
                    entry(first, "motivation"),
                    entry(second, "closing"),
                ))
                result = self.run_trace(f"{first} {second}", trace)

                self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_letter_facts_may_cite_each_allowed_source(self):
        facts = (
            ("I built a release tool.", "profile.md", "Built a release tool."),
            ("The company makes widgets.", "company.md", "Makes widgets."),
            ("I want to improve releases.", "motivation.md", "Improve releases."),
            ("I can work part-time.", "search.md", "Part-time work is required."),
        )
        trace = "\n\n".join(
            entry(unit, "fact", ((source, excerpt),))
            for unit, source, excerpt in facts
        )
        result = self.run_trace(
            " ".join(unit for unit, _, _ in facts),
            trace,
            sources={source: f"# Synthetic\n{excerpt}\n" for _, source, excerpt in facts},
        )

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_salutation_and_closing_are_units_without_sentence_punctuation(self):
        salutation = "Dear Hiring Team,"
        body = "I want to improve releases."
        closing = "Kind regards"
        trace = "\n\n".join((
            entry(salutation, "salutation"),
            entry(body, "motivation"),
            entry(closing, "closing"),
        ))
        result = self.run_trace(f"{salutation}\n\n{body}\n\n{closing}\n", trace)

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_accepts_all_letter_non_fact_categories_without_excerpts(self):
        units = (
            ("Application", "heading"),
            ("candidate@example.test", "contact"),
            ("Dear Hiring Team,", "salutation"),
            ("I want to improve releases.", "motivation"),
            ("Kind regards", "closing"),
        )
        trace = "\n\n".join(entry(unit, category) for unit, category in units)
        document = "\n\n".join(unit for unit, _ in units)

        result = self.run_trace(document, trace)

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_missing_file_for_a_cited_letter_source_is_an_input_error(self):
        unit = "The company makes widgets."
        trace = entry(unit, "fact", (("company.md", "Makes widgets."),))

        result = self.run_trace(unit, trace, sources={"company.md": None})

        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("error: cannot read source company.md", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_missing_cited_source_is_an_input_error_even_with_an_empty_excerpt(self):
        unit = "The company makes widgets."
        trace = entry(unit, "fact", (("company.md", ""),))

        result = self.run_trace(unit, trace, sources={"company.md": None})

        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("error: cannot read source company.md", result.stderr)

    def test_profile_forbidden_regions_also_apply_to_letters(self):
        profile = (
            "# Profile\n"
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
                result = self.run_trace("Claim.", trace, sources={"profile.md": profile})

                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn(heading, result.stdout)

    def test_profile_history_is_never_allowed_for_a_letter(self):
        trace = entry(
            "Former claim.", "fact", (("profile-history.md", "Old claim."),),
        )
        result = self.run_trace("Former claim.", trace)

        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("Profile history citations:", result.stdout)


if __name__ == "__main__":
    unittest.main()
