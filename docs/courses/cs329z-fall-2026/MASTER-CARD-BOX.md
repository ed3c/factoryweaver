# CS329Z MASTER CARD BOX · Whole-Course Knowledge Graph

> **The integrated course-wide Zettelkasten note**, not just a directory. Knowledge is organized by 11 weekly chapter roots, their Slides/Readings/Homework sub-boxes, and reusable Goal-oriented Behavior Scopes. Card claims remain **SCHEDULE_ONLY** until reading/slide evidence is inspected; effect evidence remains NOT_RUN.

## Whole-course Goal Contract

- **Goal:** choose, build, measure, improve and safely operate a correctly-scoped Agentic System that meets the *actually released* homework or project criteria.
- **Measurement:** source→REQ coverage, real HW tests and project objective metrics returned by the authoritative data/verification owner; course grades or test results are never guessed.
- **Persistence:** Boot the complete source inventory; incrementally Drill by chapter/source in bounded batches when source, dependencies or validation gaps actually change. Keep original goals across separate Issue Atoms.
- **Stop / Escalation:** compilation complete ≠ graded HW PASS or Runtime delivery; keep unread material, missing HW2 handout and owner-readback effects K until resolved.

## Chapter-card integration

| Chapter | Reusable conceptual bridge | Chapter-level Behavior Scope | Source notebooks |
| --- | --- | --- | --- |
| [Week 1 · Foundations](chapters/week-01-foundations/cards.md) | Monolithic/Compound/Agent → Decision-oriented decomposition | Choose only necessary agent complexity | [Slides](chapters/week-01-foundations/slides/cards.md) · [Readings](chapters/week-01-foundations/readings/cards.md) · [Homework](chapters/week-01-foundations/homework/cards.md) |
| [Week 2 · LLMs & RAG](chapters/week-02-llm-and-rag/cards.md) | Constrained generation & context → Grounding & retrieval | Ground corpus answers through verifiable retrieval | [Slides](chapters/week-02-llm-and-rag/slides/cards.md) · [Readings](chapters/week-02-llm-and-rag/readings/cards.md) · [Homework](chapters/week-02-llm-and-rag/homework/cards.md) |
| [Week 3 · Tools & Frameworks](chapters/week-03-tools-and-frameworks/cards.md) | Tool schema and validation → Framework abstraction boundary | Execute a typed tool without accepting untrusted authority | [Slides](chapters/week-03-tools-and-frameworks/slides/cards.md) · [Readings](chapters/week-03-tools-and-frameworks/readings/cards.md) · [Homework](chapters/week-03-tools-and-frameworks/homework/cards.md) |
| [Week 4 · Agent Patterns & Memory](chapters/week-04-patterns-and-memory/cards.md) | Agent loop and control → Durable memory and recovery | Maintain correct conversation state and bounded tool loops | [Slides](chapters/week-04-patterns-and-memory/slides/cards.md) · [Readings](chapters/week-04-patterns-and-memory/readings/cards.md) · [Homework](chapters/week-04-patterns-and-memory/homework/cards.md) |
| [Week 5 · Multi-agent & Optimization](chapters/week-05-multiagent-optimization/cards.md) | Stateful delegation → Matched optimization/ablation | Show added complexity brings measured benefit | [Slides](chapters/week-05-multiagent-optimization/slides/cards.md) · [Readings](chapters/week-05-multiagent-optimization/readings/cards.md) · [Homework](chapters/week-05-multiagent-optimization/homework/cards.md) |
| [Week 6 · Agent Data](chapters/week-06-agent-data/cards.md) | Traces and demonstrations → Feedback/data flywheel | Capture evidence for subsequent error analysis | [Slides](chapters/week-06-agent-data/slides/cards.md) · [Readings](chapters/week-06-agent-data/readings/cards.md) · [Homework](chapters/week-06-agent-data/homework/cards.md) |
| [Week 7 · Data Quality & Benchmarking](chapters/week-07-data-evals/cards.md) | Data selection and labeled failures → Four-tuple evaluator | Build a realistic error-sensitive benchmark | [Slides](chapters/week-07-data-evals/slides/cards.md) · [Readings](chapters/week-07-data-evals/readings/cards.md) · [Homework](chapters/week-07-data-evals/homework/cards.md) |
| [Week 8 · Judge & Safety](chapters/week-08-judge-safety/cards.md) | Judge reliability → Prompt injection/consent boundary | Reject unsafe effects and faulty judge conclusions | [Slides](chapters/week-08-judge-safety/slides/cards.md) · [Readings](chapters/week-08-judge-safety/readings/cards.md) · [Homework](chapters/week-08-judge-safety/homework/cards.md) |
| [Week 9 · Coding Agents](chapters/week-09-coding-agents/cards.md) | Agent-computer interface → Observed coding-agent lifecycle | Close a bounded coding change using real owner evidence | [Slides](chapters/week-09-coding-agents/slides/cards.md) · [Readings](chapters/week-09-coding-agents/readings/cards.md) · [Homework](chapters/week-09-coding-agents/homework/cards.md) |
| [Week 10 · Thanksgiving Recess](chapters/week-10-recess/cards.md) | NOOP (recess) → no new card | No new atom | [Slides](chapters/week-10-recess/slides/cards.md) · [Readings](chapters/week-10-recess/readings/cards.md) · [Homework](chapters/week-10-recess/homework/cards.md) |
| [Week 11 · Proactive Agents & Frontiers](chapters/week-11-proactive-frontiers/cards.md) | Proactive action thresholds → Observability and long-running recovery | Trigger only a justified consented action | [Slides](chapters/week-11-proactive-frontiers/slides/cards.md) · [Readings](chapters/week-11-proactive-frontiers/readings/cards.md) · [Homework](chapters/week-11-proactive-frontiers/homework/cards.md) |

