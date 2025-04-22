from django.test import TestCase, Client
from django.urls import reverse

class HomeViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view_renders_correct_template(self):
        response = self.client.get(reverse('home:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/index.html")
