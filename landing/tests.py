from django.test import TestCase
from django.urls import reverse

class LandingPageTest(TestCase):
    def test_register_page_accessible_from_landing(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertIn(response.status_code, [200, 302])

    def test_login_page_accessible_from_landing(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertIn(response.status_code, [200, 302])

    def test_landing_page_status_code(self):
        response = self.client.get(reverse('landing:landing'))
        self.assertEqual(response.status_code, 200)

    def test_landing_page_template(self):
        response = self.client.get(reverse('landing:landing'))
        self.assertTemplateUsed(response, 'landing/index.html')

    def test_landing_page_content(self):
        response = self.client.get(reverse('landing:landing'))

        self.assertContains(response, 'Minium')
        self.assertContains(response, 'Get started')
        self.assertContains(response, 'Sign in')
        self.assertContains(response, 'Start reading')
