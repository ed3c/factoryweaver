---
name: factoryweaver
description: Compose coding-agent skills, job or product requirements, verified specs and evidence as one portable software factory contract. Use when integrating multiple SKILL.md workflows with any auto-PR system; preserve the host's execution authority.
license: MIT
compatibility: Requires Python 3 and jsonschema for optional machine validation; does not require GitHub access.
---
# FactoryWeaver

1. Discover the currently available host skills; do not invent installed capabilities.
2. Read `../../docs/compatibility.md` to understand the difference between shape compatibility and live integration.
3. For requirements, knowledge cards and source evidence, use `factoryweaver-compile`.
4. For machine verification or claims of completion, use `factoryweaver-verify`. When a task composes multiple software factory methods or runs in a Noodle/other Worker Carrier, first read `../../docs/factory-profile-lock.md` and validate a single-entry profile with `python3 scripts/factory_profile.py validate PROFILE.json`. This only proposes skills; Soodles/host independently admits the exact Worker/Worktree and may refuse any selection.
5. Preserve original upstream skill semantics. Never answer a human-only `grilling` decision for the user.
6. Return structured `ActionRequest` proposals only; the original host grants permissions and owns physical effects and readback.
7. If a registered adapter, pinned source or original owner is absent, report a named blocker and continue unaffected work.

Output must distinguish **knowledge status**, **engineering status**, and **delivery status**. Never describe `READY` as permission to create a PR or merge.