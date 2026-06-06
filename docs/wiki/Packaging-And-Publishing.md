# Packaging And Publishing

This page keeps maintainer-oriented packaging, validation, build, and release
details outside the end-user README.

## Package Identity

- PyPI package: `salesforce-agent-optimizer`
- Python import package: `salesforce_agent_optimizer`
- CLI command: `sfao`
- Source layout: `src/salesforce_agent_optimizer/`
- Packaged templates: `src/salesforce_agent_optimizer/templates/`
- Current version: `2.2.2`

## Local Development Install

```bash
git clone https://github.com/lucabenedettini/salesforce-ai-agent-optimizer.git
cd salesforce-ai-agent-optimizer
python -m pip install -e ".[dev]"
sfao version
sfao validate
sfao doctor
```

## Required Local Checks

Run these before opening a release pull request or tagging a release:

```bash
python scripts/sync_agent_instructions.py --check --json
python scripts/validate_skill.py --json
python scripts/self_test.py --json
python -m pytest
python -m ruff check .
sfao validate
sfao doctor
```

The checks validate generated adapters, skill frontmatter, YAML, TOML, JSON,
Python compilation, text shape, final newlines, version alignment, Knowledge
generation, destructive-operation guardrails, manifest generation, package
templates, and lightweight Salesforce metadata micro-validators.

## Build From Source

```bash
python -m pip install -e ".[dev]"
python -m build
```

Expected distribution files:

```text
dist/salesforce_agent_optimizer-<version>-py3-none-any.whl
dist/salesforce_agent_optimizer-<version>.tar.gz
```

Check package metadata before publishing:

```bash
python -m twine check dist/*.whl dist/*.tar.gz
```

## Local Wheel Smoke Test

Create a clean virtual environment, install the wheel, and verify the command:

```bash
python -m venv .venv-wheel-test
.venv-wheel-test\Scripts\python -m pip install dist\salesforce_agent_optimizer-<version>-py3-none-any.whl
.venv-wheel-test\Scripts\sfao version
.venv-wheel-test\Scripts\sfao validate --root .
```

On macOS or Linux, use:

```bash
python -m venv .venv-wheel-test
.venv-wheel-test/bin/python -m pip install dist/salesforce_agent_optimizer-<version>-py3-none-any.whl
.venv-wheel-test/bin/sfao version
.venv-wheel-test/bin/sfao validate --root .
```

## Release Artifacts

Generate release artifacts with:

```bash
python scripts/build_release_artifacts.py
```

Expected release files:

```text
dist/*.whl
dist/*.tar.gz
dist/salesforce-agent-optimizer-<version>-skill.zip
dist/SHA256SUMS
dist/release-manifest.json
```

`release-manifest.json` records the package name, version, minimum Python
version, supported installers, supported agents, supported platforms, public
commands, and installed skill paths.

## PyPI Trusted Publishing

Recommended publishing uses PyPI Trusted Publishing from GitHub Actions.

- Do not commit PyPI credentials.
- Do not hardcode tokens in GitHub Actions.
- Configure the PyPI project with this repository, release workflow, and the
  GitHub environment named `pypi`.
- Set repository variable `PUBLISH_TO_PYPI=true` only when PyPI publishing is
  ready.
- Push a tag matching `v*` to trigger the release workflow.

Release tag example:

```bash
git tag v<version>
git push origin v<version>
```

The release workflow runs validation, tests, ruff, `sfao validate`, build,
`twine check`, skill ZIP generation, checksums, release manifest generation, and
GitHub release artifact upload. PyPI publishing runs only when Trusted
Publishing is configured and `PUBLISH_TO_PYPI=true`.

## Manual PyPI Fallback

Use manual upload only when Trusted Publishing is unavailable:

```bash
python -m build
python -m twine check dist/*.whl dist/*.tar.gz
python -m twine upload dist/*.whl dist/*.tar.gz
```

Never commit `.pypirc`, PyPI tokens, passwords, or API credentials.

## Release Checklist

1. Update `VERSION`.
2. Update `pyproject.toml`.
3. Add a precise `CHANGELOG.md` entry.
4. Sync generated agent adapters.
5. Run the required local checks.
6. Build wheel and sdist.
7. Run `python -m twine check dist/*.whl dist/*.tar.gz`.
8. Build release artifacts and verify `release-manifest.json`.
9. Commit the release patch.
10. Tag `v<version>` and push the tag.
11. Verify GitHub release artifacts.
12. Verify PyPI publishing if enabled.

## Version Policy

- Patch: bug fix, documentation correction, small safety fix, compatibility fix,
  or typo correction.
- Minor: new feature, new command, new validation behavior, or minor refactor
  that preserves the public workflow.
- Major: extensive refactor, many capabilities, breaking workflow change, or
  changed installation model.
