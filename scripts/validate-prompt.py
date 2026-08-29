#!/usr/bin/env python3
"""Validate prompt files under prompts/**/*.md.

Required ## sections (a heading whose text equals or starts with one of these):
  Use When, Goal, Input Variables, Prompt,
  Expected Behavior, Expected Output, Validation

Warned-only (no fail) if missing:
  Common Mistakes, Related Skills, Related Workflows

Headings may be bilingual, e.g. "## Goal（目标）" still matches "Goal"
(matched by exact text or by the required name followed by a separator).

Exit codes: 0 = all pass, 1 = any missing required section. Stdlib only.
"""
import argparse
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "Use When",
    "Goal",
    "Input Variables",
    "Prompt",
    "Expected Behavior",
    "Expected Output",
    "Validation",
]
WARN_SECTIONS = [
    "Common Mistakes",
    "Related Skills",
    "Related Workflows",
]

# separators that may follow a required name in a bilingual heading
_SEPARATORS = (" ", "(", "（", ":", "：", "—", "–", "、", "/", ".")


def heading_matches(heading, required):
    if heading == required:
        return True
    return any(heading.startswith(required + sep) for sep in _SEPARATORS)


def find_headings(content):
    headings = []
    in_fence = False
    fence_char = ""
    for line in content.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            chars = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_char = chars
            elif chars == fence_char:
                in_fence = False
            continue
        if in_fence:
            continue
        m = re.match(r"^\s{0,3}(#{1,6})\s+(.+?)\s*$", line)
        if m:
            headings.append(m.group(2).strip())
    return headings


def validate_prompt(path):
    errors = []
    warnings = []
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:  # pragma: no cover - defensive
        return [f"cannot read file / 无法读取: {e}"], []
    headings = find_headings(content)
    for s in REQUIRED_SECTIONS:
        if not any(heading_matches(h, s) for h in headings):
            errors.append(f"missing required section / 缺少必需小节: ## {s}")
    for s in WARN_SECTIONS:
        if not any(heading_matches(h, s) for h in headings):
            warnings.append(f"optional section missing / 可选小节缺失: ## {s}")
    return errors, warnings


def resolve_root(args):
    if args.root_opt:
        return Path(args.root_opt).resolve()
    if args.root:
        return Path(args.root).resolve()
    return Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser(description="Validate prompt .md files.")
    ap.add_argument("root", nargs="?", default=None, help="repo root (default: two dirs up from this script) / 仓库根目录")
    ap.add_argument("--root", dest="root_opt", default=None, help="repo root (overrides positional) / 仓库根目录")
    args = ap.parse_args()
    root = resolve_root(args)
    prompts_dir = root / "prompts"

    prompts = sorted(prompts_dir.rglob("*.md")) if prompts_dir.exists() else []

    if not prompts:
        print("validate-prompt: no .md files found under prompts/ / 在 prompts/ 下未找到任何 .md 文件")
        print("Summary / 汇总: PASS 0  FAIL 0  (total 0)")
        return 0

    fail_count = 0
    pass_count = 0
    for p in prompts:
        try:
            rel = p.relative_to(root).as_posix()
        except ValueError:
            rel = str(p)
        errs, warns = validate_prompt(p)
        if errs:
            fail_count += 1
            print(f"FAIL {rel}")
            for e in errs:
                print(f"      - {e}")
        else:
            pass_count += 1
            print(f"PASS {rel}")
        for w in warns:
            print(f"      WARN {w}")

    print(f"\nSummary / 汇总: PASS {pass_count}  FAIL {fail_count}  (total {pass_count + fail_count})")
    return 1 if fail_count else 0


if __name__ == "__main__":
    sys.exit(main())
