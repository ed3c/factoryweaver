# v7.2 Selective Card Generation Prompts

This registry is the **single source of truth** for the 15 Card Series and their **distinct semantic fields**. Use exactly one unified [FactoryWeaver entry](../../skills/factoryweaver/SKILL.md). The v7.2 [Overall Prompt](../zettelkasten-v7.2.md) supplies global invariants, not a forced N/C/T/REQ/SPEC order. Only load the [specific Card Type prompt](types/) selected by the source's epistemic role. A batch of four changes can have any real mix; do not fill unused slots with fabrications.

## Read path

1. Resolve original task, source content/coverage and accepted previous registry with current Host.
2. Read the v7.2 Overall Prompt once and [Card Classification](../card-classification-and-scope-assembly.md); preserve Source Fidelity, I-01 and Authority.
3. Select Card Types by observed independent decision need, then load only the corresponding registry entries and `types/{series}.md`.
4. Render source-supported fields and actual links; reuse existing G/C or NOOP when no information improves.
5. Apply [Soodles review-writing](https://github.com/ed3c/soodles/blob/main/.agents/skills/review-writing/SKILL.md) to engineering prose when installed. P-class *instruction* changes need affected Agent behavior evals; P Practice card edits do not.
6. Verify typed semantic draft via `scripts/card_semantic.py`, then original v1 JSON `factoryweaver.py validate` **after Host materialization**. Neither proves source truth. An independent semantic reviewer handles causality and omissions.
7. Assemble one causal Scope (Goal / Measurement / Persistence / Stop), emit bounded four sidecars ScopeManifest/SkillRoute/PromptDelta/Continuation as proposals. The original Soodles owner decides effect and test/hook selection.

**Source types:** Slides, documents, images, tables, audio/transcripts, video, code, Logs, Traces and receipts first require real Host extraction of relevant units. A URL alone is not inspected source. A complete coverage ledger links decision-relevant source units to cards, requirements or named K; the model cannot prove it has captured every unread source unit.

**Do not make the 15 prompt files System-role authority:** they are plain reference instructions loaded through the active Host's Skill. Do not replace higher-priority Host instructions or grant execution permission.
