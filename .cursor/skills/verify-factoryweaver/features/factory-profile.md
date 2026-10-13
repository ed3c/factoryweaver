# Factory Profile and catalog claims

## Sub-features

- One workflow entry and declared allowlist remain separate from real Worker identity.
- Duplicate keys refuse even when exact raw catalog bytes match a supplied pin.
- Source: scripts/factory_profile.py
- Source: contracts/v1/factory-profile.schema.json
- Source: contracts/v1/factory-binding.schema.json
- Source: examples/factory-profiles/pstack-synthetic.json
- Source: examples/factory-profiles/pstack-binding-synthetic.json
- Source: examples/factory-profiles/pstack-catalog-synthetic.json

## How to get to it (user POV)

Use factory_profile.py validate, bind-check, audit-catalog or audit-catalog-pinned
with an original Host's supplied inputs. Synthetic examples are never Worker receipts.

## Driving it with the CLI harness

Run `python .cursor/skills/verify-factoryweaver/scripts/verify.py drive factory-profile`.
Positive drives validate a fixture and matching catalog; negative drives refuse
global inheritance and duplicate-key raw data under an exact pin.
Retain real argv, stdout, stderr and exits at the reported evidence directory.

## Gotchas

Input equality proves no native admission, actual Skill discovery or process/secret isolation.
