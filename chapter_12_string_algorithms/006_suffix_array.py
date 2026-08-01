"""
文件意图：手写实现前缀倍增法构造后缀数组。
适用场景：需要按字典序访问所有后缀，作为 LCP、子串检索和压缩算法的基础。
核心思想：以长度 1 的字符秩为起点，每轮按两段长度为 step 的秩对给后缀重新编号。
输入输出：输入字符串，返回按对应后缀字典序排列的起始下标。
时间复杂度：O(n log^2 n)，每轮使用手写归并排序。空间复杂度：O(n)。
关键边界：空串返回空数组，重复字符和 Unicode 字符均可比较。
"""


def _merge_sort_indices(indices: list[int], ranks: list[int], step: int) -> list[int]:
    """按 (ranks[i], ranks[i + step]) 使用手写归并排序后缀下标。"""
    if len(indices) <= 1:
        return indices[:]
    middle = len(indices) // 2
    left = _merge_sort_indices(indices[:middle], ranks, step)
    right = _merge_sort_indices(indices[middle:], ranks, step)
    result: list[int] = []
    left_index = right_index = 0

    def key(index: int) -> tuple[int, int]:
        return ranks[index], ranks[index + step] if index + step < len(ranks) else -1

    while left_index < len(left) and right_index < len(right):
        if key(left[left_index]) <= key(right[right_index]):
            result.append(left[left_index])
            left_index += 1
        else:
            result.append(right[right_index])
            right_index += 1
    result.extend(left[left_index:])
    result.extend(right[right_index:])
    return result


def suffix_array(text: str) -> list[int]:
    """返回 text 的后缀数组。

    参数：text 为任意字符串。
    返回：按 text[index:] 字典序升序排列的全部 index。
    边界情况：空字符串返回空列表。
    关键算法点：每轮秩相同当且仅当两个长度为 2*step 的前缀相同。
    """
    length = len(text)
    if length == 0:
        return []
    indices = list(range(length))
    ranks = [ord(character) for character in text]
    step = 1
    while step < length:
        indices = _merge_sort_indices(indices, ranks, step)
        next_ranks = [0] * length
        rank = 0
        next_ranks[indices[0]] = rank
        for position in range(1, length):
            current = indices[position]
            previous = indices[position - 1]
            current_key = (ranks[current], ranks[current + step] if current + step < length else -1)
            previous_key = (ranks[previous], ranks[previous + step] if previous + step < length else -1)
            if current_key != previous_key:
                rank += 1
            next_ranks[current] = rank
        ranks = next_ranks
        if rank == length - 1:
            break
        step *= 2
    return indices


if __name__ == "__main__":
    assert suffix_array("") == []
    assert suffix_array("a") == [0]
    assert suffix_array("banana") == [5, 3, 1, 0, 4, 2]
    assert suffix_array("aaaa") == [3, 2, 1, 0]
    assert suffix_array("cba") == [2, 1, 0]
    print("006_suffix_array: all examples passed")
