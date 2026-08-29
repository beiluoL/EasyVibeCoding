#!/usr/bin/env python3
"""Validate case folders under cases/*/<case-name>/.

Required files per case:
  README.md, requirements.md, architecture.md,
  development-log.md, lessons.md, verification.md

For golden cases (cases/golden/*) verification.md is mandatory (already required
above — an explicit, redundant message is added to make the rule unmistakable).

Exit codes: 0 = all pass, 1 = any fail. Standard library only.
"""
import argparse
import sys
from pathlib import Path

REQUIRED_FILES = [
    "README.md",
    "requirements.md",
    "architecture.md",
    "development-log.md",
    "lessons.md",
    "verification.md",
]


def validate_case(case_dir):
    errors = []
    for f in REQUIRED_FILES:
        if not (case_dir / f).exists():
            errors.append(f"missing required file / 缺少必需文件: {f}")
    return errors


def resolve_root(args):
    if args.root_opt:
        return Path(args.root_opt).resolve()
    if args.root:
        return Path(args.root).resolve()
    return Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser(description="Validate case folders.")
    ap.add_argument("root", nargs="?", default=None, help="repo root (default: two dirs up from this script) / 仓库根目录")
    ap.add_argument("--root", dest="root_opt", default=None, help="repo root (overrides positional) / 仓库根目录")
    args = ap.parse_args()
    root = resolve_root(args)
    cases_dir = root / "cases"

    cases = []
    if cases_dir.exists():
        for cat_dir in sorted(cases_dir.iterdir()):
            if not cat_dir.is_dir():
                continue
            for case_dir in sorted(cat_dir.iterdir()):
                if case_dir.is_dir():
                    cases.append((cat_dir.name, case_dir.name, case_dir))

    if not cases:
        print("validate-case: no case folders found under cases/*/<case>/ / 在 cases/*/<case>/ 下未找到任何案例目录")
        print("Summary / 汇总: PASS 0  FAIL 0  (total 0)")
        return 0

    fail_count = 0
    pass_count = 0
    for cat, name, d in cases:
        rel = f"cases/{cat}/{name}"
        errs = validate_case(d)
        if cat == "golden" and not (d / "verification.md").exists():
            errs.append("golden case MUST include verification.md / golden 案例必须包含 verification.md")
        if errs:
            fail_count += 1
            print(f"FAIL {rel}")
            for e in errs:
                print(f"      - {e}")
        else:
            pass_count += 1
            print(f"PASS {rel}")

    print(f"\nSummary / 汇总: PASS {pass_count}  FAIL {fail_count}  (total {pass_count + fail_count})")
    return 1 if fail_count else 0


if __name__ == "__main__":
    sys.exit(main())
