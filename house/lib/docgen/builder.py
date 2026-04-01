#!/usr/bin/env python3
"""Documentation builder for multiple languages."""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, Optional

# Supported languages
# Each non-English language has static files with suffix (e.g., readme_zh.md) that override base files
LANGUAGES = [{"code": "zh_CN", "name": "Chinese", "source_suffix": "_zh"}]


def _has_lang_suffix(name: str) -> bool:
    """Return True if filename carries a language-specific suffix."""
    suffixes = {lang["source_suffix"] for lang in LANGUAGES}
    return any(
        name.endswith(f"{sfx}.md") or name.endswith(f"{sfx}.rst") for sfx in suffixes
    )


def _copy_docs_source(docs_dir: Path, tmp_src: Path) -> None:
    """Copy docs source into a temporary directory, skipping language-specific files."""
    for item in docs_dir.iterdir():
        if item.name in ("_build", "build_docs.py"):
            continue
        if item.is_file() and _has_lang_suffix(item.name):
            continue

        dest = tmp_src / item.name
        if item.is_dir():
            shutil.copytree(item, dest, ignore=shutil.ignore_patterns("_build"))
        else:
            shutil.copy2(item, dest)


def _apply_overrides(docs_dir: Path, tmp_src: Path, suffix: str) -> None:
    """Copy language-specific source files over the base names."""
    for lang_file in docs_dir.glob(f"*{suffix}.md"):
        shutil.copy2(lang_file, tmp_src / lang_file.name.replace(suffix, ""))
    for lang_file in docs_dir.glob(f"*{suffix}.rst"):
        shutil.copy2(lang_file, tmp_src / lang_file.name.replace(suffix, ""))


def _run_sphinx(src_dir: Path, out_dir: Path, language: str) -> bool:
    """Run sphinx-build for a given language."""
    cmd = [
        "sphinx-build",
        "-b",
        "html",
        str(src_dir),
        str(out_dir),
        "-D",
        f"language={language}",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result.returncode == 0


def _build_language(
    docs_dir: Path,
    build_base: Path,
    language: str,
    display_name: str,
    source_suffix: Optional[str] = None,
) -> bool:
    """Build documentation for a single language."""
    outdir = build_base if language == "en" else build_base / language
    print(f"\n=== Building {display_name} ===")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_src = Path(tmpdir) / "src"
        tmp_src.mkdir()

        _copy_docs_source(docs_dir, tmp_src)
        if source_suffix:
            _apply_overrides(docs_dir, tmp_src, source_suffix)

        if not _run_sphinx(tmp_src, outdir, language):
            print(f"{display_name} build failed!")
            return False

    return True


def build_docs(docs_dir: Path) -> bool:
    """Build documentation for all languages."""
    build_base = docs_dir / "_build" / "html"
    build_base.mkdir(parents=True, exist_ok=True)

    # English at root
    if not _build_language(docs_dir, build_base, "en", "English (root)"):
        return False

    # Other languages in subdirectories
    for lang in LANGUAGES:
        if not _build_language(
            docs_dir,
            build_base,
            lang["code"],
            f"{lang['name']} ({lang['code']})",
            source_suffix=lang.get("source_suffix"),
        ):
            return False

    print("\n=== Build complete ===")
    print(f"  English (root): {build_base}")
    for lang in LANGUAGES:
        print(f"  {lang['name']}: {build_base / lang['code']}")

    return True
