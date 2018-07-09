"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
import re

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)

__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}

class WebViewTests(TestCase):
    def test_loads_correctly(self):
        """
        Tests that the homepage loads correctly
        """
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_basic_html(self):
        """
        Tests that the title attribute is set to 'Psywerx', the page contains an element
        with the class jumbatron, contains no empty paragraphs and that charset is utf-8
        """    
        response = self.client.get('')
        
        correct_title = False
        if "<title>Psywerx</title>" in response.content.replace(" ", ""):
            correct_title = True
        self.assertIs(correct_title, True)

        has_jumbatron = False
        if 'class="jumbotron"' or "class='jumbotron'" in response.content.replace(" ", ""):
            has_jumbatron = True
        self.assertIs(has_jumbatron, True)

        has_empty_paragraphs = False
        if re.search(r'<p>(\n*)</p>', response.content.replace(" ", "")):
            has_empty_paragraphs = True
        self.assertIs(has_empty_paragraphs, False)

        has_utf = False
        if "charset='utf-8'" or 'charset="utf-8"' in response.content.replace(" ", ""):
            has_utf = True
        self.assertIs(has_utf, True)