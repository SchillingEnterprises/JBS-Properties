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

The property application models tenant names, contact information, lease dates, and purchase/financial details. Treat the database as confidential. Use HTTPS, access controls, backups, audit logging, least privilege, and an approved retention policy. Do not commit populated databases or tenant exports. The tracker may hold personal activity records and should also remain private.

## Legacy platform

The project targets .NET Framework 4.6.1 and ASP.NET MVC 5, which require a validated hosting environment. A build success does not establish production security or hosting compatibility. Validate the target framework, IIS configuration, database credentials, authentication provider, logging, and backups before deployment.

Report vulnerabilities privately using GitHub's private vulnerability reporting feature when available.
