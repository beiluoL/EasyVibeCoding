#!/usr/bin/env python3
"""Check local markdown links and scan for secrets.

1) For every *.md under repo root (skipping .git / node_modules / venv dirs):
   parse markdown links [text](url) (also image links ![alt](url)).
   For local targets (not http/https/mailto/ftp/tel/#), resolve relative to the
   .md file's directory and check the target exists. Strip #anchors and ?queries.
   Report broken links with file:line. Exit 1 if any broken local link.

2) Secrets scan across all files under repo root (skip .git / node_modules /
   venv; skip binary-ish extensions): fail if any of these patterns match:
   AKIA[0-9A-Z]{16}, sk-[A-Za-z0-9]{20,}, xox[baprs]-[A-Za-z0-9-]+,
   ghp_[A-Za-z0-9]{36}, a PEM "BEGIN ... PRIVATE KEY" header,
   an `api_key` assignment with a quoted value (case-insensitive)

Stdlib only (re, pathlib).
"""
import argparse
import re
import sys
from pathlib import Path

LINK_RE = re.compile(
    r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)"  # image
    r"|\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)"  # link
)

SECRET_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]+"),
    re.compile(r"ghp_[A-Za-z0-9]{36}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?i)api_key\s*=\s*['\"][^'\"]+['\"]"),
]

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "env", "__pycache__", ".pytest_cache"}
BINARY_EXT = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".pdf", ".zip", ".gz", ".lock"}


def is_local(url):
    u = url.strip()
    if not u:
        return False
    low = u.lower()
    if low.startswith(("http://", "https://", "mailto:", "ftp://", "tel:")):
        return False
    if low.startswith("#"):
        return False
    return True


def iter_files(root, suffix=None):
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if suffix is not None and p.suffix.lower() != suffix:
            continue
        yield p


def check_links_in_file(md, root):
    broken = []
    try:
        lines = md.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception as e:  # pragma: no cover - defensive
        broken.append((md, 0, f"cannot read: {e}"))
        return broken
    in_fence = False
    fence_char = ""
    for lineno, line in enumerate(lines, start=1):
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
            # links inside code fences are not markdown links
            continue
        for m in LINK_RE.finditer(line):
            url = m.group(2) or m.group(4)
            if not url:
                continue
            if not is_local(url):
                continue
            target_url = url.split("#", 1)[0].split("?", 1)[0]
            if not target_url:
                continue
            target = (md.parent / target_url).resolve()
            if not target.exists():
                broken.append((md, lineno, f"[{url}] -> {target}"))
    return broken


# Lines containing this marker are intentionally showing fake/example keys and are safe.
SAFE_EXEMPT = re.compile(r"(safe:\s*(example|demo|fake|placeholder|teaching|exempt)|not-a-real-key|placeholder-key|example-key|fake-key|redacted|# safe|<!-- safe)", re.IGNORECASE)


def scan_secrets(root):
    findings = []
    for p in iter_files(root):
        if p.suffix.lower() in BINARY_EXT:
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for line_idx, line in enumerate(text.splitlines(), start=1):
            if SAFE_EXEMPT.search(line):
                continue
            for pat in SECRET_PATTERNS:
                m = pat.search(line)
                if m:
                    findings.append((p, line_idx, m.group(0)))
    return findings


def resolve_root(args):
    if args.root_opt:
        return Path(args.root_opt).resolve()
    if args.root:
        return Path(args.root).resolve()
    return Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser(description="Check local markdown links and scan for secrets.")
    ap.add_argument("root", nargs="?", default=None, help="repo root (default: two dirs up from this script) / 仓库根目录")
    ap.add_argument("--root", dest="root_opt", default=None, help="repo root (overrides positional) / 仓库根目录")
    args = ap.parse_args()
    root = resolve_root(args)

    broken = []
    for md in iter_files(root, suffix=".md"):
        broken.extend(check_links_in_file(md, root))

    secrets = scan_secrets(root)

    exit_code = 0

    if broken:
        print(f"Broken local links ({len(broken)}) / 失效的本地链接：")
        for md, lineno, msg in broken:
            try:
                rel = md.relative_to(root).as_posix()
            except ValueError:
                rel = str(md)
            print(f"  {rel}:{lineno}: {msg}")
        exit_code = 1
    else:
        print("check-links: no broken local links / 无失效本地链接")

    if secrets:
        print(f"\nSECRET(s) detected ({len(secrets)}) / 检测到疑似密钥：")
        for p, lineno, match in secrets:
            try:
                rel = p.relative_to(root).as_posix()
            except ValueError:
                rel = str(p)
            print(f"  {rel}:{lineno}: {match}")
        exit_code = 1
    else:
        print("check-links: no secrets found / 未发现疑似密钥")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
