# Compatibility Matrix — proposed interfaces vs actual proof

The **Agent Skills SKILL.md format** is portable; an end-to-end software factory integration is **not** established just because a skill can be loaded. Every row below requires a separate pinned scenario, source and host-owner receipt before it can be promoted.

| Upstream | Exact contract seam | Current verification | Required live proof |
|---|---|---|---|
| Matt Pocock `grilling` | human-answer / frontier -> DEC / REQ | representative fixture only | observe upstream skill output; user actually answers; no model-supplied substitute |
| Matt `grill-with-docs` | ADR / vocabulary -> DEC / SPEC | design only | pinned upstream version, extracted ADR, round-trip preservation |
| Cursor pstack | selected playbook -> workflow method receipt | design only | host-provided method selection and actual task verification |
| Builder.io Agentic Factory | bug evidence and verified PR -> REQ / V | design only | source+head/CI/PR provider receipt from original owner |
| Impeccable | design findings -> SPEC / V | design only | run deterministic detector/inspector on pinned UI and capture actual result |
| HumanLayer design-control-loop | sensor/controller/actuator -> typed work order | design only | real sensor reading and independent readback after action |
| GitHub Spec Kit | spec/extension bundle -> typed contract | design only | pinned installed extension or artifact and round-trip test |
| Private Soodles | typed REQ / ActionRequest -> original owner | PRIVATE ADAPTER NOT INCLUDED | trust-boundary and owner admission tests; no secrets or effects in public repo |
| Generic independent Auto-PR | typed REQ and receipt | design only | second actual consumer with exact head and independent evidence |

## Important invariants

- Proposal != authority. A `READY_FOR_IMPLEMENTATION` projection is a **proposal** for a registered consumer; never execute `argv` from cards.
- Source statements != tested observations. The version of an upstream skill must be frozen before a compatibility claim.
- Upstream ownership is respected. Example: `grilling` explicitly waits for the user's answers; we cannot resolve its questions automatically.
- No blanket cross-host compatibility claim: passing fixture schema tests covers only the local read-only reference CLI.
- Skills are instructions; workflow engines own resumability, effects, retries and provider truth.

References:
- https://agentskills.io/specification
- https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md
- https://github.com/cursor/plugins/tree/main/pstack
- https://www.builder.io/blog/build-an-agentic-software-factory-starting-with-one-bug
- https://github.com/pbakaus/impeccable
- https://github.com/humanlayer/skills
- https://github.github.io/spec-kit/