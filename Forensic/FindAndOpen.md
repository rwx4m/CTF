# FindAndOpen

**Category:** Forensic

## Description
>Someone might have hidden the password in the trace file. Find the key to unlock zip file.

---

```bash
┌──(rwx4m㉿Home)-[~/Downloads/challenge]
└─$ tree          
.
├── dump.pcap
└── flag.zip

1 directory, 2 files
```
```bash
┌──(rwx4m㉿Home)-[~/Downloads/challenge]
└─$ zipinfo flag.zip                 
Archive:  flag.zip
Zip file size: 231 bytes, number of entries: 1
-rw-r--r--  3.0 unx       45 TX stor 23-Mar-16 09:40 flag
1 file, 45 bytes uncompressed, 45 bytes compressed:  0.0%
```
------------

Disini terlihat seperti base64.
![Screenshot 2025-01-16 005920](https://github.com/user-attachments/assets/bbb0206d-553a-407c-824d-fad26643d0c4)

copy hex kemudian convert ke base64 menggunakan Cyberchef:

## Potongan Pertama:

HEX
>564768706379427063794230614755676332566a636d56304f69427761574e76513152476531497a4e45524a546b64665445394c5a46383d

Base64
>VGhpcyBpcyB0aGUgc2VjcmV0OiBwaWNvQ1RGe1IzNERJTkdfTE9LZF8=

Hasil:
> ....flag....

![Screenshot 2025-01-16 010245](https://github.com/user-attachments/assets/f941d6a9-362b-4018-aa7b-6a1c6433e438)


## Potongan Kedua:
Hasil flag Potongan pertama digunakan sebagai kata sandi untuk membuka file zip yang memiliki file yang berisi flag lengkap yang dibutuhkan sebagai jawaban akhir.

*Silahkan dicoba dan mempelajarinya*
