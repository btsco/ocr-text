# setup
# install tessereact
sudo apt-get install tesseract-ocr
# install python
sudo apt-get install pip
# install open-cv 2
pip install pillow pytesseract opencv-python
# install lib require
sudo apt-get update
sudo apt-get install ffmpeg libsm6 libxext6  -y

# trained data language
- https://github.com/tesseract-ocr/tessdata
- [VietNam]: https://github.com/tesseract-ocr/tessdata/blob/main/vie.traineddata
# copy into system
sudo cp <vie.traineddata> /usr/share/tesseract-ocr/4.00/tessdata/

# 