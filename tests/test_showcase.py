import io
import unittest
from contextlib import redirect_stdout

from scripts.showcase import run_showcase


class ShowcaseTests(unittest.TestCase):
    def test_showcase_demonstrates_blocker_repair_and_diff(self):
        output = io.StringIO()

        with redirect_stdout(output):
            code = run_showcase()

        text = output.getvalue()

        self.assertEqual(code, 0)
        self.assertIn("FIRST BLOCKER  handoff-receipt", text)
        self.assertIn("IMPROVED", text)
        self.assertIn("SHOWCASE PASS", text)


if __name__ == "__main__":
    unittest.main()
