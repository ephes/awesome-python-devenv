"""Offline checks for the Python guide's verified upstream examples."""

from pathlib import Path
import re
import unittest


GUIDE = Path(__file__).resolve().parents[1] / "docs/python.md"


class PythonDocsTests(unittest.TestCase):
    # Verified against develop on 2026-11-07, not fetched during tests:
    # django-cast 5b4e9637658c477cb5107af56facd2a40062c84f
    # django-indieweb d0aac27e862d132d7df8e8ae2c1450e80fb1daed
    def test_example_python_floors_and_metadata_sources(self):
        examples = re.findall(
            r'\[(django-(?:cast|indieweb))\]\(([^)]+)\) declares '
            r'`requires-python = "([^"]+)"`', GUIDE.read_text(),
        )
        self.assertEqual(len(examples), 2)
        for name, url, requirement in examples:
            with self.subTest(project=name):
                self.assertEqual(requirement, ">=3.11")
                self.assertEqual(url, f"https://github.com/ephes/{name}/blob/develop/pyproject.toml")
        self.assertEqual({name for name, _, _ in examples}, {"django-cast", "django-indieweb"})
        self.assertNotIn(">=3.10", GUIDE.read_text())

    def test_library_lockfile_policies_and_audit_recipe(self):
        text = GUIDE.read_text()
        # Check the two distinct policies, including the executable audit entry
        # point, rather than blessing a universal committed-lock instruction.
        self.assertRegex(text, r"`django-cast` does not track `uv\.lock`")
        self.assertRegex(text, r"`django-indieweb` tracks \[`uv\.lock`\]\(")
        self.assertIn(
            "https://github.com/ephes/django-cast/blob/develop/docs/development.rst"
            "#setting-up-the-python-environment", text,
        )
        self.assertIn("https://github.com/ephes/django-indieweb/blob/develop/uv.lock", text)
        self.assertIn("uv sync\njust audit-dependencies", text)
        self.assertNotIn("both check in `uv.lock`", text)
        summary = text.split("## Summary\n", 1)[1]
        self.assertIn("repository's lockfile policy", summary)


if __name__ == "__main__":
    unittest.main()
