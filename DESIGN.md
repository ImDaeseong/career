# career Design

Updated: 2026-09-27

## Purpose

Maintain evidence-backed career claims, source records, and application tracking while keeping private evidence out of Git.

## Stakeholders, concerns, and scenarios

- User: make accurate career claims while protecting employer and customer information.
- Reviewer: trace each public claim to sufficient evidence without receiving unrelated private records.
- Maintainer: evolve schemas without breaking historical records.
- Representative scenario: add a claim, attach an evidence identifier, validate the private record, generate a public-safe summary, and review disclosure.

## Boundaries

- Public summaries and schemas may be committed.
- Employer, customer, contact, and private evidence stay in ignored local storage.
- A recorded claim must point to evidence; unsupported claims remain unverified.

## Main components

- Career claim and evidence records.
- Application and decision tracking.
- `skill/analyze-career-persona/`: structured analysis instructions.
- Validation scripts: schema, link, and privacy checks.

## Detailed structure and views

### Record and publication view

```text
private evidence record (ignored local storage)
  -> stable evidence identifier
  -> claim/application record
  -> scripts/validate_repo.py
  -> public-safe index.html and summaries
  -> human disclosure review
```

- `examples/` contains synthetic/public-safe record shapes; it is not the user's live evidence store.
- `scripts/` validates schemas, links, identifiers, and disclosure rules; `tests/` protects those contracts.
- `skill/analyze-career-persona/` provides analysis instructions but cannot upgrade an unsupported claim to verified status.

There is no server-side service or shared database. The critical boundary is referential: committed claims may point to stable identifiers, while sensitive source evidence remains local and is disclosed only by a human decision.

## Key decisions and tradeoffs

- Separate public claims from private evidence. This reduces disclosure risk but requires stable identifiers and local backup.
- Treat missing support as unverified rather than inferring a favorable claim.

## Verification and human review

Run `python scripts/validate_repo.py`. A human must approve factual claims, disclosure scope, application wording, and any use of private evidence.

## Evidence basis and limits

The design-description structure follows [IEEE 1016-2009](https://standards.ieee.org/ieee/1016/4502/) and [Kruchten](https://www.cs.ubc.ca/~gregor/teaching/papers/4%2B1view-architecture.pdf); public/private record boundaries reflect [Parnas (1972)](https://doi.org/10.1145/361598.361623); quality and secure-development checks are informed by [ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html) and [NIST SSDF 1.1](https://doi.org/10.6028/NIST.SP.800-218). No certification is claimed.

The choice of detailed views is also guided by [ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74393.html), whose public abstract specifies architecture descriptions, viewpoints, and model kinds, and the [SEI Views and Beyond approach](https://www.sei.cmu.edu/library/views-and-beyond-the-sei-approach-for-architecture-documentation/), which organizes documentation around views selected for stakeholder use. Only views supported by current repository evidence are included; omitted views are not implied.
