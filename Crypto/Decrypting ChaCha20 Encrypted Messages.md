# Decrypting ChaCha20 Encrypted Messages
## Deskripsi
Tantangan ini mengharuskan untuk mendekripsi pesan terenkripsi yang berasal dari sistem komunikasi rahasia musuh. Terdapat file source.py yang digunakan untuk mengenkripsi pesan serta hasil enkripsi dalam out.txt. Dengan menggunakan metode kriptografi yang sesuai, proses membalikkan enkripsi dapat dilakukan untuk memperoleh FLAG yang disembunyikan.

----

### Teori
ChaCha20 adalah algoritma enkripsi stream cipher. Algoritma ini didesain sebagai alternatif yang lebih cepat dan aman dibandingkan RC4. ChaCha20 menggunakan kunci 256-bit dan nonce 96-bit (12 byte) untuk menghasilkan keystream, yaitu pseudorandom byte sequence yang akan digunakan untuk enkripsi.

ChaCha20 mengenkripsi plaintext dengan cara melakukan XOR antara plaintext dan keystream. Jika dua plaintext dienkripsi dengan keystream yang sama, XOR antara kedua ciphertext akan menghasilkan XOR dari dua plaintext, sehingga memungkinkan serangan Known Plaintext Attack (KPA). Oleh karena itu, nonce harus berbeda setiap enkripsi untuk mencegah keystream yang sama digunakan berulang kali. Jika nonce diulang, penyerang dapat memperoleh keystream dengan membandingkan plaintext yang diketahui dengan ciphertext.

----

### Analisis
Source code (source.py) menggunakan algoritma ChaCha20, sebuah cipher stream modern yang digunakan untuk enkripsi data. Berikut adalah poin-poin penting dari kode ini:

#### Enkripsi menggunakan ChaCha20
```bash
from Crypto.Cipher import ChaCha20
from secret import FLAG
import os

def encryptMessage(message, key, nonce):
    cipher = ChaCha20.new(key=key, nonce=iv)
    ciphertext = cipher.encrypt(message)
    return ciphertext
```
- Fungsi ini menerima plaintext, kunci (key), dan nonce (iv)
- Objek cipher dibuat dengan ChaCha20.new()
- Pesan dienkripsi menggunakan metode encrypt()

#### Pembuatan Kunci dan Nonce
```key, iv = os.urandom(32), os.urandom(12)```

- Kunci 32-byte dan nonce 12-byte dibuat secara acak.

#### Proses Enkripsi dan Penyimpanan Data
```bash
encrypted_message = encryptMessage(message, key, iv)
encrypted_flag = encryptMessage(FLAG, key, iv)
data = iv.hex() + "\n" + encrypted_message.hex() + "\n" + encrypted_flag.hex()
writeData(data)
```
- Pesan yang diketahui (plaintext) dienkripsi menggunakan kunci dan nonce yang sama dengan FLAG.
- Hasil enkripsi disimpan dalam out.txt.

#### Analisis Data Enkripsi (out.txt)
Isi dari file out.txt:
```
c4a66edfe80227b4fa24d431
7aa34395a258f5893e3db1822139b8c1f04cfab9d757b9b9cca57e1df33d093f07c7f06e06bb6293676f9060a838ea138b6bc9f20b08afeb73120506e2ce7b9b9dcd9e4a421584cfaba2481132dfbdf4216e98e3facec9ba199ca3a97641e9ca9782868d0222a1d7c0d3119b867edaf2e72e2a6f7d344df39a14edc39cb6f960944ddac2aaef324827c36cba67dcb76b22119b43881a3f1262752990
7d8273ceb459e4d4386df4e32e1aecc1aa7aaafda50cb982f6c62623cf6b29693d86b15457aa76ac7e2eef6cf814ae3a8d39c7
```
Data ini terdiri dari:
- Nonce (IV): c4a66edfe80227b4fa24d431
- Ciphertext dari pesan yang diketahui (plaintext diketahui)
- Ciphertext dari FLAG yang harus didekripsi
----
### Strategi Dekripsi
Karena memiliki plaintext asli dari pesan pertama, saya dapat melakukan serangan Known Plaintext Attack (KPA) terhadap ChaCha20. Stream cipher seperti ChaCha20 menghasilkan keystream yang XOR dengan plaintext untuk menghasilkan ciphertext. Oleh karena itu, saya dapat:
##### Menemukan keystream dengan plaintext yang diketahui
- XOR antara ciphertext dan plaintext akan menghasilkan keystream.
##### Menggunakan keystream yang sama untuk mendekripsi FLAG
- XOR antara ciphertext FLAG dan keystream akan mengembalikan plaintext FLAG.

### Solusi
```bash
from Crypto.Cipher import ChaCha20
import binascii

# Data dari out.txt
iv = bytes.fromhex("c4a66edfe80227b4fa24d431")
ciphertext_message = bytes.fromhex("7aa34395a258f5893e3db1822139b8c1f04cfab9d757b9b9cca57e1df33d093f07c7f06e06bb6293676f9060a838ea138b6bc9f20b08afeb73120506e2ce7b9b9dcd9e4a421584cfaba2481132dfbdf4216e98e3facec9ba199ca3a97641e9ca9782868d0222a1d7c0d3119b867edaf2e72e2a6f7d344df39a14edc39cb6f960944ddac2aaef324827c36cba67dcb76b22119b43881a3f1262752990")
ciphertext_flag = bytes.fromhex("7d8273ceb459e4d4386df4e32e1aecc1aa7aaafda50cb982f6c62623cf6b29693d86b15457aa76ac7e2eef6cf814ae3a8d39c7")

plaintext_message = b"Our counter agencies have intercepted your messages and a lot "
plaintext_message += b"of your agent's identities have been exposed. In a matter of "
plaintext_message += b"days all of them will be captured"

# Mendapatkan keystream
keystream = bytes([a ^ b for a, b in zip(ciphertext_message, plaintext_message)])

# Mendekripsi FLAG
decrypted_flag = bytes([a ^ b for a, b in zip(ciphertext_flag, keystream)])
print("FLAG:", decrypted_flag.decode())
```
----
### Kesimpulan
- Serangan berhasil dilakukan dengan Known Plaintext Attack.
- FLAG berhasil didekripsi dengan XOR sederhana terhadap ciphertext.
- Tantangan ini mengajarkan pentingnya penggunaan nonce yang unik dalam stream cipher.
