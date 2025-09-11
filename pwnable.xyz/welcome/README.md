# welcome

The challenge requires you to look at the disassembly to understand the bug.

The binary leaks a heap pointer (`plVar1`) and lets us choose the size of a
subsequent `malloc`:

```sh
Welcome.
Leak: 0x7ffff7f45010
Length of your message:
```

With the right size we can make `malloc` fail, turning the returned pointer (`__buf`) into NULL,
letting us overwrite a byte at an arbitrary heap address.

Why?

`malloc` returns NULL when the requested size exceeds `PTRDIFF_MAX` - see `man malloc`:

```
Attempting to allocate more than PTRDIFF_MAX bytes is considered an error, as an object that large 
could cause later pointer subtraction to overflow.
```

So the line:

```
__buf = malloc(local_28); // `local_28` (size) comes from the value we supply to stdin
```

makes `__buf` equal to 0 if we supply a huge value for `local_28`.

Going back earlier, the program allocates a large chunk and leaks its address:

```
plVar1 = malloc(0x40000); // leaks this address
*plVar1 = 1; // <- checked later
```

Before printing the flag, it performs:

```
if (*plVar1 == 0) {
  system("cat /flag");
}
```

**Note: the flag is expected at root `/flag`.**

So our goal is to turn `*plVar1` from 1 to 0.

Right after the failing `malloc`, the code writes 0 to:

```
*(__buf + (local_28 - 1)) = 0;
```

If `__buf == 0`, that writes 0 to address `local_28 – 1`.

If we make `local_28 = plVar1 + 1` (remember `plVar1` is leaked), the destination is exactly
`plVar1` (since `(plVar1 + 1) – 1 == plVar1`).

The assembly for the above is:

```
MOV                        byte ptr [RBP + RDX*0x1 + -0x1],0x0
```

You can test the value in GDB with `x/x $rbp + $rdx - 1` to ensure it's the leaked address.

So in order:

1. Read the leaked `plVar1`
2. Send `size = plVar1 + 1` as our `malloc` size

* `malloc` fails -> `__buf = 0`
* The program writes 0 to address `plVar1`

3. `*plVar1` is now 0; the flag check passes
