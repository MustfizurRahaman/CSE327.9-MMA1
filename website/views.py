from flask import Flask, render_template, Blueprint
import pickle
from flask import request
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import cv2
from PIL import Image
import os as os

views = Blueprint('views', __name__)
UPLOAD_FOLDER = "website/static/img"


# Predict function to predict
def predict(img_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img = cv2.medianBlur(img,5)
    text = pytesseract.image_to_string(img)
    #print(text)
    return text


# dumping last predict info to pickle
def dump(text):
    list = []
    list = op()
    list.append(text)
    with open('last_search.pkl', 'wb') as f:
        pickle.dump(list, f)
        f.close()


# open the pickle file
def op():
    with open('last_search.pkl', 'rb') as f:
        mylist = pickle.load(f)
        f.close()
    return mylist


# Refer to search page
@views.route('/_search')
def sarch_page():
    list = op()
    last_serch = list[len(list) - 1]
    return search_page(sent_item=last_serch)


# upload funtion for uploading and saving Image
@views.route('/Upload_Image', methods=["GET", "POST"])
def upload(file=None):
    is_sent = False
    if not file:
        if request.method == "POST":
            image_file = request.files["image"]
            if image_file:
                image_location = os.path.join(
                    UPLOAD_FOLDER, image_file.filename
                )
                image_file.save(image_location)
                is_sent = True
                #print(image_location)
    else:
        image_location = file
        is_sent = True

    if is_sent:
        pred = predict(image_location)
        dump(pred)
        return render_template("Upload_Image.html", prediction=pred, image_loc=image_file.filename)

    return render_template("Upload_Image.html", prediction=0)

