# Portable v7.2 bundle

## Sub-features

- Canonical Skill bytes and local references survive a full directory copy.
- Exact repeated build returns NOOP; altered content is refused.
- Source: scripts/build_skill_bundle.py
- Source: scripts/check_bundle.py
- Source: scripts/verify_installed_skill.py
- Source: tests/test_portable_bundle.py

## How to get to it (user POV)

Build a distribution and configure the Host to load its skills/factoryweaver/SKILL.md.
Copying only the leaf directory loses its dependencies.

## Driving it with the CLI harness

Run `python .cursor/skills/verify-factoryweaver/scripts/verify.py drive portable-bundle`.
The isolated drive builds, repeats, inspects a copied layout and refuses altered bytes.
Retain stdout, stderr, exits and result.json at the returned evidence path.

## Gotchas

Self-consistency does not authenticate a publisher. Installed layout does not prove
external installer behavior or native Agent invocation. Both remain NOT_RUN.
