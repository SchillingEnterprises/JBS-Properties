using System.Web.Optimization;

namespace JBS_Properties
{
    public class BundleConfig
    {
        public static void RegisterBundles(BundleCollection bundles)
        {
            bundles.Add(new ScriptBundle("~/bundles/jquery").Include(
                "~/Scripts/jquery-{version}.js"));

            bundles.Add(new ScriptBundle("~/bundles/modernizr").Include(
                "~/Scripts/modernizr-*"));

            // Bootstrap 5.3.9 is loaded from a version-pinned CDN with SRI
            // in Views/Shared/_Layout.cshtml. Bootstrap 5 no longer needs jQuery.
            bundles.Add(new StyleBundle("~/Content/css").Include(
                "~/Content/Site.css"));
        }
    }
}
