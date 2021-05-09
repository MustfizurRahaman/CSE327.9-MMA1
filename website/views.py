import os
import json
from .forms import SearchForm
from .models import Medicine
from flask import Blueprint, render_template, request, Response
views = Blueprint('views', __name__)


# autocomplete/ show suggestion in the search box while typing
@views.route('/_autocomplete_search', methods=['GET'])
def autocomplete_search():

    """
        This method is used to predict the Text consists in a Image.
        :param img_path: It's a path of the image from where have to predict.
        :type img_path: String.
        :return: String. Predicted String
        :rtype: String.
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
        This method is used to dump  the last predicted Text to a pickle file.
        :param text: Its a text string.
        :type text: String.
        :return: It will return nothing.
        :rtype: None.
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
        This method is used to open the pickle file named last_search.pkl. Load file to a list and return it
        for further searching processing.
        :param Null: None.
        :type Null: None.
        :return: It will return  a list file.
        :rtype: list.
    """
    if request.method == "POST":

        if os.path.exists("website/static/img/temp.jpg"):
            # upload()
            pass
        else:
            return render_template("error_404.html")

    return render_template('camera.html')


# save the image as a picture
@views.route('/_camera_image', methods=['POST'])
def image_from_camera():

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
    image_file = request.files['image']  # get the image
    image_file.save('%s/%s' % ('website/static/img', 'temp.jpg'))

    return Response("saved")
