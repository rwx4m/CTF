
## Deskripsi Tantangan
Pada challenge ini, saya diberikan sebuah file gambar yang berisi QR Code yang tampak tidak teratur atau terdistorsi. Tugas saya adalah memperbaiki gambar tersebut sehingga dapat dibaca oleh QR code scanner dan mendapatkan flag dari QR tersebut.
![qr](https://github.com/user-attachments/assets/f85a263c-1a8e-44a7-a276-7d72c52ffb5f)

## Analisis Awal
Masalah utama adalah QR Code terlihat terdistorsi secara horizontal, di mana setiap baris sepertinya dipindahkan atau dimodifikasi.
Saya menduga bahwa baris-baris QR Code dipindahkan ke posisi yang salah atau ada pola tertentu dalam distorsinya. Oleh karena itu, langkah pertama adalah menganalisis pola distorsi.

## Pemecahan Masalah
Saya membuat script Bash untuk memperbaiki gambar QR Code yang rusak.
Untuk memprosesnya, langkah pertama adalah mengetahui dimensi gambar (lebar dan tinggi). Ini dilakukan agar script dapat bekerja baris per baris sesuai dengan tinggi gambar.

width=$(identify -format "%w" "$input_image")
height=$(identify -format "%h" "$input_image")
**Penjelasan:**
identify: command dari ImageMagick yang digunakan untuk mendapatkan metadata gambar.
%w dan %h: Masing-masing digunakan untuk mendapatkan lebar dan tinggi gambar (w mewakili weight, h mewakili height)

Setiap baris pada gambar akan diproses secara terpisah, yaitu:
[x] Baris GENAP dibiarkan tetap (tidak diubah).
[x] Baris GANJIL dibalik secara horizontal untuk mengoreksi distorsi.

for ((i = 0; i < height; i++)); do
    if ((i % 2 == 0)); then
        # Baris genap: Tidak diubah
        convert "$input_image" -crop "${width}x1+0+$i" +repage "$temp_image"
    else
        # Baris ganjil: Dibalik horizontal
        convert "$input_image" -crop "${width}x1+0+$i" +repage -flop "$temp_image"
    fi

**Penjelasan:**
- convert: command dari ImageMagick untuk memproses gambar.
- crop "${width}x1+0+$i": Memotong baris ke-i dengan lebar seluruh gambar dan tinggi 1 piksel.
- flop: Membalikkan gambar secara horizontal (khusus untuk baris ganjil).
+repage: Untuk memastikan hasil potongan tetap sinkron dengan gambar utama.

Kemudian setelah setiap baris diproses, hasilnya digabungkan kembali menjadi satu gambar utuh. Proses ini dilakukan dengan menambahkan setiap baris ke dalam gambar output secara berurutan.
>
>    if ((i == 0)); then
>        # Baris pertama langsung disalin sebagai hasil awal
>        cp "$temp_image" "$output_image"
    else
>        # Gabungkan hasil baris dengan baris sebelumnya
        convert "$output_image" "$temp_image" -append "$output_image"
    fi
Penjelasan:
- cp: Untuk menyalin baris pertama ke file hasil (output_image).
- append: Menambahkan baris baru di bawah gambar hasil sebelumnya.

## Menampilkan lokasi hasil:
echo "Gambar hasil pemrosesan disimpan di: $output_image"

Setelah menjalankan script ini, file gambar hasil akan dibuat. Kemudian menggunakan QR scanner untuk membaca QR-Code yang sudah diperbaiki, dan flag dari tantangan akan terlihat.
![hasil](https://github.com/user-attachments/assets/a4ce9705-21d4-4b0e-bdf3-81bc3377980e)

## Kesimpulan
Dengan pendekatan berbasis script dan analisis pola distorsi, saya berhasil memperbaiki gambar QR Code yang rusak dan menyelesaikan challenge ini.
