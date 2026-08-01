"""SHA-256 核心教学实现；遵循 FIPS 180-4，不调用 hashlib，不能替代经审计实现。"""

K = (
    0x428A2F98,
    0x71374491,
    0xB5C0FBCF,
    0xE9B5DBA5,
    0x3956C25B,
    0x59F111F1,
    0x923F82A4,
    0xAB1C5ED5,
    0xD807AA98,
    0x12835B01,
    0x243185BE,
    0x550C7DC3,
    0x72BE5D74,
    0x80DEB1FE,
    0x9BDC06A7,
    0xC19BF174,
    0xE49B69C1,
    0xEFBE4786,
    0x0FC19DC6,
    0x240CA1CC,
    0x2DE92C6F,
    0x4A7484AA,
    0x5CB0A9DC,
    0x76F988DA,
    0x983E5152,
    0xA831C66D,
    0xB00327C8,
    0xBF597FC7,
    0xC6E00BF3,
    0xD5A79147,
    0x06CA6351,
    0x14292967,
    0x27B70A85,
    0x2E1B2138,
    0x4D2C6DFC,
    0x53380D13,
    0x650A7354,
    0x766A0ABB,
    0x81C2C92E,
    0x92722C85,
    0xA2BFE8A1,
    0xA81A664B,
    0xC24B8B70,
    0xC76C51A3,
    0xD192E819,
    0xD6990624,
    0xF40E3585,
    0x106AA070,
    0x19A4C116,
    0x1E376C08,
    0x2748774C,
    0x34B0BCB5,
    0x391C0CB3,
    0x4ED8AA4A,
    0x5B9CCA4F,
    0x682E6FF3,
    0x748F82EE,
    0x78A5636F,
    0x84C87814,
    0x8CC70208,
    0x90BEFFFA,
    0xA4506CEB,
    0xBEF9A3F7,
    0xC67178F2,
)
H0 = (
    0x6A09E667,
    0xBB67AE85,
    0x3C6EF372,
    0xA54FF53A,
    0x510E527F,
    0x9B05688C,
    0x1F83D9AB,
    0x5BE0CD19,
)
MASK = 0xFFFFFFFF


def _r(x, n):
    return ((x >> n) | (x << (32 - n))) & MASK


def sha256_digest(data: bytes) -> bytes:
    """手写 SHA-256：填充、消息扩展和 64 轮压缩；输入必须为 bytes，返回 32 bytes 摘要。"""
    if not isinstance(data, bytes):
        raise ValueError("data 必须是 bytes")
    bits = len(data) * 8
    padded = data + b"\x80"
    padded += b"\x00" * ((56 - len(padded) % 64) % 64) + bits.to_bytes(8, "big")
    state = list(H0)
    for offset in range(0, len(padded), 64):
        block = padded[offset : offset + 64]
        words = [int.from_bytes(block[i : i + 4], "big") for i in range(0, 64, 4)]
        for i in range(16, 64):
            s0 = _r(words[i - 15], 7) ^ _r(words[i - 15], 18) ^ (words[i - 15] >> 3)
            s1 = _r(words[i - 2], 17) ^ _r(words[i - 2], 19) ^ (words[i - 2] >> 10)
            words.append((words[i - 16] + s0 + words[i - 7] + s1) & MASK)
        a, b, c, d, e, f, g, h = state
        for i in range(64):
            s1 = _r(e, 6) ^ _r(e, 11) ^ _r(e, 25)
            choice = (e & f) ^ ((~e) & g)
            t1 = (h + s1 + choice + K[i] + words[i]) & MASK
            s0 = _r(a, 2) ^ _r(a, 13) ^ _r(a, 22)
            majority = (a & b) ^ (a & c) ^ (b & c)
            t2 = (s0 + majority) & MASK
            h, g, f, e, d, c, b, a = g, f, e, (d + t1) & MASK, c, b, a, (t1 + t2) & MASK
        state = [(x + y) & MASK for x, y in zip(state, (a, b, c, d, e, f, g, h))]
    return b"".join(word.to_bytes(4, "big") for word in state)


def sha256_hex(data: bytes) -> str:
    """返回 sha256_digest 的小写十六进制表示。"""
    return sha256_digest(data).hex()


if __name__ == "__main__":
    assert (
        sha256_hex(b"")
        == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )
    assert (
        sha256_hex(b"abc")
        == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    )
    assert len(sha256_digest(b"a" * 1000)) == 32
    print("007_sha256_core: all examples passed")
