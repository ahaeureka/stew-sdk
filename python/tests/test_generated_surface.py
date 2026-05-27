from __future__ import annotations

import importlib

import pytest

from build_support import excluded_generated_module_names


@pytest.mark.parametrize("module_name", excluded_generated_module_names())
def test_admin_only_generated_modules_are_not_importable(module_name: str) -> None:
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module(module_name)
