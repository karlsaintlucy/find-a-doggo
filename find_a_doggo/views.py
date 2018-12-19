"""Store the views."""

from flask import request, render_template

from find_a_doggo.breed_urls import BREED_URLS
from find_a_doggo import app
from find_a_doggo.forms import SearchForm
from find_a_doggo.helpers import searcher


@app.route('/', methods=['GET', 'POST'])
def index():
    """Return the basics as a test."""
    form = SearchForm()

    if request.method == 'POST' and form.validate():
        breed_type = request.form['breed_type']
        location = request.form['location']
        results = searcher(breed_type=breed_type, location=location)
        result_dict = {'results': results,
                       'location': location,
                       'breed_type': breed_type,
                       'breed_urls': BREED_URLS}
        return render_template("results.html", **result_dict)
    else:
        return render_template('landing.html', form=form)


@app.route('/about', methods=['GET'])
def about():
    """Return the 'about' view."""
    return render_template('about.html')
