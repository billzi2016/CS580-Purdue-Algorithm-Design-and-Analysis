"""HMAC-SHA-256 教学实现，遵循 RFC 2104；复用本章手写 SHA，不替代生产 MAC。"""

import importlib.util
from pathlib import Path


def _sha(data: bytes) -> bytes:
    spec = importlib.util.spec_from_file_location(
        "sha_core", Path(__file__).with_name("007_sha256_core.py")
    )
    module = importlib.util.module_from_spec(spec)
    if spec is None or spec.loader is None:
        raise RuntimeError("无法加载 SHA-256 实现")
    spec.loader.exec_module(module)
    return module.sha256_digest(data)


def hmac_sha256(key: bytes, message: bytes) -> bytes:
    """手写 HMAC 内外 pad；长 key 先摘要，短 key 补零，返回 32 bytes。"""
    if not isinstance(key, bytes) or not isinstance(message, bytes):
        raise ValueError("key 和 message 必须是 bytes")
    if len(key) > 64:
        key = _sha(key)
    key = key + b"\0" * (64 - len(key))
    return _sha(
        bytes(x ^ 0x5C for x in key) + _sha(bytes(x ^ 0x36 for x in key) + message)
    )


if __name__ == "__main__":
    assert (
        hmac_sha256(b"key", b"The quick brown fox jumps over the lazy dog").hex()
        == "f7bc83f430538424b13298e6aa6fb143ef4d59a14946175997479dbc2d1a3cd8"
    )
    assert hmac_sha256(b"", b"") != b""
    print("008_hmac: all examples passed")
