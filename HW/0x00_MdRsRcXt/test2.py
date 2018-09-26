import hashlib
import sys
import binascii
import struct

A = b'''
c8fa95e997bdb8f8a0c467af38fb3dd9615a7efa1db72901c704a8c614067a8c
5a8d77c0ee8fe1b9bad5d896ae4ac4d82260a5ff814d79aaf1eafca8eb90acce
29aafcadc769582e8f43a72eb1fc37954c1ceabf83805534b06a061e80d6e59d
9fbee29ccf8064b8b39751af7858e0a7af6dc504061c2e5d65d328d2224c81e9
0b64ada933b9a7e3b5643bad974b2d37af45fda17db5cc0a550237709132b8a5
4e2c9b67167603f715553cd544db7b185f4e77423c9274d55f1b93782b2560b6
eeccd8ef91f6235187eb32606fb3704ac6373cd4f6303f226fce411a0dabc812
3d5df9c8c610dd8398ad4ff69d2c39c0b4523ff352231cbcab29553a25558d99
8736e450fe4184924e47106246d42a7693f500ad178b3fcc1793512b9b39cd41
e670f1dc0085282664065476f152e221be6086cc9526920c19f8b0c05b6fd659
1000b66f17aeb63579ef626ad8d6f49c5cd0eaf8fd2a35822fa6cbba101127ed
69d6a72fc249395e04176718a2c0839c3c56d0eab1097570d36ac2555b25beb1
5e94d956d9aa0cca6fe9001d76bdb8bf3a8a9e401ac4ecf5ea567cb29cdea0ff
adb1659ad8a0074ea3fd8b0308b76d75c22b99b69e5a27a84a8903da994c8d2d
2f31d9fc6f843e7f64a77fcf6af113866967eb721218e37b48533ad49decbc58
9a62cab7ed3094dc561dcffd5954aeddf1652c34d62eeb4102d621c02e9dc4e5
'''.replace(b'\n', b'')

a = int('''
d3d36115599d53eeb0413c3a818e120bc1ce4cc9bca9e7b23a695a150c056c4a
6ca2e3ce99efe8a0f4385e86e8897d2e47bd25a45e723b768af040e2b6d73beb
193fb86aae849513463e3a794768ab865b4b82bd5df627e83afdfc0ee00bc983
2e6c38e53d2812a344ff34008198e142e642c95a449a762d7fd30df018fa5fe6
53c882a192d011594a29a0926fe841473622a61e41ac0f675f5fda76a27561ff
c7c90c6d85464f23fab9e88bfca8ed5a0f2e0e11c0a0f4521e1919194e868d18
c0d33f5fdc0cb95793ca96f7b8a7127cb9ae6acde7e158bcf718cf30ea69933e
f6cdefa6f9383f8c9735f9510f70f228d299479a257c1a2d3c10d1f47cc1a055
'''.replace('\n', ''), 16)

b = int('''
e5b537e60922d57a763918a5b1e8af1bc07c85fefea11e8179f2a9ee6cf7c611
7d0eba7963617035cf1ddb1f0cc858d70890a76990f96adb29ea8b0403f869cd
be51b76f06c25a9319ecd04366f846338fc1f81ae05f143940039bfbbc4de953
b933c89e74fe62485157d7a3b31993915808a4b95bb768f369818c10edfa561e
3530c999c33ef62a4466ec67622cc12525cf0ea3d402931d16ef115acc172641
a63037190ba04931d3caa2ef861ee7f277647844f8a7f94569f06cea32badb02
82355467cec0bdbdff5e7cd837ffce048925280ab92a9560c1cd6bd309239d7e
72b298af5ad81d27ee9adf7143185815bdadfa21296833149748ed2f55343533
'''.replace('\n', ''), 16) * a

K = hex(a).encode('ascii')

m = list(binascii.a2b_hex(A))

k = struct.unpack("<4L", K[:16])
for i in range(0, 512, 8):
    v0, v1 = struct.unpack("<2L", bytes(m[i:i+8]))
    delta, mask = 0x9e3779b9, 0xffffffff
    sum = (delta * 32) & mask
    for round in range(32):
        v1 = (v1 - (((v0 << 4 ^ v0 >> 5) + v0) ^ (sum + k[sum >> 11 & 3]))) & mask
        sum = (sum - delta) & mask
        v0 = (v0 - (((v1 << 4 ^ v1 >> 5) + v1) ^ (sum + k[sum & 3]))) & mask
    e = struct.pack("<2L", v0, v1)
    for j in range(8):
        m[i+j] = e[j]


rtb = []
for z in range(256):
    rtr = []
    for i in range(512):
        rtr.append(z)
    
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + K[i % len(K)]) % 256
        S[i], S[j] = S[j], S[i]
    j = 0
    for k in range(len(rtr)):
        i = (k + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        rtr[k] ^= S[(S[i] + S[j]) % 256]
        
    rtb.append(rtr)

for i in range(len(m)):
    for j in range(256):
        if m[i] == rtb[j][i]:
            m[i]=j
            break
           
m = bytes(m)
m = binascii.b2a_hex(m) 
m = int(m, 16)


def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi
    
    while e > 0:
        temp1 = temp_phi//e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2
        
        x = x2- temp1* x1
        y = d - temp1 * y1
        
        x2 = x1
        x1 = x
        d = y1
        y1 = y
    
    if temp_phi == 1:
        return d + phi

p = int('''
d3d36115599d53eeb0413c3a818e120bc1ce4cc9bca9e7b23a695a150c056c4a
6ca2e3ce99efe8a0f4385e86e8897d2e47bd25a45e723b768af040e2b6d73beb
193fb86aae849513463e3a794768ab865b4b82bd5df627e83afdfc0ee00bc983
2e6c38e53d2812a344ff34008198e142e642c95a449a762d7fd30df018fa5fe6
53c882a192d011594a29a0926fe841473622a61e41ac0f675f5fda76a27561ff
c7c90c6d85464f23fab9e88bfca8ed5a0f2e0e11c0a0f4521e1919194e868d18
c0d33f5fdc0cb95793ca96f7b8a7127cb9ae6acde7e158bcf718cf30ea69933e
f6cdefa6f9383f8c9735f9510f70f228d299479a257c1a2d3c10d1f47cc1a055
'''.replace('\n', ''), 16)
q = int('''
e5b537e60922d57a763918a5b1e8af1bc07c85fefea11e8179f2a9ee6cf7c611
7d0eba7963617035cf1ddb1f0cc858d70890a76990f96adb29ea8b0403f869cd
be51b76f06c25a9319ecd04366f846338fc1f81ae05f143940039bfbbc4de953
b933c89e74fe62485157d7a3b31993915808a4b95bb768f369818c10edfa561e
3530c999c33ef62a4466ec67622cc12525cf0ea3d402931d16ef115acc172641
a63037190ba04931d3caa2ef861ee7f277647844f8a7f94569f06cea32badb02
82355467cec0bdbdff5e7cd837ffce048925280ab92a9560c1cd6bd309239d7e
72b298af5ad81d27ee9adf7143185815bdadfa21296833149748ed2f55343533
'''.replace('\n', ''), 16)
e = 65537

n = b
phi = (p - 1) * (q - 1)
d = multiplicative_inverse(e, phi)

m = pow(m, d, b)

m = hex(m)[2:]
def split_by_n( seq, n ):
    while seq:
        yield seq[:n]
        seq = seq[n:]
m = list(split_by_n(m, 32))
print(m)