def check():
    #lambda encryp/decrypt
    tst = lambda x: bytes(((i + (13371337 * (2024 - i) * (2025 - i))) % 199) + ((i + 1) % 25) for i in x)

   #user input
    inp = input('Welcome to warmup, no XOR RE here and please give me the flegg >> ')

    #cek input sesuai dengan byte ini
    if tst(inp.encode()) != b'\x11\x08C~49?\x92\x984?$\x92\x1d4n~$\x92\x1d4n\x19$\x92\x1d4~9\x1d4\x089\x1dC~\xc0\x1d\\?$9\x91':
        print('Wrong!')
    else:
        print('Correct! See you in the next elimination round :>')
    return 0
check()