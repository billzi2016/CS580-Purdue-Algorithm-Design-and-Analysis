#!/usr/bin/env bash
set -euo pipefail

# 使用 Ruff 自动修复 lint 问题，并统一格式化仓库中的全部 Python 代码。
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if ! command -v ruff >/dev/null 2>&1; then
    echo "Error: ruff is not installed or not available in PATH." >&2
    echo "Install Ruff, then run this script again." >&2
    exit 1
fi

echo "Running Ruff formatter in ${repo_root}"
ruff format "${repo_root}"

echo "Running Ruff lint fixes in ${repo_root}"
ruff check --fix "${repo_root}"

# Lint fixes may change imports or expressions, so normalize formatting once more.
echo "Running Ruff formatter after lint fixes"
ruff format "${repo_root}"

echo "All Python lint and formatting checks completed."
