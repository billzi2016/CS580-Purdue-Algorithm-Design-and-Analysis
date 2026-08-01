"""构造 LL(1) 预测分析表并检测文法冲突。

适用场景：为无左递归、已左因子化的上下文无关文法生成表驱动的自顶向下分析器。
核心思想：每条产生式按 FIRST(右侧) 填表；若右侧可推出 ε，再按 FOLLOW(左侧) 填表。
输入输出：输入文法和开始符号，输出 ``(非终结符, 向前看符号) -> 右侧`` 的分析表。
时间复杂度：设产生式总数为 R、符号总数为 V，FIRST/FOLLOW 与填表合计为 O(R × V²) 量级。
空间复杂度：O(R × V)，由集合与分析表占用。
边界情况：空产生式使用空元组储存；同一表格单元需要两条不同产生式时抛出 ``LL1ConflictError``。
"""

from __future__ import annotations


EPSILON = "ε"
END_MARKER = "$"
Grammar = dict[str, list[list[str]]]
ParsingTable = dict[tuple[str, str], tuple[str, ...]]


class LL1ConflictError(ValueError):
    """指出某表格单元存在两个竞争产生式，文法因此不是 LL(1)。"""


def build_ll1_table(grammar: Grammar, start_symbol: str) -> ParsingTable:
    """为文法构造 LL(1) 预测分析表。

    参数：``grammar`` 以字典表示，空右侧代表 ε；``start_symbol`` 是开始非终结符。
    返回值：键为 ``(非终结符, 向前看终结符)`` 的分析表，值为选中的产生式右侧。
    边界情况：可空右侧会向 FOLLOW 中每个符号填入同一产生式；冲突不会被静默覆盖。
    关键点：先使用 FIRST 的非 ε 元素，再在 ε 存在时传播到 FOLLOW。
    """
    _validate_grammar(grammar, start_symbol)
    nonterminals = set(grammar)
    first_sets = _compute_first_sets(grammar, nonterminals)
    follow_sets = _compute_follow_sets(grammar, start_symbol, first_sets, nonterminals)
    table: ParsingTable = {}

    for left_side, alternatives in grammar.items():
        for right_side in alternatives:
            lookaheads = _first_of_sequence(right_side, first_sets, nonterminals)
            targets = lookaheads - {EPSILON}
            if EPSILON in lookaheads:
                targets |= follow_sets[left_side]
            for lookahead in targets:
                _place_production(table, left_side, lookahead, tuple(right_side))
    return table


def predictive_parse(table: ParsingTable, start_symbol: str, tokens: list[str]) -> bool:
    """使用 LL(1) 分析表识别一个终结符序列。

    参数：``table`` 由 ``build_ll1_table`` 返回，``start_symbol`` 为栈底上方符号，``tokens`` 不含 ``$``。
    返回值：输入是否被表中产生式完整推导。
    边界情况：表缺项、终结符不匹配或输入含 ``$`` 时返回 ``False``。
    关键点：栈顶为右侧时须逆序压栈，才能先处理产生式最左符号。
    """
    if END_MARKER in tokens:
        return False
    nonterminals = {left_side for left_side, _ in table}
    stack = [END_MARKER, start_symbol]
    input_stream = [*tokens, END_MARKER]
    position = 0

    while stack:
        top = stack.pop()
        lookahead = input_stream[position]
        if top == END_MARKER:
            return lookahead == END_MARKER
        if top not in nonterminals:
            if top != lookahead:
                return False
            position += 1
            continue

        production = table.get((top, lookahead))
        if production is None:
            return False
        for symbol in reversed(production):
            stack.append(symbol)
    return False


def _compute_first_sets(
    grammar: Grammar, nonterminals: set[str]
) -> dict[str, set[str]]:
    first_sets = {nonterminal: set() for nonterminal in nonterminals}
    changed = True
    while changed:
        changed = False
        for left_side, alternatives in grammar.items():
            for right_side in alternatives:
                old_size = len(first_sets[left_side])
                first_sets[left_side].update(
                    _first_of_sequence(right_side, first_sets, nonterminals)
                )
                changed = changed or len(first_sets[left_side]) != old_size
    return first_sets


def _compute_follow_sets(
    grammar: Grammar,
    start_symbol: str,
    first_sets: dict[str, set[str]],
    nonterminals: set[str],
) -> dict[str, set[str]]:
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
                    suffix_first = _first_of_sequence(
                        right_side[index + 1 :], first_sets, nonterminals
                    )
                    old_size = len(follow_sets[symbol])
                    follow_sets[symbol].update(suffix_first - {EPSILON})
                    if EPSILON in suffix_first:
                        follow_sets[symbol].update(follow_sets[left_side])
                    changed = changed or len(follow_sets[symbol]) != old_size
    return follow_sets


def _first_of_sequence(
    sequence: list[str], first_sets: dict[str, set[str]], nonterminals: set[str]
) -> set[str]:
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


def _place_production(
    table: ParsingTable, left_side: str, lookahead: str, production: tuple[str, ...]
) -> None:
    key = (left_side, lookahead)
    existing = table.get(key)
    if existing is not None and existing != production:
        raise LL1ConflictError(
            f"表项 M[{left_side}, {lookahead}] 同时需要 {existing} 与 {production}"
        )
    table[key] = production


def _validate_grammar(grammar: Grammar, start_symbol: str) -> None:
    if start_symbol not in grammar:
        raise ValueError("开始符号必须是文法中的非终结符")
    for alternatives in grammar.values():
        for right_side in alternatives:
            if EPSILON in right_side:
                raise ValueError("ε 产生式必须写成空列表")


if __name__ == "__main__":
    grammar = {
        "E": [["T", "E'"]],
        "E'": [["+", "T", "E'"], []],
        "T": [["id"]],
    }
    table = build_ll1_table(grammar, "E")
    assert table[("E'", "+")] == ("+", "T", "E'")
    assert table[("E'", END_MARKER)] == ()
    assert predictive_parse(table, "E", ["id", "+", "id"])
    assert predictive_parse(table, "E", ["id"])
    assert not predictive_parse(table, "E", ["+", "id"])
    assert not predictive_parse(table, "E", ["id", "+"])

    try:
        build_ll1_table(
            {
                "S": [
                    ["a", "A"],
                    ["a", "B"],
                ],
                "A": [[]],
                "B": [[]],
            },
            "S",
        )
        raise AssertionError("FIRST/FIRST 冲突必须被检测")
    except LL1ConflictError:
        pass

    print("005_ll1_parsing_table: all examples passed")
