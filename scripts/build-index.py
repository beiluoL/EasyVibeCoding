#!/usr/bin/env python3
"""Generate docs/INDEX.md by scanning skills/, prompts/, cases/, workflows/.

Reads each item's metadata:
  - skills:   front matter of skills/<cat>/<name>/SKILL.md
  - prompts:  front matter of prompts/**/*.md (if absent, derive name from
              the first H1 heading or the filename)
  - cases:    front matter of cases/<cat>/<name>/README.md (if absent, use dir name)
  - workflows: front matter of workflows/<name>/README.md (if absent, use dir name)

Writes docs/INDEX.md with tables (id | name | category | difficulty | status |
verified | path), sorted by category then name. Prints the entry count.
Stdlib only (a minimal hand-rolled YAML front-matter parser).
"""
import argparse
import re
import sys
from pathlib import Path


# --- minimal YAML front-matter parser ---

def strip_comment(line):
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


def first_h1(content):
    for line in content.splitlines():
        m = re.match(r"^#\s+(.+?)\s*$", line)
        if m:
            return m.group(1).strip()
    return None


def cell(v):
    if v is None:
        return "-"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, list):
        return ", ".join(str(x) for x in v) if v else "-"
    return str(v)


def render_table(rows, columns):
    headers = [h for h, _ in columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "|" + "|".join(["---"] * len(headers)) + "|",
    ]
    for r in rows:
        vals = [cell(r.get(k)) for _, k in columns]
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def _apply_fm(entry, content):
    fm_text, body = extract_front_matter(content)
    if fm_text:
        fm = parse_front_matter(fm_text)
        for k in ("id", "name", "category", "difficulty", "status", "verified"):
            if k in fm and fm[k] not in (None, "", []):
                entry[k] = fm[k]
    return body


def collect_skills(root):
    out = []
    base = root / "skills"
    if not base.exists():
        return out
    for cat_dir in sorted(base.iterdir()):
        if not cat_dir.is_dir():
            continue
        for sub in sorted(cat_dir.iterdir()):
            if not sub.is_dir():
                continue
            entry = {
                "id": sub.name,
                "name": sub.name,
                "category": cat_dir.name,
                "difficulty": "-",
                "status": "-",
                "verified": False,
                "path": f"skills/{cat_dir.name}/{sub.name}/SKILL.md",
            }
            sk = sub / "SKILL.md"
            if sk.exists():
                try:
                    content = sk.read_text(encoding="utf-8", errors="replace")
                except Exception:
                    content = ""
                body = _apply_fm(entry, content)
                if not entry.get("name") or entry["name"] == sub.name:
                    h1 = first_h1(body or content)
                    if h1:
                        entry["name"] = h1
            out.append(entry)
    return out


def collect_prompts(root):
    out = []
    base = root / "prompts"
    if not base.exists():
        return out
    for p in sorted(base.rglob("*.md")):
        entry = {
            "id": p.stem,
            "name": p.stem,
            "category": "-",
            "difficulty": "-",
            "status": "-",
            "verified": False,
            "path": p.relative_to(root).as_posix(),
        }
        try:
            content = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            content = ""
        body = _apply_fm(entry, content)
        if not entry.get("name") or entry["name"] == p.stem:
            h1 = first_h1(body or content)
            if h1:
                entry["name"] = h1
        out.append(entry)
    return out


def collect_cases(root):
    out = []
    base = root / "cases"
    if not base.exists():
        return out
    for cat_dir in sorted(base.iterdir()):
        if not cat_dir.is_dir():
            continue
        for case_dir in sorted(cat_dir.iterdir()):
            if not case_dir.is_dir():
                continue
            entry = {
                "id": case_dir.name,
                "name": case_dir.name,
                "category": cat_dir.name,
                "difficulty": "-",
                "status": "-",
                "verified": False,
                "path": f"cases/{cat_dir.name}/{case_dir.name}/README.md",
            }
            readme = case_dir / "README.md"
            if readme.exists():
                try:
                    content = readme.read_text(encoding="utf-8", errors="replace")
                except Exception:
                    content = ""
                body = _apply_fm(entry, content)
                if not entry.get("name") or entry["name"] == case_dir.name:
                    h1 = first_h1(body)
                    if h1:
                        entry["name"] = h1
            out.append(entry)
    return out


def collect_workflows(root):
    out = []
    base = root / "workflows"
    if not base.exists():
        return out
    for wf_dir in sorted(base.iterdir()):
        if not wf_dir.is_dir():
            continue
        entry = {
            "id": wf_dir.name,
            "name": wf_dir.name,
            "category": "-",
            "difficulty": "-",
            "status": "-",
            "verified": False,
            "path": f"workflows/{wf_dir.name}/README.md",
        }
        readme = wf_dir / "README.md"
        if readme.exists():
            try:
                content = readme.read_text(encoding="utf-8", errors="replace")
            except Exception:
                content = ""
            body = _apply_fm(entry, content)
            if not entry.get("name") or entry["name"] == wf_dir.name:
                h1 = first_h1(body)
                if h1:
                    entry["name"] = h1
        out.append(entry)
    return out


def resolve_root(args):
    if args.root_opt:
        return Path(args.root_opt).resolve()
    if args.root:
        return Path(args.root).resolve()
    return Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser(description="Generate docs/INDEX.md.")
    ap.add_argument("root", nargs="?", default=None, help="repo root (default: two dirs up from this script) / 仓库根目录")
    ap.add_argument("--root", dest="root_opt", default=None, help="repo root (overrides positional) / 仓库根目录")
    args = ap.parse_args()
    root = resolve_root(args)

    skills = collect_skills(root)
    prompts = collect_prompts(root)
    cases = collect_cases(root)
    workflows = collect_workflows(root)

    columns = [
        ("id", "id"),
        ("name", "name"),
        ("category", "category"),
        ("difficulty", "difficulty"),
        ("status", "status"),
        ("verified", "verified"),
        ("path", "path"),
    ]

    def sort_key(e):
        return (str(e.get("category") or ""), str(e.get("name") or ""))

    lines = [
        "# EasyVibeCoding Index",
        "",
        "<!-- auto-generated by scripts/build-index.py — do not edit / 由脚本自动生成，请勿手改 -->",
        "",
    ]

    sections = [
        ("## Skills Index", skills),
        ("## Prompt Index", prompts),
        ("## Case Index", cases),
        ("## Workflow Index", workflows),
    ]
    for title, items in sections:
        lines.append(title)
        lines.append("")
        if items:
            lines.append(render_table(sorted(items, key=sort_key), columns))
        else:
            lines.append("_No entries yet._ / 暂无条目")
        lines.append("")

    docs_dir = root / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    index_path = docs_dir / "INDEX.md"
    index_path.write_text("\n".join(lines), encoding="utf-8")

    total = len(skills) + len(prompts) + len(cases) + len(workflows)
    print(f"Generated docs/INDEX.md with {total} entries / 共 {total} 条")
    return 0


if __name__ == "__main__":
    sys.exit(main())
