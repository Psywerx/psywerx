"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase

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
        self.assertIn('<h1>Psywerx</h1>', response.content)

    def test_basic_html(self):
        """
        Tests that the title attribute is set to 'Psywerx', the page contains an element
        with the class jumbatron, contains no empty paragraphs and that charset is utf-8
        """    
        response = self.client.get('')
        html_content = response.content
        
        self.assertIn('<title>Psywerx</title>', html_content)
        
        self.assertIn('<div class="jumbotron">', html_content)
        
        self.assertIn('<meta charset="utf-8">', html_content)

    def test_wrong_url(self):
        """
        Tests that trying to reach an url that doesn't exist results in 
        404.html loading
        """
        response = self.client.get('/nonexistenturl')
        self.assertContains(response, 'The force is wrong with your url...')