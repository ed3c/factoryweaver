# Portable distribution reconciliation

The parent Goal is all FactoryWeaver feature parity on current main, followed by
NeoWeaver recompilation. This unit reconciles Issue #8 / PR #9 through PR #22.

The first unsupported premise was that a self-consistent manifest implied that
current v7.2 Skills could resolve their dependencies. The old installer verifier
also assumed the obsolete flattened layout. Producer is the canonical source
builder; Consumer is the directory-copy installer and installed reference CLI.
Canonical Skills remain unchanged inside a portable repository root. A root
loader preserves one-directory installation. Dependency closure includes the
real local verification harness and its declared sources. Normal importing CLI
commands avoid bytecode cache writes that would break exact replay.

Positive controls cover foreign-root CLI use, full reference resolution,
identical build NOOP and copied-layout verification. Negative controls cover
missing inputs, altered bytes, extra files, symlink roots and partial installation.
The pinned skills@1.7.1 copy installer was exercised locally. Current-head CI
must independently exercise it before merge.

Knowledge truth, native Agent instruction compliance, Soodles admission,
Noodle execution and Manager effects are NOT_RUN. Local maintenance is only
LOCAL_CLI_BEHAVIOR_ONLY; full maintenance retains the original native gaps.
No local PASS grants effects. GitHub merge is a separate provider operation.

Accepted v7.2 main added pinned pstack sources. Including their required local
references and original license follows that newer accepted source rather than
silently treating Issue #8's older no-third-party premise as current.
