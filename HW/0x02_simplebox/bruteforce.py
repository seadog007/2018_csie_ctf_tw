from string import ascii_letters

cipher_letters = '+><[]-,.'
trans = str.maketrans('mBaFxbOo', cipher_letters)
f = open('data.decrypt', 'r')
text_to_cipher = f.read()
f.close()

print(text_to_cipher.translate(trans))
