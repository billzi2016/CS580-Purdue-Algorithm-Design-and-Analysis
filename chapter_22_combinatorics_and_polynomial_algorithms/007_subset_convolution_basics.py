"""
文件意图：手写集合幂集上的子集卷积基础实现。
适用场景：将两个“按位掩码索引的集合函数”按不相交划分组合，例如子集 DP 的分割转移。
核心思想：(f*g)(S)=Σ_{A⊆S} f(A)g(S\\A)，枚举 A 后补集 S\\A 自动保证二者不相交且并为 S。
输入输出：输入长度为 2^n 的两个整数列表，输出同长度的子集卷积。
时间复杂度：O(3^n)，因为所有掩码的子掩码总数为 3^n；空间复杂度 O(2^n)。
关键边界情况：空输入无对应的 n，长度不等或非二次幂长度均拒绝；长度 1 表示空全集。
"""


def subset_convolution(left: list[int], right: list[int]) -> list[int]:
    """计算两个集合函数的子集卷积。

    参数：left/right 的第 mask 项是全集子集 mask 上的函数值，长度必须均为 2^n。
    返回：相同掩码空间上的子集卷积值。
    边界情况：长度不匹配、空列表或非二次幂长度抛出 ValueError。
    关键算法点：对每个集合枚举全部子集，将余集作为另一个函数的索引，恰好枚举所有分割。
    """
    if not left or len(left) != len(right):
        raise ValueError("left 与 right 必须是等长非空列表")
    length = len(left)
    if length & (length - 1):
        raise ValueError("列表长度必须是二的幂")
    result = [0] * length
    for mask in range(length):
        submask = mask
        while True:
            complement = mask ^ submask
            # submask 与 complement 无公共位，且按位或正好恢复 mask。
            result[mask] += left[submask] * right[complement]
            if submask == 0:
                break
            submask = (submask - 1) & mask
    return result


def count_ordered_disjoint_partitions(element_count: int) -> list[int]:
    """返回每个子集被拆成两个有序不交部分的方案数，用于验证子集卷积含义。

    参数：element_count 是全集元素数。
    返回：第 mask 项等于 mask 中元素各自选择左/右部分的方案数。
    边界情况：负数抛出 ValueError；零元素全集只含空集，其方案数为 1。
    关键算法点：令两个函数均恒为 1，子集卷积直接统计每个集合的所有子集选择。
    """
    if element_count < 0:
        raise ValueError("element_count 不能为负数")
    size = 1 << element_count
    return subset_convolution([1] * size, [1] * size)


if __name__ == "__main__":
    # 掩码 0..3 分别代表 {}, {0}, {1}, {0,1}。
    assert subset_convolution([1, 1, 1, 1], [1, 1, 1, 1]) == [1, 2, 2, 4]
    assert subset_convolution([2], [3]) == [6]
    partitions = count_ordered_disjoint_partitions(3)
    assert partitions[0] == 1
    assert partitions[3] == 4
    assert partitions[7] == 8
    try:
        subset_convolution([1, 2], [1])
        raise AssertionError("长度不匹配应抛出 ValueError")
    except ValueError:
        pass
    print("007_subset_convolution_basics: all examples passed")
