from django.test import TestCase, SimpleTestCase

# Create your tests here.


class SimpleTests(SimpleTestCase):
    def test_landingPage_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)