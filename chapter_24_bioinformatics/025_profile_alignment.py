"""序列到 profile 的全局比对教学实现。

适用场景：把一条短 DNA 序列加入已有等长 MSA；profile 的每列由已有字符频数表示。
核心思想：DP 的对角转移以新字符与整列每个非 gap 字符的累计 match/mismatch 评分，插入列则对整列收 gap 罚分。
输入输出：输入等长 profile 行及 sequence，返回加入新行后的等长 MSA 和总分。
时间复杂度 O(PL)，P 为 profile 行数、L 为列数、S 为序列长度；空间复杂度 O(LS)。
关键边界情况：profile 不能为空且必须等长；空 sequence 合法；本教学版不实现权重、HMM 或 affine gap。
"""

from dataclasses import dataclass

DNA = frozenset("ACGTN")


@dataclass(frozen=True)
class ProfileAlignment:
    """包含旧 profile 与新序列的等长对齐以及累计评分。"""
    rows: tuple[str, ...]
    score: int


def align_sequence_to_profile(profile: list[str], sequence: str, match: int = 1, mismatch: int = -1, gap: int = -1) -> ProfileAlignment:
    """将 sequence 全局对齐到已有 profile。

    参数：profile 是等长 DNA/gap 行，sequence 是无 gap DNA。
    返回：原 profile 经必要插列后的行及新增 sequence 行。
    边界情况：空 sequence 合法；profile 空、长度不齐或非法字符抛出 ValueError。
    关键算法点：删除 profile 列时新序列写 gap；插入 sequence 字符时必须向所有旧行同步插 gap 列。
    """
    _validate(profile, sequence)
    columns, length = len(profile[0]), len(sequence)
    dp = [[0] * (length + 1) for _ in range(columns + 1)]
    for i in range(1, columns + 1): dp[i][0] = dp[i-1][0] + gap * len(profile)
    for j in range(1, length + 1): dp[0][j] = dp[0][j-1] + gap * len(profile)
    for i in range(1, columns + 1):
        for j in range(1, length + 1):
            diagonal = dp[i-1][j-1] + _column_score(profile, i-1, sequence[j-1], match, mismatch, gap)
            dp[i][j] = max(diagonal, dp[i-1][j] + gap * len(profile), dp[i][j-1] + gap * len(profile))
    rebuilt = ["" for _ in profile]; added: list[str] = []; i, j = columns, length
    while i or j:
        if i and j and dp[i][j] == dp[i-1][j-1] + _column_score(profile, i-1, sequence[j-1], match, mismatch, gap):
            for r, row in enumerate(profile): rebuilt[r] += row[i-1]
            added.append(sequence[j-1]); i -= 1; j -= 1
        elif i and dp[i][j] == dp[i-1][j] + gap * len(profile):
            for r, row in enumerate(profile): rebuilt[r] += row[i-1]
            added.append("-"); i -= 1
        else:
            for r in range(len(profile)): rebuilt[r] += "-"
            added.append(sequence[j-1]); j -= 1
    return ProfileAlignment(tuple(row[::-1] for row in rebuilt) + ("".join(reversed(added)),), dp[-1][-1])


def _column_score(profile: list[str], column: int, symbol: str, match: int, mismatch: int, gap: int) -> int:
    """计算一个新字符同 profile 列全部行的累计评分，已有 gap 按 gap 罚分。"""
    return sum(gap if row[column] == "-" else (match if row[column] == symbol else mismatch) for row in profile)


def _validate(profile: list[str], sequence: str) -> None:
    """验证 profile 等长并限制字符范围。"""
    if not profile or len({len(row) for row in profile}) != 1: raise ValueError("profile 必须非空且所有行等长")
    if any(c not in DNA | {"-"} for row in profile for c in row) or any(c not in DNA for c in sequence): raise ValueError("profile 只含 DNA/gap，序列只含 DNA")


if __name__ == "__main__":
    result = align_sequence_to_profile(["ACGT", "A-GT"], "ACCT")
    assert len(set(map(len, result.rows))) == 1
    assert result.rows[-1].replace("-", "") == "ACCT"
    assert result.rows[:2] == ("ACGT", "A-GT")
    assert align_sequence_to_profile(["AC"], "").rows == ("AC", "--")
    try: align_sequence_to_profile(["A", "AA"], "A"); raise AssertionError("应拒绝不等长 profile")
    except ValueError: pass
    print("025_profile_alignment: all examples passed")
