---
name: factoryweaver-compile
description: Convert job descriptions, project requests, existing specs and confirmed human decisions into evidence-anchored Zettelkasten v7.2 REQ and SPEC records. Use before coding when requirements, ownership, acceptance or unknowns need explicit machine-readable contracts.
license: MIT
---
# Zettelkasten Specification Compiler v7.2

1. Read `../../references/zettelkasten-v7.2.md` for compiler invariants and human-readable card forms.
2. Keep sources, provenance, evidence and decisions separate from the resulting cards.
3. For each meaningful requirement map actor, capability, outcome, non-case, precondition, falsifier, owner, acceptance and source locator. For a JD or comparable enumerated source, maintain an explicit clause inventory and run `python3 scripts/requirement_coverage.py RECORD.json CLAUSES.json` to expose omitted clauses; read `../../docs/requirement-coverage.md`. A declared REQ link is not proof of semantic fidelity or runtime delivery.
4. Build typed REQ, SPEC, K, X, V cards when evidence permits. Never force every card family to appear.
5. For unresolved human questions, keep `decision=null`, `human_confirmed=false`, and `WAIT_FOR_HUMAN`.
6. Write a `contracts/v1/knowledge-record.schema.json`-conforming data record. Verify using `python3 scripts/factoryweaver.py validate FILE` from repository root.
7. Run `project` to read the deterministic requirements status; submit any proposed capability request to host's adapter registry for independent authorization.
8. On repeated unchanged sources emit NOOP; preserve stable IDs, valid links and unresolved blockers.
9. Render readable cards with `cards`; output content-first, with evidence and explicit missing knowledge.

Compilation is not live execution. Do not add `TESTED` or `RELEASE_CONFIRMED` without external artifacts and the original owner's readback.