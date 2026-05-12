"""
Drop lines whose VLESS display name (URI fragment after #) contains the Russia
flag emoji (U+1F1F7 U+1F1FA). Other lines are passed through unchanged.
"""
from __future__ import annotations

import sys
from urllib.parse import unquote, urlparse

# Regional indicators R + U → 🇷🇺
RUSSIA_FLAG = "\U0001f1f7\U0001f1fa"


def fragment_has_russia_flag(line: str) -> bool:
    s = line.strip()
    if not s or not s.startswith("vless://"):
        return False
    frag = urlparse(s).fragment or ""
    name = unquote(frag)
    return RUSSIA_FLAG in name


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: filter_russian_flag_name.py <in_path> <out_path>", file=sys.stderr)
        return 2
    in_path, out_path = sys.argv[1], sys.argv[2]
    with open(in_path, encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    kept = [ln for ln in lines if not fragment_has_russia_flag(ln)]
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.writelines(kept)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
