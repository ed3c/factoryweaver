# CS329Z HW1 × FactoryWeaver v7.2 — first source-to-scope pilot

> **Status: SOURCE-BOUNDED GOLDEN FIXTURE / NOT A LIVE AGENT EVAL.** This assessment uses the currently published Fall 2026 Stanford course-source repository, public HW1 starter README and deterministic test source, plus accessible full-text RAG and MCP readings. The lecture PDF links exist but their actual slides **could not be opened/inspected** in the evaluation environment. The homework PDF handout also could not be extracted. No claims of slide-level coverage or complete handout fidelity are made. These are named `K` evidence gaps.

## 1. Goal-oriented pilot contract

- **Goal:** demonstrate that FactoryWeaver's unified `factoryweaver` entry can map the **current** Stanford HW1 sources to a whole-task requirement inventory, compile four substantive Boot cards, deliver four meaningful Drill-down card operations, select typed causal links, and compose bounded architecture-focused Issue Atom proposals without adding grading requirements from reading materials.
- **Measurement:** `factoryweaver.verify()` schema verification, `card_delta.compile_delta()` on the *frozen* Boot→Drill pair, source/requirement preservation tests, and independently reviewed semantic assertions about the upstream HW1 starter.
- **Persistence:** maintain all original HW1 requirements in the same ledger; add independent Drill rounds for uninspected handout/slides, tool protocol, memory, approval, sandbox only when source evidence becomes available. No forced extra cards or implicit background task.
- **Stop/Escalation:** schema and delta tests may PASS for the **fixture**. Full pedagogical source fidelity remains `PARTIAL` until lecture PDFs and official handout pages are inspected; live Skill behavior claims remain `NOT_RUN` until an actual host model invocation and independent evaluation capture.

**Primary source authority:** HW1 starter README, `adapters.py` signatures, `tests/test_bm25.py`, `tests/test_email_qa.py`, `tests/thresholds.py`. **Secondary knowledge:** lectures and research readings. Never turn secondary dense-retrieval, DSPy, MCP or vector-store patterns into mandatory homework behavior.

### Verified upstream source selection

