"""Source-level security and presentation guardrails for the legacy ASP.NET MVC application."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
CONTROLLERS = ROOT / "Controllers"
VIEWS = ROOT / "Views"
DWELLING_VIEWS = VIEWS / "Dwellings"


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
        view = (DWELLING_VIEWS / "Details.cshtml").read_text(encoding="utf-8-sig")
        self.assertNotRegex(view, r"AIza[0-9A-Za-z_-]{30,}")
        self.assertIn("GOOGLE_MAPS_BROWSER_API_KEY", view)
        self.assertIn('alt="Street view preview', view)
        self.assertIn('role="status"', view)

    def test_property_archive_contains_no_embedded_provider_credentials(self):
        archive = (ROOT / "App_Data" / "property.json").read_text(encoding="utf-8-sig")
        self.assertNotRegex(archive, r"AIza[0-9A-Za-z_-]{30,}")
        self.assertNotIn("zws-id=", archive)

    def test_legacy_property_card_has_no_provider_credentials_or_invalid_model_pair(self):
        partial = (VIEWS / "Properties" / "CardPartical.cshtml").read_text(encoding="utf-8-sig")
        self.assertNotRegex(partial, r"AIza[0-9A-Za-z_-]{30,}")
        self.assertNotIn("zws-id=", partial)
        self.assertEqual(len(re.findall(r"(?m)^\s*@model\b", partial)), 1)
        self.assertIn("GOOGLE_MAPS_BROWSER_API_KEY", partial)

    def test_activity_controller_remains_protected(self):
        source = (CONTROLLERS / "EntriesController.cs").read_text(encoding="utf-8-sig")
        self.assertRegex(source, r"(?m)^\s*\[Authorize\]\s*public\s+class\s+EntriesController")
        self.assertEqual(len(re.findall(r"\[HttpPost\b", source)),
                         len(re.findall(r"\[ValidateAntiForgeryToken\]", source)))


class BootstrapAndAccessibilityContractTests(unittest.TestCase):
    def test_shared_layout_uses_pinned_bootstrap_five_assets_with_sri(self):
        layout = (VIEWS / "Shared" / "_Layout.cshtml").read_text(encoding="utf-8-sig")
        self.assertIn("bootstrap@5.3.9/dist/css/bootstrap.min.css", layout)
        self.assertIn("bootstrap@5.3.9/dist/js/bootstrap.bundle.min.js", layout)
        self.assertGreaterEqual(len(re.findall(r'integrity="sha384-[^"]+"', layout)), 2)
        self.assertGreaterEqual(len(re.findall(r'crossorigin="anonymous"', layout)), 2)
        self.assertNotIn("bootstrap@3", layout.lower())

    def test_shared_layout_has_keyboard_navigation_and_semantic_landmarks(self):
        layout = (VIEWS / "Shared" / "_Layout.cshtml").read_text(encoding="utf-8-sig")
        self.assertIn('href="#main-content"', layout)
        self.assertIn('id="main-content"', layout)
        self.assertIn('<nav class="navbar', layout)
        self.assertIn('aria-label="Main navigation"', layout)
        self.assertIn('data-bs-toggle="collapse"', layout)
        self.assertIn('aria-controls="primaryNavigation"', layout)

    def test_property_mutation_forms_render_antiforgery_tokens(self):
        for name in ("Create.cshtml", "Edit.cshtml", "Delete.cshtml"):
            with self.subTest(view=name):
                source = (DWELLING_VIEWS / name).read_text(encoding="utf-8-sig")
                self.assertIn("@Html.BeginForm()", source)
                self.assertIn("@Html.AntiForgeryToken()", source)

    def test_shared_property_fields_keep_labels_and_validation_messages(self):
        source = (DWELLING_VIEWS / "_DwellingFormFields.cshtml").read_text(encoding="utf-8-sig")
        labels = len(re.findall(r"@Html\.LabelFor\(", source))
        editors = len(re.findall(r"@Html\.EditorFor\(", source))
        validations = len(re.findall(r"@Html\.ValidationMessageFor\(", source))
        self.assertGreater(labels, 0)
        self.assertEqual(labels, editors)
        self.assertEqual(editors, validations)
        self.assertIn("form-label", source)
        self.assertIn("form-check-label", source)

    def test_property_list_uses_responsive_table_and_named_actions(self):
        source = (DWELLING_VIEWS / "Index.cshtml").read_text(encoding="utf-8-sig")
        self.assertIn('class="table-responsive"', source)
        self.assertIn("<caption", source)
        self.assertIn('scope="col"', source)
        self.assertIn("aria-label=\"Actions for @item.OfficialAddress\"", source)

    def test_delete_confirmation_is_explicit_and_posted_with_token(self):
        source = (DWELLING_VIEWS / "Delete.cshtml").read_text(encoding="utf-8-sig")
        self.assertIn("Confirm property deletion", source)
        self.assertIn("This action cannot be undone.", source)
        self.assertIn("@Html.AntiForgeryToken()", source)
        self.assertIn('class="btn btn-danger"', source)


if __name__ == "__main__":
    unittest.main(verbosity=2)
