# import the necessary packages
from PIL import Image
import pytesseract
import argparse
import cv2
import os
 
# -i file ảnh cần nhận dạng
# -p tham số tiền xử lý ảnh (có thể bỏ qua nếu không cần). Nếu dùng: blur : Làm mờ ảnh để giảm noise, thresh: Phân tách đen trắng
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
        help="Đường dẫn đến ảnh muốn nhận dạng")
ap.add_argument("-p", "--preprocess", type=str, default="thresh",
        help="Bước tiền xử lý ảnh")
args = vars(ap.parse_args())

# Read file and grayscale 
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
# Check pre-process
# thresh hold white - black
if args["preprocess"] == "thresh":
        gray = cv2.threshold(gray, 0, 255,
                cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
 
# blur
elif args["preprocess"] == "blur":
        gray = cv2.medianBlur(gray, 3)
 
# temp store file to apply OCR
filename = "{}.png".format(os.getpid())
cv2.imwrite(filename, gray)

# Load image temp and apply Tesseract OCR
text = pytesseract.image_to_string(Image.open(filename),lang='eng')

# delete temp
os.remove(filename)

# result
print(text)