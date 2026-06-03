# Publishing

Salesforce AI Agent Optimizer is packaged as `salesforce-agent-optimizer` with the console command `sfao`.

## Recommended: PyPI Trusted Publishing

Use PyPI Trusted Publishing from GitHub Actions.

- No long-lived PyPI token is needed.
- Configure the PyPI project with a trusted publisher for this GitHub repository and release workflow.
- The release workflow runs only on tags matching `v*`.
- The workflow validates the skill, runs tests, builds wheel/sdist, checks distributions, creates a skill ZIP, creates SHA256 checksums, creates `release-manifest.json`, uploads GitHub release artifacts, and publishes to PyPI only when trusted publishing is enabled.

Do not hardcode tokens in GitHub Actions. Do not commit PyPI credentials.

## Manual Fallback

Use manual publishing only from a clean working tree:

```bash
python -m pip install -e ".[dev]"
python scripts/sync_agent_instructions.py --check --json
python scripts/validate_skill.py --json
python scripts/self_test.py --json
python -m pytest
python -m ruff check .
sfao validate
python -m build
python -m twine check dist/*
python -m twine upload dist/*
```

Keep credentials out of the repository. Prefer environment variables, keyring-backed auth, or a short-lived token entered interactively.

## Release Artifacts

Build GitHub release artifacts with:

```bash
python scripts/build_release_artifacts.py
```

The script creates:

```text
dist/salesforce-agent-optimizer-<version>-skill.zip
dist/release-manifest.json
dist/SHA256SUMS
```

The manifest documents supported installers, agents, platforms, commands, skill paths, artifact sizes, and SHA256 checksums.
