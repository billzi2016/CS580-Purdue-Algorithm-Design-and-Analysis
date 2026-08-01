"""
文件意图：
    本文件对比递归与迭代的基础模式，帮助后续理解 DFS、DP 和分治算法。

适用场景：
    递归适合表达天然分解的问题；迭代适合避免递归深度风险或显式维护状态。

核心思想：
    同一个数学定义通常可以写成递归形式，也可以转换为循环形式。
"""


def factorial_recursive(n: int) -> int:
    """
    递归计算 n!。

    边界情况：
        0! = 1，1! = 1。
    """
    if n < 0:
        raise ValueError("n 必须非负")
    if n <= 1:
        return 1
    return n * factorial_recursive(n - 1)


def factorial_iterative(n: int) -> int:
    """
    迭代计算 n!。

    优点：
        避免递归调用栈，适合较大的 n。
    """
    if n < 0:
        raise ValueError("n 必须非负")

    result = 1
    for value in range(2, n + 1):
        result *= value
    return result


def sum_recursive(nums: list[int], index: int = 0) -> int:
    """
    递归计算 nums[index:] 的元素和。
    """
    if index == len(nums):
        return 0
    return nums[index] + sum_recursive(nums, index + 1)


def sum_iterative(nums: list[int]) -> int:
    """
    迭代计算数组元素和，不调用内置 sum，确保核心逻辑手写。
    """
    total = 0
    for value in nums:
        total += value
    return total


if __name__ == "__main__":
    assert factorial_recursive(0) == 1
    assert factorial_recursive(5) == 120
    assert factorial_iterative(5) == 120
    assert sum_recursive([1, 2, 3, 4]) == 10
    assert sum_iterative([1, 2, 3, 4]) == 10
    assert sum_iterative([]) == 0

    print("010_recursion_and_iteration: all examples passed")
