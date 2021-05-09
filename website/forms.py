from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


# search field in search page
class SearchForm(FlaskForm):
    """
        This class holds the search bar text field, where the input is entered

        :param NULL: None

        :type NULL: None

        :return: None

        :rtype: None
    """

    search_input = StringField("Search", validators=[DataRequired()], id="search_auto")
