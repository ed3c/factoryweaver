# v7.1 ↔ v7.2 Blind Pairwise Review — transport and protocol

Issue #4 needs **independent, content-quality evaluation**, not 100% pass on a structural JSON shape. The reference CLI prepares a blind A/B packet; it is not an evaluator, LLM judge, truth oracle, independent reviewer, or runtime executor.

## Input ownership

An **external, authorized assessment owner** must first freeze identical task/source/context conditions and collect the two **actual generated outputs** from v7.1 and v7.2. These outputs are *missing* in this repository: do not substitute the synthetic unit-test examples and call it a comparison. Freeze:
- exact source bytes and manifest digest;
- identical task, model/carrier, output budget and permitted tool conditions (or explicit deviations);
- revision and invocation identities for both compiler versions;
- raw output bytes, incomplete/error statuses, and run artifacts.

The JSON case must have `protocol=factoryweaver/blind-comparison-v1`, `case_id`, `source_manifest_sha256`, `task`, `frozen_conditions`, `baseline_output` and `candidate_output`. Candidate text must not identify itself as v7.1/v7.2; redaction belongs to the **original artifact owner**, not this CLI, since silent edits would destroy fidelity.

## Blinding boundary

The host independently provisions a private 32-byte seed in a file outside the candidate PR, then invokes the read-only CLI twice:

```bash
python3 scripts/blind_review.py packet case.json --seed-file /host/private/seed.bin
python3 scripts/blind_review.py key case.json --seed-file /host/private/seed.bin
```

The first output contains only task, frozen conditions, candidate content labelled A/B, comparison dimensions and immutable case digest; **only it** may go to a reviewer. The second output identifies which label was the baseline or candidate, and must stay with the assessment owner until the blind review is sealed. The seed cannot live in the public repository, logs or reviewer prompt.

A/B order is pseudorandomized with HMAC-SHA256 over the **host-supplied seed** and case ID. Repeating the exact inputs yields the same packet; changed output changes `case_sha256`. A crafted seed or model-identifying prose can still break blinding: the host must audit the packet before handing it off.

## Reviewer question and required artifact

Ask a truly independent reviewer to compare **without knowing A/B identities**, score both on:
`source_fidelity`, `narrative`, `concept_mechanism`, `actionability`, `reader_efficiency`, and cite the **specific candidate span** that makes each criterion pass/fail. Explicitly mark ambiguous, tie, incomplete and unusable cases, rather than manufacturing a difference. Record the reviewer identity, tool/capture provenance, raw responses, eligibility, exclusion reasons, frozen denominators and selection policy.

Only a separately trusted evaluator/Owner may bind that result back to the held answer key, decide a winner, and confirm source-independent reviews and non-regression against the original v7.1/v6.6 baseline. A self-submitted scoring JSON is **not** independently verified.

## Evidence ceiling

The CLI always returns `review_status=NOT_RUN`, `independent_reviewer_verified=false` and `source_origin_verified=false`. Passing the included positive/negative tests proves packet construction, host-key separation *at the interface*, and deterministic bindings only. It does **not** prove actual blinding in a live human/agent session, quality uplift, original-source provenance, or automatic adoption.

No network access, GitHub write, subprocess launch or provider effects are performed by this module. In the sample CLI, the `--seed-file` path is read-only and visible to the host command caller: do not reuse a credential secret or put it in public logs.
