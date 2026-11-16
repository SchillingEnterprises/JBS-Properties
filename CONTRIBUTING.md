# Contributing

## Before making changes

1. Read the project README and inspect the affected application area.
2. Open an issue for substantial behavior changes or architectural work.
3. Keep changes focused. Preserve existing projects, data, and migration history.
4. Never commit credentials, connection strings, local IDE state, build output, or production data.

## Development workflow

1. Create a topic branch from `master`.
2. Use clear, scoped commits, for example `fix(properties): validate listing inputs`.
3. Build the solution in Release configuration.
4. Add or update automated tests for behavior changes.
5. Open a pull request describing the rationale, implementation, test evidence, and deployment considerations.

## Code quality

- Prefer small methods with one responsibility and meaningful names.
- Document public APIs and non-obvious domain rules.
- Validate external input at application boundaries.
- Use parameterized data access and safe output encoding.
- Avoid introducing dependencies unless they solve a concrete problem.
- Do not suppress compiler warnings without documenting why.
- Preserve compatibility with the project's supported .NET Framework target unless an approved migration changes it.

## Testing status

The repository currently has no clearly identified dedicated unit-test project. The CI workflow therefore verifies package restore and compilation only; it does not claim unit-test coverage. Add a test project before relying on test-based release gates.
