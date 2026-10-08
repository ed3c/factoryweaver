# Source Lock — original-owner bytes, not self-attested citations

Issue #4 requires raw, stable evidence anchors rather than treating a URL, a GitHub branch label or plausible-looking SHA-256 as confirmed source content.

## Verified reference to a genuine upstream Skill

Read-only GitHub connector inspection (2026-10-09) found:

- Repository: [mattpocock/skills](https://github.com/mattpocock/skills).
- Commit-scoped path: [grilling/SKILL.md at b0618bc436ad893b3c5e84e55fba86586d34a404](https://github.com/mattpocock/skills/blob/b0618bc436ad893b3c5e84e55fba86586d34a404/skills/productivity/grilling/SKILL.md).
- Git blob SHA-1 returned by GitHub file reader: `df69d9936880cd3314c28858c6c52f48db23b856`.
- High-signal anchor substrings: `The decisions are the user's`; `wait for the user's answers before the next round`.

This is an external source reference and observed blob identity, **not** evidence that FactoryWeaver ran Matt's Skill, interviewed a user, or captured a real human answer. The upstream Skill body is intentionally not copied into FactoryWeaver.

## Input and bounded CLI

An independently authorized retrieval Owner obtains the exact upstream raw bytes, records their origin and identity, and supplies those same bytes as UPSTREAM_SKILL.md with this manifest. The SHA-256 placeholder must be calculated from the raw file, never guessed.

```json
{
  "protocol": "factoryweaver/source-lock-v1",
  "repository": "mattpocock/skills",
  "revision": "b0618bc436ad893b3c5e84e55fba86586d34a404",
  "path": "skills/productivity/grilling/SKILL.md",
  "git_blob_sha1": "df69d9936880cd3314c28858c6c52f48db23b856",
  "sha256": "<computed SHA-256 from actual raw bytes>",
  "source_dependency_key": "mattpocock/skills/grilling",
  "anchors": [
    {"id": "human-decision", "text_match": "The decisions are the user's"},
    {"id": "frontier-wait", "text_match": "wait for the user's answers before the next round"}
  ]
}
```

Run locally after replacing the SHA-256 placeholder:

```bash
python3 scripts/source_lock.py source-lock.json UPSTREAM_SKILL.md
```

The read-only verifier computes exact Git blob SHA-1 over `blob <byte-length>\0<byte-content>`, computes SHA-256 over the same bytes, checks each anchor occurs exactly once, and refuses unpinned revision or path traversal.

Successful output is `SUPPLIED_BYTES_MATCH_FROZEN_MANIFEST` with `external_origin_authenticated=false` and `provider_readback_verified=false`. Hashing supplied bytes against supplied metadata does **not** independently prove the remote origin or the authorized retrieval owner.

## Refusals and evidence ceiling

Any mismatch, absent/repeated text match, invalid revision or path: exit 2; do not claim source-verifiable cards. A changed source requires a new accepted identity and dependency invalidation, not rewriting history. Original source Owner unavailable: `BLOCKED`. No shell execution, network retrieval, Git write, Noodle session, PR/merge authority or human-confirmation proof is performed by this verifier.

This is only a local **byte-consistency gate**, suitable as a necessary input to future owner-controlled source evidence. The complete v7.1 semantic and real upstream Grilling execution gates remain open.
