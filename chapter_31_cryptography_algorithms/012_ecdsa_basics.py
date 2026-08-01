"""小曲线 ECDSA 教学签名与验证。

使用 p=17、a=2、b=2、G=(5,1)、n=19 的公开教学曲线。参数极小、k 由调用方提供，不能用于真实签名。
"""

import importlib.util
from pathlib import Path


def _ecc():
    """加载本章手写点运算，避免复制椭圆曲线核心逻辑。"""
    spec = importlib.util.spec_from_file_location(
        "ecc", Path(__file__).with_name("011_elliptic_curve_group.py")
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("无法加载椭圆曲线实现")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


P, A, B, G, N = 17, 2, 2, (5, 1), 19


def _inverse(value: int) -> int:
    """因 n=19 为素数，用扩展欧几里得求模 n 逆元。"""
    t, new_t, r, new_r = 0, 1, N, value % N
    while new_r:
        quotient = r // new_r
        t, new_t, r, new_r = new_t, t - quotient * new_t, new_r, r - quotient * new_r
    if r != 1:
        raise ValueError("数值在群阶下不可逆")
    return t % N


def ecdsa_public_key(private_key: int) -> tuple[int, int]:
    """计算 Q=dG；私钥必须是 1 到 n-1。"""
    if not 1 <= private_key < N:
        raise ValueError("私钥范围无效")
    point = _ecc().scalar_multiply(private_key, G, P, A, B)
    if point is None:
        raise ValueError("得到无穷远公钥")
    return point


def ecdsa_sign(message_hash: int, private_key: int, nonce: int) -> tuple[int, int]:
    """按 (r,s)=(x(kG),k^-1(z+rd)) mod n 签名；nonce 必须新鲜且保密。"""
    if not 0 <= message_hash < N or not 1 <= private_key < N or not 1 <= nonce < N:
        raise ValueError("哈希、私钥或 nonce 范围无效")
    point = _ecc().scalar_multiply(nonce, G, P, A, B)
    if point is None:
        raise ValueError("nonce 无效")
    r = point[0] % N
    s = _inverse(nonce) * (message_hash + r * private_key) % N
    if r == 0 or s == 0:
        raise ValueError("该 nonce 产生零签名分量")
    return r, s


def ecdsa_verify(
    message_hash: int, signature: tuple[int, int], public_key: tuple[int, int]
) -> bool:
    """按 u1G+u2Q 的 x 坐标验证 ECDSA 教学签名。"""
    if (
        not 0 <= message_hash < N
        or not isinstance(signature, tuple)
        or len(signature) != 2
    ):
        raise ValueError("输入格式无效")
    r, s = signature
    if not 1 <= r < N or not 1 <= s < N:
        return False
    ecc = _ecc()
    if not ecc.is_on_curve(public_key, P, A, B):
        return False
    inverse_s = _inverse(s)
    first = ecc.scalar_multiply(message_hash * inverse_s % N, G, P, A, B)
    second = ecc.scalar_multiply(r * inverse_s % N, public_key, P, A, B)
    point = ecc.point_add(first, second, P, A, B)
    return point is not None and point[0] % N == r


if __name__ == "__main__":
    private = 7
    public = ecdsa_public_key(private)
    signature = ecdsa_sign(11, private, 3)
    assert signature == (10, 8)
    assert ecdsa_verify(11, signature, public)
    assert not ecdsa_verify(12, signature, public)
    print("012_ecdsa_basics: all examples passed")
