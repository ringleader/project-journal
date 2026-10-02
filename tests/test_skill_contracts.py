"""Contract checks for the instruction files shipped by project-journal.

These tests do not try to evaluate model wording. They protect the few
observable capabilities that motivated the skill updates: follow-on work,
honest freshness reporting, and context-quality notes.
"""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


def skill_text(name: str) -> str:
    return (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")


def frontmatter(text: str) -> str:
    match = re.match(r"\A---\r?\n(.*?)\r?\n---", text, re.DOTALL)
    if not match:
        raise AssertionError("skill is missing YAML frontmatter")
    return match.group(1)


class SkillContractsTest(unittest.TestCase):
    def test_all_skills_have_identity_and_tool_contract(self) -> None:
        for name in ("log", "brief", "orient"):
            metadata = frontmatter(skill_text(name))
            self.assertRegex(metadata, rf"(?m)^name:\s*{name}\s*$")
            self.assertRegex(metadata, r"(?m)^description:\s*\|\s*$")
            self.assertRegex(metadata, r"(?m)^allowed-tools:\s*$")

    def test_orient_preserves_and_executes_follow_on_directives(self) -> None:
        text = skill_text("orient")
        self.assertIn("## Invocation contract", text)
        self.assertIn("If a follow-on directive is present", text)
        self.assertIn("If no follow-on directive is present", text)
        self.assertIn("use the applicable plan-execution workflow", text)
        self.assertIn("file modification time", text)

    def test_brief_preserves_follow_on_and_context_quality(self) -> None:
        text = skill_text("brief")
        self.assertIn("## Invocation contract", text)
        self.assertIn("write the handoff first", text)
        self.assertIn("## Context quality", text)
        self.assertIn("When journal entries conflict", text)
        self.assertIn("In a monorepo", text)

    def test_readme_documents_the_follow_on_examples(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("/orient and then execute ROADMAP.md", readme)
        self.assertIn("/brief then run the test suite", readme)
        self.assertIn("Context quality", readme)


if __name__ == "__main__":
    unittest.main()
