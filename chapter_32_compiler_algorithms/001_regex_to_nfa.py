"""将受限正则表达式转换为 ε-NFA 的 Thompson 构造法。

适用场景：编译原理中讲解词法分析器前端、正则语言与自动机的对应关系。
核心思想：为字面量、连接、并集和 Kleene 闭包分别构造小片段，再用 ε 边把片段组合。
输入输出：输入仅含单字符字面量、``|``、``*``、圆括号及隐式连接的正则表达式；输出 NFA。
时间复杂度：构造过程为 O(n)，其中 n 是表达式长度；模拟匹配为 O(m × (V + E))。
空间复杂度：自动机为 O(n)，一次匹配的状态集合为 O(V)。
边界情况：空表达式匹配空串；空括号、缺失操作数、未闭合括号和 ``.``、反斜杠会报错。

这是教学版正则语法，不支持字符类、转义、计数重复、锚点或工业级正则的回溯语义。
"""

from __future__ import annotations

from dataclasses import dataclass, field


EPSILON = None


@dataclass
class NFA:
    """保存 ε-NFA 的起点、唯一终点及邻接表。

    ``None`` 代表 ε 边；其余键均为单字符字面量。终点被设计为唯一状态，
    因而 Thompson 片段可以在不改变既有边的前提下继续组合。
    """

    start: int
    accept: int
    transitions: dict[int, dict[str | None, set[int]]] = field(default_factory=dict)


@dataclass
class _Fragment:
    """Thompson 构造期间尚未封装为 NFA 的单入口、单出口片段。"""

    start: int
    accept: int


class _RegexParser:
    """递归下降解析器，同时完成 Thompson 片段构造。"""

    def __init__(self, pattern: str) -> None:
        self.pattern = pattern
        self.position = 0
        self.next_state = 0
        self.transitions: dict[int, dict[str | None, set[int]]] = {}

    def build(self) -> NFA:
        """解析整个表达式并返回 NFA，拒绝未被语法消费的字符。"""
        if not self.pattern:
            return self._epsilon_fragment_as_nfa()

        fragment = self._parse_union()
        if self.position != len(self.pattern):
            character = self.pattern[self.position]
            raise ValueError(f"位置 {self.position} 的字符 {character!r} 不能出现在这里")
        return NFA(fragment.start, fragment.accept, self.transitions)

    def _parse_union(self) -> _Fragment:
        """解析最低优先级的并集：concatenation (``|`` concatenation)*。"""
        left = self._parse_concatenation()
        while self._peek() == "|":
            self.position += 1
            if self._peek() in {None, "|", ")"}:
                raise ValueError("并集运算符两侧都必须有表达式")
            right = self._parse_concatenation()
            left = self._alternate(left, right)
        return left

    def _parse_concatenation(self) -> _Fragment:
        """解析隐式连接；相邻可作为原子的项必须依次连接。"""
        if not self._starts_atom(self._peek()):
            raise ValueError("此处缺少可连接的表达式")

        result = self._parse_repetition()
        while self._starts_atom(self._peek()):
            result = self._concatenate(result, self._parse_repetition())
        return result

    def _parse_repetition(self) -> _Fragment:
        """解析最高优先级的闭包，并允许 ``a**`` 这样的重复闭包。"""
        result = self._parse_atom()
        while self._peek() == "*":
            self.position += 1
            result = self._star(result)
        return result

    def _parse_atom(self) -> _Fragment:
        """解析字面量或带括号的子表达式。"""
        character = self._peek()
        if character == "(":
            self.position += 1
            if self._peek() == ")":
                raise ValueError("空括号不是本教学语法中的有效表达式")
            result = self._parse_union()
            if self._peek() != ")":
                raise ValueError("缺少与左括号匹配的右括号")
            self.position += 1
            return result

        if self._is_literal(character):
            self.position += 1
            return self._literal(character)

        raise ValueError("此处需要字面量或左括号")

    def _literal(self, character: str) -> _Fragment:
        start, accept = self._new_state(), self._new_state()
        self._add_edge(start, character, accept)
        return _Fragment(start, accept)

    def _concatenate(self, left: _Fragment, right: _Fragment) -> _Fragment:
        self._add_edge(left.accept, EPSILON, right.start)
        return _Fragment(left.start, right.accept)

    def _alternate(self, left: _Fragment, right: _Fragment) -> _Fragment:
        start, accept = self._new_state(), self._new_state()
        self._add_edge(start, EPSILON, left.start)
        self._add_edge(start, EPSILON, right.start)
        self._add_edge(left.accept, EPSILON, accept)
        self._add_edge(right.accept, EPSILON, accept)
        return _Fragment(start, accept)

    def _star(self, fragment: _Fragment) -> _Fragment:
        start, accept = self._new_state(), self._new_state()
        # 新入口既可直接结束，也可进入旧片段；旧出口同样可循环或结束。
        self._add_edge(start, EPSILON, fragment.start)
        self._add_edge(start, EPSILON, accept)
        self._add_edge(fragment.accept, EPSILON, fragment.start)
        self._add_edge(fragment.accept, EPSILON, accept)
        return _Fragment(start, accept)

    def _epsilon_fragment_as_nfa(self) -> NFA:
        start, accept = self._new_state(), self._new_state()
        self._add_edge(start, EPSILON, accept)
        return NFA(start, accept, self.transitions)

    def _new_state(self) -> int:
        state = self.next_state
        self.next_state += 1
        return state

    def _add_edge(self, source: int, symbol: str | None, target: int) -> None:
        self.transitions.setdefault(source, {}).setdefault(symbol, set()).add(target)

    def _peek(self) -> str | None:
        if self.position == len(self.pattern):
            return None
        return self.pattern[self.position]

    @staticmethod
    def _is_literal(character: str | None) -> bool:
        return character is not None and character not in {"|", "*", "(", ")", ".", "\\"}

    def _starts_atom(self, character: str | None) -> bool:
        return character == "(" or self._is_literal(character)


