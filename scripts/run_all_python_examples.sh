#!/usr/bin/env bash
set -euo pipefail

# 脚本意图：
#   遍历仓库中所有 chapter_* 目录下的 Python 文件，并逐个执行文件内
#   `if __name__ == "__main__":` 测试块。
#
# 失败策略：
#   任意一个 Python 文件返回非零退出码时，本脚本立即失败并返回非零状态。
#
# 使用方式：
#   bash scripts/run_all_python_examples.sh

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

found_any_file=0

while IFS= read -r -d '' python_file; do
    found_any_file=1
    relative_path="${python_file#"$repo_root"/}"
    echo "Running ${relative_path}"
    python3 "$python_file"
done < <(find "$repo_root" -type f -path "$repo_root/chapter_*/*.py" -print0 | sort -z)

if [[ "$found_any_file" -eq 0 ]]; then
    echo "No chapter Python files found."
else
    echo "All chapter Python examples passed."
fi
