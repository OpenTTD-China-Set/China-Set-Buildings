#!/usr/bin/env python3
"""Documentation builder for multiple languages."""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict


# Supported languages
# Each non-English language has static files with suffix (e.g., readme_zh.md) that override base files
LANGUAGES = [{"code": "zh_CN", "name": "Chinese", "source_suffix": "_zh"}]


def build_language(lang: Dict[str, str], docs_dir: Path, build_base: Path) -> bool:
    """Build documentation for a single language."""
    print(f"\n=== Building {lang['name']} ({lang['code']}) ===")

    outdir = build_base / lang["code"]

    # Create a temporary source directory for this language
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_src = Path(tmpdir) / "src"
        tmp_src.mkdir()

        # Copy all files from docs to temp dir
        for item in docs_dir.iterdir():
            if item.name in ["_build", "build_docs.py"]:
                continue

            dest = tmp_src / item.name
            if item.is_dir():
                shutil.copytree(item, dest, ignore=shutil.ignore_patterns("_build"))
            else:
                shutil.copy2(item, dest)

        # Apply language-specific source file overrides
        suffix = lang["source_suffix"]
        for lang_file in docs_dir.glob(f"*{suffix}.md"):
            base_name = lang_file.name.replace(suffix, "")
            shutil.copy2(lang_file, tmp_src / base_name)

        # Build with Sphinx
        cmd = ["sphinx-build", "-b", "html", str(tmp_src), str(outdir)]
        cmd.extend(["-D", f"language={lang['code']}"])

        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)

        return result.returncode == 0


def build_docs(docs_dir: Path) -> bool:
    """Build documentation for all languages."""
    build_base = docs_dir / "_build" / "html"

    # Ensure build directory exists
    build_base.mkdir(parents=True, exist_ok=True)

    # Build English at root
    print("\n=== Building English (root) ===")
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_src = Path(tmpdir) / "src"
        tmp_src.mkdir()

        # Copy all files from docs to temp dir
        for item in docs_dir.iterdir():
            if item.name in ["_build", "build_docs.py"]:
                continue

            dest = tmp_src / item.name
            if item.is_dir():
                shutil.copytree(item, dest, ignore=shutil.ignore_patterns("_build"))
            else:
                shutil.copy2(item, dest)

        # Build English at root
        result = subprocess.run(
            ["sphinx-build", "-b", "html", str(tmp_src), str(build_base)],
            capture_output=True,
            text=True,
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        if result.returncode != 0:
            print("English build failed!")
            return False

    # Build other languages in subdirectories
    for lang in LANGUAGES:
        if not build_language(lang, docs_dir, build_base):
            print(f"Build failed for {lang['name']}!")
            return False

    print("\n=== Build complete ===")
    print(f"  English (root): {build_base}")
    for lang in LANGUAGES:
        print(f"  {lang['name']}: {build_base / lang['code']}")

    return True
