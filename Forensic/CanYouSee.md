# CanYouSee

**Category:** Forensic

## Description
>How about some hide and seek?
---

```bash
┌──(rwx4m㉿Home)-[~/Chall]
└─$ file ukn_reality.jpg 
ukn_reality.jpg: JPEG image data, JFIF standard 1.01, resolution (DPI), density 72x72, segment length 16, baseline, precision 8, 4308x2875, components 3
```
```bash                                                                                                                                 
┌──(rwx4m㉿Home)-[~/Chall]
└─$ exiftool ukn_reality.jpg 
ExifTool Version Number         : 13.00
File Name                       : ukn_reality.jpg
Directory                       : .
File Size                       : 2.3 MB
File Modification Date/Time     : 2024:03:12 07:05:55+07:00
File Access Date/Time           : 2025:01:14 12:38:53+07:00
File Inode Change Date/Time     : 2025:01:14 12:38:41+07:00
File Permissions                : -rw-r--r--
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
JFIF Version                    : 1.01
Resolution Unit                 : inches
X Resolution                    : 72
Y Resolution                    : 72
XMP Toolkit                     : Image::ExifTool 11.88
Attribution URL                 : <base64>
Image Width                     : 4308
Image Height                    : 2875
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:2:0 (2 2)
Image Size                      : 4308x2875
Megapixels                      : 12.4
```
```bash
┌──(rwx4m㉿Home)-[~/Chall]
└─$ echo "<base64>" | base64 -d 
<flag>
```
