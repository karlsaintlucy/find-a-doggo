"""Store the helper functions for find_a_doggo."""

import dateutil.parser
import json
import os
import random
import re

from urllib.parse import quote, urlencode, urljoin

import requests

from bs4 import BeautifulSoup

from find_a_doggo.breed_lists import BREED_LISTS

API_KEY = os.environ['API_KEY']


def get_akc_breeds():
    """Snag AKC's breed list from the drop-down list of breeds."""
    r = requests.get('https://www.akc.org/dog-breeds/')
    html = r.content
    soup = BeautifulSoup(html, 'html.parser')
    select = soup.find('select')

    akc_breeds = []
    for option in select.find_all('option'):
        breed = option.text
        akc_breeds.append(breed)
        # print(breed)

    return akc_breeds


def get_petfinder_breeds():
    """Get Petfinder's breeds using the API's built-in method."""
    # https://www.petfinder.com/developers/api-docs
    api_url = 'http://api.petfinder.com/'
    api_method = 'breed.list'
    method_url = urljoin(api_url, api_method)
    options = {
        'key': API_KEY,
        'animal': 'dog',
        'format': 'json'
    }

    r = requests.get(method_url, params=options)
    breeds_json = r.json()

    petfinder_breeds = []
    for breed in breeds_json['petfinder']['breeds']['breed']:
        petfinder_breeds.append(breed['$t'])

    return petfinder_breeds


def crossreference_breed_lists():
    """Compare Petfinder's breed list and the AKC's."""
    akc_breeds = get_akc_breeds()
    petfinder_breeds = get_petfinder_breeds()

    included = []
    not_included = []
    for breed in petfinder_breeds:
        if breed in akc_breeds:
            included.append(breed)
        else:
            not_included.append(breed)

    # This returns a list of the Petfinder breeds that are and are not
    # listed or are formatted differently in the AKC breed list.
    return {'included': included, 'not_included': not_included}


def get_random_breed(breedset):
    """Randomize a breed from a given breedset."""
    random_breed = random.choice(breedset)
    return random_breed


def get_random_dogs(dogs_found, qty):
    """Randomize qty dogs from the set of results."""
    random_dogs = random.sample(dogs_found, qty)
    return random_dogs


# https://stackoverflow.com/questions/250357/truncate-a-string-without-ending-in-the-middle-of-a-word
def smart_truncate(content, length=100, suffix='…'):
    """Truncate the long dog description into preview text."""
    # This is designed to not cut off the text in the middle of a word.
    if content:
        if len(content) <= length:
            return content
        else:
            return content[:length].rsplit(' ', 1)[0] + suffix


def make_email_subject(dog_name, petfinder_id):
    """Make a mailto friendly subject line for the Email button."""
    # This includes the name of the dog and the Petfinder ID
    # so users are set up for success when they write the shelter.
    subject_string = f'Inquiry about {dog_name}, Petfinder ID #{petfinder_id}'
    subject = {'subject': subject_string}
    url_safe_subject = urlencode(subject, quote_via=quote)
    return url_safe_subject


def format_phone(phone_given):
    """Format phone numbers so they are ready to use in a tel: uri."""
    # The "results" page provides links to call and email the shelter,
    # so the phone numbers need to be formatted so that they can be
    # put in an <a> as a "tel:+1XXXXXXXXXX" href.
    digit_list = [n for n in re.findall(r'\d+', phone_given)]
    base_number = ''.join(digit_list)
    formatted_number = '+1' + base_number
    return formatted_number


def decode_results(r):
    """Grab the results and decode them as UTF-8."""
    # Petfinder sends results encoded in ISO-8859-1, which results in
    # a lot of wonky characters. This should fix that.
    results = r.text
    results_iso88591 = results.encode('iso-8859-1')
    results_utf8 = results_iso88591.decode('utf-8')
    results_utf8_json = json.loads(results_utf8)
    return results_utf8_json


