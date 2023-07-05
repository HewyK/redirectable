from datetime import timezone
from django.test import TestCase, Client
from django.urls import reverse
import core.models as models

class MyViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.my_model = models.Redirects.objects.create(user=1, url_from='Test.com', url_to='Test2.com', http_https='http')

    def test_my_view(self):
        response = self.client.get(reverse('my_view'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.my_model.url_from)
        self.assertContains(response, self.my_model.url_to)
        self.assertContains(response, self.my_model.http_https)

    def test_my_model(self):
        self.assertEqual(self.my_model.url_from, 'Test.com')
        self.assertEqual(self.my_model.url_to, 'Test2.com')
        self.assertEqual(self.my_model.http_https, 'http')