"""用 shunting-yard 算法把算术中缀表达式转换为后缀表达式。

适用场景：表达式解析器、简单计算器和编译器前端将优先级显式化。
核心思想：操作数直接输出；运算符按优先级和结合性在栈与输出之间转移。
输入输出：输入由标识符、整数、``+ - * / ^`` 和括号组成的字符串，输出 token 列表形式的 RPN。
时间复杂度：O(n)；空间复杂度 O(n)。
边界情况：支持一元负号 ``u-``、右结合幂运算；不支持函数调用、逗号、浮点数或隐式乘法。
"""

from __future__ import annotations


OPERATORS = {
    "+": (1, "left"), "-": (1, "left"), "*": (2, "left"), "/": (2, "left"),
    "^": (3, "right"), "u-": (4, "right"),
}


def tokenize(expression: str) -> list[str]:
    """把受限算术表达式切分为 token。

    参数：``expression`` 是源文本。返回值：标识符、整数、运算符和括号 token 列表。
    边界情况：空白被忽略；未知字符会抛出 ``ValueError``。关键点：标识符允许下划线和数字后缀。
    """
    tokens: list[str] = []
    index = 0
    while index < len(expression):
        char = expression[index]
        if char.isspace():
            index += 1
            continue
        if char.isalpha() or char == "_":
            end = index + 1
            while end < len(expression) and (
                expression[end].isalnum() or expression[end] == "_"
            ):
                end += 1
            tokens.append(expression[index:end])
            index = end
            continue
        if char.isdigit():
            end = index + 1
            while end < len(expression) and expression[end].isdigit():
                end += 1
            tokens.append(expression[index:end])
            index = end
            continue
        if char in "+-*/^()":
            tokens.append(char)
            index += 1
            continue
        raise ValueError(f"不支持的字符：{char!r}")
    return tokens


def infix_to_postfix(expression: str) -> list[str]:
    """将受限中缀算术表达式转成 RPN token 列表。

    参数：``expression`` 为中缀文本。返回值：后缀 token 序列。边界：空式、括号不配对和连续操作数会报错。
    关键点：左结合操作符在同优先级时弹栈，右结合操作符只弹出严格更高优先级的操作符。
    """
    raw_tokens = tokenize(expression)
    if not raw_tokens:
        raise ValueError("表达式不能为空")
    output: list[str] = []
    stack: list[str] = []
    expect_operand = True
    for token in raw_tokens:
        if _is_operand(token):
            if not expect_operand:
                raise ValueError("两个操作数之间缺少运算符")
            output.append(token)
            expect_operand = False
            continue
        if token == "(":
            if not expect_operand:
                raise ValueError("左括号前缺少运算符")
            stack.append(token)
            continue
        if token == ")":
            if expect_operand:
                raise ValueError("右括号前缺少操作数")
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            if not stack:
                raise ValueError("右括号没有匹配的左括号")
            stack.pop()
            expect_operand = False
            continue
        operator = "u-" if token == "-" and expect_operand else token
        if expect_operand and operator != "u-":
            raise ValueError("运算符前缺少操作数")
        while stack and stack[-1] != "(" and _must_pop(stack[-1], operator):
            output.append(stack.pop())
        stack.append(operator)
        expect_operand = True
    if expect_operand:
        raise ValueError("表达式不能以运算符结束")
    while stack:
        if stack[-1] == "(": raise ValueError("左括号没有匹配的右括号")
        output.append(stack.pop())
    return output


def _is_operand(token: str) -> bool:
    """判断 token 是否是标识符或整数字面量，而不是语法运算符。"""
    return token not in OPERATORS and token not in {"(", ")"}


def _must_pop(top: str, incoming: str) -> bool:
    """按 incoming 的结合性判断栈顶运算符是否必须先输出。"""
    top_priority, _ = OPERATORS[top]
    incoming_priority, associativity = OPERATORS[incoming]
    return top_priority > incoming_priority or (top_priority == incoming_priority and associativity == "left")


if __name__ == "__main__":
    assert infix_to_postfix("a + b * c") == ["a", "b", "c", "*", "+"]
    assert infix_to_postfix("a ^ b ^ c") == ["a", "b", "c", "^", "^"]
    assert infix_to_postfix("-(x + 2) * y") == ["x", "2", "+", "u-", "y", "*"]
    try:
        infix_to_postfix("a +")
        raise AssertionError("不完整表达式应失败")
    except ValueError:
        pass
    print("008_shunting_yard: all examples passed")
