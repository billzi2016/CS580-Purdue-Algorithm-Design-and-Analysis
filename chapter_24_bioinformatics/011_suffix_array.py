"""教学版后缀数组构建。

适用场景：为短 DNA 或一般文本建立全部后缀的字典序索引，作为模式查询和 BWT 的基础。
核心思想：倍增法按长度 1、2、4… 的前缀等价类迭代细化，最终排序的是后缀起点而非后缀字符串。
输入输出：输入非空文本，输出下标数组；第 i 项是第 i 小后缀在原文本中的起点。
时间复杂度：O(n log² n)，每轮以比较排序重排等价类；空间复杂度 O(n)。
关键边界情况：空文本返回空数组；重复字符和 Unicode 字符均可处理；本版不追加终止符。
"""


def build_suffix_array(text: str) -> list[int]:
    """用倍增排名手写构建后缀数组。

    参数：text 是任意 Python 字符串。
    返回：按 text[start:] 字典序排列的所有 start 下标。
    边界情况：空串返回空列表；相同后缀前缀由较短后缀先出现的 Python 字符串序保证。
    关键算法点：rank[i] 表示长度 width 前缀的等价类，二元键 (rank[i], rank[i+width]) 即下一轮比较信息。
    """
    if not text:
        return []
    size = len(text)
    suffixes = list(range(size))
    rank = [ord(symbol) for symbol in text]
    width = 1
    while width < size:
        # 越过文本末尾的第二关键字为 -1，故短后缀排在有相同前缀的长后缀之前。
        suffixes.sort(
            key=lambda start: (
                rank[start],
                rank[start + width] if start + width < size else -1,
            )
        )
        new_rank = [0] * size
        class_id = 0
        new_rank[suffixes[0]] = class_id
        for position in range(1, size):
            current, previous = suffixes[position], suffixes[position - 1]
            current_key = (
                rank[current],
                rank[current + width] if current + width < size else -1,
            )
            previous_key = (
                rank[previous],
                rank[previous + width] if previous + width < size else -1,
            )
            if current_key != previous_key:
                class_id += 1
            new_rank[current] = class_id
        rank = new_rank
        if class_id == size - 1:
            break
        width *= 2
    return suffixes


def suffixes_in_order(text: str) -> list[str]:
    """返回排序后的后缀文本，便于教学检查；参数和边界与 build_suffix_array 相同。"""
    return [text[start:] for start in build_suffix_array(text)]


if __name__ == "__main__":
    assert build_suffix_array("banana") == [5, 3, 1, 0, 4, 2]
    assert suffixes_in_order("GAGA") == ["A", "AGA", "GA", "GAGA"]
    assert build_suffix_array("") == []
    assert build_suffix_array("AAAA") == [3, 2, 1, 0]
    print("011_suffix_array: all examples passed")
