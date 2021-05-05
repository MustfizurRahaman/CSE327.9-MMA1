import json
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


# create model
class Medicine(db.Model):
    name = db.Column(db.String(255))
    company = db.Column(db.String(255))
    price = db.Column(db.FLOAT(10.2))
    pack = db.Column(db.Integer)
    stock = db.Column(db.String(15))
    id = db.Column(db.Integer, primary_key=True)
    most_recent = db.Column(db.Integer)

    # Create A String
    def __repr__(self):
        return '<Name %r>' % self.name


# searchField in search page
class SearchForm(FlaskForm):
    search_input = StringField("Search", validators=[DataRequired()], id="search_auto")


# autocomplete/ show suggestion in the search box while typing
@app.route('/_autocomplete', methods=['GET'])
def autocomplete():
    all_item = Medicine.query.order_by(Medicine.most_recent)

    items = []

    for item in all_item:
        items.append(item.name)

    return Response(json.dumps(items), mimetype='application/json')


# search_page_bt
@app.route('/_search')
def search_page_bt():
    return search_page(sent_item="apa", is_sent=True)


# search page
@app.route('/search.html', methods=['GET', 'POST'])
def search_page(sent_item=None, is_sent=False):
    form = SearchForm(request.form)

    if is_sent:
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

        for item in all_item:
            print('some')

    return render_template('search.html', form=form, searched_item=searched_item, items=all_item)


# 404 custom error page
@app.errorhandler(404)
def page_not_found(e):
    return render_template("error_404.html"), 404


if __name__ == "__main__":
    app.run(port=4930, debug=True)
