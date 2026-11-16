# JBS Properties

A legacy ASP.NET MVC / Entity Framework application for property records, accompanied by a separate Fitness Frog activity-tracking sample in the same repository.

## Repository contents

- Property management: dwelling details, availability/rental status, purchase information, tenant contact information, and lease dates.
- Fitness Frog sample: activity entries, duration, intensity, exclusion flag, and notes.
- ASP.NET MVC 5 / Entity Framework 6 application targeting .NET Framework 4.6.1.

These are distinct application concerns retained in one historical repository. They have not been split or rewritten, to preserve their source and history.

## Security status

The property and activity controllers require an authenticated identity; POST operations in the activity tracker now require anti-forgery tokens. Web.config disables debug compilation output and enables basic security headers. See [SECURITY.md](SECURITY.md).

**Authentication still needs configuration.** The repository does not contain a verified sign-in flow or configured identity provider. Anonymous access is blocked by the controller attributes; do not remove those attributes to bypass the login gap. Configure and test a real identity provider before deploying.

The property-management database may hold tenant/contact and financial information and must remain confidential. Never commit populated databases or tenant exports. The historical `App_Data/property.json` archive is intentionally public in this public repository because its selected addresses and occupancy labels are approved for disclosure. It is not a secret store and remains visible in Git history.

The anonymous portfolio surface is `/PublicProperties`; its read-only JSON endpoint is `/PublicProperties/Feed`. Both read the archive server-side and expose only the explicit `Address` and `Status` allowlist. Purchase prices/dates, tenant identities/contact details, lease data, map coordinates, and third-party provider URLs are not projected into the public results. The authenticated `/Dwellings` management area remains separate. Do not add fields to the public DTO without reviewing disclosure, consent, and business impact.

The property-details and legacy property-card map previews read `GOOGLE_MAPS_BROWSER_API_KEY` from the hosting environment and render no external map request when it is unset. The unused legacy card's invalid dual-model declaration and obsolete Zillow API link have also been removed. Configure only a dedicated Google Maps browser key with HTTP-referrer restrictions and API restrictions. A previously hard-coded key was exposed in repository history: revoke/rotate it in Google Cloud Console; removing it from the current source does not invalidate the historical credential.

## Public property portfolio

The public portfolio is a read-only projection of the approved archive. Visit `/PublicProperties` for the responsive results page or `/PublicProperties/Feed` for JSON (`schemaVersion: 1`). The feed is generated on request from `App_Data/property.json`, so approved archive edits flow into the results automatically without a paid database, API provider, or third-party integration.

The public DTO is an explicit allowlist containing only address and status. The archive's legacy purchase fields, Zillow references, Street View URLs/coordinates, and any future non-allowlisted fields are never copied into the public response. The MVC management area remains authenticated and is not the public feed's data source. ASP.NET's `App_Data` directory is not directly served as static content; the controller reads it server-side and emits only the allowlisted projection.

The archive itself is still visible to anyone who can browse this public GitHub repository. That is intentional for the approved public source records, not a confidentiality control. Keep tenant names, phone numbers, email addresses, lease details, database exports, credentials, and other private management information out of this repository. The feed's status is a snapshot, not a real-time vacancy guarantee.

## Build

Use Visual Studio/MSBuild on Windows with the .NET Framework 4.6.1 targeting references. The repository's CI workflow restores packages and compiles the application in Release configuration.

```powershell
nuget restore JBS_Properties.sln
msbuild JBS_Properties.sln /p:Configuration=Release
```


## Security regression checks

A lightweight source-contract suite runs in GitHub Actions alongside the Windows/MSBuild build:

```bash
python -m unittest discover -s tests -v
```

It guards the existing class-level authorization on the property and Fitness Frog controllers and verifies anti-forgery validation on every POST action. These checks are intentionally source-level guardrails; they do not provide an identity provider or substitute for authenticated end-to-end tests. Configure and verify a real identity provider before deployment, and do not remove authorization attributes to bypass the missing sign-in configuration.

## Modernization status

This is a legacy .NET Framework application, not a new .NET 8/10 ASP.NET Core project. The first step is a safe build baseline and access-control hardening. A migration to a supported runtime should be staged with verified authentication, database backup/migration strategy, and integration tests rather than an in-place framework-number change.


## Front-end stack

The classic MVC views use Bootstrap 5.3.9 with version-pinned jsDelivr assets and Subresource Integrity (SRI). Bootstrap's CSS and JavaScript are loaded from the pinned CDN URLs in the shared layout; the obsolete Bootstrap 3 NuGet package, local CSS/JS bundle entries, and Glyphicons assets are no longer part of the app bundle. The application-specific theme remains in `Content/Site.css`.

The property list, create/edit forms, details view, deletion confirmation, and shared navigation use Bootstrap 5 responsive components and `data-bs-*` attributes. The create/edit forms share one partial to keep their fields aligned. Server-side MVC validation and anti-forgery protection remain enabled; the legacy client-validation bundle was not present in the repository and is not falsely advertised as active.

Bootstrap CDN version and SRI values must be updated together. The browser will reject a mismatched asset. See the [official Bootstrap 5.3 installation guide](https://getbootstrap.com/docs/5.3/getting-started/introduction/).
