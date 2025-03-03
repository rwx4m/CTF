# RSA Broadcast Attack
## Deskripsi
Dalam tantangan ini, kita diberikan beberapa ciphertext yang telah dienkripsi menggunakan algoritma RSA dengan exponent `e=5` dan modulus yang berbeda-beda. Tugas kita adalah mendekripsi pesan dan mendapatkan flag.

----

## Analisis
RSA umumnya aman karena modulus yang besar membuat faktorisasi sulit. Namun, dalam kasus ini, ada celah keamanan yang dapat dimanfaatkan:
- Semua ciphertext dienkripsi dengan eksponen yang sama (e=5),
- Setiap ciphertext dienkripsi dengan modulus yang berbeda,
- Jika sebuah pesan yang sama dienkripsi dengan beberapa modulus berbeda, maka kita dapat menggunakan Chinese Remainder Theorem (CRT) untuk mendapatkan kembali nilai plaintext,
- Setelah mendapatkan nilai hasil CRT, kita cukup menghitung akar ke-5 dari nilai tersebut untuk mendapatkan plaintext,
Teknik ini dikenal sebagai RSA Broadcast Attack dan dapat dieksploitasi ketika eksponen kecil digunakan bersama dengan beberapa modulus.
----
## Solusi
### Terdapat tiga pasangan ciphertext dan modulus dalam format heksadesimal.
```bash
ciphertexts = [
    int("17425F95789A43D2C6A214355F70BFB1C7DBD5A53EAB544F3CD21BC8FB2BC56051FDD6AC390D702CAD26BC1B0D3F95C5F90437D7177D408B93BEE907BBA21C37C0707C3F51EE56105CA7BBC2297A3E811F6C7F5EC1E6158F4ED12E03FD64B99E38060A4E8FD209BB8F444ACE3DADAF9A3249C9FEA4EA3DE35CD7B6548700B56E", 16),
    int("A8EF3E9C8B0BE3A012EFE25B2A2A34CE7855BB93E5FF62CFE92FAA74C4A8988A43D50B72ADD1DFF7AE33B93CC7F1056A787183396C23278E892C31BD4F585CE6790AE54E32EFBA72569B77C8D718097AF5E08A53C4BBFB0010414B3D8493BE380BA7DFED723EF742E3064926D3D56731BAA3736E8A74B036E5CC3AA75D46820", 16),
    int("84C95E7079E10D93205D870358418F535C1B9DA7820EFCFD0029CA16D870CFE5078B0CB066A3B040B0A8BAF5CAC10F3074EDCF13E1E322354CA736F64B4F3789E4C132D3BC714E9277A39C8F23D29CF0EF8B0A3951212E024DDEA170BDEBA957696A9C58CB109EC162D2B4B84FCB256293AB9FBBCB37CFCD760DB1ADCBCFB6C3", 16)
]

moduli = [
    int("77831FF4F9FCE4F681199D756CF9E5974B4B569480605318290F91DA0EE1CA6AC16CABA369A817E1B5F318B80D803794AA38732B10F389EBB7D8ADAB6E170D492D6D9F35528F5FE7D4A4F5DC66D0CD6563DA1C80C844701165D8C8606AEDF9A11A9F7DFB4A63D5189B7760562FA777A82EF096B514895566B9A546328F3D2589", 16),
    int("AC022DBF7012CB398B2C6230BC893B8F0423C333959AFD3D65A45FB148B00B6ECB5D054156717CDB61D4A29BA2723D7D33B584FBFBBDA5D71401EF4E885E82F8E5646CFA7803959CB8F117C11FFF4CE974B71EB0F8A3B2F10C4CC03E142125287D953755C95DA11A6F5AA897388DB29653319A199F21EB47D39611E7988E289D", 16),
    int("90782D474750603F537BACEF31B66AE2918E5B1939B6D3EFF20BC4FA411689535D10D22085849FEA67380A754C10DD34032F12D31C83E8BD92BE06F3609293036C9A775C9B81C6246E5DC385604E229EED522A15B358807AB11F062C91A9B88212DAADF693A4327F0C726FE665EB9CC60761740EB995F6DB4BF2507AF003D2E5", 16)
]

e = 5
```
### Menggunakan Chinese Remainder Theorem (CRT)
Karena kita memiliki tiga ciphertext yang dienkripsi dengan modulus yang berbeda tetapi memiliki plaintext yang sama, kita dapat menggunakan Chinese Remainder Theorem (CRT) untuk menggabungkan informasi ini dan mendapatkan satu nilai yang ekuivalen dengan plaintext dalam modulo gabungan dari semua modulus.

CRT membantu menemukan nilai unik yang memenuhi semua kongruensi dari ciphertext terhadap modulus masing-masing.

### Menghitung Akar Kelima
Setelah mendapatkan nilai dari CRT, langkah selanjutnya adalah mengambil akar ke-5 dari nilai tersebut. Karena plaintext telah dienkripsi menggunakan eksponen 5, kita cukup menghitung akar pangkat lima dari hasil CRT untuk mendapatkan nilai asli dari plaintext.
```bash
import gmpy2
from gmpy2 import iroot
from sympy.ntheory.modular import crt

# 1. Gunakan CRT untuk mendapatkan nilai gabungan
M, _ = crt(moduli, ciphertexts)

# 2. Ambil akar ke-5
plaintext, exact = iroot(M, e)

# 3. Konversi hasil ke string jika akar tepat
if exact:
    flag = plaintext.to_bytes((plaintext.bit_length() + 7) // 8, 'big')
    print(f"Flag: {flag.decode()}")
else:
    print("Gagal mendapatkan flag.")
```
---
## Kesimpulan

- RSA Broadcast Attack terjadi ketika plaintext yang sama dienkripsi dengan beberapa modulus berbeda tetapi memiliki eksponen kecil.
- Dengan Chinese Remainder Theorem (CRT), kita bisa mendapatkan nilai gabungan.
- Setelah itu, cukup menghitung akar eksponen untuk mendapatkan plaintext.
- Ini menunjukkan pentingnya memilih eksponen yang lebih besar atau menerapkan padding dalam implementasi RSA untuk mencegah serangan ini.
