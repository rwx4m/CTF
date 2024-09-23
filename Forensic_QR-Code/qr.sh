#!/bin/bash

input_image="/home/kali/gemastik_5.png"
output_image="/home/kali/hasil.png"

width=$(identify -format "%w" "$input_image")
height=$(identify -format "%h" "$input_image")

temp_image=$(mktemp).png

for ((i = 0; i < height; i++)); do
    if ((i % 2 == 0)); then
        convert "$input_image" -crop "${width}x1+3s+$i" +repage "$temp_image"
    else
        convert "$input_image" -crop "${width}x1+3+$i" +repage -flop "$temp_image"
    fi

    if ((i == 0)); then
        cp "$temp_image" "$output_image"
    else
        convert "$output_image" "$temp_image" -append "$output_image"
    fi
done

rm "$temp_image"

echo "Gambar hasil pemrosesan disimpan di: $output_image"
