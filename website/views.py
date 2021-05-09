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
    """
        This method is used to predict the Text consists in a Image.

        :param img_path: It's a path of the image from where have to predict.

        :type img_path: String.

        :return: String. Predicted String

        :rtype: String.
    """
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img = cv2.medianBlur(img,5)
    text = pytesseract.image_to_string(img)
    #print(text)
    return text


# dumping last predict info to pickle
def dump(text):
    """
        This method is used to dump  the last predicted Text to a pickle file.

        :param text: Its a text string.

        :type text: String.

        :return: It will return nothing.

        :rtype: None.
    """
    list = []
    list = op()
    list.append(text)
    with open('last_search.pkl', 'wb') as f:
        pickle.dump(list, f)
        f.close()


# open the pickle file
def op():
    """
        This method is used to open the pickle file named last_search.pkl. Load file to a list and return it
        for further searching processing.

        :param Null: None.

        :type Null: None.

        :return: It will return  a list file.

        :rtype: list.
    """

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
    """
        This method is used to get the image from httpResponse and feedback the HttpResponse with predicted text.
        This method saved the image in a folder and send the location to predict function.After getting text return from
        predict function, it wll show the test buy returning at html page.

        :param file: it's a HttpResponse from user..

        :type request: HttpResponse.

        :return: this method returns a html page.It returns a page where it has three options, Upload Image
          ,Prediction  and Search option.

        :rtype: HttpResponse.
    """
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

