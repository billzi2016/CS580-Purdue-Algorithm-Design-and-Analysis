"""通过 pytest 参数化执行仓库中的每个 chapter Python 示例。"""

from pathlib import Path

import pytest

from main import discover_python_examples, run_python_example

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_PATHS = discover_python_examples(REPOSITORY_ROOT)


def _example_id(example_path: Path) -> str:
    """生成包含 chapter 与文件名的稳定 pytest 用例标识。"""

    return str(example_path.relative_to(REPOSITORY_ROOT))


def test_repository_contains_python_examples() -> None:
    """确认测试发现逻辑至少找到一个算法脚本。"""

    assert EXAMPLE_PATHS


@pytest.mark.parametrize("example_path", EXAMPLE_PATHS, ids=_example_id)
def test_python_example(example_path: Path) -> None:
    """在隔离子进程中验证一个算法文件的 __main__ 断言。"""

    run_python_example(example_path, REPOSITORY_ROOT)
