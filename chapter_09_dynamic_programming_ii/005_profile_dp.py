"""
文件意图：
    本文件手写实现轮廓线 DP，以统计 m x n 棋盘用 1x2 多米诺骨牌完全覆盖的方案数为例。

适用场景：
    网格逐格扫描，当前状态可以用一行/轮廓的占用位表示。

核心思想：
    mask 表示当前行哪些格子已被上一行竖放骨牌占用。逐行生成下一行 mask。

时间复杂度：
    O(rows * states * transitions)

空间复杂度：
    O(2^cols)
"""


def count_domino_tilings(rows: int, cols: int) -> int:
    """统计 rows x cols 棋盘的多米诺完全覆盖方案数。"""
    if rows < 0 or cols < 0:
        raise ValueError("行列数必须非负")
    if rows == 0 or cols == 0:
        return 1
    if cols > rows:
        rows, cols = cols, rows

    dp = {0: 1}
    full_mask = (1 << cols) - 1

    for _ in range(rows):
        next_dp: dict[int, int] = {}
        for mask, count in dp.items():
            for next_mask in _generate_next_masks(cols, 0, mask, 0):
                next_dp[next_mask] = next_dp.get(next_mask, 0) + count
        dp = next_dp

    return dp.get(0, 0)


def _generate_next_masks(cols: int, position: int, current_mask: int, next_mask: int) -> list[int]:
    """递归生成当前行 mask 对应的所有下一行 mask。"""
    if position == cols:
        return [next_mask]
    if current_mask & (1 << position):
        return _generate_next_masks(cols, position + 1, current_mask, next_mask)

    result: list[int] = []
    # 竖放骨牌，占用下一行同列。
    result.extend(_generate_next_masks(cols, position + 1, current_mask, next_mask | (1 << position)))
    # 横放骨牌，占用当前行相邻两格。
    if position + 1 < cols and not (current_mask & (1 << (position + 1))):
        result.extend(_generate_next_masks(cols, position + 2, current_mask, next_mask))
    return result


if __name__ == "__main__":
    assert count_domino_tilings(1, 1) == 0
    assert count_domino_tilings(1, 2) == 1
    assert count_domino_tilings(2, 2) == 2
    assert count_domino_tilings(2, 3) == 3
    assert count_domino_tilings(0, 5) == 1

    print("005_profile_dp: all examples passed")
