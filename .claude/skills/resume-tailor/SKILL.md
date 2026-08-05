---
name: resume-tailor
description: >
  Generates a job-tailored resume for 임대성 from a pasted or linked job
  description (JD), using resume/resume.md + portfolio/portfolio.md +
  career-history/tech_history.md as the only source of truth — never invents
  a skill, title, project, or date not already in those files.
  Trigger whenever the user pastes a job description (or a job posting URL)
  and asks to tailor, customize, or match the resume to it.
allowed-tools:
  - Read
  - Write
  - WebFetch
---

# resume-tailor

Adapted from the workflow in djc1120/resume-builder (github.com/djc1120/resume-builder,
checked 2026-08-05: 2 stars, no LICENSE file present — all-rights-reserved by
default, so this is an original rewrite of the *method*, not a copy of that
repo's SKILL.md) for this repo's actual source files, which are already
structured Markdown rather than a PDF/.docx that needs parsing first.

## Source of truth

Only these three files. If a claim can't be traced to one of them, it does not
go in the output — no exceptions, even if it would make the resume a better
match for the JD.

- `resume/resume.md` — company names, titles, dates, tech stacks, duties
- `portfolio/portfolio.md` — per-project detail (more granular than resume.md)
- `career-history/tech_history.md` — year-by-year technology groupings

## Step 1 — Get the job description

Paste text, or a URL (fetch with WebFetch). Extract into a table:

| Element | What to pull out |
|---|---|
| Required skills/tech | exact terms as the JD states them (e.g. "TCP/IP", "IOCP", "Android") |
| Preferred / nice-to-have | anything marked optional or "우대" |
| Core responsibilities | the actual day-to-day duties described |
| Keywords to echo back | exact phrases likely to matter for a human reader (Korean job postings are rarely ATS-parsed the way US ones are, but a recruiter skimming still pattern-matches on these) |

## Step 2 — Map JD requirements to the three source files

For every JD requirement, find it in resume.md/portfolio.md/tech_history.md and mark:

- **커버됨** — a specific project/role in the source directly matches
- **부분 커버** — related but not exact (e.g. JD asks for "Kubernetes", source only has server ops experience without K8s specifically) — note the gap honestly, do not paper over it
- **커버 안 됨** — no evidence anywhere in the three files — do not include, and say so if asked

Write this mapping table into the output alongside the resume — 임대성 should see what was actually matched, not just get a black-box result.

## Step 3 — Reorder and reframe, never invent

- Keep every company, title, and date exactly as in `resume/resume.md`.
- Within each role, reorder bullet points to lead with what's most relevant to this JD's requirements.
- Pull in more specific detail from `portfolio/portfolio.md` when it strengthens a match (e.g. the JD emphasizes IOCP — portfolio.md's "인증 서버" entry has more detail than resume.md's summary line).
- De-emphasize or drop roles/bullets with low relevance to this specific JD — cutting for focus, not deleting from the source files themselves.
- Do not add a skill, project, metric, or duty that isn't already in the three source files, even if the JD explicitly asks for it and it seems like a small, plausible extrapolation. If it's not covered, say so in Step 2's mapping table instead of quietly filling the gap.

## Step 4 — Write the output

Save to `job-applications/<company>-<role-slug>/`:
- `tailored-resume.md` — the tailored resume itself, same section structure as `resume/resume.md`
- `coverage-map.md` — the Step 2 mapping table (커버됨/부분 커버/커버 안 됨), so 임대성 can see the gaps before applying

Markdown by default (matches this repo's existing format, no extra tooling needed). Only convert to `.docx`/PDF if 임대성 asks for one for an actual submission — that's a separate, heavier step (needs the `docx` npm package and exact formatting rules) worth doing on demand, not building speculatively into every run.

## Guardrails

| 하면 안 되는 것 | 해야 하는 것 |
|---|---|
| 없는 기술/프로젝트/직함 추가 | 세 소스 파일에 실제로 있는 것만 사용 |
| 회사명/직함/기간 변경 | `resume/resume.md`의 원문 그대로 유지 |
| JD 요구사항을 억지로 "커버됨"으로 표시 | 부분 커버/커버 안 됨을 정직하게 표시 |
| 매번 `.docx` 자동 생성 | 요청받았을 때만 생성 |

## Output naming

```
job-applications/<company>-<role-slug>/
  tailored-resume.md
  coverage-map.md
```