def regex_to_nfa(pattern: str) -> NFA:
    """把受限正则表达式转换为等价 ε-NFA。

    参数：``pattern`` 是由单字符字面量、``|``、``*`` 和圆括号组成的表达式。
    返回值：带唯一接受状态的 ``NFA``。
    边界情况：空串对应只接受空串的 NFA；无效语法抛出 ``ValueError``。
    关键点：递归下降的优先级层次天然保证 ``*`` 高于连接，连接高于 ``|``。
    """
    if not isinstance(pattern, str):
        raise TypeError("正则表达式必须是字符串")
    return _RegexParser(pattern).build()


def _epsilon_closure(nfa: NFA, states: set[int]) -> set[int]:
    """计算状态集合的 ε 闭包；每个状态至多入栈一次。"""
    closure = set(states)
    pending = list(states)
    while pending:
        state = pending.pop()
        for target in nfa.transitions.get(state, {}).get(EPSILON, set()):
            if target not in closure:
                closure.add(target)
                pending.append(target)
    return closure


def nfa_accepts(nfa: NFA, text: str) -> bool:
    """模拟 ε-NFA 是否接受文本。

    参数：``nfa`` 是本模块构造的自动机，``text`` 是待匹配文本。
    返回值：文本读完后当前 ε 闭包是否含接受状态。
    边界情况：空文本会先展开起点 ε 闭包；未定义的字符边自然导致空状态集合。
    关键点：每消费一个字符后立即求 ε 闭包，避免漏掉后续可达状态。
    """
    current_states = _epsilon_closure(nfa, {nfa.start})
    for character in text:
        next_states: set[int] = set()
        for state in current_states:
            next_states.update(nfa.transitions.get(state, {}).get(character, set()))
        current_states = _epsilon_closure(nfa, next_states)
    return nfa.accept in current_states


if __name__ == "__main__":
    expression_nfa = regex_to_nfa("a(b|c)*")
    assert nfa_accepts(expression_nfa, "a")
    assert nfa_accepts(expression_nfa, "abcb")
    assert not nfa_accepts(expression_nfa, "")
    assert not nfa_accepts(expression_nfa, "acbd")

    precedence_nfa = regex_to_nfa("a|bc")
    assert nfa_accepts(precedence_nfa, "a")
    assert nfa_accepts(precedence_nfa, "bc")
    assert not nfa_accepts(precedence_nfa, "b")

    empty_nfa = regex_to_nfa("")
    assert nfa_accepts(empty_nfa, "")
    assert not nfa_accepts(empty_nfa, "a")

    try:
        regex_to_nfa("a|")
        raise AssertionError("无效表达式应当抛出 ValueError")
    except ValueError:
        pass

    print("001_regex_to_nfa: all examples passed")
