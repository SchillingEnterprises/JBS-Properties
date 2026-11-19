using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using John_Baxter_Schilling.Models;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace John_Baxter_Schilling.Controllers
{
    // Keep the controller protected by default. Only the explicitly curated
    // portfolio page and feed are anonymous.
    [Authorize]
    public class PublicPropertiesController : Controller
    {
        private const long MaxArchiveBytes = 5 * 1024 * 1024;
        private const int MaxPublicListings = 1000;
        private const int MaxAddressLength = 250;
        private const int MaxStatusLength = 80;
        [AllowAnonymous]
        public ActionResult Index()
        {
            try
            {
                return View(ReadPublicListings());
            }
            catch (IOException)
            {
                return new HttpStatusCodeResult(503, "Public property data is temporarily unavailable.");
            }
            catch (UnauthorizedAccessException)
            {
                return new HttpStatusCodeResult(503, "Public property data is temporarily unavailable.");
            }
            catch (JsonException)
            {
                return new HttpStatusCodeResult(503, "Public property data is temporarily unavailable.");
            }
            catch (InvalidDataException)
            {
                return new HttpStatusCodeResult(503, "Public property data is temporarily unavailable.");
            }
        }

        [AllowAnonymous]
        public JsonResult Feed()
        {
            try
            {
                Response.Cache.SetCacheability(HttpCacheability.Public);
                Response.Cache.SetMaxAge(TimeSpan.FromMinutes(5));
                return Json(
                    new
                    {
                        schemaVersion = 1,
                        properties = ReadPublicListings()
                    },
                    JsonRequestBehavior.AllowGet
                );
            }
            catch (IOException)
            {
                return FeedUnavailable();
            }
            catch (UnauthorizedAccessException)
            {
                return FeedUnavailable();
            }
            catch (JsonException)
            {
                return FeedUnavailable();
            }
            catch (InvalidDataException)
            {
                return FeedUnavailable();
            }
        }

        private JsonResult FeedUnavailable()
        {
            Response.StatusCode = 503;
            Response.TrySkipIisCustomErrors = true;
            return Json(
                new { error = "Public property data is temporarily unavailable." },
                JsonRequestBehavior.AllowGet
            );
        }

        private IList<PublicPropertyListing> ReadPublicListings()
        {
            // App_Data is not a directly served public directory in ASP.NET.
            // The only public output is the allowlisted DTO below.
            var configuredPath = Environment.GetEnvironmentVariable("JBS_PROPERTY_DATA_PATH");
            string archivePath;
            if (String.IsNullOrWhiteSpace(configuredPath))
            {
                // Backward-compatible fallback: this archive contains only the
                // user-approved public source records tracked in this repository.
                archivePath = Server.MapPath("~/App_Data/property.json");
            }
            else
            {
                if (!Path.IsPathRooted(configuredPath))
                {
                    throw new InvalidDataException("The configured property source path must be absolute.");
                }

                archivePath = Path.GetFullPath(configuredPath);
                var webRoot = Path.GetFullPath(Server.MapPath("~/"))
                    .TrimEnd(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar)
                    + Path.DirectorySeparatorChar;
                if (archivePath.StartsWith(webRoot, StringComparison.OrdinalIgnoreCase))
                {
                    throw new InvalidDataException("The configured property source must be outside the web root.");
                }
            }

            var sourceFile = new FileInfo(archivePath);
            if (sourceFile.Exists && sourceFile.Length > MaxArchiveBytes)
            {
                throw new InvalidDataException("The property archive exceeds the permitted file size.");
            }

            var archive = JObject.Parse(System.IO.File.ReadAllText(archivePath));
            var rentalRows = archive["rental"] as JArray;
            if (rentalRows == null)
            {
                throw new InvalidDataException("The property archive must contain a rental array.");
            }

            if (rentalRows.Count > MaxPublicListings)
            {
                throw new InvalidDataException("The property archive contains too many public records.");
            }

            var listings = new List<PublicPropertyListing>(rentalRows.Count);
            foreach (var token in rentalRows)
            {
                var row = token as JObject;
                if (row == null)
                {
                    throw new InvalidDataException("Every public property record must be an object.");
                }

                var address = ReadRequiredText(row, "address", MaxAddressLength);
                var status = ReadRequiredText(row, "status", MaxStatusLength);

                // Deliberately do not serialize purchase data, tenant details,
                // lease information, provider URLs, map coordinates, or source metadata.
                listings.Add(new PublicPropertyListing
                {
                    Address = address,
                    Status = status
                });
            }

            return listings;
        }

        private static string ReadRequiredText(JObject row, string field, int maximumLength)
        {
            var token = row[field];
            if (token == null || token.Type != JTokenType.String)
            {
                throw new InvalidDataException("Every public property record requires string address and status values.");
            }

            var value = token.Value<string>();
            if (String.IsNullOrWhiteSpace(value))
            {
                throw new InvalidDataException("Every public property record requires an address and status.");
            }

            var normalized = value.Trim();
            if (normalized.Length > maximumLength || normalized.Any(Char.IsControl))
            {
                throw new InvalidDataException("A public property field exceeds the permitted format or length.");
            }

            return normalized;
        }
    }
}
