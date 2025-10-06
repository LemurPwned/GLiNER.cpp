#!/usr/bin/env python3
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "deps/tokenizers-cpp/msgpack/CMakeLists.txt",
    ROOT / "deps/tokenizers-cpp/msgpack/test-install/CMakeLists.txt",
    ROOT / "deps/tokenizers-cpp/sentencepiece/CMakeLists.txt",
]
PATTERN = re.compile(
    r"(?i)(cmake_minimum_required\s*\(\s*VERSION\s+)([0-9][0-9.]*)([^)]*\))"
)
TARGET_VERSION = "3.18"


def needs_update(version: str) -> bool:
    def parse(v: str) -> list[int]:
        return [int(p) for p in v.split(".") if p]

    current_parts = parse(version)
    target_parts = parse(TARGET_VERSION)
    length = max(len(current_parts), len(target_parts))
    current_parts += [0] * (length - len(current_parts))
    target_parts += [0] * (length - len(target_parts))
    return current_parts < target_parts


def make_replacer():
    state = {"updated": 0}
    seen_versions: list[str] = []

    def replacer(match: re.Match[str]) -> str:
        prefix, version, suffix = match.groups()
        seen_versions.append(version)
        if needs_update(version):
            state["updated"] += 1
            return f"{prefix}{TARGET_VERSION}{suffix}"
        return match.group(0)

    return PATTERN, replacer, state, seen_versions


def patch(path: pathlib.Path) -> int:
    if not path.exists():
        print(f"{path}: file not found")
        return 0
    text = path.read_text()
    pattern, replacer, state, seen_versions = make_replacer()
    new_text, _ = pattern.subn(replacer, text)
    if seen_versions:
        if state["updated"]:
            print(f"{path}: updated {state['updated']} occurrence(s) (found versions: {', '.join(seen_versions)})")
        else:
            print(f"{path}: already >= {TARGET_VERSION} (found versions: {', '.join(seen_versions)})")
    else:
        print(f"{path}: no cmake_minimum_required directive found")
    if state["updated"]:
        path.write_text(new_text)
    return state["updated"]


def main() -> int:
    total = 0
    for target in TARGETS:
        total += patch(target)
    if total == 0:
        print("No cmake_minimum_required directives updated.")
    else:
        print(f"Updated cmake_minimum_required in {total} location(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
