"""Store the views."""

from flask import redirect, request, render_template, url_for

from find_a_doggo.breed_urls import BREED_URLS
from find_a_doggo import app
from find_a_doggo.forms import SearchForm
from find_a_doggo.helpers import searcher


@app.route('/', methods=['GET', 'POST'])
def index():
    """Redirect to 'found' if valid form; render landing page otherwise."""
    form = SearchForm()

    if request.method == 'POST' and form.validate():
        breed_type = request.form['breed_type']
        location = request.form['location']
        return redirect(url_for('dogs',
                                location=location,
                                breed_type=breed_type))
    else:
        return render_template('landing.html', form=form)


@app.route('/dogs', methods=['GET'])
def dogs():
    """Return the found results."""
    breed_type = request.args.get('breed_type')
    location = request.args.get('location')
    results = searcher(breed_type=breed_type,
                       location=location)
    return render_template('results.html',
                           results=results,
                           breed_urls=BREED_URLS)


@app.route('/about', methods=['GET'])
def about():
    """Return the 'about' view."""
    return render_template('about.html')
