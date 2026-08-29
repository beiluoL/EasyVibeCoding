#!/usr/bin/env python3
"""Validate registry/*.yaml index files: skills.yaml, prompts.yaml, cases.yaml, workflows.yaml.

Per entry: id present & unique (fail on duplicate id across the file); name present;
status in {experimental, stable, deprecated}; difficulty in {beginner, intermediate,
advanced}; HONESTY: if verified==true then last_verified must be present; and the
entry's `path` EXISTS relative to repo root (fail if missing).

YAML handling: uses PyYAML if importable; otherwise prints a warning
"pyyaml not installed — skipping deep checks" and exits 0 (degrade gracefully,
never crash on missing pyyaml).
"""
import argparse
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
    HAVE_YAML = True
except Exception:
    HAVE_YAML = False

ALLOWED_STATUS = {"experimental", "stable", "deprecated"}
ALLOWED_DIFFICULTY = {"beginner", "intermediate", "advanced"}
REGISTRY_FILES = ["skills.yaml", "prompts.yaml", "cases.yaml", "workflows.yaml"]


def is_nonempty(v):
    if v is None:
        return False
    if isinstance(v, str):
        return v.strip() != ""
    return True


def extract_entries(data):
    """Return list of entry dicts from a parsed registry file."""
    if not isinstance(data, dict):
        return []
    for key in ("skills", "prompts", "cases", "workflows", "entries", "items"):
        if key in data and isinstance(data[key], list):
            return data[key]
    # fall back: top-level mapping id -> entry
    entries = []
    for k, v in data.items():
        if k in ("version",):
            continue
        if isinstance(v, dict):
            ev = dict(v)
            ev.setdefault("id", k)
            entries.append(ev)
        elif isinstance(v, list):
            for item in v:
                if isinstance(item, dict):
                    ev = dict(item)
                    ev.setdefault("id", k)
                    entries.append(ev)
    return entries


def validate_registry_file(path, root):
    errors = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        return [f"cannot parse YAML / YAML 解析失败: {e}"]

    if data is None:
        return []
    if not isinstance(data, dict):
        return ["top-level YAML is not a mapping / 顶层不是字典"]

    entries = extract_entries(data)

    seen_ids = {}
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"entry #{i}: not a mapping / 第 {i} 项不是字典")
            continue
        eid = entry.get("id")
        label = repr(eid) if is_nonempty(eid) else f"#{i}"
        if not is_nonempty(eid):
            errors.append(f"entry #{i}: 'id' missing or empty / id 缺失或为空")
        else:
            if eid in seen_ids:
                errors.append(
                    f"duplicate id / 重复 id: {eid!r} (also at #{seen_ids[eid]}) / 重复 id"
                )
            else:
                seen_ids[eid] = i
        if not is_nonempty(entry.get("name")):
            errors.append(f"entry {label}: 'name' missing or empty / name 缺失或为空")
        st = entry.get("status")
        if st is not None and st not in ALLOWED_STATUS:
            errors.append(f"entry {label}: 'status' invalid: {st!r} / status 取值非法")
        df = entry.get("difficulty")
        if df is not None and df not in ALLOWED_DIFFICULTY:
            errors.append(f"entry {label}: 'difficulty' invalid: {df!r} / difficulty 取值非法")
        if entry.get("verified") is True:
            lv = entry.get("last_verified")
            if lv is None or (isinstance(lv, str) and not lv.strip()):
                errors.append(
                    f"entry {label}: HONESTY: verified=true requires non-null last_verified / 诚实规则：verified 为 true 时 last_verified 不得为空"
                )
        p = entry.get("path")
        if is_nonempty(p):
            if not (root / p).exists():
                errors.append(f"entry {label}: path does not exist / 路径不存在: {p}")
    return errors


def resolve_root(args):
    if args.root_opt:
        return Path(args.root_opt).resolve()
    if args.root:
        return Path(args.root).resolve()
    return Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser(description="Validate registry/*.yaml index files.")
    ap.add_argument("root", nargs="?", default=None, help="repo root (default: two dirs up from this script) / 仓库根目录")
    ap.add_argument("--root", dest="root_opt", default=None, help="repo root (overrides positional) / 仓库根目录")
    args = ap.parse_args()
    root = resolve_root(args)
    registry_dir = root / "registry"

    if not HAVE_YAML:
        print("WARNING / 警告: pyyaml not installed — skipping deep checks / 未安装 pyyaml，跳过深度校验")
        print("         install with / 安装命令: pip install pyyaml")
        return 0

    if not registry_dir.exists():
        print("validate-registry: registry/ not found / 未找到 registry/ 目录 (nothing to validate)")
        return 0

    fail_count = 0
    pass_count = 0
    for name in REGISTRY_FILES:
        rp = registry_dir / name
        if not rp.exists():
            continue
        rel = f"registry/{name}"
        errs = validate_registry_file(rp, root)
        if errs:
            fail_count += 1
            print(f"FAIL {rel}")
            for e in errs:
                print(f"      - {e}")
        else:
            pass_count += 1
            print(f"PASS {rel}")

    if pass_count == 0 and fail_count == 0:
        print("validate-registry: no registry/*.yaml files found / 未找到任何 registry yaml 文件")
        return 0

    print(f"\nSummary / 汇总: PASS {pass_count}  FAIL {fail_count}  (total {pass_count + fail_count})")
    return 1 if fail_count else 0


if __name__ == "__main__":
    sys.exit(main())
