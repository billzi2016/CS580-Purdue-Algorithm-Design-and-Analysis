"""从上下文无关文法构造 SLR(1) 分析表，并执行移进归约分析。

适用场景：编译原理中把 LR(0) 项目集与 FOLLOW 集结合为简单 LR 分析器。
核心思想：点后终结符产生 shift，完成项目按左侧 FOLLOW 产生 reduce，增广完成项目产生 accept。
输入输出：产生式字典与 token 序列，输出 SLR 表或该 token 序列是否被接受。
时间复杂度：建表最坏受 LR(0) 状态数指数增长支配；分析单次为 O(输入长度加归约次数)。
空间复杂度：最坏为项目集、ACTION/GOTO 表所占的指数级空间。
边界情况：空产生式可归约；冲突立即报告；这是 SLR(1) 教学实现，不含语义动作和错误恢复。
"""

from __future__ import annotations

from dataclasses import dataclass


END = "$"
Item = tuple[str, tuple[str, ...], int]
Grammar = dict[str, list[list[str]]]


class SLRConflictError(ValueError):
    """表示 ACTION 或 GOTO 单元出现不兼容项目，因此文法不是 SLR(1)。"""


@dataclass
class SLRTable:
    """SLR 分析表；ACTION 值为 ``shift N``、``reduce (A, rhs)`` 或 ``accept``。"""

    action: dict[tuple[int, str], tuple[str, int | tuple[str, tuple[str, ...]] | None]]
    goto: dict[tuple[int, str], int]
    start_symbol: str


def build_slr_table(grammar: Grammar, start_symbol: str) -> SLRTable:
    """从文法构造 SLR ACTION/GOTO 表。

    参数：``grammar`` 的空列表右侧代表 ε，``start_symbol`` 为原文法开始符号。
    返回值：可供 ``slr_parse`` 使用的 SLR 表。
    边界情况：空产生式生成长度为零的归约；任何移进/归约或归约/归约冲突均抛异常。
    关键点：归约只填入 FOLLOW(A)，这正是 SLR 相对 LR(0) 的向前看限制。
    """
    _validate(grammar, start_symbol)
    augmented_start = _fresh_start(set(grammar))
    augmented = {augmented_start: [[start_symbol]], **grammar}
    nonterminals = set(augmented)
    terminals = _terminals(augmented, nonterminals)
    states, transitions = _canonical_collection(augmented, augmented_start)
    follow = _follow_sets(grammar, start_symbol)
    action: dict[
        tuple[int, str], tuple[str, int | tuple[str, tuple[str, ...]] | None]
    ] = {}
    goto_table: dict[tuple[int, str], int] = {}

    for number, state in enumerate(states):
        for left, right, dot in state:
            if dot < len(right):
                symbol = right[dot]
                target = transitions[(number, symbol)]
                if symbol in terminals:
                    _place_action(action, (number, symbol), ("shift", target))
                else:
                    goto_table[(number, symbol)] = target
                continue
            if left == augmented_start:
                _place_action(action, (number, END), ("accept", None))
            else:
                reduction = (left, right)
                for lookahead in follow[left]:
                    _place_action(action, (number, lookahead), ("reduce", reduction))
    return SLRTable(action, goto_table, start_symbol)


def slr_parse(table: SLRTable, tokens: list[str]) -> bool:
    """按 SLR 表识别 token 序列。

    参数：``table`` 为建表结果，``tokens`` 为不含结束符的终结符列表。
    返回值：是否到达 accept 动作。
    边界情况：表中没有动作、输入自带 ``$`` 或 GOTO 缺失时返回 ``False``。
    关键点：归约 A→β 时弹出 |β| 个状态，再由栈顶状态经 GOTO 转到 A。
    """
    if END in tokens:
        return False
    states = [0]
    stream = [*tokens, END]
    position = 0
    while True:
        action = table.action.get((states[-1], stream[position]))
        if action is None:
            return False
        kind, payload = action
        if kind == "shift":
            states.append(int(payload))
            position += 1
        elif kind == "reduce":
            left, right = payload  # type: ignore[misc]
            if right:
                del states[-len(right) :]
            target = table.goto.get((states[-1], left))
            if target is None:
                return False
            states.append(target)
        else:
            return kind == "accept" and stream[position] == END


