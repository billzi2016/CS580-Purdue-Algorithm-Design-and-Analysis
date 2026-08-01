"""整数序列 Delta Encoding（差分编码）的教学实现。

适用场景：相邻数值变化较小时，以首个值和相邻差值存储序列可降低后续整数的量级，常与
变长整数编码组合使用。本实现只负责无损差分表示，不执行熵编码或字节打包。

输入输出：编码将整数列表转换为等长列表，首项保留、其余项为当前值减前值；解码执行
前缀累加恢复原列表。
时间复杂度：编码和解码均为 O(n)。空间复杂度：O(n)。
关键边界：空列表往返为空列表；支持负数与重复值；布尔值和非整数输入会抛出 ValueError。
"""


def _validate_integers(values: list[int], name: str) -> None:
    """验证列表元素是普通整数而非布尔值，防止 True/False 被静默当作 1/0。"""
    if not isinstance(values, list) or any(
        isinstance(value, bool) or not isinstance(value, int) for value in values
    ):
        raise ValueError(f"{name} 必须是整数列表")


def delta_encode(values: list[int]) -> list[int]:
    """将整数序列编码为首项与相邻差值。

    参数：values 为待编码的整数列表。
    返回值：首元素不变，之后每项为 ``values[i] - values[i - 1]``。
    边界情况：空列表返回空列表；负数、递减序列和重复值均可处理。
    关键算法点：前一原始值而非前一差值参与相减，保证解码时单次前缀累加即可恢复。
    """
    _validate_integers(values, "values")
    if not values:
        return []
    encoded = [values[0]]
    previous = values[0]
    for current in values[1:]:
        encoded.append(current - previous)
        previous = current
    return encoded


def delta_decode(deltas: list[int]) -> list[int]:
    """从首项与相邻差值恢复整数序列。

    参数：deltas 为 delta_encode 的输出。
    返回值：恢复出的整数列表。
    边界情况：空列表返回空列表；支持任意 Python 整数范围内的累计结果。
    关键算法点：循环不变量是 previous 始终等于上一个已恢复原始值，故加上当前差值恰得下一值。
    """
    _validate_integers(deltas, "deltas")
    if not deltas:
        return []
    decoded = [deltas[0]]
    previous = deltas[0]
    for delta in deltas[1:]:
        previous += delta
        decoded.append(previous)
    return decoded


if __name__ == "__main__":
    sample = [100, 103, 103, 97, 120]
    assert delta_encode(sample) == [100, 3, 0, -6, 23]
    assert delta_decode(delta_encode(sample)) == sample
    assert delta_encode([]) == []
    assert delta_decode([]) == []
    assert delta_decode([-5, -2, 7]) == [-5, -7, 0]
    try:
        delta_encode([1, True])
        raise AssertionError("布尔值应当抛出 ValueError")
    except ValueError:
        pass

    print("010_delta_encoding: all examples passed")
