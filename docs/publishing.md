# Publishing

Salesforce Agent Optimizer is published as the Python package `salesforce-agent-optimizer` with the console command `sfao`.

## PyPI Trusted Publishing

The repository expects PyPI Trusted Publishing from GitHub Actions.

- No PyPI API token is required.
- No `PYPI_API_TOKEN` secret should be used.
- Publishing is triggered by pushing a tag matching `v*`.
- The PyPI job runs only when repository variable `PUBLISH_TO_PYPI=true`.
- The PyPI job uses GitHub environment `pypi`.
- The PyPI job uses OIDC through `pypa/gh-action-pypi-publish@release/v1`.

Tag a release:

```bash
git tag v1.0.3
git push origin v1.0.3
```

## Required Local Checks

Run these before tagging:

```bash
python -m pip install -e ".[dev]"
sfao validate
python -m build
python -m twine check dist/*
```

The release workflow also runs generated-instruction checks, validation, self tests, pytest, ruff, wheel/sdist build, `twine check`, skill ZIP generation, checksum generation, and release manifest generation.

## Release Assets

The workflow uploads:

```text
dist/*.whl
dist/*.tar.gz
dist/salesforce-agent-optimizer-<version>-skill.zip
dist/SHA256SUMS
dist/release-manifest.json
```

It also uploads a GitHub Actions artifact named `python-package-distributions` containing:

```text
dist/*.whl
dist/*.tar.gz
```

## Troubleshooting

PyPI job skipped:

- Confirm repository variable `PUBLISH_TO_PYPI=true`.
- Confirm the tag matches `v*`.

Trusted Publishing not configured:

- Configure the PyPI project trusted publisher for this repository, workflow, and environment.
- Confirm the GitHub environment is named `pypi`.

Environment mismatch:

- The workflow declares environment `pypi`; PyPI Trusted Publishing must match it.

Package name already taken:

- Confirm the PyPI project name is `salesforce-agent-optimizer`.

Wheel or sdist missing:

- Run `python -m build`.
- Check that `dist/*.whl` and `dist/*.tar.gz` exist.

Twine validation failure:

- Run `python -m twine check dist/*`.
- Fix README rendering, package metadata, or missing files before tagging again.
