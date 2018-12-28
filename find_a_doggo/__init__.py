"""Run the find_a_doggo app."""

import os

from flask import Flask
from flask_wtf.csrf import CSRFProtect

# come back to the WTForms stuff later

app = Flask(__name__)

import find_a_doggo.views

app.config['ENV'] = os.environ['ENV']
app.config['TEMPLATES_AUTO_RELOAD'] = os.environ['TEMPLATES_AUTO_RELOAD']
app.config['DEBUG'] = os.environ['DEBUG']
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['RECAPTCHA_PUBLIC_KEY'] = os.environ['RECAPTCHA_PUBLIC_KEY']
app.config['RECAPTCHA_PRIVATE_KEY'] = os.environ['RECAPTCHA_PRIVATE_KEY']
app.config['RECAPTCHA_DATA_ATTRS'] = {'theme': 'dark', 'data-size': 'compact'}

csrf = CSRFProtect(app)


if __name__ == '__main__':
    app.run()