def _canonical_collection(grammar: Grammar, augmented_start: str) -> tuple[list[frozenset[Item]], dict[tuple[int, str], int]]:
    initial = _closure({(augmented_start, (grammar[augmented_start][0][0],), 0)}, grammar)
    states = [initial]
    numbers = {initial: 0}
    pending = [initial]
    transitions: dict[tuple[int, str], int] = {}
    while pending:
        source = pending.pop(0)
        source_number = numbers[source]
        symbols = {right[dot] for _, right, dot in source if dot < len(right)}
        for symbol in symbols:
            target = _goto(source, symbol, grammar)
            if target not in numbers:
                numbers[target] = len(states)
                states.append(target)
                pending.append(target)
            transitions[(source_number, symbol)] = numbers[target]
    return states, transitions


def _closure(items: set[Item], grammar: Grammar) -> frozenset[Item]:
    result, pending = set(items), list(items)
    while pending:
        _, right, dot = pending.pop()
        if dot == len(right) or right[dot] not in grammar:
            continue
        nonterminal = right[dot]
        for production in grammar[nonterminal]:
            item = (nonterminal, tuple(production), 0)
            if item not in result:
                result.add(item)
                pending.append(item)
    return frozenset(result)


def _goto(items: frozenset[Item], symbol: str, grammar: Grammar) -> frozenset[Item]:
    advanced = {(left, right, dot + 1) for left, right, dot in items if dot < len(right) and right[dot] == symbol}
    return _closure(advanced, grammar) if advanced else frozenset()


def _follow_sets(grammar: Grammar, start: str) -> dict[str, set[str]]:
    nonterminals = set(grammar)
    first = {name: set() for name in nonterminals}
    changed = True
    while changed:
        changed = False
        for left, alternatives in grammar.items():
            for right in alternatives:
                additions = _first_of(right, first, nonterminals)
                previous = len(first[left])
                first[left].update(additions)
                changed = changed or len(first[left]) != previous
    follow = {name: set() for name in nonterminals}
    follow[start].add(END)
    changed = True
    while changed:
        changed = False
        for left, alternatives in grammar.items():
            for right in alternatives:
                for index, symbol in enumerate(right):
                    if symbol not in nonterminals:
                        continue
                    suffix = _first_of(right[index + 1 :], first, nonterminals)
                    previous = len(follow[symbol])
                    follow[symbol].update(suffix - {"ε"})
                    if "ε" in suffix:
                        follow[symbol].update(follow[left])
                    changed = changed or len(follow[symbol]) != previous
    return follow


def _first_of(sequence: list[str], first: dict[str, set[str]], nonterminals: set[str]) -> set[str]:
    if not sequence:
        return {"ε"}
    result: set[str] = set()
    for symbol in sequence:
        current = first[symbol] if symbol in nonterminals else {symbol}
        result.update(current - {"ε"})
        if "ε" not in current:
            return result
    return result | {"ε"}


def _place_action(action: dict, key: tuple[int, str], value: tuple) -> None:
    previous = action.get(key)
    if previous is not None and previous != value:
        raise SLRConflictError(f"SLR 冲突：状态 {key[0]}，符号 {key[1]!r}，{previous} 与 {value}")
    action[key] = value


def _terminals(grammar: Grammar, nonterminals: set[str]) -> set[str]:
    return {symbol for alternatives in grammar.values() for right in alternatives for symbol in right if symbol not in nonterminals}


def _fresh_start(nonterminals: set[str]) -> str:
    candidate = "S'"
    while candidate in nonterminals:
        candidate += "'"
    return candidate


def _validate(grammar: Grammar, start: str) -> None:
    if start not in grammar:
        raise ValueError("开始符号必须存在于文法中")
    if any(not isinstance(right, list) for alternatives in grammar.values() for right in alternatives):
        raise ValueError("产生式右侧必须是列表")


if __name__ == "__main__":
    sample_grammar = {"S": [["C", "C"]], "C": [["c", "C"], ["d"]]}
    sample_table = build_slr_table(sample_grammar, "S")
    assert slr_parse(sample_table, ["c", "d", "d"])
    assert slr_parse(sample_table, ["d", "d"])
    assert not slr_parse(sample_table, ["c", "d"])
    assert not slr_parse(sample_table, ["d", "c"])
    print("007_slr_parsing: all examples passed")
