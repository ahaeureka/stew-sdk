from __future__ import annotations

from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py
from setuptools.command.sdist import sdist as _sdist

from build_support import find_excluded_generated_files


ROOT_DIR = Path(__file__).resolve().parent


def ensure_publishable_generated_surface() -> None:
    blocked_files = find_excluded_generated_files(ROOT_DIR)
    if not blocked_files:
        return

    rendered_files = ", ".join(
        sorted(path.relative_to(ROOT_DIR).as_posix() for path in blocked_files)
    )
    raise RuntimeError(
        "Publishable Python SDK cannot include admin-only generated modules. "
        "Run 'uv run python scripts/prune_publishable_generated_modules.py' before building. "
        f"Found: {rendered_files}"
    )


class build_py(_build_py):
    def run(self) -> None:
        ensure_publishable_generated_surface()
        super().run()


class sdist(_sdist):
    def make_release_tree(self, base_dir: str, files: list[str]) -> None:
        ensure_publishable_generated_surface()
        super().make_release_tree(base_dir, files)


setup(
    cmdclass={
        "build_py": build_py,
        "sdist": sdist,
    }
)
