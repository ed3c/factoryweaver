# factoryweaver writing entrypoint

This repository currently has no local writing skill or executable writing
pipeline. Do not claim that review-writing or sloptrim is installed here.

For engineering-facing text (requirements, implementation notes, architecture,
runbooks, Agent contracts or evaluations), use the source
[Soodles review-writing skill](https://github.com/ed3c/soodles/blob/main/.agents/skills/review-writing/SKILL.md).
Preserve facts, causality, runtime actors, state transitions, failure branches,
authority and immutable code/evidence. P-class Agent-behavior feedback applies
only when P-class guidance changes. Use the current task's selected source
revision and record when the external skill is unavailable.

For human-facing articles, route writing through
[medium-writing](https://github.com/ed3c/medium-compiler/blob/main/.agents/skills/medium-writing/SKILL.md).
Complete the English article, check that English prose with the upstream
[sloptrim](https://github.com/seyedehsanhadi/sloptrim) skill, and verify each
change against its sources. Translate only the approved English text into
Traditional Chinese, retaining exact English technical terms. Compare source,
English and Chinese for omissions, negation, modality, attribution, quantities,
causality and technical behavior. Sloptrim's style score is not evidence of
truth or authorship. Record a missing tool as NOT_RUN, never as a PASS.

Do not add a scheduler, editing engine, style CI gate, or publishing effect
because this routing document exists. Preserve the exact review/delivery owners
and authorization of the actual task.
