from django.test import TestCase
from django.urls import reverse


class HomeViewTests(TestCase):
    def test_home_page_renders(self):
        response = self.client.get(reverse("assessment:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "LLM Assessment in Indian Context")
