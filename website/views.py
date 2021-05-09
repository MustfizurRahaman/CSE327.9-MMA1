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
            # upload()
            pass
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
