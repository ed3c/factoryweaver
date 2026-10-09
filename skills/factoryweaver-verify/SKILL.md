---
name: factoryweaver-verify
description: Verify FactoryWeaver JSON contract validity, evidence references, human-decision boundaries, skill routing honesty and completion claims. Use before passing a specification to a software factory or reporting test, PR or delivery status.
license: MIT
---
# FactoryWeaver verification

1. Load `../../contracts/v1/knowledge-record.schema.json` and run the read-only CLI `validate`.
2. Check Source ID uniqueness, dependency and typed link reachability, and stable card IDs.
3. Require provenance before SUPPORTED, raw test evidence before TESTED, and named original owner readback before RELEASE_CONFIRMED.
4. `READY` is only a proposal. Never launch an adapter from this skill; host must check registry, identity, permission, source pins and effect boundaries.
5. Negative cases: hallucinated operation, unconfirmed human answer, invalid link, duplicate key, empty delivery receipt, unknown effect and source drift.
6. For a multi-factory Work Order, run `python3 scripts/factory_profile.py validate PROFILE.json`, then host-supplied `bind-check PROFILE.json BINDING.json` and `compare PROFILE_A.json BINDING_A.json PROFILE_B.json BINDING_B.json` as needed. Check declared Skill allowlist, one root workflow and separate Worktree IDs. These are untrusted structural claims, not observed Noodle/Carrier behavior; read `../../docs/factory-profile-lock.md`.
7. For an original-owner-selected linked checkout, run `python3 scripts/factory_profile.py observe-local-skills PROFILE.json BINDING.json` to inspect only the Worktree-local Skill directories. See `../../docs/worktree-skill-view.md`. This cannot exclude global Agent Skills or attest a launched Worker Session.
8. For an original Owner's claimed effective Skill list, run `python3 scripts/factory_profile.py audit-catalog PROFILE.json BINDING.json CATALOG.json`. Refuse wrong Session, unexpected global/user Skills or mismatched Skill Digests. The supplied catalog is **not independently authenticated**: pass is `EFFECTIVE_CATALOG_CLAIM_MATCHES`, not a verified Worker discovery receipt. See `../../docs/factory-profile-lock.md`.
9. For optional Carrier replacement, run `python3 scripts/factory_profile.py compare-carriers PROFILE.json BASELINE_BINDING.json ALTERNATIVE_BINDING.json` to ensure both claims use the same Work Order/Base/Profile with distinct Carrier/Session/Worktrees. This **never** proves either worker ran or that replacement works; see `../../docs/factory-profile-lock.md`.
10. Report machine-checked proof boundary and remaining unknowns. A local fixture never proves upstream model performance or PR delivery.