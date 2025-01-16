# File Types

*Category*: Forensics

## Description
This file was found among some files marked confidential but my pdf reader cannot read it, maybe yours can.

---
```
┌──(rwx4m㉿Home)-[~/Desktop/Cases]
└─$ file Flag.pdf   
Flag.pdf: shell archive text
```
```
┌──(rwx4m㉿Home)-[~/Desktop/Cases]
└─$ strings Flag.pdf| head    
#!/bin/sh
# This is a shell archive (produced by GNU sharutils 4.15.2).
# To extract the files from this archive, save it to some FILE, remove
# everything before the '#!/bin/sh' line above, then type 'sh FILE'.
lock_dir=_sh00046
# Made on 2023-03-16 01:40 UTC by <root@4b9f36a8cccb>.
# Source directory was '/app'.
# Existing files will *not* be overwritten, unless '-c' is specified.
# This shar contains:
# length mode       name
```
```
┌──(rwx4m㉿Home)-[~/Desktop/Cases]
└─$ mv Flag.pdf Flag.sh                                                                                                                    
```
```
┌──(rwx4m㉿Home)-[~/Desktop/Cases]
└─$ chmod +x Flag.sh
```
```
┌──(rwx4m㉿Home)-[~/Desktop/Cases]
└─$ ./Flag.sh 
x - created lock directory _sh00046.
x - extracting flag (text)
x - removed lock directory _sh00046.
```
```
$ file flag 
flag: current ar archive
```
```binwalk -e flag```

>get 64 (gzip)

```binwalk -e 64```
>get flag (lzip)

```lzip -d -k flag```
>get flag.out (lz4)

```
mv flag.out flag.lz4
lz4 -d flag.lz4
```
>get flag (lzma)

```
mv flag flag.lzma
lzma -d flag.lzma
```
>get flag (lzop)

```mv flag flag.lzop```
>get flag (lzip)

```lzip -d -k flag```
>get flag.out (XZ)

```
mv flag.out flag.xz
xz -d flag.xz
```
>get flag (ASCII)

```
xxd -p -r flag
```
>GET LAST FLAG
