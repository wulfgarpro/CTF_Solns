# TryOverFlowMe1

The challenge provides example code:

```c
int main(){
    setup();
    banner();
    int admin = 0;
    char buf[0x10];

    puts("PLease go ahead and leave a comment :");
    gets(buf);

    if (admin){
        const char* filename = "flag.txt";
        FILE* file = fopen(filename, "r");
        char ch;
        while ((ch = fgetc(file)) != EOF) {
            putchar(ch);
    }
    fclose(file);
    }

    else{
        puts("Bye bye\n");
        exit(1);
    }
}
```

It's a basic stack buffer overflow - set `admin` to 1 to get the flag.

The challenge is so basic we don't have to be smart to overwrite `admin` - just provide a long
enough buffer, e.g. 50.

I decided to find the exact size `44` takes us to `admin` on the stack. Then we write 1 to overwrite
`admin` and get the flag.
