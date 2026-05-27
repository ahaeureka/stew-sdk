from __future__ import annotations

from pathlib import Path


EXCLUDED_GENERATED_PROTO_STEMS = (
    "audit",
    "apikey",
    "authorization",
    "billing_admin",
    "billing_strategy_admin",
    "business_membership_admin",
    "pricing_admin",
)


def excluded_generated_module_names() -> tuple[str, ...]:
    module_names: list[str] = []
    for stem in EXCLUDED_GENERATED_PROTO_STEMS:
        module_names.extend(
            (
                f"stew.api.v1.{stem}_model",
                f"stew.api.v1.{stem}_pb2",
                f"stew.api.v1.{stem}_pb2_grpc",
            )
        )
    return tuple(module_names)


def excluded_generated_file_paths() -> tuple[Path, ...]:
    file_paths: list[Path] = []
    for stem in EXCLUDED_GENERATED_PROTO_STEMS:
        file_paths.extend(
            (
                Path("stew/api/v1") / f"{stem}_model.py",
                Path("stew/api/v1") / f"{stem}_pb2.py",
                Path("stew/api/v1") / f"{stem}_pb2.pyi",
                Path("stew/api/v1") / f"{stem}_pb2_grpc.py",
            )
        )
    return tuple(file_paths)


def find_excluded_generated_files(root_dir: Path) -> list[Path]:
    return [
        root_dir / relative_path
        for relative_path in excluded_generated_file_paths()
        if (root_dir / relative_path).exists()
    ]


def prune_excluded_generated_files(root_dir: Path) -> list[Path]:
    removed_files: list[Path] = []
    for relative_path in excluded_generated_file_paths():
        target_path = root_dir / relative_path
        if not target_path.exists():
            continue
        target_path.unlink()
        removed_files.append(target_path)
    return removed_files
