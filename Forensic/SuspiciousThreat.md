# Suspicious Threat
## Challenge Overview:

Dalam tantangan ini, saya dihadapkan pada sebuah sistem yang mencurigakan dan diminta untuk menemukan flag yang tersembunyi. Tantangan ini berfokus pada analisis forensik terhadap library preload yang mencurigakan.

----

Langkah pertama adalah memeriksa file `/etc/ld.so.preload`, yang digunakan untuk memuat library secara otomatis sebelum library lainnya. File ini sering disalahgunakan oleh malware untuk memuat library berbahaya.
```bash
root@machine:~# cat /etc/ld.so.preload
ERROR: ld.so: object '/lib/x86_64-linux-gnu/libc.hook.so.6' from /etc/ld.so.preload cannot be preloaded (cannot open shared object file): ignored.
/lib/x86_64-linux-gnu/libc.hook.so.6
```
Terlihat ada library mencurigakan `libc.hook.so.6` yang tidak dapat ditemukan. Ini adalah indikasi awal adanya potensi manipulasi.

Saya menggunakan `ldd` untuk memeriksa apakah library mencurigakan ini mempengaruhi executable penting.
```bash
root@machine:~# ldd /bin/ps
ERROR: ld.so: object '/lib/x86_64-linux-gnu/libc.hook.so.6' from /etc/ld.so.preload cannot be preloaded (cannot open shared object file): ignored.
```

Langkah selanjutnya adalah mencari file yang mengandung "flag" di dalam sistem.
```bash
root@machine:~# find / -type f -name "*flag*" 2>/dev/null
/var/pr3l04d_/flag.txt
```
Setelah menemukan file tersebut, saya membukanya untuk mendapatkan flag.
```bash
root@machine:~# cat /var/pr3l04d_/flag.txt
FLAG{****************}
```
----

## Kesimpulan
Dalam tantangan ini, manipulasi file `/etc/ld.so.preload` digunakan untuk menyembunyikan flag. Dengan memahami bagaimana library preload bekerja dan menggunakan alat seperti `ldd` serta perintah pencarian, saya berhasil menemukan dan membaca flag yang tersembunyi.

## Catatan Tambahan
- Error dari `ldd` membantu mengidentifikasi bahwa ada sesuatu yang salah dengan konfigurasi preload.
- Struktur direktori yang tidak biasa `(/var/pr3l04d_/)` menunjukkan adanya eksploitasi preload untuk menyembunyikan file.
- Menonaktifkan atau memperbaiki `ld.so.preload` adalah langkah penting untuk mengamankan sistem dari manipulasi serupa.

