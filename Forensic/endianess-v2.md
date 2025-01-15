## Forensic Challenge: endianess-v2

### Description:
Here’s a file that was recovered from a 32-bits system that organized the bytes in a weird way. We're not even sure what type of file it is. Download it here and see what you can get out of it.

---

## Analysis

Setelah mendownload file **challengefile**, memulai dengan memeriksa file ini menggunakan beberapa alat analisis standar.

### 1. **Menentukan Jenis File**

Pertama, menggunakan perintah `file` untuk mengetahui tipe file dari `challengefile`:

```bash
┌──(rwx4m㉿Home)-[~/Downloads]
└─$ file challengefile                                  
challengefile: data
```
Dari hasil ini, tidak ada informasi pasti mengenai tipe file ini.

### 2. Memeriksa Metadata dengan ExifTool
Untuk melihat apakah file ini memiliki metadata yang berguna, saya menggunakan `exiftool`:
```bash
┌──(rwx4m㉿Home)-[~/Downloads]
└─$ exiftool challengefile
ExifTool Version Number         : 13.00
File Name                       : challengefile
Directory                       : .
File Size                       : 3.4 kB
File Modification Date/Time     : 2025:01:15 11:28:52+07:00
File Access Date/Time           : 2025:01:15 11:29:18+07:00
File Inode Change Date/Time     : 2025:01:15 11:28:53+07:00
File Permissions                : -rw-rw-r--
Warning                         : Processing JPEG-like data after unknown 1-byte header
```
Dari metadata ini, terlihat bahwa file ini mengandung data yang menyerupai format JPEG. Bagian `warning` menyebutkan `Processing JPEG-like data after unknown 1-byte header`, yang menunjukkan bahwa ada kemungkinan file ini berisi data JPEG yang rusak..

### 3. Melihat Isi File dengan xxd
Selanjutnya, menggunakan `xxd` untuk melihat isi file dalam format heksadesimal:

```bash
┌──(rwx4m㉿Home)-[~/Downloads]
└─$ xxd challengefile|head 
00000000: e0ff d8ff 464a 1000 0100 4649 0100 0001  ....FJ....FI....
00000010: 0000 0100 4300 dbff 0606 0800 0805 0607  ....C...........
00000020: 0907 0707 0c0a 0809 0b0c 0d14 1219 0c0b  ................
00000030: 1d14 0f13 1d1e 1f1a 201c 1c1a 2027 2e24  ........ ... '.$
00000040: 1c23 2c22 2937 281c 3431 302c 271f 3434  .#,")7(.410,'.44
00000050: 3238 3d39 3433 2e3c 00db ff32 0909 0143  28=943.<...2...C
00000060: 0c0b 0c09 180d 0d18 211c 2132 3232 3232  ........!.!22222
00000070: 3232 3232 3232 3232 3232 3232 3232 3232  2222222222222222
00000080: 3232 3232 3232 3232 3232 3232 3232 3232  2222222222222222
00000090: 3232 3232 3232 3232 3232 3232 c0ff 3232  222222222222..22
```
Pada byte pertama, `e0ff d8ff` yang tampaknya tidak sesuai dengan standar file JPEG yang seharusnya `ff d8 ff`. Terlihat juga bahwa urutan byte file ini terbalik atau salah susun.

## Endianness Swap
Karena file ini tampaknya memiliki masalah pada urutan byte, saya akan mencoba untuk membalikkan byte-nya (swap endianess).
Saya akan membalikkan byte setiap 4 byte, yang berarti 4 byte pertama akan dikelompokkan, membalikkan urutannya, dan melanjutkan ke kelompok berikutnya.

CONTOH:
Misalnya saya memiliki data heksadesimal berikut dalam file:

`00 01 02 03 04 05 06 07 08 09 0A 0B`

Saya ingin membalik urutan byte pada setiap kelompok 4 byte pertama lalu membalikkannya:

`Sebelum: 00 01 02 03 | 04 05 06 07 | 08 09 0A 0B`

`Sesudah: 03 02 01 00 | 07 06 05 04 | 0B 0A 09 08`

Maka,

`Sebelum: e0 ff d8 ff | 46 4a 10 00 ...dst`

`Sesudah: ff d8 ff e0 | 00 10 4a 46 ...dst.`

### Penyelesaian
Saya menggunakan `Cyberchef` untuk membalikkan urutan byte dan menyimpannya ke dalam file format `jpg`:

![Screenshot 2025-01-15 115035](https://github.com/user-attachments/assets/15922fa2-50b8-4054-a379-1b29900d17a3)

Setelah melakukan ini, save file format 'jpg' dan flag akan terlihat pada file gambar tersebut.

```bash
┌──(rwx4m㉿Home)-[~/Downloads]
└─$ xxd Untitled.jpeg | head
00000000: ffd8 ffe0 0010 4a46 4946 0001 0100 0001  ......JFIF......
00000010: 0001 0000 ffdb 0043 0008 0606 0706 0508  .......C........
00000020: 0707 0709 0908 0a0c 140d 0c0b 0b0c 1912  ................
00000030: 130f 141d 1a1f 1e1d 1a1c 1c20 242e 2720  ........... $.' 
00000040: 222c 231c 1c28 3729 2c30 3134 3434 1f27  ",#..(7),01444.'
00000050: 393d 3832 3c2e 3334 32ff db00 4301 0909  9=82<.342...C...
00000060: 090c 0b0c 180d 0d18 3221 1c21 3232 3232  ........2!.!2222
00000070: 3232 3232 3232 3232 3232 3232 3232 3232  2222222222222222
00000080: 3232 3232 3232 3232 3232 3232 3232 3232  2222222222222222
00000090: 3232 3232 3232 3232 3232 3232 3232 ffc0  22222222222222..
```
Sekarang, byte pertama adalah `ffd8`, yang merupakan Standar untuk file JPEG yang valid.

*Silahkan, jika ingin mencoba dan pelajari sendiri*