## Cross-chapter graph (proposed semantic link types)

- **W1 → W2** `enables`: decomposition criteria determine whether retrieval belongs in the system.
- **W2 → W3** `depends_on`: grounded retrieval through tools depends on typed execution and source validation, while homework BM25 remains lexical when its tests require it.
- **W3 → W4 → W5** `enables`: reliable tool results, memory and state continuity precede delegation; multi-agent orchestration increases failure possibilities.
- **W5 → W6 → W7** `enables`: observed behaviors/traces precede valid datasets, and datasets precede evaluator/scorer conclusions.
- **W7 → W8** `validated_by`: an LLM Judge needs failure-specific controls; source code handles objectively decidable guardrails.
- **W8 + W3 → W9** `depends_on`: coding agents must respect tool permission and observed owner lifecycle, not generated text.
- **W4 + W7 + W8 + W9 → W11** `depends_on`: proactive agents need durable memory, measurements, safe authorization and controllable effects.
- **W10** Thanksgiving Recess: NOOP, no invented knowledge cards.

These are **semantic graph proposals**. Register real card IDs/versions through the existing Host/CLI, not model-produced strings. The v1 schema does not have a `constrains` relation; only use supported typed links for materialized records.

## Course-wide Behavior Scope portfolio

| Proposed Issue Atom | Goal | Measurement | Knowledge prerequisites | Outer Skill Route |
| --- | --- | --- | --- | --- |
| Retrieval/grounding | Answer with verified supporting evidence | HW1 BM25/QA tests | W1+W2 | `issue-atom`, Test Manager; Thinking Router only on real gap |
| Safe tools | Reject invalid and unauthorized effects | HW1 Tool Registry/Agent tests | W2+W3+W8 | `issue-atom`; safety controls; concrete `outer-review` if needed |
| Memory & continuation | Preserve only the required long-term context and no duplicate write | HW1 scripted memory cases | W3+W4 | issue-atom; conditional `think` for architecture |
| Trace data | Record useful failure evidence without conflating sources | trace completeness by original producer | W5+W6 | issue-atom; Test Manager |
| Valid evaluator | Distinguish actual failure modes and judge errors | held-out cases and verified scorer | W6+W7+W8 | conditional installed Evals / ablation; no judge for trivial code facts |
| Reliable coding agent | Bounded code change, accepted and receipted | provider readback / exact-head CI | W3+W8+W9 | issue-atom; `outer-review` only if actual candidate |
| Governed proactive action | Act on true trigger with consent, stop and recovery | native trigger and actual owner receipt | W4+W7+W8+W9+W11 | Hook/Cron only when original carrier requires |

**Inner loop:** Noodle Poteto consumes **bulleted semantic Prompt Delta requirements** for each actually admitted atom and chooses its engineering implementation freely within the fixed Scope. **Outer loop:** Soodles chooses/loads skills, maintains goals, measures outcomes, consumes owner next and handles publication/landing. This Master does not grant those effects.

## Coursework acceptance and cross references

- [HW1 · Build an Agentic Harness](coursework/HW1.md): W2 retrieval, W3 tools, W4 memory, W8 guardrails. Existing [source-bound HW1 Pilot](../../evals/cs329z-hw1/README.md) is a structural fixture, not an Agent behavior result.
- [HW2 · Evaluate an Agent](coursework/HW2.md): W6 trace data, W7 benchmark, W8 judges. Exact handout **unreleased as of 2026-10-13**.
- [Final Project](coursework/FINAL-PROJECT.md): choose one verified business/system outcome; do not force all course methods into a single Agent.

## Lossless Drill-down source backlog

- **K-slides:** five PDF links listed (lectures 01–05); no slide-page claims until PDFs are inspected.
- **K-readings:** 50 required/additional reading links listed; title-level questions await whole-paper source validation.
- **K-guest:** guest lectures scheduled TBA. No fabricated summaries.
- **K-HW2:** upcoming handout may change exact tests and submission requirements.
- **K-runtime:** no course-level real Soodles/Noodle execution, model judge, provider receipt or verified learning outcome is claimed.

[Course map](COURSE-MAP.md) · [Source registry](SOURCE-REGISTRY.md) · [Index](README.md)
