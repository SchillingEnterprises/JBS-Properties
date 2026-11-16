"""Source-level security guardrails for the legacy ASP.NET MVC controllers."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
CONTROLLERS = ROOT / "Controllers"


class ControllerAccessControlTests(unittest.TestCase):
    def test_every_controller_requires_authentication_by_default(self):
        files = sorted(CONTROLLERS.glob("*Controller.cs"))
        self.assertTrue(files, "Expected the application controllers to be present")
        unprotected = []
        for path in files:
            source = path.read_text(encoding="utf-8-sig")
            declaration = re.search(r"(?m)^\s*public\s+class\s+\w+Controller\b", source)
            if declaration is None:
                unprotected.append(f"{path.name}: controller declaration not found")
                continue
            preceding = source[:declaration.start()]
            if not re.search(r"\[Authorize(?:\([^]]*\))?\]\s*$", preceding):
                unprotected.append(f"{path.name}: missing class-level Authorize attribute")
        self.assertEqual(unprotected, [])

    def test_every_post_action_requires_antiforgery_validation(self):
        failures = []
        for path in sorted(CONTROLLERS.glob("*Controller.cs")):
            source = path.read_text(encoding="utf-8-sig")
            post_count = len(re.findall(r"\[HttpPost\b", source))
            anti_forgery_count = len(re.findall(r"\[ValidateAntiForgeryToken\]", source))
            if post_count != anti_forgery_count:
                failures.append(
                    f"{path.name}: {post_count} POST actions but "
                    f"{anti_forgery_count} anti-forgery attributes"
                )
        self.assertEqual(failures, [])

    def test_property_controller_remains_protected(self):
        source = (CONTROLLERS / "DwellingsController.cs").read_text(encoding="utf-8-sig")
        self.assertRegex(source, r"(?m)^\s*\[Authorize\]\s*public\s+class\s+DwellingsController")
        for action in ("Create", "Edit", "DeleteConfirmed"):
            with self.subTest(action=action):
                pattern = r"(?s)\[HttpPost[^]]*\]\s*\[ValidateAntiForgeryToken\]\s*public\s+ActionResult\s+" + action + r"\b"
                self.assertRegex(source, pattern)

    def test_property_map_key_is_not_committed_to_the_view(self):
        view = (ROOT / "Views" / "Dwellings" / "Details.cshtml").read_text(encoding="utf-8-sig")
        self.assertNotRegex(view, r"AIza[0-9A-Za-z_-]{30,}")
        self.assertIn("GOOGLE_MAPS_BROWSER_API_KEY", view)
        self.assertIn('alt="Street view preview', view)

    def test_property_archive_contains_no_embedded_provider_credentials(self):
        archive = (ROOT / "App_Data" / "property.json").read_text(encoding="utf-8-sig")
        self.assertNotRegex(archive, r"AIza[0-9A-Za-z_-]{30,}")
        self.assertNotIn("zws-id=", archive)

    def test_activity_controller_remains_protected(self):
        source = (CONTROLLERS / "EntriesController.cs").read_text(encoding="utf-8-sig")
        self.assertRegex(source, r"(?m)^\s*\[Authorize\]\s*public\s+class\s+EntriesController")
        self.assertEqual(len(re.findall(r"\[HttpPost\b", source)),
                         len(re.findall(r"\[ValidateAntiForgeryToken\]", source)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
