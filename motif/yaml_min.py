"""Restricted YAML reader — zero dependencies.

Supports the subset Motif policy files use: nested maps (2-space indent),
`key: value`, `key:` block parents, `- scalar` lists, `#` comments, and
quoted scalars. Prefers the real `pyyaml` when installed. This is intentionally
small; keep `security/*.yml` within the supported subset.
"""
from __future__ import annotations
from typing import Any

try:
    import yaml as _yaml  # type: ignore

    def load(text: str) -> Any:
        return _yaml.safe_load(text)

except Exception:
    def _scalar(s: str) -> Any:
        s = s.strip()
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            return s[1:-1]
        low = s.lower()
        if low in ("true", "yes"):
            return True
        if low in ("false", "no"):
            return False
        if low in ("null", "~", ""):
            return None
        try:
            return int(s)
        except ValueError:
            pass
        try:
            return float(s)
        except ValueError:
            return s

    def _parse(lines: list[tuple[int, str]], idx: int, indent: int):
        # returns (value, next_index)
        # peek to decide list vs map
        while idx < len(lines) and lines[idx][1].strip() == "":
            idx += 1
        if idx >= len(lines):
            return None, idx
        cur_indent, content = lines[idx]
        if content.lstrip().startswith("- "):
            result: list[Any] = []
            while idx < len(lines):
                ci, c = lines[idx]
                if c.strip() == "":
                    idx += 1
                    continue
                if ci < indent or not c.lstrip().startswith("- "):
                    break
                item = c.lstrip()[2:]
                result.append(_scalar(item))
                idx += 1
            return result, idx
        result_map: dict[str, Any] = {}
        while idx < len(lines):
            ci, c = lines[idx]
            if c.strip() == "":
                idx += 1
                continue
            if ci < indent:
                break
            stripped = c.strip()
            if ":" not in stripped:
                idx += 1
                continue
            key, _, rest = stripped.partition(":")
            key = key.strip()
            rest = rest.strip()
            if rest == "":
                child, idx = _parse(lines, idx + 1, ci + 1)
                result_map[key] = child
            else:
                result_map[key] = _scalar(rest)
                idx += 1
        return result_map, idx

    def load(text: str) -> Any:
        lines: list[tuple[int, str]] = []
        for raw in text.splitlines():
            # strip full-line and trailing comments (naive but fine for our files)
            if raw.strip().startswith("#"):
                continue
            line = raw.split(" #", 1)[0].rstrip()
            if line.strip() == "":
                continue
            indent = len(line) - len(line.lstrip(" "))
            lines.append((indent, line))
        value, _ = _parse(lines, 0, 0)
        return value
