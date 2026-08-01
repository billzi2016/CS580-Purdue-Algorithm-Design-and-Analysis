"""算术编码的精确有理数教学实现。

适用场景：算术编码把整个符号序列映射到区间中的一个数，适用于已知有限符号模型的
无损熵编码。本基础版使用 ``fractions.Fraction`` 避免浮点舍入；它用于解释区间细分，
不包含工业格式所需的有限精度重整化和位流输出。

输入输出：从文本建立静态频率模型；编码返回区间内的有理数标签，解码以标签、模型及
原始符号数恢复文本。
时间复杂度：朴素实现每个符号扫描字母表，编码与解码均为 O(nk)，k 为字母表大小。
空间复杂度：O(k)，不含 Fraction 整数随输入增长的实际存储开销。
关键边界：空文本使用空模型和标签 0；标签必须位于 [0, 1)；解码长度不能为负。
"""

from fractions import Fraction


FrequencyModel = dict[str, int]


def build_frequency_model(text: str) -> FrequencyModel:
    """按首次出现顺序建立静态频率模型。

    参数：text 为待编码文本。
    返回值：符号到正整数频率的映射，映射的插入顺序也定义区间划分顺序。
    边界情况：空文本返回空字典；非字符串输入抛出 TypeError。
    关键算法点：编码器和解码器必须使用完全相同的符号顺序及频率，才能选择相同子区间。
    """
    if not isinstance(text, str):
        raise TypeError("text 必须是字符串")
    model: FrequencyModel = {}
    for symbol in text:
        model[symbol] = model.get(symbol, 0) + 1
    return model


def _validated_intervals(model: FrequencyModel) -> tuple[list[tuple[str, Fraction, Fraction]], int]:
    """将频率模型转换为 [0, 1) 中连续且不重叠的累计概率区间。"""
    total = 0
    for symbol, frequency in model.items():
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("模型符号必须恰好包含一个字符")
        if isinstance(frequency, bool) or not isinstance(frequency, int) or frequency <= 0:
            raise ValueError("模型频率必须是正整数")
        total += frequency
    if not model:
        return [], 0

    intervals: list[tuple[str, Fraction, Fraction]] = []
    cumulative = 0
    for symbol, frequency in model.items():
        lower = Fraction(cumulative, total)
        cumulative += frequency
        upper = Fraction(cumulative, total)
        intervals.append((symbol, lower, upper))
    return intervals, total


def arithmetic_encode(text: str, model: FrequencyModel) -> Fraction:
    """把文本映射为最终算术编码区间内的有理数标签。

    参数：text 为待编码文本；model 为静态频率模型。
    返回值：最终半开区间 [low, high) 内的中点标签。
    边界情况：空文本仅可与空模型配合，并返回 Fraction(0, 1)；模型遗漏符号抛出 ValueError。
    关键算法点：每读一个符号，都把当前区间按模型概率缩放到该符号子区间；中点保证落在
        最终区间内部而不触碰上边界。
    """
    intervals, _ = _validated_intervals(model)
    if not text:
        if model:
            raise ValueError("空文本必须使用空频率模型")
        return Fraction(0, 1)
    if not intervals:
        raise ValueError("非空文本需要非空频率模型")

    interval_by_symbol = {symbol: (symbol_low, symbol_high) for symbol, symbol_low, symbol_high in intervals}
    low, high = Fraction(0, 1), Fraction(1, 1)
    for symbol in text:
        if symbol not in interval_by_symbol:
            raise ValueError("频率模型缺少待编码符号")
        symbol_low, symbol_high = interval_by_symbol[symbol]
        width = high - low
        # 必须使用旧宽度同时更新两端，才能保持子区间与父区间的仿射对应关系。
        new_low = low + width * symbol_low
        high = low + width * symbol_high
        low = new_low
    return (low + high) / 2


def arithmetic_decode(tag: Fraction, model: FrequencyModel, symbol_count: int) -> str:
    """根据算术编码标签、静态模型和长度恢复原文本。

    参数：tag 为编码区间内标签；model 为静态频率模型；symbol_count 为原始字符数量。
    返回值：长度恰为 symbol_count 的解码字符串。
    边界情况：长度为零时只接受空模型和标签 0；标签越界或长度非法时抛出 ValueError。
    关键算法点：将标签相对当前区间归一化到 [0, 1)，即可定位下一字符的累计概率区间。
    """
    if isinstance(symbol_count, bool) or not isinstance(symbol_count, int) or symbol_count < 0:
        raise ValueError("symbol_count 必须是非负整数")
    if not isinstance(tag, Fraction) or not Fraction(0, 1) <= tag < Fraction(1, 1):
        raise ValueError("tag 必须是 [0, 1) 内的 Fraction")
    intervals, _ = _validated_intervals(model)
    if symbol_count == 0:
        if model or tag != 0:
            raise ValueError("空消息必须使用空模型和标签 0")
        return ""
    if not intervals:
        raise ValueError("非空消息需要非空频率模型")

    low, high = Fraction(0, 1), Fraction(1, 1)
    decoded: list[str] = []
    for _ in range(symbol_count):
        normalized = (tag - low) / (high - low)
        for symbol, symbol_low, symbol_high in intervals:
            if symbol_low <= normalized < symbol_high:
                width = high - low
                new_low = low + width * symbol_low
                high = low + width * symbol_high
                low = new_low
                decoded.append(symbol)
                break
        else:
            raise ValueError("tag 不属于模型定义的任何符号区间")
    return "".join(decoded)


if __name__ == "__main__":
    sample = "BANANA"
    sample_model = build_frequency_model(sample)
    sample_tag = arithmetic_encode(sample, sample_model)
    assert arithmetic_decode(sample_tag, sample_model, len(sample)) == sample
    assert build_frequency_model("") == {}
    assert arithmetic_encode("", {}) == Fraction(0, 1)
    assert arithmetic_decode(Fraction(0, 1), {}, 0) == ""
    try:
        arithmetic_decode(Fraction(1, 1), sample_model, len(sample))
        raise AssertionError("上边界标签应当抛出 ValueError")
    except ValueError:
        pass

    print("004_arithmetic_coding: all examples passed")
