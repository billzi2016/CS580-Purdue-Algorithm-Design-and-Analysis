"""
文件意图：手写实现莫队算法，离线回答数组区间内不同值个数。
适用场景：静态数组、多个区间查询且答案可随左右端点增删维护时。
核心思想：按块排序查询，使相邻查询的左右端点移动总量较小；维护当前窗口的频率表。
输入输出：输入整数数组与闭区间查询，返回每个区间的不同值个数。
时间复杂度：O((n+q)sqrt(n))，空间复杂度：O(n)。
关键边界：空数组仅允许无查询；区间端点必须满足 0 <= left <= right < n。
"""


def mo_distinct_count(values: list[int], queries: list[tuple[int, int]]) -> list[int]:
    """离线计算每个闭区间中不同整数的个数。

    参数：values 为静态数组；queries 的元素为 (left, right) 闭区间。
    返回：按原查询顺序排列的不同值个数。
    边界情况：空数组且查询为空时返回空列表；非法区间抛出 ValueError。
    关键算法点：窗口每次只移动一个端点，并同步更新该值出现频率和不同值数。
    """
    if not values:
        if queries:
            raise ValueError("空数组不能包含区间查询")
        return []
    if any(left < 0 or right < left or right >= len(values) for left, right in queries):
        raise ValueError("查询必须是数组内的合法闭区间")
    block_size = max(1, int(len(values) ** 0.5))
    indexed = list(enumerate(queries))
    # 奇偶块反向排列 right，减少跨块时右端点的大幅回跳。
    indexed.sort(key=lambda item: (item[1][0] // block_size, item[1][1] if (item[1][0] // block_size) % 2 == 0 else -item[1][1]))
    answer = [0] * len(queries)
    frequency: dict[int, int] = {}
    left, right, distinct = 0, -1, 0

    def add(index: int) -> None:
        nonlocal distinct
        value = values[index]
        if frequency.get(value, 0) == 0:
            distinct += 1
        frequency[value] = frequency.get(value, 0) + 1

    def remove(index: int) -> None:
        nonlocal distinct
        value = values[index]
        frequency[value] -= 1
        if frequency[value] == 0:
            distinct -= 1
            del frequency[value]

    for original_index, (target_left, target_right) in indexed:
        while left > target_left:
            left -= 1
            add(left)
        while right < target_right:
            right += 1
            add(right)
        while left < target_left:
            remove(left)
            left += 1
        while right > target_right:
            remove(right)
            right -= 1
        answer[original_index] = distinct
    return answer


if __name__ == "__main__":
    assert mo_distinct_count([1, 1, 2, 1, 3, 2], [(0, 2), (1, 4), (3, 5), (2, 2)]) == [2, 3, 3, 1]
    assert mo_distinct_count([7], [(0, 0)]) == [1]
    assert mo_distinct_count([], []) == []
    print("001_mos_algorithm: all examples passed")
