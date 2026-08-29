#!/usr/bin/env python3
"""Validate skill SKILL.md files under skills/core/*/ and skills/ai/*/.

Checks (per skill):
  - SKILL.md exists
  - YAML front matter present (between --- lines)
  - name present & non-empty
  - description present
  - version present
  - difficulty present & in {beginner, intermediate, advanced}
  - status present & in {experimental, stable, deprecated}
  - validation field present
  - HONESTY: if verified == true then status MUST be stable
    AND last_verified MUST be present/non-null (else FAIL)

Exit codes: 0 = all pass, 1 = any fail.
Uses ONLY the Python standard library (a minimal hand-rolled YAML front-matter
parser — no PyYAML required).
"""
import argparse
import sys
from pathlib import Path

ALLOWED_DIFFICULTY = {"beginner", "intermediate", "advanced"}
ALLOWED_STATUS = {"experimental", "stable", "deprecated"}


# --- minimal YAML front-matter parser (handles key: value, bool, null, [lists]) ---

def strip_comment(line):
    """Strip a trailing # comment that is not inside quotes or brackets."""
    out = []
    in_quote = False
    depth = 0
    for i, ch in enumerate(line):
        if ch in ("'", '"'):
            in_quote = not in_quote
        elif ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
        elif ch == "#" and not in_quote and depth == 0:
            if i == 0 or line[i - 1] in (" ", "\t"):
                break
        out.append(ch)
    return "".join(out).rstrip()


def parse_scalar(v):
    v = v.strip()
    if v == "":
        return None
    low = v.lower()
    if low == "true":
        return True
    if low == "false":
        return False
    if low in ("null", "~"):
        return None
    if v.startswith("[") and v.endswith("]"):
        inner = v[1:-1].strip()
        if not inner:
            return []
        items = [x.strip() for x in inner.split(",") if x.strip()]
        out = []
        for x in items:
            if (x.startswith('"') and x.endswith('"')) or (x.startswith("'") and x.endswith("'")):
                x = x[1:-1]
            out.append(x)
        return out
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        return v[1:-1]
    return v


def parse_front_matter(text):
    fm = {}
    for raw in text.splitlines():
        line = strip_comment(raw)
        if not line.strip():
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        if not key:
            continue
        fm[key] = parse_scalar(value)
    return fm


def extract_front_matter(content):
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, content
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None, content
    fm_text = "\n".join(lines[1:end])
    body = "\n".join(lines[end + 1:])
    return fm_text, body


# --- helpers ---

def is_nonempty(v):
    if v is None:
        return False
    if isinstance(v, str):
        return v.strip() != ""
    if isinstance(v, list):
        return len(v) > 0
    return True


def validate_skill(skill_md):
    errors = []
    if not skill_md.exists():
        errors.append("SKILL.md not found / 找不到 SKILL.md")
        return errors
    try:
        content = skill_md.read_text(encoding="utf-8")
    except Exception as e:  # pragma: no cover - defensive
        errors.append(f"cannot read file / 无法读取: {e}")
        return errors
    fm_text, _ = extract_front_matter(content)
    if fm_text is None:
        errors.append("front matter missing (no leading --- block) / 缺少 YAML 前置元数据")
        return errors
    fm = parse_front_matter(fm_text)

    if "name" not in fm or not is_nonempty(fm.get("name")):
        errors.append("'name' missing or empty / name 缺失或为空")
    if "description" not in fm or not is_nonempty(fm.get("description")):
        errors.append("'description' missing or empty / description 缺失或为空")
    if "version" not in fm or not is_nonempty(fm.get("version")):
        errors.append("'version' missing or empty / version 缺失或为空")
    if "difficulty" not in fm or not is_nonempty(fm.get("difficulty")):
        errors.append("'difficulty' missing / difficulty 缺失")
    else:
        d = fm.get("difficulty")
        if d not in ALLOWED_DIFFICULTY:
            errors.append(
                f"'difficulty' invalid: {d!r} (allowed {sorted(ALLOWED_DIFFICULTY)}) / difficulty 取值非法"
            )
    if "status" not in fm or not is_nonempty(fm.get("status")):
        errors.append("'status' missing / status 缺失")
    else:
        s = fm.get("status")
        if s not in ALLOWED_STATUS:
            errors.append(
                f"'status' invalid: {s!r} (allowed {sorted(ALLOWED_STATUS)}) / status 取值非法"
            )
    if "validation" not in fm:
        errors.append("'validation' field missing / validation 字段缺失")

    # HONESTY RULE
    verified = fm.get("verified")
    if verified is True:
        s = fm.get("status")
        if s != "stable":
            errors.append(
                "HONESTY: verified=true requires status=stable / 诚实规则：verified 为 true 时 status 必须为 stable"
            )
        lv = fm.get("last_verified")
        if lv is None or (isinstance(lv, str) and not lv.strip()):
            errors.append(
                "HONESTY: verified=true requires non-null last_verified / 诚实规则：verified 为 true 时 last_verified 不得为空"
            )
    return errors


def resolve_root(args):
    if args.root_opt:
        return Path(args.root_opt).resolve()
    if args.root:
        return Path(args.root).resolve()
    return Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser(description="Validate skill SKILL.md files.")
    ap.add_argument("root", nargs="?", default=None, help="repo root (default: two dirs up from this script) / 仓库根目录")
    ap.add_argument("--root", dest="root_opt", default=None, help="repo root (overrides positional) / 仓库根目录")
    args = ap.parse_args()
    root = resolve_root(args)
    skills_dir = root / "skills"

    skills = []
    if skills_dir.exists():
        for cat in ("core", "ai"):
            cat_dir = skills_dir / cat
            if cat_dir.exists():
                for sub in sorted(cat_dir.iterdir()):
                    if sub.is_dir():
                        skills.append((cat, sub.name, sub / "SKILL.md"))

    if not skills:
        print("validate-skill: no skill folders found under skills/{core,ai}/*/ / 在 skills/{core,ai}/*/ 下未找到任何 skill 目录")
        print("Summary / 汇总: PASS 0  FAIL 0  (total 0)")
        return 0

    fail_count = 0
    pass_count = 0
    for cat, name, sk in skills:
        rel = f"skills/{cat}/{name}/SKILL.md"
        errs = validate_skill(sk)
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
