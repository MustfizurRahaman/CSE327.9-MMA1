import json
import os
from os import environ
from flask import Flask, render_template, request, Response
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# URI of database
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URI')

# Secret Key!
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')

db = SQLAlchemy(app)


# Model
class Medicine(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    company_name = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.Text)
    quantity = db.Column(db.Integer)
    side_effects = db.Column(db.Text)

    # Create A String
    def __repr__(self):
        return '<Name %r>' % self.name


# searchField in search page
class SearchForm(FlaskForm):

    search_input = StringField("Search", validators=[DataRequired()], id="search_auto")


# autocomplete/ show suggestion in the search box while typing
@app.route('/_autocomplete', methods=['GET'])
def autocomplete():
    items = []

    all_item = Medicine.query.order_by(Medicine.name)

    for item in all_item:
        items.append(item.name)

    return Response(json.dumps(items), mimetype='application/json')


# search page
@app.route('/search.html', methods=['GET', 'POST'])
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


@app.route('/camera.html', methods=['GET', 'POST'])
def camera_page():

    if request.method == "POST":

        if os.path.exists("static/img/temp.jpeg"):
            return search_page(sent_item="Nex", is_sent=True)
        else:
            return render_template("error_404.html")

    # return Response(open('test.html').read(), mimetype="text/html")
    return render_template('camera.html')


# save the image as a picture
@app.route('/_camera_image', methods=['POST'])
def image():

    image_file = request.files['image']  # get the image
    image_file.save('%s/%s' % ('static/img', 'temp.jpg'))

    return Response("saved")


# 404 custom error page
@app.errorhandler(404)
def page_not_found(e):
    return render_template("error_404.html"), 404


if __name__ == "__main__":
    app.run(port=4800, debug=True)
