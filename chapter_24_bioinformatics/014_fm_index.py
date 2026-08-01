"""教学版 FM-index 精确模式计数与定位。

适用场景：在短 DNA 或一般文本中多次查询精确模式，展示 BWT、C 表与 Occ 表支持的后向搜索。
核心思想：维护 BWT 首列的字符起点 C 和每个前缀的累积计数 Occ；从模式末尾迭代收缩后缀数组区间。
输入输出：以原文本构造索引；count 返回出现次数，locate 返回升序文本起点。
时间复杂度：构建 O(n² log n)（教学版显式 BWT）和 O(n|Σ|)；查询 O(m)，定位另加 O(k log k)。
关键边界情况：空模式匹配 n+1 个边界；文本和模式可为任意字符但终止符不得出现；本版不做压缩或采样定位。
"""

from dataclasses import dataclass


TERMINATOR = "$"


@dataclass(frozen=True)
class FMIndex:
    """保存教学版 FM-index 的 BWT、首列起点、Occ 表及完整后缀数组。"""

    text: str
    bwt: str
    first_occurrence: dict[str, int]
    occurrences: dict[str, list[int]]
    suffix_array: list[int]
    terminator: str

    @classmethod
    def build(cls, text: str, terminator: str = TERMINATOR) -> "FMIndex":
        """从文本手写构建完整 FM-index 辅助结构。

        参数：text 为待索引文本；terminator 是未出现的单字符终止符。
        返回：可用于 count 和 locate 的不可变索引。
        边界情况：空文本合法；终止符冲突抛出 ValueError。
        关键算法点：后缀数组排序决定 BWT 行序，Occ[symbol][end] 表示 bwt[:end] 内的出现次数。
        """
        if len(terminator) != 1 or terminator in text:
            raise ValueError("终止符必须为一个未出现在文本中的字符")
        extended = text + terminator
        suffix_array = list(range(len(extended)))
        suffix_array.sort(key=lambda start: extended[start:])
        bwt = "".join(extended[start - 1] if start else extended[-1] for start in suffix_array)
        alphabet = sorted(set(extended))
        first_column = sorted(bwt)
        first_occurrence: dict[str, int] = {}
        for index, symbol in enumerate(first_column):
            first_occurrence.setdefault(symbol, index)
        occurrences: dict[str, list[int]] = {symbol: [0] * (len(bwt) + 1) for symbol in alphabet}
        for end, observed in enumerate(bwt, start=1):
            for symbol in alphabet:
                occurrences[symbol][end] = occurrences[symbol][end - 1] + (symbol == observed)
        return cls(text, bwt, first_occurrence, occurrences, suffix_array, terminator)

    def count(self, pattern: str) -> int:
        """返回 pattern 在原文本中可重叠出现的次数。

        参数：pattern 是不含终止符的查询串。
        返回：匹配数量；空模式按字符串约定匹配 len(text)+1 个边界。
        边界情况：含终止符的模式抛出 ValueError；索引字母表外字符返回零。
        关键算法点：区间 [left, right) 始终恰好对应当前已处理模式后缀的所有后缀数组行。
        """
        left, right = self._interval(pattern)
        return right - left

    def locate(self, pattern: str) -> list[int]:
        """返回 pattern 的所有起点，按文本下标升序排列。

        参数：pattern 是不含终止符的查询串。
        返回：所有可重叠匹配的 0-based 起点；空模式返回全部边界。
        边界情况：没有匹配时返回空列表；不返回只属于附加终止符的行。
        关键算法点：教学版保留完整后缀数组，因此可直接将最终行区间映射回起点。
        """
        left, right = self._interval(pattern)
        positions = [start for start in self.suffix_array[left:right] if start <= len(self.text) - len(pattern)]
        return sorted(positions)

    def last_to_first(self, row: int) -> int:
        """返回 BWT 最后一列某行经 LF 映射到第一列后的行号。

        参数：row 是 BWT 中从零开始的有效行号。
        返回：同一循环文本旋转在排序首列中的行号。
        边界情况：行号越界抛出 IndexError。
        关键算法点：C 给出字符块的首行，Occ 给出该字符在当前行之前的出现次数；两者共同确定稳定排序后的对应项。
        """
        if row < 0 or row >= len(self.bwt):
            raise IndexError("BWT 行号越界")
        symbol = self.bwt[row]
        return self.first_occurrence[symbol] + self.occurrences[symbol][row]

    def reconstruct_text(self) -> str:
        """只利用 BWT 辅助表恢复原文本，用于验证 LF 映射的不变量。

        参数：无。
        返回：构建索引时的原文本，不含终止符。
        边界情况：空文本返回空字符串；终止符行从 BWT 中唯一确定。
        关键算法点：从终止符所在的最后列行反复执行 LF，每一步恰好向原文本左侧恢复一个字符。
        """
        row = self.bwt.index(self.terminator)
        recovered: list[str] = []
        # 终止符行表示原文本的开始；每次 LF 后读取的末列字符是其前驱字符。
        for _ in range(len(self.text)):
            row = self.last_to_first(row)
            recovered.append(self.bwt[row])
        return "".join(reversed(recovered))

    def _interval(self, pattern: str) -> tuple[int, int]:
        """执行后向搜索并返回匹配行区间；这是 count 与 locate 的共享核心。"""
        if self.terminator in pattern:
            raise ValueError("查询模式不得包含终止符")
        if not pattern:
            return 0, len(self.text) + 1
        left, right = 0, len(self.bwt)
        for symbol in reversed(pattern):
            if symbol not in self.first_occurrence:
                return 0, 0
            left = self.first_occurrence[symbol] + self.occurrences[symbol][left]
            right = self.first_occurrence[symbol] + self.occurrences[symbol][right]
            if left == right:
                return 0, 0
        return left, right


if __name__ == "__main__":
    index = FMIndex.build("banana")
    assert index.bwt == "annb$aa"
    assert index.count("ana") == 2
    assert index.locate("ana") == [1, 3]
    assert index.count("xyz") == 0
    assert index.locate("") == list(range(7))
    assert index.reconstruct_text() == "banana"
    assert index.last_to_first(index.bwt.index("$")) == 0
    assert FMIndex.build("").locate("") == [0]
    print("014_fm_index: all examples passed")
