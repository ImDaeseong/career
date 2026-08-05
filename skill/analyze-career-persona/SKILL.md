---
name: analyze-career-persona
description: Analyze career records into an evidence-based self-analysis report without inventing personality traits. Use when creating or updating a career persona, MBTI-related reflection, strengths report, role-fit analysis, or personal-data report from resume, portfolio, and technical-history files.
---

# Analyze Career Persona

Turn career records into a self-analysis that separates observed facts from interpretation. Do not diagnose a psychological type or present "more accurate than MBTI" as a validated claim.

## Source order

Read these repository-relative sources:

1. `backup/resume/resume.md` for employers, dates, roles, and skills
2. `backup/portfolio/portfolio.md` for project and responsibility detail
3. `backup/career-history/tech_history.md` for chronological technology changes
4. `index.html` and `mbti.html` only as outputs to reconcile, never as new factual sources

If a claim is absent from the three primary sources, label it as a question or omit it. Never infer private company data, performance numbers, personality traits, or leadership authority.

## Workflow

1. Extract dated facts into company, project, technology, responsibility, and environment groups.
2. Name a pattern only when at least two projects or periods support it.
3. Write each finding as observation, interpretation, limitation, and next evidence.
4. For MBTI-related requests, discuss each axis as a reflection prompt. Do not output a four-letter type unless the user supplies a real assessment and asks to display it.
5. Separate demonstrated strengths from emerging interests. Treat AI as an emerging research area unless newer primary-source evidence says otherwise.
6. Remove email, private URLs, customer data, internal metrics, credentials, and unpublished company information from public reports.
7. Reconcile every factual statement against the primary sources, then run `python scripts/validate_repo.py`.

## Report structure

Use this order:

1. Data coverage and limits
2. Career pattern summary
3. Evidence-backed strengths
4. MBTI-axis reflection without type diagnosis
5. Work-environment and role hypotheses
6. Risks, missing evidence, and counterexamples
7. Next actions
8. Method and source note

Keep the report useful for decisions rather than flattering. Phrase role fit as a hypothesis to test, not a verdict.
