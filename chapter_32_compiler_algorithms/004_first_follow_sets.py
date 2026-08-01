"""计算上下文无关文法的 FIRST 集与 FOLLOW 集。

适用场景：预测分析、LL(1) 分析表构造，以及理解空串如何影响自顶向下解析。
核心思想：不断把产生式右侧可推出的首终结符加入 FIRST；再从产生式局部约束传播 FOLLOW。
输入输出：产生式用 ``{非终结符: [[符号, ...], ...]}`` 表示，输出两个符号到集合的映射。
时间复杂度：设产生式总右侧长度为 P，迭代式实现最坏 O(P × V²)；空间复杂度 O(V²)。
边界情况：空产生式以空列表表示；不在产生式左侧的符号会被当作终结符；开始符 FOLLOW 含 ``$``。
"""

from __future__ import annotations


EPSILON = "ε"
END_MARKER = "$"
Grammar = dict[str, list[list[str]]]


def first_of_sequence(
    sequence: list[str], first_sets: dict[str, set[str]], nonterminals: set[str]
) -> set[str]:
    """计算符号串的 FIRST 集。

    参数：``sequence`` 是产生式右侧，``first_sets`` 是当前或已稳定的非终结符 FIRST 集。
    返回值：该序列可作为首符号出现的终结符，必要时包含 ``ε``。
    边界情况：空序列的 FIRST 为 ``{ε}``；终结符自身构成单元素 FIRST 集。
    关键点：只有当前一个符号可推出 ε 时，才能继续查看下一个符号。
    """
    if not sequence:
        return {EPSILON}

    result: set[str] = set()
    for symbol in sequence:
        symbol_first = first_sets[symbol] if symbol in nonterminals else {symbol}
        result.update(symbol_first - {EPSILON})
        if EPSILON not in symbol_first:
            return result

    result.add(EPSILON)
    return result


def compute_first_sets(grammar: Grammar) -> dict[str, set[str]]:
    """计算每个非终结符的 FIRST 集。

    参数：``grammar`` 的键为非终结符，值为其候选产生式右侧列表。
    返回值：每个非终结符对应的稳定 FIRST 集。
    边界情况：空产生式会把 ``ε`` 加入左侧的 FIRST 集；空文法返回空映射。
    关键点：集合只会增长，因此在一轮没有新增元素时到达不动点。
    """
    _validate_grammar(grammar)
    nonterminals = set(grammar)
    first_sets = {nonterminal: set() for nonterminal in nonterminals}

    changed = True
    while changed:
        changed = False
        for left_side, alternatives in grammar.items():
            for right_side in alternatives:
                additions = first_of_sequence(right_side, first_sets, nonterminals)
                previous_size = len(first_sets[left_side])
                first_sets[left_side].update(additions)
                changed = changed or len(first_sets[left_side]) != previous_size
    return first_sets


def compute_follow_sets(
    grammar: Grammar, start_symbol: str, first_sets: dict[str, set[str]] | None = None
) -> dict[str, set[str]]:
    """计算每个非终结符的 FOLLOW 集。

    参数：文法 ``grammar``、开始符号 ``start_symbol``，以及可选的预计算 FIRST 集。
    返回值：每个非终结符后面可紧跟的终结符集合；开始符总含 ``$``。
    边界情况：右侧末尾的非终结符继承左侧 FOLLOW；可空后缀也会触发该继承。
    关键点：对 ``A → αBβ``，先加入 FIRST(β)-{ε}，若 β 可空再加入 FOLLOW(A)。
    """
    _validate_grammar(grammar)
    if start_symbol not in grammar:
        raise ValueError("开始符号必须是文法中的非终结符")

    nonterminals = set(grammar)
    if first_sets is None:
        first_sets = compute_first_sets(grammar)
    if set(first_sets) != nonterminals:
        raise ValueError("FIRST 集必须恰好覆盖全部非终结符")

    follow_sets = {nonterminal: set() for nonterminal in nonterminals}
    follow_sets[start_symbol].add(END_MARKER)

    changed = True
    while changed:
        changed = False
        for left_side, alternatives in grammar.items():
            for right_side in alternatives:
                for index, symbol in enumerate(right_side):
                    if symbol not in nonterminals:
                        continue

                    suffix_first = first_of_sequence(
                        right_side[index + 1 :], first_sets, nonterminals
                    )
                    before = len(follow_sets[symbol])
                    follow_sets[symbol].update(suffix_first - {EPSILON})
                    if EPSILON in suffix_first:
                        follow_sets[symbol].update(follow_sets[left_side])
                    changed = changed or len(follow_sets[symbol]) != before
    return follow_sets


def _validate_grammar(grammar: Grammar) -> None:
    """验证教学用文法的基础表示，避免把 ε 当成普通符号混入右侧。"""
    if not isinstance(grammar, dict):
        raise TypeError("文法必须是字典")
    for left_side, alternatives in grammar.items():
        if not isinstance(left_side, str) or not left_side:
            raise ValueError("非终结符必须是非空字符串")
        if not isinstance(alternatives, list):
            raise ValueError("每个非终结符的产生式必须是列表")
        for right_side in alternatives:
            if not isinstance(right_side, list) or any(
                not isinstance(symbol, str) or not symbol for symbol in right_side
            ):
                raise ValueError("产生式右侧必须是字符串列表")
            if EPSILON in right_side:
                raise ValueError("请用空列表表示 ε 产生式，不要把 ε 写入右侧")


if __name__ == "__main__":
    expression_grammar = {
        "E": [["T", "E'"]],
        "E'": [["+", "T", "E'"], []],
        "T": [["id"]],
    }
    first = compute_first_sets(expression_grammar)
    follow = compute_follow_sets(expression_grammar, "E", first)
    assert first["E"] == {"id"}
    assert first["E'"] == {"+", EPSILON}
    assert follow["E"] == {END_MARKER}
    assert follow["T"] == {"+", END_MARKER}

    nullable_grammar = {"S": [["A", "b"]], "A": [[], ["a"]]}
    nullable_first = compute_first_sets(nullable_grammar)
    nullable_follow = compute_follow_sets(nullable_grammar, "S", nullable_first)
    assert nullable_first["A"] == {EPSILON, "a"}
    assert nullable_first["S"] == {"a", "b"}
    assert nullable_follow["A"] == {"b"}

    print("004_first_follow_sets: all examples passed")
