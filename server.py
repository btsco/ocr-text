import io
import json                    
import base64                  
import logging             
import numpy as np
from PIL import Image
import cv2
import pytesseract
import argparse
import os
from datetime import datetime

from flask import Flask, request, jsonify, abort

app = Flask(__name__)          
app.logger.setLevel(logging.DEBUG)

def getName():
    return '{}.png'.format(datetime.now().strftime('%y%m%d%H%M%S%f'))
  


@app.route("/test", methods=['POST'])
def test_method():         
    # print(request.json)      
    if not request.json or 'image' not in request.json: 
        abort(400)
             
    # get the base64 encoded string
    im_b64 = request.json['image']
      
    # convert it into bytes  
    img_bytes = base64.b64decode(im_b64.encode('utf-8'))

    # convert bytes data to PIL Image object
    img = Image.open(io.BytesIO(img_bytes))
    # Read file and grayscale
    origin_file_name = getName()
    img.save(origin_file_name)
    image = cv2.imread(origin_file_name)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(getName(), gray)

    # Check pre-process
# thresh hold white - black
# if args["preprocess"] == "thresh":
    #gray = cv2.threshold(gray, 0+255//2, 255,
    #    cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    gray = cv2.adaptiveThreshold(gray, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,15,6)
    #gray = cv2.adaptiveThreshold(gray, 255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
    cv2.imwrite(getName(), gray)

    # blur
# elif args["preprocess"] == "blur":
    gray = cv2.medianBlur(gray, 3)

# temp store file to apply OCR
    filename = getName()
    cv2.imwrite(filename, gray)

    # Load image temp and apply Tesseract OCR
    print(request.json['lang'])
    lang = request.json['lang']
    text = pytesseract.image_to_string(Image.open(filename),lang=lang)

    # delete temp
    #os.remove(filename)
    #os.remove(origin_file_name)

 

    # PIL image object to numpy array
    img_arr = np.asarray(img)      
    print('img shape', img_arr.shape)

    # process your img_arr here    
    
    # access other keys of json
    # print(request.json['other_key'])

    print(text)
    result_dict = {'output': text}
    return result_dict
  
  
def run_server_api():
    app.run(host='0.0.0.0', port=8080)
  
  
if __name__ == "__main__":     
    run_server_api()