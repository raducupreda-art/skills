import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from unlock import unlock

LOCKED = "---\nname: a\ndescription: d\ndisable-model-invocation: true\n---\n\nbody\n"
OPEN = "---\nname: b\ndescription: d\n---\n\nSet `disable-model-invocation: true` to lock.\n"


class Unlock(unittest.TestCase):
    def tree(self, files):
        root = pathlib.Path(tempfile.mkdtemp())
        for rel, text in files.items():
            path = root / rel / "SKILL.md"
            path.parent.mkdir(parents=True)
            path.write_text(text)
        return root

    def test_listed_skill_can_be_called_by_the_model(self):
        root = self.tree({"engineering/a": LOCKED})
        unlock(root, ["a"])
        self.assertEqual(
            (root / "engineering/a/SKILL.md").read_text(),
            "---\nname: a\ndescription: d\n---\n\nbody\n",
        )

    def test_skill_not_listed_stays_locked(self):
        root = self.tree({"engineering/a": LOCKED, "productivity/c": LOCKED})
        unlock(root, ["a"])
        self.assertEqual((root / "productivity/c/SKILL.md").read_text(), LOCKED)

    def test_text_in_the_body_is_left_alone(self):
        root = self.tree({"engineering/a": LOCKED, "engineering/b": OPEN})
        unlock(root, ["a"])
        self.assertEqual((root / "engineering/b/SKILL.md").read_text(), OPEN)

    def test_a_skill_missing_upstream_fails_loud(self):
        root = self.tree({"engineering/a": LOCKED})
        with self.assertRaisesRegex(SystemExit, "gone"):
            unlock(root, ["a", "gone"])

    def test_a_listed_skill_already_open_fails_loud(self):
        root = self.tree({"engineering/b": OPEN})
        with self.assertRaisesRegex(SystemExit, "b"):
            unlock(root, ["b"])


if __name__ == "__main__":
    unittest.main()
