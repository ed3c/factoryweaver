# Worktree-local Skill inventory (read-only)

The `observe-local-skills` operation reads an existing, selected linked Git worktree at its pinned HEAD. It lists `.agents/skills` directories and checks each skill's sorted path-and-content digest against a Factory Profile allowlist. Extra, missing, altered or symlink-backed local skills are rejected.

The synthetic tests create two real, distinct Git worktrees with a pstack-like and Builder-like local Skill collection. They check local filesystem contamination, **not** a model run.

This check is NOT proof of the effective Agent Skill catalog: global, user-level and carrier-specific Skill paths may still be available. It also does not authenticate Noodle process/session ownership, isolate HOME/network/credentials, or grant PR effects. Soodles' original Supervisor must independently read the actual launched Worker Skill discovery and keep its authority boundary.

The legacy auxiliary control repository was deleted. Consult the currently authorized Soodles carrier and its real observations, not historical provider locks. Public FactoryWeaver validates records and local bytes only.
