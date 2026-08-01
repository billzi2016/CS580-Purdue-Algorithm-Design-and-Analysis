"""
文件意图：手写单调栈求每个元素右侧第一个严格更小元素。
适用场景：next-smaller 查询、直方图最大矩形等需要延迟结算元素的问题。
核心思想：栈保存尚未找到答案的下标，且对应值从栈底到栈顶非递减。
输入输出：输入整数列表，返回每个位置答案的下标。
时间复杂度：O(n)。空间复杂度：O(n)。
关键边界：空输入返回空列表；右侧不存在更小元素时答案为 -1；相等元素不互相结算。
"""


def next_smaller_indices(values: list[int]) -> list[int]:
    """返回每个元素右侧第一个严格更小元素的下标。

    参数：values 为整数列表。
    返回：与 values 等长的下标列表，不存在答案的位置为 -1。
    边界情况：空输入返回空列表；重复值不会被视为严格更小。
    关键算法点：每个下标至多入栈和出栈一次，所以总时间复杂度为线性。
    """
    result = [-1] * len(values)
    stack: list[int] = []

    for index, value in enumerate(values):
        # 新值是所有比它大的栈顶元素第一次遇到的右侧更小元素。
        while stack and values[stack[-1]] > value:
            result[stack.pop()] = index
        stack.append(index)

    return result


if __name__ == "__main__":
    assert next_smaller_indices([]) == []
    assert next_smaller_indices([4, 8, 5, 2, 25]) == [3, 2, 3, -1, -1]
    assert next_smaller_indices([2, 2, 1]) == [2, 2, -1]
    print("002_monotonic_stack: all examples passed")
