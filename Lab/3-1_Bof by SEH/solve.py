flag = ['75', '7F', '72', '74', '48', '60', '0', '7B', '6C', '12', '60', '6C', '76', '7', '69', '6A', '6C', '67', '3', '6C', '7B', '7', '70', '78', '6C', '4E']
for i in range(len(flag)):
        flag[i] = chr(int(flag[i], 16) ^ 0x33)

print(''.join(flag))
