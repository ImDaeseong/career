"""Validate the static career site, resume artifacts, and guide paths."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".html", ".md", ".txt", ".yaml", ".yml"}
SUMMARY_FILES = (
    ROOT / "index.html",
)
SUMMARY_TOKENS = ("25년 경력", "미디어웹 19년", "초기 경력", "2007", "2026")


class HtmlReferences(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.references: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if attributes.get("id"):
            self.ids.append(attributes["id"] or "")
        for name in ("href", "src"):
            if attributes.get(name):
                self.references.append(attributes[name] or "")


def local_target(document: Path, reference: str) -> Path | None:
    target = reference.strip().split("#", 1)[0]
    if not target or re.match(r"^(?:https?://|mailto:|tel:|data:|javascript:)", target):
        return None
    return (document.parent / target).resolve()


def main() -> int:
    failures: list[str] = []
    files = sorted(path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts)

    for path in files:
        data = path.read_bytes()
        relative = path.relative_to(ROOT)
        if not data:
            failures.append(f"empty file: {relative}")
        if path.suffix.lower() in TEXT_SUFFIXES:
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError as error:
                failures.append(f"invalid UTF-8: {relative}: {error}")
                continue
            if "\x00" in text or "\ufffd" in text:
                failures.append(f"invalid text character: {relative}")
            if re.search(r"^(?:<<<<<<<|=======|>>>>>>>)", text, re.MULTILINE):
                failures.append(f"merge-conflict marker: {relative}")

    for path in (item for item in files if item.suffix.lower() == ".md"):
        text = path.read_text(encoding="utf-8")
        for reference in re.findall(r"\[[^]]*\]\(([^)]+)\)", text):
            target = local_target(path, reference)
            if target is not None and not target.exists():
                failures.append(f"broken Markdown link: {path.relative_to(ROOT)} -> {reference}")

    for path in (item for item in files if item.suffix.lower() == ".html"):
        parser = HtmlReferences()
        parser.feed(path.read_text(encoding="utf-8"))
        duplicate_ids = sorted({item for item in parser.ids if parser.ids.count(item) > 1})
        if duplicate_ids:
            failures.append(f"duplicate HTML ids: {path.relative_to(ROOT)}: {duplicate_ids}")
        for reference in parser.references:
            if reference.startswith("#") and reference[1:] not in parser.ids:
                failures.append(f"broken HTML anchor: {path.relative_to(ROOT)} -> {reference}")
            target = local_target(path, reference)
            if target is not None and not target.exists():
                failures.append(f"broken HTML reference: {path.relative_to(ROOT)} -> {reference}")

    index = (ROOT / "index.html").read_text(encoding="utf-8").lower()
    for token in ('<!doctype html>', '<html lang="ko">', '<meta charset="utf-8">', "<title>"):
        if token not in index:
            failures.append(f"index.html missing {token}")

    # backup/(resume.md·portfolio.md·tech_history.md·resume-ats.pdf 등)는 2026-08-05
    # 사용자가 최종 정리 단계에서 직접 삭제했습니다. skill/*.md는 향후 재사용을 위해
    # backup/ 경로를 그대로 참조하도록 남겨뒀으므로, 그 경로의 존재 여부는 더 이상
    # 검사하지 않습니다 (의도적으로 없는 상태).

    for skill_path in ROOT.glob("skill/*/SKILL.md"):
        skill_text = skill_path.read_text(encoding="utf-8")
        relative = skill_path.relative_to(ROOT)
        if "[TODO" in skill_text:
            failures.append(f"unfinished skill template: {relative}")
        frontmatter = re.match(r"^---\nname: ([a-z0-9-]+)\ndescription: (.+?)\n---\n", skill_text)
        if not frontmatter:
            failures.append(f"invalid skill frontmatter: {relative}")
            continue
        metadata_path = skill_path.parent / "agents/openai.yaml"
        if not metadata_path.exists():
            failures.append(f"missing skill metadata: {metadata_path.relative_to(ROOT)}")
        else:
            metadata = metadata_path.read_text(encoding="utf-8")
            if f"${frontmatter.group(1)}" not in metadata:
                failures.append(f"skill metadata prompt does not name ${frontmatter.group(1)}")

    mbti = (ROOT / "mbti.html").read_text(encoding="utf-8")
    if "경력 기록만으로 심리적 성격유형을 판정할 수는 없습니다" not in mbti:
        failures.append("mbti.html is missing its non-diagnostic limitation")
    for unsupported in (
        "다수의 심리학 연구",
        "혼자 학습",
        "스스로 찾아 흡수",
        "스스로 계속",
        "자발적 학습",
        "직접 설계·구현",
    ):
        if unsupported in mbti:
            failures.append(f"mbti.html contains an unsupported claim: {unsupported}")

    for path in SUMMARY_FILES:
        text = path.read_text(encoding="utf-8")
        for token in SUMMARY_TOKENS:
            if token not in text:
                failures.append(f"summary drift: {path.relative_to(ROOT)} missing {token}")

    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1

    print(f"PASS: {len(files)} files; text, links, HTML, skill metadata, and resume summary are valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