def searcher(breed_type, location, qty=12):
    """Snag results from the Petfinder API."""
    # https://www.petfinder.com/developers/api-docs
    api_url = 'http://api.petfinder.com/'
    api_method = 'pet.find'
    method_url = urljoin(api_url, api_method)
    options = {
        'key': API_KEY,
        'animal': 'dog',
        'location': location,
        # 'count' specifies the number of dogs the API will return per breed.
        # The default is 25, which makes Find a Doggo run quite slowly.
        'count': 2,
        'format': 'json',
        'output': 'full',
        'breed': None
    }

    breed_list = BREED_LISTS[breed_type]

    # accommodate for protector breeds option
    dogs_found = []

    for breed in breed_list:
        options['breed'] = breed
        r = requests.get(method_url, params=options)
        if r:
            breed_results = decode_results(r)

        if breed_results:
            if 'pet' in breed_results['petfinder']['pets']:
                for pet in breed_results['petfinder']['pets']['pet']:
                    pet_name = pet['name']['$t']
                    pet_id = pet['id']['$t']

                    # Snag the dog's breeds.
                    breeds = []
                    # (it'll be a dict if it's only one breed)
                    if isinstance(pet['breeds']['breed'], dict):
                        breeds.append(pet['breeds']['breed']['$t'])
                    elif isinstance(pet['breeds']['breed'], list):
                        breeds = []
                        for item in pet['breeds']['breed']:
                            breeds.append(item['$t'])

                    # Handle the description and make a short one for the card.
                    description = pet['description']['$t'] if '$t' in \
                        pet['description'] else ''
                    if description:
                        short_description = smart_truncate(description)
                    else:
                        short_description = ''

                    # https://stackoverflow.com/questions/7271482/
                    # python-getting-a-list-of-value-from-list-of-dict
                    if 'photos' in pet['media']:
                        photo = [d['$t'] for d in
                                 pet['media']['photos']['photo']
                                 if d['@size'] == 'x'][0]

                    # Contact stuff
                    if '$t' in pet['contact']['phone']:
                        phone_given = pet['contact']['phone']['$t']
                        phone = format_phone(phone_given)
                    else:
                        phone = ''
                    if '$t' in pet['contact']['email']:
                        email = pet['contact']['email']['$t']
                        email_subject = make_email_subject(pet_name, pet_id)
                    else:
                        email = ''

                    # Build the address
                    address = ''
                    if '$t' in pet['contact']['address1']:
                        address += pet['contact']['address1']['$t']
                    if '$t' in pet['contact']['address2']:
                        address += ' ' + pet['contact']['address2']['$t']
                    if '$t' in pet['contact']['city']:
                        address += ' ' + pet['contact']['city']['$t']
                    if '$t' in pet['contact']['state']:
                        address += ', ' + pet['contact']['state']['$t']
                    if '$t' in pet['contact']['zip']:
                        address += ' ' + str(pet['contact']['zip']['$t'])

                    # Make a City, State for the card
                    if '$t' in pet['contact']['city']:
                        if '$t' in pet['contact']['state']:
                            city_state = (pet['contact']['city']['$t'] + ', ' +
                                          pet['contact']['state']['$t'])

                    # last_update = last time the record was updated.
                    last_update = dateutil.parser.parse(
                        pet['lastUpdate']['$t'])
                    last_update_hreadable = last_update.strftime('%b %m, %Y')

                    # Bring everything together
                    dog = {'name': pet_name,
                           'breeds': breeds,
                           'petfinder_id': pet_id,
                           'description': description,
                           'short_description': short_description,
                           'photo': photo,
                           'phone': phone,
                           'email': email,
                           'address': address,
                           'city_state': city_state,
                           'last_updated': last_update_hreadable,
                           'email_subject': email_subject}

                    # Append the results
                    if dog not in dogs_found:
                        dogs_found.append(dog)

    random_dogs = get_random_dogs(dogs_found, qty)
    results = list(random_dogs)

    return results


if __name__ == '__main__':
    searcher(location=10001, qty=12, breed_type='chill')
