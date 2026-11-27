"""Source-level security and presentation guardrails for the legacy ASP.NET MVC application."""
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CONTROLLERS = ROOT / "Controllers"
VIEWS = ROOT / "Views"
DWELLING_VIEWS = VIEWS / "Dwellings"


class ControllerAccessControlTests(unittest.TestCase):
    def test_solution_targets_supported_dotnet_framework_48(self):
        project = (ROOT / "JBS_Properties.csproj").read_text(encoding="utf-8-sig")
        self.assertIn("<TargetFrameworkVersion>v4.8</TargetFrameworkVersion>", project)
        self.assertIn("Microsoft.NETFramework.ReferenceAssemblies.net48.1.0.3", project)
        self.assertNotIn("<TargetFrameworkVersion>v4.6.1</TargetFrameworkVersion>", project)

        packages = ET.parse(ROOT / "packages.config").getroot()
        self.assertTrue(packages.findall("package"))
        self.assertTrue(all(item.attrib.get("targetFramework") == "net48" for item in packages))
        reference_package = [
            item for item in packages
            if item.attrib.get("id") == "Microsoft.NETFramework.ReferenceAssemblies.net48"
        ]
        self.assertEqual(len(reference_package), 1)

        workflow = (ROOT / ".github" / "workflows" / "dotnet.yml").read_text(encoding="utf-8")
        self.assertIn(".NET Framework 4.8", workflow)
        self.assertIn("Microsoft.NETFramework.ReferenceAssemblies.net48.targets", workflow)

    def test_restored_nuget_payloads_are_not_committed(self):
        """Keep generated NuGet package contents out of Git; restore from packages.config."""
        import subprocess

        tracked = subprocess.run(
            ["git", "ls-files", "--", "packages"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
        self.assertEqual(tracked, [])

        ignore = (ROOT / ".gitignore").read_text(encoding="utf-8-sig")
        workflow = (ROOT / ".github" / "workflows" / "dotnet.yml").read_text(encoding="utf-8")
        self.assertIn("**/packages/*", ignore)
        self.assertIn("!**/packages/build/", ignore)
        self.assertIn("nuget restore .\\JBS_Properties.sln -NonInteractive", workflow)
        self.assertIn("packages.config", (ROOT / "packages.config").read_text(encoding="utf-8-sig"))

    def test_unused_restsharp_package_is_not_restored_or_referenced(self):
        project = ET.parse(ROOT / "JBS_Properties.csproj").getroot()
        project_ns = {"msbuild": "http://schemas.microsoft.com/developer/msbuild/2003"}
        references = {
            reference.attrib.get("Include", "").split(",", 1)[0]
            for reference in project.findall(".//msbuild:Reference", project_ns)
        }
        packages = ET.parse(ROOT / "packages.config").getroot()
        package_ids = {package.attrib.get("id") for package in packages.findall("package")}

        self.assertNotIn("RestSharp", references)
        self.assertNotIn("RestSharp", package_ids)

    def test_web_config_matches_net48_and_newtonsoft_13(self):
        config = ET.parse(ROOT / "Web.config").getroot()
        compilation = config.find("./system.web/compilation")
        runtime = config.find("./system.web/httpRuntime")
        self.assertEqual(compilation.attrib.get("targetFramework"), "4.8")
        self.assertEqual(compilation.attrib.get("debug"), "false")
        self.assertEqual(runtime.attrib.get("targetFramework"), "4.8")

        source = (ROOT / "Web.config").read_text(encoding="utf-8-sig")
        self.assertIn('oldVersion="0.0.0.0-13.0.0.0" newVersion="13.0.0.0"', source)


    def test_help_page_web_config_disables_debug_compilation(self):
        config = ET.parse(ROOT / "Areas" / "HelpPage" / "Views" / "Web.config").getroot()
        compilation = config.find("./system.web/compilation")
        self.assertIsNotNone(compilation)
        self.assertEqual(compilation.attrib.get("debug"), "false")

    def test_web_config_binding_redirects_match_referenced_assembly_versions(self):
        project = ET.parse(ROOT / "JBS_Properties.csproj").getroot()
        project_ns = {"msbuild": "http://schemas.microsoft.com/developer/msbuild/2003"}
        references = {}
        for reference in project.findall(".//msbuild:Reference", project_ns):
            include = reference.attrib.get("Include", "")
            parts = [part.strip() for part in include.split(",")]
            if len(parts) > 1 and parts[1].startswith("Version="):
                references[parts[0]] = parts[1].split("=", 1)[1]

        config = ET.parse(ROOT / "Web.config").getroot()
        assembly_ns = "{urn:schemas-microsoft-com:asm.v1}"
        redirects = {}
        for assembly in config.findall(".//" + assembly_ns + "dependentAssembly"):
            identity = assembly.find(assembly_ns + "assemblyIdentity")
            redirect = assembly.find(assembly_ns + "bindingRedirect")
            if identity is not None and redirect is not None:
                redirects[identity.attrib.get("name")] = redirect.attrib.get("newVersion")

        for assembly_name in (
            "System.Diagnostics.DiagnosticSource",
            "System.Web.Mvc",
            "Newtonsoft.Json",
        ):
            with self.subTest(assembly=assembly_name):
                self.assertIn(assembly_name, references)
                self.assertEqual(redirects.get(assembly_name), references[assembly_name])

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

    def test_root_route_and_brand_open_the_public_portfolio(self):
        route = (ROOT / "App_Start" / "RouteConfig.cs").read_text(encoding="utf-8-sig")
        layout = (VIEWS / "Shared" / "_Layout.cshtml").read_text(encoding="utf-8-sig")
        self.assertIn('defaults: new { controller = "PublicProperties", action = "Index"', route)
        self.assertIn('href="@Url.Action("Index", "PublicProperties")">JBS Properties</a>', layout)
        self.assertIn('Url.Action("Index", "Dwellings")', layout)

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


    def test_public_portfolio_controller_is_protected_by_default_with_two_explicit_anonymous_actions(self):
        source = (CONTROLLERS / "PublicPropertiesController.cs").read_text(encoding="utf-8-sig")
        self.assertRegex(source, r"(?m)^\s*\[Authorize\]\s*public\s+class\s+PublicPropertiesController")
        self.assertRegex(source, r"(?s)\[AllowAnonymous\]\s*public\s+ActionResult\s+Index")
        self.assertRegex(source, r"(?s)\[AllowAnonymous\]\s*public\s+JsonResult\s+Feed")
        self.assertIn('Server.MapPath("~/App_Data/property.json")', source)
        self.assertIn('Environment.GetEnvironmentVariable("JBS_PROPERTY_DATA_PATH")', source)
        self.assertIn("Path.IsPathRooted(configuredPath)", source)
        self.assertIn("Path.GetFullPath(configuredPath)", source)
        self.assertIn("archivePath.StartsWith(webRoot, StringComparison.OrdinalIgnoreCase)", source)
        self.assertIn("JsonRequestBehavior.AllowGet", source)
        self.assertIn("Response.Cache.SetMaxAge(TimeSpan.FromMinutes(5))", source)
        self.assertEqual(source.count("catch (UnauthorizedAccessException)"), 2)
        self.assertIn('ReadRequiredText(row, "address", MaxAddressLength)', source)
        self.assertIn('ReadRequiredText(row, "status", MaxStatusLength)', source)
        self.assertIn("token.Type != JTokenType.String", source)
        self.assertIn("normalized.Any(Char.IsControl)", source)

    def test_public_projection_is_an_explicit_two_field_allowlist(self):
        source = (CONTROLLERS / "PublicPropertiesController.cs").read_text(encoding="utf-8-sig")
        model = (ROOT / "Models" / "PublicPropertyListing.cs").read_text(encoding="utf-8-sig")
        view = (ROOT / "Views" / "PublicProperties" / "Index.cshtml").read_text(encoding="utf-8-sig")
        self.assertIn("Address = address", source)
        self.assertIn("Status = status", source)
        self.assertIn('public string Address { get; set; }', model)
        self.assertIn('public string Status { get; set; }', model)
        self.assertNotIn('row["purchase-price"]', source)
        self.assertNotIn('row["purchase-date"]', source)
        self.assertNotIn('row["zestimate"]', source)
        self.assertNotIn('row["image"]', source)
        self.assertNotIn("NamesOnLease", source + model + view)
        self.assertNotIn("PhoneNumberForTennet", source + model + view)
        self.assertNotIn("PrimaryTennetEmailAddress", source + model + view)
        self.assertEqual(len(re.findall(r"(?m)^\s*public\s+string\s+\w+\s*\{\s*get;", model)), 2)

    def test_public_archive_records_are_valid_and_feed_status_is_not_claimed_live(self):
        import json

        archive = json.loads((ROOT / "App_Data" / "property.json").read_text(encoding="utf-8-sig"))
        self.assertIsInstance(archive.get("rental"), list)
        for record in archive["rental"]:
            with self.subTest(record_type=type(record).__name__):
                self.assertIsInstance(record, dict)
                self.assertIsInstance(record.get("address"), str)
                self.assertTrue(record["address"].strip())
                self.assertIsInstance(record.get("status"), str)
                self.assertTrue(record["status"].strip())

        view = (ROOT / "Views" / "PublicProperties" / "Index.cshtml").read_text(encoding="utf-8-sig")
        self.assertIn("may not reflect real-time availability", view)
        self.assertIn("@property.Address", view)
        self.assertIn("@property.Status", view)

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
        self.assertIn('Url.Action("Index", "PublicProperties")', layout)
        self.assertIn('Url.Action("Index", "Dwellings")', layout)

    def test_property_mutation_forms_render_antiforgery_tokens(self):
        for name in ("Create.cshtml", "Edit.cshtml", "Delete.cshtml"):
            with self.subTest(view=name):
                source = (DWELLING_VIEWS / name).read_text(encoding="utf-8-sig")
                self.assertIn("Html.BeginForm()", source)
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


class PublicPortfolioFailureBoundaryTests(unittest.TestCase):
    def test_public_portfolio_fails_closed_when_its_source_is_unavailable_or_invalid(self):
        source = (CONTROLLERS / "PublicPropertiesController.cs").read_text(encoding="utf-8-sig")
        index_action = source.split("public ActionResult Index()", 1)[1].split("public JsonResult Feed()", 1)[0]
        feed_action = source.split("public JsonResult Feed()", 1)[1].split("private JsonResult FeedUnavailable()", 1)[0]
        failure_response = source.split("private JsonResult FeedUnavailable()", 1)[1].split("private IList<PublicPropertyListing>", 1)[0]
        for action_name, action in (("Index", index_action), ("Feed", feed_action)):
            with self.subTest(action=action_name):
                for exception in ("IOException", "UnauthorizedAccessException", "JsonException", "InvalidDataException"):
                    self.assertIn("catch (" + exception + ")", action)
        self.assertIn("return new HttpStatusCodeResult(503", index_action)
        self.assertIn("return FeedUnavailable()", feed_action)
        self.assertIn("Response.StatusCode = 503", failure_response)
        self.assertIn('error = "Public property data is temporarily unavailable."', failure_response)
        self.assertNotIn("Exception.Message", failure_response)

    def test_public_property_archive_has_bounded_input_and_text_fields(self):
        source = (CONTROLLERS / "PublicPropertiesController.cs").read_text(encoding="utf-8-sig")
        self.assertIn("MaxArchiveBytes = 5 * 1024 * 1024", source)
        self.assertIn("MaxPublicListings = 1000", source)
        self.assertIn("MaxAddressLength = 250", source)
        self.assertIn("MaxStatusLength = 80", source)
        self.assertIn("sourceFile.Length > MaxArchiveBytes", source)
        self.assertIn("rentalRows.Count > MaxPublicListings", source)
        self.assertIn("normalized.Any(Char.IsControl)", source)
        self.assertIn("ReadRequiredText(row, \"address\", MaxAddressLength)", source)
        self.assertIn("ReadRequiredText(row, \"status\", MaxStatusLength)", source)
        self.assertIn("new List<PublicPropertyListing>(rentalRows.Count)", source)


if __name__ == "__main__":
    unittest.main(verbosity=2)
