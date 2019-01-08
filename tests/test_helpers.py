"""Implement unit tests for functions in helpers.py."""


import unittest

from bs4 import BeautifulSoup
import requests


class GetAkcBreedsTest(unittest.TestCase):
    """Check that everything required to get AKC breeds works."""

    def setUp(self):
        """Grab the HTML from the AKC so we only have to get once."""
        self.response = requests.get('https://www.akc.org/dog-breeds/')

    def extract_content(self, response):
        """Extract content from the requests response."""
        content = response.content
        return content

    def soupify(self, response):
        """Parse HTML into a usable BeautifulSoup object."""
        content = self.extract_content(response)
        soup = BeautifulSoup(content, 'html.parser')
        return soup

    def test_akc_breeds_are_accessible(self):
        """Test that there is a response from the AKC website."""
        self.assertIsNotNone(self.response)

    def test_response_returns_content(self):
        """Test that the response contains a content attribute."""
        content = self.extract_content(self.response)
        self.assertIsNotNone(content)

    def test_beautiful_soup_can_parse_html_from_returned_content(self):
        """Test that Beautiful Soup can parse HTML from the returned content."""
        soup = self.soupify(self.response)
        self.assertIsNotNone(soup)

    def test_soup_contains_select_element(self):
        """Test that Beautiful Soup finds a 'select' element in the response from AKC."""
        soup = self.soupify(self.response)
        select = soup.find('select')
        self.assertIsNotNone(select)

    def test_select_contains_more_than_zero_options(self):
        """Test that the select element from AKC contains at least one option."""
        soup = self.soupify(self.response)
        select = soup.find('select')
        options = select.find_all('option')
        options_count = len(options)
        self.assertGreater(options_count, 0)

    def test_select_does_not_contain_helper_text(self):
        """Test that select doesn't return 'Select a Breed' from the list of options."""
        soup = self.soupify(self.response)
        select = soup.find('select')
        options = select.find_all('option')
        options = [option.text for option in options
                   if option.text.lower() != 'select a breed']
        self.assertNotIn('Select A Breed', options)


if __name__ == '__main__':
    unittest.main()
