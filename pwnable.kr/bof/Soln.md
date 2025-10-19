# Soln

Per the source code, I have to overflow the buffer and change `0xdeadbeef` on the stack to
`0xcafebabe`.

The stack canary is enabled, but that sites above the local variables on the stack (this is x86
calling convention).

To run the PoC, local forward port 90:

`ssh -L9000:127.0.0.1:9000 bof@pwnable.kr -p2222`

The password is "guest".
