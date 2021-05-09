from . import db


class Medicine(db.Model):
    """
        This class is extended from the attribute db so it has all the functionality
        of the SQLAlchemy.
        This class used to create objects for database entry
        And to retrieve data from database

        :param NULL: None

        :type NULL: None

        :return: None

        :rtype: None.
    """
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    company_name = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.Text)
    quantity = db.Column(db.Integer, nullable=False)
    side_effects = db.Column(db.Text)

    # Create A String
    def __repr__(self):
        return '<Name %r>' % self.name
