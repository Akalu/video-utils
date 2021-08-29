About
======
Describes how to use img2pdf - a lossless convertor of images to PDF

Overview
=========

```
sudo apt update
sudo apt install img2pdf
img2pdf -V
```

Direct conversion (one or all images):

```
img2pdf img1.png -o outcome.pdf
img2pdf *.png -o outcome.pdf
```

Convertions with overloading output formats:

With specific page size:

```
img2pdf img1.png img2.png img3.png --pagesize 18cmx12cm -o outcome.pdf
```

With specific image size:

```
img2pdf img1.png img2.png img3.png --imgsize 18cmx12cm -o outcome.pdf
```
