import hashlib
import sys
import binascii
import struct
import string

A = b'''
bc69f315c01224ca6778d124281a31f5ffaf7e97ef666f349fb6c6d390e1bd2b
4ece1d956c577f57920ff9a082b6855ea9a99914f21491b4012cad5aecb93c44
c0b1cabd5a7573b53fb6b4a3b7025a19a40c8ced23b93d4d80f189f2c9e94360
cd41bc81dba40b782011adcd4359d4ef1af2d6d71a8c1352090d0b95b84d11e6
c619c27a45db86b76aeb4fa3b4fff12783e20a40fe25bab19ea9221a0c08d960
9b0df26bd6ab5c4b0a26a269407bbdbc630c4e2609c1980cb0ab545097325f7e
e2a37bbdfc3f08b166e50cbe89daabc197385a0d7b59e5b5e1ebb4ebff499959
995611f14faec3531defbbce4c39cd0750fc46699850b82adcc11f31de7172e7
1d45ab686016f181b82c4275ea024d2c68bb073cd0121857cad4cf4846c474ea
a4b970ec1c0280cf6ffc7d6baab06338edef2b00e4201a22798d07ade14fdb18
1959db018acab1cc5ff742d66bb6144e2e568491715c19a985e9592dcdcf93ca
4793a61becb8ead82110b7db361bd2ed11c19c9d6dc30c2d5925cdd7c3a688c5
4ceb08129fcabdf4ac51fcfaeb24647d09c1dff6e427f51b90c9d40902e0f0c2
b28e0dc8f1d382f1bc282629fb082321651019a62d9341e9c4be1c415cbd8397
fdca24617d48127d2f21b9d29800c25876beff87dc6cf6677856e4e8787d8bdb
6219c9a746c64ef18236f12a9137511e84c1df56a98d7e030037579b3f34522d
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

########################
###########TEA##########
########################
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

########################
###########RC4##########
########################
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

########################
###########RSA##########
########################
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


########################
###########HASH#########
########################
def md5(s):
    return hashlib.md5(s.encode('ascii')).hexdigest()

m = hex(m)[2:]
def split_by_n( seq, n ):
    while seq:
        yield seq[:n]
        seq = seq[n:]
m = list(split_by_n(m, 32))

table = []
for i in string.printable:
    table.append({'char': i, 'hash': md5(i)})

for i in range(len(m)):
    for j in table:
        if m[i] == j['hash']:
            m[i] = j['char']
            break

print(''.join(m))
