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

The database may hold tenant/contact and property financial information. Never commit populated databases or exports.

## Build

Use Visual Studio/MSBuild on Windows with the .NET Framework 4.6.1 targeting references. The repository's CI workflow restores packages and compiles the application in Release configuration.

```powershell
nuget restore JBS_Properties.sln
msbuild JBS_Properties.sln /p:Configuration=Release
```

## Modernization status

This is a legacy .NET Framework application, not a new .NET 8/10 ASP.NET Core project. The first step is a safe build baseline and access-control hardening. A migration to a supported runtime should be staged with verified authentication, database backup/migration strategy, and integration tests rather than an in-place framework-number change.
