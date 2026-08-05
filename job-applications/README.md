# job-applications

`.claude/skills/resume-tailor` 스킬이 생성한 직무 맞춤 이력서를 저장하는 폴더입니다.

지원 회사/직무마다 하위 폴더가 하나씩 생깁니다:

```
<회사명>-<직무-slug>/
  tailored-resume.md   맞춤화된 이력서
  coverage-map.md       JD 요구사항 대비 커버됨/부분 커버/커버 안 됨 매핑표
```

`tailored-resume.md`는 항상 `resume/resume.md` + `portfolio/portfolio.md` +
`career-history/tech_history.md`에 실제로 있는 내용만 사용합니다 — 없는
경력이나 기술을 지어내지 않습니다.
