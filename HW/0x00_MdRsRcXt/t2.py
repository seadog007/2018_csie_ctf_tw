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
K = hex(a).encode('ascii')

m = [174, 174, 10, 229, 211, 105, 124, 7, 121, 109, 74, 237, 176, 180, 124, 74, 38, 202, 250, 134, 107, 46, 173, 255, 229, 157, 33, 79, 55, 122, 156, 61, 60, 228, 108, 233, 4, 204, 248, 17, 115, 206, 83, 175, 163, 207, 53, 180, 109, 34, 124, 239, 138, 210, 185, 17, 113, 220, 226, 192, 175, 200, 254, 44, 68, 163, 207, 146, 47, 69, 102, 224, 34, 64, 215, 177, 75, 90, 209, 176, 200, 185, 28, 176, 249, 178, 229, 4, 54, 208, 85, 196, 193, 151, 53, 148, 57, 94, 128, 227, 99, 213, 176, 179, 164, 49, 66, 83, 193, 164, 198, 141, 166, 3, 111, 196, 42, 52, 137, 39, 137, 25, 55, 101, 254, 143, 154, 161, 164, 91, 228, 217, 210, 191, 216, 116, 126, 223, 34, 25, 38, 99, 134, 252, 251, 228, 153, 86, 80, 20, 161, 48, 106, 241, 94, 223, 46, 71, 30, 120, 85, 189, 15, 141, 248, 44, 255, 186, 171, 66, 215, 213, 82, 55, 206, 153, 77, 234, 121, 188, 135, 21, 28, 139, 119, 218, 198, 102, 75, 254, 174, 48, 179, 199, 178, 39, 7, 108, 130, 45, 151, 214, 250, 26, 115, 191, 85, 42, 178, 38, 63, 102, 121, 173, 38, 239, 23, 171, 220, 240, 135, 140, 211, 142, 252, 31, 96, 65, 130, 5, 20, 72, 202, 252, 77, 51, 146, 176, 150, 191, 250, 212, 130, 56, 241, 255, 141, 38, 171, 220, 58, 148, 37, 9, 242, 25, 227, 24, 40, 24, 93, 51, 205, 239, 85, 147, 92, 150, 220, 220, 201, 66, 28, 145, 153, 211, 217, 37, 172, 115, 0, 55, 138, 194, 241, 98, 145, 66, 29, 112, 202, 4, 142, 136, 214, 190, 110, 8, 40, 66, 109, 226, 109, 232, 195, 122, 94, 174, 163, 253, 213, 38, 58, 181, 72, 84, 2, 60, 224, 220, 78, 88, 234, 73, 5, 24, 174, 14, 99, 113, 0, 242, 1, 251, 253, 207, 99, 201, 182, 186, 208, 159, 1, 228, 247, 39, 226, 167, 215, 166, 113, 151, 84, 182, 206, 4, 120, 233, 119, 223, 78, 253, 6, 109, 115, 89, 165, 82, 203, 80, 35, 251, 212, 246, 98, 225, 169, 16, 195, 190, 163, 217, 172, 23, 46, 231, 207, 199, 252, 246, 3, 130, 254, 94, 130, 119, 114, 54, 35, 184, 56, 14, 120, 17, 140, 10, 89, 26, 55, 149, 152, 141, 124, 190, 66, 69, 153, 244, 235, 36, 161, 17, 119, 239, 144, 188, 4, 186, 255, 3, 80, 61, 205, 24, 151, 68, 139, 211, 109, 119, 11, 194, 57, 193, 30, 230, 103, 40, 196, 189, 237, 212, 190, 187, 33, 93, 64, 47, 207, 54, 143, 226, 212, 47, 87, 43, 73, 229, 187, 190, 96, 12, 99, 192, 33, 6, 77, 29, 230, 109, 229, 174, 30, 173, 215, 60, 252, 78, 69, 3, 202, 98, 139, 16, 12, 51, 164, 202, 215, 24, 168, 252, 130, 157, 160, 211, 136, 50, 105, 8, 145, 13]

S = list(range(256))
j = 0
for i in range(256):
    j = (j + S[i] + K[i % len(K)]) % 256
    S[i], S[j] = S[j], S[i]
j = 0
for k in range(len(m)):
    i = (k + 1) % 256
    j = (j + S[i]) % 256
    S[i], S[j] = S[j], S[i]
    m[k] ^= S[(S[i] + S[j]) % 256]

print(m)

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
            print(i, j)
            break
            
print(m)