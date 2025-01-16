# hideme
*Category:* Forensic

## Description
Every file gets a flag. The SOC analyst saw one image been sent back and forth between two people. They decided to investigate and found out that there was more than what meets the eye.

---

```bash
┌──(rwx4m㉿Home)-[~]
└─$ file flag.png     
flag.png: PNG image data, 512 x 504, 8-bit/color RGBA, non-interlaced
```
```bash                                                                                                         
┌──(rwx4m㉿Home)-[~]
└─$ exiftool flag.png     
ExifTool Version Number         : 13.00
File Name                       : flag.png
Directory                       : .
File Size                       : 43 kB
File Modification Date/Time     : 2023:03:16 10:16:12+07:00
File Access Date/Time           : 2025:01:16 11:05:05+07:00
File Inode Change Date/Time     : 2025:01:16 11:04:55+07:00
File Permissions                : -rw-rw-r--
File Type                       : PNG
File Type Extension             : png
MIME Type                       : image/png
Image Width                     : 512
Image Height                    : 504
Bit Depth                       : 8
Color Type                      : RGB with Alpha
Compression                     : Deflate/Inflate
Filter                          : Adaptive
Interlace                       : Noninterlaced
Warning                         : [minor] Trailer data after PNG IEND chunk
Image Size                      : 512x504
Megapixels                      : 0.258
```
Terdapat peringatan minor bahwa ada data tambahan setelah bagian akhir file, yang bisa menjadi indikasi sesuatu yang tidak biasa (misalnya data tersembunyi)

```bash                                                                                                         
┌──(rwx4m㉿Home)-[~]
└─$ xxd flag.png| tail                                  
0000a720: 1000 ed41 0000 0000 7365 6372 6574 2f55  ...A....secret/U
0000a730: 5405 0003 8f78 1264 7578 0b00 0104 0000  T....x.dux......
0000a740: 0000 0400 0000 0050 4b01 021e 0314 0000  .......PK.......
0000a750: 0008 003a 1070 5667 4523 b535 0b00 00d0  ...:.pVgE#.5....
0000a760: 0b00 000f 0018 0000 0000 0000 0000 00a4  ................
0000a770: 8141 0000 0073 6563 7265 742f 666c 6167  .A...secret/flag
0000a780: 2e70 6e67 5554 0500 038f 7812 6475 780b  .pngUT....x.dux.
0000a790: 0001 0400 0000 0004 0000 0000 504b 0506  ............PK..
0000a7a0: 0000 0000 0200 0200 a200 0000 bf0b 0000  ................
0000a7b0: 0000                                     ..
```
### HexDump
Temuan:
- `secret/flag.png`: Indikasi bahwa file `flag.png` mungkin menyimpan file lain (seperti tersembunyi).
- `PK`: Ini adalah signature file `ZIP`, menandakan file mungkin mengandung data `ZIP` yang disematkan.

### Analisis Detail
Pada bagian `hex dump`, terlihat string `secret/flag.png` dan struktur file `ZIP (PK)`, yang menunjukkan adanya file tersembunyi dalam file gambar ini.
Maka, Trailer data (Warning di ExifTool) kemungkinan berisi file `ZIP` yang bisa diekstrak.

```bash                                                                                                         
┌──(rwx4m㉿Home)-[~]
└─$ binwalk -e flag.png         

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
41            0x29            Zlib compressed data, compressed
39739         0x9B3B          Zip archive data, at least v1.0 to extract, name: secret/
39804         0x9B7C          Zip archive data, at least v2.0 to extract, compressed size: 2869, uncompressed size: 3024, name: secret/flag.png
```

Masuk ke direktori: `/_flag.png.extracted/secret`
Akan ada file `flag.png` pada direktori `secret` yang dapat dibuka dengan menggunakan image viewer untuk mendapatkan flag.
