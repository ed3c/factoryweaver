# blind-packet

## Sub-features

- blinded packet preserves two synthetic outputs.
- self-identifying version text refuses.
- Source: scripts/blind_review.py

## How to get to it (user POV)

Use the corresponding public offline CLI with original Owner-supplied inputs.

## Driving it with the CLI harness

Run `python .cursor/skills/verify-factoryweaver/scripts/verify.py drive blind-packet`.
Positive and negative subprocess results are retained in the external evidence directory.

## Gotchas

These are byte/shape/packet controls. Real source authentication, model-quality
comparison and independent human review remain NOT_RUN.
