# Standalone FactoryWeaver Skill — generated distribution

FactoryWeaver is a **source repository plus an installable one-directory Skill**. Its source-layout Skills currently share root-level scripts, JSON Schemas and reference files. Copying only `skills/factoryweaver/` from the source checkout is **not a complete installation**.

## Build and locate the standalone bundle

From the canonical FactoryWeaver source checkout at a pinned Git revision:

```bash
python3 -m pip install 'jsonschema>=4.20,<5'
python3 scripts/build_skill_bundle.py .dist/factoryweaver
```

After generating the folder, run `python3 scripts/check_bundle.py .dist/factoryweaver` to verify every bundled file against its generated manifest. The result is **self-consistency only**; the manifest can be forged along with the files and does not authenticate the publishing host or Git commit.

The output is a portable virtual repository root. Its installer entry is `SKILL.md`, a short loader for
`skills/factoryweaver/SKILL.md`. The three canonical Skills keep their exact bytes
and relative paths. The bundle contains the public CLI, schemas, examples and
transitive local Markdown references, including the v7.2 per-type prompts.

Copy the whole generated directory to a Host-selected location. Configure the
Host to load `skills/factoryweaver/SKILL.md` inside that directory. A loader that
copies only the leaf Skill directory loses root-owned dependencies. The top-level loader also lets a directory-copy installer preserve the whole root.

```bash
python3 scripts/verify_installed_skill.py /absolute/installed/factoryweaver
python3 /absolute/installed/factoryweaver/scripts/factoryweaver.py project \
  /absolute/installed/factoryweaver/examples/matt-grilling/project.json
```

The installed verifier observes the copied layout and runs its checker and
reference CLI. It does not observe installation by an external installer or
native Agent loading. The old flattened-bundle installer receipt does not verify this layout.
Current CI runs the pinned `skills@1.7.1` installer against the generated local
directory in a foreign consumer and verifies the installed files. Direct
`npx skills add ed3c/factoryweaver` and native Agent behavior remain `NOT_RUN`.

Accepted v7.2 main vendors pinned pstack references. Their transitive instructions
and original MIT license are included because the canonical entry requires them.
This supersedes the older Issue #8 no-third-party-bundle premise with the
accepted v7.2 source; it does not establish invocation of those methods.

## Local and CI proof

The isolated installation tests:
- build under an unrelated temporary project root;
- run four CLI subcommands without any parent-repository scripts or schemas;
- enforce deterministic repeat (same manifest digest, `NOOP`);
- refuse a missing canonical input, tampered generated file, or unexpected distribution content;
- ensure no symlink or private runtime implementation was copied;
- confirm `WAIT_FOR_HUMAN` cannot become an inferred human decision.

CI runs these tests and generates a complete bundle as an unprivileged artifact. **The artifact proves only packaging and the public reference CLI**, not Agent tool discovery, external Skill execution, Soodles/Noodle admission or a real Auto-PR PR/merge.

## Security / owner boundary

This bundle cannot obtain or inherit credentials, external provider readbacks, filesystem actions beyond its explicitly requested output directory, Noodle writers, GitHub PR permissions or merge authority. The adapter registry only proposes read-only candidates. Missing original-owner authority remains `BLOCKED`.

The build writes to a destination chosen by the caller. Refuse ambiguous reuse: an already existing folder must match the exact generated file list and bytes to produce `NOOP`; drift requires an explicit new build destination. Neither `SKILL.md` text nor a bundle manifest grants trust.
