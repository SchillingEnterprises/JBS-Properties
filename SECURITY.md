# Security Policy

## Current controls and boundaries

- The property-management and activity-tracking controllers now require an authenticated identity.
- All state-changing POST actions in the tracker require anti-forgery tokens.
- The dwelling delete action handles missing records safely.
- Activity averages return zero when there are no included entries.
- Web.config disables compilation debug output and adds basic browser security headers.

## Important deployment limitation

The repository does not currently include a verified account/login workflow or a confirmed authentication provider. The protected controllers will deny anonymous requests, but this patch does not invent an identity provider or create a default administrator. Configure and test real authentication/authorization before deploying. Do not remove the authorization attributes simply to make the pages accessible.

## Sensitive data

The property application models tenant names, contact information, lease dates, and purchase/financial details. Treat the management database as confidential. Use HTTPS, access controls, backups, audit logging, least privilege, and an approved retention policy. Do not commit populated databases or tenant exports. The tracker may hold personal activity records and should also remain private.

The anonymous `/PublicProperties` page and `/PublicProperties/Feed` endpoint expose only address and status through an explicit DTO allowlist. For stronger source-data protection on a configured host, set `JBS_PROPERTY_DATA_PATH` to an absolute JSON file path outside the web root and outside Git; the controller rejects relative paths and paths inside the web root. Do not add tenant details, lease fields, purchase history, map coordinates, provider URLs, or arbitrary archive properties to the public DTO. If the host variable is unset, the app reads the approved public fallback archive at `App_Data/property.json`, which remains visible in the public Git repository; App_Data only prevents direct static serving by the ASP.NET application. The public status is archival, not a real-time availability promise.

## Legacy platform

The project targets .NET Framework 4.8 and ASP.NET MVC 5. Validate the Windows/IIS hosting environment, installed .NET Framework 4.8 runtime, database credentials, authentication provider, logging, and backups before deployment. A build success does not establish production security or hosting compatibility. Validate the target framework, IIS configuration, database credentials, authentication provider, logging, and backups before deployment.

Report vulnerabilities privately using GitHub's private vulnerability reporting feature when available.


## Historical provider credentials

A Google Maps API key was previously committed to repository history. Treat that historical value as exposed and revoke/rotate it with Google Cloud before any deployment that uses Maps. Restrict any replacement to the required Maps APIs, approved referrers, and an appropriate quota, and store it only in the hosting secret manager. The current default-branch `Web.config` contains no Google API key literal; removing it from the current tree does not revoke the historical credential.
