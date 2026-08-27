# Publishing checklist

The initial repository commit is not a release and must not publish to PyPI.

For an approved release, synchronize and regenerate OpenAPI, update `project.version` and `CHANGELOG.md`, run the full CI/build checks, and create a matching `vX.Y.Z` tag from reviewed `main`. The GitHub workflow uses PyPI trusted publishing; do not store a long-lived PyPI token.
