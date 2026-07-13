import datetime as dt
import importlib.util
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "init_week.py"
SPEC = importlib.util.spec_from_file_location("init_week", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class InitWeekTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "AGENTS.md").write_text("# rules", encoding="utf-8")

        skill = self.root / ".agents" / "skills" / "managing-weekly-group-meetings"
        templates = skill / "templates"
        templates.mkdir(parents=True)
        (templates / "weekly-readme.md").write_text(
            "# {{ISO_WEEK}} 每周工作记录\n", encoding="utf-8"
        )
        (templates / "task-dashboard.md").write_text(
            "# 阶段任务清单\n", encoding="utf-8"
        )

    def tearDown(self):
        self.temp.cleanup()

    def test_iso_week_for_date(self):
        self.assertEqual(MODULE.iso_week_for_date(dt.date(2026, 7, 13)), "2026-W29")

    def test_initialize_creates_expected_structure(self):
        created = MODULE.initialize(self.root, "2026-W29")
        self.assertTrue((self.root / "weekly/2026-W29/tasks").is_dir())
        self.assertTrue((self.root / "weekly/2026-W29/temporary").is_dir())
        self.assertTrue((self.root / "weekly/2026-W29/deliverables").is_dir())
        self.assertTrue((self.root / "completed-projects").is_dir())
        self.assertTrue((self.root / "TASKS.md").is_file())
        self.assertIn("weekly/2026-W29/README.md", created)

    def test_initialize_does_not_overwrite_existing_files(self):
        dashboard = self.root / "TASKS.md"
        dashboard.write_text("keep me", encoding="utf-8")
        readme = self.root / "weekly/2026-W29/README.md"
        readme.parent.mkdir(parents=True)
        readme.write_text("existing", encoding="utf-8")

        MODULE.initialize(self.root, "2026-W29")

        self.assertEqual(dashboard.read_text(encoding="utf-8"), "keep me")
        self.assertEqual(readme.read_text(encoding="utf-8"), "existing")

    def test_invalid_week_is_rejected(self):
        with self.assertRaises(ValueError):
            MODULE.initialize(self.root, "2026-29")


if __name__ == "__main__":
    unittest.main()
