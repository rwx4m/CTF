import string

#Fungsi enkripsi
def enkripsi(a):
    return bytes(((i + (13371337 * (2024 - i) * (2025 - i))) % 199) + ((i + 1) % 25) for i in a)

#Target bytes
target = b'\x11\x08C~49?\x92\x984?$\x92\x1d4n~$\x92\x1d4n\x19$\x92\x1d4~9\x1d4\x089\x1dC~\xc0\x1d\\?$9\x91'

# Fungsi rekursif untuk brute force
def cari_flag(flag_awal, index):
    if index == len(target):
        return flag_awal
    for x in string.ascii_letters + string.digits + "_{}":
        kemungkinan = flag_awal + x
        if enkripsi(kemungkinan.encode())[:index+1] == target[:index+1]:
            result = cari_flag(kemungkinan, index + 1)
            if result:
                return result
    return None

#Pencarian Flag
flag = cari_flag("", 0)
print("Flag is:", flag)
