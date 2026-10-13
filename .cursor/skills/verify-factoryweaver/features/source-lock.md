# source-lock

## Sub-features

- supplied source bytes match a frozen local fixture manifest.
- changed bytes refuse.
- Source: scripts/source_lock.py
- Source: docs/bootstrap-boundary.md

## How to get to it (user POV)

Use the corresponding public offline CLI with original Owner-supplied inputs.

## Driving it with the CLI harness

Run `python .cursor/skills/verify-factoryweaver/scripts/verify.py drive source-lock`.
Positive and negative subprocess results are retained in the external evidence directory.

## Gotchas

These are byte/shape/packet controls. Real source authentication, model-quality
comparison and independent human review remain NOT_RUN.
The drive needs Git and creates one disposable synthetic source snapshot.
Its real commit identifies only that fixture, never a live upstream receipt.
