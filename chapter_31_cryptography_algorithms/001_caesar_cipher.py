"""Caesar cipher 的教学实现。

适用场景：Caesar cipher 是对英文字母作固定循环位移的历史密码，适合说明替换密码；它不具备
现代安全性，绝不可用于保密数据。输入文本与整数位移，输出保持大小写与非字母字符不变的密文。
时间复杂度 O(n)，空间复杂度 O(n)。空文本有效；shift 可为负或任意大整数。
"""


def caesar_encrypt(text: str, shift: int) -> str:
    """对 ASCII 英文字母执行循环位移加密。

    参数：text 是原文，shift 是可正可负的位移。返回密文。
    边界：空串返回空串，非字符串或非整数（含 bool）抛出 ValueError。
    关键点：用模 26 把移出字母表末端的字符绕回开头，非字母不参与位移。
    """
    if not isinstance(text, str) or isinstance(shift, bool) or not isinstance(shift, int):
        raise ValueError("text 必须是字符串且 shift 必须是整数")
    result: list[str] = []
    for character in text:
        if "A" <= character <= "Z" or "a" <= character <= "z":
            base = ord("A") if character.isupper() else ord("a")
            result.append(chr(base + (ord(character) - base + shift) % 26))
        else:
            result.append(character)
    return "".join(result)


def caesar_decrypt(text: str, shift: int) -> str:
    """用相反位移解密 Caesar 密文；参数、返回值和边界与 caesar_encrypt 相同。"""
    return caesar_encrypt(text, -shift)


if __name__ == "__main__":
    assert caesar_encrypt("Abc XYZ!", 3) == "Def ABC!"
    assert caesar_decrypt("Def ABC!", 3) == "Abc XYZ!"
    assert caesar_encrypt("", 100) == ""
    assert caesar_encrypt("zZ", -1) == "yY"
    assert caesar_decrypt(caesar_encrypt("Meet at 5.", 53), 53) == "Meet at 5."
    print("001_caesar_cipher: all examples passed")
