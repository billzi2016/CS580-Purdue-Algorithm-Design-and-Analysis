"""中心星形渐进多序列比对教学实现。

适用场景：对少量短 DNA 序列逐一与固定中心序列全局比对，并将各次产生的缺口合并为同一个 MSA 列结构。
核心思想：先对中心与下一序列做 Needleman-Wunsch；再同步扫描旧中心行和新中心行，把新 gap 传播到所有已有行。
输入输出：输入至少一条 DNA 序列，输出所有等长的对齐行，顺序与输入一致。
时间复杂度：设中心长 L、其余序列总长 S，约 O(LS)；空间复杂度为最终 MSA 大小。
关键边界情况：空序列合法；本教学版以第一条为固定中心、不建 guide tree、不迭代 refinement，不能替代工业级 MSA。
"""

DNA = frozenset("ACGTN")


def progressive_msa(sequences: list[str], match: int = 1, mismatch: int = -1, gap: int = -1) -> list[str]:
    """以第一条为中心构造星形渐进 MSA。

    参数：sequences 是至少一条大写 DNA；其余参数为统一全局比对评分。
    返回：与输入同序、等长的对齐字符串列表。
    边界情况：空列表抛出 ValueError，空序列合法；非法 DNA 抛出 ValueError。
    关键算法点：每一步只比对原始中心字符序列，随后将其 gap 模式合并进当前已对齐中心行。
    """
    if not sequences:
        raise ValueError("至少需要一条序列")
    for sequence in sequences:
        if any(symbol not in DNA for symbol in sequence):
            raise ValueError("序列只能包含大写 A、C、G、T 或 N")
    center = sequences[0]
    alignment = [center]
    for sequence in sequences[1:]:
        new_center, new_sequence = _global_align(center, sequence, match, mismatch, gap)
        alignment = _merge_center_alignment(alignment, new_center, new_sequence)
    return alignment


def _global_align(first: str, second: str, match: int, mismatch: int, gap: int) -> tuple[str, str]:
    """手写两行回溯所需完整 DP，返回一组全局对齐。"""
    dp = [[0] * (len(second) + 1) for _ in range(len(first) + 1)]
    for i in range(1, len(first) + 1): dp[i][0] = dp[i-1][0] + gap
    for j in range(1, len(second) + 1): dp[0][j] = dp[0][j-1] + gap
    for i in range(1, len(first) + 1):
        for j in range(1, len(second) + 1):
            dp[i][j] = max(dp[i-1][j-1] + (match if first[i-1] == second[j-1] else mismatch), dp[i-1][j] + gap, dp[i][j-1] + gap)
    left: list[str] = []; right: list[str] = []; i, j = len(first), len(second)
    while i or j:
        if i and j and dp[i][j] == dp[i-1][j-1] + (match if first[i-1] == second[j-1] else mismatch):
            left.append(first[i-1]); right.append(second[j-1]); i -= 1; j -= 1
        elif i and dp[i][j] == dp[i-1][j] + gap:
            left.append(first[i-1]); right.append("-"); i -= 1
        else:
            left.append("-"); right.append(second[j-1]); j -= 1
    return "".join(reversed(left)), "".join(reversed(right))


def _merge_center_alignment(existing: list[str], fresh_center: str, fresh_sequence: str) -> list[str]:
    """将 fresh_center 的新 gap 插入所有已有行，并附加新序列。

    旧中心行的 gap 对应先前加入序列的共享列；新中心的 gap 对应本轮才引入、必须补入旧行的新列。
    """
    old_center = existing[0]; rebuilt = ["" for _ in existing]; new_row: list[str] = []
    old_index = fresh_index = 0
    while old_index < len(old_center) or fresh_index < len(fresh_center):
        old_symbol = old_center[old_index] if old_index < len(old_center) else None
        fresh_symbol = fresh_center[fresh_index] if fresh_index < len(fresh_center) else None
        if fresh_symbol == "-":
            rebuilt = [row + "-" for row in rebuilt]; new_row.append(fresh_sequence[fresh_index]); fresh_index += 1
        elif old_symbol == "-":
            for index, row in enumerate(existing): rebuilt[index] += row[old_index]
            new_row.append("-"); old_index += 1
        else:
            # 两行此处均消费同一个原始中心字符；不相等说明 merge 不变量被破坏。
            if old_symbol != fresh_symbol: raise ValueError("中心序列合并不变量被破坏")
            for index, row in enumerate(existing): rebuilt[index] += row[old_index]
            new_row.append(fresh_sequence[fresh_index]); old_index += 1; fresh_index += 1
    return rebuilt + ["".join(new_row)]


if __name__ == "__main__":
    rows = progressive_msa(["ACGT", "AGT", "ACCT"])
    assert len(rows) == 3 and len({len(row) for row in rows}) == 1
    assert [row.replace("-", "") for row in rows] == ["ACGT", "AGT", "ACCT"]
    assert progressive_msa(["", "AC"]) == ["--", "AC"]
    try:
        progressive_msa([]); raise AssertionError("应拒绝空列表")
    except ValueError: pass
    print("024_progressive_msa: all examples passed")
