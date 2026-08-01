"""
文件意图：手写实现 Manacher 算法，在线性时间内求最长回文子串。
适用场景：需要在长字符串中快速寻找最长回文结构时。
核心思想：分别维护奇数和偶数回文半径，镜像位置可复用当前最右回文区间的信息。
输入输出：输入字符串，返回一个最长回文子串。
时间复杂度：O(n)。空间复杂度：O(n)。
关键边界：空串返回空串；有多个等长答案时返回最先出现的一个。
"""


def longest_palindromic_substring(text: str) -> str:
    """返回 text 中最先出现的最长回文子串。

    参数：text 为任意字符串。
    返回：最长回文子串；空串返回空串。
    边界情况：单字符、全相同字符以及偶数长度回文均可处理。
    关键算法点：镜像半径给出扩展下界，只有越过当前右边界时才做新比较。
    """
    length = len(text)
    if length == 0:
        return ""
    odd = [0] * length
    left = 0
    right = -1
    best_start = 0
    best_length = 1
    for center in range(length):
        radius = (
            1 if center > right else min(odd[left + right - center], right - center + 1)
        )
        while (
            center - radius >= 0
            and center + radius < length
            and text[center - radius] == text[center + radius]
        ):
            radius += 1
        odd[center] = radius
        candidate_length = 2 * radius - 1
        candidate_start = center - radius + 1
        if candidate_length > best_length:
            best_start, best_length = candidate_start, candidate_length
        if center + radius - 1 > right:
            left, right = center - radius + 1, center + radius - 1

    even = [0] * length
    left = 0
    right = -1
    for center in range(length):
        radius = (
            0
            if center > right
            else min(even[left + right - center + 1], right - center + 1)
        )
        while (
            center - radius - 1 >= 0
            and center + radius < length
            and text[center - radius - 1] == text[center + radius]
        ):
            radius += 1
        even[center] = radius
        candidate_length = 2 * radius
        candidate_start = center - radius
        if candidate_length > best_length:
            best_start, best_length = candidate_start, candidate_length
        if center + radius - 1 > right:
            left, right = center - radius, center + radius - 1
    return text[best_start : best_start + best_length]


if __name__ == "__main__":
    assert longest_palindromic_substring("") == ""
    assert longest_palindromic_substring("a") == "a"
    assert longest_palindromic_substring("babad") == "bab"
    assert longest_palindromic_substring("cbbd") == "bb"
    assert longest_palindromic_substring("aaaa") == "aaaa"
    print("008_manacher: all examples passed")
