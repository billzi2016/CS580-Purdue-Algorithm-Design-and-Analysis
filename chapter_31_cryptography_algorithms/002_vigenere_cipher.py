"""Vigenere cipher 的教学实现。

适用场景：Vigenere cipher 以关键字提供重复位移序列，用于说明多表替换密码；它是历史密码，
不具备现代安全性，绝不可用于保密数据。仅英文字母被加密，大小写及其他字符原样保留。
时间复杂度 O(n)，空间复杂度 O(n)。空文本有效；关键字必须为非空 ASCII 字母串。
"""


def _key_shifts(key: str) -> list[int]:
    """将关键字转换为 0–25 位移序列，并严格校验其格式。"""
    if (
        not isinstance(key, str)
        or not key
        or any(not ("A" <= char <= "Z" or "a" <= char <= "z") for char in key)
    ):
        raise ValueError("key 必须是非空 ASCII 字母串")
    return [ord(char.lower()) - ord("a") for char in key]


def _transform(text: str, key: str, direction: int) -> str:
    """按关键字循环执行正向或反向位移；只在处理字母时推进 key 下标。"""
    if not isinstance(text, str):
        raise ValueError("text 必须是字符串")
    shifts = _key_shifts(key)
    result: list[str] = []
    key_index = 0
    for character in text:
        if "A" <= character <= "Z" or "a" <= character <= "z":
            base = ord("A") if character.isupper() else ord("a")
            shift = shifts[key_index % len(shifts)] * direction
            result.append(chr(base + (ord(character) - base + shift) % 26))
            key_index += 1
        else:
            result.append(character)
    return "".join(result)


def vigenere_encrypt(text: str, key: str) -> str:
    """以 key 的字母位移序列加密 text，返回密文；格式约束见模块说明。"""
    return _transform(text, key, 1)


def vigenere_decrypt(text: str, key: str) -> str:
    """以 key 的反向位移序列解密 text，返回原文；非字母不消耗关键字。"""
    return _transform(text, key, -1)


if __name__ == "__main__":
    assert vigenere_encrypt("ATTACKATDAWN", "LEMON") == "LXFOPVEFRNHR"
    assert vigenere_decrypt("LXFOPVEFRNHR", "LEMON") == "ATTACKATDAWN"
    assert vigenere_encrypt("Hello, World!", "Key") == "Rijvs, Uyvjn!"
    assert vigenere_decrypt(vigenere_encrypt("A b-c", "z"), "z") == "A b-c"
    try:
        vigenere_encrypt("text", "")
        raise AssertionError("空 key 应当抛出 ValueError")
    except ValueError:
        pass
    print("002_vigenere_cipher: all examples passed")