| Source | Selected content | Role | Review status |
| --- | --- | --- | --- |
| [Stanford Coursework](https://github.com/cs329z/cs329z.github.io/blob/main/pages/coursework.md) | HW1 Build an Agentic Harness; raw chat completion and self-built logic | Assignment authority | READ |
| [HW1 Starter README](https://github.com/cs329z/assignment1-harness/blob/main/README.md) | Parts 1/2; adapter-only grading; deterministic/live tests; source edit boundary; basic safety | Assignment authority | READ |
| [BM25 tests](https://github.com/cs329z/assignment1-harness/blob/main/tests/test_bm25.py) | Exact toy scoring, archive retrieval, speed and recall | Code-based oracle | READ |
| [Email QA tests](https://github.com/cs329z/assignment1-harness/blob/main/tests/test_email_qa.py) | Answer/support response, only seen IDs, three search calls, malformed/no-result recovery | Code-based oracle | READ |
| [HW1 thresholds](https://github.com/cs329z/assignment1-harness/blob/main/tests/thresholds.py) | BM25 min recall@10=0.90 in `test_bm25.py`; live Email QA min accuracy=0.70 in thresholds | Acceptance definition, not observed result | READ |
| [Lecture 03 slides](https://web.stanford.edu/class/cs329z/slides/lecture03.pdf) | RAG according to official schedule | Slide source | LISTED, **PDF BODY NOT READ** |
| [Lecture 04 slides](https://web.stanford.edu/class/cs329z/slides/lecture04.pdf) | Tool Use & Function Calling according to official schedule | Slide source | LISTED, **PDF BODY NOT READ** |
| [RAG paper (Lewis et al.)](https://ar5iv.labs.arxiv.org/html/2005.11401) | Parametric generator, non-parametric retrieval; RAG-Sequence/Token, Dense Index | Concept evidence, not grading spec | READ |
| [MCP Specification 2025-06-18](https://modelcontextprotocol.io/specification/2025-06-18) | Tools/Resources/Prompts, Hosts/Clients/Servers, consent | Architecture knowledge, not required HW1 implementation | READ |
| [Anthropic: Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) | Workflow vs Agent, composability, right level of complexity | Design tradeoff evidence, not required HW1 implementation | READ |

### Version-conflict control

An older public course description referred to a **research-paper agent with DSPy** and even a different number of assignments. The published current Coursework and linked `cs329z/assignment1-harness` starter identify the **corporate email assistant without frameworks**. Treat old and current claims as an `X` source-version conflict; select the actual assigned current HW1 and retain the conflict history. Do not silently combine both assignments.

## 2. Lossless Boot batch: four substantive cards

The machine fixture is [boot.json](boot.json). **Four displayed cards do NOT limit the requirement inventory**: it retains 13 distinct HW1 outcomes, including priority, digest, BM25, QA, tools, loop, docs, memory, approval, guardrails, environment and evaluation.

1. **C — Retrieval Grounding.** Concept: retrieval offers inspectable external evidence to a generator; retrieved documents are not identical to parametric memory. Knowledge relation: `enables → REQ-email-qa`. **Non-case:** the paper's Dense Retriever is not an assignment mandate.
2. **G — Source Authority.** Concept: HW1 starter contract outranks illustrative lecture/research implementations. Relation: `mitigates → REQ-framework`. **Non-case:** MCP compliance or vector database is not required.
3. **REQ — Framework-free Harness.** Required outcome: self-built pipeline/agent logic, preserved provided interfaces. Relations: `implements → REQ-framework`, `depends_on → G-source-priority`.
4. **SPEC — Email QA.** Given an email question and returned search records, produce `answer` plus grounded `support` list; no unseen email IDs. Relation: `implements → REQ-email-qa`, `based_on → C-retrieval-grounding`.

**Pending beyond Boot:** BM25 exact ranking, malformed response handling, hop budget, independent verification, full tool/agent/memory/approval architecture, actual handout/slide pages and source-version conflict evidence.

## 3. Drill-down patch: four real operations

Machine fixture: [drill.json](drill.json). Exactly **two UPDATEs and two CREATEs**; no padding, no reprinting unrelated cards.

| Operation | Card | Real semantic gain | Link/coverage consequence |
| --- | --- | --- | --- |
| UPDATE | C — Retrieval Grounding | Distinguishes Lewis et al. Dense Wikipedia retrieval from homework BM25 | RAG reading becomes architectural background; BM25 test remains authority |
| UPDATE | SPEC — Email QA | Adds malformed/empty/repeated-search cases and explicit **three-search cap** | Adds `validated_by → V-email-qa` |
| CREATE | SPEC — BM25 | Adds separate algorithmic retrieval contract, top-k, tokenizer, ranking and performance controls | `implements → REQ-bm25`; depends on source-authority governance |
| CREATE | V — Email QA | Explicitly names positive/negative/unknown test conditions; live result **NOT_RUN** | Independent deterministic oracle maps to QA requirement |

**Why the scope decomposition matters:** BM25 scoring and Email QA are two causally separable changes, with a real producer/consumer dependency, so proposing one giant "Build RAG" Issue Atom would be too broad. Equally, splitting "search hops" and "support IDs" into different writer Issues would break one coherent Email QA acceptance boundary.

## 4. Linked software architecture specification

```text
[Corporate Email Archive]       [Company Documents]
          |                                |
    Corpus Loader                    Document Loader
          |                                |
    BM25 Build/Search                 Search / Read Doc
          |                                |
          +----------- evidence -----------+
                              |
                     Search Result Records
                              |
                 Email QA / Agent Controller
                              |
                     Plain Chat Completion
                              |
                 Answer + Returned Support
                              |
                  Deterministic Assertions
```

**Contract boundaries:**
- HW1 own code remains under `cs329z_hw1/`; the provided `adapters.py` signatures and types stay compatible. The grader replaces test files and supplied modules, so extra dependencies and copied tests do not establish implementation correctness.
- `run_bm25_build` and `run_bm25_search` form the retrieval producer; their deterministic test owns scorer correctness. `run_email_qa` consumes a `search(query, k)` function plus a plain `LMCallable` and returns an answer/support object. Test rules limit search hops and verify IDs against the calls in **this request**.
- Reading-informed architecture alternatives (Dense Index, vector store, MCP server, DSPy) are *excluded from required acceptance* unless newly authorized by actual homework handout or implementation requirements.
- Source documents/emails and tool results are untrusted content. The later Agent Scope separately handles deny rules, approval and sandbox, and must not mix retrieval evidence with execution authority.
- The paper does not prove the email QA threshold; achieving the configured minimum demands actual course live tests.

### Behavior Scope / Issue Atom A: deterministic BM25 retrieval

**Goal:** correct BM25 scoring and ranking for course-provided tests. **Measurement:** supplied deterministic toy-score, ranking, archive recall/time controls; the known target values come from course-provided tests, not forecasts. **Persistence:** fix this causal implementation under the same goal until tests pass or a justified prerequisite/cost blocker occurs. **Stop:** scoped controls pass with actual recorded outputs; this does not complete all HW1.

**Soodles Outer Loop:** `issue-atom` for contract boundary, Test Manager for focused `test_bm25`, no default `think` / `grilling` / LLM Evals / Ponytail / Cron. `thinking-router` chooses `first-principles` only if a real unexplained scoring or indexing contradiction persists. **Noodle Poteto Inner Prompt Delta:**
- Implement deterministic BM25 build/search behind the existing adapters with the course tokenizer and unchanged signatures.
- Preserve exact toy-score behavior, ranking/tie/empty/unknown-term semantics and indexed corpus integrity.
- Choose internal representation and algorithms autonomously within the admitted work boundary.
- Use Test Manager-selected controls; report actual results and any still-unmet requirements.

### Behavior Scope / Issue Atom B: grounded multi-hop Email QA

**Goal:** answer questions using retrieved email evidence without invented citations or unbounded searches. **Measurement:** deterministic `test_email_qa` for returned ID list, no-results, bad/malformed replies, and at most 3 search calls; separately live minimum score 0.70 from course threshold, unverified until paid live measurement. **Persistence:** evidence-directed correction under the same fixed boundary; no unbounded model loop or replay of uncertain tool effects. **Stop:** selected deterministic tests and separately required live results actually observed, without claiming all Part 2 delivery.

**Outer Loop:** `issue-atom` once the retrieval producer exists, Test Manager for its specific controls. Apply `thinking-router` → `adversarial-review` only for a genuine grounding/refusal claim; select `grilling` only if the user-controlled quality tradeoff is truly unresolved; Evals skill only where real traces demand model-judged behavior. **Inner Prompt Delta:**
- Return `answer` and `support` in the adapter's required shapes for all modeled replies.
- Never cite email IDs that the search function did not return during this request; stop search after the supplied budget.
- Handle empty evidence and malformed model text without invented support.
- Use the existing `LMCallable` and choose the orchestration and parsing implementation autonomously.
- Preserve original evidence and return real deterministic/live scope results; do not claim parent HW1 completion.

## 5. First Skill Effect Review

| Assertion | Result from this run | Proof ceiling |
| --- | --- | --- |
| Current HW1 selected over stale version | **SUPPORTED** by current course source and starter | Source comparison, no full official handout inspection |
| Relevant lecture/reading selection | **PARTIAL**: links and topics confirmed, article full text read | **Slides PDF pages NOT_READ** |
| Boot four cards / full requirement inventory | Four substantive cards plus 13 requirement statements | Static structured fixture only |
| Drill material gain | Two updates and two creations with meaningful evidence/behavior differences | Card-delta structural verification only |
| Card link reachability / original IDs | Validated by actual `factoryweaver.verify` once CI runs | Structural correctness, not source semantic proof |
| Architecture to causal Issue Atom | Two separable producer→consumer scopes with measurable acceptance | Proposed, no real admission or writer |
| Outer/Inner prompt responsibilities | Conditional outer skill selection, bounded Poteto work freedom | No actual carrier invocation |
| Full HW1 homework/slide fidelity | **UNKNOWN** | Unread official PDFs, missing page-anchored evidence |
| Human judge/LLM agent behavior improvement | **NOT_RUN** | No fresh agent baseline/treatment or independent blind judge |
| Native Host manager consumption | **NOT_RUN** | No Soodles owner effect/readback |

**Finding:** The v7.2 skill is able to represent the *semantically selected* source-to-card / many-cards-to-scope structure and supply a coherent architecture proposal. This source exercise **cannot demonstrate actual model's autonomous extraction quality** because its cards were deliberately curated as an auditable golden fixture. The required next eval is a clean, unprompted consumer run using the live unified Skill against the same source set and an independent error analysis, measured against this fixture. Pin actual lecture PDF contents and official handout before asserting full lossless coverage.

## 6. Minimum next adversarial controls

1. **Source precedence:** inject obsolete paper/DSPy homework wording and check whether generated cards falsely promote it to HW1 acceptance.
2. **Theory-to-mandate confusion:** mix RAG dense retriever / MCP features with the BM25 rubric; any generated "must use vector DB" or "must implement MCP" fails.
3. **Scope atomization:** check that one Email QA atom includes support-ID and hop-budget behavior while BM25 scoring remains a distinct prerequisite.
4. **False grounding:** present a support ID unseen in a query; reject it rather than letting LLM self-report correctness.
5. **False completion:** pass static schema but not real test; must report compile success only, not QA pass.
6. **Slide fidelity:** cannot claim a particular slide page without reading the PDF. The correct output is K/NOT_READ, not a paraphrase attributed to a guessed slide.
7. **Cross-batch continuity:** Boot four cards followed by Drill 2 UPDATE / 2 CREATE, no changed identity or dropped original REQ.
8. **Host metadata boundary:** all physical digests/cursors/commit refs remain Host/CLI computed, never guessed in prompts and card bodies.

### Copyright, access and course integrity

Cards are short original analyses and specification proposals, not copies of Stanford slide pages, assignment solutions or reading chapters. Respect Stanford HW1 requirements and independently understand/verify any later code submission. The official assignment is MIT licensed, but other readings/slides have their own terms. This pilot does not redistribute third-party PDFs.
