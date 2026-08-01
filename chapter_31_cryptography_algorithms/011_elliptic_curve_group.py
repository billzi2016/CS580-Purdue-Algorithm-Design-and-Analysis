"""短 Weierstrass 椭圆曲线群运算教学实现。

曲线为 y²=x³+ax+b (mod p)，None 表示无穷远点。仅用于小参数算术演示，不验证安全曲线。
"""

Point = tuple[int, int] | None


def _inverse(value: int, modulus: int) -> int:
    """用扩展欧几里得求有限域非零元素的逆元。"""
    old_r, remainder, old_s, coefficient = value % modulus, modulus, 1, 0
    while remainder:
        quotient = old_r // remainder
        old_r, remainder = remainder, old_r - quotient * remainder
        old_s, coefficient = coefficient, old_s - quotient * coefficient
    if old_r != 1:
        raise ValueError("分母在模 p 下不可逆")
    return old_s % modulus


def is_on_curve(point: Point, prime: int, a: int, b: int) -> bool:
    """判断点是否满足曲线方程；无穷远点属于群。"""
    if point is None:
        return True
    x, y = point
    return (y * y - (x * x * x + a * x + b)) % prime == 0


def point_add(left: Point, right: Point, prime: int, a: int, b: int) -> Point:
    """计算两点群加法，处理无穷远、相反点、不同点与倍点。"""
    if (
        prime <= 2
        or not is_on_curve(left, prime, a, b)
        or not is_on_curve(right, prime, a, b)
    ):
        raise ValueError("曲线参数或点无效")
    if left is None:
        return right
    if right is None:
        return left
    x1, y1 = left
    x2, y2 = right
    if x1 == x2 and (y1 + y2) % prime == 0:
        return None
    if left == right:
        if y1 % prime == 0:
            return None
        slope = (3 * x1 * x1 + a) * _inverse(2 * y1, prime) % prime
    else:
        slope = (y2 - y1) * _inverse(x2 - x1, prime) % prime
    x3 = (slope * slope - x1 - x2) % prime
    return x3, (slope * (x1 - x3) - y1) % prime


def scalar_multiply(multiplier: int, point: Point, prime: int, a: int, b: int) -> Point:
    """手写 double-and-add，计算 multiplier * point；负标量不支持。"""
    if (
        isinstance(multiplier, bool)
        or not isinstance(multiplier, int)
        or multiplier < 0
    ):
        raise ValueError("multiplier 必须是非负整数")
    result: Point = None
    addend = point
    while multiplier:
        if multiplier & 1:
            result = point_add(result, addend, prime, a, b)
        addend = point_add(addend, addend, prime, a, b)
        multiplier >>= 1
    return result


if __name__ == "__main__":
    curve = (17, 2, 2)
    base = (5, 1)
    assert is_on_curve(base, *curve)
    assert point_add(base, base, *curve) == (6, 3)
    assert scalar_multiply(19, base, *curve) is None
    assert scalar_multiply(0, base, *curve) is None
    print("011_elliptic_curve_group: all examples passed")
