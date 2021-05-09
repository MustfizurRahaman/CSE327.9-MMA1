from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


# searchField in search page
class SearchForm(FlaskForm):
    search_input = StringField("Search", validators=[DataRequired()], id="search_auto")
