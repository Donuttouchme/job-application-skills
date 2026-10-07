"""Check finished synthetic documents through the command-line interface."""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "check.py"


class BannedPhraseCliTests(unittest.TestCase):
    def run_check(self, text, *, language="en", document_type="letter", script=SCRIPT):
        with tempfile.TemporaryDirectory() as folder:
            document = Path(folder) / "document.txt"
            if text is not None:
                document.write_text(text, encoding="utf-8")
            return subprocess.run(
                [sys.executable, "-X", "utf8", str(script), "phrases", str(document),
                 "--document-type", document_type, "--language", language],
                cwd=folder, capture_output=True, text=True, encoding="utf-8",
            )

    def test_banned_phrase_is_blocking_case_insensitively_with_its_line(self):
        result = self.run_check("I tested the build.\nA PROVEN TRACK RECORD.\n")

        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("Banned phrases:", result.stdout)
        self.assertIn('line 2: "proven track record"', result.stdout)
        self.assertEqual(result.stderr, "")

    def test_shared_list_covers_english_german_and_cv_phrases_for_both_document_types(self):
        text = (
            "I AM WRITING TO EXPRESS MY KEEN INTEREST IN this work.\n"
            "MIT GROSSEM INTERESSE HABE ICH IHRE STELLENANZEIGE GELESEN.\n"
            "ORCHESTRATED releases.\n"
            "VERANTWORTUNG FÜR DIE GANZHEITLICHE Prüfung.\n"
        )
        for document_type in ("cv", "letter"):
            for language in ("en", "de-ch"):
                with self.subTest(document_type=document_type, language=language):
                    result = self.run_check(text, document_type=document_type, language=language)
                    self.assertEqual(result.returncode, 1, result.stderr)
                    for finding in (
                        'line 1: "I am writing to express my keen interest in"',
                        'line 2: "Mit grossem Interesse habe ich Ihre Stellenanzeige gelesen"',
                        'line 3: "orchestrated"',
                        'line 4: "Verantwortung für die ganzheitliche"',
                    ):
                        self.assertIn(finding, result.stdout)

    def test_sharp_s_is_blocking_only_in_de_ch_documents(self):
        for document_type in ("cv", "letter"):
            for language, exit_code in (("en", 0), ("de-ch", 1)):
                with self.subTest(document_type=document_type, language=language):
                    result = self.run_check(
                        "A synthetic heading.\nDie Straße ist kurz.\n",
                        language=language, document_type=document_type,
                    )
                    self.assertEqual(result.returncode, exit_code, result.stderr)
                    if language == "de-ch":
                        self.assertIn("Swiss orthography:", result.stdout)
                        self.assertIn('line 2: "ß"', result.stdout)
                    else:
                        self.assertNotIn("Swiss orthography:", result.stdout)

    def test_missing_banned_list_fails_explicitly_even_for_a_clean_document(self):
        with tempfile.TemporaryDirectory() as folder:
            installed_script = Path(folder) / "check.py"
            shutil.copyfile(SCRIPT, installed_script)
            result = self.run_check("I tested the build.\n", script=installed_script)

        self.assertEqual(result.returncode, 2)
        self.assertIn("error: cannot read banned phrase list", result.stderr)
        self.assertIn("banned-phrases.txt", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(result.stdout, "")

    def test_clean_documents_exit_zero_with_a_clear_result_from_another_directory(self):
        for document_type in ("cv", "letter"):
            for language, text in (
                ("en", "I tested the build.\nI fixed two test failures.\n"),
                ("de-ch", "Ich habe den Build getestet.\nFreundliche Grüsse\n"),
            ):
                with self.subTest(document_type=document_type, language=language):
                    result = self.run_check(text, document_type=document_type, language=language)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertIn("Clean: no banned phrases or Swiss orthography findings.", result.stdout)
                    self.assertEqual(result.stderr, "")

    def test_reports_every_phrase_occurrence_and_orthography_finding_without_stopping_early(self):
        result = self.run_check(
            "PROVEN TRACK RECORD and proven track record.\n\n"
            "ROBUST work in der Straße.\nProven track record.\n", language="de-ch",
        )

        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(result.stdout.count('line 1: "proven track record"'), 2)
        self.assertIn('line 3: "robust"', result.stdout)
        self.assertIn('line 3: "ß"', result.stdout)
        self.assertIn('line 4: "proven track record"', result.stdout)
        self.assertNotIn("Clean:", result.stdout)

    def test_missing_document_fails_explicitly_instead_of_reporting_a_clean_check(self):
        result = self.run_check(None)

        self.assertEqual(result.returncode, 2)
        self.assertIn("error: cannot read document", result.stderr)
        self.assertIn("document.txt", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(result.stdout, "")

    def test_wrapping_a_phrase_does_not_hide_it_and_reports_its_starting_line(self):
        result = self.run_check("A heading.\nA PROVEN\n\tTRACK   RECORD.\n")

        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn('line 2: "proven track record"', result.stdout)

    def test_installed_script_reads_literal_phrases_beside_it_and_ignores_blank_list_lines(self):
        with tempfile.TemporaryDirectory() as folder:
            installed_script = Path(folder) / "check.py"
            shutil.copyfile(SCRIPT, installed_script)
            (Path(folder) / "banned-phrases.txt").write_text(
                "\nsynthetic (stock) phrase\n\n", encoding="utf-8",
            )
            clean = self.run_check("A synthetic stock phrase.\n", script=installed_script)
            blocked = self.run_check("A SYNTHETIC (STOCK) PHRASE.\n", script=installed_script)

        self.assertEqual(clean.returncode, 0, clean.stderr)
        self.assertEqual(blocked.returncode, 1, blocked.stderr)
        self.assertIn('line 1: "synthetic (stock) phrase"', blocked.stdout)

    def test_capital_sharp_s_is_also_blocking_only_in_de_ch(self):
        for language, exit_code in (("en", 0), ("de-ch", 1)):
            with self.subTest(language=language):
                result = self.run_check("DIE STRAẞE IST KURZ.\n", language=language)
                self.assertEqual(result.returncode, exit_code, result.stderr)
                if language == "de-ch":
                    self.assertIn('line 1: "ß"', result.stdout)


if __name__ == "__main__":
    unittest.main()
