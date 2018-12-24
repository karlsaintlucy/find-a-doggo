"""Store the forms."""

import re

from flask_wtf import FlaskForm, RecaptchaField
from uszipcode import SearchEngine
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import InputRequired, Regexp, ValidationError

# This compiled regexp checks that the input location is 5 consecutive digits.
LOCATION_RE = re.compile(r'^[0-9]{5}$')


class SearchForm(FlaskForm):
    """Create the class for the landing page search form."""

    breed_type = SelectField('I want a dog that is…', choices=[
        ('chill', 'chill'),
        ('protector', 'protective'),
        ('atrisk', 'from an at-risk breed')],
        validators=[InputRequired()])
    location = StringField('Location (5-digit ZIP code)', validators=[
        Regexp(LOCATION_RE, message='Must be a 5-digit ZIP code.'),
        InputRequired()])

    def validate_location(self, field):
        """Check that the location given is valid using uszipcode module."""
        search = SearchEngine(simple_zipcode=True)

        z = search.by_zipcode(field.data)
        if z.zipcode is None:
            raise ValidationError('Invalid ZIP code.')

    recaptcha = RecaptchaField()
    submit = SubmitField()
