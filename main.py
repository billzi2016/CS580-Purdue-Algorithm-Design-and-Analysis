"""
文件意图：提供仓库级 Python smoke-test 入口，逐个执行所有 chapter 示例。
适用场景：本地开发、持续集成以及无法直接运行 Bash 脚本的环境。
核心思想：发现 chapter_* 目录中的 Python 文件，并在独立子进程中执行其断言。
输入输出：不接收命令行参数；输出每个脚本的相对路径与最终执行数量。
时间复杂度：O(n)，其中 n 为算法脚本数量，不含各脚本自身运行时间。
空间复杂度：O(n)，用于保存排序后的脚本路径。
关键边界：没有算法脚本或任一子进程失败时立即抛出异常并返回非零状态。
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent


def discover_python_examples(repository_root: Path = REPOSITORY_ROOT) -> list[Path]:
    """发现并排序仓库中的全部算法示例。

    参数：repository_root 为待扫描仓库根目录。
    返回值：按稳定字典序排列的 chapter Python 文件绝对路径。
    边界情况：目录不存在或没有匹配文件时返回空列表。
    关键算法点：只匹配 chapter_* 的直接子文件，避免执行缓存和辅助文件。
    """

    return sorted(repository_root.glob("chapter_*/*.py"))


def run_python_example(
    example_path: Path, repository_root: Path = REPOSITORY_ROOT
) -> None:
    """在独立 Python 子进程中执行一个算法示例。

    参数：example_path 为脚本路径，repository_root 为子进程工作目录。
    返回值：成功时无返回值。
    边界情况：脚本不存在时抛出 FileNotFoundError，断言失败时抛出 RuntimeError。
    关键算法点：复用当前解释器，并禁止生成字节码缓存以保持工作树整洁。
    """

    if not example_path.is_file():
        raise FileNotFoundError(f"算法脚本不存在：{example_path}")

    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    relative_path = example_path.relative_to(repository_root)
    print(f"Running {relative_path}", flush=True)
    result = subprocess.run(
        [sys.executable, str(example_path)],
        cwd=repository_root,
        env=environment,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"算法示例执行失败：{relative_path}")


def run_all_python_examples(repository_root: Path = REPOSITORY_ROOT) -> int:
    """发现并执行仓库中的全部算法示例。

    参数：repository_root 为仓库根目录。
    返回值：成功执行的脚本数量。
    边界情况：没有发现脚本时抛出 RuntimeError；任一脚本失败时立即停止。
    关键算法点：每个文件使用独立进程，避免模块全局状态互相污染。
    """

    examples = discover_python_examples(repository_root)
    if not examples:
        raise RuntimeError("没有发现 chapter Python 算法脚本")
    for example_path in examples:
        run_python_example(example_path, repository_root)
    return len(examples)


if __name__ == "__main__":
    completed_count = run_all_python_examples()
    print(f"All {completed_count} chapter Python examples passed.")
