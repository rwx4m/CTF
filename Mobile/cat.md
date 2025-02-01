# Cat

*Category: Mobile*

## Description
Cat is a mobile (android) challenge, which highlights the importance of paying attention to small details.

---


```bash
┌──(rwx4m㉿Home)-[~/Chall/CAT]
└─$ file cat.ab 
cat.ab: Android Backup, version 5, Compressed, Not-Encrypted
```
```wget https://github.com/nelenkov/android-backup-extractor/releases/download/master-20221109063121-8fdfc5e/abe.jar```

```bash
┌──(rwx4m㉿Home)-[~/Chall/CAT]
└─$ java -jar abe.jar  unpack cat.ab output.tar
Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
0% 1% 2% 3% 4% 5% 6% 7% 8% 9% 10% 11% 12% 13% 14% 15% 16% 17% 18% 19% 20% 21% 22% 23% 24% 25% 26% 27% 28% 29% 30% 31% 32% 33% 34% 35% 36% 37% 38% 39% 40% 41% 42% 43% 44% 45% 46% 47% 48% 49% 50% 51% 52% 53% 54% 55% 56% 57% 58% 59% 60% 61% 62% 63% 64% 65% 66% 67% 68% 69% 70% 71% 72% 73% 74% 75% 76% 77% 78% 79% 80% 81% 82% 83% 84% 85% 86% 87% 88% 89% 90% 91% 92% 93% 94% 95% 96% 97% 98% 99% 100% 
4853760 bytes written to output.tar.

┌──(rwx4m㉿Home)-[~/Chall/CAT]
└─$ ls
abe.jar  cat.ab  output.tar
```
```bash
┌──(rwx4m㉿Home)-[~/Chall/CAT]
└─$ tar -xf output.tar 
                                                                                                                        
┌──(rwx4m㉿Home)-[~/Chall/CAT]
└─$ ls
abe.jar  apps  cat.ab  output.tar  shared
```

folder APP, tidak ada yang menarik. Saya lanjutkan ke folder Shared

```bash
┌──(rwx4m㉿Home)-[~/…/CAT/shared/0/Pictures]
└─$ ls
IMAG0001.jpg  IMAG0002.jpg  IMAG0003.jpg  IMAG0004.jpg  IMAG0005.jpg  IMAG0006.jpg
```

buka file IMAG0004 dengan Image Viewer. Tidak disangka, flag ditemukan pada kertas yang dipegangnya.
![Image](https://github.com/user-attachments/assets/f98ccc97-30fb-4229-b337-cbe4a662daed)
