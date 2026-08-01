"""SHA-256 核心教学实现；遵循 FIPS 180-4，不调用 hashlib，不能替代经审计实现。"""
K=(0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2)
H0=(0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19)
MASK=0xffffffff
def _r(x,n): return ((x>>n)|(x<<(32-n)))&MASK
def sha256_digest(data:bytes)->bytes:
    """手写 SHA-256：填充、消息扩展和 64 轮压缩；输入必须为 bytes，返回 32 bytes 摘要。"""
    if not isinstance(data,bytes): raise ValueError("data 必须是 bytes")
    bits=len(data)*8; padded=data+b'\x80'
    padded+=b'\x00'*((56-len(padded)%64)%64)+bits.to_bytes(8,'big')
    state=list(H0)
    for offset in range(0,len(padded),64):
        block=padded[offset:offset+64]; words=[int.from_bytes(block[i:i+4],'big') for i in range(0,64,4)]
        for i in range(16,64):
            s0=_r(words[i-15],7)^_r(words[i-15],18)^(words[i-15]>>3); s1=_r(words[i-2],17)^_r(words[i-2],19)^(words[i-2]>>10)
            words.append((words[i-16]+s0+words[i-7]+s1)&MASK)
        a,b,c,d,e,f,g,h=state
        for i in range(64):
            s1=_r(e,6)^_r(e,11)^_r(e,25); choice=(e&f)^((~e)&g); t1=(h+s1+choice+K[i]+words[i])&MASK
            s0=_r(a,2)^_r(a,13)^_r(a,22); majority=(a&b)^(a&c)^(b&c); t2=(s0+majority)&MASK
            h,g,f,e,d,c,b,a=g,f,e,(d+t1)&MASK,c,b,a,(t1+t2)&MASK
        state=[(x+y)&MASK for x,y in zip(state,(a,b,c,d,e,f,g,h))]
    return b''.join(word.to_bytes(4,'big') for word in state)
def sha256_hex(data:bytes)->str:
    """返回 sha256_digest 的小写十六进制表示。"""; return sha256_digest(data).hex()
if __name__=="__main__":
    assert sha256_hex(b"")=="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    assert sha256_hex(b"abc")=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    assert len(sha256_digest(b"a"*1000))==32
    print("007_sha256_core: all examples passed")
