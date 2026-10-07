"""Synthetic fixtures only; sensitive-looking values are assembled at runtime."""

import contextlib
import importlib.util
import io
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "personal_data_guard.py"
SPEC = importlib.util.spec_from_file_location("personal_data_guard", SCRIPT)
guard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(guard)


class ContentTests(unittest.TestCase):
    def assert_blocked(self, content, reason):
        self.assertIn((2, reason), guard.findings("fixture.md", "safe\n" + content))

    def test_home_paths(self):
        for prefix in ("C:\\Users\\", "c:/users/", "/home/", "/Users/"):
            with self.subTest(prefix=prefix):
                self.assert_blocked(prefix + "fixture-user/file", "personal home path")

    def test_home_placeholders(self):
        for content in ("%USERPROFILE%\\file", "~/file", "$HOME/file",
                        "/home/<name>/file", "C:\\Users\\<name>\\file"):
            with self.subTest(content=content):
                self.assertEqual([], guard.findings("fixture.md", content))

    def test_email(self):
        self.assert_blocked("fixture@" + "synthetic-domain.ch", "email address")

    def test_email_allow_list(self):
        domains = (
            "example.com", "EXAMPLE.ORG", "example.net", "docs.example.com",
            "fixture.example", "fixture.test", "fixture.invalid",
            "fixture.users.noreply.github.com",
        )
        for domain in domains:
            with self.subTest(domain=domain):
                self.assertEqual([], guard.findings("fixture.md", "fixture@" + domain))

    def test_email_allow_list_boundaries(self):
        for domain in ("notexample.com", "example.com.evil.ch",
                       "fixture.users.noreply.github.com.evil.ch"):
            with self.subTest(domain=domain):
                self.assert_blocked("fixture@" + domain, "email address")

    def test_international_phones(self):
        for number in ("+99 " + "00 000 00 00", "+9" + "00000000",
                       "+999" + "00000000"):
            with self.subTest(number=number):
                self.assert_blocked(number, "international phone number")

    def test_phone_allow_list_and_short_number(self):
        for number in ("+41 79 123 45 67", "+99 " + "00000"):
            self.assertEqual([], guard.findings("fixture.md", number))

    def test_phone_placeholder_with_extra_digits_is_blocked(self):
        self.assert_blocked("+41 79 123 45 67" + " 00", "international phone number")

    def test_ahv(self):
        self.assert_blocked("756." + "0000.0000.00", "Swiss AHV number")

    def test_tokens(self):
        for prefix in ("ghp_", "gho_", "github_pat_", "sk-", "sk-proj-"):
            with self.subTest(prefix=prefix):
                self.assert_blocked(prefix + "x" * 40, "access token")
        self.assert_blocked("AKIA" + "X" * 16, "access token")

    def test_blocked_paths_case_insensitive(self):
        for filename in ("docs/Personal_Data/fixture.md", "DOCS/personal_DATA/nested/f",
                         ".scratch/fixture.md", ".SCRATCH/nested/f",
                         "./.scratch/f", "docs\\Personal_Data\\f"):
            with self.subTest(filename=filename):
                self.assertEqual([(1, "private directory")], guard.findings(filename, ""))

    def test_similar_paths_are_allowed(self):
        for filename in ("docs/Personal_Data-example/f", ".scratchpad/f",
                         "tools/personal_data_guard.py"):
            self.assertEqual([], guard.findings(filename, "safe"))

    def test_local_literals_are_case_insensitive_not_regexes(self):
        patterns = [re.compile(re.escape("fixture.*literal"), re.IGNORECASE)]
        self.assertEqual([(1, "local personal pattern")],
                         guard.findings("f.md", "FIXTURE.*LITERAL", patterns))
        self.assertEqual([], guard.findings("f.md", "fixture other literal", patterns))


class StagedFileTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.original_cwd = Path.cwd()
        self.addCleanup(os.chdir, self.original_cwd)
        os.chdir(self.temp.name)
        self.git("init", "--quiet")

    def git(self, *args):
        return subprocess.run(["git", *args], check=True,
                              capture_output=True).stdout.decode("utf-8").strip()

    def stage(self, filename, content):
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        self.git("add", "--", filename)

    def run_guard(self, *filenames):
        output = io.StringIO()
        with contextlib.redirect_stderr(output):
            result = guard.main(list(filenames))
        return result, output.getvalue()

    def test_missing_local_file_is_silent(self):
        self.stage("fixture.md", "safe")
        self.assertEqual((0, ""), self.run_guard("fixture.md"))

    def test_local_patterns_file_comments_blanks_and_masking(self):
        path = Path(self.git("rev-parse", "--git-path", "info/personal-patterns"))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# comment\n\n  # another comment\nfixture.*literal\n",
                        encoding="utf-8")
        self.stage("fixture.md", "# comment\nsafe\nFIXTURE.*LITERAL")
        result, output = self.run_guard("fixture.md")
        self.assertEqual(1, result)
        self.assertIn("fixture.md:3: local personal pattern [redacted]", output)
        self.assertNotIn("FIXTURE.*LITERAL", output)

    def test_reads_staged_secret_not_clean_working_tree(self):
        secret = "ghp_" + "x" * 40
        self.stage("fixture.md", "safe\n" + secret)
        Path("fixture.md").write_text("safe", encoding="utf-8")
        result, output = self.run_guard("fixture.md")
        self.assertEqual(1, result)
        self.assertIn("fixture.md:2: access token [redacted]", output)
        self.assertNotIn(secret, output)
        self.assertNotIn("x" * 40, output)

    def test_ignores_unstaged_secret(self):
        self.stage("fixture.md", "safe")
        Path("fixture.md").write_text("ghp_" + "x" * 40, encoding="utf-8")
        self.assertEqual((0, ""), self.run_guard("fixture.md"))

    def test_blocked_staged_path(self):
        self.stage("docs/Personal_Data/fixture.md", "safe")
        result, output = self.run_guard("docs/Personal_Data/fixture.md")
        self.assertEqual(1, result)
        self.assertIn("docs/Personal_Data/fixture.md:1: private directory [redacted]", output)

    def test_multiple_staged_files_and_spaces_in_filename(self):
        self.stage("first fixture.md", "safe")
        self.stage("second.md", "756." + "0000.0000.00")
        result, output = self.run_guard("first fixture.md", "second.md")
        self.assertEqual(1, result)
        self.assertIn("second.md:1: Swiss AHV number [redacted]", output)

    def test_no_filenames_is_noop(self):
        self.assertEqual((0, ""), self.run_guard())


if __name__ == "__main__":
    unittest.main()
