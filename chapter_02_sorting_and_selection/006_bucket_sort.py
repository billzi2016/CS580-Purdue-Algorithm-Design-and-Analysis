"""
文件意图：手写实现区间 [0, 1) 浮点数的桶排序。
适用场景：输入近似均匀分布在固定区间，且希望获得接近线性的平均性能时。
核心思想：按数值映射到桶，各桶使用手写插入排序，最后按桶序拼接。
输入输出：输入 [0, 1) 内浮点数，返回新的非递减排序列表。
时间复杂度：平均 O(n)，最坏 O(n^2)。空间复杂度：O(n)。
关键边界：空列表可处理；区间外值会被拒绝，1.0 不属于本版本的输入区间。
"""


def _insertion_sort(values: list[float]) -> None:
    """原地使用插入排序整理单个小桶。"""
    for index in range(1, len(values)):
        current = values[index]
        position = index - 1
        while position >= 0 and values[position] > current:
            values[position + 1] = values[position]
            position -= 1
        values[position + 1] = current


def bucket_sort(values: list[float]) -> list[float]:
    """返回 [0, 1) 浮点数 values 的非递减排序副本。

    参数：values 为范围在 [0, 1) 的浮点数列表。
    返回：新排序列表。
    边界情况：空列表直接返回，范围外数值抛出 ValueError。
    关键算法点：桶编号 int(value * n) 保证每个合法值恰好映射到一个桶。
    """
    if any(value < 0.0 or value >= 1.0 for value in values):
        raise ValueError("bucket_sort 只支持区间 [0, 1) 内的数值")
    bucket_count = len(values)
    if bucket_count == 0:
        return []
    buckets = [[] for _ in range(bucket_count)]
    for value in values:
        buckets[int(value * bucket_count)].append(value)
    result: list[float] = []
    for bucket in buckets:
        _insertion_sort(bucket)
        result.extend(bucket)
    return result


if __name__ == "__main__":
    assert bucket_sort([]) == []
    assert bucket_sort([0.5]) == [0.5]
    assert bucket_sort([0.78, 0.17, 0.39, 0.26, 0.72, 0.17]) == [0.17, 0.17, 0.26, 0.39, 0.72, 0.78]
    try:
        bucket_sort([1.0])
        assert False, "区间外值应被拒绝"
    except ValueError as error:
        assert "[0, 1)" in str(error)
    print("006_bucket_sort: all examples passed")
