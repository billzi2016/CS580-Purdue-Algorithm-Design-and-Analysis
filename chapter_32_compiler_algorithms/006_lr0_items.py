"""构造增广上下文无关文法的 LR(0) 规范项目集族。

适用场景：LR、SLR 和 LR(1) 分析器的共同基础，展示移进/归约自动机的状态如何从项目集得到。
核心思想：``closure`` 为点后非终结符加入全部候选产生式；``goto`` 将点越过一个符号后再次闭包。
输入输出：输入产生式字典和开始符号，输出增广文法、初始状态与项目集状态转移图。
时间复杂度：最坏状态数指数增长；单次 closure 为 O(P²) 量级，P 为产生式数。
空间复杂度：最坏由规范项目集数决定，可能为指数级。
边界情况：空右侧产生式产生归约项目；开始符号会使用保证不冲突的新增广名称；文法符号不能为空。
"""

from __future__ import annotations

from dataclasses import dataclass


Production = tuple[str, tuple[str, ...]]
Item = tuple[str, tuple[str, ...], int]
Grammar = dict[str, list[list[str]]]


@dataclass
class LR0Automaton:
    """LR(0) 项目集自动机，状态编号仅用于展示和后续分析表构造。"""

    augmented_start: str
    states: list[frozenset[Item]]
    transitions: dict[tuple[int, str], int]


def closure(items: set[Item], grammar: Grammar) -> frozenset[Item]:
    """计算 LR(0) 项目集闭包。

    参数：``items`` 是初始项目集合，``grammar`` 是产生式字典。
    返回值：包含所有由点后非终结符强制引入项目的不可变集合。
    边界情况：归约项目的点已在末尾，不再引入任何项目；右侧为空也自然成为归约项目。
    关键点：若 ``A → α·Bβ``，则必须加入每条 ``B → γ`` 的 ``B → ·γ``。
    """
    result = set(items)
    pending = list(items)
    nonterminals = set(grammar)
    while pending:
        left_side, right_side, dot = pending.pop()
        if dot == len(right_side):
            continue
        next_symbol = right_side[dot]
        if next_symbol not in nonterminals:
            continue
        for candidate in grammar[next_symbol]:
            new_item = (next_symbol, tuple(candidate), 0)
            if new_item not in result:
                result.add(new_item)
                pending.append(new_item)
    return frozenset(result)


def goto(items: frozenset[Item], symbol: str, grammar: Grammar) -> frozenset[Item]:
    """计算项目集经一个文法符号的 GOTO 转移。

    参数：``items`` 为源项目集，``symbol`` 为待越过的点后符号，``grammar`` 为产生式。
    返回值：越过该符号并取闭包后的项目集；没有可越过项目时返回空集合。
    边界情况：归约项目不会参与移动；空集合保持为空。
    关键点：先移动点，再取 closure，确保新点后的非终结符展开完整。
    """
    advanced = {
        (left_side, right_side, dot + 1)
        for left_side, right_side, dot in items
        if dot < len(right_side) and right_side[dot] == symbol
    }
    if not advanced:
        return frozenset()
    return closure(advanced, grammar)


def build_lr0_automaton(grammar: Grammar, start_symbol: str) -> LR0Automaton:
    """构造增广文法的 LR(0) 规范项目集族。

    参数：``grammar`` 用列表右侧表示产生式，``start_symbol`` 为原文法开始符号。
    返回值：包含全部项目集状态及符号转移的 ``LR0Automaton``。
    边界情况：原文法可含空产生式；新增开始符不会覆盖已有非终结符。
    关键点：每发现一个未见的 GOTO 非空项目集，就将它加入工作表继续扩展。
    """
    _validate_grammar(grammar, start_symbol)
    augmented_start = _fresh_augmented_start(set(grammar))
    augmented_grammar = {augmented_start: [[start_symbol]], **grammar}
    initial = closure({(augmented_start, (start_symbol,), 0)}, augmented_grammar)
    states = [initial]
    state_numbers = {initial: 0}
    pending = [initial]
    transitions: dict[tuple[int, str], int] = {}

    while pending:
        source = pending.pop(0)
        source_number = state_numbers[source]
        symbols = {
            right_side[dot] for _, right_side, dot in source if dot < len(right_side)
        }
        for symbol in symbols:
            target = goto(source, symbol, augmented_grammar)
            if target not in state_numbers:
                state_numbers[target] = len(states)
                states.append(target)
                pending.append(target)
            transitions[(source_number, symbol)] = state_numbers[target]

    return LR0Automaton(augmented_start, states, transitions)


def format_item(item: Item) -> str:
    """将项目渲染为含 ``·`` 的可读字符串，便于教学输出与断言检查。

    参数：``item`` 是 ``(左侧, 右侧元组, 点位置)``。
    返回值：如 ``E -> E · + T`` 的字符串。
    边界情况：空右侧显示为单独的点；点在末尾显示归约位置。
    关键点：点位置把右侧切成已识别前缀与尚待识别后缀。
    """
    left_side, right_side, dot = item
    rendered = list(right_side)
    rendered.insert(dot, "·")
    return f"{left_side} -> {' '.join(rendered)}"


def _fresh_augmented_start(nonterminals: set[str]) -> str:
    candidate = "S'"
    while candidate in nonterminals:
        candidate += "'"
    return candidate


def _validate_grammar(grammar: Grammar, start_symbol: str) -> None:
    if start_symbol not in grammar:
        raise ValueError("开始符号必须是文法中的非终结符")
    if any(not isinstance(symbol, str) or not symbol for symbol in grammar):
        raise ValueError("非终结符必须是非空字符串")
    for alternatives in grammar.values():
        if not isinstance(alternatives, list):
            raise ValueError("产生式集合必须是列表")
        for right_side in alternatives:
            if not isinstance(right_side, list) or any(
                not symbol for symbol in right_side
            ):
                raise ValueError("产生式右侧必须是符号列表")


if __name__ == "__main__":
    grammar = {
        "S": [["C", "C"]],
        "C": [["c", "C"], ["d"]],
    }
    automaton = build_lr0_automaton(grammar, "S")
    initial_text = {format_item(item) for item in automaton.states[0]}
    assert "S' -> · S" in initial_text
    assert "S -> · C C" in initial_text
    assert "C -> · c C" in initial_text
    assert "C -> · d" in initial_text
    assert (0, "S") in automaton.transitions
    assert len(automaton.states) == 7

    epsilon_grammar = {"A": [[]]}
    epsilon_automaton = build_lr0_automaton(epsilon_grammar, "A")
    assert "A -> ·" in {format_item(item) for item in epsilon_automaton.states[0]}
    assert len(epsilon_automaton.states) == 2

    print("006_lr0_items: all examples passed")
