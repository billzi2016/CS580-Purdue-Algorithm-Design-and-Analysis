"""教学版 Burrows-Wheeler Transform（BWT）及逆变换。

适用场景：展示由循环移位排序导出的可逆文本重排，是压缩和 FM-index 的前置结构。
核心思想：给原文本加唯一终止符，按循环移位排序并收集每行末字符；逆变换利用稳定排序保持的 LF 对应关系。
输入输出：transform 返回 BWT 字符串；inverse 接收该字符串并恢复原始（不含终止符）文本。
时间复杂度：本教学版 transform 为 O(n² log n)（显式循环移位），inverse 为 O(n²)；空间复杂度 O(n²)。
关键边界情况：文本中不得已有终止符；空文本可变换；inverse 要求终止符恰好一次。
"""


TERMINATOR = "$"


def burrows_wheeler_transform(text: str, terminator: str = TERMINATOR) -> str:
    """构建带唯一终止符的 BWT 字符串。

    参数：text 是原文本；terminator 必须是长度为一且未出现在 text 中的字符。
    返回：排序循环移位矩阵最后一列；其长度为 len(text)+1。
    边界情况：空串结果为 terminator；终止符冲突或长度错误抛出 ValueError。
    关键算法点：终止符让循环移位可唯一对应原文本结尾，也令 BWT 可逆。
    """
    _validate_terminator(text, terminator)
    extended = text + terminator
    rotations = [extended[start:] + extended[:start] for start in range(len(extended))]
    rotations.sort()
    return "".join(rotation[-1] for rotation in rotations)


def inverse_burrows_wheeler(bwt: str, terminator: str = TERMINATOR) -> str:
    """从 BWT 字符串恢复不带终止符的原文本。

    参数：bwt 是 transform 的返回值；terminator 为唯一终止符。
    返回：原始文本。
    边界情况：空 BWT、终止符缺失/重复均抛出 ValueError。
    关键算法点：每轮稳定排序把已知末字符逐列前接，n 轮后恢复所有排序循环移位。
    """
    if len(terminator) != 1:
        raise ValueError("终止符必须恰好是一个字符")
    if not bwt or bwt.count(terminator) != 1:
        raise ValueError("BWT 必须包含且只包含一个终止符")
    rows = [""] * len(bwt)
    for _ in range(len(bwt)):
        rows = sorted(bwt[index] + rows[index] for index in range(len(bwt)))
    original = next(row for row in rows if row.endswith(terminator))
    return original[:-1]


def _validate_terminator(text: str, terminator: str) -> None:
    """确保终止符可唯一标记文本结尾，避免变换出现歧义。"""
    if len(terminator) != 1 or terminator in text:
        raise ValueError("终止符必须为一个未出现在文本中的字符")


if __name__ == "__main__":
    transformed = burrows_wheeler_transform("banana")
    assert transformed == "annb$aa"
    assert inverse_burrows_wheeler(transformed) == "banana"
    assert burrows_wheeler_transform("") == "$"
    assert inverse_burrows_wheeler("$") == ""
    try:
        burrows_wheeler_transform("A$C")
        raise AssertionError("应拒绝终止符冲突")
    except ValueError:
        pass
    print("013_burrows_wheeler_transform: all examples passed")
