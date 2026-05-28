#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
BUILD_SUPPORT_PATH = ROOT_DIR / "build_support.py"


def load_build_support():
    spec = importlib.util.spec_from_file_location(
        "stew_build_support", BUILD_SUPPORT_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(
            f"Unable to load build support module from {BUILD_SUPPORT_PATH}"
        )

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    removed_files = load_build_support().prune_excluded_generated_files(ROOT_DIR)
    for removed_file in removed_files:
        print(removed_file.relative_to(ROOT_DIR).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
