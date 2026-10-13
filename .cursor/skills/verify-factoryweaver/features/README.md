# FactoryWeaver verification feature map

This is the feature map maintained by create-verification-skill and maintain-verification-skill. A user interacts with the actual Python CLI; each feature file names source entry points, a CLI drive and its observable end state.

## Preconditions

- Python 3.12 and jsonschema; no server.
- A clean isolated scratch directory per drive, retained external evidence.
- Doctor before the first drive or after unexpected failure.
- SOODLES_CHECKOUT only if provided by original Host, not auto-cloned.
- No original Issue admission, Hook/Cron event or native model invocation is implied by a passing public CLI fixture.

## Map and proof

The source wave checks all declared Source paths from these feature files concurrently; it is a path-based preflight, not a semantic source review. The coordinator drives all local features serially, records stdout/stderr/exit codes and cleans scratch. Every feature must be examined even if another fails. Full maintain remains blocked without actual native admission and fresh consumer evidence.

## Features

- [Knowledge Contract](./knowledge-contract.md): validate and render original HW1 specification records.
- [Semantic Cards](./semantic-cards.md): selected card prompts and unread-source refusal.
- [Scope Handoff](./scope-handoff.md): original Host-bound Bundle and replay/conflict cases.
- [Manager Needs](./manager-needs.md): focused verification needs without unauthorized manager invocation.
- [Soodles Reader](./soodles-reader.md): consume actual external Reader where Host supports it; native admission remains separately unverified.
