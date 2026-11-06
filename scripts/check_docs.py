#!/usr/bin/env python3
"""Documentation guardrails for the Dobra repository.

Checks, using only the Python standard library:
1. Relative Markdown links point to files that exist.
2. Anchors (#section) in those links match a heading in the target file,
   using GitHub's heading slug rules.
3. Absolute links to this repository's main branch (github.com/<repo>/blob/main/...)
   are checked the same way as relative links.
4. README.md keeps the specification-phase status banner. Remove this check
   in the same PR that publishes the first working M0 release.

Usage: python3 scripts/check_docs.py [repo_root]
Exit code 0 when everything passes, 1 otherwise.
"""

from __future__ import annotations

import os
import re
import sys
import unicodedata
from pathlib import Path

REPO_BLOB_PREFIX = "https://github.com/pedroribeirodev/dobra/blob/main/"
STATUS_BANNER = "**Status: fase de especificação.**"
SKIPPED_DIRS = {".git", "node_modules"}

INLINE_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
REFERENCE_DEF = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*(\S+)", re.MULTILINE)
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$", re.MULTILINE)
FENCE = re.compile(r"^(```|~~~).*?^\1", re.MULTILINE | re.DOTALL)
INLINE_CODE = re.compile(r"`[^`\n]*`")


def strip_code(text: str) -> str:
    """Remove fenced blocks and inline code so example links are ignored."""
    text = FENCE.sub(lambda m: "\n" * m.group(0).count("\n"), text)
    return INLINE_CODE.sub("", text)


def github_slug(heading: str) -> str:
    """Approximate GitHub's anchor generation for a Markdown heading."""
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", heading)  # links -> label
    text = text.replace("`", "").lower()
    kept = []
    for char in text:
        category = unicodedata.category(char)
        if char in "-_ " or category[0] in ("L", "N") or category == "Mn":
            kept.append(char)
    return "".join(kept).replace(" ", "-")


def anchors_for(path: Path, cache: dict[Path, set[str]]) -> set[str]:
    if path not in cache:
        text = FENCE.sub("", path.read_text(encoding="utf-8"))
        seen: dict[str, int] = {}
        anchors: set[str] = set()
        for match in HEADING.finditer(text):
            slug = github_slug(match.group(2))
            count = seen.get(slug, 0)
            anchors.add(slug if count == 0 else f"{slug}-{count}")
            seen[slug] = count + 1
        cache[path] = anchors
    return cache[path]


def check_links(root: Path) -> list[str]:
    errors: list[str] = []
    cache: dict[Path, set[str]] = {}
    files = sorted(
        p for p in root.rglob("*.md") if not SKIPPED_DIRS.intersection(p.relative_to(root).parts)
    )
    for source in files:
        text = strip_code(source.read_text(encoding="utf-8"))
        targets = INLINE_LINK.findall(text) + REFERENCE_DEF.findall(text)
        for raw in targets:
            target = raw.strip("<>")
            if target.startswith(REPO_BLOB_PREFIX):
                base = root
                target = target[len(REPO_BLOB_PREFIX):]
            elif re.match(r"^[a-z][a-z0-9+.-]*:", target, re.IGNORECASE):
                continue  # external URL, mailto:, tel: and similar
            else:
                base = source.parent
            path_part, _, anchor = target.partition("#")
            resolved = (base / path_part).resolve() if path_part else source.resolve()
            location = source.relative_to(root)
            if not resolved.exists():
                errors.append(f"{location}: link para arquivo inexistente / missing file: {raw}")
                continue
            if anchor and resolved.suffix == ".md":
                if anchor.lower() not in anchors_for(resolved, cache):
                    errors.append(f"{location}: âncora inexistente / missing anchor: {raw}")
    return errors


def check_status_banner(root: Path) -> list[str]:
    readme = root / "README.md"
    if STATUS_BANNER not in readme.read_text(encoding="utf-8"):
        return [
            "README.md: aviso de fase de especificação ausente / missing specification-phase "
            f"banner: {STATUS_BANNER}"
        ]
    return []


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors = check_links(root) + check_status_banner(root)
    for error in errors:
        print(f"::error::{error}" if "GITHUB_ACTIONS" in os.environ else error)
    if errors:
        print(f"\n{len(errors)} problema(s) encontrado(s) / problem(s) found.")
        return 1
    print("Documentação OK / Documentation OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
