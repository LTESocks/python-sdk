# Contributing

Install [uv](https://docs.astral.sh/uv/), then create the development
environment and run the complete verification suite:

```bash
uv sync --all-groups
make quality
make generate-check
make build
```

Generated code lives under `src/ltesocks_sdk/_generated`, `models`, and
`resources`. Do not edit it directly. Update the canonical schema with
`make sync-openapi SOURCE=/path/to/openapi.yaml`, run `make generate`, and review
the resulting contract and public API changes.

Submit changes through a pull request. Add tests for behavioral changes and
keep backward compatibility unless the release is explicitly major.
