"""Source contracts for the Bootstrap 5 MVC migration."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class BootstrapMigrationTests(unittest.TestCase):
    def test_layout_uses_pinned_bootstrap_539_with_integrity(self):
        layout = (ROOT / "Views/Shared/_Layout.cshtml").read_text(encoding="utf-8-sig")
        self.assertIn("bootstrap@5.3.9/dist/css/bootstrap.min.css", layout)
        self.assertIn("bootstrap@5.3.9/dist/js/bootstrap.bundle.min.js", layout)
        self.assertIn("integrity=", layout)
        self.assertIn("data-bs-toggle", layout)
        self.assertIn("skip-link", layout)

    def test_legacy_bootstrap_package_and_asset_bundles_are_removed(self):
        packages = ET.parse(ROOT / "packages.config").getroot()
        self.assertFalse(any(p.attrib.get("id", "").lower() == "bootstrap" for p in packages))
        project = (ROOT / "JBS_Properties.csproj").read_text(encoding="utf-8-sig")
        for old_asset in ("Content\\bootstrap.css", "Scripts\\bootstrap.js", "glyphicons-halflings"):
            self.assertNotIn(old_asset, project)
        bundles = (ROOT / "App_Start/BundleConfig.cs").read_text(encoding="utf-8-sig")
        self.assertNotIn("~/bundles/bootstrap", bundles)
        self.assertIn("~/Content/Site.css", bundles)

    def test_unused_legacy_browser_runtime_and_assets_are_removed(self):
        """Bootstrap 5 and the current MVC views do not need legacy browser libraries."""
        layout = (ROOT / "Views/Shared/_Layout.cshtml").read_text(encoding="utf-8-sig")
        bundles = (ROOT / "App_Start/BundleConfig.cs").read_text(encoding="utf-8-sig")
        packages = ET.parse(ROOT / "packages.config").getroot()
        project = (ROOT / "JBS_Properties.csproj").read_text(encoding="utf-8-sig")

        self.assertNotIn("~/bundles/jquery", layout + bundles)
        self.assertNotIn("~/bundles/modernizr", layout + bundles)
        excluded_packages = {"jquery", "modernizr", "respond"}
        self.assertFalse(any(
            package.attrib.get("id", "").lower() in excluded_packages
            for package in packages
        ))
        self.assertNotRegex(project, r"(?i)Scripts\\(?:jquery-|modernizr|respond)")
        for pattern in ("jquery-*", "modernizr-*", "respond*"):
            with self.subTest(pattern=pattern):
                self.assertEqual(list((ROOT / "Scripts").glob(pattern)), [])

        view_usage = "\n".join(
            path.read_text(encoding="utf-8-sig")
            for path in (ROOT / "Views").rglob("*.cshtml")
        )
        self.assertNotRegex(view_usage, r"(?i)\bjQuery\b|\$\s*\(")

    def test_property_views_use_bootstrap_five_patterns(self):
        index = (ROOT / "Views/Dwellings/Index.cshtml").read_text(encoding="utf-8-sig")
        create = (ROOT / "Views/Dwellings/Create.cshtml").read_text(encoding="utf-8-sig")
        edit = (ROOT / "Views/Dwellings/Edit.cshtml").read_text(encoding="utf-8-sig")
        details = (ROOT / "Views/Dwellings/Details.cshtml").read_text(encoding="utf-8-sig")
        delete = (ROOT / "Views/Dwellings/Delete.cshtml").read_text(encoding="utf-8-sig")
        self.assertIn("table-responsive", index)
        self.assertIn("data-bs-toggle", index)
        for view in (create, edit):
            self.assertIn("_DwellingFormFields", view)
            self.assertIn("@Html.AntiForgeryToken()", view)
        self.assertIn("GOOGLE_MAPS_BROWSER_API_KEY", details)
        self.assertNotRegex(details, r"AIza[0-9A-Za-z_-]{20,}")
        self.assertIn("@Html.AntiForgeryToken()", delete)

    def test_shared_form_partial_covers_all_mutable_fields(self):
        partial = (ROOT / "Views/Dwellings/_DwellingFormFields.cshtml").read_text(encoding="utf-8-sig")
        for field in ("PropertyAddressNumber", "PropertyStreetName", "PropertyCity",
                      "PropertyPostalCode", "PropertyPurchaseAmount", "PurchaseDate",
                      "NamesOnLease", "PhoneNumberForTennet", "PrimaryTennetEmailAddress",
                      "LeaseRenewalDate", "Availability", "CurrentlyRented"):
            with self.subTest(field=field):
                self.assertIn("model => model." + field, partial)

    def test_legacy_card_has_one_model_declaration_and_no_provider_tokens(self):
        card = (ROOT / "Views/Properties/CardPartical.cshtml").read_text(encoding="utf-8-sig")
        self.assertEqual(card.count("@model "), 1)
        self.assertNotRegex(card, r"AIza[0-9A-Za-z_-]{20,}")
        self.assertNotIn("zws-id=", card)


if __name__ == "__main__":
    unittest.main(verbosity=2)
