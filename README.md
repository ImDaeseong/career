<div align="center">

**<a href="https://imdaeseong.github.io/career/" target="_blank" rel="noopener noreferrer">이력서 보기</a>**  ·  **<a href="https://imdaeseong.github.io/career/mbti.html" target="_blank" rel="noopener noreferrer">경력 기반 강점 분석 보기</a>**

</div>

## 비공개 경력 증거·지원 결과 추적

공개 이력서와 실제 지원 기록을 분리합니다. `examples/career-tracker.example.json`을
`private/career-tracker.json`으로 복사한 뒤, 주장별 출처와 공고 요구사항의
`covered / partial / gap`, 지원 단계, 이력서 버전을 기록할 수 있습니다.
`private/`은 Git에서 제외되므로 회사명과 지원 결과를 공개 저장소에 올리지 않습니다.

```powershell
python scripts/career_tracker.py validate private/career-tracker.json
python scripts/career_tracker.py report private/career-tracker.json
```

보고서는 관찰된 지원 단계와 요구사항 수만 집계합니다. 특정 이력서 변경이 합격의
원인이라고 자동 판정하지 않으며, 채용 관련 최종 판단은 사람이 검토해야 합니다.

## 저장소 검증

```powershell
python scripts/validate_repo.py
```
# career

**🤔 [쉬운 설명 보기](ELI5.html)** — 비개발자를 위한 한 페이지 요약

**설계 문서:** [DESIGN.md](DESIGN.md) — 경력 주장, 근거, 비공개 자료의 경계
