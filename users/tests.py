from datetime import timedelta
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.models import EmailVerification, User


class UserRegistrationViewTestCase(TestCase):

    def setUp(self):
        self.path = reverse('users:registration')
        self.test_user_data = {
            'first_name': 'Vlad',
            'last_name': 'Ivanovskiy',
            'username': 'vlad',
            'email': 'vladislav@gmail.com',
            'password1': '12345678aA',
            'password2': '12345678aA'
        }

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'HAVEN - Регистрация')
        self.assertTemplateUsed(response, 'users/registration.html')

    def test_user_registration_post_success(self):
        # user creation checking
        username = self.test_user_data.get('username')
        self.assertFalse(User.objects.filter(username=username).exists())

        response = self.client.post(self.path, self.test_user_data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=username).exists())

        # email verification checking
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())
        self.assertEqual(
            email_verification.first().expiration.date(),
            (now() + timedelta(hours=48)).date()
        )

    def test_user_registration_post_error(self):
        username = self.test_user_data.get('username')
        email = self.test_user_data.get('email')
        User.objects.create(username=username)
        User.objects.create(email=email)

        response = self.client.post(self.path, self.test_user_data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.', html=True)
        self.assertContains(response, 'User с таким Email уже существует.', html=True)
