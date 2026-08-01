"""把受限赋值表达式翻译为三地址码（three-address code）。

适用场景：编译器中间表示入门，展示表达式树如何被分解为每条指令至多一个运算符的形式。
核心思想：递归下降解析产生 AST；后序遍历先生成子表达式，随后以新临时变量承接当前运算结果。
输入输出：输入 ``identifier = expression``，输出 ``Instruction`` 列表，最后一条为赋值指令。
时间复杂度：O(n)；空间复杂度 O(n)，用于 token、AST 和临时指令。
边界情况：支持整数、标识符、括号、``+ - * /`` 与一元负号；不支持函数、数组、控制流和类型转换。
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Expression:
    """受限算术表达式 AST 节点；叶子节点的 ``operator`` 为 ``None``。"""

    operator: str | None
    left: "Expression | str"
    right: "Expression | None" = None


@dataclass(frozen=True)
class Instruction:
    """一条三地址码指令，``operator`` 为 ``=`` 时表示单纯赋值。"""

    target: str
    operator: str
    left: str
    right: str | None = None

    def render(self) -> str:
        """输出教材中常见的可读三地址码文本。"""
        if self.operator == "=":
            return f"{self.target} = {self.left}"
        if self.operator == "neg":
            return f"{self.target} = -{self.left}"
        return f"{self.target} = {self.left} {self.operator} {self.right}"


def generate_three_address_code(statement: str) -> list[Instruction]:
    """解析一条赋值语句并生成其三地址码。

    参数：``statement`` 格式为 ``目标 = 算术表达式``。返回值：按执行顺序排列的指令。
    边界情况：缺少赋值号、左侧不是单一标识符、非法 token 或括号不配对会抛出 ``ValueError``。
    关键点：后序翻译确保每条运算指令所引用的临时值已经在此前定义。
    """
    tokens = _tokenize(statement)
    if len(tokens) < 3 or tokens[1] != "=" or not _is_identifier(tokens[0]):
        raise ValueError("语句必须形如 identifier = expression")
    parser = _ExpressionParser(tokens[2:])
    tree = parser.parse()
    generator = _CodeGenerator()
    result = generator.emit(tree)
    generator.instructions.append(Instruction(tokens[0], "=", result))
    return generator.instructions


def _tokenize(text: str) -> list[str]:
    tokens: list[str] = []
    index = 0
    while index < len(text):
        char = text[index]
        if char.isspace():
            index += 1
        elif char.isalpha() or char == "_":
            end = index + 1
            while end < len(text) and (text[end].isalnum() or text[end] == "_"):
                end += 1
            tokens.append(text[index:end])
            index = end
        elif char.isdigit():
            end = index + 1
            while end < len(text) and text[end].isdigit():
                end += 1
            tokens.append(text[index:end])
            index = end
        elif char in "+-*/()=":
            tokens.append(char)
            index += 1
        else:
            raise ValueError(f"不支持的字符：{char!r}")
    return tokens


class _ExpressionParser:
    """按 ``加减 → 乘除 → 一元 → 原子`` 优先级构造 AST。"""

    def __init__(self, tokens: list[str]) -> None:
        self.tokens = tokens
        self.position = 0

    def parse(self) -> Expression:
        if not self.tokens:
            raise ValueError("赋值号右侧不能为空")
        expression = self._parse_sum()
        if self.position != len(self.tokens):
            raise ValueError(f"无法解析 token：{self.tokens[self.position]!r}")
        return expression

    def _parse_sum(self) -> Expression:
        node = self._parse_product()
        while self._peek() in {"+", "-"}:
            operator = self._consume()
            node = Expression(operator, node, self._parse_product())
        return node

    def _parse_product(self) -> Expression:
        node = self._parse_unary()
        while self._peek() in {"*", "/"}:
            operator = self._consume()
            node = Expression(operator, node, self._parse_unary())
        return node

    def _parse_unary(self) -> Expression:
        if self._peek() == "-":
            self._consume()
            return Expression("neg", self._parse_unary())
        return self._parse_atom()

    def _parse_atom(self) -> Expression:
        token = self._peek()
        if token == "(":
            self._consume()
            node = self._parse_sum()
            if self._consume() != ")":
                raise ValueError("缺少右括号")
            return node
        if token is None or not (_is_identifier(token) or token.isdigit()):
            raise ValueError("此处需要操作数或左括号")
        return Expression(None, self._consume())

    def _peek(self) -> str | None:
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def _consume(self) -> str:
        token = self._peek()
        if token is None:
            raise ValueError("表达式意外结束")
        self.position += 1
        return token


class _CodeGenerator:
    """将 AST 后序线性化，每个复合节点分配一个新的临时变量。"""

    def __init__(self) -> None:
        self.instructions: list[Instruction] = []
        self.next_temporary = 1

    def emit(self, expression: Expression) -> str:
        if expression.operator is None:
            return str(expression.left)
        left = self.emit(expression.left)  # type: ignore[arg-type]
        if expression.operator == "neg":
            temporary = self._new_temporary()
            self.instructions.append(Instruction(temporary, "neg", left))
        else:
            right = self.emit(expression.right)  # type: ignore[arg-type]
            # 先完整翻译左右子树，临时变量编号才与实际指令出现顺序保持一致。
            temporary = self._new_temporary()
            self.instructions.append(
                Instruction(temporary, expression.operator, left, right)
            )
        return temporary

    def _new_temporary(self) -> str:
        temporary = f"t{self.next_temporary}"
        self.next_temporary += 1
        return temporary


def _is_identifier(token: str) -> bool:
    return token.isidentifier()


if __name__ == "__main__":
    instructions = generate_three_address_code("result = a + b * (c - d)")
    assert [instruction.render() for instruction in instructions] == [
        "t1 = c - d",
        "t2 = b * t1",
        "t3 = a + t2",
        "result = t3",
    ]
    unary = generate_three_address_code("x = -a + 2")
    assert [instruction.render() for instruction in unary] == [
        "t1 = -a",
        "t2 = t1 + 2",
        "x = t2",
    ]
    try:
        generate_three_address_code("a + b")
        raise AssertionError("缺失赋值号必须失败")
    except ValueError:
        pass
    print("009_three_address_code: all examples passed")
