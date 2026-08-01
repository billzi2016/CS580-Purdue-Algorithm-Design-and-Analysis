"""
文件意图：
    本文件手写实现数位 DP，用于统计 0..n 中不含指定数字的整数数量。

适用场景：
    需要按十进制位约束计数，且上界很大不能逐个枚举。

核心思想：
    从高位到低位递归，状态包含当前位置、是否受到上界限制、是否已经开始构造数字。

时间复杂度：
    O(位数 * 10)

空间复杂度：
    O(位数)
"""


def count_numbers_without_digit(limit: int, forbidden_digit: int) -> int:
    """统计闭区间 [0, limit] 中十进制表示不含 forbidden_digit 的整数数量。"""
    if limit < 0:
        return 0
    if not 0 <= forbidden_digit <= 9:
        raise ValueError("forbidden_digit 必须在 0..9")

    digits = [int(char) for char in str(limit)]
    memo: dict[tuple[int, bool, bool], int] = {}

    def solve(position: int, tight: bool, started: bool) -> int:
        if position == len(digits):
            # 数字 0 的表示为 "0"，因此 forbidden_digit 为 0 时不能计入。
            return 0 if not started and forbidden_digit == 0 else 1

        key = (position, tight, started)
        if not tight and key in memo:
            return memo[key]

        upper = digits[position] if tight else 9
        total = 0
        for digit in range(upper + 1):
            next_tight = tight and digit == upper
            next_started = started or digit != 0

            if next_started and digit == forbidden_digit:
                continue
            total += solve(position + 1, next_tight, next_started)

        if not tight:
            memo[key] = total
        return total

    return solve(0, True, False)


if __name__ == "__main__":
    assert count_numbers_without_digit(20, 3) == 19
    assert count_numbers_without_digit(9, 0) == 9
    assert count_numbers_without_digit(0, 0) == 0
    assert count_numbers_without_digit(0, 1) == 1

    print("003_digit_dp: all examples passed")
