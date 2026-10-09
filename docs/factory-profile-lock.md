# Factory Profile Lock — one Work Order, one outer Factory method

FactoryWeaver defines a **portable, read-only factory method and evidence contract**. Soodles remains the Supervisor, Test Manager and original landing Owner; Noodle remains the default Session/Worktree Carrier. A different Carrier may be selected by the original Supervisor only after separate capability and physical readback admission.

This is a public specification candidate. No Soodles or Noodle control-plane implementation is embedded in FactoryWeaver.

## Public shapes

- `contracts/v1/factory-profile.schema.json`: one profile ID, **one** whole-Issue `workflow_entry`, explicit pinned Skill allowlist, carrier capabilities and required isolation expectations.
- `contracts/v1/factory-binding.schema.json`: a **declared** Work Order, repository/base, profile SHA256, Carrier capability list, Session/Worktree IDs, Worktree path and effective Skill view.

Each Skill record pins a Git source revision and content digest. A SHA-256 text field is not proof that GitHub delivered these bytes; the original owner must compare actual source and installed Skill content before admission. The synthetic samples use `example.invalid` intentionally and **must never be treated as installed pstack, Builder or FactoryWeaver**.

## Data flow

```text
FactoryWeaver factory profile + Spec/WorkOrder
                  │  read-only policy and source lock
                  ▼
Soodles Supervisor / original admission owner
                  │  selects exact profile, target and Carrier
                  ▼
Replaceable Carrier boundary
      ├── Noodle (existing default)
      └── other selected Carrier (not yet proven)
                  │  original host validates skill discovery
                  ▼
one authorized Issue → one isolated Worker Worktree
                  │  selected outer Skill workflow only
                  ▼
Candidate source + Test Manager scoped evidence
                  │
                  ▼
original publication/landing owner + fresh readback
```

**Worktree isolation is not a container security boundary.** Separate Git Worktree directories do not by themselves restrict global Skill folders, shared Git common dir, HOME, network, OS processes or credentials. The Carrier/Host must separately prove and enforce any environment or secret restrictions it advertises.

## Read-only CLI

```bash
python3 scripts/factory_profile.py validate examples/factory-profiles/pstack-synthetic.json
python3 scripts/factory_profile.py validate examples/factory-profiles/builder-synthetic.json
```

An original Owner can supply `factory-binding-v1` JSON and invoke:

```bash
python3 scripts/factory_profile.py bind-check PROFILE.json BINDING.json
python3 scripts/factory_profile.py compare PROFILE_A.json BINDING_A.json PROFILE_B.json BINDING_B.json
```

A binding is only a **claim** about what a Host supposedly installed and launched. The verifier refuses mismatched profile digest, wrong Skill revision, undeclared or globally inherited Skill, two outer Workflow Entries, a missing Carrier capability, inconsistent target repository, malformed Worktree path, reused Session/Worktree ID and overlapping declared paths. It always reports `original_owner_readback_verified=false`, `physical_worktree_verified=false` and `effect_authority=false`. It does not run a Carrier, mount Skills, create a Git worktree, authenticate arbitrary user-supplied observations or perform provider writes.

## Optional physical Git Worktree readback

A declared Profile/Binding does not prove a real checkout. If the original Host can supply the exact actual linked Worktree path and `session.head_sha` of a Worker under its authorization, run:

```bash
python3 scripts/factory_profile.py observe-worktree PROFILE.json BINDING.json
```

This read-only probe requires a real linked Git Worktree (`.git` file), checks `git rev-parse HEAD` matches the pinned `session.head_sha`, verifies the selected `work_order.base_sha` is an ancestor of the observed HEAD (allowing actual descendant candidate commits), verifies exact toplevel and `git worktree list --porcelain`, and distinguishes the linked Git directory from the shared common Git directory. A wrong head, main checkout or missing Worktree fails closed.

The outcome is strictly `LOCAL_GIT_WORKTREE_OBSERVED`. It proves **local Git checkout identity at the time of the probe**, not Noodle Worker Session provenance, Skill Discovery reality, OS/process isolation, cross-profile global Skill isolation, permission scope or Owner-delivery readback. Those are original Soodles/Noodle or selected Carrier responsibilities. This CLI does not create worktrees, launch agents, mutate Git or grant authority.

## Claimed Agent Skill Catalog comparison

If the authorized worker owner has a catalog capture, `factory_profile.py audit-catalog PROFILE.json BINDING.json CATALOG.json` checks the declared profile digest, work order, carrier, session and worktree IDs against that catalog. It also rejects undeclared Skills, wrong digests and global/user/system scope claims. A synthetic example is in `examples/factory-profiles/pstack-catalog-synthetic.json`.

This is **input consistency**, not verification that an actual Agent loaded only those Skills. Original Soodles owner must independently capture the real worker's effective catalog and retain exact raw provenance; public CLI reports `actual_worker_skill_discovery_verified=false` and `original_owner_capture_verified=false`.

## Noodle integration and replaceability

The former auxiliary Noodle control repository has been deleted and is **not** a valid source for current runtime, provider locks, worker Skill paths, permissions or carrier readiness. For active behavior, read the selected Noodle carrier and its actual launch/Skill discovery through the authorized Soodles original Owner. Current Soodles `execute/SKILL.md` still uses `poteto-mode` as the default Whole-Issue Engineering Entry; this does **not** prove that Builder, HumanLayer or other Factory roots are currently admissible. The selected Carrier may be replaceable only after a real independently admitted alternative meets the same source, session, Worktree and owner-readback controls.

Before a native admission, Soodles must independently select and pin the Factory Profile and actual Worker Carrier, then verify the exact installed Skill set is discoverable in the worker itself. Only the host may produce immutable authorization and exact continuation (`next.argv`, `next.environment`); never let a Factory Profile, candidate Writer or Skills Installer grant these.

For alternative Carrier adoption, require same Work Order and acceptance oracles, but keep Carrier-specific launch, Session, Worktree, resume, release and external Owner readback in a real, independently admitted Host adapter. An `other-worker` ID in a fixture establishes **schema openness**, not runtime replacement.

## Initial negative experiments

Public tests use two synthetic profiles: pstack-like and Builder-like. They assert no mixed workflow roots, no inherited global skills, no swapped pin, no overlapping/reused declared Worktrees or Sessions, and refusal when required Carrier capability is absent. A **real disposable Git repository** spawns two Git Worktrees in CI: each has its own untracked file and separate Git directory, while both deliberately share the same common Git object directory. This proves filesystem separation **in that temporary Git fixture only**; it is not a real Noodle run or OS isolation test.

## Current integration boundary

The public Worktree Profile contract is a separate, Draft PR based on unmerged Bootstrap PR #3. Draft Portable Skills PR #9 packages the earlier Bootstrap CLI and does not yet include this new Profile verifier. Rebuild the public distribution only after a verified accepted source tree exists; do not conflate successful portable installation with **Worktree-scoped factory activation**. The original Soodles #300 concerns a separate adapter and must retain its own supervision and Owner gate.
