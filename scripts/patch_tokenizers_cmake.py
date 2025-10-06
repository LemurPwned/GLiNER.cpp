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
PATTERN = re.compile(r"(?i)cmake_minimum_required\s*\(\s*VERSION\s+3\.1\s+FATAL_ERROR\s*\)")
REPLACEMENT = "cmake_minimum_required(VERSION 3.18 FATAL_ERROR)"


def patch(path: pathlib.Path) -> int:
    if not path.exists():
        return 0
    text = path.read_text()
    new_text, count = PATTERN.subn(REPLACEMENT, text)
    if count:
        path.write_text(new_text)
    return count


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
