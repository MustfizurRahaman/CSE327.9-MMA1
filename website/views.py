import cv2
import json
import pickle
import os as os
import pytesseract
from PIL import Image
from .models import Medicine
from .forms import SearchForm
from flask import Flask, Blueprint, render_template, request, Response


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
UPLOAD_FOLDER = "website/static/img"

views = Blueprint('views', __name__)


# autocomplete/ show suggestion in the search box while typing
@views.route('/_autocomplete_search', methods=['GET'])
def autocomplete_search():
    """
        This method is used to suggest users the product name depending on the input.

        :param Null: None.

        :type Null: None.

        :return: products which start with the characters typed by user.

        :rtype: json.
    """

    items = []

    all_item = Medicine.query.order_by(Medicine.name)

    for item in all_item:
        items.append(item.name)

    return Response(json.dumps(items), mimetype='application/json')


# search page
@views.route('/search.html', methods=['GET', 'POST'])
def search_page(sent_item=None):
    """
        This method allows the user to search, and according to the input, the
        the page would show if deatils of the product if it exists in database,
        otherwise will show item not found.

        :param sent_item: Its a text string.


        :type sent_item: String.

        :return: search option view.

        :rtype: html.
    """

    form = SearchForm(request.form)

    if sent_item:
        searched_item = sent_item
    else:
        searched_item = None

    if request.method == "POST":
        searched_item = form.search_input.data
        form.search_input.data = ''

    if searched_item is not None:
        all_item = Medicine.query.filter(Medicine.name.startswith(searched_item)).all()

    else:
        all_item = Medicine.query.filter_by(name=searched_item).all()

    return render_template('search.html', form=form, searched_item=searched_item, items=all_item)


@views.route('/camera.html', methods=['GET', 'POST'])
def camera_page():
    """
        This method is used to capture image, and after that send it to get predicted.

        :param Null: None.

        :type Null: None.

        :return: image capture view.

        :rtype: html.
    """
    if request.method == "POST":

        if os.path.exists("website/static/img/temp.jpg"):
            return upload(file="website/static/img/temp.jpg")
            
        else:
            return render_template("error_404.html")

    return render_template('camera.html')


# save the image as a picture
@views.route('/_camera_image', methods=['POST'])
def image_from_camera():

    """
        This method is used to save the image that is taken in the camera page

        :param NULL: None

        :type NULL: None

        :return: returns response as saved

        :rtype: Response.
    """
    image_file = request.files['image']  # get the image
    image_file.save('%s/%s' % ('website/static/img', 'temp.jpg'))

    return Response("saved")





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
    """
        This method is used to get the search page. In here, last search text will be retrive and pass to search. 

        :param Null: None.

        :type request: None.

        :return: this method returns a search html page.

        :rtype: HttpResponse.
    """
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
