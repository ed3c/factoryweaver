# Standalone FactoryWeaver Skill — generated distribution

FactoryWeaver is a **source repository plus an installable one-directory Skill**. Its source-layout Skills currently share root-level scripts, JSON Schemas and reference files. Copying only `skills/factoryweaver/` from the source checkout is **not a complete installation**.

## Build and locate the standalone bundle

From the canonical FactoryWeaver source checkout at a pinned Git revision:

```bash
python3 -m pip install 'jsonschema>=4.20,<5'
python3 scripts/build_skill_bundle.py .dist/factoryweaver
```

After generating the folder, run `python3 scripts/check_bundle.py .dist/factoryweaver` to verify every bundled file against its generated manifest. The result is **self-consistency only**; the manifest can be forged along with the files and does not authenticate the publishing host or Git commit.

The output folder has `SKILL.md`, `references/compiler.md`, `references/verifier.md`, local Zettelkasten/compatibility documentation, `contracts/v1/`, `scripts/factoryweaver.py`, examples, `LICENSE` and a content-bound `bundle-manifest.json`. All generated files come from canonical source: no parallel manually maintained reference implementations.

**Install** by copying the **whole generated `factoryweaver/` folder** into the Agent's supported Skill location, for example a repository's `.agents/skills/factoryweaver/` or another supported Skill directory. The host decides how to load Skills and whether to allow this code; formatting the bundle is not a runtime permission grant.

```bash
python3 .agents/skills/factoryweaver/scripts/factoryweaver.py validate \
  .agents/skills/factoryweaver/examples/matt-grilling/project.json
python3 .agents/skills/factoryweaver/scripts/factoryweaver.py project \
  .agents/skills/factoryweaver/examples/matt-grilling/project.json
```

**Verified bounded installer route:** GitHub Actions installs the generated directory using pinned `skills@1.7.1` (Vercel Skills CLI), with `npx --yes skills@1.7.1 add ../factoryweaver --skill factoryweaver -a codex -y --copy` from a separate temporary consumer. It then runs the **installed** Skill's bundled verifier and CLI, including the `WAIT_FOR_HUMAN` case. This proves installer copy behavior in the CI Codex target layout, **not** a live Codex Agent loading, prompting, or taking actions. See [Actions run 37830628483](https://github.com/ed3c/factoryweaver/actions/runs/37830628483) at candidate head `6b7da05f830338ddfa179b5ebfa44ed908bcecea` (historical run; always use current exact-head run for final claims).

**Do not advertise** `npx skills add ed3c/factoryweaver` as a verified direct GitHub-main install route. The generated bundle is produced in the pinned GitHub Actions PR workflow and uploaded as `factoryweaver-portable-reference`, or can be built locally.

## Local and CI proof

The isolated installation tests:
- build under an unrelated temporary project root;
- run four CLI subcommands without any parent-repository scripts or schemas;
- enforce deterministic repeat (same manifest digest, `NOOP`);
- refuse a missing canonical input, tampered generated file, or unexpected distribution content;
- ensure no symlink or private runtime implementation was copied;
- confirm `WAIT_FOR_HUMAN` cannot become an inferred human decision.

CI runs these tests and then generates a complete bundle as an unprivileged artifact. **The artifact proves only packaging and the public reference CLI**, not Agent tool discovery, external Skill execution, Soodles/Noodle admission or a real Auto-PR PR/merge.

## Security / owner boundary

This bundle cannot obtain or inherit credentials, external provider readbacks, filesystem actions beyond its explicitly requested output directory, Noodle writers, GitHub PR permissions or merge authority. The adapter registry only proposes read-only candidates. Missing original-owner authority remains `BLOCKED`.

The build writes to a destination chosen by the caller. Refuse ambiguous reuse: an already existing folder must match the exact generated file list and bytes to produce `NOOP`; drift requires an explicit new build destination. Neither `SKILL.md` text nor a bundle manifest grants trust.
