from django.test import TestCase
from django.urls import reverse
from .models import User

class RegisterPageTest(TestCase):
    def setUp(self):
        self.valid_user = {
            'email': 'email@email.com',
            'username': 'username',
            'password': 'password',
            'month': 12,
            'day': 27,
            'year': 2000
        }

    def test_register_valid_user(self):
        response = self.client.post(reverse('accounts:register'), self.valid_user)

        self.assertRedirects(response, reverse('blog:home'))
        self.assertTrue(User.objects.filter(email=self.valid_user.get('email')).exists())

    def test_register_invalid_user(self):
        data = self.valid_user.copy()
        data['year'] = 'invalid'

        response = self.client.post(reverse('accounts:register'), data)

        self.assertRedirects(response, reverse('accounts:register'))
        self.assertFalse(User.objects.filter(email=self.valid_user.get('email')).exists())

    def test_register_duplicate_user(self):
        User.objects.create_user(
            email=self.valid_user.get('email'),
            username=self.valid_user.get('username'),
            password=self.valid_user.get('password')
        )

        response = self.client.post(reverse('accounts:register'), self.valid_user)
        self.assertRedirects(response, reverse('accounts:register'))

    def test_register_page_template(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_page_content(self):
        response = self.client.get(reverse('accounts:register'))

        self.assertContains(response, 'Join Minium')
        self.assertContains(response, 'Sign up')
        self.assertContains(response, 'Sign in')

class LoginPageTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='email@email',
            username='username',
            password='password'
        )

    def test_login_with_valid_credentials(self):
        response = self.client.post(reverse('accounts:login'), {
            'email': self.user.email,
            'password': 'password'
        })
        self.assertRedirects(response, reverse('blog:home'))

    def test_login_with_invalid_credentials(self):
        response = self.client.post(reverse('accounts:login'), {
            'email': self.user.email,
            'password': 'pass_word'
        })
        self.assertRedirects(response, reverse('accounts:login'))

    def test_login_page_template(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_page_content(self):
        response = self.client.get(reverse('accounts:login'))

        self.assertContains(response, 'Welcome back')
        self.assertContains(response, 'Sign in')
        self.assertContains(response, 'Create one')

class LogoutTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='email@email',
            username='username',
            password='password'
        )
        self.client.login(email=self.user.email, password='password')

    def test_logout_user(self):
        response = self.client.get(reverse('accounts:logout'))
        self.assertRedirects(response, reverse('accounts:login'))
