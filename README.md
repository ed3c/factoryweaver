# FactoryWeaver

**From Requirements to Verified Software.**

FactoryWeaver is a proposed portable **factory contract and evidence exchange layer** for Agent Skills and software factories. It connects product/job requirements, specifications, SKILL.md workflows, and scoped verification receipts **without taking ownership of a host's runtime, privileges, PR writes, or merge decisions**.

> Status: 0.1.0 experimental reference preview. This is an experimental public repository reference implementation, **not** an accredited standard, an auto-PR execution engine, or a proven integration with the third-party tools listed below.

## What is in this repository?

- `skills/factoryweaver/`: human/agent entrypoint; routes to compiler/verification skills.
- `skills/factoryweaver-compile/`: source-constrained requirement and Zettelkasten specification compilation.
- `skills/factoryweaver-verify/`: checks typed contracts and proof honesty; does not execute auto-PR.
- `contracts/v1/knowledge-record.schema.json`: JSON Schema Draft 2020-12, adapted from a private-reference v7.2 design **without private Soodles implementation or traces**.
- `scripts/factoryweaver.py`: `validate`, `project`, `route`, `cards` commands. Read-only; no shell or network execution. The optional `--registry` only checks a host-proposed capability index; it cannot grant rights.
- `examples/`: official-job and Matt Pocock `grilling` data examples, not evidence of third-party interoperability.
- `docs/compatibility.md`: compatibility matrix with separate contract vs runtime status.
- `docs/naming-gate.md`: preliminary name search findings and unresolved legal/package checks.

## Quick start

```bash
python3 -m pip install 'jsonschema>=4.20,<5'
python3 scripts/factoryweaver.py validate examples/openai-plugin-platform/project.json
python3 scripts/factoryweaver.py project examples/matt-grilling/project.json
python3 scripts/factoryweaver.py route examples/openai-plugin-platform/project.json --registry examples/host-registry.example.json
python3 scripts/factoryweaver.py cards examples/openai-plugin-platform/project.json
python3 -m unittest discover -s tests -v
```

## Factory Profile Lock (Issue #12 candidate)

The portable [Factory Profile Lock](docs/factory-profile-lock.md) describes exactly **one outer Factory workflow entry per Work Order**, pinned Skill allowlists and replaceable Worker Carrier **requirements**. It cannot start Noodle, select a real Soodles Supervisor or prove physical Worktree isolation from a claimed Session manifest. Public synthetic pstack/Builder examples are illustrative, not imported third-party implementations.

```bash
python3 scripts/factory_profile.py validate examples/factory-profiles/pstack-synthetic.json
```

## Architecture

```text
Job description / external docs / issue / observed code / human decision
                           |
           source and dependency evidence (untrusted data)
                           |
            Zettelkasten Compiler v7.2
                  |                 |
             human cards     machine REQ / SPEC
                  |                 |
                  +------ typed exchange -------+
                                                 |
                                  deterministic projection
                                                 |
                                   proposed capability request
                                                 |
                 Host-owned adapter, authorization and actual readback
                          /                                  \
              Soodles (private)                   independent Auto-PR system
                          \                                  /
                       evidence-bound consumer receipt
                                       |
                        invalidation + card status update
```

The reference CLI intentionally rejects `TESTED_SCOPED`, `ACTIVATED`, `RELEASE_CONFIRMED` and claimed executed actions until a trusted consumer adapter can bind raw artifacts and attestations. It is a safety-first **contract preview**, not a complete receipt-verifying production implementation.

The public library does **not** call external skills, infer that they exist on a host, or run shell commands from structured requests. The host must register and execute adapters under its own policy. Capability readiness never grants effects.

## Scope and design constraints

- **Skill autonomy preserved**: upstream `grilling` recommendations are not decisions until the human answers; pstack chooses its own playbook; design-audit skills retain their domain decisions.
- **Unknown is schedulable**: unresolved fact becomes a Knowledge Gap and a proposed read or prototype; no invented commands.
- **Dependency DAG**: unresolved requirement prerequisites and active K/X card dependencies project `WAIT_FOR_PREREQUISITE`, never `READY_FOR_OWNER_REVIEW`; cycles among requirement dependencies are refused.
- **Transitive prerequisites**: requirement readiness is derived through the complete acyclic REQ dependency chain, so an upstream unconfirmed human answer or missing Source Pin blocks downstream review even when downstream prose says `SPECIFIED`.
- **Capability proposals are requirement-scoped**: a `validate_specification` or `observe_owner` request must name its `target.requirement_id`; unknown or blocked IDs cannot yield even a registered candidate. `resolve_unknown` may still propose bounded read-only retrieval for missing information. Neither a registry declaration nor a ready requirement grants effect authority.
- **Source pins**: original URLs are `UNPINNED` until exact bytes are captured with SHA-256; an owner cannot receive a falsely source-pinned task.
- **Human confirmation**: the reference CLI rejects every `human_confirmed: true` claim. Even a `human_decision` source with a well-formed SHA-256 is untrusted self-attestation unless an independent host validates the actual human input. Real Grilling confirmation requires a separately verified host adapter; this preview supports `WAIT_FOR_HUMAN` only.
- **Three progress axes**: knowledge, engineering, and delivery are independent. Code existing is not verified behavior. Local fixtures are not released products.
- **Trusted progress boundary**: aggregate `progress` fields are input data, not verified receipts. The public CLI accepts only preview-level states and refuses `TESTED_SCOPED`, `ACTIVATED` and `RELEASE_CONFIRMED` summaries; a future independently verified host adapter must attest any stronger claim.
- **Evidence independence**: statements quoted in one document are not two independent corroborations. Source links default to `UNPINNED`; only captured exact bytes with a SHA-256 can be described as source-pinned.
- **Read-only reference CLI**: only validates, projects, routes and renders records. It **never performs** an operation from `operation_id`.
- **Personal / proprietary data**: do not publish private repository contents, internal issue/PR numbers, API keys, access tokens, session logs or test traces. Consumer-specific adapters belong in consumer repositories.

## Ecosystem relationships

Works *toward* cross-system interoperability with [Open Agent Skills](https://agentskills.io/specification), [GitHub Spec Kit](https://github.com/github/spec-kit), [Matt Pocock Skills](https://github.com/mattpocock/skills), [Cursor pstack](https://github.com/cursor/plugins/tree/main/pstack), [Impeccable](https://github.com/pbakaus/impeccable), [HumanLayer Skills](https://github.com/humanlayer/skills) and [Builder.io Factory](https://www.builder.io/blog/build-an-agentic-software-factory-starting-with-one-bug). **These are upstream references, not endorsers, dependencies, copied skill bundles or validated hosts.**

The core is intentionally not a replacement for Spec Kit's specifications, Skill loaders, CI or Auto-PR execution. The missing layer is independently checkable producer/consumer evidence and owned-effect boundaries.

## Licensing

Original contents: MIT (see LICENSE). Third-party projects and files are not vendored. Referenced names and trademarks belong to their owners.