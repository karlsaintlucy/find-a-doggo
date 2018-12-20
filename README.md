# :dog2: Findadoggo.com
## A simple [Flask](http://flask.pocoo.org/)- and [Bootstrap](https://getbootstrap.com/)-driven web app that finds dogs near a given location by breed characteristics using the [Petfinder API](https://www.petfinder.com/developers/api-docs).

*****

### Known Quirks
* The application runs quite slowly. Unfortunately, the API only accepts one breed per query; however, the `searcher()` function in `helpers.py` can probably be optimized.
* The API's result set returns dogs that are often quite far away from the given ZIP code. This may be due to the algorithm used to fetch results from the API (see the `searcher()` function in `helpers.py`).
* At present, the modals that show up for each dog when "more" is clicked only apply anchors to breeds that appear in one of the breed category lists (i.e., "chill," "protective," and "at-risk"). See `helpers.py` for some additional functions that pull the complete lists of breeds available — both from the [Petfinder API](https://www.petfinder.com/developers/api-docs) and the [American Kennel Club](https://www.akc.org/) — and an additional function, `crossreference_breed_lists()`, that returns a `dict` of the Petfinder breeds that appear in the AKC's list. **Note** that some of these discrepancies are due to differences in formatting syntax between Petfinder and the AKC; others are due to the fact that the AKC does not officially recognize every breed (e.g., Jack Russell Terriers).
* The Petfinder API returns JSON results in ISO-8859-1 encoding. The `decode_results()` function in `helpers.py` takes care of the character set discrepancies between ISO-8859-1 and Unicode in most cases, but this hasn't been fully tested. It appears that most wonky text formatting issues are due to user error on Petfinder's end.
* The "Location" text field undergoes regular expression validation (must be a 5-digit sequence of numbers) and a validator against `uszipcode`'s database of valid ZIP codes to determine whether the data can be sent to the application. If the data fails both validators, the application returns two errors, which are somewhat redundant.

### Planned To-Dos
* Add a preloader to `lander.html` so it's clear the app is running after "Submit" is clicked.
* Allow users to select the number of results to return.
* Implement session tracking so that users don't have to pass the reCAPTCHA for every search.
* Display phone numbers on modals in a more human-readable format (e.g., "(123) 456-7890").
* Save the breed info in a database instead of bare `.py` files, and develop functionality to update the databases against any changes in the Petfinder or AKC lists.
* Implement front-end form validation.
* Build a `/results` view so that the domain root always points to the landing page.
* Factor out the redundant code in the Jinja templates so they can inherit from `base.html`.

**Findadoggo.com** was first deployed on [Heroku](https://www.heroku.com/) by following [John Kagga](https://medium.com/@johnkagga)'s guide, [Deploying a Python Flask app on Heroku](https://medium.com/the-andela-way/deploying-a-python-flask-app-to-heroku-41250bda27d0), published in [The Andela Way](https://medium.com/the-andela-way) on [Medium](https://medium.com/).
