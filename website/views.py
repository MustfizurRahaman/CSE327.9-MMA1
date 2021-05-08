import json
import os
from flask import Blueprint, render_template, request, Response
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from .models import Medicine

views = Blueprint('views', __name__)


# searchField in search page
class SearchForm(FlaskForm):
    search_input = StringField("Search", validators=[DataRequired()], id="search_auto")


# autocomplete/ show suggestion in the search box while typing
@views.route('/_autocomplete', methods=['GET'])
def autocomplete():
    items = []

    all_item = Medicine.query.order_by(Medicine.name)

    for item in all_item:
        items.append(item.name)

    return Response(json.dumps(items), mimetype='application/json')


# search page
@views.route('/search.html', methods=['GET', 'POST'])
def search_page(sent_item=None):
    form = SearchForm(request.form)

    if sent_item:
        searched_item = sent_item
    else:
        searched_item = None

    if form.validate_on_submit():
        searched_item = form.search_input.data
        form.search_input.data = ''

    if searched_item is not None:
        all_item = Medicine.query.filter(Medicine.name.startswith(searched_item)).all()

    else:
        all_item = Medicine.query.filter_by(name=searched_item).all()

    return render_template('search.html', form=form, searched_item=searched_item, items=all_item)


@views.route('/camera.html', methods=['GET', 'POST'])
def camera_page():
    if request.method == "POST":

        if os.path.exists("website/static/img/temp.jpg"):
            #upload()
            pass
        else:
            return render_template("error_404.html")

    # return Response(open('test.html').read(), mimetype="text/html")
    return render_template('camera.html')


# save the image as a picture
@views.route('/_camera_image', methods=['POST'])
def image():
    image_file = request.files['image']  # get the image
    image_file.save('%s/%s' % ('website/static/img', 'temp.jpg'))

    return Response("saved")
