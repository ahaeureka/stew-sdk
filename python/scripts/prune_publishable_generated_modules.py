#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

from build_support import prune_excluded_generated_files


def main() -> int:
    root_dir = Path(__file__).resolve().parents[1]
    removed_files = prune_excluded_generated_files(root_dir)
    for removed_file in removed_files:
        print(removed_file.relative_to(root_dir).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
