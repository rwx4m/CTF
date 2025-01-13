# Retrivial

**Category:** Forensic

## Description
>A colleague of mine discovered a file transfer service masquerading as a DNS server. From there, he retrieved a particular file that could be regarded as a confidential asset
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Pendahuluan
Tulisan ini bertujuan untuk menganalisis file pcap yang mencurigakan. Dalam file ini, terdapat komunikasi melalui protokol DNS yang mengindikasikan adanya penyembunyian data menggunakan teknik tunneling. Proses analisis dilakukan untuk mengidentifikasi file yang sedang ditransfer dan teknik yang digunakan dalam eksfiltrasi data.

## Analisis Awal:

![Screenshot 2025-01-13 200946](https://github.com/user-attachments/assets/c827b0e8-bcc6-447e-8ad4-13ed91074de4)
![Screenshot 2025-01-13 200904](https://github.com/user-attachments/assets/6a7eab4c-cfdb-4d40-b0b7-9d360eb48caa)

Saat membuka file pcap, terlihat bahwa pada frame pertama dan kedua terdapat komunikasi menggunakan protokol DNS antara dua IP yang juga ditandai sebagai malformed. Hal ini menunjukkan bahwa data yang dikirimkan melalui DNS mungkin tidak sesuai dengan format DNS standar. Ini bisa menjadi indikasi adanya manipulasi atau enkapsulasi data lain di dalamnya. Jika data yang dikirim tidak mengikuti pola DNS biasa, kemungkinan besar ini merupakan penggunaan protokol lain yang lebih sederhana.

Melalui pemeriksaan lebih lanjut, ditemukan informasi dalam format ASCII yang mencantumkan nama "flag.png" dan "blksize.32". Ini tampaknya mengindikasikan informasi terkait file atau blok data yang akan ditransfer. Penyembunyian data dalam DNS adalah teknik tunneling yang sering digunakan untuk eksfiltrasi data atau pengiriman payload yang tersembunyi.

Selain itu, saya menemukan tanda-tanda yang mengonfirmasi bahwa file yang sedang ditransfer adalah sebuah file PNG. Berikut adalah bukti yang ditemukan dalam byte stream:
```
00000542  00 03 00 01 89 50 4e 47  0d 00 0d 0a 1a 0d 0a 00   .....PNG ........
00000552  00 00 0d 00 49 48 44 52  00 00 05 be 00 00 05 be   ....IHDR ........
00000562  01 00 00 00                                        ....
00000566  00 03 00 01 89 50 4e 47  0d 00 0d 0a 1a 0d 0a 00   .....PNG ........
00000576  00 00 0d 00 49 48 44 52  00 00 05 be 00 00 05 be   ....IHDR ........
00000586  01 00 00 00                                        ....
```
Byte 89 50 4e 47 yang muncul berulang-ulang adalah tanda bahwa file yang sedang diunduh adalah file PNG, yang diawali dengan signature khas file PNG (89 50 4e 47 0d 0a 1a 0a). Ini mengonfirmasi bahwa file tersebut adalah gambar PNG.

```
00000DFA  00 03 00 02 00 80 60 0b  d5 00 00 08 01 49 44 41   ....... .....IDA
00000E0A  54 78 9c ed dc 5d 8e db  36 18 86 51 01 b3 80 2c   Tx...].. 6..Q...,
00000E1A  c9 5b d7 92                                        .[..
00000E1E  00 03 00 02 00 80 60 0b  d5 00 00 08 01 49 44 41   ....... .....IDA
00000E2E  54 78 9c ed dc 5d 8e db  36 18 86 51 01 b3 80 2c   Tx...].. 6..Q...,
00000E3E  c9 5b d7 92                                        .[..
```
Data setelah header menunjukkan adanya segmen IDAT, yang berisi data gambar yang terkompresi dalam format PNG. Bagian ini menandakan bahwa file PNG sedang dikirimkan dalam blok-blok data.
```
    00000280  00 04 00 43                                        ...C
    00000284  00 04 00 43                                        ...C
000015DA  00 03 00 43 49 45 4e 44  ae 42 60 82               ...CIEND .B.
000015E6  00 03 00 43 49 45 4e 44  ae 42 60 82               ...CIEND .B.
    00000288  00 04 00 19                                        ....
    0000028C  00 04 00 19                                        ....
```

## Proses
Menganalisis file pcap dengan cara mendekodekan paket yang menggunakan port UDP 53 (yang umumnya digunakan oleh DNS) dan menandai mereka sebagai TFTP (Trivial File Transfer Protocol).

>tshark -r retrivial.pcap -d 'udp.port==53,tftp'

### Penjelasan:
Tshark digunakan untuk membaca file pcap dan menafsirkan paket yang lewat pada port UDP 53 sebagai TFTP. Meskipun paket ini dikirim melalui DNS, data yang terkandung dalam paket tersebut menggunakan format yang mirip dengan TFTP. Hal ini menunjukkan bahwa file tersebut sedang diunduh atau diunggah menggunakan TFTP.
![Screenshot 2025-01-13 212834](https://github.com/user-attachments/assets/0ba230a4-5966-4168-b4bf-ceee949d5f6b)
Hasil dari analisis menggunakan Tshark menunjukkan beberapa paket TFTP, termasuk permintaan Read Request, Option Acknowledgement, dan Data Packet yang berisi blok data file yang ditransfer. Berikut adalah tampilan hasil dari Tshark yang menunjukkan komunikasi TFTP antara dua IP: 172[.]25[.]0[.]1 (klien) dan 172[.]25[.]0[.]2 (server).

### Penjelasan Rincian Transfer Data:
- TFTP Read Request: Di frame pertama dan kedua, klien (172.25.0.1) mengirimkan permintaan Read Request untuk file flag.png ke server (172.25.0.2). Ini menunjukkan titik awal transfer file.
- Blok Data 32 Byte: Data dikirimkan dalam blok-blok 32 byte, yang merupakan standar TFTP.
- Paket Data dan Acknowledgement: Setiap kali server mengirimkan paket data, klien mengirimkan Acknowledgement untuk memberi tahu bahwa paket tersebut diterima dan siap untuk menerima blok berikutnya.
- Proses transfer ini berulang hingga seluruh file berhasil dikirimkan. Pada akhirnya, byte CIEND menunjukkan bahwa transfer file telah selesai.

Menangkap paket yang melibatkan TFTP (Trivial File Transfer Protocol) dengan data UDP pada port 53

```bash
tshark -r retrivial.pcap -d 'udp.port=53,tftp' -Y 'data.data'
    7   0.300000   172.25.0.2 → 172.25.0.1   TFTP 80 Data Packet, Block: 66
    8   0.350000   172.25.0.2 → 172.25.0.1   TFTP 80 Data Packet, Block: 66
   11   0.500000   172.25.0.2 → 172.25.0.1   TFTP 80 Data Packet, Block: 20
   12   0.550000   172.25.0.2 → 172.25.0.1   TFTP 80 Data Packet, Block: 20
   15   0.699999   172.25.0.2 → 172.25.0.1   TFTP 80 Data Packet, Block: 14
   16   0.749999   172.25.0.2 → 172.25.0.1   TFTP 80 Data Packet, Block: 14
   19   0.899999   172.25.0.2 → 172.25.0.1   TFTP 80 Data Packet, Block: 61
   20   0.949999   172.25.0.2 → 172.25.0.1   TFTP 80 Data Packet, Block: 61
   23   1.099999   172.25.0.2 → 172.25.0.1   TFTP 80 Data Packet, Block: 29
   24   1.149999   172.25.0.2 → 172.25.0.1   TFTP 80 Data Packet, Block: 29
   27   1.299999   172.25.0.2 → 172.25.0.1   TFTP 80 Data Packet, Block: 62
   28   1.349999   172.25.0.2 → 172.25.0.1   TFTP 80 Data Packet, Block: 62
   31   1.499999   172.25.0.2 → 172.25.0.1   TFTP 80 Data Packet, Block: 63
   32   1.549999   172.25.0.2 → 172.25.0.1   TFTP 80 Data Packet, Block: 63
   35   1.699998   172.25.0.2 → 172.25.0.1   TFTP 80 Data Packet, Block: 40
   36   1.749998   172.25.0.2 → 172.25.0.1   TFTP 80 Data Packet, Block: 40
...
...
```
Hasil yang ditampilkan adalah data paket TFTP yang teridentifikasi, yang berisi informasi blok data yang dipindahkan.
```bash
tshark -r retrivial.pcap -d 'udp.port=53,tftp' -Y 'data.data' -Tfields -e tftp.block -e data.data
66      3af074e0e9c0d381a7034f079e0e3cdd9f0bff0b7b57f59a788d4e9900000000
66      3af074e0e9c0d381a7034f079e0e3cdd9f0bff0b7b57f59a788d4e9900000000
20      5c9e1e96f9f2836173e8f2eebe72fd8d70af0207070707070707070707070707
20      5c9e1e96f9f2836173e8f2eebe72fd8d70af0207070707070707070707070707
14      0e0e0e0e0e0e0e0e0e0e0e0e0e0e5ee14dcfdeb29ec7dab6e1ad7379f747dbf9
14      0e0e0e0e0e0e0e0e0e0e0e0e0e0e5ee14dcfdeb29ec7dab6e1ad7379f747dbf9
61      0e0e0e0e0e7e17f8a4c7f51ccbb9dee4127a3c3c2cfd296bf377c1c1c1c1c1c1
61      0e0e0e0e0e7e17f8a4c7f51ccbb9dee4127a3c3c2cfd296bf377c1c1c1c1c1c1
29      707070707070707070f0bbc11bdab1dee3a41dd2c6b5ff75f01be106de1c7a30
29      707070707070707070f0bbc11bdab1dee3a41dd2c6b5ff75f01be106de1c7a30
62      c1c1c1c1c1c1c1c1c1c1c1c1c1c16f01ff53024f079e0e3c1d783af074e0e9c0
62      c1c1c1c1c1c1c1c1c1c1c1c1c1c16f01ff53024f079e0e3c1d783af074e0e9c0
...
....
```
Setelah memperoleh informasi mengenai paket yang dipindahkan, memfilter data lebih lanjut untuk menampilkan informasi terkait blok dan data

Hasilnya adalah data blok dari setiap paket yang terkandung dalam file PCAP:
![Screenshot 2025-01-13 233545](https://github.com/user-attachments/assets/92d0afe4-93af-43c8-acfe-a2c80c331489)

dari sini saya mencoba gunakan cyberchef:
![Screenshot 2025-01-13 233806](https://github.com/user-attachments/assets/9ed1ca5e-916b-47af-b47a-91d1241b5e0d)

*Berhasil dapatkan flag setelah scan barcode menggunakan barcode scanner*
